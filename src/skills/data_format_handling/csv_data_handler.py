"""
CSV/Data Handler Skill

Load, transform, and export CSV, TSV, and XLSX tabular data.
"""
import csv
import json
import logging
import os
from io import StringIO, BytesIO
from typing import Any, Dict, List, Optional

import time
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_openpyxl():
    """Safely import openpyxl."""
    try:
        import openpyxl
        return openpyxl
    except ImportError:
        return None


def _get_pandas():
    """Safely import pandas."""
    try:
        import pandas as pd
        return pd
    except ImportError:
        return None


def detect_delimiter(file_path: str) -> str:
    """Detect CSV delimiter."""
    with open(file_path, 'r', encoding='utf-8') as f:
        sample = f.read(1024)
        if '\t' in sample:
            return '\t'
        return ','


def read_csv(file_path: str, delimiter: Optional[str] = None) -> Dict[str, Any]:
    """Read CSV/TSV file."""
    if delimiter is None:
        delimiter = detect_delimiter(file_path)
    
    rows = []
    headers = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter)
        headers = next(reader)
        for row in reader:
            rows.append(dict(zip(headers, row)))
    
    return {"headers": headers, "rows": rows, "row_count": len(rows)}


def read_xlsx(file_path: str) -> Dict[str, Any]:
    """Read XLSX file."""
    wb = _get_openpyxl()
    if wb is None:
        raise ImportError("openpyxl not installed: pip install openpyxl")
    
    workbook = wb.load_workbook(file_path, data_only=True)
    sheet = workbook.active
    
    headers = [cell.value for cell in sheet[1]]
    rows = []
    
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if any(row):
            rows.append(dict(zip(headers, [str(v) if v is not None else '' for v in row])))
    
    return {"headers": headers, "rows": rows, "row_count": len(rows), "sheet": sheet.title}


def write_csv(data: Dict[str, Any], file_path: str, delimiter: str = ',') -> str:
    """Write data to CSV file."""
    headers = data.get("headers", [])
    rows = data.get("rows", [])
    
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)
    
    return file_path


def export_to_json(data: Dict[str, Any], file_path: str) -> str:
    """Export data to JSON."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return file_path


def infer_types(data: Dict[str, Any]) -> Dict[str, Any]:
    """Infer data types for each column."""
    headers = data.get("headers", [])
    rows = data.get("rows", [])
    
    type_hints = {}
    for header in headers:
        values = [row.get(header, '') for row in rows]
        non_empty = [v for v in values if v]
        
        if not non_empty:
            type_hints[header] = "unknown"
        elif all(v.isdigit() for v in non_empty):
            type_hints[header] = "integer"
        elif all(v.replace('.', '').replace('-', '').isdigit() for v in non_empty if v):
            type_hints[header] = "float"
        elif all(v.lower() in ('true', 'false', 'yes', 'no') for v in non_empty):
            type_hints[header] = "boolean"
        else:
            type_hints[header] = "string"
    
    return {"headers": headers, "types": type_hints, "row_count": len(rows)}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for skill invocation."""
    start_time = time.time()
    timestamp = datetime.datetime.now().isoformat()
    
    action = payload.get("action", "read")
    file_path = payload.get("file_path")
    output_path = payload.get("output_path")
    delimiter = payload.get("delimiter")
    
    try:
        if action == "read":
            if not file_path or not os.path.exists(file_path):
                return {"result": {"error": f"File not found: {file_path}"}, "metadata": {"timestamp": timestamp}}
            
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext in ('.csv', '.tsv'):
                data = read_csv(file_path, delimiter)
            elif ext == '.xlsx':
                data = read_xlsx(file_path)
            else:
                return {"result": {"error": f"Unsupported format: {ext}"}, "metadata": {"timestamp": timestamp}}
            
            return {"result": data, "metadata": {"timestamp": timestamp, "format": ext}}
        
        elif action == "write":
            if not file_path or not output_path:
                return {"result": {"error": "file_path and output_path required"}, "metadata": {"timestamp": timestamp}}
            
            ext = os.path.splitext(output_path)[1].lower()
            
            if ext == '.csv':
                write_csv(payload.get("data", {}), output_path, delimiter or ',')
            elif ext == '.json':
                export_to_json(payload.get("data", {}), output_path)
            else:
                return {"result": {"error": f"Unsupported output format: {ext}"}, "metadata": {"timestamp": timestamp}}
            
            return {"result": {"output_file": output_path}, "metadata": {"timestamp": timestamp}}
        
        elif action == "infer_types":
            if not file_path or not os.path.exists(file_path):
                return {"result": {"error": f"File not found: {file_path}"}, "metadata": {"timestamp": timestamp}}
            
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext in ('.csv', '.tsv'):
                data = read_csv(file_path, delimiter)
            elif ext == '.xlsx':
                data = read_xlsx(file_path)
            else:
                return {"result": {"error": f"Unsupported format: {ext}"}, "metadata": {"timestamp": timestamp}}
            
            types = infer_types(data)
            return {"result": types, "metadata": {"timestamp": timestamp}}
        
        else:
            return {"result": {"error": f"Unknown action: {action}", "available": ["read", "write", "infer_types"]}, "metadata": {"timestamp": timestamp}}
    
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"timestamp": timestamp, "error": str(e)}}


def register_skill():
    return {"name": "csv-data-handler", "description": "Load, transform, and export CSV, TSV, and XLSX data", "version": "1.0.0", "domain": "DATA_FORMAT_HANDLING"}
