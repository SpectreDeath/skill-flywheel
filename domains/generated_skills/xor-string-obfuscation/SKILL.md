---
name: xor-string-obfuscation
description: "Use when: hiding sensitive strings (debug messages, error text, IP addresses, file paths) from binary analysis by XOR-encoding at build time and decoding at runtime. Triggers: 'obfuscate strings', 'hide strings', 'XOR encode', 'string encryption', 'anti-reverse engineering'. NOT for: protecting data at runtime in memory (use encryption), or when performance overhead is unacceptable."
---

# XOR String Obfuscation Pipeline

## Overview

Build-time + runtime string obfuscation system. Python scripts transform plaintext `#define` strings into XOR-encoded hex arrays. At runtime, an `init_strings()` function decodes all strings back to plaintext. Prevents static analysis from revealing sensitive strings in the binary.

## Pipeline

```
Build Time:
  project_strings.source.h        (plaintext #define FOO "sensitive string")
       |
  mod_hexify.py                   (XOR encode string to hex array)
       |
  mod_gen_string_header.py        (generate C headers + init function)
       |
  proj_strings.h                  (extern declarations only -- no plaintext)
  proj_strings_main.h             (hex array definitions)
  init_strings.c                  (init_strings() calls cl_string() for each)
  crypto_proj_strings.h           (crypto-specific variant)

Runtime:
  main() -> init_strings() -> cl_string(SRV_CERT_FILE, sizeof(SRV_CERT_FILE))
                               -> cl_string(BEACON_IP, sizeof(BEACON_IP))
                               -> ... all strings decoded in-place
```

## Build-Time: Python Hexification

```python
# mod_hexify.py - XOR encode string with per-character key
def obfs(string, flag):
    hex_string = "{ "
    for char in string:
        encoded = ord(char) ^ ord(flag)  # XOR with flag byte
        hex_string += "0x%02x, " % encoded
    hex_string += "0x00 }"  # null terminator
    return hex_string, len(string) + 1
```

## Generated Header Pattern

```c
// proj_strings.h -- only declarations, no plaintext
extern unsigned char SRV_CERT_FILE[15];
extern unsigned char BEACON_IP[20];

// init_strings.c -- decode function
void init_strings() {
    cl_string(SRV_CERT_FILE, 15);
    cl_string(BEACON_IP, 20);
    // ... one line per string
}

// proj_strings_main.h -- hex arrays (in source, not linked)
unsigned char SRV_CERT_FILE[] = { 0x32, 0x65, 0x72, ... };
```

## Runtime: cl_string() Decode

```c
// In-place XOR decode -- same XOR operation encodes and decodes
void cl_string(unsigned char *str, int len) {
    for (int i = 0; i < len - 1; i++) {
        str[i] ^= XOR_FLAG;  // XOR with same key to decode
    }
}
```

## Crypto-Specific Variant

A separate pipeline (`mod_gen_cryptostring_header.py`) generates `crypto_proj_strings.h` for cryptographic constants (DH parameters, personalization strings). This separation ensures crypto strings have different XOR keys from operational strings.

## Usage Pattern

```c
int main(int argc, char **argv) {
    init_strings();  // Decode all strings at startup
    // Now SRV_CERT_FILE contains "/path/to/server.crt"
    load_certificate(SRV_CERT_FILE);
    // ...
}
```

## Constraints

- MUST call `init_strings()` before any string is accessed
- MUST NOT reference obfuscated strings in `const` or `static` initializers -- they aren't decoded yet
- XOR key should differ between operational strings and crypto strings (separate pipelines)
- SHOULD use the generated `proj_strings.h` (extern declarations) in all source files, never the `_main.h` variant
- MUST ensure null terminator is included in the hex array and decode length
- ALWAYS verify decoded string length matches expected value after decode
- NEVER log decoded strings in production builds -- defeats the purpose
