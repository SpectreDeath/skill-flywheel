"""
API Documentation Generator

Generates API documentation from Python code snippets using:
- AST analysis for FastAPI, Flask, Django view parsing
- OpenAPI/Swagger and Markdown output formats
- Request/response example generation
"""

import ast
import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List
from datetime import datetime


@dataclass
class Endpoint:
    path: str
    method: str
    function_name: str
    params: List[Dict[str, Any]] = field(default_factory=list)
    return_type: str | None = None
    description: str | None = None
    decorators: List[str] = field(default_factory=list)


def parse_fastapi_endpoint(
    node: ast.FunctionDef, decorators: List[str]
) -> Endpoint | None:
    """Parse a FastAPI endpoint from AST node"""
    path = ""
    method = "GET"

    for dec in decorators:
        if dec.startswith("@app."):
            parts = dec.split(".")
            if len(parts) >= 3:
                method = parts[2].upper()
                path = "/"
        elif dec.startswith("@router."):
            match = re.search(
                r'@router\.(get|post|put|patch|delete|options|head)\(["\']([^"\']+)["\']',
                dec,
            )
            if match:
                method = match.group(1).upper()
                path = match.group(2)
        elif dec.startswith("@app."):
            match = re.search(
                r'@app\.(get|post|put|patch|delete|options|head)\(["\']([^"\']+)["\']',
                dec,
            )
            if match:
                method = match.group(1).upper()
                path = match.group(2)

    if not path:
        return None

    params = []
    for arg in node.args.args:
        param = {"name": arg.arg, "type": "string", "required": True}
        if arg.annotation:
            param["type"] = (
                ast.unparse(arg.annotation) if hasattr(ast, "unparse") else "any"
            )

        if arg in node.args.defaults:
            param["required"] = False
            default_idx = node.args.defaults.index(arg)
            param["default"] = (
                ast.unparse(node.args.defaults[default_idx])
                if hasattr(ast, "unparse")
                else None
            )

        params.append(param)

    returns = None
    if node.returns:
        returns = ast.unparse(node.returns) if hasattr(ast, "unparse") else None

    return Endpoint(
        path=path,
        method=method,
        function_name=node.name,
        params=params,
        return_type=returns,
        decorators=decorators,
    )


def parse_flask_endpoint(
    node: ast.FunctionDef, decorators: List[str]
) -> Endpoint | None:
    """Parse a Flask endpoint from AST node"""
    path = ""
    method = "GET"

    for dec in decorators:
        match = re.search(
            r'@app\.route\(["\']([^"\']+)["\'](?:,\s*methods=\[(["\',\s\w]+)\])?\)', dec
        )
        if match:
            path = match.group(1)
            if match.group(2):
                methods = re.findall(r'["\'](\w+)["\']', match.group(2))
                method = methods[0].upper() if methods else "GET"
            break

        match = re.search(
            r'@(?:app|blueprint)\.(get|post|put|patch|delete)\(["\']([^"\']+)["\']', dec
        )
        if match:
            method = match.group(1).upper()
            path = match.group(2)
            break

    if not path:
        return None

    params = []
    for arg in node.args.args:
        param = {"name": arg.arg, "type": "string", "required": True}
        if arg.annotation:
            param["type"] = (
                ast.unparse(arg.annotation) if hasattr(ast, "unparse") else "any"
            )

        if arg in node.args.defaults:
            param["required"] = False
            default_idx = node.args.defaults.index(arg)
            param["default"] = (
                ast.unparse(node.args.defaults[default_idx])
                if hasattr(ast, "unparse")
                else None
            )

        params.append(param)

    returns = None
    if node.returns:
        returns = ast.unparse(node.returns) if hasattr(ast, "unparse") else None

    return Endpoint(
        path=path,
        method=method,
        function_name=node.name,
        params=params,
        return_type=returns,
        decorators=decorators,
    )


def parse_django_view(
    node: ast.FunctionDef, decorators: List[str]
) -> Endpoint | None:
    """Parse a Django view from AST node"""
    path = ""
    method = "GET"

    for dec in decorators:
        match = re.search(
            r'@route\(["\']([^"\']+)["\'](?:,\s*method=["\'](\w+)["\'])?', dec
        )
        if match:
            path = match.group(1)
            if match.group(2):
                method = match.group(2).upper()
            break

        if "login_required" in dec or "require" in dec:
            match_method = re.search(
                r'require_(?:http_method|method)\(["\'](\w+)["\']', dec
            )
            if match_method:
                method = match_method.group(1).upper()

    if not path:
        return None

    params = []
    for arg in node.args.args:
        param = {"name": arg.arg, "type": "string", "required": True}
        if arg.annotation:
            param["type"] = (
                ast.unparse(arg.annotation) if hasattr(ast, "unparse") else "any"
            )

        if arg in node.args.defaults:
            param["required"] = False
            default_idx = node.args.defaults.index(arg)
            param["default"] = (
                ast.unparse(node.args.defaults[default_idx])
                if hasattr(ast, "unparse")
                else None
            )

        params.append(param)

    returns = None
    if node.returns:
        returns = ast.unparse(node.returns) if hasattr(ast, "unparse") else None

    return Endpoint(
        path=path,
        method=method,
        function_name=node.name,
        params=params,
        return_type=returns,
        decorators=decorators,
    )


def detect_framework(code: str) -> str:
    """Detect the API framework from code"""
    if "FastAPI" in code or "fastapi" in code or "@app" in code and "router" in code:
        return "fastapi"
    elif "Flask" in code or "flask" in code or "@app.route" in code:
        return "flask"
    elif "django" in code.lower() or "views.py" in code or "HttpResponse" in code:
        return "django"
    return "fastapi"


def parse_api_code(code: str) -> List[Endpoint]:
    """Parse API code and extract endpoints"""
    endpoints = []
    framework = detect_framework(code)

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return endpoints

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            decorators = []
            for dec in node.decorator_list:
                try:
                    dec_str = ast.unparse(dec) if hasattr(ast, "unparse") else ""
                    decorators.append(dec_str)
                except:
                    pass

            endpoint = None
            if framework == "fastapi":
                endpoint = parse_fastapi_endpoint(node, decorators)
            elif framework == "flask":
                endpoint = parse_flask_endpoint(node, decorators)
            elif framework == "django":
                endpoint = parse_django_view(node, decorators)

            if endpoint:
                endpoints.append(endpoint)

    return endpoints


def generate_openapi(endpoints: List[Endpoint], title: str = "API") -> Dict[str, Any]:
    """Generate OpenAPI/Swagger documentation"""
    openapi_doc = {
        "openapi": "3.0.0",
        "info": {
            "title": title,
            "version": "1.0.0",
            "description": "Auto-generated API documentation",
        },
        "paths": {},
    }

    for ep in endpoints:
        path_item = {
            ep.method.lower(): {
                "summary": ep.function_name,
                "operationId": ep.function_name,
                "parameters": [],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {"application/json": {"schema": {"type": "object"}}},
                    }
                },
            }
        }

        for param in ep.params:
            param_obj = {
                "name": param["name"],
                "in": "query",
                "required": param.get("required", True),
                "schema": {"type": param.get("type", "string")},
            }
            if "description" in param:
                param_obj["description"] = param["description"]
            if "default" in param:
                param_obj["schema"]["default"] = param["default"]

            path_item[ep.method.lower()]["parameters"].append(param_obj)

        if ep.return_type:
            path_item[ep.method.lower()]["responses"]["200"]["content"][
                "application/json"
            ]["schema"] = {"type": ep.return_type}

        openapi_doc["paths"][ep.path] = path_item

    return openapi_doc


def generate_markdown(
    endpoints: List[Endpoint], title: str = "API Documentation"
) -> str:
    """Generate Markdown documentation"""
    md = [f"# {title}\n"]
    md.append("## Endpoints\n")

    for ep in endpoints:
        md.append(f"### `{ep.method} {ep.path}`\n")
        md.append(f"**Function:** `{ep.function_name}`\n")

        if ep.description:
            md.append(f"\n{ep.description}\n")

        if ep.params:
            md.append("\n**Parameters:**\n")
            md.append("| Name | Type | Required | Description |\n")
            md.append("|------|------|----------|-------------|\n")
            for param in ep.params:
                required = "Yes" if param.get("required", True) else "No"
                desc = param.get("description", "")
                md.append(
                    f"| {param['name']} | {param.get('type', 'string')} | {required} | {desc} |\n"
                )

        if ep.return_type:
            md.append(f"\n**Return Type:** `{ep.return_type}`\n")

        md.append("\n---\n")

    return "\n".join(md)


def generate_examples(endpoints: List[Endpoint]) -> List[Dict[str, Any]]:
    """Generate request/response examples"""
    examples = []

    for ep in endpoints:
        example = {
            "endpoint": f"{ep.method} {ep.path}",
            "function": ep.function_name,
            "request": {
                "method": ep.method,
                "url": f"http://localhost:8000{ep.path}",
                "headers": {"Content-Type": "application/json"},
            },
            "parameters": {},
        }

        for param in ep.params:
            param_name = param["name"]
            param_type = param.get("type", "string")

            if param_type == "int":
                example["parameters"][param_name] = 0
            elif param_type == "float":
                example["parameters"][param_name] = 0.0
            elif param_type == "bool":
                example["parameters"][param_name] = True
            elif param_type == "list":
                example["parameters"][param_name] = []
            elif param_type == "dict":
                example["parameters"][param_name] = {}
            else:
                example["parameters"][param_name] = "string"

        if ep.return_type:
            if "List" in ep.return_type or "list" in ep.return_type:
                example["response"] = [{"id": 1, "name": "example"}]
            elif "Dict" in ep.return_type or "dict" in ep.return_type:
                example["response"] = {"id": 1, "name": "example"}
            elif "int" in ep.return_type:
                example["response"] = 1
            elif "str" in ep.return_type:
                example["response"] = "example"
            elif "bool" in ep.return_type:
                example["response"] = True
            else:
                example["response"] = {"message": "success"}
        else:
            example["response"] = {"message": "success"}

        example["curl"] = build_curl_command(ep, example["parameters"])

        examples.append(example)

    return examples


def build_curl_command(endpoint: Endpoint, params: Dict[str, Any]) -> str:
    """Build a curl command for the endpoint"""
    method = endpoint.method
    url = f"http://localhost:8000{endpoint.path}"

    if params:
        query_params = "&".join([f"{k}={v}" for k, v in params.items()])
        url_with_params = f"{url}?{query_params}"
    else:
        url_with_params = url

    curl = f'curl -X {method} "{url_with_params}"'

    if method in ["POST", "PUT", "PATCH"]:
        curl += ' -H "Content-Type: application/json"'
        if params:
            curl += f" -d '{json.dumps(params, indent=2)}'"

    return curl


def api_doc_generator(code: str, options: dict = None) -> dict:
    """
    Main function to generate API documentation.

    Args:
        code: API source code (FastAPI, Flask, or Django)
        options: Output format options
            - format: "openapi" or "markdown" (default: "openapi")
            - title: API title for documentation

    Returns:
        dict with status, endpoints, documentation, and examples
    """
    if not code:
        return {
            "status": "error",
            "error": "No code provided",
            "endpoints": [],
            "documentation": "",
            "examples": [],
        }

    options = options or {}
    output_format = options.get("format", "openapi")
    title = options.get("title", "API Documentation")

    endpoints = parse_api_code(code)

    if not endpoints:
        return {
            "status": "error",
            "error": "No API endpoints found in code",
            "endpoints": [],
            "documentation": "",
            "examples": [],
        }

    endpoints_data = []
    for ep in endpoints:
        endpoints_data.append(
            {
                "path": ep.path,
                "method": ep.method,
                "function": ep.function_name,
                "parameters": ep.params,
                "return_type": ep.return_type,
                "decorators": ep.decorators,
            }
        )

    if output_format == "markdown":
        documentation = generate_markdown(endpoints, title)
    else:
        openapi_doc = generate_openapi(endpoints, title)
        documentation = json.dumps(openapi_doc, indent=2)

    examples = generate_examples(endpoints)

    return {
        "status": "success",
        "endpoints": endpoints_data,
        "documentation": documentation,
        "examples": examples,
        "format": output_format,
        "framework": detect_framework(code),
    }


async def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "generate")
    code = payload.get("code", "")
    options = payload.get("options", {})

    if action == "generate":
        result = api_doc_generator(code, options)
    elif action == "detect":
        result = {"status": "success", "framework": detect_framework(code)}
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return{
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
def register_skill():
    """Return skill metadata"""
    return {
        "name": "api-doc-generator",
        "description": "Generate API documentation from FastAPI, Flask, or Django code",
        "version": "1.0.0",
        "domain": "DOCUMENTATION",
        "capabilities": [
            "parse_fastapi",
            "parse_flask",
            "parse_django",
            "generate_openapi",
            "generate_markdown",
            "generate_examples",
        ],
    }
