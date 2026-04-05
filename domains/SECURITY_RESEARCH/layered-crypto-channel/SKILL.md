---
name: layered-crypto-channel
description: "Use when: implementing encrypted network communications with defense-in-depth using multiple cryptographic layers. Triggers: 'layered encryption', 'crypto channel', 'defense in depth', 'key exchange', 'symmetric encryption'. NOT for: single-layer encryption (use standard TLS), or when performance is critical."
---

# Layered Cryptographic Channel

## Overview

Three-layer encryption pattern for network communications: TLS for transport security, Diffie-Hellman for forward-secret key agreement, and AES-256-CBC for application-level encryption.

## Stack Architecture

```
[Application Data]
       |
  [AES-256-CBC]      <-- Layer 3: Application encryption with DH-derived key
       |
  [Diffie-Hellman]    <-- Layer 2: Key exchange over established TLS
       |
  [TLS/SSL]           <-- Layer 1: Transport security
       |
  [TCP Socket]
```

## Implementation Pattern

### Layer 1: TLS Handshake

```c
// Server setup
ssl_set_endpoint(ssl, SSL_IS_SERVER);
ssl_set_own_cert(ssl, &srvcert, &rsa);
ssl_set_ca_chain(ssl, &ca_chain, NULL, NULL);
ssl_set_dh_param(ssl, dhm_P, dhm_G);
ssl_handshake(ssl);

// Client setup
ssl_set_endpoint(ssl, SSL_IS_CLIENT);
ssl_set_authmode(ssl, SSL_VERIFY_NONE);
ssl_handshake(ssl);
```

### Layer 2: Diffie-Hellman Key Exchange

```
Server:                                         Client:
  dhm_make_params(dhm, keylen, buf) --->
         (P, G, Ys=G^Xs mod P, RSA_sig)
                                                dhm_read_params(dhm, &p, end)
                                                dhm_make_public(dhm, keylen, buf)
                          <--- (Yc=G^Xc mod P)
  dhm_read_public(dhm, buf, len)
  dhm_calc_secret(dhm, buf, &n)
  K = Ys^Xc mod P                             K = Ys^Xc mod P
```

Use RFC 3526 MODP 2048-bit group for P and G parameters.

### Layer 3: AES-256-CBC Encryption

```c
// Derive IV from shared key
md5(shared_key, AES_KEY_SIZE, iv);

// Write: embed 2-byte length, pad to 16-byte boundary, encrypt
bufsize = ((size + 2) % 16) ? (size + 2) + (16 - (size + 2) % 16) : (size + 2);
encbuf[0] = (size >> 8);  // length high byte
encbuf[1] = size;          // length low byte
memcpy(encbuf + 2, buf, size);
aes_setkey_enc(aes_ctx, shared_key, AES_KEY_SIZE);
aes_crypt_cbc(aes_ctx, AES_ENCRYPT, bufsize, iv, encbuf, encbuf);
ssl_write(ssl, encbuf, bufsize);

// Read: decrypt, extract embedded length, copy data
ssl_read(ssl, encbuf, bufsize);
aes_setkey_dec(aes_ctx, shared_key, AES_KEY_SIZE);
aes_crypt_cbc(aes_ctx, AES_DECRYPT, received, iv, encbuf, encbuf);
actual_len = (encbuf[0] << 8) + encbuf[1];
memcpy(buf, encbuf + 2, actual_len);
```

## Key Management

- IV derived from MD5 hash of the shared DH secret (not sent separately)
- Length field embedded inside the encrypted payload (prevents traffic analysis of exact sizes)
- Padding to AES block boundary (16 bytes) handled transparently
- RNG seeded with CTR-DRBG using entropy context

## Constraints

- NEVER reuse IVs -- derive fresh IV from each new DH exchange
- MUST verify DH modulus size is within expected range (64-256 bytes)
- SHOULD use `SSL_VERIFY_NONE` only for implant-to-server; server must verify implant via Optional Client Authentication
- MUST zero-fill AES context on termination (`memset(ctx, 0, sizeof(aes_context))`)
- MUST free DHM context after key extraction
- ALWAYS check return codes from `ssl_read`/`ssl_write` for `WANT_READ`/`WANT_WRITE` retry conditions
