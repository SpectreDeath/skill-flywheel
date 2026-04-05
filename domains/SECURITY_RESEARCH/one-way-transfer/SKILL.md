---
name: one-way-transfer
description: "Use when: implementing automated one-way data exfiltration with file change detection and SWIFT upload. Triggers: 'data exfiltration', 'file monitoring', 'change detection', 'SWIFT upload', 'mtime tracking'. NOT for: bidirectional sync (use standard sync tools), or when local processing only."
---

# One-Way Transfer (OWT) Data Exfiltration

## Overview

Automated file transfer system that monitors directories for changed files (using mtime comparison), packages changed files into timestamped tar archives, and uploads them via SWIFT protocol. Uses pickle-based persistence for tracking modification times across runs.

## Architecture

```
[Monitored Directories]
       |
  mtime comparison (.hcOwt.data persistence)
       |
  changed files identified
       |
  cp to TRANSFER_DIR/YYYYMMDDHHMMSS/
       |
  tar cfz YYYYMMDDHHMMSS_name.tgz
       |
  swift_upload() via HTTP PUT to OWT feeder
       |
  persist new mtimes to .hcOwt.data
```

## Configuration

```ini
[config]
name:     beacon_logs          # Included in archive filename
feeder:   111.111.111.111      # OWT feeder IP
where:    somewhere             # OWT destination field
username: username              # SWIFT auth username
password: password              # SWIFT auth password

[owtDirectories]
/var/log/honeycomb: .           # path:archive_path mapping
/beacons:             beacons
```

## Change Detection

```python
PERSIST_FILE = ".hcOwt.data"

# Load previous mtimes
old = {}
if os.path.isfile(PERSIST_FILE):
    with open(PERSIST_FILE, 'rb') as f:
        old = cPickle.load(f)

# Scan directories for changes
new = {}
changed = []
for (dir, dest) in owtDirs:
    for file in os.listdir(dir):
        filePath = os.path.join(dir, file)
        if os.path.isfile(filePath):
            new[filePath] = os.stat(filePath)[stat.ST_MTIME]
            if (filePath not in old) or old[filePath] != new[filePath]:
                changed.append(filePath)
```

## Packaging and Upload

```python
# Create timestamped transfer directory
timeStr = "%04d%02d%02d%02d%02d%02d" % (NOW[0], NOW[1], NOW[2], NOW[3], NOW[4], NOW[5])
transferDir = os.path.join(TRANSFER_DIR, timeStr)

# Copy changed files maintaining directory structure
for file in changed:
    destPath = os.path.join(transferDir, name, dest)
    os.system("mkdir -p %s" % destPath)
    os.system("cp %s %s" % (file, destPath))

# Create archive
uploadFile = "%s_%s.tgz" % (timeStr, name)
os.system("tar cfz %s *" % uploadFile)

# Upload via SWIFT
swift.upload(uploadFile, username, password, uploadFile, where, feeder)

# Persist mtimes on success
with open(PERSIST_FILE, 'wb') as f:
    cPickle.dump(new, f, cPickle.HIGHEST_PROTOCOL)
```

## Logging

```python
# Rotating log file (500k max, 2 backups)
fileHandler = logging.handlers.RotatingFileHandler(
    "hcOwt.log", maxBytes=512000, backupCount=2)
LOGGER.addHandler(fileHandler)
```

## Constraints

- MUST persist mtimes only after successful upload (not before)
- MUST use cPickle with HIGHEST_PROTOCOL for mtime persistence
- MUST NOT recurse into subdirectories (top-level only)
- MUST handle missing directories gracefully (warn and continue)
- SHOULD use timestamped directory names to prevent collisions
- MUST exclude the OWT script itself from archives
- MUST rotate log files to prevent disk exhaustion
- Deleting the persist file forces full re-transfer of all files
