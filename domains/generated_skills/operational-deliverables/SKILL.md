---
name: operational-deliverables
description: Use when packaging operational software into a structured deliverables directory with separated BIN/DOC/SRC/OTHER categories, MD5 integrity verification files, and compressed source archives for field deployment.
---

# Operational Deliverables Packaging

## Overview

Makefile-driven packaging system that creates a structured deliverables directory for field deployment. Separates binaries, documentation, source code, and other assets into distinct directories with MD5 integrity verification files alongside each artifact.

## Directory Structure

```
deliverables/
├── BIN/
│   ├── cutthroat                    # Operator interface binary
│   ├── cutthroat.md5                # MD5 integrity check
│   ├── hive                         # ILM shared library
│   ├── hive.md5
│   ├── CCS.xml                      # Command set definition
│   ├── hive-patcher                 # Binary patcher tool
│   ├── hive-patcher.md5
│   ├── honeycomb.py                 # Beacon management gateway
│   ├── honeycomb.py.md5
│   ├── hiveReset_v1_0.py            # Remote timer reset tool
│   ├── server.key                   # SSL certificate
│   ├── server.crt
│   ├── ca.crt
│   └── unpatched/                   # Platform-specific implant binaries
│       ├── hived-linux-x86-unpatched
│       ├── hived-linux-x86-unpatched.md5
│       ├── hived-mikrotik-mips-unpatched
│       ├── hived-mikrotik-mips-unpatched.md5
│       └── ...
├── DOC/
│   ├── UsersGuide.pdf               # End-user documentation
│   └── ...
├── SRC/
│   └── hive.tar.bz2                 # Compressed source archive
└── OTHER/
    └── ...
```

## Makefile Implementation

```makefile
.PHONY: deliverables
deliverables: remove-deliverables tarball
    printf "Packaging Deliverables, please wait ...\n"
    mkdir -p deliverables/BIN
    mkdir -p deliverables/DOC
    mkdir -p deliverables/SRC
    mkdir -p deliverables/OTHER

    # Source archive
    bzip2 -fc hive.tar > deliverables/SRC/hive.tar.bz2

    # Operator binaries
    cp -a ilm-client/CCS.xml* deliverables/BIN
    cp -a ilm-client/cutthroat* deliverables/BIN
    cp -a ilm-client/hive deliverables/BIN
    cp -a ilm-client/hive.md5 deliverables/BIN
    cp -a client/hive-patcher deliverables/BIN
    cp -a client/hive-patcher.md5 deliverables/BIN

    # Tools
    cp -a ilm-client/resetTimer_v1.0/hiveReset_v1_0.py deliverables/BIN
    cp -a honeycomb/honeycomb.py deliverables/BIN
    md5sum honeycomb/honeycomb.py > deliverables/BIN/honeycomb.py.md5

    # SSL certificates
    cp -a ilm-client/server.key deliverables/BIN
    cp -a ilm-client/server.crt deliverables/BIN
    cp -a ilm-client/ca.crt deliverables/BIN

    # Unpatched binaries with MD5
    mkdir -p deliverables/BIN/unpatched
    cp -aL client/hived-*-*-unpatched deliverables/BIN/unpatched
    (cd deliverables/BIN/unpatched; for i in *; do md5sum $$i > $$i.md5; done)

    # Documentation
    cp -a documentation/UsersGuide/* deliverables/DOC/
```

## MD5 Integrity Verification

```bash
# Generate MD5 for each artifact
md5sum honeycomb.py > honeycomb.py.md5

# Batch generate for unpatched binaries
cd deliverables/BIN/unpatched
for i in *; do md5sum $i > $i.md5; done
```

## Source Archive Creation

```makefile
.PHONY: tarball
tarball:
    tar --exclude=.svn \
        --exclude=*.o \
        --exclude=*.a \
        --exclude=*.md5 \
        --exclude=*.gz \
        --exclude=*.tar \
        --exclude=*.tgz \
        --exclude=snapshot_* \
        --exclude=documentation/html/* \
        -cvf hive.tar *
```

## Cleaning

```makefile
.PHONY: remove-deliverables
remove-deliverables:
    rm -rf deliverables
```

## Constraints

- MUST generate MD5 files for all binary artifacts in BIN/
- MUST separate source (SRC), binaries (BIN), documentation (DOC), and other (OTHER)
- MUST exclude build artifacts (.o, .a, .svn) from source tarball
- MUST exclude snapshot directories from source tarball
- MUST use bzip2 compression for source archive (not gzip)
- SHOULD regenerate deliverables from scratch (remove-deliverables first)
- MUST include SSL certificates with restricted permissions
- ALWAYS verify MD5 integrity before deploying to target
