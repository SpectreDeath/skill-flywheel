#!/usr/bin/env python3
"""
Python Import Placement Fixer

Detects and fixes imports that got accidentally placed inside function bodies
instead of at module level. Common after automated editing or code generation.

Can be used standalone or after running skill_fixer to clean up any
misplaced imports.
"""

import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


def find_misplaced_imports(content: str) -> List[Dict[str, Any]]:
    """
    Find imports that are inside function bodies instead of at module level.

    Args:
        content: Python source code

    Returns:
        List of dicts with line, import_statement, and context
    """
    misplaced = []
    lines = content.split('\n')

    in_function = False
    function_indent = 0

    for i, line in enumerate(lines, 1):
        # Detect function start
        stripped = line.lstrip()
        current_indent = len(line) - len(stripped)

        if stripped.startswith('def ') or stripped.startswith('async def '):
            in_function = True
            function_indent = current_indent
            continue

        # Check if we've exited the function
        if in_function and stripped and current_indent <= function_indent:
            in_function = False

        # Check for import inside function
        if in_function and (stripped.startswith('import ') or stripped.startswith('from ')):
            # Make sure it's not a local import of a variable (common pattern)
            if not any(
                stripped.startswith(f'import ') or stripped.startswith(f'from ')
                for prefix in ['local_', 'self.']
            ):
                misplaced.append({
                    'line': i,
                    'import_statement': stripped,
                    'context': line
                })

    return misplaced


def has_module_level_import(content: str, import_statement: str) -> bool:
    """Check if the import exists at module level."""
    lines = content.split('\n')

    for line in lines:
        # Line must start at column 0 (module level)
        if line.startswith(import_statement) or line.startswith(f'{import_statement} '):
            return True
        # Handle 'from X import Y'
        if import_statement.startswith('from ') and line.startswith(import_statement):
            return True

    return False


def fix_misplaced_imports(filepath: str, dry_run: bool = False) -> Dict[str, Any]:
    """
    Fix misplaced imports in a Python file.

    Args:
        filepath: Path to the file to fix
        dry_run: If True, don't write changes

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

    # Find misplaced imports
    misplaced = find_misplaced_imports(original_content)

    if not misplaced:
        return {
            "status": "success",
            "file": filepath,
            "changed": False,
            "misplaced_found": 0,
            "message": "No misplaced imports found"
        }

    content = original_content
    fixed_imports = []
    removed_lines = set()

    for issue in misplaced:
        import_stmt = issue['import_statement']

        # Check if already exists at module level
        import_base = import_stmt.split('#')[0].strip()

        if not has_module_level_import(original_content, import_base):
            # Need to add at module level
            lines = content.split('\n')

            # Find last module-level import line
            last_import_idx = 0
            for i, line in enumerate(lines):
                stripped = line.strip()
                if (stripped.startswith('import ') or stripped.startswith('from ')) and not line[0:1].isspace():
                    last_import_idx = i

            # Add import after last import
            lines.insert(last_import_idx + 1, import_base)
            content = '\n'.join(lines)

        fixed_imports.append({
            'original_line': issue['line'],
            'import': import_base,
            'action': 'moved_to_module_level' if has_module_level_import(original_content, import_base) else 'added_at_module_level'
        })

        # Remove the misplaced import line
        line_num = issue['line']
        lines = content.split('\n')
        if 0 < line_num <= len(lines):
            # Only remove if it's just the import (no other code on same line)
            stripped = lines[line_num - 1].strip()
            if stripped == import_base:
                lines[line_num - 1] = ''
                content = '\n'.join(lines)

    # Clean up blank lines
    content = re.sub(r'\n\n\n+', '\n\n', content)

    changed = content != original_content

    if changed and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return {
        "status": "success",
        "file": filepath,
        "changed": changed,
        "misplaced_found": len(misplaced),
        "fixed_imports": fixed_imports,
        "dry_run": dry_run
    }


def scan_directory_for_misplaced_imports(
    directory: str,
    recursive: bool = True
) -> Dict[str, Any]:
    """
    Scan directory for files with misplaced imports.

    Args:
        directory: Directory to scan
        recursive: Whether to scan recursively

    Returns:
        Dictionary with scan results
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return {
            "status": "error",
            "error": f"Directory not found: {directory}"
        }

    results = []
    files_scanned = 0
    files_with_issues = 0

    if recursive:
        file_iter = dir_path.rglob('*.py')
    else:
        file_iter = dir_path.glob('*.py')

    for filepath in file_iter:
        if filepath.name.startswith('__'):
            continue

        files_scanned += 1

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        misplaced = find_misplaced_imports(content)

        if misplaced:
            files_with_issues += 1
            results.append({
                "file": str(filepath),
                "misplaced_count": len(misplaced),
                "issues": misplaced
            })

    return {
        "status": "success",
        "files_scanned": files_scanned,
        "files_with_issues": files_with_issues,
        "results": results
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "fix_file")
    filepath = payload.get("filepath")
    directory = payload.get("directory")
    dry_run = payload.get("dry_run", False)
    recursive = payload.get("recursive", True)

    if action == "fix_file":
        if not filepath:
            return {
                "result": {"status": "error", "error": "filepath required"},
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat(),
                },
            }

        result = fix_misplaced_imports(filepath, dry_run=dry_run)
        return {
            "result": result,
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }

    elif action == "scan_directory":
        if not directory:
            return {
                "result": {"status": "error", "error": "directory required"},
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat(),
                },
            }

        result = scan_directory_for_misplaced_imports(directory, recursive)
        return {
            "result": result,
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }

    elif action == "check_single":
        if not filepath:
            return {
                "result": {"status": "error", "error": "filepath required"},
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat(),
                },
            }

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            misplaced = find_misplaced_imports(content)

            return {
                "result": {
                    "status": "success",
                    "file": filepath,
                    "misplaced_count": len(misplaced),
                    "issues": misplaced
                },
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
    return {
        "name": "imports-fixer",
        "description": "Detects and fixes Python imports that are placed inside function bodies instead of at module level",
        "version": "1.0.0",
        "domain": "TESTING_QUALITY",
    }
