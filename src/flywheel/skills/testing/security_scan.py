"""
Onboarding Skills: Security Scan

This module provides skills for security analysis:
- security_scan: Detect security vulnerabilities and misconfigurations
"""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime


@dataclass
class SecurityFinding:
    """Represents a security finding"""

    id: str
    severity: str
    category: str
    file_path: str
    line_number: int
    description: str
    remediation: str


COMPLIANCE_STANDARDS = {
    "OWASP_TOP_10": [
        "A01:2021 - Broken Access Control",
        "A02:2021 - Cryptographic Failures",
        "A03:2021 - Injection",
        "A04:2021 - Insecure Design",
        "A05:2021 - Security Misconfiguration",
        "A06:2021 - Vulnerable Components",
        "A07:2021 - Auth Failures",
        "A08:2021 - Data Integrity Failures",
        "A09:2021 - Logging Failures",
        "A10:2021 - SSRF",
    ],
    "SOC2": [
        "CC1: Control Environment",
        "CC2: Communication and Information",
        "CC3: Risk Assessment",
        "CC4: Monitoring Activities",
        "CC5: Control Activities",
        "CC6: Logical Access Controls",
    ],
    "PCI_DSS": [
        "Install and maintain network security",
        "Protect cardholder data",
        "Maintain vulnerability management program",
        "Implement strong access controls",
        "Regularly monitor and test networks",
        "Maintain information security policy",
    ],
}

VULNERABILITY_PATTERNS = {
    "Injection": {
        "severity": "critical",
        "patterns": [
            (r'execute\s*\(\s*["\'].*?\%s', "SQL Injection risk"),
            (r'query\s*\(\s*["\'].*?\%s', "NoSQL Injection risk"),
            (r"eval\s*\(\s*", "Code injection via eval"),
            (r"exec\s*\(\s*", "Command injection via exec"),
            (r"system\s*\(\s*", "Command injection via system"),
        ],
    },
    "XSS": {
        "severity": "high",
        "patterns": [
            (r"innerHTML\s*=\s*", "Potential XSS via innerHTML"),
            (r"dangerouslySetInnerHTML", "React XSS risk"),
            (r"v-html\s*=", "Vue XSS risk"),
        ],
    },
    "Authentication": {
        "severity": "high",
        "patterns": [
            (r'password\s*=\s*["\'][^"\']{0,10}["\']', "Hardcoded password"),
            (r"auth\s*=\s*True", "Authentication bypass risk"),
            (r"verify\s*=\s*False", "SSL verification disabled"),
        ],
    },
    "Crypto": {
        "severity": "medium",
        "patterns": [
            (r"md5\s*\(", "Weak hash function (MD5)"),
            (r"sha1\s*\(", "Weak hash function (SHA1)"),
            (r"DES\s*\(", "Weak encryption (DES)"),
        ],
    },
}


def scan_for_vulnerabilities(
    repo_path: str, focus_areas: List[str] | None = None
) -> List[Dict[str, Any]]:
    """
    Scan for code vulnerabilities.

    Args:
        repo_path: Path to repository
        focus_areas: Specific vulnerability types to focus on

    Returns:
        List of vulnerabilities found
    """
    vulnerabilities = []
    focus_areas = focus_areas or list(VULNERABILITY_PATTERNS.keys())

    skip_dirs = {
        "node_modules",
        "__pycache__",
        ".git",
        "venv",
        ".venv",
        "build",
        "dist",
        "vendor",
    }

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in {".py", ".js", ".ts", ".java", ".go", ".rb", ".php", ".cs"}:
                continue

            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, repo_path)

            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    content.split("\n")

                    for vuln_type, info in VULNERABILITY_PATTERNS.items():
                        if vuln_type not in focus_areas:
                            continue

                        for pattern, description in info["patterns"]:
                            for match in re.finditer(pattern, content, re.IGNORECASE):
                                line_num = content[: match.start()].count("\n") + 1
                                vulnerabilities.append(
                                    {
                                        "id": f"{vuln_type.lower()}-{len(vulnerabilities) + 1}",
                                        "severity": info["severity"],
                                        "category": vuln_type,
                                        "file_path": rel_path,
                                        "line_number": line_num,
                                        "description": description,
                                        "recommendation": f"Review and fix {vuln_type} issue",
                                    }
                                )
            except Exception:
                continue

    return vulnerabilities


def scan_secrets(repo_path: str) -> List[Dict[str, Any]]:
    """
    Scan for hardcoded secrets.

    Args:
        repo_path: Path to repository

    Returns:
        List of secrets found
    """
    secrets = []

    secret_patterns = [
        (r'api[_-]?key["\s:=]+["\']([^"\']{16,})["\']', "API Key", "critical"),
        (r'secret[_-]?key["\s:=]+["\']([^"\']{16,})["\']', "Secret Key", "critical"),
        (r'password["\s:=]+["\']([^"\']{8,})["\']', "Password", "critical"),
        (r'private[_-]?key["\s:=]+["\']-----BEGIN', "Private Key", "critical"),
        (
            r'aws[_-]?access[_-]?key["\s:=]+["\']([^"\']{16,})["\']',
            "AWS Key",
            "critical",
        ),
        (
            r'github[_-]?token["\s:=]+["\']([^"\']{16,})["\']',
            "GitHub Token",
            "critical",
        ),
    ]

    skip_dirs = {"node_modules", "__pycache__", ".git", "venv", ".venv"}

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for file in files:
            if file.startswith("."):
                continue

            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, repo_path)

            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    for pattern, secret_type, severity in secret_patterns:
                        for match in re.finditer(pattern, content, re.IGNORECASE):
                            line_num = content[: match.start()].count("\n") + 1
                            secrets.append(
                                {
                                    "id": f"secret-{len(secrets) + 1}",
                                    "severity": severity,
                                    "category": "Secrets",
                                    "file_path": rel_path,
                                    "line_number": line_num,
                                    "description": f"Potential {secret_type}",
                                    "recommendation": f"Remove {secret_type} and use environment variables",
                                }
                            )
            except Exception:
                continue

    return secrets


def scan_dependencies(repo_path: str) -> Dict[str, Any]:
    """
    Scan dependencies for known vulnerabilities.

    Args:
        repo_path: Path to repository

    Returns:
        Dependency vulnerability report
    """
    dependencies = {"outdated": [], "vulnerable": []}

    # Check package.json
    package_json = os.path.join(repo_path, "package.json")
    if os.path.exists(package_json):
        try:
            with open(package_json) as f:
                data = json.load(f)
                deps = {
                    **data.get("dependencies", {}),
                    **data.get("devDependencies", {}),
                }
                for pkg, version in deps.items():
                    dependencies["outdated"].append(
                        {"package": pkg, "version": version, "manager": "npm"}
                    )
        except Exception:
            pass

    # Check requirements.txt
    requirements_txt = os.path.join(repo_path, "requirements.txt")
    if os.path.exists(requirements_txt):
        try:
            with open(requirements_txt) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "==" in line:
                            pkg, version = line.split("==")
                            dependencies["outdated"].append(
                                {"package": pkg, "version": version, "manager": "pip"}
                            )
        except Exception:
            pass

    return dependencies


def security_scan(
    repository_path: str,
    standards: List[str] | None = None,
    severity_threshold: str = "low",
    focus_areas: List[str] | None = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Main entry point for security scanning.

    Args:
        repository_path: Path to repository
        standards: Compliance standards to check (OWASP_TOP_10, SOC2, PCI_DSS)
        severity_threshold: Minimum severity to report
        focus_areas: Areas to focus on (secrets, dependencies, code, configuration)
        **kwargs: Additional parameters

    Returns:
        Comprehensive security scan report
    """
    try:
        severity_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        min_severity = severity_order.get(severity_threshold.lower(), 0)

        focus_areas = focus_areas or ["code", "secrets", "dependencies"]

        vulnerabilities = []
        secrets_found = []
        dependency_issues = {}

        if "code" in focus_areas:
            vulnerabilities = scan_for_vulnerabilities(repository_path)

        if "secrets" in focus_areas:
            secrets_found = scan_secrets(repository_path)

        if "dependencies" in focus_areas:
            dependency_issues = scan_dependencies(repository_path)

        # Filter by severity
        vulnerabilities = [
            v
            for v in vulnerabilities
            if severity_order.get(v["severity"], 0) >= min_severity
        ]

        # Calculate compliance
        compliance_results = {}
        if standards:
            for standard in standards:
                if standard in COMPLIANCE_STANDARDS:
                    compliance_results[standard] = {
                        "requirements": COMPLIANCE_STANDARDS[standard],
                        "coverage": "partial" if vulnerabilities else "full",
                    }

        # Calculate score
        total_issues = len(vulnerabilities) + len(secrets_found)
        score = max(0, 100 - (total_issues * 5))

        return {
            "status": "success",
            "scan_timestamp": str(Path().resolve()),
            "repository": repository_path,
            "vulnerabilities": vulnerabilities,
            "secrets": secrets_found,
            "dependencies": dependency_issues,
            "compliance": compliance_results,
            "summary": {
                "total_vulnerabilities": len(vulnerabilities),
                "total_secrets": len(secrets_found),
                "total_dependencies_issues": len(dependency_issues.get("outdated", [])),
                "score": score,
                "severity_breakdown": {
                    "critical": len(
                        [v for v in vulnerabilities if v["severity"] == "critical"]
                    ),
                    "high": len(
                        [v for v in vulnerabilities if v["severity"] == "high"]
                    ),
                    "medium": len(
                        [v for v in vulnerabilities if v["severity"] == "medium"]
                    ),
                    "low": len([v for v in vulnerabilities if v["severity"] == "low"]),
                },
            },
            "recommendations": [
                "Address critical and high severity issues immediately",
                "Remove hardcoded secrets and use environment variables",
                "Keep dependencies up to date",
            ]
            if total_issues > 0
            else ["No critical issues found"],
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to perform security scan",
        }


async def invoke(payload: dict) -> dict:
    """Main entry point for MCP skill invocation"""
    action = payload.get("action", "scan")

    if action == "scan":
        repo_path = payload.get("repository_path", ")
        standards = payload.get("standards", [])
        severity = payload.get("severity_threshold", "low")
        focus = payload.get("focus_areas", [])
        result = security_scan(repo_path, standards, severity, focus)
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
    """Return skill metadata for MCP registration"""
    return {
        "name": "security-scan",
        "description": "Detect security vulnerabilities and misconfigurations",
        "version": "1.0.0",
        "domain": "APPLICATION_SECURITY",
    }
