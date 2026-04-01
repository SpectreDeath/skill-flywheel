"""
Diagnostic script to identify skill module failure categories.
"""
import os
import ast
import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Skills base directory
SKILLS_DIR = Path('src/flywheel/skills')

# Results storage
no_invoke: List[Dict[str, Any]] = []
wrong_format: List[Dict[str, Any]] = []
junction_failures: List[Tuple[str, str]] = []

def check_module(filepath: Path) -> None:
    """Check a single Python module for issues."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (OSError, PermissionError) as e:
        # Windows junction failure
        junction_failures.append((str(filepath), str(e)))
        return
    except Exception:
        return
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return
    
    # Check for async def invoke function
    has_invoke = False
    invoke_nodes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.AsyncFunctionDef) and node.name == 'invoke':
            has_invoke = True
            invoke_nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name == 'invoke':
            has_invoke = True
            invoke_nodes.append(node)
    
    if not has_invoke:
        # Check if module has classes with methods (Type 1: no invoke)
        has_class_with_methods = False
        class_names = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                if methods:
                    has_class_with_methods = True
                    class_names.append((node.name, methods))
        
        no_invoke.append({
            'file': str(filepath),
            'has_class_with_methods': has_class_with_methods,
            'classes': class_names
        })
    else:
        # Check return format in invoke function (Type 2: wrong format)
        for invoke_node in invoke_nodes:
            for node in ast.walk(invoke_node):
                if isinstance(node, ast.Return) and node.value:
                    # Check if it's a dict with 'result' but no 'metadata'
                    if isinstance(node.value, ast.Dict):
                        keys = []
                        for k in node.value.keys:
                            if isinstance(k, ast.Constant):
                                keys.append(k.value)
                            elif hasattr(k, 's'):  # Python 3.7 compat
                                keys.append(k.s)
                        if 'result' in keys and 'metadata' not in keys:
                            wrong_format.append({
                                'file': str(filepath),
                                'has_result': True,
                                'has_metadata': False
                            })
                            break


def main() -> None:
    """Main diagnostic entry point."""
    # Walk through all Python files
    for root, dirs, files in os.walk(SKILLS_DIR):
        # Skip __pycache__ and .git
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'ARCHIVED']]
        
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                filepath = Path(root) / file
                check_module(filepath)
    
    # Print results
    print('=' * 80)
    print('DIAGNOSTIC RESULTS')
    print('=' * 80)
    
    print(f'\nType 1 - No invoke() function: {len(no_invoke)} modules')
    print('-' * 40)
    for item in sorted(no_invoke, key=lambda x: x['file']):
        classes_info = ''
        if item['has_class_with_methods']:
            classes_info = f' [Classes: {len(item["classes"])}]'
        print(f'  - {item["file"]}{classes_info}')
    
    print(f'\nType 2 - Wrong format (result without metadata): {len(wrong_format)} modules')
    print('-' * 40)
    for item in sorted(wrong_format, key=lambda x: x['file']):
        print(f'  - {item["file"]}')
    
    print(f'\nType 3 - Windows junction failures: {len(junction_failures)} modules')
    print('-' * 40)
    for filepath, error in junction_failures:
        print(f'  - {filepath}: {error}')
    
    print('\n' + '=' * 80)
    print(f'SUMMARY: {len(no_invoke)} no-invoke | {len(wrong_format)} wrong-format | {len(junction_failures)} junction failures')
    print('=' * 80)
    
    # Save results to JSON for further processing
    results = {
        'no_invoke': no_invoke,
        'wrong_format': wrong_format,
        'junction_failures': [{'file': f, 'error': e} for f, e in junction_failures]
    }
    
    with open('diagnostic_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f'\nResults saved to diagnostic_results.json')


if __name__ == '__main__':
    main()