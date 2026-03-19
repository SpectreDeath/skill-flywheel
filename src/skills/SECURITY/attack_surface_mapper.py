"""
Attack Surface Mapper - Security Analysis Tool

Maps attack surfaces in application code by:
- Detecting endpoints and entry points
- Identifying input vectors
- Analyzing authentication and authorization
- Mapping data flow
- Scoring exposure levels
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RiskLevel(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"


@dataclass
class Endpoint:
    path: str
    method: str
    file: str
    line: int
    parameters: List[str] = field(default_factory=list)
    auth_required: bool = False
    auth_type: str = "unknown"
    is_internal: bool = False
    risk_score: int = 0


@dataclass
class InputPoint:
    name: str
    location: str
    source: str
    type: str
    sanitized: bool = False
    risk_level: str = "Medium"
    validators: List[str] = field(default_factory=list)


@dataclass
class AuthGap:
    issue: str
    location: str
    severity: str
    description: str
    recommendation: str


@dataclass
class DataFlow:
    source: str
    destination: str
    sanitized: bool
    risk_points: List[str] = field(default_factory=list)


ENDPOINT_PATTERNS = {
    "python_fastapi": [
        (r"@app\.(get|post|put|delete|patch)\([\"']([^\"']+)[\"']", "fastapi"),
        (r"@router\.(get|post|put|delete|patch)\([\"']([^\"']+)[\"']", "fastapi"),
        (r"@app\.route\([\"']([^\"']+)[\"'].*methods\s*=\s*\[([^\]]+)\]", "flask"),
    ],
    "python_flask": [
        (r"@app\.route\([\"']([^\"']+)[\"']", "flask"),
        (r"@route\([\"']([^\"']+)[\"']", "flask"),
    ],
    "express": [
        (
            r"(?:app|router)\.(get|post|put|delete|patch|options)\([\"']([^\"']+)[\"']",
            "express",
        ),
        (r"(?:app|router)\[\"([^\"']+)\"\]\([\"']([^\"']+)[\"']", "express"),
    ],
    "django": [
        (r"path\([\"']([^\"']+)[\"']\s*,\s*([^\)]+)\)", "django"),
        (r"re_path\(r[\"'](\^.*?)[\"']", "django"),
    ],
    "spring": [
        (
            r"@(?:GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping)\([\"']([^\"']+)[\"']",
            "spring",
        ),
        (r"@RequestMapping\(value\s*=\s*[\"']([^\"']+)[\"']", "spring"),
    ],
    "go_gin": [
        (r"(?:r\.Get|r\.Post|r\.Put|r\.Delete|r\.Patch)\([\"']([^\"']+)[\"']", "gin"),
        (r"(?:router|group)\.(Get|Post|Put|Delete|Patch)\([\"']([^\"']+)[\"']", "gin"),
    ],
    "node_express": [
        (r"server\.(get|post|put|delete|patch)\([\"']([^\"']+)[\"']", "express"),
    ],
    "ruby_rails": [
        (r"get\s+[\"']([^\"']+)[\"']", "rails"),
        (r"post\s+[\"']([^\"']+)[\"']", "rails"),
        (r"put\s+[\"']([^\"']+)[\"']", "rails"),
        (r"delete\s+[\"']([^\"']+)[\"']", "rails"),
    ],
    "java_servlet": [
        (r"@WebServlet\([\"']([^\"']+)[\"']", "servlet"),
        (
            r"@(GetMapping|PostMapping|PutMapping|DeleteMapping)\([\"']([^\"']+)[\"']",
            "spring",
        ),
    ],
}

INPUT_PATTERNS = {
    "query_params": [
        (r"request\.query\[[\"']([^\"']+)[\"']", "query"),
        (r"request\.args\.get\([\"']([^\"']+)[\"']", "query"),
        (r"req\.query\[[\"']([^\"']+)[\"']", "query"),
        (r"req\.params\.([a-zA-Z_][a-zA-Z0-9_]*)", "path"),
        (r"@PathVariable\s*(?:\([^)]*\))?\s*([a-zA-Z_][a-zA-Z0-9_]*)", "path"),
        (r"@RequestParam\s*(?:\([^)]*\))?\s*([a-zA-Z_][a-zA-Z0-9_]*)", "query"),
    ],
    "body_input": [
        (r"request\.body", "body"),
        (r"request\.json", "body"),
        (r"req\.body", "body"),
        (r"req\.body\.", "body"),
        (r"@RequestBody\s+([a-zA-Z_][a-zA-Z0-9_]*)", "body"),
        (r"@ModelAttribute\s+([a-zA-Z_][a-zA-Z0-9_]*)", "body"),
    ],
    "header_input": [
        (r"request\.headers\[[\"']([^\"']+)[\"']", "header"),
        (r"req\.headers\[[\"']([^\"']+)[\"']", "header"),
        (r"request\.getHeader\([\"']([^\"']+)[\"']", "header"),
    ],
    "cookie_input": [
        (r"request\.cookies\[[\"']([^\"']+)[\"']", "cookie"),
        (r"req\.cookies\[[\"']([^\"']+)[\"']", "cookie"),
    ],
    "form_input": [
        (r"request\.form\[[\"']([^\"']+)[\"']", "form"),
        (r"req\.body\[[\"']([^\"']+)[\"']", "form"),
    ],
}

AUTH_PATTERNS = {
    "decorators": [
        (r"@require_auth", "custom"),
        (r"@login_required", "django"),
        (r"@auth_required", "custom"),
        (r"@authenticated", "custom"),
        (r"@jwt_required", "jwt"),
        (r"@token_required", "token"),
        (r"@auth", "custom"),
    ],
    "middleware": [
        (r"authMiddleware", "custom"),
        (r"authenticateToken", "custom"),
        (r"verifyToken", "jwt"),
        (r"checkAuth", "custom"),
        (r"ensureAuthenticated", "custom"),
    ],
    "session": [
        (r"session\[[\"']user[\"']", "session"),
        (r"req\.session", "session"),
        (r"request\.session", "session"),
    ],
    "jwt": [
        (r"jwt\.verify", "jwt"),
        (r"JWT\(.*\)\.decode", "jwt"),
        (r"verify_jwt_token", "jwt"),
    ],
    "oauth": [
        (r"oauth2", "oauth"),
        (r"OAuth2", "oauth"),
    ],
    "api_key": [
        (r"x-api-key", "api_key"),
        (r"API_KEY", "api_key"),
        (r"api_key", "api_key"),
    ],
}

SANITIZATION_PATTERNS = {
    "input_validation": [
        (r"validateInput", "validation"),
        (r"sanitize", "sanitization"),
        (r"escape", "sanitization"),
        (r"validate\(", "validation"),
        (r"checkInput", "validation"),
    ],
    "orm_protection": [
        (r"\.filter\(", "orm"),
        (r"\.where\(", "orm"),
        (r"parameterized", "orm"),
        (r"prepared.*statement", "orm"),
    ],
    "encoding": [
        (r"html\.escape", "encoding"),
        (r"encodeForHTML", "encoding"),
        (r"urlencode", "encoding"),
    ],
    "framework": [
        (r"@valid", "validation"),
        (r"@validated", "validation"),
        (r"@NotNull", "validation"),
        (r"@NotBlank", "validation"),
        (r"@Size", "validation"),
        (r"Pydantic", "validation"),
    ],
}


def detect_language(code: str) -> str:
    """Detect the programming language of the code."""
    if "fastapi" in code.lower() or "uvicorn" in code.lower():
        return "python_fastapi"
    elif "flask" in code.lower() or "from flask" in code.lower():
        return "python_flask"
    elif "express" in code.lower() or "express()" in code.lower():
        return "express"
    elif "django" in code.lower() or "from django" in code.lower():
        return "django"
    elif "@spring" in code.lower() or "springframework" in code.lower():
        return "spring"
    elif "gin." in code.lower() or 'gin "github.com/gin-gonic/gin"' in code.lower():
        return "go_gin"
    elif "rails" in code.lower() or "Rails" in code:
        return "ruby_rails"
    elif "servlet" in code.lower() or "@WebServlet" in code:
        return "java_servlet"
    return "unknown"


def detect_endpoints(code: str, include_internal: bool = False) -> List[Dict]:
    """Detect API endpoints and routes in the code."""
    endpoints = []
    language = detect_language(code)
    lines = code.split("\n")

    patterns = ENDPOINT_PATTERNS.get(language, [])
    if language == "unknown":
        for pattern_list in ENDPOINT_PATTERNS.values():
            patterns.extend(pattern_list)

    seen_endpoints = set()

    for line_num, line in enumerate(lines, 1):
        for pattern, framework in patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                groups = match.groups()
                if len(groups) >= 2:
                    method = (
                        groups[0]
                        if groups[0]
                        in ["get", "post", "put", "delete", "patch", "options"]
                        else "unknown"
                    )
                    path = groups[1] if len(groups) > 1 else groups[0]
                elif len(groups) == 1:
                    method = "unknown"
                    path = groups[0]
                else:
                    continue

                endpoint_key = f"{method}:{path}"
                if endpoint_key in seen_endpoints:
                    continue
                seen_endpoints.add(endpoint_key)

                params = re.findall(r"<([^>]+)>|:([a-zA-Z_][a-zA-Z0-9_]*)", path)

                auth_required = False
                auth_type = "none"
                for auth_pattern, auth_name in sum(
                    [
                        list(p.items())
                        if isinstance(p, dict)
                        else p.items()
                        if hasattr(p, "items")
                        else []
                        for p in [AUTH_PATTERNS]
                    ],
                    [],
                ):
                    if isinstance(AUTH_PATTERNS, dict):
                        for ap, at in AUTH_PATTERNS.items():
                            for p, n in at:
                                if re.search(p, line):
                                    auth_required = True
                                    auth_type = n
                                    break

                is_internal = (
                    "/internal/" in path or "/admin/" in path or path.startswith("/_")
                )

                risk_score = calculate_endpoint_risk(
                    method, path, auth_required, is_internal
                )

                endpoints.append(
                    {
                        "path": path,
                        "method": method.upper(),
                        "file": "analyzed",
                        "line": line_num,
                        "parameters": params,
                        "auth_required": auth_required,
                        "auth_type": auth_type,
                        "is_internal": is_internal,
                        "risk_score": risk_score,
                    }
                )

    if not include_internal:
        endpoints = [e for e in endpoints if not e.get("is_internal", False)]

    return endpoints


def calculate_endpoint_risk(
    method: str, path: str, auth_required: bool, is_internal: bool
) -> int:
    """Calculate risk score for an endpoint."""
    score = 0

    if method in ["POST", "PUT", "PATCH"]:
        score += 20
    elif method == "DELETE":
        score += 25

    if ":id" in path or ":slug" in path or "<id>" in path:
        score += 15

    if "/admin" in path or "/manage" in path:
        score += 10

    if not auth_required:
        score += 30

    if "file" in path or "upload" in path:
        score += 20

    if "auth" in path or "login" in path or "register" in path:
        score += 15

    return min(score, 100)


def identify_inputs(code: str, options: Optional[Dict] = None) -> List[Dict]:
    """Identify input points in the code."""
    inputs = []
    depth = options.get("depth", 1) if options else 1

    seen_inputs = set()

    for category, patterns in INPUT_PATTERNS.items():
        for pattern, input_type in patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                input_name = match.group(1) if match.groups() else "unknown"

                input_key = f"{input_type}:{input_name}"
                if input_key in seen_inputs:
                    continue
                seen_inputs.add(input_key)

                line_num = code[: match.start()].count("\n") + 1

                sanitized = is_input_sanitized(code, input_name, line_num)

                risk = "Medium"
                if not sanitized:
                    if input_type in ["body", "query"]:
                        risk = "High"
                    elif input_type == "header":
                        risk = "Medium"
                    elif input_type == "cookie":
                        risk = "High"

                validators = find_validators(code, input_name)

                inputs.append(
                    {
                        "name": input_name,
                        "location": f"line {line_num}",
                        "source": input_type,
                        "type": determine_input_type(input_name),
                        "sanitized": sanitized,
                        "risk_level": risk,
                        "validators": validators,
                    }
                )

    return inputs


def is_input_sanitized(code: str, input_name: str, line_num: int) -> bool:
    """Check if input is sanitized."""
    lines = code.split("\n")
    context_start = max(0, line_num - 10)
    context_end = min(len(lines), line_num + 10)
    context = "\n".join(lines[context_start:context_end])

    for category, patterns in SANITIZATION_PATTERNS.items():
        for pattern, _ in patterns:
            if re.search(pattern, context, re.IGNORECASE):
                return True
    return False


def find_validators(code: str, input_name: str) -> List[str]:
    """Find validators applied to an input."""
    validators = []

    validation_patterns = [
        r"@Valid",
        r"@NotNull",
        r"@NotBlank",
        r"@Size",
        r"@Min",
        r"@Max",
        r"@Pattern",
        r"validate.*" + re.escape(input_name),
        re.escape(input_name) + r".*validate",
    ]

    for pattern in validation_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            validators.append(pattern)

    return validators[:5]


def determine_input_type(input_name: str) -> str:
    """Determine the type of input based on its name."""
    name_lower = input_name.lower()

    if any(x in name_lower for x in ["email", "mail"]):
        return "email"
    elif any(x in name_lower for x in ["password", "pwd", "pass"]):
        return "password"
    elif any(x in name_lower for x in ["name", "username", "user"]):
        return "string"
    elif any(x in name_lower for x in ["id", "uid", "uuid"]):
        return "identifier"
    elif any(x in name_lower for x in ["url", "uri", "link"]):
        return "url"
    elif any(x in name_lower for x in ["file", "attachment", "image", "photo"]):
        return "file"
    elif any(x in name_lower for x in ["phone", "tel", "mobile"]):
        return "phone"
    elif any(x in name_lower for x in ["age", "count", "num", "quantity", "price"]):
        return "number"
    elif any(x in name_lower for x in ["date", "time", "created", "updated"]):
        return "datetime"

    return "unknown"


def analyze_auth(code: str) -> List[Dict]:
    """Analyze authentication and authorization in the code."""
    auth_gaps = []

    has_auth = False
    auth_type = "none"

    for category, patterns in AUTH_PATTERNS.items():
        for pattern, name in patterns:
            if re.search(pattern, code, re.IGNORECASE):
                has_auth = True
                if category in ["jwt", "oauth", "api_key"]:
                    auth_type = category

    endpoint_lines = []
    for line_num, line in enumerate(code.split("\n"), 1):
        for patterns in ENDPOINT_PATTERNS.values():
            for pattern, _ in patterns:
                if re.search(pattern, line):
                    endpoint_lines.append((line_num, line))

    unprotected = 0
    for line_num, line in endpoint_lines:
        has_auth_check = False
        for category, patterns in AUTH_PATTERNS.items():
            for pattern, _ in patterns:
                if re.search(pattern, line):
                    has_auth_check = True

        if not has_auth_check:
            unprotected += 1
            if unprotected <= 3:
                auth_gaps.append(
                    {
                        "issue": "Unprotected endpoint",
                        "location": f"line {line_num}",
                        "severity": "High",
                        "description": "Endpoint may lack authentication",
                        "recommendation": "Add authentication middleware or decorator",
                    }
                )

    if not has_auth:
        auth_gaps.append(
            {
                "issue": "No authentication detected",
                "location": "application",
                "severity": "Critical",
                "description": "No authentication mechanisms found in code",
                "recommendation": "Implement authentication (JWT, OAuth, session-based)",
            }
        )

    if re.search(r"password\s*=\s*['\"][^'\"]+['\"]", code, re.IGNORECASE):
        auth_gaps.append(
            {
                "issue": "Hardcoded password",
                "location": "code",
                "severity": "Critical",
                "description": "Hardcoded password detected",
                "recommendation": "Use environment variables or secrets manager",
            }
        )

    if re.search(r"\.query\([^)]*\+[^)]*\)", code):
        auth_gaps.append(
            {
                "issue": "Potential SQL injection",
                "location": "database queries",
                "severity": "Critical",
                "description": "String concatenation in SQL query detected",
                "recommendation": "Use parameterized queries or ORM",
            }
        )

    if re.search(r"exec\s*\(|eval\s*\(|spawn\s*\(", code):
        auth_gaps.append(
            {
                "issue": "Dangerous code execution",
                "location": "code",
                "severity": "Critical",
                "description": "Dangerous function calls that execute code",
                "recommendation": "Avoid eval/exec or sanitize all inputs strictly",
            }
        )

    return auth_gaps


def map_data_flow(code: str, depth: int = 1) -> List[Dict]:
    """Map how data flows through the system."""
    data_flows = []

    input_sources = [
        ("request.body", "body"),
        ("request.query", "query"),
        ("request.params", "path"),
        ("request.headers", "header"),
        ("req.body", "body"),
        ("req.query", "query"),
        ("req.params", "path"),
    ]

    sinks = [
        (
            "database",
            ["filter", "where", "save", "insert", "update", "delete", "execute"],
        ),
        ("response", ["send", "json", "render", "return"]),
        ("file", ["write", "open", "create", "save"]),
        ("external", ["fetch", "axios", "http", "request"]),
    ]

    for source, source_type in input_sources:
        if source in code:
            for sink_name, sink_keywords in sinks:
                for keyword in sink_keywords:
                    if f".{keyword}(" in code or f"{keyword}(" in code:
                        sanitized = is_sanitized_in_flow(code, source, keyword)

                        risk_points = []
                        if not sanitized:
                            risk_points.append(f"unsanitized flow from {source_type}")
                        if sink_name == "database" and not sanitized:
                            risk_points.append("potential injection")

                        data_flows.append(
                            {
                                "source": source,
                                "destination": sink_name,
                                "sanitized": sanitized,
                                "risk_points": risk_points,
                            }
                        )

    db_operations = re.findall(
        r"\.(filter|where|query|execute|save|create)\([^)]*\)", code
    )
    if db_operations:
        data_flows.append(
            {
                "source": "user_input",
                "destination": "database",
                "sanitized": is_input_sanitized(code, "", 1),
                "risk_points": ["check query parameterization"],
            }
        )

    return data_flows[:20]


def is_sanitized_in_flow(code: str, source: str, sink: str) -> bool:
    """Check if data is sanitized between source and sink."""
    for category, patterns in SANITIZATION_PATTERNS.items():
        for pattern, _ in patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return True
    return False


def score_exposure(
    endpoints: List[Dict],
    inputs: List[Dict],
    auth_gaps: List[Dict],
    data_flows: List[Dict],
) -> Dict:
    """Calculate overall exposure score."""
    score = 0
    max_score = 100

    score += min(len(endpoints) * 2, 30)
    score += min(len([i for i in inputs if not i.get("sanitized", True)]) * 5, 25)
    score += len(auth_gaps) * 15
    score += min(len([d for d in data_flows if not d.get("sanitized", True)]) * 3, 20)

    critical_gaps = [g for g in auth_gaps if g.get("severity") == "Critical"]
    high_gaps = [g for g in auth_gaps if g.get("severity") == "High"]

    score += len(critical_gaps) * 10

    score = min(score, max_score)

    if score >= 80:
        rating = "Critical"
    elif score >= 60:
        rating = "High"
    elif score >= 40:
        rating = "Medium"
    elif score >= 20:
        rating = "Low"
    else:
        rating = "Minimal"

    return {
        "score": score,
        "rating": rating,
        "endpoint_count": len(endpoints),
        "unsecured_inputs": len([i for i in inputs if not i.get("sanitized", True)]),
        "auth_gaps": len(auth_gaps),
        "risky_data_flows": len(
            [d for d in data_flows if not d.get("sanitized", True)]
        ),
    }


def attack_surface_mapper(
    code: str, options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Map attack surface in application code.

    Args:
        code: Application source code to analyze
        options: Optional configuration:
            - include_internal: Include internal endpoints (default: False)
            - depth: Analysis depth level 1-3 (default: 1)

    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - endpoints: Detected endpoints
        - inputs: Input points with risk assessment
        - auth_gaps: Authentication issues
        - data_flow: Data flow analysis
        - exposure_score: Overall exposure metrics
    """
    if options is None:
        options = {}

    if not code or not isinstance(code, str):
        return {
            "status": "error",
            "error": "Invalid code input provided",
            "endpoints": [],
            "inputs": [],
            "auth_gaps": [],
            "data_flow": [],
            "exposure_score": {},
        }

    try:
        include_internal = options.get("include_internal", False)
        depth = options.get("depth", 1)

        language = detect_language(code)
        endpoints = detect_endpoints(code, include_internal)
        inputs = identify_inputs(code, options)
        auth_gaps = analyze_auth(code)
        data_flows = map_data_flow(code, depth)
        exposure_score = score_exposure(endpoints, inputs, auth_gaps, data_flows)

        return {
            "status": "success",
            "endpoints": endpoints,
            "inputs": inputs,
            "auth_gaps": auth_gaps,
            "data_flow": data_flows,
            "exposure_score": exposure_score,
            "metadata": {
                "language_detected": language,
                "analysis_depth": depth,
                "include_internal": include_internal,
                "code_lines": len(code.split("\n")),
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "endpoints": [],
            "inputs": [],
            "auth_gaps": [],
            "data_flow": [],
            "exposure_score": {},
        }


def invoke(payload: dict) -> dict:
    """
    Main entry point for MCP skill invocation.

    Args:
        payload: Dictionary with:
        - code: Source code to analyze (required)
        - options: Optional configuration dict
        - action: Action to perform (default: "map")

    Returns:
        Dictionary with result
    """
    action = payload.get("action", "map")

    if action == "map":
        code = payload.get("code", "")
        options = payload.get("options", {})
        result = attack_surface_mapper(code, options)
    elif action == "endpoints":
        code = payload.get("code", "")
        include_internal = payload.get("include_internal", False)
        result = {"endpoints": detect_endpoints(code, include_internal)}
    elif action == "inputs":
        code = payload.get("code", "")
        options = payload.get("options", {})
        result = {"inputs": identify_inputs(code, options)}
    elif action == "auth":
        code = payload.get("code", "")
        result = {"auth_gaps": analyze_auth(code)}
    elif action == "flow":
        code = payload.get("code", "")
        depth = payload.get("depth", 1)
        result = {"data_flow": map_data_flow(code, depth)}
    elif action == "score":
        code = payload.get("code", "")
        options = payload.get("options", {})
        result = attack_surface_mapper(code, options)
        result = {"exposure_score": result.get("exposure_score", {})}
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return {"result": result}


def register_skill() -> dict:
    """
    Return skill metadata for MCP registration.

    Returns:
        Dictionary with skill metadata
    """
    return {
        "name": "attack-surface-mapper",
        "description": "Maps attack surfaces in application code by detecting endpoints, identifying inputs, analyzing authentication, mapping data flow, and scoring exposure",
        "version": "1.0.0",
        "domain": "SECURITY",
        "capabilities": [
            "endpoint_detection",
            "input_identification",
            "authentication_analysis",
            "data_flow_mapping",
            "exposure_scoring",
        ],
        "supported_languages": [
            "python_fastapi",
            "python_flask",
            "express",
            "django",
            "spring",
            "go_gin",
            "ruby_rails",
            "java_servlet",
        ],
    }
