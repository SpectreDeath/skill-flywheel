"""
Schema Validator Skill

Validate JSON Schema and OpenAPI specifications.
"""
import json
import logging
import os
import re
import sys
from typing import Any, Dict, List, Optional

import time
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_jsonschema():
    """Safely import jsonschema."""
    try:
        import jsonschema
        return jsonschema
    except ImportError:
        return None


def _get_yaml():
    """Safely import yaml."""
    try:
        import yaml
        return yaml
    except ImportError:
        return None


def load_schema_file(file_path: str) -> Dict[str, Any]:
    """Load schema from file (JSON or YAML)."""
    ext = os.path.splitext(file_path)[1].lower()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        if ext in ('.yaml', '.yml'):
            yaml_mod = _get_yaml()
            if yaml_mod is None:
                raise ImportError("PyYAML not installed")
            return yaml_mod.safe_load(f)
        else:
            return json.load(f)


def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """Validate data against JSON Schema."""
    jsonschema = _get_jsonschema()
    if jsonschema is None:
        raise ImportError("jsonschema not installed: pip install jsonschema")
    
    validator = jsonschema.Draft7Validator(schema)
    errors = []
    
    for error in validator.iter_errors(data):
        errors.append({
            "path": ".".join(str(p) for p in error.path),
            "message": error.message,
            "schema_path": ".".join(str(p) for p in error.schema_path)
        })
    
    return {"valid": len(errors) == 0, "errors": errors}


def validate_openapi(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Basic OpenAPI validation."""
    errors = []
    warnings = []
    
    required = ["openapi", "info", "paths"]
    for field in required:
        if field not in spec:
            errors.append(f"Missing required field: {field}")
    
    if "openapi" in spec:
        if not re.match(r"3\.\d+\.\d+", str(spec["openapi"])):
            warnings.append(f"Unusual OpenAPI version: {spec['openapi']}")
    
    if "paths" in spec:
        for path, path_item in spec["paths"].items():
            if not path.startswith("/"):
                errors.append(f"Path must start with /: {path}")
    
    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


def generate_sample_from_schema(schema: Dict[str, Any]) -> Any:
    """Generate sample data from JSON Schema."""
    schema_type = schema.get("type", "object")
    
    if schema_type == "object":
        result = {}
        properties = schema.get("properties", {})
        for prop, prop_schema in properties.items():
            result[prop] = generate_sample_from_schema(prop_schema)
        return result
    
    elif schema_type == "array":
        item_schema = schema.get("items", {})
        return [generate_sample_from_schema(item_schema)]
    
    elif schema_type == "string":
        return "string"
    
    elif schema_type == "integer":
        return 0
    
    elif schema_type == "number":
        return 0.0
    
    elif schema_type == "boolean":
        return True
    
    return None


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for skill invocation."""
    start_time = time.time()
    timestamp = datetime.datetime.now().isoformat()
    
    action = payload.get("action", "validate")
    schema_path = payload.get("schema_path")
    data_path = payload.get("data_path")
    data = payload.get("data")
    schema = payload.get("schema")
    
    try:
        if action == "validate_json_schema":
            if schema_path:
                if not os.path.exists(schema_path):
                    return {"result": {"error": f"Schema not found: {schema_path}"}, "metadata": {"timestamp": timestamp}}
                schema = load_schema_file(schema_path)
            
            if not schema:
                return {"result": {"error": "schema or schema_path required"}, "metadata": {"timestamp": timestamp}}
            
            if data_path:
                if not os.path.exists(data_path):
                    return {"result": {"error": f"Data file not found: {data_path}"}, "metadata": {"timestamp": timestamp}}
                with open(data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            if not data:
                return {"result": {"error": "data or data_path required"}, "metadata": {"timestamp": timestamp}}
            
            result = validate_json_schema(data, schema)
            return {"result": result, "metadata": {"timestamp": timestamp}}
        
        elif action == "validate_openapi":
            if schema_path:
                if not os.path.exists(schema_path):
                    return {"result": {"error": f"Schema not found: {schema_path}"}, "metadata": {"timestamp": timestamp}}
                spec = load_schema_file(schema_path)
            elif schema:
                spec = schema
            else:
                return {"result": {"error": "schema or schema_path required"}, "metadata": {"timestamp": timestamp}}
            
            result = validate_openapi(spec)
            return {"result": result, "metadata": {"timestamp": timestamp}}
        
        elif action == "generate_sample":
            if schema_path:
                if not os.path.exists(schema_path):
                    return {"result": {"error": f"Schema not found: {schema_path}"}, "metadata": {"timestamp": timestamp}}
                schema = load_schema_file(schema_path)
            
            if not schema:
                return {"result": {"error": "schema or schema_path required"}, "metadata": {"timestamp": timestamp}}
            
            sample = generate_sample_from_schema(schema)
            return {"result": {"sample": sample}, "metadata": {"timestamp": timestamp}}
        
        else:
            return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"timestamp": timestamp}}
    
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"timestamp": timestamp, "error": str(e)}}


def register_skill():
    return {"name": "schema-validator", "description": "Validate JSON Schema and OpenAPI specifications", "version": "1.0.0", "domain": "DATA_FORMAT_HANDLING"}
