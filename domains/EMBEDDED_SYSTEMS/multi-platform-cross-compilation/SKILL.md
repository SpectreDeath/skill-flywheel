---
name: multi-platform-cross-compilation
description: "Use when: building C/C++ projects for multiple architectures (x86, ARM, MIPS, PPC) using cross-compilation toolchains. Triggers: 'cross-compile', 'multi-arch', 'Buildroot', 'ARM toolchain', 'embedded build'. NOT for: single-platform only (use native compilation), or when interpreted languages suffice."
---

# Multi-Platform Cross-Compilation Pipeline

## Overview

Build system pattern for compiling a single C codebase against multiple target architectures from a single build host. Uses hierarchical Makefiles with per-platform include files and Buildroot cross-compiler toolchains.

## Architecture

```
Makefile (top-level: clean, tarball, all targets)
  |
  +-- server/Makefile (delegates to Makefile.arch)
  |     |
  |     +-- Makefile.arch (architecture-agnostic build rules)
  |           |
  |           +-- common/Makefile-include.linux-x86
  |           +-- common/Makefile-include.mikrotik-mips
  |           +-- common/Makefile-include.avtech-arm
  |           +-- ...
  |
  +-- client/Makefile (client + patcher builds)
```

## Platform Configuration Template

Each `Makefile-include.<platform>` must define:

```makefile
# Cross-compiler prefix
CC := /opt/buildroot/.../bin/<arch>-linux-gcc
AR := /opt/buildroot/.../bin/<arch>-linux-ar
RANLIB := /opt/buildroot/.../bin/<arch>-linux-ranlib
STRIP := /opt/buildroot/.../bin/<arch>-linux-strip

# Architecture defines
CFLAGS += -D<PLATFORM> -D_<ARCH> -static
LDFLAGS += -static

# Debug level: 1=symbols, 2=platform-debug, 3=library-debug
CFLAGS += -DDEBUG_LEVEL=2
```

## Key Patterns

### 1. Architecture-Agnostic Source with Platform Guards

```c
#if defined MIKROTIK && defined _MIPS
    // MIPS BE specific code
#elif defined LINUX && defined _X86
    // x86 specific code
#endif
```

### 2. Packed Structures for Wire Formats

```c
struct __attribute__((packed)) wire_header {
    uint32_t sig;
    uint16_t port;
    // fields must use fixed-width types
};
```

### 3. Endianness Handling

```c
// Convert when targeting big-endian platforms (MIPS BE, PPC)
copy_of_args.beacon_port = htonl(copy_of_args.beacon_port);
copy_of_args.sig = htonl(copy_of_args.sig);
```

### 4. Static Linking with uClibc

All targets link statically against uClibc to avoid shared library dependencies on embedded targets.

## Build Flow

1. Platform Makefile-include sets CC/AR/RANLIB/STRIP to cross-compiler
2. Sets architecture defines (-DLINUX -D_X86, -DMIKROTIK -D_MIPS, etc.)
3. Links statically against uClibc
4. Each platform target produces a separate binary

## Supported Platforms Reference

| Platform | Arch | Cross-Compiler | Endianness |
|----------|------|----------------|------------|
| Linux x86 | i386 | i386-linux-gcc | Little |
| Linux x86_64 | x86_64 | x86_64-linux-gcc | Little |
| MikroTik MIPS | mips | mips-linux-gcc | Big |
| MikroTik PPC | powerpc | powerpc-linux-gcc | Big |
| Ubiquiti MIPS | mips | mips-linux-gcc | Big |
| AVTech ARM | arm | arm-linux-gcc | Little |

## Constraints

- NEVER mix host and target object files -- each platform must have isolated build artifacts
- ALWAYS use fixed-width integer types (uint8_t, uint16_t, uint32_t) in wire-format code
- MUST handle endianness conversion for big-endian targets
- SHOULD use `__attribute__((packed))` for on-wire structures
- MUST link statically for embedded targets without shared library support
