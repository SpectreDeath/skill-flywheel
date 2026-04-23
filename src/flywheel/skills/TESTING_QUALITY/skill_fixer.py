#!/usr/bin/env python3
"""
Skill Sync Invoke Fixer

Automatically fixes the most common skill failures by:
- Adding missing datetime import if not present
- Converting def invoke() to async def invoke()
- Wrapping return values with metadata dict

Designed to work with diagnostic results from skill_diagnostic.
"""

import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def ensure_datetime_import(content: str) -> str:
    """Add datetime import if not present at module level."""
    if 'from datetime import datetime' in content or 'import datetime' in content:
        return content

    lines = content.split('\n')
    last_import_idx = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if (stripped.startswith('import ') or stripped.startswith('from ')) and not line[0:1].isspace():
            last_import_idx = i

    lines.insert(last_import_idx + 1, 'from datetime import datetime')
    return '\n'.join(lines)


def make_invoke_async(content: str) -> str:
    """Convert def invoke to async def invoke at module level."""
    return re.sub(
        r'^(def invoke\()',
        r'async def invoke(',
        content,
        flags=re.MULTILINE
    )


def fix_return_format(content: str) -> str:
    """Fix return format to include metadata."""
    pattern = re.compile(
        r'(\s+return\s*)\{\s*"result"\s*:\s*(.*?)\s*\}\s*$',
        re.MULTILINE | re.DOTALL
    )

    def replacer(match):
        indent = match.group(1)
        result_expr = match.group(2).strip().rstrip(',')
        return (
            f'{indent}{{\n'
            f'{indent}    "result": {result_expr},\n'
            f'{indent}    "metadata": {{\n'
            f'{indent}        "action": action,\n'
            f'{indent}        "timestamp": datetime.now().isoformat(),\n'
            f'{indent}    }},\n'
            f'{indent}}}'
        )

    return pattern.sub(replacer, content)


def fix_sync_invoke_file(filepath: str) -> Dict[str, Any]:
    """
    Fix a single sync invoke file.

    Args:
        filepath: Path to the file to fix

    Returns:
        Dictionary with fix results
    """
    filepath_obj = Path(filepath)

    if not filepath_obj.exists():
        return {
            "status": "error",
            "error": f"File not found: {filepath}"
        }

    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()

    content = original_content

    # Step 1: Ensure datetime import
    content = ensure_datetime_import(content)

    # Step 2: Make invoke async
    content = make_invoke_async(content)

    # Step 3: Fix return format
    content = fix_return_format(content)

    changed = content != original_content

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return {
        "status": "success",
        "file": filepath,
        "changed": changed,
        "actions": [
            "check_datetime_import",
            "convert_to_async",
            "fix_return_format"
        ]
    }


def fix_multiple_files(filepaths: List[str]) -> Dict[str, Any]:
    """
    Fix multiple sync invoke files.

    Args:
        filepaths: List of file paths to fix

    Returns:
        Dictionary with overall results
    """
    results = []
    fixed_count = 0
    error_count = 0

    for filepath in filepaths:
        try:
            result = fix_sync_invoke_file(filepath)
            results.append(result)
            if result.get("changed"):
                fixed_count += 1
        except Exception as e:
            results.append({
                "file": filepath,
                "status": "error",
                "error": str(e)
            })
            error_count += 1

    return {
        "status": "success",
        "total_files": len(filepaths),
        "fixed": fixed_count,
        "errors": error_count,
        "results": results
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "fix_single")
    filepath = payload.get("filepath")
    filepaths = payload.get("filepaths", [])

    if action == "fix_single":
        if not filepath:
            return {
                "result": {"status": "error", "error": "filepath required"},
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat(),
                },
            }
        result = fix_sync_invoke_file(filepath)
        return {
            "result": result,
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }

    elif action == "fix_multiple":
        if not filepaths:
            return {
                "result": {"status": "error", "error": "filepaths required"},
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat(),
                },
            }
        result = fix_multiple_files(filepaths)
        return {
            "result": result,
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }

    elif action == "dry_run":
        if not filepath:
            return {
                "result": {"status": "error", "error": "filepath required for dry run"},
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat(),
                },
            }

        # Dry run - don't actually write
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original = f.read()

            modified = original
            modified = ensure_datetime_import(modified)
            modified = make_invoke_async(modified)
            modified = fix_return_format(modified)

            result = {
                "status": "success",
                "file": filepath,
                "would_change": modified != original,
                "actions_needed": []
            }

            if 'from datetime import datetime' not in original and 'import datetime' not in original:
                result["actions_needed"].append("add_datetime_import")
            if re.search(r'^(def invoke\()', original, re.MULTILINE):
                result["actions_needed"].append("convert_to_async")
            if re.search(r'return\s*\{\s*"result"\s*:', original):
                result["actions_needed"].append("fix_return_format")

            return {
                "result": result,
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat(),
                },
            }
        except Exception as e:
            return {
                "result": {"status": "error", "error": str(e)},
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat(),
                },
            }

    else:
        return {
            "result": {"status": "error", "message": f"Unknown action: {action}"},
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }


def register_skill():
    """Return skill metadata."""

if __name__ == "__main__":
    return {
            "name": "skill-fixer",
            "description": "Automatically fixes sync invoke functions by converting them to async and adding metadata to return format",
            "version": "1.0.0",
            "domain": "TESTING_QUALITY",
        }