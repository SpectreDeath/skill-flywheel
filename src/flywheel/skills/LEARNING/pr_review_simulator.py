import re
from collections import defaultdict
from datetime import datetime


class PRReviewSimulator:
    def __init__(self):
        self.diff = ""
        self.issues = []
        self.comments = []
        self.categories = {
            "must_fix": [],
            "should_fix": [],
            "nitpick": [],
            "security": [],
            "style": [],
            "performance": [],
            "bug": [],
        }
        self.score = 0

    def analyze_diff(self, diff: str) -> dict:
        self.diff = diff
        parsed_changes = {
            "files": [],
            "additions": 0,
            "deletions": 0,
            "total_lines": 0,
        }

        if not diff or not isinstance(diff, str):
            return parsed_changes

        file_blocks = re.split(r"diff --git", diff)

        for block in file_blocks:
            if not block.strip():
                continue

            file_info = self._parse_file_block(block)
            if file_info:
                parsed_changes["files"].append(file_info)
                parsed_changes["additions"] += file_info.get("additions", 0)
                parsed_changes["deletions"] += file_info.get("deletions", 0)

        parsed_changes["total_lines"] = (
            parsed_changes["additions"] + parsed_changes["deletions"]
        )
        return parsed_changes

    def _parse_file_block(self, block: str) -> dict:
        file_match = re.search(r"a/(.+?)\s+b/(.+)", block)
        if not file_match:
            return None

        file_path = file_match.group(2)

        additions = len(re.findall(r"^\+[^+]", block, re.MULTILINE))
        deletions = len(re.findall(r"^-[^-]", block, re.MULTILINE))

        hunks = []
        hunk_matches = re.finditer(r"@@\s*-(\d+),?(\d*)\s*\+(\d+),?(\d*)", block)
        for match in hunk_matches:
            hunks.append(
                {
                    "old_start": int(match.group(1)),
                    "old_lines": int(match.group(2)) if match.group(2) else 1,
                    "new_start": int(match.group(3)),
                    "new_lines": int(match.group(4)) if match.group(4) else 1,
                }
            )

        return {
            "path": file_path,
            "additions": additions,
            "deletions": deletions,
            "hunks": hunks,
            "raw": block[:500],
        }

    def identify_issues(self, diff: str, style: str = "relaxed") -> list[dict]:
        self.issues = []

        file_blocks = re.split(r"diff --git", diff)

        for block in file_blocks:
            if not block.strip():
                continue

            file_issues = self._scan_file_for_issues(block, style)
            self.issues.extend(file_issues)

        return self.issues

    def _scan_file_for_issues(self, block: str, style: str) -> list[dict]:
        issues = []

        file_match = re.search(r"b/(.+)", block)
        file_path = file_match.group(1) if file_match else "unknown"

        lines = block.split("\n")

        for i, line in enumerate(lines):
            if not line.startswith("+") or line.startswith("+++"):
                continue

            content = line[1:]

            security_issue = self._check_security_issues(content, file_path, i)
            if security_issue:
                issues.append(security_issue)

            bug_issue = self._check_potential_bugs(content, file_path, i)
            if bug_issue:
                issues.append(bug_issue)

            performance_issue = self._check_performance(content, file_path, i)
            if performance_issue:
                issues.append(performance_issue)

            if style == "strict":
                style_issue = self._check_style(content, file_path, i)
                if style_issue:
                    issues.append(style_issue)

        return issues

    def _check_security_issues(
        self, content: str, file_path: str, line_num: int
    ) -> dict | None:
        dangerous_patterns = [
            (r"eval\s*\(", "Use of eval() is dangerous - potential code injection"),
            (r"exec\s*\(", "Use of exec() is dangerous - potential code injection"),
            (r"password\s*=\s*['\"][^'\"]+['\"]", "Hardcoded password detected"),
            (r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]", "Hardcoded API key detected"),
            (r"secret\s*=\s*['\"][^'\"]+['\"]", "Hardcoded secret detected"),
            (r"os\.system\s*\(", "os.system() call - shell injection risk"),
            (r"subprocess\.call\s*\(\s*\[", "Potential command injection"),
            (r"SELECT.*FROM.*WHERE.*=", "SQL query without parameterization"),
            (r"\.innerHTML\s*=", "Potential XSS - use textContent instead"),
        ]

        for pattern, message in dangerous_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return {
                    "type": "security",
                    "severity": "must_fix",
                    "file": file_path,
                    "line": line_num,
                    "message": message,
                    "code": content[:80],
                }
        return None

    def _check_potential_bugs(
        self, content: str, file_path: str, line_num: int
    ) -> dict | None:
        bug_patterns = [
            (r"==\s*None", "Use 'is None' for None comparisons"),
            (r"!=\s*None", "Use 'is not None' for None comparisons"),
            (
                r"\.get\s*\(\s*['\"][^'\"]*['\"]\s*,\s*None\)",
                "Unnecessary default None in dict.get()",
            ),
            (r"if\s+True:", "Always-true condition detected"),
            (r"if\s+False:", "Always-false condition detected"),
            (r"try:.*except:\s*pass", "Empty except clause - silently swallows errors"),
            (
                r"for\s+.*\s+in\s+range\s*\(\s*len\s*\(",
                "Use enumerate() instead of range(len())",
            ),
            (r"print\s*\(\s*\)", "Empty print statement"),
        ]

        for pattern, message in bug_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return {
                    "type": "bug",
                    "severity": "should_fix",
                    "file": file_path,
                    "line": line_num,
                    "message": message,
                    "code": content[:80],
                }
        return None

    def _check_performance(
        self, content: str, file_path: str, line_num: int
    ) -> dict | None:
        perf_patterns = [
            (
                r"for\s+.*\s+in\s+.*:\s*.*\.append\s*\(",
                "Consider list comprehension for better performance",
            ),
            (r"\+\s*\[\]", "Use list() or list comprehension instead of + []"),
            (r"\.join\s*\(\s*list\s*\(", "Unnecessary list() conversion in join"),
        ]

        for pattern, message in perf_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return {
                    "type": "performance",
                    "severity": "should_fix",
                    "file": file_path,
                    "line": line_num,
                    "message": message,
                    "code": content[:80],
                }
        return None

    def _check_style(self, content: str, file_path: str, line_num: int) -> dict | None:
        style_issues = []

        if len(content) > 120:
            style_issues.append(f"Line too long ({len(content)} > 120 characters)")

        if content.rstrip() != content:
            style_issues.append("Trailing whitespace")

        if re.match(r"^\s{4,}", content):
            style_issues.append("Inconsistent indentation - avoid deep nesting")

        if len(content.strip()) > 0 and content.strip()[-1] == ";":
            style_issues.append("Unnecessary semicolon")

        if re.match(r"^[A-Z_][A-Z0-9_]*\s*=", content) and not content.startswith("#"):
            pass
        elif re.match(r"^[a-z][a-zA-Z0-9_]*\s*\(", content):
            if not re.match(r"^[a-z][a-zA-Z0-9_]*\s*\(\s*(self|cls)?", content):
                if not any(
                    kw in content
                    for kw in ["def ", "class ", "if ", "for ", "while ", "return "]
                ) and not re.match(r"^[a-z][a-zA-Z0-9_]*\s*\(\s*\)", content):
                    pass

        if style_issues:
            return {
                "type": "style",
                "severity": "nitpick",
                "file": file_path,
                "line": line_num,
                "message": "; ".join(style_issues),
                "code": content[:80],
            }
        return None

    def categorize_issues(self, issues: list[dict] = None) -> dict:
        if issues is None:
            issues = self.issues

        categories = {
            "must_fix": [],
            "should_fix": [],
            "nitpick": [],
            "security": [],
            "style": [],
            "performance": [],
            "bug": [],
        }

        for issue in issues:
            severity = issue.get("severity", "nitpick")
            issue_type = issue.get("type", "style")

            if severity == "must_fix":
                categories["must_fix"].append(issue)
            elif severity == "should_fix":
                categories["should_fix"].append(issue)

            if issue_type in categories:
                categories[issue_type].append(issue)
            else:
                categories["nitpick"].append(issue)

        self.categories = categories
        return categories

    def generate_comments(self, style: str = "relaxed") -> list[dict]:
        self.comments = []

        for issue in self.issues:
            comment = self._format_comment(issue, style)
            self.comments.append(comment)

        return self.comments

    def _format_comment(self, issue: dict, style: str) -> dict:
        severity = issue.get("severity", "nitpick")
        issue_type = issue.get("type", "style")
        message = issue.get("message", "")
        file_path = issue.get("file", "")
        code = issue.get("code", "")

        prefixes = {
            "must_fix": "[MUST FIX]",
            "should_fix": "[SHOULD FIX]",
            "nitpick": "[NITPICK]",
        }

        severity_prefix = prefixes.get(severity, "[COMMENT]")

        if style == "strict":
            tone = "Please address this critical issue"
        else:
            tone = "Consider addressing this"

        if issue_type == "security":
            tone = (
                """Security issue - please address immediately"""
                if severity == "must_fix"
                else "Security consideration"
            )

        formatted = {
            "file": file_path,
            "line": issue.get("line", 0),
            "type": issue_type,
            "severity": severity,
            "body": f"{severity_prefix} {tone}: {message}",
            "code_snippet": code,
        }

        return formatted

    def calculate_score(self, diff: str = "", issues: list[dict] = None) -> int:
        if issues is None:
            issues = self.issues

        base_score = 100

        severity_penalties = {
            "must_fix": 15,
            "should_fix": 8,
            "nitpick": 2,
        }

        type_bonuses = {
            "security": 5,
            "bug": 3,
            "performance": 2,
        }

        total_penalty = 0
        issue_counts = defaultdict(int)

        for issue in issues:
            severity = issue.get("severity", "nitpick")
            issue_type = issue.get("type", "style")

            penalty = severity_penalties.get(severity, 2)
            total_penalty += penalty
            issue_counts[issue_type] += 1

        for issue_type, count in issue_counts.items():
            if issue_type in type_bonuses:
                total_penalty += type_bonuses[issue_type] * min(count, 3)

        if diff:
            additions = len(re.findall(r"^\+[^+]", diff, re.MULTILINE))
            deletions = len(re.findall(r"^-[^-]", diff, re.MULTILINE))
            total_changes = additions + deletions

            if total_changes > 500:
                total_penalty += 10
            elif total_changes > 1000:
                total_penalty += 20

        self.score = max(0, min(100, base_score - total_penalty))
        return self.score

    def generate_summary(self, style: str = "relaxed") -> dict:
        total_issues = len(self.issues)
        must_fix = len(self.categories.get("must_fix", []))
        should_fix = len(self.categories.get("should_fix", []))
        nitpick = len(self.categories.get("nitpick", []))

        if style == "strict":
            verdict = "Changes require revisions before merge"
        elif must_fix > 0:
            verdict = "Please address critical issues before merging"
        elif should_fix > 0:
            verdict = "Changes look good with minor improvements suggested"
        else:
            verdict = "LGTM! Ready to merge"

        return {
            "total_issues": total_issues,
            "must_fix_count": must_fix,
            "should_fix_count": should_fix,
            "nitpick_count": nitpick,
            "score": self.score,
            "verdict": verdict,
            "recommendation": "request_changes"
            if must_fix > 0
            else ("approve" if should_fix == 0 else "comment"),
        }


_reviewer_instance = PRReviewSimulator()


def pr_review_simulator(diff: str, options: dict = None) -> dict:
    options = options or {}
    style = options.get("style", "relaxed")

    try:
        if not diff:
            return {
                "status": "error",
                "error": "No diff provided",
                "comments": [],
                "categories": {},
                "score": 0,
                "summary": {},
            }

        parsed_changes = _reviewer_instance.analyze_diff(diff)

        issues = _reviewer_instance.identify_issues(diff, style)

        categories = _reviewer_instance.categorize_issues(issues)

        comments = _reviewer_instance.generate_comments(style)

        score = _reviewer_instance.calculate_score(diff, issues)

        summary = _reviewer_instance.generate_summary(style)

        return {
            "status": "success",
            "comments": comments,
            "categories": {
                "must_fix": categories.get("must_fix", []),
                "should_fix": categories.get("should_fix", []),
                "nitpick": categories.get("nitpick", []),
                "security": categories.get("security", []),
                "bug": categories.get("bug", []),
                "performance": categories.get("performance", []),
                "style": categories.get("style", []),
            },
            "score": score,
            "summary": summary,
            "analysis": {
                "files_changed": len(parsed_changes.get("files", [])),
                "additions": parsed_changes.get("additions", 0),
                "deletions": parsed_changes.get("deletions", 0),
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "comments": [],
            "categories": {},
            "score": 0,
            "summary": {},
        }


async def invoke(payload: dict) -> dict:
    diff = payload.get("diff", "")
    options = payload.get("options", {})

    return pr_review_simulator(diff, options)


def register_skill() -> dict:
    return {
        "name": "pr_review_simulator",
        "description": "Simulates code review by analyzing git diffs, identifying issues, and providing human-like feedback with quality scoring",
        "version": "1.0.0",
        "functions": {
            "pr_review_simulator": {
                "description": "Main function to simulate code review on a git diff",
                "parameters": {
                    "diff": "Git diff string to analyze",
                    "options": "Optional settings (style: strict|relaxed)",
                },
            },
            "invoke": {
                "description": "Skill invocation entry point",
                "parameters": {"payload": "Dict with diff and options"},
            },
            "register_skill": {
                "description": "Returns skill metadata for registration"
            },
        },
        "capabilities": [
            "analyze_diff",
            "identify_issues",
            "categorize_issues",
            "generate_comments",
            "calculate_score",
        ],
    }
