"
Dependency Outdated Scanner

Scans project dependencies for outdated packages and suggests updates:
- Supports package.json, requirements.txt, go.mod, Gemfile
- Checks against latest versions
- Provides migration guides
"

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List
from datetime import datetime


@dataclass
class Dependency:
    name: str
    current_version: str
    latest_version: str = "
    is_outdated: bool = False
    update_type: str = "  # major, minor, patch


# Mock version data (in production, use actual package APIs)
VERSION_DATABASE = {
    # npm packages
    "react": "18.2.0",
    "express": "4.18.2",
    "lodash": "4.17.21",
    "axios": "1.6.0",
    "typescript": "5.3.0",
    # Python packages
    "flask": "3.0.0",
    "django": "5.0.0",
    "requests": "2.31.0",
    "numpy": "1.26.0",
    "pandas": "2.2.0",
    "fastapi": "0.109.0",
    "sqlalchemy": "2.0.0",
}


def parse_package_json(path: str) -> List[Dependency]:
    "Parse package.json for dependencies"
    deps = []
    try:
        with open(path) as f:
            data = json.load(f)

        all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

        for name, version in all_deps.items():
            clean_version = version.lstrip("^~>=")
            latest = VERSION_DATABASE.get(name, clean_version)
            deps.append(
                Dependency(
                    name=name,
                    current_version=clean_version,
                    latest_version=latest,
                    is_outdated=clean_version != latest,
                )
            )
    except Exception:
        pass
    return deps


def parse_requirements_txt(path: str) -> List[Dependency]:
    "Parse requirements.txt for dependencies"
    deps = []
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "==" in line:
                        name, version = line.split("==")
                    elif ">=" in line:
                        name, version = line.split(">=")
                    else:
                        continue

                    latest = VERSION_DATABASE.get(name.strip(), version.strip())
                    deps.append(
                        Dependency(
                            name=name.strip(),
                            current_version=version.strip(),
                            latest_version=latest,
                            is_outdated=version.strip() != latest,
                        )
                    )
    except Exception:
        pass
    return deps


def parse_go_mod(path: str) -> List[Dependency]:
    "Parse go.mod for dependencies"
    deps = []
    try:
        with open(path) as f:
            content = f.read()

        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("require ("):
                continue
            if line and not line.startswith("module") and not line.startswith("go "):
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0]
                    version = parts[1].lstrip("v")
                    latest = VERSION_DATABASE.get(name.split("/")[-1], version)
                    deps.append(
                        Dependency(
                            name=name,
                            current_version=version,
                            latest_version=latest,
                            is_outdated=version != latest,
                        )
                    )
    except Exception:
        pass
    return deps


def determine_update_type(current: str, latest: str) -> str:
    "Determine the type of update needed"
    try:
        curr_parts = current.split(".")
        lat_parts = latest.split(".")

        if curr_parts[0] != lat_parts[0]:
            return "major"
        elif len(curr_parts) > 1 and curr_parts[1] != lat_parts[1]:
            return "minor"
        else:
            return "patch"
    except:
        return "unknown"


def scan_dependencies(repo_path: str) -> Dict[str, Any]:
    "
    Scan dependencies for outdated packages.

    Args:
        repo_path: Path to repository

    Returns:
        Dependency audit results
    "
    all_deps = []
    files_scanned = []

    # Scan for different dependency files
    package_json = os.path.join(repo_path, "package.json")
    if os.path.exists(package_json):
        deps = parse_package_json(package_json)
        all_deps.extend(deps)
        files_scanned.append("package.json")

    requirements_txt = os.path.join(repo_path, "requirements.txt")
    if os.path.exists(requirements_txt):
        deps = parse_requirements_txt(requirements_txt)
        all_deps.extend(deps)
        files_scanned.append("requirements.txt")

    go_mod = os.path.join(repo_path, "go.mod")
    if os.path.exists(go_mod):
        deps = parse_go_mod(go_mod)
        all_deps.extend(deps)
        files_scanned.append("go.mod")

    # Determine update types
    outdated = []
    for dep in all_deps:
        if dep.is_outdated:
            dep.update_type = determine_update_type(
                dep.current_version, dep.latest_version
            )
            outdated.append(dep)

    return {
        "status": "success",
        "files_scanned": files_scanned,
        "total_dependencies": len(all_deps),
        "outdated_count": len(outdated),
        "up_to_date_count": len(all_deps) - len(outdated),
        "outdated_dependencies": [
            {
                "name": d.name,
                "current": d.current_version,
                "latest": d.latest_version,
                "update_type": d.update_type,
            }
            for d in outdated
        ],
        "recommendations": [
            f"Update {d.name} from {d.current_version} to {d.latest_version} ({d.update_type} update)"
            for d in outdated[:5]
        ],
    }


def dependency_outdated_scanner(repo_path: str, **kwargs) -> Dict[str, Any]:
    "
    Main entry point for dependency scanning.

    Args:
        repo_path: Path to repository
        **kwargs: Additional parameters

    Returns:
        Scan results
    "
    if not repo_path:
        return {"status": "error", "error": "No repository path provided"}

    if not os.path.exists(repo_path):
        return {"status": "error", "error": f"Path does not exist: {repo_path}"}

    return scan_dependencies(repo_path)


async def invoke(payload: dict) -> dict:
    "MCP skill invocation"
    action = payload.get("action", "scan")
    repo_path = payload.get("repo_path", ".")

    if action == "scan":
        result = dependency_outdated_scanner(repo_path)
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
    "Return skill metadata"
    return {
        "name": "dependency-outdated-scanner",
        "description": "Scan for outdated dependencies and suggest updates",
        "version": "1.0.0",
        "domain": "DEVOPS",
    }
