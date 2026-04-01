"""
Changelog Generator Skill

Generates changelogs from git log data:
- Parses git log commit messages and PR references
- Categorizes changes into features, fixes, breaking changes
- Detects semantic version tags
- Formats output in standard changelog format
"""

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

SEMVER_PATTERN = r"\bv?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?\b"

FEATURE_PREFIXES = [
    r"^feat(?:\([^\)]+\))?:",
    r"^add(?:\([^\)]+\))?:",
    r"^new(?:\([^\)]+\))?:",
    r"^feature:",
]

FIX_PREFIXES = [
    r"^fix(?:\([^\)]+\))?:",
    r"^bug(?:\([^\)]+\))?:",
    r"^hotfix:",
    r"^patch:",
    r"^repair:",
]

BREAKING_PATTERNS = [
    r"BREAKING[- ]CHANGE:",
    r"BREAKING[- ]CHANGES?:",
    r"^[^:]+!:.+",
]

PR_PATTERNS = [
    r"\(#(\d+)\)",
    r"PR\s*#?(\d+)",
    r"pull/(\d+)",
    r"github\.com/[^\/]+/[^\/]+/pull/(\d+)",
]


@dataclass
class Commit:
    hash: str
    message: str
    author: str | None = None
    date: str | None = None
    pr_number: str | None = None
    category: str = "other"
    is_breaking: bool = False
    scope: str | None = None
    raw: str = ""


@dataclass
class Version:
    tag: str
    major: int
    minor: int
    patch: int
    prerelease: str | None = None
    date: str | None = None
    commits: List[Commit] = field(default_factory=list)


def parse_git_log_line(line: str) -> Dict[str, str] | None:
    """Parse a single line from git log output."""
    patterns = [
        r"^([a-f0-9]{7,40})\s+(.+)$",
        r"^commit\s+([a-f0-9]{7,40})",
    ]

    for pattern in patterns:
        match = re.match(pattern, line, re.IGNORECASE)
        if match:
            return {"hash": match.group(1)[:7], "message": match.group(2).strip()}
    return None


def detect_pr_number(message: str) -> str | None:
    """Extract PR number from commit message."""
    for pattern in PR_PATTERNS:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def detect_scope(message: str) -> str | None:
    """Extract scope from commit message (e.g., feat(api): message)."""
    match = re.match(r"^\w+(?:\(([^)]+)\))?:", message)
    if match:
        return match.group(1)
    return None


def categorize_commit(message: str) -> tuple[str, bool]:
    """Categorize a commit and detect if it's breaking."""
    message_lower = message.lower().strip()
    is_breaking = any(re.search(p, message, re.IGNORECASE) for p in BREAKING_PATTERNS)

    for pattern in FEATURE_PREFIXES:
        if re.search(pattern, message, re.IGNORECASE):
            return "feature", is_breaking

    for pattern in FIX_PREFIXES:
        if re.search(pattern, message, re.IGNORECASE):
            return "fix", is_breaking

    if "docs" in message_lower and any(
        p in message_lower for p in ["readme", "doc", "documentation"]
    ):
        return "documentation", is_breaking

    if any(p in message_lower for p in ["refactor", "restructure", "reorganize"]):
        return "refactor", is_breaking

    if any(p in message_lower for p in ["test", "spec", "coverage"]):
        return "testing", is_breaking

    if any(p in message_lower for p in ["chore", "maintain", "update deps", "bump"]):
        return "chore", is_breaking

    if any(p in message_lower for p in ["perf", "optimize", "improve performance"]):
        return "performance", is_breaking

    if any(p in message_lower for p in ["ci", "cd", "pipeline", "workflow"]):
        return "ci", is_breaking

    return "other", is_breaking


def detect_versions(git_log: str) -> List[Version]:
    """Detect semantic version tags from git log."""
    versions = []
    version_pattern = r"(?:tag:\s*)?" + SEMVER_PATTERN

    for line in git_log.split("\n"):
        matches = re.findall(version_pattern, line)
        for match in matches:
            tag = f"v{match[0]}" if not line.startswith("v") else match[0]
            version = Version(
                tag=tag,
                major=int(match[0]),
                minor=int(match[1]),
                patch=int(match[2]),
                prerelease=match[3] if match[3] else None,
            )

            existing = next((v for v in versions if v.tag == version.tag), None)
            if not existing:
                versions.append(version)

    versions.sort(key=lambda v: (v.major, v.minor, v.patch), reverse=True)
    return versions


def parse_commits(git_log: str) -> List[Commit]:
    """Parse commits from git log output."""
    commits = []
    current_commit = None

    for line in git_log.split("\n"):
        line = line.strip()

        if not line:
            continue

        if line.startswith("Merge:"):
            continue

        if line.startswith("Author:") or line.startswith("Date:"):
            if current_commit:
                if line.startswith("Author:"):
                    current_commit.author = line.replace("Author:", "").strip()
                elif line.startswith("Date:"):
                    current_commit.date = line.replace("Date:", "").strip()
            continue

        hash_match = re.match(r"^([a-f0-9]{7,40})\s+(.+)$", line)
        if hash_match:
            if current_commit:
                commits.append(current_commit)

            commit_hash = hash_match.group(1)[:7]
            message = hash_match.group(2).strip()
            category, is_breaking = categorize_commit(message)

            current_commit = Commit(
                hash=commit_hash,
                message=message,
                pr_number=detect_pr_number(message),
                category=category,
                is_breaking=is_breaking,
                scope=detect_scope(message),
                raw=line,
            )
            continue

        if (
            current_commit
            and not line.startswith("Author:")
            and not line.startswith("Date:")
        ):
            current_commit.message += " " + line

    if current_commit:
        commits.append(current_commit)

    return commits


def categorize_changes(commits: List[Commit]) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize commits into groups."""
    changes = {
        "breaking": [],
        "features": [],
        "fixes": [],
        "documentation": [],
        "refactor": [],
        "testing": [],
        "chore": [],
        "performance": [],
        "ci": [],
        "other": [],
    }

    for commit in commits:
        change = {
            "hash": commit.hash,
            "message": commit.message,
            "scope": commit.scope,
            "pr": commit.pr_number,
            "author": commit.author,
        }

        if commit.is_breaking:
            changes["breaking"].append(change)
        elif commit.category == "feature":
            changes["features"].append(change)
        elif commit.category == "fix":
            changes["fixes"].append(change)
        elif commit.category in changes:
            changes[commit.category].append(change)
        else:
            changes["other"].append(change)

    return changes


def format_changelog_markdown(
    changes: Dict[str, List[Dict[str, Any]]], versions: List[Version], options: dict
) -> str:
    """Format changelog as Markdown."""
    options.get(
        "include_sections", ["breaking", "features", "fixes", "breaking"]
    )
    show_pr = options.get("show_pr", True)
    show_author = options.get("show_author", False)
    include_date = options.get("include_date", True)

    output = []
    output.append("# Changelog")
    output.append("")

    current_date = datetime.now().strftime("%Y-%m-%d")

    if versions:
        for version in versions:
            output.append(
                f"## [{version.tag}] - {current_date if include_date else 'Unreleased'}"
            )
            output.append("")

            if changes["breaking"]:
                output.append("### Breaking Changes")
                output.append("")
                for change in changes["breaking"]:
                    msg = f"- {change['message']}"
                    if show_pr and change.get("pr"):
                        msg += f" (#{change['pr']})"
                    if show_author and change.get("author"):
                        msg += f" - {change['author']}"
                    output.append(msg)
                output.append("")

            if changes["features"]:
                output.append("### Features")
                output.append("")
                for change in changes["features"]:
                    msg = f"- {change['message']}"
                    if show_pr and change.get("pr"):
                        msg += f" (#{change['pr']})"
                    if show_author and change.get("author"):
                        msg += f" - {change['author']}"
                    output.append(msg)
                output.append("")

            if changes["fixes"]:
                output.append("### Bug Fixes")
                output.append("")
                for change in changes["fixes"]:
                    msg = f"- {change['message']}"
                    if show_pr and change.get("pr"):
                        msg += f" (#{change['pr']})"
                    if show_author and change.get("author"):
                        msg += f" - {change['author']}"
                    output.append(msg)
                output.append("")

            for section in [
                "documentation",
                "refactor",
                "testing",
                "chore",
                "performance",
                "ci",
                "other",
            ]:
                if section in changes and changes[section]:
                    section_title = section.capitalize()
                    output.append(f"### {section_title}")
                    output.append("")
                    for change in changes[section]:
                        msg = f"- {change['message']}"
                        if show_pr and change.get("pr"):
                            msg += f" (#{change['pr']})"
                        if show_author and change.get("author"):
                            msg += f" - {change['author']}"
                        output.append(msg)
                    output.append("")
    else:
        output.append("## Unreleased")
        output.append("")

        for category in [
            "breaking",
            "features",
            "fixes",
            "documentation",
            "refactor",
            "testing",
            "chore",
            "performance",
            "ci",
            "other",
        ]:
            if changes.get(category):
                section_title = {
                    "breaking": "Breaking Changes",
                    "features": "Features",
                    "fixes": "Bug Fixes",
                    "documentation": "Documentation",
                    "refactor": "Refactoring",
                    "testing": "Testing",
                    "chore": "Maintenance",
                    "performance": "Performance",
                    "ci": "CI/CD",
                    "other": "Other",
                }.get(category, category.capitalize())

                output.append(f"### {section_title}")
                output.append("")
                for change in changes[category]:
                    msg = f"- {change['message']}"
                    if show_pr and change.get("pr"):
                        msg += f" (#{change['pr']})"
                    if show_author and change.get("author"):
                        msg += f" - {change['author']}"
                    output.append(msg)
                output.append("")

    return "\n".join(output)


def format_changelog_json(
    changes: Dict[str, List[Dict[str, Any]]], versions: List[Version], options: dict
) -> str:
    """Format changelog as JSON."""
    data = {
        "generated": datetime.now().isoformat(),
        "versions": [
            {
                "tag": v.tag,
                "major": v.major,
                "minor": v.minor,
                "patch": v.patch,
                "prerelease": v.prerelease,
            }
            for v in versions
        ],
        "changes": changes,
    }
    return json.dumps(data, indent=2)


def format_changelog_keep_a_changelog(
    changes: Dict[str, List[Dict[str, Any]]], versions: List[Version], options: dict
) -> str:
    """Format changelog using Keep a Changelog format."""
    show_pr = options.get("show_pr", True)
    options.get("show_author", False)

    output = []
    output.append("# Changelog")
    output.append("")
    output.append(
        "All notable changes to this project will be documented in this file."
    )
    output.append("")
    output.append(
        "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),"
    )
    output.append(
        "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)."
    )
    output.append("")

    current_date = datetime.now().strftime("%Y-%m-%d")
    version_label = versions[0].tag if versions else "Unreleased"

    output.append(f"## [{version_label}] - {current_date}")
    output.append("")

    if changes["breaking"]:
        output.append("### ⚠️ Breaking Changes")
        output.append("")
        for change in changes["breaking"]:
            msg = f"- {change['message']}"
            if show_pr and change.get("pr"):
                msg += f" (#[{change['pr']}](https://github.com/org/repo/pull/{change['pr']}))"
            output.append(msg)
        output.append("")

    if changes["features"]:
        output.append("### ✨ Features")
        output.append("")
        for change in changes["features"]:
            msg = f"- {change['message']}"
            if show_pr and change.get("pr"):
                msg += f" (#[{change['pr']}](https://github.com/org/repo/pull/{change['pr']}))"
            output.append(msg)
        output.append("")

    if changes["fixes"]:
        output.append("### 🐛 Bug Fixes")
        output.append("")
        for change in changes["fixes"]:
            msg = f"- {change['message']}"
            if show_pr and change.get("pr"):
                msg += f" (#[{change['pr']}](https://github.com/org/repo/pull/{change['pr']}))"
            output.append(msg)
        output.append("")

    for section, title in [
        ("documentation", "### 📚 Documentation"),
        ("refactor", "### 🔧 Refactoring"),
        ("performance", "### ⚡ Performance"),
        ("testing", "### 🧪 Testing"),
        ("chore", "### 🔨 Maintenance"),
    ]:
        if changes[section]:
            output.append(title)
            output.append("")
            for change in changes[section]:
                msg = f"- {change['message']}"
                if show_pr and change.get("pr"):
                    msg += f" (#[{change['pr']}](https://github.com/org/repo/pull/{change['pr']}))"
                output.append(msg)
            output.append("")

    return "\n".join(output)


def changelog_generator(git_log: str, options: dict) -> dict:
    """
    Generate a changelog from git log data.

    Args:
        git_log: Git log output string
        options: Dictionary with options:
            - format: Output format ("markdown", "json", "keep-a-changelog")
            - detect_versions: Whether to detect version tags (default: True)
            - include_sections: List of sections to include
            - show_pr: Show PR numbers (default: True)
            - show_author: Show author (default: False)
            - include_date: Include date in version headers (default: True)

    Returns:
        Dictionary with:
            - status: "success" or "error"
            - versions: List of detected versions
            - changes: Categorized changes
            - changelog: Generated changelog content
    """
    try:
        if not git_log or not git_log.strip():
            return {"status": "error", "message": "Empty git log provided"}

        detect_versions_enabled = options.get("detect_versions", True)
        output_format = options.get("format", "markdown")

        versions = detect_versions(git_log) if detect_versions_enabled else []

        commits = parse_commits(git_log)

        if not commits:
            return {"status": "error", "message": "No commits found in git log"}

        changes = categorize_changes(commits)

        if output_format == "json":
            changelog = format_changelog_json(changes, versions, options)
        elif output_format == "keep-a-changelog":
            changelog = format_changelog_keep_a_changelog(changes, versions, options)
        else:
            changelog = format_changelog_markdown(changes, versions, options)

        return {
            "status": "success",
            "versions": [
                {
                    "tag": v.tag,
                    "major": v.major,
                    "minor": v.minor,
                    "patch": v.patch,
                    "prerelease": v.prerelease,
                }
                for v in versions
            ],
            "changes": changes,
            "changelog": changelog,
            "format": output_format,
            "commit_count": len(commits),
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


async def invoke(payload: dict) -> dict:
    """MCP skill invocation."""
    git_log = payload.get("git_log", "")
    options = payload.get("options", {})

    if not git_log:
        return {"status": "error", "message": "No git_log provided"}

    result = changelog_generator(git_log, options)
    return result


def register_skill():
    """Return skill metadata."""
    return {
        "name": "changelog-generator",
        "description": "Generate changelogs from git log data with semantic versioning support",
        "version": "1.0.0",
        "domain": "DOCUMENTATION",
        "capabilities": [
            "parse_git_log",
            "detect_pr_numbers",
            "detect_semver_tags",
            "categorize_changes",
            "format_markdown",
            "format_json",
            "format_keep_a_changelog",
        ],
        "options": {
            "format": {
                "type": "string",
                "enum": ["markdown", "json", "keep-a-changelog"],
                "default": "markdown",
            },
            "detect_versions": {"type": "boolean", "default": True},
            "show_pr": {"type": "boolean", "default": True},
            "show_author": {"type": "boolean", "default": False},
            "include_date": {"type": "boolean", "default": True},
        },
    }
