---
name: beacon-management-gateway
description: Use when building a Python beacon management gateway that receives encrypted implant check-ins, parses custom binary protocols (BTHP), decrypts XTEA-encrypted data, and generates XML report files (RSI) for downstream processing.
---

# Beacon Management Gateway (Honeycomb BTHP)

## Overview

Python-based TCP listener that accepts beacon connections from implants, handles a custom binary protocol (BTHP), manages XTEA encryption key exchange, parses beacon payloads containing system survey data, and writes structured XML (RSI) files.

## Protocol Stack

```
[TCP Connection]
       |
  [BTHP Header]        -- Beacon Transport Header Protocol
       |
  [Random Key Exchange] -- 32 bytes each direction, XOR-derived key
       |
  [XTEA Encrypted Data] -- 32-round ECB mode, 8-byte blocks
       |
  [Beacon Payload]      -- Version + OS + type/length data fields
```

## BTHP Header Format

```python
BTHP_HDR_FMT = '>BBHII'  # Big-endian: version(u8), type(u8), hdrLen(u16), dataLen(u32), proxyId(u32)
BTHP_ADDL_HDR_FMT = '>BB' # type(u8), len(u8)

# Additional header types:
#   type=2: beacon IP (4 bytes)
#   type=3: destination IP (4 bytes)
#   type=6: proxy IP (4 bytes)
```

## Key Exchange

```python
XOR_KEY = 5

def create_key(rand_bytes):
    # Extract 16-byte XTEA key from 32 random bytes
    offset = (ord(rand_bytes[0]) ^ XOR_KEY) % 15
    return rand_bytes[(offset+1):(offset+17)]
```

## XTEA Decryption

```python
def xtea_decrypt(key, block, n=32, endian="!"):
    v0, v1 = struct.unpack(endian+"2L", block)
    k = struct.unpack(endian+"4L", key)
    delta, mask = 0x9e3779b9, 0xffffffff
    sum = (delta * n) & mask
    for round in range(n):
        v1 = (v1 - (((v0<<4 ^ v0>>5) + v0) ^ (sum + k[sum>>11 & 3]))) & mask
        sum = (sum - delta) & mask
        v0 = (v0 - (((v1<<4 ^ v1>>5) + v1) ^ (sum + k[sum & 3]))) & mask
    return struct.pack(endian+"2L", v0, v1)
```

## Beacon Data Fields

```python
# Type-length encoded fields in decrypted beacon payload
BEACON_FIELDS = {
    1: 'mac',           # MAC address
    2: 'uptime',        # System uptime
    3: 'proc_list',     # Process list (ps -ef)
    4: 'ipconfig',      # Network configuration (ifconfig)
    5: 'netstat_rn',    # Routing table (netstat -rn)
    6: 'netstat_an',    # Active connections (netstat -an)
    7: 'next_beacon',   # Time until next beacon
}

# OS detection codes
OS_CODES = {
    10: "Windows", 20: "Linux-x86",
    30: "Solaris-SPARC", 31: "Solaris-x86",
    40: "MikroTik-MIPS", 41: "MikroTik-MIPSEL",
    42: "MikroTik-x86", 43: "MikroTik-PPC",
    50: "Ubiquiti-MIPS", 61: "AVTech-ARM",
}
```

## Connection Flow

```python
def listen_for_beacons(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        # 1. Receive first packet (32 bytes = v1, larger = v2)
        data = conn.recv(4096)
        parse_bthp_packet(data)

        # 2. Detect version from payload size
        is_v1 = len(data[offset:]) == 32

        # 3. Generate and send 32 random bytes for key exchange
        rand_bytes = os.urandom(32)
        key = create_key(rand_bytes)
        packet = create_return_packet(rand_bytes)
        conn.send(packet)

        # 4. Process beacon based on version
        if is_v1:
            process_ver1_beacon(conn, key)
        else:
            process_ver2_beacon(conn, key, packet_size)
        conn.close()
```

## v2 Chunked Reception

```python
MAX_CHUNK_SIZE = 4052

def process_ver2_beacon(conn, key, packet_size):
    received = 0
    data = ''
    while received < packet_size:
        chunk = conn.recv(min(MAX_CHUNK_SIZE + 44, packet_size - received + 44),
                         socket.MSG_WAITALL)
        parse_bthp_packet(chunk)
        data += chunk[offset:]
        received += len(chunk[offset:])
        send_ack(conn, len(chunk[offset:]))  # ACK-based flow control

    decrypted = decrypt_data(key, data)
    parse_beacon_data(decrypted)
```

## RSI XML Output

```python
def write_rsi_file(beacon_data):
    # Generates timestamped .rsi XML files:
    # <ToolHandlerFile version="1.0">
    #   <header>
    #     <ID>MAC_WITHOUT_DASHES</ID>
    #     <IP>PROXY_IP</IP>
    #     <toolHandlerID>88</toolHandlerID>
    #   </header>
    #   <beacon>
    #     <deviceStats>...</deviceStats>
    #     <MACAddress>...</MACAddress>
    #     <extraData label="os">Linux-x86</extraData>
    #     <extraData label="processList">...</extraData>
    #   </beacon>
    # </ToolHandlerFile>
```

## Constraints

- MUST handle both v1 (32-byte) and v2 (chunked) beacon formats
- MUST use big-endian byte order for all BTHP protocol fields
- MUST parse all BTHP additional headers before accessing payload data
- MUST send ACK after each v2 chunk for flow control
- SHOULD use `select.select()` for non-blocking I/O
- MUST validate BTHP header length before attempting unpack
- MUST log all parsing errors with source IP for forensics
- ALWAYS close connection after beacon processing completes
