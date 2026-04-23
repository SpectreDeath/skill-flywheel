#!/usr/bin/env python3
"""
Operational Deliverables Packaging

Makefile-driven packaging system for field deployment that:
- Separates binaries, documentation, source code, and other assets
- Generates MD5 integrity verification files
- Creates compressed source archives
- Verifies artifact integrity before deployment

Pattern extracted from Buildroot-style deliverable packaging workflows.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class DeliverablePackage:
    """Structured deliverable package for field deployment."""

    DIRECTORIES = ["BIN", "DOC", "SRC", "OTHER"]

    def __init__(self, base_dir: str = "deliverables"):
        self.base_dir = Path(base_dir)
        self.subdirs = {
            name: self.base_dir / name
            for name in self.DIRECTORIES
        }
        self.artifacts = {}

    def initialize(self) -> None:
        """Create directory structure."""
        self.remove()
        for d in self.subdirs.values():
            d.mkdir(parents=True, exist_ok=True)

    def remove(self) -> None:
        """Remove entire deliverables directory."""
        import shutil
        if self.base_dir.exists():
            shutil.rmtree(self.base_dir)

    def add_binary(
        self,
        source_path: str,
        generate_md5: bool = True
    ) -> Dict[str, str]:
        """Add a binary artifact with optional MD5 verification."""
        src = Path(source_path)
        if not src.exists():
            raise FileNotFoundError(f"Source not found: {source_path}")

        dest = self.subdirs["BIN"] / src.name
        import shutil
        shutil.copy2(str(src), str(dest))

        result = {"binary": str(dest)}

        if generate_md5:
            import hashlib
            md5 = hashlib.md5(src.read_bytes()).hexdigest()
            md5_path = dest.with_suffix(dest.suffix + ".md5")
            md5_path.write_text(md5)
            result["md5_file"] = str(md5_path)
            result["md5"] = md5

        self.artifacts[src.name] = result
        return result

    def add_documentation(self, source_path: str) -> str:
        """Add documentation file."""
        src = Path(source_path)
        if not src.exists():
            raise FileNotFoundError(f"Source not found: {source_path}")

        dest = self.subdirs["DOC"] / src.name
        import shutil
        shutil.copy2(str(src), str(dest))
        self.artifacts[src.name] = {"doc": str(dest)}
        return str(dest)

    def add_source_archive(
        self,
        source_dir: str,
        exclude_patterns: Optional[List[str]] = None,
        compression: str = "bzip2"
    ) -> str:
        """Create compressed source archive."""
        excludes = exclude_patterns or []
        exclude_names = {
            ".svn", ".git", "__pycache__", "*.o", "*.a", "*.md5",
            "*.gz", "*.tar", "*.tgz", "snapshot_*", "documentation/html/*"
        }
        all_excludes = exclude_names | set(excludes)

        import tarfile
        import shutil

        tar_path = self.subdirs["SRC"] / "source.tar"
        with tarfile.open(str(tar_path), "w") as tar:
            src_dir = Path(source_dir)
            for item in src_dir.iterdir():
                if any(item.match(p) for p in all_excludes):
                    continue
                tar.add(str(item), arcname=item.name)

        if compression == "bzip2":
            import bz2
            compressed_path = self.subdirs["SRC"] / "source.tar.bz2"
            with open(str(tar_path), "rb") as f:
                compressed_path.write_bytes(bz2.compress(f.read()))
            tar_path.unlink()
            return str(compressed_path)
        elif compression == "gzip":
            import gzip
            compressed_path = self.subdirs["SRC"] / "source.tar.gz"
            with open(str(tar_path), "rb") as f:
                compressed_path.write_bytes(gzip.compress(f.read()))
            tar_path.unlink()
            return str(compressed_path)
        else:
            return str(tar_path)

    def list_artifacts(self) -> Dict[str, Any]:
        """List all artifacts in the package."""
        result = {}
        for name, subdir in self.subdirs.items():
            if subdir.exists():
                files = [f.name for f in subdir.iterdir()]
                result[name] = files
            else:
                result[name] = []
        return result

    def verify_integrity(self) -> Dict[str, Any]:
        """Verify MD5 integrity of all binary artifacts."""
        bin_dir = self.subdirs["BIN"]
        if not bin_dir.exists():
            return {"status": "error", "message": "BIN directory not found"}

        import hashlib

        verified = []
        failed = []
        missing_md5 = []

        for md5_file in bin_dir.glob("*.md5"):
            binary_file = md5_file.with_suffix("")
            if not binary_file.exists():
                failed.append({
                    "file": str(binary_file),
                    "error": "Binary file not found"
                })
                continue

            expected_md5 = md5_file.read_text().strip()
            actual_md5 = hashlib.md5(binary_file.read_bytes()).hexdigest()

            if expected_md5 == actual_md5:
                verified.append({
                    "file": str(binary_file),
                    "md5": actual_md5,
                    "status": "verified"
                })
            else:
                failed.append({
                    "file": str(binary_file),
                    "expected": expected_md5,
                    "actual": actual_md5,
                    "status": "failed"
                })

        return {
            "status": "success",
            "verified_count": len(verified),
            "failed_count": len(failed),
            "verified": verified,
            "failed": failed,
        }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "list_artifacts")

    if action == "initialize":
        base_dir = payload.get("base_dir", "deliverables")
        package = DeliverablePackage(base_dir)
        package.initialize()
        return {
            "result": {
                "status": "initialized",
                "base_dir": base_dir,
                "directories": DeliverablePackage.DIRECTORIES,
            },
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "add_binary":
        base_dir = payload.get("base_dir", "deliverables")
        source_path = payload.get("source_path", "")
        generate_md5 = payload.get("generate_md5", True)

        if not source_path:
            return {
                "result": {"error": "source_path required"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        package = DeliverablePackage(base_dir)
        try:
            result = package.add_binary(source_path, generate_md5)
            return {
                "result": result,
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }
        except FileNotFoundError as e:
            return {
                "result": {"error": str(e)},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    elif action == "verify_integrity":
        base_dir = payload.get("base_dir", "deliverables")
        package = DeliverablePackage(base_dir)
        result = package.verify_integrity()
        return {
            "result": result,
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "list_artifacts":
        base_dir = payload.get("base_dir", "deliverables")
        package = DeliverablePackage(base_dir)
        result = package.list_artifacts()
        return {
            "result": result,
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "create_source_archive":
        base_dir = payload.get("base_dir", "deliverables")
        source_dir = payload.get("source_dir", "")
        compression = payload.get("compression", "bzip2")
        excludes = payload.get("exclude_patterns", [])

        if not source_dir:
            return {
                "result": {"error": "source_dir required"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        package = DeliverablePackage(base_dir)
        archive_path = package.add_source_archive(source_dir, excludes, compression)
        return {
            "result": {"archive": archive_path, "compression": compression},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    else:
        return {
            "result": {"error": f"Unknown action: {action}"},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }


def register_skill():
    """Return skill metadata."""

if __name__ == "__main__":
    return {
            "name": "operational-deliverables",
            "description": "Packaging system for creating structured field deployment artifacts with MD5 integrity verification and compressed source archives",
            "version": "1.0.0",
            "domain": "DATA_ENGINEERING",
        }