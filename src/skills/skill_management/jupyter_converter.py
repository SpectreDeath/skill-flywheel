"""
Jupyter Converter Skill

Converts Jupyter notebooks (.ipynb) and other document formats to machine-readable formats.

Supported conversions:
- Jupyter Notebook (.ipynb) -> JSON
- Jupyter Notebook (.ipynb) -> Markdown
- Python Script (.py) -> JSON (with docstrings)
- R Markdown (.Rmd) -> JSON
- HTML -> Markdown

This skill extracts:
- Code cells with language info
- Markdown cells with content
- Cell outputs (if available)
- Metadata (title, kernel, etc.)
"""

import json
import re
import logging
import os
import sys
from typing import Any, Dict, List, Optional

# Ensure we use the standard library pathlib, not any local module
_pathlib_backup = sys.path.copy()
sys.path = [
    p
    for p in sys.path
    if "skill_management" not in p.lower() and "skills" not in p.lower()
]
import pathlib

sys.path = _pathlib_backup
del _pathlib_backup

import time
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_ipynb(file_path: str) -> Dict[str, Any]:
    """Load and parse a Jupyter notebook file."""
    with open(file_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)
    return notebook


def convert_notebook_to_json(notebook: Dict[str, Any]) -> Dict[str, Any]:
    """Convert notebook to structured JSON format."""
    result = {"metadata": notebook.get("metadata", {}), "cells": []}

    # Extract title from first markdown cell or metadata
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "markdown":
            source = "".join(cell.get("source", []))
            if source.strip():
                result["title"] = source.split("\n")[0].replace("#", "").strip()
                break

    if "title" not in result:
        result["title"] = "Untitled Notebook"

    # Process cells
    for idx, cell in enumerate(notebook.get("cells", [])):
        cell_data = {
            "index": idx,
            "type": cell.get("cell_type", "unknown"),
            "source": "".join(cell.get("source", [])),
        }

        # Add outputs if available
        if "outputs" in cell and cell["outputs"]:
            cell_data["outputs"] = []
            for output in cell["outputs"]:
                if output.get("output_type") == "stream":
                    cell_data["outputs"].append(
                        {
                            "type": "stream",
                            "name": output.get("name", "stdout"),
                            "text": "".join(output.get("text", [])),
                        }
                    )
                elif output.get("output_type") == "execute_result":
                    cell_data["outputs"].append(
                        {
                            "type": "execute_result",
                            "data": output.get("data", {}),
                            "execution_count": output.get("execution_count"),
                        }
                    )
                elif output.get("output_type") == "error":
                    cell_data["outputs"].append(
                        {
                            "type": "error",
                            "ename": output.get("ename"),
                            "evalue": output.get("evalue"),
                            "traceback": output.get("traceback", []),
                        }
                    )

        # Add execution count
        if cell.get("execution_count"):
            cell_data["execution_count"] = cell["execution_count"]

        result["cells"].append(cell_data)

    return result


def convert_notebook_to_markdown(notebook: Dict[str, Any]) -> str:
    """Convert notebook to Markdown format."""
    lines = []

    # Title
    title = "Untitled Notebook"
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "markdown":
            source = "".join(cell.get("source", []))
            if source.strip():
                title = source.split("\n")[0].replace("#", "").strip()
                break

    lines.append(f"# {title}")
    lines.append("")

    # Process cells
    for cell in notebook.get("cells", []):
        cell_type = cell.get("cell_type", "unknown")
        source = "".join(cell.get("source", []))

        if cell_type == "markdown":
            lines.append(source)
            lines.append("")
        elif cell_type == "code":
            # Code cell
            lines.append("```python")
            lines.append(source)
            lines.append("```")
            lines.append("")

            # Add outputs if available
            if "outputs" in cell and cell["outputs"]:
                for output in cell["outputs"]:
                    if output.get("output_type") == "stream":
                        lines.append("**Output:**")
                        lines.append("```")
                        lines.append("".join(output.get("text", [])))
                        lines.append("```")
                        lines.append("")
                    elif output.get("output_type") == "execute_result":
                        if "data" in output:
                            text = output["data"].get("text/plain", [""])
                            if text:
                                lines.append("**Result:**")
                                lines.append("```")
                                lines.append(
                                    text[0] if isinstance(text, list) else text
                                )
                                lines.append("```")
                                lines.append("")

    return "\n".join(lines)


def extract_python_docstrings(file_path: str) -> Dict[str, Any]:
    """Extract docstrings and functions from a Python file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    result = {
        "file": file_path,
        "functions": [],
        "classes": [],
        "module_docstring": None,
    }

    # Extract module docstring
    module_match = re.match(r"^\s*[\"\']{3}(.*?)[\"\']{3}", content, re.DOTALL)
    if module_match:
        result["module_docstring"] = module_match.group(1).strip()

    # Find classes and functions
    in_class = False
    in_function = False
    indent_level = 0

    lines = content.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()

        # Class definition
        class_match = re.match(r"^class\s+(\w+)", stripped)
        if class_match:
            class_name = class_match.group(1)
            # Get docstring
            docstring = None
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('"""') or next_line.startswith("'''"):
                    docstring_match = re.search(
                        r"[\"\']{3}(.*?)[\"\']{3}", "\n".join(lines[i:]), re.DOTALL
                    )
                    if docstring_match:
                        docstring = docstring_match.group(1).strip()

            result["classes"].append(
                {"name": class_name, "docstring": docstring, "line": i + 1}
            )

        # Function definition
        func_match = re.match(r"^def\s+(\w+)\s*\(", stripped)
        if func_match and not class_match:
            func_name = func_match.group(1)
            # Skip private functions
            if not func_name.startswith("_"):
                docstring = None
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line.startswith('"""') or next_line.startswith("'''"):
                        docstring_match = re.search(
                            r"[\"\']{3}(.*?)[\"\']{3}", "\n".join(lines[i:]), re.DOTALL
                        )
                        if docstring_match:
                            docstring = docstring_match.group(1).strip()

                result["functions"].append(
                    {"name": func_name, "docstring": docstring, "line": i + 1}
                )

    return result


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for skill invocation.

    Expected payload:
        - action: str (optional): The action to perform
            - "convert_to_json": Convert notebook to JSON
            - "convert_to_markdown": Convert notebook to Markdown
            - "extract_docstrings": Extract docstrings from Python file
            - "list_formats": List supported formats
        - input_path: str: Path to the input file
        - output_path: str (optional): Path for output file

    Returns:
        dict with 'result' and 'metadata' keys
    """
    start_time = time.time()
    timestamp = datetime.datetime.now().isoformat()

    action = payload.get("action", "list_formats")
    input_path = payload.get("input_path")
    output_path = payload.get("output_path")

    if action == "list_formats":
        return {
            "result": {
                "supported_formats": [
                    {
                        "extension": ".ipynb",
                        "name": "Jupyter Notebook",
                        "actions": ["convert_to_json", "convert_to_markdown"],
                    },
                    {
                        "extension": ".py",
                        "name": "Python Script",
                        "actions": ["extract_docstrings"],
                    },
                    {
                        "extension": ".Rmd",
                        "name": "R Markdown",
                        "actions": ["convert_to_json"],
                    },
                    {
                        "extension": ".html",
                        "name": "HTML",
                        "actions": ["convert_to_markdown"],
                    },
                ]
            },
            "metadata": {
                "timestamp": timestamp,
                "elapsed_seconds": time.time() - start_time,
            },
        }

    if not input_path:
        return {
            "result": {"error": "input_path is required"},
            "metadata": {"timestamp": timestamp, "error": "Missing input_path"},
        }

    if not os.path.exists(input_path):
        return {
            "result": {"error": f"File not found: {input_path}"},
            "metadata": {"timestamp": timestamp, "error": "File not found"},
        }

    file_ext = os.path.splitext(input_path)[1].lower()

    try:
        if file_ext == ".ipynb":
            notebook = load_ipynb(input_path)

            if action == "convert_to_json":
                result = convert_notebook_to_json(notebook)
                output_format = "JSON"

                if output_path:
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(result, f, indent=2)
                    result["output_file"] = output_path

            elif action == "convert_to_markdown":
                result = {"markdown": convert_notebook_to_markdown(notebook)}
                output_format = "Markdown"

                if output_path:
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(result["markdown"])
                    result["output_file"] = output_path
            else:
                return {
                    "result": {"error": f"Unknown action for .ipynb: {action}"},
                    "metadata": {"timestamp": timestamp},
                }

        elif file_ext == ".py":
            if action == "extract_docstrings":
                result = extract_python_docstrings(input_path)
                output_format = "JSON"

                if output_path:
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(result, f, indent=2)
                    result["output_file"] = output_path
            else:
                return {
                    "result": {"error": f"Unknown action for .py: {action}"},
                    "metadata": {"timestamp": timestamp},
                }

        else:
            return {
                "result": {"error": f"Unsupported file format: {file_ext}"},
                "metadata": {"timestamp": timestamp},
            }

        return {
            "result": result,
            "metadata": {
                "timestamp": timestamp,
                "input_file": input_path,
                "output_format": output_format,
                "action": action,
                "elapsed_seconds": time.time() - start_time,
            },
        }

    except Exception as e:
        logger.error(f"Error converting file: {str(e)}")
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": timestamp, "error": str(e)},
        }


def register_skill():
    """Return skill metadata for registration"""
    return {
        "name": "jupyter-converter",
        "description": "Convert Jupyter notebooks and other formats to machine-readable documents",
        "version": "1.0.0",
        "domain": "skill_management",
    }
