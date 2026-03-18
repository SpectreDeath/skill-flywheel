"""
Filesystem Maintenance

Handles file system maintenance tasks including:
- Clean temporary files (cache, temp, __pycache__)
- Find large files (identify space hogs)
- Organize structure (suggest directory organization)
- Find duplicates (detect duplicate files)
- Backup files (create backup copies)
"""

import os
import shutil
import hashlib
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class CleanResult:
    """Result of cleaning operation."""

    files_removed: int = 0
    directories_removed: int = 0
    space_freed: int = 0
    errors: List[str] = field(default_factory=list)


@dataclass
class LargeFile:
    """Represents a large file."""

    path: str
    size: int
    modified: str


@dataclass
class DuplicateGroup:
    """Group of duplicate files."""

    hash: str
    size: int
    files: List[str]


@dataclass
class BackupResult:
    """Result of backup operation."""

    files_backed_up: int = 0
    total_size: int = 0
    backup_path: str = ""
    errors: List[str] = field(default_factory=list)


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def get_file_hash(filepath: str) -> Optional[str]:
    """Calculate MD5 hash of a file."""
    try:
        hasher = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (IOError, OSError):
        return None


def clean_temp_files(path: str, options: dict) -> CleanResult:
    """Clean temporary files from directory."""
    result = CleanResult()

    patterns = options.get(
        "patterns",
        [
            "__pycache__",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".pytest_cache",
            ".tox",
            "*.tmp",
            "*.temp",
            "*.log",
            ".cache",
            "node_modules",
            ".next",
            ".nuxt",
            "dist",
            "build",
            "coverage",
            ".coverage",
            "*.egg-info",
            ".mypy_cache",
            ".ruff_cache",
        ],
    )

    dry_run = options.get("dry_run", False)

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in [".git", ".svn", "node_modules"]]

        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if any(
                pattern == dir_name or dir_name.endswith(pattern.replace("*", ""))
                for pattern in patterns
            ):
                try:
                    size = sum(
                        os.path.getsize(os.path.join(dp, f))
                        for dp, dn, fn in os.walk(dir_path)
                        for f in fn
                    )
                    if not dry_run:
                        shutil.rmtree(dir_path)
                    result.directories_removed += 1
                    result.space_freed += size
                except Exception as e:
                    result.errors.append(f"Failed to remove {dir_path}: {e}")

        for file_name in files:
            file_path = os.path.join(root, file_name)
            if any(
                file_name.endswith(pattern.replace("*", ""))
                for pattern in patterns
                if "*" in pattern
            ):
                try:
                    size = os.path.getsize(file_path)
                    if not dry_run:
                        os.remove(file_path)
                    result.files_removed += 1
                    result.space_freed += size
                except Exception as e:
                    result.errors.append(f"Failed to remove {file_path}: {e}")

    return result


def find_large_files(path: str, options: dict) -> List[LargeFile]:
    """Find large files in directory."""
    min_size = options.get("min_size_mb", 1) * 1024 * 1024
    limit = options.get("limit", 50)

    large_files = []

    for root, _, files in os.walk(path):
        dirs_to_skip = [".git", "node_modules", "__pycache__"]
        if any(skip in root for skip in dirs_to_skip):
            continue

        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                size = os.path.getsize(file_path)
                if size >= min_size:
                    mtime = os.path.getmtime(file_path)
                    large_files.append(
                        LargeFile(
                            path=file_path,
                            size=size,
                            modified=datetime.fromtimestamp(mtime).isoformat(),
                        )
                    )
            except (OSError, IOError):
                continue

    large_files.sort(key=lambda x: x.size, reverse=True)
    return large_files[:limit]


def analyze_directory_structure(path: str, options: dict) -> Dict[str, Any]:
    """Analyze and suggest directory organization."""
    structure = {
        "total_files": 0,
        "total_dirs": 0,
        "total_size": 0,
        "file_types": {},
        "depth": 0,
        "largest_dirs": [],
        "suggestions": [],
    }

    dir_sizes = {}

    for root, dirs, files in os.walk(path):
        depth = root.replace(path, "").count(os.sep)
        structure["depth"] = max(structure["depth"], depth)
        structure["total_dirs"] += len(dirs)

        dirs_to_skip = [".git", "node_modules", "__pycache__", ".venv", "venv"]
        dirs[:] = [d for d in dirs if d not in dirs_to_skip]

        current_dir_size = 0
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                size = os.path.getsize(file_path)
                structure["total_files"] += 1
                structure["total_size"] += size
                current_dir_size += size

                ext = os.path.splitext(file_name)[1].lower() or "no_extension"
                structure["file_types"][ext] = structure["file_types"].get(ext, 0) + 1
            except (OSError, IOError):
                continue

        if current_dir_size > 0:
            dir_sizes[root] = current_dir_size

    structure["largest_dirs"] = [
        {"path": k, "size": v, "size_formatted": format_size(v)}
        for k, v in sorted(dir_sizes.items(), key=lambda x: x[1], reverse=True)[:10]
    ]

    file_type_counts = sorted(
        structure["file_types"].items(), key=lambda x: x[1], reverse=True
    )
    structure["top_file_types"] = [
        {"ext": k, "count": v} for k, v in file_type_counts[:10]
    ]

    if structure["depth"] > 5:
        structure["suggestions"].append("Consider flattening deep directory structure")

    if any("test" in d.lower() for d in dir_sizes.keys()):
        structure["suggestions"].append(
            "Consider separating test files into dedicated test directories"
        )

    src_found = any("src" in d.lower() for d in dir_sizes.keys())
    if not src_found:
        structure["suggestions"].append("Consider organizing code into 'src' directory")

    if (
        not any("docs" in d.lower() for d in dir_sizes.keys())
        and structure["total_files"] > 10
    ):
        structure["suggestions"].append(
            "Consider adding a 'docs' directory for documentation"
        )

    structure["total_size_formatted"] = format_size(structure["total_size"])

    return structure


def find_duplicates(path: str, options: dict) -> List[DuplicateGroup]:
    """Find duplicate files in directory."""
    min_size = options.get("min_size", 1024)
    hash_map: Dict[str, List[tuple]] = {}

    for root, _, files in os.walk(path):
        dirs_to_skip = [".git", "node_modules", "__pycache__"]
        if any(skip in root for skip in dirs_to_skip):
            continue

        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                size = os.path.getsize(file_path)
                if size < min_size:
                    continue

                file_hash = get_file_hash(file_path)
                if file_hash:
                    key = f"{file_hash}_{size}"
                    if key not in hash_map:
                        hash_map[key] = []
                    hash_map[key].append((file_path, size))
            except (OSError, IOError):
                continue

    duplicates = []
    for key, files in hash_map.items():
        if len(files) > 1:
            hash_val = key.rsplit("_", 1)[0]
            size = files[0][1]
            duplicates.append(
                DuplicateGroup(hash=hash_val, size=size, files=[f[0] for f in files])
            )

    duplicates.sort(key=lambda x: x.size, reverse=True)
    return duplicates


def backup_files(path: str, options: dict) -> BackupResult:
    """Create backup copies of files."""
    result = BackupResult()

    backup_dir = options.get(
        "backup_dir",
        os.path.join(path, ".backups", datetime.now().strftime("%Y%m%d_%H%M%S")),
    )
    include_patterns = options.get(
        "include", ["*.py", "*.js", "*.json", "*.yaml", "*.yml", "*.md", "*.txt"]
    )
    exclude_patterns = options.get(
        "exclude", ["__pycache__", "node_modules", ".git", "*.pyc", "*.log"]
    )

    os.makedirs(backup_dir, exist_ok=True)
    result.backup_path = backup_dir

    import fnmatch

    for root, dirs, files in os.walk(path):
        dirs[:] = [
            d
            for d in dirs
            if not any(fnmatch.fnmatch(d, p.replace("*", "")) for p in exclude_patterns)
        ]

        for file_name in files:
            if any(fnmatch.fnmatch(file_name, p) for p in include_patterns):
                if any(fnmatch.fnmatch(file_name, p) for p in exclude_patterns):
                    continue

                file_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(file_path, path)
                dest_path = os.path.join(backup_dir, rel_path)

                try:
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy2(file_path, dest_path)
                    size = os.path.getsize(file_path)
                    result.files_backed_up += 1
                    result.total_size += size
                except Exception as e:
                    result.errors.append(f"Failed to backup {file_path}: {e}")

    return result


def filesystem_maintenance(path: str, action: str, options: dict = None) -> dict:
    """
    Main function for filesystem maintenance operations.

    Args:
        path: Target directory path
        action: Action to perform (clean, analyze, organize, find_duplicates, backup)
        options: Action-specific options

    Returns:
        dict with status, action, results, and summary
    """
    if options is None:
        options = {}

    if not os.path.exists(path):
        return {
            "status": "error",
            "action": action,
            "results": {},
            "summary": f"Path does not exist: {path}",
        }

    if not os.path.isdir(path):
        return {
            "status": "error",
            "action": action,
            "results": {},
            "summary": f"Path is not a directory: {path}",
        }

    try:
        if action == "clean":
            result = clean_temp_files(path, options)
            return {
                "status": "success",
                "action": action,
                "results": {
                    "files_removed": result.files_removed,
                    "directories_removed": result.directories_removed,
                    "space_freed": result.space_freed,
                    "space_freed_formatted": format_size(result.space_freed),
                    "errors": result.errors,
                    "dry_run": options.get("dry_run", False),
                },
                "summary": f"Removed {result.files_removed} files and {result.directories_removed} directories, freed {format_size(result.space_freed)}",
            }

        elif action == "analyze" or action == "organize":
            result = analyze_directory_structure(path, options)
            return {
                "status": "success",
                "action": action,
                "results": result,
                "summary": f"Found {result['total_files']} files in {result['total_dirs']} directories, total size: {result['total_size_formatted']}",
            }

        elif action == "find_duplicates":
            result = find_duplicates(path, options)
            total_wasted = sum(dup.size * (len(dup.files) - 1) for dup in result)
            return {
                "status": "success",
                "action": action,
                "results": {
                    "duplicate_groups": [
                        {
                            "hash": dup.hash,
                            "size": dup.size,
                            "size_formatted": format_size(dup.size),
                            "count": len(dup.files),
                            "files": dup.files,
                        }
                        for dup in result
                    ],
                    "total_groups": len(result),
                    "total_wasted_space": total_wasted,
                    "total_wasted_formatted": format_size(total_wasted),
                },
                "summary": f"Found {len(result)} duplicate groups, wasted space: {format_size(total_wasted)}",
            }

        elif action == "backup":
            result = backup_files(path, options)
            return {
                "status": "success",
                "action": action,
                "results": {
                    "files_backed_up": result.files_backed_up,
                    "total_size": result.total_size,
                    "total_size_formatted": format_size(result.total_size),
                    "backup_path": result.backup_path,
                    "errors": result.errors,
                },
                "summary": f"Backed up {result.files_backed_up} files ({format_size(result.total_size)}) to {result.backup_path}",
            }

        else:
            return {
                "status": "error",
                "action": action,
                "results": {},
                "summary": f"Unknown action: {action}. Supported actions: clean, analyze, organize, find_duplicates, backup",
            }

    except Exception as e:
        return {
            "status": "error",
            "action": action,
            "results": {},
            "summary": f"Error performing {action}: {str(e)}",
        }


def invoke(payload: dict) -> dict:
    """MCP skill invocation."""
    path = payload.get("path", "")
    action = payload.get("action", "analyze")
    options = payload.get("options", {})

    if not path:
        return {
            "status": "error",
            "action": action,
            "results": {},
            "summary": "No path provided",
        }

    result = filesystem_maintenance(path, action, options)
    return result


def register_skill():
    """Return skill metadata."""
    return {
        "name": "filesystem-maintenance",
        "description": "Handles file system maintenance tasks including cleaning temp files, finding large files, analyzing directory structure, finding duplicates, and creating backups",
        "version": "1.0.0",
        "domain": "DEVOPS",
    }
