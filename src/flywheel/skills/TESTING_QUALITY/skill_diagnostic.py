#!/usr/bin/env python3
"""
Skill Module Diagnostic Analyzer

Scans all Python files in the skills directory and categorizes them by:
- Missing invoke() function (Type 1)
- Synchronous invoke() instead of async (Type 2)
- Wrong return format (missing metadata)
- Windows junction failures
- Correctly formatted modules

Returns structured diagnostic results for automated repair workflows.
"""

import ast
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


def check_module(filepath: Path) -> Optional[Dict[str, Any]]:
    """Check a single Python module for invoke function issues."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (OSError, PermissionError) as e:
        return {
            'file': str(filepath),
            'issue_type': 'junction_failure',
            'error': str(e)
        }
    except Exception:
        return None

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return None

    # Check for invoke functions
    has_async_invoke = False
    has_sync_invoke = False
    invoke_nodes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.AsyncFunctionDef) and node.name == 'invoke':
            has_async_invoke = True
            invoke_nodes.append(('async', node))
        elif isinstance(node, ast.FunctionDef) and node.name == 'invoke':
            has_sync_invoke = True
            invoke_nodes.append(('sync', node))

    if not has_async_invoke and not has_sync_invoke:
        # Type 1: No invoke at all
        has_class_with_methods = False
        class_names = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                methods = [
                    n.name for n in node.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]
                if methods:
                    has_class_with_methods = True
                    class_names.append((node.name, methods))

        return {
            'file': str(filepath),
            'issue_type': 'no_invoke',
            'has_class_with_methods': has_class_with_methods,
            'classes': [c[0] for c in class_names]
        }
    elif has_sync_invoke and not has_async_invoke:
        # Type 2: Sync invoke (should be async)
        return {
            'file': str(filepath),
            'issue_type': 'sync_invoke',
            'type': 'sync_invoke'
        }
    else:
        # Has async invoke - check return format
        has_correct_format = False
        has_wrong_format = False

        for invoke_type, invoke_node in invoke_nodes:
            for node in ast.walk(invoke_node):
                if isinstance(node, ast.Return) and node.value:
                    if isinstance(node.value, ast.Dict):
                        keys = []
                        for k in node.value.keys:
                            if isinstance(k, ast.Constant):
                                keys.append(k.value)
                        if 'result' in keys and 'metadata' in keys:
                            has_correct_format = True
                        elif 'result' in keys and 'metadata' not in keys:
                            has_wrong_format = True

        if has_wrong_format and not has_correct_format:
            return {
                'file': str(filepath),
                'issue_type': 'wrong_format',
                'has_result': True,
                'has_metadata': False
            }

    return None


def categorize_results(results: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize diagnostic results by issue type."""
    categories = {
        'no_invoke': [],
        'sync_invoke': [],
        'wrong_format': [],
        'junction_failures': [],
        'cognitive_skills': [],
        'data_pipelines': [],
        'openclaw_modules': [],
    }

    for item in results:
        issue_type = item.get('issue_type')
        filepath = item.get('file', '')

        if issue_type == 'junction_failure':
            categories['junction_failures'].append(item)
        elif issue_type == 'no_invoke':
            categories['no_invoke'].append(item)
            if 'cognitive_skills' in filepath:
                categories['cognitive_skills'].append(item)
            elif 'apache_beam' in filepath or 'federated_learning' in filepath:
                categories['data_pipelines'].append(item)
            elif 'openclaw' in filepath or 'nemoclaw' in filepath:
                categories['openclaw_modules'].append(item)
        elif issue_type == 'sync_invoke':
            categories['sync_invoke'].append(item)
        elif issue_type == 'wrong_format':
            categories['wrong_format'].append(item)

    return categories


def run_skill_diagnostic(
    skills_dir: str = "src/flywheel/skills",
    skip_archived: bool = True
) -> Dict[str, Any]:
    """
    Run comprehensive diagnostic on all skill modules.

    Args:
        skills_dir: Path to skills directory
        skip_archived: Whether to skip ARCHIVED directories

    Returns:
        Dictionary containing:
        - total_scanned: Number of files scanned
        - results: List of all diagnostic results
        - categories: Results grouped by issue type
        - summary: Quick overview counts
    """
    results = []
    file_count = 0

    skill_dir = Path(skills_dir)
    if not skill_dir.exists():
        return {
            "status": "error",
            "error": f"Skills directory not found: {skills_dir}"
        }

    dirs_to_skip = {'__pycache__', '.git'}
    if skip_archived:
        dirs_to_skip.add('ARCHIVED')

    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in dirs_to_skip]

        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                filepath = Path(root) / file
                result = check_module(filepath)
                if result:
                    results.append(result)
                file_count += 1

    categories = categorize_results(results)

    return {
        "status": "success",
        "total_scanned": file_count,
        "results": results,
        "categories": categories,
        "summary": {
            "no_invoke": len(categories['no_invoke']),
            "sync_invoke": len(categories['sync_invoke']),
            "wrong_format": len(categories['wrong_format']),
            "junction_failures": len(categories['junction_failures']),
            "cognitive_skills_no_invoke": len(categories['cognitive_skills']),
            "data_pipelines_no_invoke": len(categories['data_pipelines']),
            "openclaw_no_invoke": len(categories['openclaw_modules']),
        }
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "diagnose")
    skills_dir = payload.get("skills_dir", "src/flywheel/skills")
    skip_archived = payload.get("skip_archived", True)
    save_results = payload.get("save_results", False)
    output_file = payload.get("output_file", "diagnostic_results.json")

    if action == "diagnose":
        result = run_skill_diagnostic(skills_dir, skip_archived)

        if save_results and result.get("status") == "success":
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)

        return {
            "result": result,
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }

    elif action == "check_single":
        filepath = payload.get("filepath")
        if not filepath:
            return {
                "result": {"status": "error", "error": "filepath required"},
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat(),
                },
            }

        result = check_module(Path(filepath))
        return {
            "result": result or {"status": "ok", "message": "No issues found"},
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }

    elif action == "summary":
        result = run_skill_diagnostic(skills_dir, skip_archived)
        return {
            "result": {"status": "success", "summary": result.get("summary", {})},
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
        "name": "skill-diagnostic",
        "description": "Comprehensive diagnostic analyzer for skill modules, detecting missing invoke functions, sync vs async issues, and format problems",
        "version": "1.0.0",
        "domain": "TESTING_QUALITY",
    }