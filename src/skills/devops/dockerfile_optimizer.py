#!/usr/bin/env python3
"""
Skill: dockerfile-optimizer
Domain: devops
Description: Analyzes and optimizes Dockerfiles for size, build speed, and best practices
"""

import re
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


BASE_IMAGE_SIZES = {
    "ubuntu": 80,
    "debian": 120,
    "alpine": 5,
    "centos": 200,
    "fedora": 180,
    "node": 350,
    "node:alpine": 50,
    "python": 900,
    "python:alpine": 40,
    "golang": 800,
    "golang:alpine": 50,
    "ruby": 700,
    "ruby:alpine": 40,
    "java": 500,
    "openjdk": 500,
    "maven": 500,
    "gradle": 500,
    "rust": 1500,
    "nginx": 25,
    "redis": 30,
    "postgres": 350,
    "mysql": 450,
    "mongo": 400,
}


class IssueSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class DockerfileIssue:
    severity: IssueSeverity
    category: str
    description: str
    line: int
    suggestion: str


@dataclass
class Optimization:
    category: str
    description: str
    before: str
    after: str
    estimated_savings_mb: float
    priority: int


@dataclass
class DockerfileParser:
    lines: List[str]
    instructions: List[Dict[str, Any]] = field(default_factory=list)
    base_image: Optional[str] = None
    stages: List[Dict[str, Any]] = field(default_factory=list)

    def parse(self) -> None:
        current_stage = {"name": "base", "from": None, "instructions": []}

        for idx, line in enumerate(self.lines):
            stripped = line.strip()

            if not stripped or stripped.startswith("#"):
                continue

            upper = stripped.upper()

            if upper.startswith("FROM"):
                if current_stage["from"]:
                    self.stages.append(current_stage)
                    current_stage = {
                        "name": f"stage{len(self.stages)}",
                        "from": None,
                        "instructions": [],
                    }

                match = re.match(
                    r"FROM\s+(?:--platform=[^\s]+\s+)?(\S+)(?:\s+AS\s+(\S+))?",
                    stripped,
                    re.IGNORECASE,
                )
                if match:
                    base = match.group(1)
                    stage_name = match.group(2)
                    current_stage["from"] = base
                    current_stage["name"] = stage_name or current_stage["name"]
                    if not self.base_image:
                        self.base_image = base
                    self.instructions.append(
                        {
                            "type": "FROM",
                            "value": base,
                            "line": idx + 1,
                            "stage": len(self.stages),
                        }
                    )

            elif upper.startswith("RUN"):
                cmd = stripped[4:].strip()
                current_stage["instructions"].append(
                    {"type": "RUN", "value": cmd, "line": idx + 1}
                )
                self.instructions.append({"type": "RUN", "value": cmd, "line": idx + 1})

            elif upper.startswith("COPY"):
                cmd = stripped[5:].strip()
                current_stage["instructions"].append(
                    {"type": "COPY", "value": cmd, "line": idx + 1}
                )
                self.instructions.append(
                    {"type": "COPY", "value": cmd, "line": idx + 1}
                )

            elif upper.startswith("ADD"):
                cmd = stripped[4:].strip()
                current_stage["instructions"].append(
                    {"type": "ADD", "value": cmd, "line": idx + 1}
                )
                self.instructions.append({"type": "ADD", "value": cmd, "line": idx + 1})

            elif upper.startswith("WORKDIR"):
                cmd = stripped[8:].strip()
                current_stage["instructions"].append(
                    {"type": "WORKDIR", "value": cmd, "line": idx + 1}
                )
                self.instructions.append(
                    {"type": "WORKDIR", "value": cmd, "line": idx + 1}
                )

            elif upper.startswith("ENV"):
                cmd = stripped[4:].strip()
                current_stage["instructions"].append(
                    {"type": "ENV", "value": cmd, "line": idx + 1}
                )
                self.instructions.append({"type": "ENV", "value": cmd, "line": idx + 1})

            elif upper.startswith("EXPOSE"):
                cmd = stripped[8:].strip()
                current_stage["instructions"].append(
                    {"type": "EXPOSE", "value": cmd, "line": idx + 1}
                )
                self.instructions.append(
                    {"type": "EXPOSE", "value": cmd, "line": idx + 1}
                )

            elif upper.startswith("LABEL"):
                cmd = stripped[6:].strip()
                current_stage["instructions"].append(
                    {"type": "LABEL", "value": cmd, "line": idx + 1}
                )
                self.instructions.append(
                    {"type": "LABEL", "value": cmd, "line": idx + 1}
                )

            elif upper.startswith("ARG"):
                cmd = stripped[4:].strip()
                current_stage["instructions"].append(
                    {"type": "ARG", "value": cmd, "line": idx + 1}
                )
                self.instructions.append({"type": "ARG", "value": cmd, "line": idx + 1})

            elif upper.startswith("ENTRYPOINT"):
                cmd = stripped[11:].strip()
                current_stage["instructions"].append(
                    {"type": "ENTRYPOINT", "value": cmd, "line": idx + 1}
                )
                self.instructions.append(
                    {"type": "ENTRYPOINT", "value": cmd, "line": idx + 1}
                )

            elif upper.startswith("CMD"):
                cmd = stripped[4:].strip()
                current_stage["instructions"].append(
                    {"type": "CMD", "value": cmd, "line": idx + 1}
                )
                self.instructions.append({"type": "CMD", "value": cmd, "line": idx + 1})

            elif upper.startswith("VOLUME"):
                cmd = stripped[7:].strip()
                current_stage["instructions"].append(
                    {"type": "VOLUME", "value": cmd, "line": idx + 1}
                )
                self.instructions.append(
                    {"type": "VOLUME", "value": cmd, "line": idx + 1}
                )

            elif upper.startswith("USER"):
                cmd = stripped[5:].strip()
                current_stage["instructions"].append(
                    {"type": "USER", "value": cmd, "line": idx + 1}
                )
                self.instructions.append(
                    {"type": "USER", "value": cmd, "line": idx + 1}
                )

            elif upper.startswith("HEALTHCHECK"):
                cmd = stripped[12:].strip()
                current_stage["instructions"].append(
                    {"type": "HEALTHCHECK", "value": cmd, "line": idx + 1}
                )
                self.instructions.append(
                    {"type": "HEALTHCHECK", "value": cmd, "line": idx + 1}
                )

            elif upper.startswith("ONBUILD"):
                cmd = stripped[8:].strip()
                current_stage["instructions"].append(
                    {"type": "ONBUILD", "value": cmd, "line": idx + 1}
                )
                self.instructions.append(
                    {"type": "ONBUILD", "value": cmd, "line": idx + 1}
                )

        if current_stage["from"]:
            self.stages.append(current_stage)


def detect_issues(dockerfile: str, parser: DockerfileParser) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []

    if not parser.base_image:
        issues.append(
            {
                "severity": "critical",
                "category": "structure",
                "description": "No base image specified (no FROM instruction found)",
                "line": 0,
                "suggestion": "Add a FROM instruction at the beginning of the Dockerfile",
            }
        )
        return issues

    base_image_lower = parser.base_image.lower()
    is_alpine = "alpine" in base_image_lower

    if base_image_lower in BASE_IMAGE_SIZES:
        size = BASE_IMAGE_SIZES[base_image_lower]
        if size > 100 and not is_alpine:
            issues.append(
                {
                    "severity": "high",
                    "category": "size",
                    "description": f"Large base image '{parser.base_image}' (~{size}MB)",
                    "line": 1,
                    "suggestion": f"Consider using '{parser.base_image.split(':')[0]}:alpine' or a slim variant (~5-50MB savings)",
                }
            )

    if "latest" in base_image_lower:
        issues.append(
            {
                "severity": "medium",
                "category": "best_practice",
                "description": "Using 'latest' tag is not recommended",
                "line": 1,
                "suggestion": "Use a specific version tag for reproducibility (e.g., node:18-alpine)",
            }
        )

    run_count = sum(1 for inst in parser.instructions if inst["type"] == "RUN")
    if run_count > 20:
        issues.append(
            {
                "severity": "medium",
                "category": "layer_efficiency",
                "description": f"Too many RUN commands ({run_count}) can increase image size",
                "line": 0,
                "suggestion": "Combine multiple RUN commands using && to reduce layers",
            }
        )

    copy_count = sum(
        1 for inst in parser.instructions if inst["type"] in ["COPY", "ADD"]
    )
    if copy_count > 15:
        issues.append(
            {
                "severity": "medium",
                "category": "layer_efficiency",
                "description": f"Many COPY/ADD commands ({copy_count}) may indicate opportunity for consolidation",
                "line": 0,
                "suggestion": "Combine related files and use .dockerignore to exclude unnecessary files",
            }
        )

    has_caching_issue = False
    prev_was_copy = False
    for inst in parser.instructions:
        if inst["type"] in ["COPY", "ADD"]:
            if prev_was_copy:
                has_caching_issue = True
            prev_was_copy = True
        elif inst["type"] == "RUN":
            prev_was_copy = False

    if has_caching_issue:
        issues.append(
            {
                "severity": "low",
                "category": "caching",
                "description": "Multiple consecutive COPY commands may benefit from consolidation",
                "line": 0,
                "suggestion": "Order instructions from least to most frequently changing for better layer caching",
            }
        )

    for inst in parser.instructions:
        if inst["type"] == "ADD" and "*" in inst["value"]:
            issues.append(
                {
                    "severity": "low",
                    "category": "best_practice",
                    "description": "ADD with wildcards may include unwanted files",
                    "line": inst["line"],
                    "suggestion": "Use COPY instead of ADD unless extracting archives or fetching URLs",
                }
            )

        if (
            inst["type"] == "RUN"
            and "apt-get update" in inst["value"].lower()
            and "apt-get clean" not in inst["value"].lower()
        ):
            if "rm -rf /var/lib/apt/lists" not in inst["value"].lower():
                issues.append(
                    {
                        "severity": "high",
                        "category": "size",
                        "description": "apt-get update without cleanup increases image size",
                        "line": inst["line"],
                        "suggestion": "Add '&& apt-get clean && rm -rf /var/lib/apt/lists/*' to reduce size by ~100MB",
                    }
                )

        if (
            inst["type"] == "RUN"
            and "pip install" in inst["value"].lower()
            and "--no-cache-dir" not in inst["value"].lower()
        ):
            issues.append(
                {
                    "severity": "medium",
                    "category": "size",
                    "description": "pip install without --no-cache-dir caches downloaded packages",
                    "line": inst["line"],
                    "suggestion": "Use 'pip install --no-cache-dir' to avoid storing pip cache (~50MB savings)",
                }
            )

        if (
            inst["type"] == "RUN"
            and "npm install" in inst["value"].lower()
            and "npm cache clean" not in inst["value"].lower()
        ):
            issues.append(
                {
                    "severity": "medium",
                    "category": "size",
                    "description": "npm install without cache cleanup",
                    "line": inst["line"],
                    "suggestion": "Use 'npm install --production && npm cache clean --force' for production",
                }
            )

    has_explicit_user = any(inst["type"] == "USER" for inst in parser.instructions)
    if not has_explicit_user and parser.base_image:
        issues.append(
            {
                "severity": "low",
                "category": "security",
                "description": "No explicit USER instruction - running as root",
                "line": 0,
                "suggestion": "Create and use a non-root user for better security",
            }
        )

    has_healthcheck = any(inst["type"] == "HEALTHCHECK" for inst in parser.instructions)
    if not has_healthcheck:
        issues.append(
            {
                "severity": "low",
                "category": "best_practice",
                "description": "No HEALTHCHECK instruction defined",
                "line": 0,
                "suggestion": "Add HEALTHCHECK to help Docker detect unresponsive containers",
            }
        )

    if len(parser.stages) == 1 and len(parser.instructions) > 15:
        issues.append(
            {
                "severity": "medium",
                "category": "optimization",
                "description": "Single-stage build with many instructions - consider multi-stage build",
                "line": 0,
                "suggestion": "Multi-stage builds can significantly reduce final image size",
            }
        )

    return issues


def generate_optimizations(
    dockerfile: str, parser: DockerfileParser, options: dict
) -> List[Dict[str, Any]]:
    optimizations: List[Dict[str, Any]] = []
    target_size = options.get("target_size_mb", 100)
    include_multistage = options.get("include_multistage", True)

    if parser.base_image and "alpine" not in parser.base_image.lower():
        base_name = parser.base_image.split(":")[0]
        alpine_image = f"{base_name}:alpine"
        optimizations.append(
            {
                "category": "base_image",
                "description": f"Switch to Alpine-based image for smaller footprint",
                "before": parser.base_image,
                "after": alpine_image,
                "estimated_savings_mb": 200,
                "priority": 1,
            }
        )

    optimized_lines = dockerfile.split("\n")
    new_lines = []
    cleaned_apt = False
    cleaned_pip = False
    cleaned_npm = False

    for line in optimized_lines:
        original = line

        if "apt-get update" in line.lower() and not cleaned_apt:
            if "&&" in line:
                if (
                    "apt-get clean" not in line
                    and "rm -rf /var/lib/apt/lists" not in line
                ):
                    line = line + " && apt-get clean && rm -rf /var/lib/apt/lists/*"
                    cleaned_apt = True
                    optimizations.append(
                        {
                            "category": "cleanup",
                            "description": "Add apt cache cleanup to reduce image size",
                            "before": original.strip(),
                            "after": line.strip(),
                            "estimated_savings_mb": 100,
                            "priority": 2,
                        }
                    )
            else:
                idx = len(new_lines)
                new_lines.append(line)
                new_lines.append("RUN apt-get clean && rm -rf /var/lib/apt/lists/*")
                cleaned_apt = True
                optimizations.append(
                    {
                        "category": "cleanup",
                        "description": "Add apt cache cleanup to reduce image size",
                        "before": "apt-get without cleanup",
                        "after": "apt-get + cleanup",
                        "estimated_savings_mb": 100,
                        "priority": 2,
                    }
                )
                continue

        if "pip install" in line.lower() and not cleaned_pip:
            if "--no-cache-dir" not in line.lower():
                line = line.replace("pip install", "pip install --no-cache-dir")
                cleaned_pip = True
                optimizations.append(
                    {
                        "category": "cleanup",
                        "description": "Disable pip caching",
                        "before": original.strip(),
                        "after": line.strip(),
                        "estimated_savings_mb": 50,
                        "priority": 3,
                    }
                )

        if "npm install" in line.lower() and not cleaned_npm:
            if "--production" not in line.lower():
                line = line.replace("npm install", "npm install --production")
                cleaned_npm = True
                optimizations.append(
                    {
                        "category": "cleanup",
                        "description": "Install only production dependencies",
                        "before": original.strip(),
                        "after": line.strip(),
                        "estimated_savings_mb": 100,
                        "priority": 3,
                    }
                )

        new_lines.append(line)

    run_commands = [l for l in new_lines if l.strip().upper().startswith("RUN")]
    if len(run_commands) > 10:
        optimizations.append(
            {
                "category": "layer_optimization",
                "description": f"Consolidate {len(run_commands)} RUN commands into fewer layers",
                "before": f"{len(run_commands)} separate RUN commands",
                "after": "Combined RUN commands with &&",
                "estimated_savings_mb": 20,
                "priority": 4,
            }
        )

    if include_multistage and len(parser.stages) == 1 and len(parser.instructions) > 10:
        optimizations.append(
            {
                "category": "multistage",
                "description": "Implement multi-stage build to separate build dependencies",
                "before": "Single-stage build",
                "after": "Multi-stage build with builder pattern",
                "estimated_savings_mb": 300,
                "priority": 1,
            }
        )

    return optimizations


def create_optimized_dockerfile(dockerfile: str, options: dict) -> str:
    parser = DockerfileParser(lines=dockerfile.split("\n"))
    parser.parse()

    optimized_lines = []
    base_image_changed = False

    for line in dockerfile.split("\n"):
        original = line

        if line.strip().upper().startswith("FROM"):
            match = re.match(
                r"FROM\s+(?:--platform=[^\s]+\s+)?(\S+)(?:\s+AS\s+(\S+))?",
                line.strip(),
                re.IGNORECASE,
            )
            if match:
                base = match.group(1)
                if "alpine" not in base.lower() and "slim" not in base.lower():
                    base_name = base.split(":")[0]
                    new_base = f"{base_name}:alpine"
                    line = line.replace(base, new_base)
                    base_image_changed = True

        if "apt-get update" in line.lower():
            if "apt-get clean" not in line and "rm -rf /var/lib/apt/lists" not in line:
                if "&&" in line:
                    line = line + " && apt-get clean && rm -rf /var/lib/apt/lists/*"
                else:
                    line = line + " && apt-get clean && rm -rf /var/lib/apt/lists/*"

        if "pip install" in line.lower() and "--no-cache-dir" not in line.lower():
            line = line.replace("pip install", "pip install --no-cache-dir")

        if "npm install" in line.lower() and "--production" not in line.lower():
            line = line.replace("npm install", "npm install --production")

        optimized_lines.append(line)

    if options.get("add_user", True):
        has_user = any(l.strip().upper().startswith("USER") for l in optimized_lines)
        if not has_user:
            optimized_lines.append("")
            optimized_lines.append("USER node")

    if options.get("add_healthcheck", False):
        has_healthcheck = any(
            l.strip().upper().startswith("HEALTHCHECK") for l in optimized_lines
        )
        if not has_healthcheck:
            optimized_lines.append("")
            optimized_lines.append(
                "HEALTHCHECK --interval=30s --timeout=3s CMD node -e \"require('http').get('http://localhost:\", (r) => process.exit(r.statusCode === 200 ? 0 : 1))\""
            )

    return "\n".join(optimized_lines)


def estimate_savings(issues: List[Dict], optimizations: List[Dict]) -> Dict[str, Any]:
    size_savings = 0
    build_time_savings = 0

    for opt in optimizations:
        size_savings += opt.get("estimated_savings_mb", 0)

    for issue in issues:
        if issue.get("severity") in ["high", "critical"]:
            if "apt" in issue.get("description", "").lower():
                size_savings += 100
            if "pip" in issue.get("description", "").lower():
                size_savings += 50

    run_commands_issue = sum(1 for i in issues if "RUN" in i.get("description", ""))
    if run_commands_issue > 5:
        build_time_savings += run_commands_issue * 5

    return {
        "size_reduction_mb": size_savings,
        "size_reduction_percent": min(size_savings / 10, 95),
        "build_time_savings_seconds": build_time_savings,
        "layers_reduced": sum(
            1 for o in optimizations if o.get("category") == "layer_optimization"
        )
        * 5,
    }


def dockerfile_optimizer(dockerfile: str, options: dict = None) -> dict:
    if options is None:
        options = {}

    if not dockerfile or not dockerfile.strip():
        return {
            "status": "error",
            "error": "No Dockerfile content provided",
            "issues": [],
            "optimizations": [],
            "optimized_dockerfile": "",
            "estimated_savings": {},
        }

    try:
        parser = DockerfileParser(lines=dockerfile.split("\n"))
        parser.parse()

        issues = detect_issues(dockerfile, parser)
        optimizations = generate_optimizations(dockerfile, parser, options)
        optimized_dockerfile = create_optimized_dockerfile(dockerfile, options)
        estimated_savings = estimate_savings(issues, optimizations)

        return {
            "status": "success",
            "issues": issues,
            "optimizations": optimizations,
            "optimized_dockerfile": optimized_dockerfile,
            "estimated_savings": estimated_savings,
            "analysis": {
                "base_image": parser.base_image,
                "total_instructions": len(parser.instructions),
                "stages": len(parser.stages),
                "layers": len(
                    [
                        i
                        for i in parser.instructions
                        if i["type"] in ["RUN", "COPY", "ADD"]
                    ]
                ),
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "issues": [],
            "optimizations": [],
            "optimized_dockerfile": "",
            "estimated_savings": {},
        }


def invoke(payload: dict) -> dict:
    dockerfile = payload.get("dockerfile", "")
    options = payload.get("options", {})

    if not dockerfile:
        return {"status": "error", "error": "No dockerfile provided"}

    return dockerfile_optimizer(dockerfile, options)


def register_skill() -> dict:
    return {
        "name": "dockerfile-optimizer",
        "description": "Analyzes and optimizes Dockerfiles for size, build speed, and best practices",
        "version": "1.0.0",
        "functions": {
            "dockerfile_optimizer": {
                "description": "Analyze and optimize a Dockerfile for better performance and smaller image size",
                "parameters": {
                    "dockerfile": {
                        "type": "string",
                        "description": "Dockerfile content to optimize",
                    },
                    "options": {
                        "type": "object",
                        "description": "Optimization options",
                        "properties": {
                            "target_size_mb": {
                                "type": "number",
                                "description": "Target image size in MB",
                            },
                            "include_multistage": {
                                "type": "boolean",
                                "description": "Include multi-stage build suggestions",
                            },
                            "add_user": {
                                "type": "boolean",
                                "description": "Add non-root USER instruction",
                            },
                            "add_healthcheck": {
                                "type": "boolean",
                                "description": "Add HEALTHCHECK instruction",
                            },
                        },
                    },
                },
                "returns": {
                    "status": "string",
                    "issues": "array",
                    "optimizations": "array",
                    "optimized_dockerfile": "string",
                    "estimated_savings": "object",
                    "analysis": "object",
                },
            },
            "invoke": {
                "description": "Entry point for skill invocation",
                "parameters": {"payload": {"type": "object"}},
            },
        },
        "checks_supported": [
            "large_base_image",
            "no_caching",
            "too_many_layers",
            "apt_cache",
            "pip_cache",
            "npm_cache",
            "missing_user",
            "missing_healthcheck",
            "latest_tag",
            "consecutive_copies",
        ],
    }


if __name__ == "__main__":
    sample_dockerfile = """FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
COPY . /app
RUN pip install flask
RUN pip install requests
RUN npm install
COPY package.json /app/
RUN echo "done"
CMD ["python3", "app.py"]
"""

    result = dockerfile_optimizer(sample_dockerfile, {"include_multistage": True})
    print(f"Status: {result['status']}")
    print(f"Issues found: {len(result['issues'])}")
    for issue in result["issues"]:
        print(f"  - [{issue['severity']}] {issue['description']}")

    print(f"\nOptimizations: {len(result['optimizations'])}")
    for opt in result["optimizations"]:
        print(
            f"  - [{opt['category']}] {opt['description']} (~{opt['estimated_savings_mb']}MB)"
        )

    print(f"\nEstimated savings: {result['estimated_savings']}")
    print(f"\nOptimized Dockerfile:\n{result['optimized_dockerfile']}")
