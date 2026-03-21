"""
Config Parser Skill

Parse and convert between JSON, YAML, TOML, and ENV configuration formats.
"""
import json
import logging
import os
import sys
from typing import Any, Dict

import time
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_yaml():
    """Safely import yaml."""
    try:
        import yaml
        return yaml
    except ImportError:
        return None


def _get_toml():
    """Safely import tomli/tomllib."""
    try:
        import tomllib
        return tomllib
    except ImportError:
        try:
            import tomli as t
            return t
        except ImportError:
            return None


def parse_json(file_path: str) -> Dict[str, Any]:
    """Parse JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_yaml(file_path: str) -> Dict[str, Any]:
    """Parse YAML file."""
    yaml_mod = _get_yaml()
    if yaml_mod is None:
        raise ImportError("PyYAML not installed: pip install PyYAML")
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml_mod.safe_load(f)


def parse_toml(file_path: str) -> Dict[str, Any]:
    """Parse TOML file."""
    toml_mod = _get_toml()
    if toml_mod is None:
        raise ImportError("toml not installed: pip install tomli")
    with open(file_path, 'rb') as f:
        return toml_mod.load(f)


def parse_env(file_path: str) -> Dict[str, Any]:
    """Parse .env file."""
    config = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    return config


def detect_format(file_path: str) -> str:
    """Detect config format from file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    format_map = {'.json': 'json', '.yaml': 'yaml', '.yml': 'yaml', '.toml': 'toml', '.env': 'env'}
    return format_map.get(ext, 'unknown')


def parse_config(file_path: str) -> Dict[str, Any]:
    """Auto-detect format and parse config file."""
    fmt = detect_format(file_path)
    parsers = {'json': parse_json, 'yaml': parse_yaml, 'toml': parse_toml, 'env': parse_env}
    if fmt not in parsers:
        raise ValueError(f"Unsupported format: {fmt}")
    return parsers[fmt](file_path)


def convert_config(data: Dict[str, Any], to_format: str) -> str:
    """Convert config data to specified format."""
    if to_format == 'json':
        return json.dumps(data, indent=2)
    elif to_format == 'yaml':
        yaml_mod = _get_yaml()
        if yaml_mod is None:
            raise ImportError("PyYAML not installed")
        return yaml_mod.dump(data, default_flow_style=False)
    else:
        raise ValueError(f"Unsupported output format: {to_format}")


def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple config dictionaries (later ones override)."""
    result = {}
    for config in configs:
        result.update(config)
    return result


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for skill invocation."""
    start_time = time.time()
    timestamp = datetime.datetime.now().isoformat()
    
    action = payload.get("action", "parse")
    file_path = payload.get("file_path")
    output_format = payload.get("output_format")
    merge_files = payload.get("merge_files", [])
    
    try:
        if action == "detect_format":
            if not file_path:
                return {"result": {"error": "file_path required"}, "metadata": {"timestamp": timestamp}}
            fmt = detect_format(file_path)
            return {"result": {"format": fmt, "file_path": file_path}, "metadata": {"timestamp": timestamp}}
        
        if action == "parse":
            if not file_path or not os.path.exists(file_path):
                return {"result": {"error": f"File not found: {file_path}"}, "metadata": {"timestamp": timestamp}}
            data = parse_config(file_path)
            fmt = detect_format(file_path)
            return {"result": {"data": data, "format": fmt}, "metadata": {"timestamp": timestamp}}
        
        elif action == "convert":
            if not file_path or not output_format:
                return {"result": {"error": "file_path and output_format required"}, "metadata": {"timestamp": timestamp}}
            data = parse_config(file_path)
            converted = convert_config(data, output_format)
            return {"result": {"data": converted, "to_format": output_format}, "metadata": {"timestamp": timestamp}}
        
        elif action == "merge":
            if not file_path:
                return {"result": {"error": "file_path required"}, "metadata": {"timestamp": timestamp}}
            configs = [parse_config(file_path)]
            for mf in merge_files:
                configs.append(parse_config(mf))
            merged = merge_configs(*configs)
            return {"result": {"merged": merged, "sources": [file_path] + merge_files}, "metadata": {"timestamp": timestamp}}
        
        else:
            return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"timestamp": timestamp}}
    
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"timestamp": timestamp, "error": str(e)}}


def register_skill():
    return {"name": "config-parser", "description": "Parse JSON, YAML, TOML, ENV configs", "version": "1.0.0", "domain": "DATA_FORMAT_HANDLING"}
