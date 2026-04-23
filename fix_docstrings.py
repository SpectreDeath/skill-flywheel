#!/usr/bin/env python3
"""
Script to fix malformed docstrings in Python files.

This script finds and fixes:
1. Module docstrings that start with single quotes instead of triple quotes
2. Function docstrings that start with single quotes instead of triple quotes
3. Unterminated string literals in default parameter values
"""

import os
import re
import sys
from pathlib import Path


def fix_file(filepath):
    """Fix malformed docstrings and syntax errors in a Python file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Fix module docstrings that start with single quote
        # Pattern: start of file, single quote, then text, then single quote on next line(s)
        pattern = r'^(\s*)"([^"]*?)"\s*$'
        lines = content.split('\n')
        if len(lines) >= 3:
            # Check if first line is shebang
            start_idx = 0
            if lines[0].startswith('#!'):
                start_idx = 1

            # Check for malformed module docstring
            if start_idx < len(lines) and lines[start_idx].strip() == '"':
                # Find the closing quote
                for i in range(start_idx + 1, len(lines)):
                    if lines[i].strip() == '"':
                        # Replace with triple quotes
                        lines[start_idx] = lines[start_idx].replace('"', '"""')
                        lines[i] = lines[i].replace('"', '"""')
                        break

        content = '\n'.join(lines)

        # Fix function docstrings that start with single quote
        # Pattern: def function(...):\n    "docstring"\n
        pattern = r'(def\s+\w+[^:]*:\s*$)\n(\s*)"([^"]*?)"\s*$'
        content = re.sub(pattern, r'\1\n\2""" \3 """', content, flags=re.MULTILINE)

        # Fix unterminated string literals in default parameters
        # Pattern: parameter: str = "
        pattern = r'(\w+\s*:\s*str\s*=\s*)"([^"]*)$'
        content = re.sub(pattern, r'\1"""\2"""', content, flags=re.MULTILINE)

        # Fix register_skill function docstrings
        pattern = r'(def register_skill\(\):\s*$)\n(\s*)"([^"]*?)"\s*$'
        content = re.sub(pattern, r'\1\n\2""" \3 """', content, flags=re.MULTILINE)

        # Fix test code that should be in if __name__ == "__main__"
        # Look for code after a triple-quoted string that ends with """
        if 'if __name__ == "__main__":' not in content:
            # Find triple-quoted strings and check if there's executable code after
            triple_quote_pattern = r'""".*?"""'
            matches = list(re.finditer(triple_quote_pattern, content, re.DOTALL))
            if matches:
                last_match = matches[-1]
                after_pos = last_match.end()
                remaining_content = content[after_pos:].strip()
                if remaining_content and not remaining_content.startswith('if __name__'):
                    # Check if there's actual executable code (not just comments)
                    code_lines = [line for line in remaining_content.split('\n') if line.strip() and not line.strip().startswith('#')]
                    if code_lines:
                        content = content[:after_pos] + '\n\nif __name__ == "__main__":\n' + '\n'.join('    ' + line if line.strip() else line for line in remaining_content.split('\n'))

        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

    return False


def main():
    """Main function to fix all Python files in the src directory."""
    if len(sys.argv) != 2:
        print("Usage: python fix_docstrings.py <directory>")
        sys.exit(1)

    directory = Path(sys.argv[1])
    if not directory.exists():
        print(f"Directory {directory} does not exist")
        sys.exit(1)

    fixed_count = 0
    for py_file in directory.rglob("*.py"):
        if fix_file(py_file):
            print(f"Fixed: {py_file}")
            fixed_count += 1

    print(f"Fixed {fixed_count} files")


if __name__ == "__main__":
    main()