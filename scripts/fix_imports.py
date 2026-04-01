#!/usr/bin/env python3
"""Fix misplaced datetime imports in fixed files."""
import json
import os
import re
from pathlib import Path


def get_sync_invoke_files() -> list:
    """Get list of files that were fixed."""
    with open('diagnostic_results_v2.json', 'r') as f:
        data = json.load(f)
    return sorted([item['file'] for item in data['sync_invoke']], key=lambda x: x)


def fix_misplaced_import(filepath: str) -> bool:
    """Fix misplaced datetime import that got inserted inside function body."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for misplaced import (inside function body, not at top level)
    # Pattern: indented "from datetime import datetime"
    misplaced_pattern = re.compile(r'^\s+from datetime import datetime$', re.MULTILINE)
    
    if not misplaced_pattern.search(content):
        # No misplaced import
        return False

    # Remove misplaced imports
    content = misplaced_pattern.sub('', content)
    
    # Check if datetime import is in proper location (top level)
    proper_import = re.compile(r'^from datetime import datetime$', re.MULTILINE)
    
    if not proper_import.search(content):
        # Need to add proper import
        # Find the last import at top level
        lines = content.split('\n')
        last_import_idx = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                # Only count if line starts at column 0 (top-level)
                if not line[0].isspace() if line else True:
                    last_import_idx = i

        # Insert after last top-level import
        lines.insert(last_import_idx + 1, 'from datetime import datetime')
        content = '\n'.join(lines)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True


def main():
    """Main entry point."""
    files = get_sync_invoke_files()
    print(f"Checking {len(files)} files for misplaced imports...")
    
    fixed = 0
    for filepath in files:
        if os.path.exists(filepath):
            if fix_misplaced_import(filepath):
                print(f"  Fixed: {filepath}")
                fixed += 1
    
    print(f"\nFixed {fixed} files with misplaced imports")


if __name__ == '__main__':
    main()