"""
SQL Handler Skill

Extract schemas and query SQL dumps and SQLite databases.
"""
import json
import logging
import os
import re
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_schema_from_sql(sql_content: str) -> Dict[str, Any]:
    """Extract table schemas from SQL dump."""
    tables = {}
    current_table = None
    current_columns = []
    
    for line in sql_content.split('\n'):
        create_match = re.match(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`\"]?(\w+)[`\"]?", line, re.IGNORECASE)
        if create_match:
            if current_table:
                tables[current_table] = current_columns
            current_table = create_match.group(1)
            current_columns = []
        
        col_match = re.match(r"\s+([`\"]?\w+[`\"]?)\s+(\w+(?:\([^)]+\))?)", line)
        if col_match and current_table:
            current_columns.append({"name": col_match.group(1), "type": col_match.group(2)})
    
    if current_table:
        tables[current_table] = current_columns
    
    return {"tables": tables, "count": len(tables)}

def extract_tables_from_db(db_path: str) -> Dict[str, Any]:
    """Extract table info from SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    tables = {}
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    
    for row in cursor.fetchall():
        table_name = row[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = []
        for col in cursor.fetchall():
            columns.append({"name": col[1], "type": col[2], "nullable": not col[3], "default": col[4], "pk": col[5]})
        tables[table_name] = columns
    
    conn.close()
    return {"tables": tables, "count": len(tables)}

def parse_sql_queries(sql_content: str) -> List[Dict[str, Any]]:
    """Parse SQL queries from content."""
    queries = []
    for match in re.finditer(r"(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)\s+.*?;", sql_content, re.IGNORECASE | re.DOTALL):
        query = match.group(0).strip()
        queries.append({"query": query[:100], "type": query.split()[0].upper() if query else "UNKNOWN"})
    return queries

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()
    timestamp = datetime.now().isoformat()
    
    action = payload.get("action", "extract_schema")
    file_path = payload.get("file_path")
    
    try:
        if not file_path or not os.path.exists(file_path):
            return {"result": {"error": f"File not found: {file_path}"}, "metadata": {"timestamp": timestamp}}
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if action == "extract_schema":
            if ext == ".db" or ext == ".sqlite":
                data = extract_tables_from_db(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    sql = f.read()
                data = extract_schema_from_sql(sql)
            return {"result": data, "metadata": {"timestamp": timestamp}}
        
        elif action == "parse_queries":
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                sql = f.read()
            queries = parse_sql_queries(sql)
            return {"result": {"queries": queries, "count": len(queries)}, "metadata": {"timestamp": timestamp}}
        
        else:
            return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"timestamp": timestamp}}
    
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"timestamp": timestamp}}

def register_skill():
    return {"name": "sql-handler", "description": "Extract schemas from SQL dumps and SQLite databases", "version": "1.0.0", "domain": "DATA_FORMAT_HANDLING"}
