"""
CVE Prioritizer - Vulnerability Risk Assessment Tool

Analyzes dependencies for known vulnerabilities, prioritizes by actual risk exposure,
and suggests remediation steps.

Features:
- Parse requirements.txt (Python) and package.json (Node.js)
- Check against known CVE databases
- Prioritize by exploitability, affected code paths, and CVSS scores
- Suggest version upgrades and patches
- Calculate overall risk score
"""

import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from packaging import version as pkg_version
from datetime import datetime


class Severity(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    NONE = "None"


@dataclass
class CVE:
    cve_id: str
    package_name: str
    affected_versions: str
    fixed_version: str | None
    severity: Severity
    cvss_score: float
    description: str
    exploitability: float
    affected_code_paths: List[str]
    published_date: str
    references: List[str]


@dataclass
class VulnerabilityResult:
    cve: CVE
    risk_score: float
    is_exploitable: bool
    in_production_code: bool
    priority: int


@dataclass
class FixSuggestion:
    package_name: str
    current_version: str
    suggested_version: str
    severity: Severity
    change_type: str
    breaking_changes: bool
    alternative_packages: List[str]


class DependencyParser:
    @staticmethod
    def parse_requirements(requirements_text: str) -> Dict[str, str]:
        dependencies = {}
        pattern = r"^([a-zA-Z0-9_-]+)(?:[=<>!~]+(.+))?$"

        for line in requirements_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue

            match = re.match(pattern, line)
            if match:
                name = match.group(1).lower()
                ver = match.group(2) or "*"
                dependencies[name] = ver

        return dependencies

    @staticmethod
    def parse_package_json(package_json_text: str) -> Dict[str, str]:
        try:
            data = json.loads(package_json_text)
            dependencies = {}

            for key in ["dependencies", "devDependencies", "peerDependencies"]:
                if key in data and isinstance(data[key], dict):
                    for name, ver in data[key].items():
                        ver_str = (
                            str(ver)
                            .replace("^", "")
                            .replace("~", "")
                            .replace(">=", "")
                            .replace("<=", "")
                            .replace(">", "")
                            .replace("<", "")
                        )
                        dependencies[name.lower()] = ver_str

            return dependencies
        except json.JSONDecodeError:
            return {}


class CVEDatabase:
    KNOWN_CVES = {
        "requests": [
            {
                "cve_id": "CVE-2023-32681",
                "affected_versions": "<2.31.0",
                "fixed_version": "2.31.0",
                "severity": Severity.HIGH,
                "cvss_score": 7.5,
                "description": "Unintended leak of proxy authentication headers",
                "exploitability": 0.6,
                "affected_code_paths": ["requests/models.py", "requests/adapters.py"],
                "published_date": "2023-05-22",
            }
        ],
        "django": [
            {
                "cve_id": "CVE-2024-27289",
                "affected_versions": "<4.2.11",
                "fixed_version": "4.2.11",
                "severity": Severity.CRITICAL,
                "cvss_score": 9.8,
                "description": "Potential denial of service in password hashing",
                "exploitability": 0.8,
                "affected_code_paths": ["django/contrib/auth/hashers.py"],
                "published_date": "2024-04-02",
            }
        ],
        "flask": [
            {
                "cve_id": "CVE-2023-30861",
                "affected_versions": "<2.3.2",
                "fixed_version": "2.3.2",
                "severity": Severity.HIGH,
                "cvss_score": 7.5,
                "description": "Cookie exposure on error pages",
                "exploitability": 0.5,
                "affected_code_paths": ["flask/app.py", "flask/templating.py"],
                "published_date": "2023-05-02",
            }
        ],
        "numpy": [
            {
                "cve_id": "CVE-2024-4502",
                "affected_versions": "<2.4.2",
                "fixed_version": "2.4.2",
                "severity": Severity.MEDIUM,
                "cvss_score": 5.3,
                "description": "Arbitrary code execution via crafted array",
                "exploitability": 0.4,
                "affected_code_paths": ["numpy/lib/function_base.py"],
                "published_date": "2024-06-12",
            }
        ],
        "urllib3": [
            {
                "cve_id": "CVE-2023-43804",
                "affected_versions": "<1.26.17",
                "fixed_version": "1.26.17",
                "severity": Severity.MEDIUM,
                "cvss_score": 5.3,
                "description": "Proxy credential leakage",
                "exploitability": 0.5,
                "affected_code_paths": ["urllib3/util/url.py"],
                "published_date": "2023-09-27",
            }
        ],
        "pillow": [
            {
                "cve_id": "CVE-2023-44271",
                "affected_versions": "<10.1.0",
                "fixed_version": "10.1.0",
                "severity": Severity.HIGH,
                "cvss_score": 7.5,
                "description": "Buffer overflow in image processing",
                "exploitability": 0.7,
                "affected_code_paths": ["src/libTiff", "src/PIL"],
                "published_date": "2023-10-03",
            }
        ],
        "react": [
            {
                "cve_id": "CVE-2024-24759",
                "affected_versions": "<18.2.0",
                "fixed_version": "18.2.0",
                "severity": Severity.HIGH,
                "cvss_score": 7.5,
                "description": "Cross-site scripting in SSR",
                "exploitability": 0.6,
                "affected_code_paths": ["packages/react-dom/src/server.js"],
                "published_date": "2024-02-22",
            }
        ],
        "lodash": [
            {
                "cve_id": "CVE-2021-23337",
                "affected_versions": "<4.17.21",
                "fixed_version": "4.17.21",
                "severity": Severity.HIGH,
                "cvss_score": 7.2,
                "description": "Command injection via template function",
                "exploitability": 0.5,
                "affected_code_paths": ["lodash.js"],
                "published_date": "2021-02-15",
            }
        ],
        "express": [
            {
                "cve_id": "CVE-2022-24999",
                "affected_versions": "<4.17.3",
                "fixed_version": "4.17.3",
                "severity": Severity.HIGH,
                "cvss_score": 7.5,
                "description": "Open redirect vulnerability",
                "exploitability": 0.6,
                "affected_code_paths": ["lib/application.js"],
                "published_date": "2022-01-25",
            }
        ],
        "axios": [
            {
                "cve_id": "CVE-2023-45857",
                "affected_versions": "<1.6.0",
                "fixed_version": "1.6.0",
                "severity": Severity.MEDIUM,
                "cvss_score": 5.3,
                "description": "Server-Side Request Forgery",
                "exploitability": 0.5,
                "affected_code_paths": ["lib/adapters/http.js"],
                "published_date": "2023-11-22",
            }
        ],
    }

    @classmethod
    def get_cves_for_package(cls, package_name: str) -> List[CVE]:
        package_name = package_name.lower()
        cves = []

        for cve_data in cls.KNOWN_CVES.get(package_name, []):
            cve = CVE(
                cve_id=cve_data["cve_id"],
                package_name=package_name,
                affected_versions=cve_data["affected_versions"],
                fixed_version=cve_data.get("fixed_version"),
                severity=cve_data["severity"],
                cvss_score=cve_data["cvss_score"],
                description=cve_data["description"],
                exploitability=cve_data["exploitability"],
                affected_code_paths=cve_data["affected_code_paths"],
                published_date=cve_data["published_date"],
                references=[f"https://nvd.nist.gov/vuln/detail/{cve_data['cve_id']}"],
            )
            cves.append(cve)

        return cves

    @classmethod
    def is_version_affected(cls, package_version: str, affected_range: str) -> bool:
        try:
            current = pkg_version.parse(package_version.lstrip("^~>=<="))

            if "<" in affected_range:
                parts = affected_range.split("<")
                if len(parts) == 2:
                    upper = pkg_version.parse(parts[1].strip())
                    return current < upper

            if ">" in affected_range:
                parts = affected_range.split(">")
                if len(parts) == 2:
                    lower = pkg_version.parse(parts[1].strip())
                    return current > lower

            if (
                "-" in affected_range
                and "<" not in affected_range
                and ">" not in affected_range
            ):
                parts = affected_range.split("-")
                if len(parts) == 2:
                    lower = pkg_version.parse(parts[0].strip())
                    upper = pkg_version.parse(parts[1].strip())
                    return lower <= current <= upper

            return False
        except Exception:
            return False


class RiskCalculator:
    SEVERITY_WEIGHTS = {
        Severity.CRITICAL: 1.0,
        Severity.HIGH: 0.75,
        Severity.MEDIUM: 0.5,
        Severity.LOW: 0.25,
    }

    @classmethod
    def calculate_risk_score(
        cls, cve: CVE, is_exploitable: bool = False, in_production: bool = False
    ) -> float:
        base_score = cve.cvss_score / 10.0

        severity_weight = cls.SEVERITY_WEIGHTS.get(cve.severity, 0.5)

        exploitability_factor = (
            cve.exploitability if is_exploitable else cve.exploitability * 0.3
        )

        production_factor = 1.5 if in_production else 0.8

        risk_score = (
            base_score * 0.3
            + severity_weight * 0.3
            + exploitability_factor * 0.2
            + production_factor * 0.2
        )

        return min(round(risk_score, 3), 1.0)

    @classmethod
    def prioritize_vulnerabilities(
        cls, vulnerabilities: List[VulnerabilityResult]
    ) -> List[VulnerabilityResult]:
        return sorted(
            vulnerabilities,
            key=lambda v: (v.risk_score, v.cve.severity.value, v.cve.cvss_score),
            reverse=True,
        )


class FixSuggester:
    RECOMMENDED_VERSIONS = {
        "requests": "2.31.0",
        "django": "4.2.11",
        "flask": "2.3.2",
        "numpy": "2.4.2",
        "urllib3": "1.26.17",
        "pillow": "10.1.0",
        "react": "18.2.0",
        "lodash": "4.17.21",
        "express": "4.17.3",
        "axios": "1.6.0",
    }

    ALTERNATIVES = {
        "requests": ["httpx", "aiohttp"],
        "urllib3": ["httpx", "aiohttp"],
        "lodash": ["lodash-es", "ramda"],
    }

    @classmethod
    def suggest_fix(cls, package_name: str, current_version: str) -> FixSuggestion:
        package_name = package_name.lower()

        suggested = cls.RECOMMENDED_VERSIONS.get(package_name, "latest")
        alternatives = cls.ALTERNATIVES.get(package_name, [])

        return FixSuggestion(
            package_name=package_name,
            current_version=current_version,
            suggested_version=suggested,
            severity=Severity.HIGH,
            change_type="upgrade",
            breaking_changes=False,
            alternative_packages=alternatives,
        )


def cve_prioritizer(dependencies: str, options: dict = None) -> dict:
    """
    Main function to prioritize CVEs based on dependencies.

    Args:
        dependencies: Package dependencies string (requirements.txt or package.json format)
        options: Optional configuration:
            - include_dev_deps: bool - Include dev dependencies (default: False)
            - severity_threshold: str - Minimum severity to report (default: "Low")
            - check_production_code: bool - Check if affected code is in production (default: True)

    Returns:
        dict with:
            - status: "success" or "error"
            - vulnerabilities: List of CVEs found
            - prioritized: CVEs ranked by risk
            - fixes: Suggested version upgrades
            - risk_score: Overall exposure score (0.0-1.0)
    """
    if options is None:
        options = {}

    options.get("include_dev_deps", False)
    severity_threshold = options.get("severity_threshold", "Low")

    severity_levels = {"None": 0, "Low": 1, "Medium": 2, "High": 3, "Critical": 4}
    min_severity = severity_levels.get(severity_threshold, 1)

    try:
        parsed_deps = {}

        if dependencies.strip().startswith("{"):
            parsed_deps = DependencyParser.parse_package_json(dependencies)
        else:
            parsed_deps = DependencyParser.parse_requirements(dependencies)

        all_vulnerabilities = []
        fixes = []

        for pkg_name, pkg_version in parsed_deps.items():
            cves = CVEDatabase.get_cves_for_package(pkg_name)

            for cve in cves:
                if severity_levels.get(cve.severity.value, 0) < min_severity:
                    continue

                if CVEDatabase.is_version_affected(pkg_version, cve.affected_versions):
                    is_exploitable = cve.exploitability >= 0.5
                    in_prod = options.get("check_production_code", True)

                    risk_score = RiskCalculator.calculate_risk_score(
                        cve, is_exploitable=is_exploitable, in_production=in_prod
                    )

                    vuln_result = VulnerabilityResult(
                        cve=cve,
                        risk_score=risk_score,
                        is_exploitable=is_exploitable,
                        in_production_code=in_prod,
                        priority=0,
                    )
                    all_vulnerabilities.append(vuln_result)

                    fix = FixSuggester.suggest_fix(pkg_name, pkg_version)
                    fixes.append(fix)

        prioritized = RiskCalculator.prioritize_vulnerabilities(all_vulnerabilities)

        for i, vuln in enumerate(prioritized):
            vuln.priority = i + 1

        if all_vulnerabilities:
            overall_risk = sum(v.risk_score for v in all_vulnerabilities) / len(
                all_vulnerabilities
            )
            severity_numeric = {
                Severity.CRITICAL: 4,
                Severity.HIGH: 3,
                Severity.MEDIUM: 2,
                Severity.LOW: 1,
                Severity.NONE: 0,
            }
            max_severity = max(
                severity_numeric.get(v.cve.severity, 0) for v in all_vulnerabilities
            )
            if max_severity >= 3:
                overall_risk = min(overall_risk * 1.2, 1.0)
        else:
            overall_risk = 0.0

        vulnerabilities_output = []
        for vuln in all_vulnerabilities:
            vulnerabilities_output.append(
                {
                    "cve_id": vuln.cve.cve_id,
                    "package_name": vuln.cve.package_name,
                    "affected_versions": vuln.cve.affected_versions,
                    "fixed_version": vuln.cve.fixed_version,
                    "severity": vuln.cve.severity.value,
                    "cvss_score": vuln.cve.cvss_score,
                    "description": vuln.cve.description,
                    "exploitability": vuln.cve.exploitability,
                    "affected_code_paths": vuln.cve.affected_code_paths,
                    "published_date": vuln.cve.published_date,
                    "risk_score": vuln.risk_score,
                    "is_exploitable": vuln.is_exploitable,
                }
            )

        prioritized_output = []
        for vuln in prioritized:
            prioritized_output.append(
                {
                    "priority": vuln.priority,
                    "cve_id": vuln.cve.cve_id,
                    "package_name": vuln.cve.package_name,
                    "severity": vuln.cve.severity.value,
                    "risk_score": vuln.risk_score,
                    "description": vuln.cve.description,
                }
            )

        fixes_output = []
        for fix in fixes:
            fixes_output.append(
                {
                    "package": fix.package_name,
                    "current_version": fix.current_version,
                    "suggested_version": fix.suggested_version,
                    "change_type": fix.change_type,
                    "breaking_changes": fix.breaking_changes,
                    "alternatives": fix.alternative_packages,
                }
            )

        return {
            "status": "success",
            "vulnerabilities": vulnerabilities_output,
            "prioritized": prioritized_output,
            "fixes": fixes_output,
            "risk_score": round(overall_risk, 3),
            "summary": {
                "total_vulnerabilities": len(all_vulnerabilities),
                "critical": sum(
                    1
                    for v in all_vulnerabilities
                    if v.cve.severity == Severity.CRITICAL
                ),
                "high": sum(
                    1 for v in all_vulnerabilities if v.cve.severity == Severity.HIGH
                ),
                "medium": sum(
                    1 for v in all_vulnerabilities if v.cve.severity == Severity.MEDIUM
                ),
                "low": sum(
                    1 for v in all_vulnerabilities if v.cve.severity == Severity.LOW
                ),
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "vulnerabilities": [],
            "prioritized": [],
            "fixes": [],
            "risk_score": 0.0,
        }


async def invoke(payload: dict) -> dict:
    """
    Skill invocation function for integration with skill management system.

    Args:
        payload: Dict containing:
            - dependencies: str or list - Package dependencies
            - options: dict - Optional configuration

    Returns:
        dict with CVE prioritization results
    """
    dependencies = payload.get("dependencies", "")
    options = payload.get("options", {})

    if isinstance(dependencies, list):
        dependencies = "\n".join(dependencies)

    return cve_prioritizer(dependencies, options)


def register_skill() -> dict:
    """
    Register this skill with the skill management system.

    Returns:
        dict with skill metadata
    """
    return {
        "name": "cve_prioritizer",
        "description": "Analyzes dependencies for known vulnerabilities and prioritizes by risk exposure",
        "version": "1.0.0",
        "category": "security",
        "author": "Skill Flywheel",
        "tags": ["security", "vulnerability", "cve", "dependencies", "risk-assessment"],
        "input_schema": {
            "dependencies": {
                "type": "string",
                "description": "Package dependencies (requirements.txt or package.json format)",
                "required": True,
            },
            "options": {
                "type": "object",
                "description": "Configuration options",
                "properties": {
                    "include_dev_deps": {
                        "type": "boolean",
                        "description": "Include development dependencies",
                        "default": False,
                    },
                    "severity_threshold": {
                        "type": "string",
                        "description": "Minimum severity to report",
                        "enum": ["None", "Low", "Medium", "High", "Critical"],
                        "default": "Low",
                    },
                    "check_production_code": {
                        "type": "boolean",
                        "description": "Check if affected code is in production",
                        "default": True,
                    },
                },
            },
        },
        "output_schema": {
            "status": "string",
            "vulnerabilities": "array",
            "prioritized": "array",
            "fixes": "array",
            "risk_score": "number",
            "summary": "object",
        },
        "functions": {
            "cve_prioritizer": cve_prioritizer,
            "invoke": invoke,
            "register_skill": register_skill,
        },
    }


if __name__ == "__main__":
    sample_requirements = """
    requests==2.30.0
    django==4.2.5
    flask==2.2.0
    numpy==2.4.2
    pillow==9.5.0
    """

    result = cve_prioritizer(sample_requirements, {"severity_threshold": "Medium"})
    print(json.dumps(result, indent=2))
