"""
Secret Scanner - Credential Detection in Code

Scans code for hardcoded secrets, API keys, tokens, passwords, and provides:
- Detection of common secret patterns
- Severity assessment
- Redacted code output
- Remediation recommendations
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List


class Severity(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


@dataclass
class SecretFinding:
    type: str
    value: str
    line_number: int
    column_start: int
    column_end: int
    context: str
    severity: str
    access_level: str
    redacted_value: str


SECRET_PATTERNS = {
    "AWS Access Key": {
        "pattern": r'(?:aws[_-]?)?access[_-]?key[_-]?id["\s:=]+["\']([A-Z0-9]{20})["\']',
        "severity": Severity.CRITICAL,
        "access": "AWS Resources",
        "context_pattern": r".{0,30}(?:aws[_-]?)?access[_-]?key[_-]?id.{0,30}",
    },
    "AWS Secret Key": {
        "pattern": r'(?:aws[_-]?)?secret[_-]?access[_-]?key["\s:=]+["\']([A-Za-z0-9/+=]{40})["\']',
        "severity": Severity.CRITICAL,
        "access": "AWS Resources",
        "context_pattern": r".{0,30}(?:aws[_-]?)?secret[_-]?access.{0,30}",
    },
    "AWS Session Token": {
        "pattern": r'aws[_-]?session[_-]?token["\s:=]+["\']([A-Za-z0-9/+=]{200,})["\']',
        "severity": Severity.CRITICAL,
        "access": "AWS Resources",
        "context_pattern": r".{0,30}aws[_-]?session[_-]?token.{0,30}",
    },
    "GitHub Token": {
        "pattern": r'(?:github[_-]?)?token["\s:=]+["\'](gh[pousr]_[A-Za-z0-9_]{36,})["\']',
        "severity": Severity.CRITICAL,
        "access": "GitHub Repositories",
        "context_pattern": r".{0,30}(?:github[_-]?)?token.{0,30}",
    },
    "GitHub PAT": {
        "pattern": r'github[_-]?pat["\s:=]+["\']([A-Za-z0-9_]{22,})["\']',
        "severity": Severity.CRITICAL,
        "access": "GitHub Repositories",
        "context_pattern": r".{0,30}github[_-]?pat.{0,30}",
    },
    "Generic API Key": {
        "pattern": r'api[_-]?key["\s:=]+["\']([A-Za-z0-9_\-]{16,64})["\']',
        "severity": Severity.HIGH,
        "access": "Unknown API",
        "context_pattern": r".{0,30}api[_-]?key.{0,30}",
    },
    "Generic Secret": {
        "pattern": r'secret[_-]?key["\s:=]+["\']([A-Za-z0-9_\-]{16,64})["\']',
        "severity": Severity.HIGH,
        "access": "Unknown Service",
        "context_pattern": r".{0,30}secret[_-]?key.{0,30}",
    },
    "Password": {
        "pattern": r'password["\s:=]+["\']([^"\']{4,})["\']',
        "severity": Severity.CRITICAL,
        "access": "User Accounts",
        "context_pattern": r".{0,30}password.{0,30}",
    },
    "Private Key": {
        "pattern": r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
        "severity": Severity.CRITICAL,
        "access": "Cryptographic Systems",
        "context_pattern": r".{0,30}PRIVATE KEY.{0,30}",
    },
    "Google API Key": {
        "pattern": r'google[_-]?api[_-]?key["\s:=]+["\']([A-Za-z0-9_\-]{39})["\']',
        "severity": Severity.CRITICAL,
        "access": "Google Cloud",
        "context_pattern": r".{0,30}google[_-]?api[_-]?key.{0,30}",
    },
    "Stripe Key": {
        "pattern": r'stripe[_-]?(?:live[_-]?)?(?:secret[_-]?)?key["\s:=]+["\'](sk_live_[A-Za-z0-9]{24,})["\']',
        "severity": Severity.CRITICAL,
        "access": "Stripe Payments",
        "context_pattern": r".{0,30}stripe[_-]?key.{0,30}",
    },
    "Stripe Publishable": {
        "pattern": r'stripe[_-]?(?:live[_-]?)?publishable[_-]?key["\s:=]+["\'](pk_live_[A-Za-z0-9]{24,})["\']',
        "severity": Severity.MEDIUM,
        "access": "Stripe Payments",
        "context_pattern": r".{0,30}stripe[_-]?publishable.{0,30}",
    },
    "Database URL": {
        "pattern": r'(?:mysql|postgresql|mongodb|redis)://[^\s"\'>]+',
        "severity": Severity.HIGH,
        "access": "Database",
        "context_pattern": r".{0,30}(?:mysql|postgresql|mongodb|redis)://.{0,30}",
    },
    "JWT Token": {
        "pattern": r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
        "severity": Severity.HIGH,
        "access": "Authentication",
        "context_pattern": r".{0,30}eyJ[A-Za-z0-9_-]+\.{3}.{0,30}",
    },
    "Slack Token": {
        "pattern": r"xox[baprs]-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*",
        "severity": Severity.CRITICAL,
        "access": "Slack Workspace",
        "context_pattern": r".{0,30}xox[baprs]-.{0,30}",
    },
    "Slack Webhook": {
        "pattern": r"https://hooks\.slack\.com/services/T[a-zA-Z0-9]+/B[a-zA-Z0-9]+/[a-zA-Z0-9]+",
        "severity": Severity.HIGH,
        "access": "Slack Notifications",
        "context_pattern": r".{0,30}hooks\.slack\.com.{0,30}",
    },
    "Azure Key": {
        "pattern": r'azure[_-]?(?:storage[_-]?)?(?:account[_-]?)?(?:key|connection)["\s:=]+["\']([A-Za-z0-9+/=]{86})["\']',
        "severity": Severity.CRITICAL,
        "access": "Azure Storage",
        "context_pattern": r".{0,30}azure[_-]?key.{0,30}",
    },
    "SendGrid Key": {
        "pattern": r'sendgrid[_-]?api[_-]?key["\s:=]+["\'](SG\.[A-Za-z0-9_\-]{22}\.[A-Za-z0-9_\-]{43})["\']',
        "severity": Severity.CRITICAL,
        "access": "SendGrid Email",
        "context_pattern": r".{0,30}sendgrid[_-]?api[_-]?key.{0,30}",
    },
    "Twilio Key": {
        "pattern": r'twilio[_-]?(?:account[_-]?)?sid["\s:=]+["\'](AC[a-z0-9]{32})["\']',
        "severity": Severity.CRITICAL,
        "access": "Twilio SMS/Voice",
        "context_pattern": r".{0,30}twilio[_-]?sid.{0,30}",
    },
    "Twilio Auth": {
        "pattern": r'twilio[_-]?auth[_-]?token["\s:=]+["\']([a-z0-9]{32})["\']',
        "severity": Severity.CRITICAL,
        "access": "Twilio SMS/Voice",
        "context_pattern": r".{0,30}twilio[_-]?auth[_-]?token.{0,30}",
    },
    "NPM Token": {
        "pattern": r'npm[_-]?token["\s:=]+["\'](npm_[A-Za-z0-9]{36})["\']',
        "severity": Severity.CRITICAL,
        "access": "NPM Registry",
        "context_pattern": r".{0,30}npm[_-]?token.{0,30}",
    },
    "Heroku API Key": {
        "pattern": r'heroku[_-]?api[_-]?key["\s:=]+["\']([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})["\']',
        "severity": Severity.CRITICAL,
        "access": "Heroku",
        "context_pattern": r".{0,30}heroku[_-]?api[_-]?key.{0,30}",
    },
    "Docker Hub Token": {
        "pattern": r'docker[_-]?hub[_-]?token["\s:=]+["\']([A-Za-z0-9]{20,})["\']',
        "severity": Severity.HIGH,
        "access": "Docker Hub",
        "context_pattern": r".{0,30}docker[_-]?hub[_-]?token.{0,30}",
    },
    "SSH Private Key": {
        "pattern": r"-----BEGIN OPENSSH PRIVATE KEY-----",
        "severity": Severity.CRITICAL,
        "access": "SSH Access",
        "context_pattern": r".{0,30}OPENSSH PRIVATE KEY.{0,30}",
    },
    "Basic Auth": {
        "pattern": r"(?:https?://)[^:]+:[^@]+@[a-zA-Z]",
        "severity": Severity.HIGH,
        "access": "HTTP Basic Auth",
        "context_pattern": r".{0,30}:[^@]+@.{0,30}",
    },
    "Connection String": {
        "pattern": r'(?:mongodb|mysql|postgresql|redis|amqp)://[^\s"\'>]+',
        "severity": Severity.HIGH,
        "access": "Database/Message Queue",
        "context_pattern": r".{0,30}(?:mongodb|mysql|postgresql|redis)://.{0,30}",
    },
    "Firebase Key": {
        "pattern": r'firebase[_-]?(?:api[_-]?key|database[_-]?url)["\s:=]+["\']([A-Za-z0-9_-]{30,})["\']',
        "severity": Severity.HIGH,
        "access": "Firebase",
        "context_pattern": r".{0,30}firebase[_-]?(?:api[_-]?key|database[_-]?url).{0,30}",
    },
    "Mapbox Key": {
        "pattern": r'mapbox[_-]?(?:api[_-]?)?key["\s:=]+["\'](pk\.[A-Za-z0-9_\-]{40,})["\']',
        "severity": Severity.HIGH,
        "access": "Mapbox",
        "context_pattern": r".{0,30}mapbox[_-]?key.{0,30}",
    },
    "Mailchimp Key": {
        "pattern": r'mailchimp[_-]?api[_-]?key["\s:=]+["\']([a-z0-9]{32}-us[0-9]{1,2})["\']',
        "severity": Severity.CRITICAL,
        "access": "Mailchimp",
        "context_pattern": r".{0,30}mailchimp[_-]?api[_-]?key.{0,30}",
    },
    "Square Key": {
        "pattern": r'square[_-]?(?:access[_-]?)?token["\s:=]+["\'](sq0atp-[A-Za-z0-9_-]{22})["\']',
        "severity": Severity.CRITICAL,
        "access": "Square Payments",
        "context_pattern": r".{0,30}square[_-]?token.{0,30}",
    },
}


HIGH_INTENSITY_PATTERNS = {
    "Hardcoded Bearer": {
        "pattern": r"bearer\s+[A-Za-z0-9_\-\.]{20,}",
        "severity": Severity.HIGH,
        "access": "Bearer Token",
        "context_pattern": r".{0,30}bearer\s+.{0,30}",
    },
    "Base64 Long String": {
        "pattern": r'["\']([A-Za-z0-9+/]{50,}={0,2})["\']',
        "severity": Severity.MEDIUM,
        "access": "Encoded Secret",
        "context_pattern": r".{0,30}[A-Za-z0-9+/]{50,}={0,2}.{0,30}",
    },
    "Hex Long String": {
        "pattern": r'["\'](0x[a-fA-F0-9]{40,})["\']',
        "severity": Severity.LOW,
        "access": "Hex Value",
        "context_pattern": r".{0,30}0x[a-fA-F0-9]{40,}.{0,30}",
    },
    "Credential Assignment": {
        "pattern": r'(?:credential|cred|pwd|passwd)["\s:=]+["\']([^"\']{8,})["\']',
        "severity": Severity.HIGH,
        "access": "Unknown",
        "context_pattern": r".{0,30}(?:credential|cred|pwd|passwd).{0,30}",
    },
    "Token Assignment": {
        "pattern": r'(?:token|access[_-]?token)["\s:=]+["\']([A-Za-z0-9_\-\.]{20,})["\']',
        "severity": Severity.HIGH,
        "access": "Authentication",
        "context_pattern": r".{0,30}(?:token|access[_-]?token).{0,30}",
    },
}


def redact_secret(value: str, secret_type: str) -> str:
    """Generate a redacted version of a secret."""
    if "private" in secret_type.lower() or "key" in secret_type.lower():
        return "[REDACTED_PRIVATE_KEY]"

    if len(value) <= 8:
        return "*" * len(value)

    if value.startswith("sk_live_") or value.startswith("pk_live_"):
        return value[:8] + "*" * (len(value) - 8)

    if "github" in secret_type.lower() and value.startswith("gh"):
        return value[:4] + "*" * (len(value) - 4)

    return value[:4] + "*" * (len(value) - 4)


def get_line_context(code: str, line_number: int, context_size: int = 50) -> str:
    """Extract context around a line number."""
    lines = code.split("\n")
    if 0 < line_number <= len(lines):
        line = lines[line_number - 1]
        return line.strip()
    return ""


def calculate_overall_severity(secrets: List[SecretFinding]) -> str:
    """Calculate overall severity based on findings."""
    if not secrets:
        return "None"

    severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for secret in secrets:
        severity_counts[secret.severity] = severity_counts.get(secret.severity, 0) + 1

    if severity_counts["Critical"] > 0:
        return "Critical"
    elif severity_counts["High"] > 0:
        return "High"
    elif severity_counts["Medium"] > 0:
        return "Medium"
    elif severity_counts["Low"] > 0:
        return "Low"
    return "None"


def generate_recommendations(secrets: List[SecretFinding]) -> List[str]:
    """Generate remediation recommendations based on findings."""
    recommendations = []
    secret_types = {s.type for s in secrets}

    recommendations.append("Remove all hardcoded secrets from source code immediately")
    recommendations.append(
        "Use environment variables or a secrets manager (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault)"
    )

    if any("AWS" in t for t in secret_types):
        recommendations.append(
            "Rotate AWS credentials immediately and review IAM roles"
        )
        recommendations.append("Use IAM roles instead of access keys where possible")

    if any("GitHub" in t for t in secret_types):
        recommendations.append("Revoke the exposed GitHub tokens and create new ones")
        recommendations.append(
            "Enable 2FA on GitHub account and use fine-grained tokens"
        )

    if any("password" in t.lower() for t in secret_types):
        recommendations.append(
            "Implement password hashing (bcrypt, argon2) for user credentials"
        )

    if any("private" in t.lower() or "key" in t.lower() for t in secret_types):
        recommendations.append(
            "Never commit private keys - use secure key management systems"
        )
        recommendations.append("Add sensitive files to .gitignore")

    if any("database" in t.lower() or "connection" in t.lower() for t in secret_types):
        recommendations.append(
            "Use database connection pooling with secure credential storage"
        )
        recommendations.append("Implement database encryption at rest and in transit")

    recommendations.append("Set up automated secret scanning in CI/CD pipeline")
    recommendations.append(
        "Consider using git-secrets or similar tools to prevent future leaks"
    )

    return recommendations


def redact_code(code: str, secrets: List[SecretFinding]) -> str:
    """Create a redacted version of the code."""
    redacted = code

    sorted_secrets = sorted(secrets, key=lambda s: s.column_start, reverse=True)

    for secret in sorted_secrets:
        lines = redacted.split("\n")
        if 0 < secret.line_number <= len(lines):
            line = lines[secret.line_number - 1]
            if secret.value in line:
                redacted_line = line.replace(secret.value, secret.redacted_value)
                lines[secret.line_number - 1] = redacted_line
                redacted = "\n".join(lines)

    return redacted


def secret_scanner(
    code: str, options: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    """
    Scan code for hardcoded secrets and credentials.

    Args:
        code: The source code to scan
        options: Optional configuration:
            - intensity: "normal" or "high" (default: "normal")
            - include_history: bool to include commit history context

    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - secrets: List of detected secrets with locations
        - severity: Overall severity level
        - redacted_code: Safe version of code
        - recommendations: How to fix issues
    """
    if options is None:
        options = {}

    intensity = options.get("intensity", "normal")
    include_history = options.get("include_history", False)

    if not code or not isinstance(code, str):
        return {
            "status": "error",
            "error": "Invalid code input provided",
            "secrets": [],
            "severity": "None",
            "redacted_code": "",
            "recommendations": [],
        }

    try:
        secrets_found = []
        code.split("\n")

        active_patterns = {**SECRET_PATTERNS}
        if intensity == "high":
            active_patterns.update(HIGH_INTENSITY_PATTERNS)

        for secret_type, config in active_patterns.items():
            pattern = config["pattern"]
            severity = config["severity"].value
            access_level = config["access"]
            config.get("context_pattern", r".{0,30}.{0,30}")

            for match in re.finditer(pattern, code, re.IGNORECASE):
                value = match.group(1) if match.groups() else match.group(0)

                line_number = code[: match.start()].count("\n") + 1

                col_start = match.start() - code.rfind("\n", 0, match.start()) - 1
                col_end = col_start + len(value)

                context = get_line_context(code, line_number)

                redacted = redact_secret(value, secret_type)

                finding = SecretFinding(
                    type=secret_type,
                    value=value,
                    line_number=line_number,
                    column_start=col_start,
                    column_end=col_end,
                    context=context,
                    severity=severity,
                    access_level=access_level,
                    redacted_value=redacted,
                )
                secrets_found.append(finding)

        secrets_found.sort(key=lambda x: (x.line_number, x.column_start))

        secrets_data = [
            {
                "type": s.type,
                "value": s.value,
                "line_number": s.line_number,
                "column_start": s.column_start,
                "column_end": s.column_end,
                "context": s.context,
                "severity": s.severity,
                "access_level": s.access_level,
                "redacted_value": s.redacted_value,
            }
            for s in secrets_found
        ]

        overall_severity = calculate_overall_severity(secrets_found)

        redacted_code = redact_code(code, secrets_found)

        recommendations = generate_recommendations(secrets_found)

        return {
            "status": "success",
            "secrets": secrets_data,
            "severity": overall_severity,
            "redacted_code": redacted_code,
            "recommendations": recommendations,
            "scan_options": {
                "intensity": intensity,
                "include_history": include_history,
                "patterns_scanned": len(active_patterns),
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "secrets": [],
            "severity": "None",
            "redacted_code": code,
            "recommendations": [],
        }


def invoke(payload: dict) -> dict:
    """
    Main entry point for MCP skill invocation.

    Args:
        payload: Dictionary with:
        - code: Source code to scan (required)
        - options: Optional configuration dict

    Returns:
        Dictionary with result
    """
    action = payload.get("action", "scan")

    if action == "scan":
        code = payload.get("code", "")
        options = payload.get("options", {})
        result = secret_scanner(code, options)
    elif action == "redact":
        code = payload.get("code", "")
        options = payload.get("options", {})
        result = secret_scanner(code, options)
        result = {"redacted_code": result.get("redacted_code", "")}
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
        "name": "secret-scanner",
        "description": "Scan code for hardcoded secrets, API keys, tokens, and passwords with severity assessment and redaction",
        "version": "1.0.0",
        "domain": "SECURITY",
        "capabilities": [
            "credential_detection",
            "secret_redaction",
            "severity_assessment",
            "remediation_guidance",
        ],
        "supported_secret_types": list(SECRET_PATTERNS.keys()),
    }
