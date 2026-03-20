"""
Onboarding Skills: Repository Reconnaissance

This module provides skills for analyzing and understanding codebases:
- repo_recon: Map structure, tech stack, and risks
"""

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class RepositoryAnalysis:
    """Results from repository analysis"""

    structure: Dict[str, Any] = field(default_factory=dict)
    tech_stack: List[Dict[str, str]] = field(default_factory=list)
    risks: List[Dict[str, str]] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)


TECH_STACK_PATTERNS = {
    "JavaScript/TypeScript": [
        ("package.json", "package.json"),
        ("tsconfig.json", "tsconfig.json"),
    ],
    "Python": [
        ("requirements.txt", "requirements.txt"),
        ("pyproject.toml", "pyproject.toml"),
        ("setup.py", "setup.py"),
    ],
    "Java": [("pom.xml", "Maven"), ("build.gradle", "Gradle")],
    "Go": [("go.mod", "go.mod")],
    "Rust": [("Cargo.toml", "Cargo.toml")],
    "Ruby": [("Gemfile", "Gemfile")],
    "PHP": [("composer.json", "composer.json")],
    ".NET": [("*.csproj", ".NET"), ("*.sln", ".NET")],
    "Docker": [("Dockerfile", "Dockerfile"), ("docker-compose.yml", "docker-compose")],
}

SECURITY_PATTERNS = {
    "Secrets": [
        (r'api[_-]?key["\s:=]+["\'][^"\']{8,}', "Potential API key"),
        (r'secret["\s:=]+["\'][^"\']{8,}', "Potential secret"),
        (r'password["\s:=]+["\'][^"\']{6,}', "Potential password"),
        (r'token["\s:=]+["\'][^"\']{8,}', "Potential token"),
    ],
    "Vulnerabilities": [
        (r"exec\s*\(", "Potential code injection"),
        (r"eval\s*\(", "Use of eval()"),
        (r"system\s*\(", "System command execution"),
    ],
}


def analyze_repository_structure(
    repo_path: str, depth: int = 3, include_hidden: bool = False
) -> Dict[str, Any]:
    """
    Analyze repository structure.

    Args:
        repo_path: Absolute path to the repository
        depth: Maximum depth to traverse
        include_hidden: Whether to include hidden files

    Returns:
        Dictionary with structure analysis
    """
    result = {
        "root": os.path.basename(repo_path),
        "total_files": 0,
        "total_dirs": 0,
        "files_by_extension": {},
        "directory_tree": {},
        "largest_files": [],
    }

    if not os.path.exists(repo_path):
        return {"error": f"Repository path does not exist: {repo_path}"}

    files_info = []

    for root, dirs, files in os.walk(repo_path):
        # Filter hidden directories
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith(".")]

        rel_root = os.path.relpath(root, repo_path)
        depth_check = len(Path(rel_root).parts) if rel_root != "." else 0

        if depth_check >= depth:
            continue

        result["total_dirs"] += len(dirs)

        for file in files:
            if not include_hidden and file.startswith("."):
                continue

            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                ext = os.path.splitext(file)[1] or "no_extension"

                result["total_files"] += 1
                result["files_by_extension"][ext] = (
                    result["files_by_extension"].get(ext, 0) + 1
                )

                files_info.append(
                    {
                        "path": os.path.join(rel_root, file),
                        "size": size,
                        "extension": ext,
                    }
                )
            except Exception:
                continue

    # Get largest files
    files_info.sort(key=lambda x: x.get("size", 0), reverse=True)
    result["largest_files"] = files_info[:10]

    return result


def detect_tech_stack(repo_path: str) -> List[Dict[str, str]]:
    """
    Detect technology stack from repository files.

    Args:
        repo_path: Absolute path to the repository

    Returns:
        List of detected technologies
    """
    tech_stack = []

    for tech, patterns in TECH_STACK_PATTERNS.items():
        for filename, display_name in patterns:
            file_path = os.path.join(repo_path, filename)
            if os.path.exists(file_path):
                tech_stack.append(
                    {"name": display_name, "category": tech, "file": filename}
                )
                break

    # Check for common frameworks
    framework_patterns = {
        "React": [("src/index.js", "React"), ("src/App.js", "React")],
        "Vue": [("src/main.js", "Vue"), ("vue.config.js", "Vue")],
        "Angular": [("angular.json", "Angular")],
        "Django": [("manage.py", "Django"), ("settings.py", "Django")],
        "Flask": [("app.py", "Flask"), ("wsgi.py", "Flask")],
        "FastAPI": [("main.py", "FastAPI")],
        "Express": [("index.js", "Express"), ("app.js", "Express")],
    }

    for _framework, patterns in framework_patterns.items():
        for filename, display_name in patterns:
            file_path = os.path.join(repo_path, filename)
            if os.path.exists(file_path):
                tech_stack.append(
                    {"name": display_name, "category": "Framework", "file": filename}
                )
                break

    return tech_stack


def scan_security_issues(
    repo_path: str, severity_threshold: str = "medium"
) -> Dict[str, Any]:
    """
    Scan repository for security issues.

    Args:
        repo_path: Absolute path to the repository
        severity_threshold: Minimum severity to report (low, medium, high, critical)

    Returns:
        Dictionary with security findings
    """
    severity_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    min_severity = severity_order.get(severity_threshold.lower(), 1)

    findings = {"secrets": [], "vulnerabilities": [], "configuration_issues": []}

    # Skip binary and generated files
    skip_extensions = {".pyc", ".class", ".o", ".so", ".dll", ".exe", ".bin"}

    for root, dirs, files in os.walk(repo_path):
        # Skip common non-source directories
        dirs[:] = [
            d
            for d in dirs
            if d
            not in {
                "node_modules",
                "__pycache__",
                ".git",
                "venv",
                ".venv",
                "build",
                "dist",
            }
        ]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in skip_extensions:
                continue

            file_path = os.path.join(root, file)

            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    rel_path = os.path.relpath(file_path, repo_path)

                    # Check for secrets
                    for pattern, description in SECURITY_PATTERNS["Secrets"]:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            findings["secrets"].append(
                                {
                                    "file": rel_path,
                                    "type": description,
                                    "severity": "critical",
                                    "line": content[: match.start()].count("\n") + 1,
                                }
                            )

                    # Check for vulnerabilities
                    for pattern, description in SECURITY_PATTERNS["Vulnerabilities"]:
                        matches = re.finditer(pattern, content)
                        for match in matches:
                            findings["vulnerabilities"].append(
                                {
                                    "file": rel_path,
                                    "type": description,
                                    "severity": "high",
                                    "line": content[: match.start()].count("\n") + 1,
                                }
                            )
            except Exception:
                continue

    # Filter by severity
    filtered_findings = {}
    for category, items in findings.items():
        filtered = [
            f
            for f in items
            if severity_order.get(f.get("severity", "low"), 0) >= min_severity
        ]
        filtered_findings[category] = filtered

    return filtered_findings


def repo_recon(
    repository_path: str, depth: int = 3, include_hidden: bool = False, **kwargs
) -> Dict[str, Any]:
    """
    Main entry point for repository reconnaissance.

    Args:
        repository_path: Absolute path to the repository
        depth: Maximum depth to traverse
        include_hidden: Whether to include hidden files
        **kwargs: Additional parameters

    Returns:
        Comprehensive repository analysis
    """
    try:
        # Analyze structure
        structure = analyze_repository_structure(repository_path, depth, include_hidden)

        # Detect tech stack
        tech_stack = detect_tech_stack(repository_path)

        # Scan for security issues
        severity = kwargs.get("severity_threshold", "medium")
        security_issues = scan_security_issues(repository_path, severity)

        # Calculate risk score
        risk_score = min(
            100,
            len(security_issues.get("secrets", [])) * 20
            + len(security_issues.get("vulnerabilities", [])) * 10,
        )

        return {
            "status": "success",
            "repository": repository_path,
            "structure": structure,
            "tech_stack": tech_stack,
            "security": security_issues,
            "summary": {
                "total_files": structure.get("total_files", 0),
                "total_directories": structure.get("total_dirs", 0),
                "technologies_detected": len(tech_stack),
                "risk_score": risk_score,
                "security_issues": sum(len(v) for v in security_issues.values()),
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to analyze repository",
        }


def invoke(payload: dict) -> dict:
    """Main entry point for MCP skill invocation"""
    action = payload.get("action", "recon")

    if action == "recon":
        repo_path = payload.get("repository_path", "")
        depth = payload.get("depth", 3)
        include_hidden = payload.get("include_hidden", False)
        result = repo_recon(repo_path, depth, include_hidden)
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return {"result": result}


def register_skill():
    """Return skill metadata for MCP registration"""
    return {
        "name": "repo-recon",
        "description": "Map structure, tech stack, and risks of a repository",
        "version": "1.0.0",
        "domain": "APPLICATION_SECURITY",
    }
