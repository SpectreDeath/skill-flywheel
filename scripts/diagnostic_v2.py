"""
Comprehensive diagnostic script to identify skill module failure categories.
Checks all skill files recursively in src/flywheel/skills/ directory.
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
sync_invoke: List[Dict[str, Any]] = []
has_invoke_correct: List[str] = []

def check_module(filepath: Path) -> None:
    """Check a single Python module for issues."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (OSError, PermissionError) as e:
        junction_failures.append((str(filepath), str(e)))
        return
    except Exception as e:
        return
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return
    
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
    
    # Categorize
    if not has_async_invoke and not has_sync_invoke:
        # Type 1: No invoke at all
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
    elif has_sync_invoke and not has_async_invoke:
        # Sync invoke (should be async)
        sync_invoke.append({
            'file': str(filepath),
            'type': 'sync_invoke'
        })
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
                            elif hasattr(k, 's'):
                                keys.append(k.s)
                        if 'result' in keys and 'metadata' in keys:
                            has_correct_format = True
                        elif 'result' in keys and 'metadata' not in keys:
                            has_wrong_format = True
        
        if has_wrong_format and not has_correct_format:
            wrong_format.append({
                'file': str(filepath),
                'has_result': True,
                'has_metadata': False
            })
        elif has_correct_format:
            has_invoke_correct.append(str(filepath))


def main() -> None:
    """Main diagnostic entry point."""
    file_count = 0
    
    # Walk through all Python files
    for root, dirs, files in os.walk(SKILLS_DIR):
        # Skip __pycache__ and .git
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'ARCHIVED']]
        
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                filepath = Path(root) / file
                check_module(filepath)
                file_count += 1
    
    # Print results
    print('=' * 80)
    print('COMPREHENSIVE DIAGNOSTIC RESULTS')
    print('=' * 80)
    print(f'\nTotal skill files scanned: {file_count}')
    
    print(f'\nType 1 - No invoke() function: {len(no_invoke)} modules')
    print('-' * 60)
    
    # Group by category
    cognitive_skills = []
    data_pipelines = []
    openclaw_modules = []
    other_modules = []
    
    for item in sorted(no_invoke, key=lambda x: x['file']):
        filepath = item['file']
        if 'cognitive_skills' in filepath:
            cognitive_skills.append(item)
        elif 'apache_beam' in filepath or 'federated_learning' in filepath:
            data_pipelines.append(item)
        elif 'openclaw' in filepath or 'nemoclaw' in filepath:
            openclaw_modules.append(item)
        else:
            other_modules.append(item)
    
    print(f'\n  Cognitive Skills ({len(cognitive_skills)}):')
    for item in cognitive_skills:
        classes_info = ''
        if item['has_class_with_methods']:
            classes_info = f' [Classes: {", ".join(c[0] for c in item["classes"])}]'
        print(f'    - {item["file"]}{classes_info}')
    
    print(f'\n  Data Pipelines ({len(data_pipelines)}):')
    for item in data_pipelines:
        classes_info = ''
        if item['has_class_with_methods']:
            classes_info = f' [Classes: {", ".join(c[0] for c in item["classes"])}]'
        print(f'    - {item["file"]}{classes_info}')
    
    print(f'\n  OpenClaw/NemoClaw Modules ({len(openclaw_modules)}) [DO NOT TOUCH]:')
    for item in openclaw_modules:
        classes_info = ''
        if item['has_class_with_methods']:
            classes_info = f' [Classes: {", ".join(c[0] for c in item["classes"])}]'
        print(f'    - {item["file"]}{classes_info}')
    
    print(f'\n  Other Modules ({len(other_modules)}):')
    for item in other_modules:
        classes_info = ''
        if item['has_class_with_methods']:
            classes_info = f' [Classes: {", ".join(c[0] for c in item["classes"])}]'
        print(f'    - {item["file"]}{classes_info}')
    
    print(f'\nType 2 - Wrong format (result without metadata): {len(wrong_format)} modules')
    print('-' * 60)
    for item in sorted(wrong_format, key=lambda x: x['file']):
        print(f'  - {item["file"]}')
    
    print(f'\nSync invoke (should be async): {len(sync_invoke)} modules')
    print('-' * 60)
    for item in sorted(sync_invoke, key=lambda x: x['file']):
        print(f'  - {item["file"]}')
    
    print(f'\nCorrect format (has invoke with metadata): {len(has_invoke_correct)} modules')
    
    print(f'\nType 3 - Windows junction failures: {len(junction_failures)} modules')
    print('-' * 60)
    for filepath, error in junction_failures:
        print(f'  - {filepath}: {error}')
    
    print('\n' + '=' * 80)
    print(f'SUMMARY:')
    print(f'  Type 1 (No invoke): {len(no_invoke)} modules')
    print(f'    - Cognitive skills: {len(cognitive_skills)}')
    print(f'    - Data pipelines: {len(data_pipelines)}')
    print(f'    - OpenClaw/NemoClaw: {len(openclaw_modules)} (DO NOT TOUCH)')
    print(f'    - Other: {len(other_modules)}')
    print(f'  Type 2 (Wrong format): {len(wrong_format)} modules')
    print(f'  Sync invoke: {len(sync_invoke)} modules')
    print(f'  Correct: {len(has_invoke_correct)} modules')
    print(f'  Type 3 (Junction failures): {len(junction_failures)} modules')
    print('=' * 80)
    
    # Save results to JSON
    results = {
        'no_invoke': no_invoke,
        'wrong_format': wrong_format,
        'sync_invoke': sync_invoke,
        'junction_failures': [{'file': f, 'error': e} for f, e in junction_failures],
        'correct_format': has_invoke_correct,
        'summary': {
            'total_scanned': file_count,
            'no_invoke': len(no_invoke),
            'wrong_format': len(wrong_format),
            'sync_invoke': len(sync_invoke),
            'correct': len(has_invoke_correct),
            'junction_failures': len(junction_failures),
            'cognitive_skills_no_invoke': len(cognitive_skills),
            'data_pipelines_no_invoke': len(data_pipelines),
            'openclaw_no_invoke': len(openclaw_modules)
        }
    }
    
    with open('diagnostic_results_v2.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f'\nResults saved to diagnostic_results_v2.json')


if __name__ == '__main__':
    main()