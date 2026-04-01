#!/usr/bin/env python3
"""
Parity Auditor

Compares a porting workspace against an archived source to identify:
- Missing files that exist in archive but not in port
- Missing subsystems/modules
- Coverage percentages
- Parity gaps with severity ratings

Pattern extracted from Claw Code's parity_audit.py.
"""

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


@dataclass
class ParityGap:
    """A single gap in parity between source and target."""
    path: str
    category: str  # 'file', 'subsystem', 'command', 'tool'
    severity: str  # 'critical', 'high', 'medium', 'low'
    description: str


@dataclass
class AuditResult:
    """Result of a parity audit."""
    source_file_count: int
    target_file_count: int
    source_subsystem_count: int
    target_subsystem_count: int
    gaps: List[ParityGap] = field(default_factory=list)

    @property
    def file_coverage_pct(self) -> float:
        if self.source_file_count == 0:
            return 100.0
        return round((self.target_file_count / self.source_file_count) * 100, 2)

    @property
    def subsystem_coverage_pct(self) -> float:
        if self.source_subsystem_count == 0:
            return 100.0
        return round((self.target_subsystem_count / self.source_subsystem_count) * 100, 2)

    @property
    def gap_count(self) -> int:
        return len(self.gaps)

    @property
    def critical_gaps(self) -> int:
        return len([g for g in self.gaps if g.severity == 'critical'])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_file_count": self.source_file_count,
            "target_file_count": self.target_file_count,
            "source_subsystem_count": self.source_subsystem_count,
            "target_subsystem_count": self.target_subsystem_count,
            "file_coverage_pct": self.file_coverage_pct,
            "subsystem_coverage_pct": self.subsystem_coverage_pct,
            "total_gaps": self.gap_count,
            "critical_gaps": self.critical_gaps,
            "gaps": [
                {"path": g.path, "category": g.category, "severity": g.severity, "description": g.description}
                for g in self.gaps
            ]
        }


def count_files_in_directory(directory: str, extensions: Optional[Set[str]] = None) -> int:
    """Count files in a directory, optionally filtered by extension."""
    dir_path = Path(directory)
    if not dir_path.exists():
        return 0

    count = 0
    for f in dir_path.rglob('*'):
        if f.is_file():
            if extensions is None or f.suffix in extensions:
                count += 1
    return count


def get_subsystems(directory: str) -> Set[str]:
    """Get subsystem names from a directory."""
    dir_path = Path(directory)
    if not dir_path.exists():
        return set()

    subsystems = set()
    for item in dir_path.iterdir():
        if item.is_dir() and not item.name.startswith(('.', '__')):
            subsystems.add(item.name)
    return subsystems


def run_parity_audit(
    source_dir: str,
    target_dir: str,
    extensions: Optional[Set[str]] = None
) -> AuditResult:
    """
    Run a parity audit between source and target directories.

    Args:
        source_dir: Reference (archive) directory
        target_dir: Ported directory
        extensions: File extensions to count

    Returns:
        AuditResult with coverage stats and gaps
    """
    source_files = count_files_in_directory(source_dir, extensions)
    target_files = count_files_in_directory(target_dir, extensions)

    source_subsystems = get_subsystems(source_dir)
    target_subsystems = get_subsystems(target_dir)

    gaps = []

    # Check for missing subsystems
    missing_subsystems = source_subsystems - target_subsystems
    for ss in missing_subsystems:
        gaps.append(ParityGap(
            path=f"subsystems/{ss}",
            category="subsystem",
            severity="critical" if ss in {'core', 'runtime', 'tools'} else "high",
            description=f"Missing subsystem: {ss}"
        ))

    # Check for extra subsystems (not in source)
    extra_subsystems = target_subsystems - source_subsystems
    for ss in extra_subsystems:
        gaps.append(ParityGap(
            path=f"subsystems/{ss}",
            category="subsystem",
            severity="low",
            description=f"Extra subsystem (not in source): {ss}"
        ))

    # File count disparity
    if source_files > 0 and target_files < source_files * 0.5:
        gaps.append(ParityGap(
            path="files",
            category="file",
            severity="critical",
            description=f"Target has {target_files} files vs source {source_files} ({target_files/source_files*100:.1f}%)"
        ))
    elif source_files > 0 and target_files < source_files * 0.8:
        gaps.append(ParityGap(
            path="files",
            category="file",
            severity="high",
            description=f"Target has {target_files} files vs source {source_files} ({target_files/source_files*100:.1f}%)"
        ))

    return AuditResult(
        source_file_count=source_files,
        target_file_count=target_files,
        source_subsystem_count=len(source_subsystems),
        target_subsystem_count=len(target_subsystems),
        gaps=gaps
    )


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "audit")

    if action == "audit":
        source_dir = payload.get("source_dir", "")
        target_dir = payload.get("target_dir", "")
        extensions = payload.get("extensions")

        if not source_dir or not target_dir:
            return {
                "result": {"error": "source_dir and target_dir required"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        ext_set = set(extensions) if extensions else None
        result = run_parity_audit(source_dir, target_dir, ext_set)

        return {
            "result": result.to_dict(),
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "count_files":
        directory = payload.get("directory", "")
        extensions = payload.get("extensions")

        if not directory:
            return {
                "result": {"error": "directory required"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        ext_set = set(extensions) if extensions else None
        count = count_files_in_directory(directory, ext_set)

        return {
            "result": {"directory": directory, "file_count": count},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "list_subsystems":
        directory = payload.get("directory", "")

        if not directory:
            return {
                "result": {"error": "directory required"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        subsystems = get_subsystems(directory)

        return {
            "result": {
                "directory": directory,
                "subsystem_count": len(subsystems),
                "subsystems": sorted(list(subsystems))
            },
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    else:
        return {
            "result": {"error": f"Unknown action: {action}"},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }


def register_skill():
    """Return skill metadata."""
    return {
        "name": "parity-auditor",
        "description": "Compares porting workspace against archived source to identify missing files, subsystems, and coverage gaps",
        "version": "1.0.0",
        "domain": "MODERN_BACKEND",
    }