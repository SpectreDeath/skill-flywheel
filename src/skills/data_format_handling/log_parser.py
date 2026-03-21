"""
Log Parser Skill

Parse and analyze log files.
"""
import json
import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOG_PATTERNS = {
    "timestamp": r"(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2})",
    "level": r"\b(DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL|FATAL|TRACE)\b",
    "ip": r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b",
    "email": r"[\w.-]+@[\w.-]+\.\w+",
    "url": r"https?://[^\s]+",
}

def parse_log_line(line: str) -> Dict[str, Any]:
    """Parse a single log line."""
    result = {"raw": line, "timestamp": None, "level": None, "fields": {}}
    
    ts_match = re.search(LOG_PATTERNS["timestamp"], line)
    if ts_match:
        result["timestamp"] = ts_match.group(1)
    
    lvl_match = re.search(LOG_LEVEL := LOG_PATTERNS["level"], line, re.IGNORECASE)
    if lvl_match:
        result["level"] = lvl_match.group(1).upper()
    
    return result

def parse_log_file(file_path: str) -> Dict[str, Any]:
    """Parse entire log file."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    entries = []
    levels = {}
    
    for line in lines:
        if line.strip():
            entry = parse_log_line(line)
            entries.append(entry)
            if entry.get("level"):
                levels[entry["level"]] = levels.get(entry["level"], 0) + 1
    
    return {"entries": entries, "total": len(entries), "levels": levels}

def parse_syslog(file_path: str) -> Dict[str, Any]:
    """Parse syslog format."""
    entries = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = re.match(r"^(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(.*)$", line)
            if match:
                entries.append({"timestamp": match.group(1), "host": match.group(2), "message": match.group(3)})
    
    return {"entries": entries, "format": "syslog", "total": len(entries)}

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()
    timestamp = datetime.now().isoformat()
    
    action = payload.get("action", "parse")
    file_path = payload.get("file_path")
    
    try:
        if not file_path or not os.path.exists(file_path):
            return {"result": {"error": f"File not found: {file_path}"}, "metadata": {"timestamp": timestamp}}
        
        if action == "parse":
            data = parse_log_file(file_path)
            return {"result": data, "metadata": {"timestamp": timestamp}}
        
        elif action == "parse_syslog":
            data = parse_syslog(file_path)
            return {"result": data, "metadata": {"timestamp": timestamp}}
        
        elif action == "count_levels":
            data = parse_log_file(file_path)
            return {"result": {"levels": data["levels"]}, "metadata": {"timestamp": timestamp}}
        
        else:
            return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"timestamp": timestamp}}
    
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"timestamp": timestamp}}

def register_skill():
    return {"name": "log-parser", "description": "Parse and analyze log files", "version": "1.0.0", "domain": "DATA_FORMAT_HANDLING"}
