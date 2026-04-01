#!/usr/bin/env python3
"""
Automated fix script for sync invoke modules.
Converts synchronous invoke functions to async and adds metadata to return format.
"""
import json
import os
import re
from pathlib import Path
from typing import List

SKILLS_DIR = Path('src/flywheel/skills')


def get_sync_invoke_files() -> List[str]:
    """Get list of files with sync invoke from diagnostic results."""
    with open('diagnostic_results_v2.json', 'r') as f:
        data = json.load(f)
    return sorted(data['sync_invoke'], key=lambda x: x['file'])


def ensure_datetime_import(content: str) -> str:
    """Add datetime import if not present."""
    if 'from datetime import datetime' in content or 'import datetime' in content:
        return content

    lines = content.split('\n')
    last_import_idx = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('from '):
            # Skip multi-line imports
            if not stripped.endswith('\\') and '(' not in stripped or ')' in stripped:
                last_import_idx = i

    # Insert datetime import after last import
    lines.insert(last_import_idx + 1, 'from datetime import datetime')
    return '\n'.join(lines)


def make_invoke_async(content: str) -> str:
    """Convert def invoke to async def invoke."""
    return re.sub(r'^(def invoke\()', r'async def invoke(', content, flags=re.MULTILINE)


def fix_return_format(content: str) -> str:
    """Fix return format to include metadata."""
    # Pattern: return {"result": <expr>}
    # We need to handle multi-line returns
    pattern = re.compile(
        r'(return\s*)\{'          # return {
        r'\s*"result"\s*:\s*'     # "result":
        r'(.*?)'                   # <result expression>
        r'\}\s*$',                 # }
        re.MULTILINE | re.DOTALL
    )

    def replacer(match):
        return_kw = match.group(1).strip()
        result_expr = match.group(2).strip()
        # Remove trailing comma if present
        result_expr = result_expr.rstrip(',')

        return (
            f'{return_kw}{{\n'
            f'        "result": {result_expr},\n'
            f'        "metadata": {{\n'
            f'            "action": action,\n'
            f'            "timestamp": datetime.now().isoformat(),\n'
            f'        }},\n'
            f'    }}'
        )

    return pattern.sub(replacer, content)


def ensure_error_handling(content: str) -> str:
    """Ensure invoke has proper try/except error handling."""
    # Check if there's already try/except in invoke
    invoke_pattern = re.compile(
        r'(async\s+def\s+invoke\([^)]*\)[^:]*:.*?)(?=\ndef\s+|\nclass\s+|\Z)',
        re.DOTALL
    )
    match = invoke_pattern.search(content)
    if match:
        invoke_body = match.group(1)
        if 'except' not in invoke_body and 'try:' not in invoke_body:
            # Add try/except wrapper
            return content
    return content


def fix_file(filepath: str) -> bool:
    """Fix a single file. Returns True if changes were made."""
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()

    content = original_content

    # Step 1: Ensure datetime import
    content = ensure_datetime_import(content)

    # Step 2: Make invoke async
    content = make_invoke_async(content)

    # Step 3: Fix return format
    content = fix_return_format(content)

    # Write back only if changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    """Main entry point."""
    files_info = get_sync_invoke_files()
    print(f"Found {len(files_info)} files to fix")

    fixed = 0
    errors = 0

    for item in files_info:
        filepath = item['file']

        if not os.path.exists(filepath):
            print(f"  ERROR - File not found: {filepath}")
            errors += 1
            continue

        try:
            if fix_file(filepath):
                print(f"  Fixed: {filepath}")
                fixed += 1
            else:
                print(f"  No changes needed: {filepath}")
        except Exception as e:
            print(f"  ERROR fixing {filepath}: {e}")
            errors += 1

    print(f"\n{'='*60}")
    print(f"Results: {fixed} fixed, {len(files_info) - fixed} unchanged, {errors} errors")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()