import json
from pathlib import Path


def scan_tutorials():
    source_dir = Path("AI-Tutorial-Codes-Included-main")
    output_dir = Path("domains/agentic_ai/flywheel_output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    tutorial_catalog = {
        "catalog_metadata": {
            "total_tutorials": 0,
            "file_types": ["*.ipynb", "*.py", "*.md"],
            "scan_date": "2024-01-01",
            "source_directory": str(source_dir)
        },
        "tutorials": [],
        "statistics": {
            "by_type": {},
            "by_category": {},
            "total_lines": 0,
            "total_size": 0
        }
    }
    
    # Scan for Jupyter notebooks
    for notebook in source_dir.rglob("*.ipynb"):
        try:
            with open(notebook, encoding='utf-8') as f:
                notebook_data = json.load(f)
            
            # Extract metadata
            cells = notebook_data.get('cells', [])
            code_cells = [cell for cell in cells if cell['cell_type'] == 'code']
            markdown_cells = [cell for cell in cells if cell['cell_type'] == 'markdown']
            
            tutorial_info = {
                "tutorial_id": notebook.stem,
                "file_path": str(notebook),
                "file_type": "jupyter_notebook",
                "file_size": notebook.stat().st_size,
                "total_cells": len(cells),
                "code_cells": len(code_cells),
                "markdown_cells": len(markdown_cells),
                "languages": [],
                "topics": [],
                "description": "",
                "extracted_content": {
                    "code_snippets": [],
                    "markdown_content": [],
                    "metadata": notebook_data.get('metadata', {})
                }
            }
            
            # Extract code snippets and languages
            for cell in code_cells:
                source = ''.join(cell.get('source', []))
                if source.strip():
                    tutorial_info["extracted_content"]["code_snippets"].append({
                        "cell_number": len(tutorial_info["extracted_content"]["code_snippets"]) + 1,
                        "source": source,
                        "execution_count": cell.get('execution_count')
                    })
            
            # Extract markdown content
            for cell in markdown_cells:
                source = ''.join(cell.get('source', []))
                if source.strip():
                    tutorial_info["extracted_content"]["markdown_content"].append(source)
            
            tutorial_catalog["tutorials"].append(tutorial_info)
            tutorial_catalog["statistics"]["total_lines"] += sum(len(cell.get('source', [])) for cell in cells)
            tutorial_catalog["statistics"]["total_size"] += notebook.stat().st_size
            
            # Update statistics
            file_type = "jupyter_notebook"
            tutorial_catalog["statistics"]["by_type"][file_type] = tutorial_catalog["statistics"]["by_type"].get(file_type, 0) + 1
            
        except Exception as e:
            print(f"Error processing {notebook}: {e}")
    
    # Scan for Python files
    for py_file in source_dir.rglob("*.py"):
        try:
            with open(py_file, encoding='utf-8') as f:
                content = f.read()
            
            tutorial_info = {
                "tutorial_id": py_file.stem,
                "file_path": str(py_file),
                "file_type": "python_script",
                "file_size": py_file.stat().st_size,
                "total_lines": len(content.splitlines()),
                "description": "",
                "extracted_content": {
                    "full_content": content,
                    "functions": [],
                    "classes": [],
                    "imports": []
                }
            }
            
            tutorial_catalog["tutorials"].append(tutorial_info)
            tutorial_catalog["statistics"]["total_lines"] += len(content.splitlines())
            tutorial_catalog["statistics"]["total_size"] += py_file.stat().st_size
            
            # Update statistics
            file_type = "python_script"
            tutorial_catalog["statistics"]["by_type"][file_type] = tutorial_catalog["statistics"]["by_type"].get(file_type, 0) + 1
            
        except Exception as e:
            print(f"Error processing {py_file}: {e}")
    
    # Scan for Markdown files
    for md_file in source_dir.rglob("*.md"):
        try:
            with open(md_file, encoding='utf-8') as f:
                content = f.read()
            
            tutorial_info = {
                "tutorial_id": md_file.stem,
                "file_path": str(md_file),
                "file_type": "markdown",
                "file_size": md_file.stat().st_size,
                "total_lines": len(content.splitlines()),
                "description": "",
                "extracted_content": {
                    "full_content": content,
                    "headings": [],
                    "code_blocks": []
                }
            }
            
            tutorial_catalog["tutorials"].append(tutorial_info)
            tutorial_catalog["statistics"]["total_lines"] += len(content.splitlines())
            tutorial_catalog["statistics"]["total_size"] += md_file.stat().st_size
            
            # Update statistics
            file_type = "markdown"
            tutorial_catalog["statistics"]["by_type"][file_type] = tutorial_catalog["statistics"]["by_type"].get(file_type, 0) + 1
            
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    tutorial_catalog["catalog_metadata"]["total_tutorials"] = len(tutorial_catalog["tutorials"])
    
    # Save catalog
    with open(output_dir / "extracted_tutorial_catalog.json", 'w') as f:
        json.dump(tutorial_catalog, f, indent=2)
    
    print("Tutorial scanning complete!")
    print(f"Total tutorials found: {tutorial_catalog['catalog_metadata']['total_tutorials']}")
    print(f"Total lines of code: {tutorial_catalog['statistics']['total_lines']}")
    print(f"Total size: {tutorial_catalog['statistics']['total_size']} bytes")
    print(f"File types: {tutorial_catalog['statistics']['by_type']}")
    
    return tutorial_catalog

if __name__ == "__main__":
    scan_tutorials()
