import re
import ast
from typing import Dict, List, Any, Optional


def secure_patterns(code: str, options: dict = None) -> dict:
    options = options or {}
    check_types = options.get(
        "check_types",
        [
            "sql_injection",
            "xss",
            "csrf",
            "hardcoded_secrets",
            "insecure_deserialization",
            "path_traversal",
            "command_injection",
        ],
    )
    severity_filter = options.get("severity", ["critical", "high", "medium", "low"])

    issues = []
    secure_patterns_found = []
    fixes = []

    if "sql_injection" in check_types:
        sql_result = _check_sql_injection(code)
        issues.extend(sql_result["issues"])
        secure_patterns_found.extend(sql_result["secure_patterns"])
        fixes.extend(sql_result["fixes"])

    if "xss" in check_types:
        xss_result = _check_xss(code)
        issues.extend(xss_result["issues"])
        secure_patterns_found.extend(xss_result["secure_patterns"])
        fixes.extend(xss_result["fixes"])

    if "csrf" in check_types:
        csrf_result = _check_csrf(code)
        issues.extend(csrf_result["issues"])
        secure_patterns_found.extend(csrf_result["secure_patterns"])
        fixes.extend(csrf_result["fixes"])

    if "hardcoded_secrets" in check_types:
        secrets_result = _check_hardcoded_secrets(code)
        issues.extend(secrets_result["issues"])
        secure_patterns_found.extend(secrets_result["secure_patterns"])
        fixes.extend(secrets_result["fixes"])

    if "insecure_deserialization" in check_types:
        deser_result = _check_insecure_deserialization(code)
        issues.extend(deser_result["issues"])
        secure_patterns_found.extend(deser_result["secure_patterns"])
        fixes.extend(deser_result["fixes"])

    if "path_traversal" in check_types:
        path_result = _check_path_traversal(code)
        issues.extend(path_result["issues"])
        secure_patterns_found.extend(path_result["secure_patterns"])
        fixes.extend(path_result["fixes"])

    if "command_injection" in check_types:
        cmd_result = _check_command_injection(code)
        issues.extend(cmd_result["issues"])
        secure_patterns_found.extend(cmd_result["secure_patterns"])
        fixes.extend(cmd_result["fixes"])

    severity_map = {"critical": 25, "high": 15, "medium": 10, "low": 5}
    deductions = sum(
        severity_map.get(i["severity"], 10)
        for i in issues
        if i["severity"] in severity_filter
    )
    score = max(0, 100 - deductions)

    return {
        "status": "success",
        "issues": [i for i in issues if i["severity"] in severity_filter],
        "secure_patterns": secure_patterns_found,
        "score": score,
        "fixes": fixes,
        "summary": {
            "total_issues": len(issues),
            "critical_count": len([i for i in issues if i["severity"] == "critical"]),
            "high_count": len([i for i in issues if i["severity"] == "high"]),
            "medium_count": len([i for i in issues if i["severity"] == "medium"]),
            "low_count": len([i for i in issues if i["severity"] == "low"]),
            "checks_performed": check_types,
        },
    }


def _check_sql_injection(code: str) -> dict:
    issues = []
    secure_patterns_found = []
    fixes = []

    insecure_patterns = [
        (r'execute\s*\(\s*["\'].*%s', "String formatting in SQL execute"),
        (r'execute\s*\(\s*f["\']', "f-string in SQL execute"),
        (r"cursor\.execute\s*\([^,)]*\+", "String concatenation in SQL execute"),
        (r"SELECT.*\+.*request", "Dynamic SQL query construction"),
    ]

    for pattern, desc in insecure_patterns:
        matches = re.finditer(pattern, code, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            issues.append(
                {
                    "type": "sql_injection",
                    "severity": "critical",
                    "description": desc,
                    "line": code[: match.start()].count("\n") + 1,
                    "match": match.group(),
                }
            )
            fixes.append(
                {
                    "type": "sql_injection",
                    "description": "Use parameterized queries or prepared statements",
                    "example": "cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))",
                }
            )

    secure_patterns = [
        (r'execute\s*\(\s*["\'][^"\']*\?[^"\']*["\']', "Parameterized query"),
        (
            r'execute\s*\(\s*["\'][^"\']*\%s[^"\']*["\']',
            "Prepared statement with placeholder",
        ),
        (r"cursor\.execute\s*\([^,)]*,\s*\(", "Tuple parameter in execute"),
    ]

    for pattern, desc in secure_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            secure_patterns_found.append({"type": "sql_injection", "description": desc})

    return {"issues": issues, "secure_patterns": secure_patterns_found, "fixes": fixes}


def _check_xss(code: str) -> dict:
    issues = []
    secure_patterns_found = []
    fixes = []

    insecure_patterns = [
        (r"innerHTML\s*=\s*", "Direct innerHTML assignment"),
        (r"document\.write\s*\(", "document.write usage"),
        (r"<script[^>]*>.*?</script>", "Inline script tag"),
        (r'on\w+\s*=\s*["\'][^"\']*\$', "Unescaped event handler"),
    ]

    for pattern, desc in insecure_patterns:
        matches = re.finditer(pattern, code, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        for match in matches:
            issues.append(
                {
                    "type": "xss",
                    "severity": "high",
                    "description": desc,
                    "line": code[: match.start()].count("\n") + 1,
                    "match": match.group()[:100],
                }
            )
            fixes.append(
                {
                    "type": "xss",
                    "description": "Use textContent instead of innerHTML, or sanitize input",
                    "example": "element.textContent = userInput",
                }
            )

    if re.search(r"textContent", code, re.IGNORECASE):
        secure_patterns_found.append(
            {
                "type": "xss",
                "description": "Using textContent for safe DOM manipulation",
            }
        )
    if re.search(r"DOMPurify|he\.encode|escapeHtml", code, re.IGNORECASE):
        secure_patterns_found.append(
            {"type": "xss", "description": "HTML encoding/sanitization detected"}
        )
    if re.search(r"ContentSecurityPolicy|csp", code, re.IGNORECASE):
        secure_patterns_found.append(
            {"type": "xss", "description": "Content Security Policy configured"}
        )

    return {"issues": issues, "secure_patterns": secure_patterns_found, "fixes": fixes}


def _check_csrf(code: str) -> dict:
    issues = []
    secure_patterns_found = []
    fixes = []

    if re.search(r"@app\.route.*methods.*POST", code) and not re.search(
        r"csrf_token|CSRF|csrf", code, re.IGNORECASE
    ):
        issues.append(
            {
                "type": "csrf",
                "severity": "medium",
                "description": "POST endpoint without CSRF protection",
                "line": 1,
                "match": "POST endpoint",
            }
        )
        fixes.append(
            {
                "type": "csrf",
                "description": "Enable CSRF protection with Flask-WTF or similar",
                "example": "from flask_wtf import CSRFProtect; csrf = CSRFProtect(app)",
            }
        )

    if re.search(r"<form[^>]*>", code) and not re.search(
        r"csrf_token|{{ csrf_token }}", code
    ):
        issues.append(
            {
                "type": "csrf",
                "severity": "medium",
                "description": "Form without CSRF token",
                "line": code[: re.search(r"<form", code).start()].count("\n") + 1,
                "match": "<form>",
            }
        )
        fixes.append(
            {
                "type": "csrf",
                "description": "Add CSRF token to form",
                "example": "<input type='hidden' name='csrf_token' value='{{ csrf_token() }}'>",
            }
        )

    if re.search(r"CSRFProtect|CSRFProtection|@csrf_exempt", code, re.IGNORECASE):
        secure_patterns_found.append(
            {"type": "csrf", "description": "CSRF protection enabled"}
        )

    return {"issues": issues, "secure_patterns": secure_patterns_found, "fixes": fixes}


def _check_hardcoded_secrets(code: str) -> dict:
    issues = []
    secure_patterns_found = []
    fixes = []

    secret_patterns = [
        (r'password\s*=\s*["\'][^"\']{3,}["\']', "Hardcoded password", "critical"),
        (r'api_key\s*=\s*["\'][^"\']{8,}["\']', "Hardcoded API key", "critical"),
        (r'secret\s*=\s*["\'][^"\']{8,}["\']', "Hardcoded secret", "critical"),
        (r'token\s*=\s*["\'][^"\']{10,}["\']', "Hardcoded token", "high"),
        (r'private_key\s*=\s*["\']', "Hardcoded private key", "critical"),
        (r'aws_access_key\s*=\s*["\']', "Hardcoded AWS key", "critical"),
        (
            r'connection_string\s*=\s*["\'][^"\']*password=',
            "Hardcoded connection string",
            "high",
        ),
    ]

    for pattern, desc, severity in secret_patterns:
        matches = re.finditer(pattern, code, re.IGNORECASE)
        for match in matches:
            if not any(
                x in match.group().lower()
                for x in ["example", "placeholder", "test", "your_", "<", "?"]
            ):
                issues.append(
                    {
                        "type": "hardcoded_secret",
                        "severity": severity,
                        "description": desc,
                        "line": code[: match.start()].count("\n") + 1,
                        "match": match.group()[:50] + "...",
                    }
                )
                fixes.append(
                    {
                        "type": "hardcoded_secret",
                        "description": "Use environment variables or secrets management",
                        "example": "import os; password = os.environ.get('PASSWORD')",
                    }
                )

    if re.search(r"os\.environ|os\.getenv|environ\.get", code, re.IGNORECASE):
        secure_patterns_found.append(
            {
                "type": "hardcoded_secret",
                "description": "Environment variables usage detected",
            }
        )
    if re.search(r"SecretManager|secretsmanager|aws.*secret", code, re.IGNORECASE):
        secure_patterns_found.append(
            {
                "type": "hardcoded_secret",
                "description": "Secrets management service usage",
            }
        )

    return {"issues": issues, "secure_patterns": secure_patterns_found, "fixes": fixes}


def _check_insecure_deserialization(code: str) -> dict:
    issues = []
    secure_patterns_found = []
    fixes = []

    insecure_patterns = [
        (r"pickle\.loads?\s*\(", "Insecure pickle deserialization"),
        (r"yaml\.load\s*\([^,)]*\)(?!", "Insecure YAML load"),
        (r"marshal\.loads?\s*\(", "Insecure marshal deserialization"),
        (r"eval\s*\(", "Dangerous eval usage"),
        (r"exec\s*\(", "Dangerous exec usage"),
    ]

    for pattern, desc in insecure_patterns:
        matches = re.finditer(pattern, code, re.IGNORECASE)
        for match in matches:
            issues.append(
                {
                    "type": "insecure_deserialization",
                    "severity": "critical",
                    "description": desc,
                    "line": code[: match.start()].count("\n") + 1,
                    "match": match.group(),
                }
            )
            fixes.append(
                {
                    "type": "insecure_deserialization",
                    "description": "Use safer alternatives or validate input",
                    "example": "json.loads(data) instead of pickle",
                }
            )

    if re.search(r"json\.loads?", code):
        secure_patterns_found.append(
            {"type": "insecure_deserialization", "description": "JSON parsing (safe)"}
        )
    if re.search(r"yaml\.safe_load", code):
        secure_patterns_found.append(
            {"type": "insecure_deserialization", "description": "YAML safe_load usage"}
        )

    return {"issues": issues, "secure_patterns": secure_patterns_found, "fixes": fixes}


def _check_path_traversal(code: str) -> dict:
    issues = []
    secure_patterns_found = []
    fixes = []

    insecure_patterns = [
        (r"open\s*\([^,)]*\+[^,)]*\)", "Path concatenation in open()"),
        (r"os\.path\.join\s*\([^,)]*\+", "Path join with concatenation"),
        (r"request\.args\.get\([^)]+\)\s*\+", "User input concatenated to path"),
        (r"request\.form\.get\([^)]+\)\s*\+", "Form input concatenated to path"),
    ]

    for pattern, desc in insecure_patterns:
        matches = re.finditer(pattern, code, re.IGNORECASE)
        for match in matches:
            issues.append(
                {
                    "type": "path_traversal",
                    "severity": "high",
                    "description": desc,
                    "line": code[: match.start()].count("\n") + 1,
                    "match": match.group(),
                }
            )
            fixes.append(
                {
                    "type": "path_traversal",
                    "description": "Validate and sanitize path inputs",
                    "example": "os.path.basename(user_input) to prevent traversal",
                }
            )

    if re.search(r"os\.path\.basename|Path\(.*\)\.name", code):
        secure_patterns_found.append(
            {
                "type": "path_traversal",
                "description": "Using basename to sanitize paths",
            }
        )

    return {"issues": issues, "secure_patterns": secure_patterns_found, "fixes": fixes}


def _check_command_injection(code: str) -> dict:
    issues = []
    secure_patterns_found = []
    fixes = []

    insecure_patterns = [
        (r"os\.system\s*\([^)]*\+", "os.system with string concatenation"),
        (r"subprocess\.call\s*\([^,]*\+", "subprocess.call with dynamic command"),
        (r"os\.popen\s*\([^)]*\+", "os.popen with dynamic command"),
        (r"commands\..*\+", "commands module with dynamic input"),
        (r"shell=True", "subprocess with shell=True"),
    ]

    for pattern, desc in insecure_patterns:
        matches = re.finditer(pattern, code, re.IGNORECASE)
        for match in matches:
            issues.append(
                {
                    "type": "command_injection",
                    "severity": "critical",
                    "description": desc,
                    "line": code[: match.start()].count("\n") + 1,
                    "match": match.group(),
                }
            )
            fixes.append(
                {
                    "type": "command_injection",
                    "description": "Use subprocess with shell=False and list arguments",
                    "example": "subprocess.run(['ls', user_dir], shell=False)",
                }
            )

    if re.search(r"subprocess\.(run|call|Popen)\s*\(\s*\[", code):
        secure_patterns_found.append(
            {
                "type": "command_injection",
                "description": "Using subprocess with list arguments",
            }
        )

    return {"issues": issues, "secure_patterns": secure_patterns_found, "fixes": fixes}


def invoke(payload: dict) -> dict:
    code = payload.get("code", "")
    options = payload.get("options", {})

    if not code:
        return {"status": "error", "error": "No code provided"}

    return secure_patterns(code, options)


def register_skill() -> dict:
    return {
        "name": "secure_patterns",
        "description": "Validates secure coding practices including SQL injection, XSS, CSRF, hardcoded secrets, insecure deserialization, path traversal, and command injection detection",
        "version": "1.0.0",
        "functions": {
            "secure_patterns": {
                "description": "Check code for security vulnerabilities and suggest fixes",
                "parameters": {
                    "code": {"type": "string", "description": "Code to validate"},
                    "options": {
                        "type": "object",
                        "description": "Check types and severity filter",
                        "properties": {
                            "check_types": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "severity": {"type": "array", "items": {"type": "string"}},
                        },
                    },
                },
                "returns": {
                    "status": "string",
                    "issues": "array",
                    "secure_patterns": "array",
                    "score": "integer",
                    "fixes": "array",
                },
            },
            "invoke": {
                "description": "Entry point for skill invocation",
                "parameters": {"payload": {"type": "object"}},
            },
        },
        "checks_supported": [
            "sql_injection",
            "xss",
            "csrf",
            "hardcoded_secrets",
            "insecure_deserialization",
            "path_traversal",
            "command_injection",
        ],
        "severity_levels": ["critical", "high", "medium", "low"],
    }


if __name__ == "__main__":
    test_code = """
    import sqlite3
    user_input = request.args.get('username')
    cursor.execute("SELECT * FROM users WHERE name = " + user_input)
    password = "secret123"
    eval(user_input)
    """
    result = secure_patterns(test_code)
    print(f"Score: {result['score']}")
    print(f"Issues: {len(result['issues'])}")
    for issue in result["issues"]:
        print(f"  - {issue['type']}: {issue['description']}")
