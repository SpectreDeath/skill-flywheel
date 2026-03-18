import json
import re
import ast
from collections import defaultdict
from typing import Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class StyleRule:
    rule_id: str
    severity: str
    category: str
    pattern: str = ""
    fix_template: str = ""
    auto_fixable: bool = False


@dataclass
class Violation:
    rule_id: str
    message: str
    line: int
    column: int
    severity: str
    category: str
    fix: str = ""
    auto_fixable: bool = False


class StyleConfigParser:
    def __init__(self):
        self.rules = []

    def parse_pylintrc(self, config: str) -> list[StyleRule]:
        rules = []
        current_section = ""

        for line in config.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                if current_section == "MESSAGES":
                    rule_id = f"pylint-{key.lower()}"
                    rules.append(
                        StyleRule(
                            rule_id=rule_id,
                            severity=self._map_pylint_severity(value),
                            category="message",
                            auto_fixable=False,
                        )
                    )
                elif current_section == "FORMAT":
                    if key == "max-line-length":
                        rules.append(
                            StyleRule(
                                rule_id="max-line-length",
                                severity="warning",
                                category="format",
                                auto_fixable=False,
                            )
                        )

        return rules

    def parse_eslintrc(self, config: str) -> list[StyleRule]:
        rules = []

        try:
            config_data = json.loads(config)
        except json.JSONDecodeError:
            return rules

        eslint_rules = config_data.get("rules", {})

        rule_mapping = {
            "semi": ["semicolon", True, "{%s}"],
            "quotes": ["quotes", True, "'%s'"],
            "indent": ["indent", False, "%s"],
            "comma-dangle": ["comma-dangle", True, "%s"],
            "no-unused-vars": ["no-unused-vars", False, ""],
            "no-trailing-spaces": ["no-trailing-spaces", True, ""],
            "eqeqeq": ["eqeqeq", True, ""],
            "max-len": ["max-len", False, ""],
        }

        for rule_name, (display_name, is_fixable, template) in rule_mapping.items():
            if rule_name in eslint_rules:
                rule_config = eslint_rules[rule_name]
                severity = self._map_eslint_severity(rule_config)

                rules.append(
                    StyleRule(
                        rule_id=f"eslint-{rule_name}",
                        severity=severity,
                        category="lint",
                        auto_fixable=is_fixable and severity in ["error", "warning"],
                        fix_template=template,
                    )
                )

        return rules

    def parse_json_config(self, config: str) -> list[StyleRule]:
        rules = []

        try:
            config_data = json.loads(config)
        except json.JSONDecodeError:
            return rules

        if "rules" in config_data:
            for rule_name, rule_config in config_data["rules"].items():
                severity = self._map_eslint_severity(rule_config)
                rules.append(
                    StyleRule(
                        rule_id=rule_name,
                        severity=severity,
                        category="lint",
                        auto_fixable=severity in ["error", "warning"],
                    )
                )

        return rules

    def detect_and_parse(self, config: str) -> list[StyleRule]:
        config = config.strip()

        if config.startswith("{"):
            return self.parse_json_config(config)

        if "[MASTER]" in config or "[MESSAGES]" in config or "[REPORTS]" in config:
            return self.parse_pylintrc(config)

        if "eslint" in config.lower() or '"rules"' in config:
            return self.parse_eslintrc(config)

        return self.parse_json_config(config)

    def _map_pylint_severity(self, value: str) -> str:
        value = value.upper()
        if "E" in value or "ERROR" in value:
            return "error"
        elif "W" in value or "WARNING" in value:
            return "warning"
        return "info"

    def _map_eslint_severity(self, rule_config: Any) -> str:
        if isinstance(rule_config, int):
            if rule_config == 2 or rule_config == "error":
                return "error"
            elif rule_config == 1 or rule_config == "warn":
                return "warning"
            return "info"
        if isinstance(rule_config, list):
            return self._map_eslint_severity(rule_config[0])
        return "info"


class StyleViolationDetector:
    def __init__(self, rules: list[StyleRule]):
        self.rules = rules
        self.violations = []

    def detect(self, code: str, language: str = "python") -> list[Violation]:
        self.violations = []

        if language in ["python", "py"]:
            self._detect_python_violations(code)
        elif language in ["javascript", "js", "typescript", "ts"]:
            self._detect_js_violations(code)
        else:
            self._detect_generic_violations(code)

        return self.violations

    def _detect_python_violations(self, code: str):
        max_line_length = 120
        for rule in self.rules:
            if rule.rule_id == "max-line-length":
                try:
                    max_line_length = int(rule.pattern) if rule.pattern else 120
                except ValueError:
                    pass

        lines = code.split("\n")

        for rule in self.rules:
            if rule.rule_id == "max-line-length":
                for i, line in enumerate(lines, 1):
                    if len(line) > max_line_length:
                        self.violations.append(
                            Violation(
                                rule_id=rule.rule_id,
                                message=f"Line too long ({len(line)} > {max_line_length})",
                                line=i,
                                column=len(line),
                                severity=rule.severity,
                                category=rule.category,
                                auto_fixable=False,
                            )
                        )

        for i, line in enumerate(lines, 1):
            stripped = line.rstrip()
            if line != stripped:
                self.violations.append(
                    Violation(
                        rule_id="trailing-whitespace",
                        message="Trailing whitespace",
                        line=i,
                        column=len(stripped) + 1,
                        severity="warning",
                        category="format",
                        fix=stripped,
                        auto_fixable=True,
                    )
                )

        if len(lines) > 1 and lines[-1].strip() == "":
            self.violations.append(
                Violation(
                    rule_id="final-newline",
                    message="No final newline",
                    line=len(lines),
                    column=1,
                    severity="info",
                    category="format",
                    fix=code + "\n" if not code.endswith("\n") else code,
                    auto_fixable=True,
                )
            )

        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.name.islower() and not node.name.startswith("_"):
                        self.violations.append(
                            Violation(
                                rule_id="function-naming",
                                message=f"Function '{node.name}' should be lowercase",
                                line=node.lineno,
                                column=node.col_offset + 1,
                                severity="warning",
                                category="naming",
                                auto_fixable=False,
                            )
                        )
                if isinstance(node, ast.ClassDef):
                    if not node.name[0].isupper():
                        self.violations.append(
                            Violation(
                                rule_id="class-naming",
                                message=f"Class '{node.name}' should use CapWords",
                                line=node.lineno,
                                column=node.col_offset + 1,
                                severity="warning",
                                category="naming",
                                auto_fixable=False,
                            )
                        )
        except SyntaxError:
            pass

        for i, line in enumerate(lines, 1):
            if re.search(r"\t", line):
                self.violations.append(
                    Violation(
                        rule_id="no-tabs",
                        message="Tab found, use spaces instead",
                        line=i,
                        column=line.find("\t") + 1,
                        severity="warning",
                        category="format",
                        fix=line.replace("\t", "    "),
                        auto_fixable=True,
                    )
                )

    def _detect_js_violations(self, code: str):
        lines = code.split("\n")

        for i, line in enumerate(lines, 1):
            stripped = line.rstrip()
            if line != stripped:
                self.violations.append(
                    Violation(
                        rule_id="no-trailing-spaces",
                        message="Trailing spaces",
                        line=i,
                        column=len(stripped) + 1,
                        severity="warning",
                        category="format",
                        fix=stripped,
                        auto_fixable=True,
                    )
                )

            if "console.log" in line:
                self.violations.append(
                    Violation(
                        rule_id="no-console",
                        message="Unexpected console statement",
                        line=i,
                        column=line.find("console.log") + 1,
                        severity="warning",
                        category="best-practice",
                        auto_fixable=False,
                    )
                )

            if re.search(r"var\s+\w+", line):
                self.violations.append(
                    Violation(
                        rule_id="no-var",
                        message="Use 'let' or 'const' instead of 'var'",
                        line=i,
                        column=re.search(r"var\s+", line).start() + 1,
                        severity="warning",
                        category="es6",
                        fix=re.sub(r"\bvar\b", "let", line),
                        auto_fixable=True,
                    )
                )

            if re.search(r"==(?!=)", line):
                self.violations.append(
                    Violation(
                        rule_id="eqeqeq",
                        message="Use '===' instead of '=='",
                        line=i,
                        column=re.search(r"==", line).start() + 1,
                        severity="error",
                        category="best-practice",
                        auto_fixable=False,
                    )
                )

            if (
                not line.strip().endswith(";")
                and not line.strip().endswith("{")
                and not line.strip().endswith("}")
                and line.strip()
                and not line.strip().startswith("//")
                and not line.strip().startswith("/*")
            ):
                pass

    def _detect_generic_violations(self, code: str):
        lines = code.split("\n")

        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                self.violations.append(
                    Violation(
                        rule_id="max-line-length",
                        message=f"Line too long ({len(line)} > 120)",
                        line=i,
                        column=len(line),
                        severity="warning",
                        category="format",
                        auto_fixable=False,
                    )
                )

            if line.rstrip() != line:
                self.violations.append(
                    Violation(
                        rule_id="trailing-whitespace",
                        message="Trailing whitespace",
                        line=i,
                        column=len(line.rstrip()) + 1,
                        severity="info",
                        category="format",
                        fix=line.rstrip(),
                        auto_fixable=True,
                    )
                )


class StyleAutoFixer:
    def __init__(self, violations: list[Violation]):
        self.violations = violations
        self.fixed_lines = {}

    def apply_fixes(self, code: str) -> str:
        lines = code.split("\n")

        for violation in self.violations:
            if not violation.auto_fixable or not violation.fix:
                continue

            line_idx = violation.line - 1
            if 0 <= line_idx < len(lines):
                lines[line_idx] = violation.fix

        return "\n".join(lines)


class StyleEnforcer:
    def __init__(self):
        self.config_parser = StyleConfigParser()
        self.detector = None
        self.violations = []

    def enforce(self, code: str, config: str, options: dict) -> dict:
        try:
            rules = self.config_parser.detect_and_parse(config)

            if not rules:
                rules = self._get_default_rules()

            language = options.get("language", "python")
            self.detector = StyleViolationDetector(rules)
            self.violations = self.detector.detect(code, language)

            fixable = [v for v in self.violations if v.auto_fixable]
            fixed_code = code

            if options.get("auto_fix", False) and fixable:
                fixer = StyleAutoFixer(fixable)
                fixed_code = fixer.apply_fixes(code)

            threshold = options.get("threshold", "warning")
            threshold_order = ["info", "warning", "error"]

            if threshold in threshold_order:
                min_level = threshold_order.index(threshold)
                filtered = [
                    v
                    for v in self.violations
                    if threshold_order.index(v.severity) >= min_level
                ]
            else:
                filtered = self.violations

            violations_data = []
            for v in filtered:
                violations_data.append(
                    {
                        "rule_id": v.rule_id,
                        "message": v.message,
                        "line": v.line,
                        "column": v.column,
                        "severity": v.severity,
                        "category": v.category,
                        "auto_fixable": v.auto_fixable,
                    }
                )

            fixable_data = []
            for v in fixable:
                fixable_data.append(
                    {
                        "rule_id": v.rule_id,
                        "message": v.message,
                        "line": v.line,
                        "fix": v.fix,
                    }
                )

            return {
                "status": "success",
                "violations": violations_data,
                "fixable": fixable_data,
                "fixed_code": fixed_code if options.get("auto_fix", False) else "",
                "summary": self._generate_summary(filtered, fixable, rules),
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "violations": [],
                "fixable": [],
                "fixed_code": "",
                "summary": {},
            }

    def _get_default_rules(self) -> list[StyleRule]:
        return [
            StyleRule(rule_id="max-line-length", severity="warning", category="format"),
            StyleRule(
                rule_id="trailing-whitespace",
                severity="info",
                category="format",
                auto_fixable=True,
            ),
            StyleRule(
                rule_id="no-tabs",
                severity="warning",
                category="format",
                auto_fixable=True,
            ),
            StyleRule(
                rule_id="final-newline",
                severity="info",
                category="format",
                auto_fixable=True,
            ),
        ]

    def _generate_summary(
        self,
        violations: list[Violation],
        fixable: list[Violation],
        rules: list[StyleRule],
    ) -> dict:
        by_severity = defaultdict(int)
        by_category = defaultdict(int)

        for v in violations:
            by_severity[v.severity] += 1
            by_category[v.category] += 1

        return {
            "total_violations": len(violations),
            "fixable_count": len(fixable),
            "by_severity": dict(by_severity),
            "by_category": dict(by_category),
            "rules_configured": len(rules),
            "timestamp": datetime.now().isoformat(),
        }


_enforcer_instance = StyleEnforcer()


def style_enforcer(code: str, config: str, options: dict = None) -> dict:
    options = options or {}
    return _enforcer_instance.enforce(code, config, options)


def invoke(payload: dict) -> dict:
    code = payload.get("code", "")
    config = payload.get("config", "")
    options = payload.get("options", {})

    return style_enforcer(code, config, options)


def register_skill() -> dict:
    return {
        "name": "style_enforcer",
        "description": "Enforces project style conventions by parsing config files, detecting violations, categorizing issues, auto-fixing where possible, and reporting summaries",
        "version": "1.0.0",
        "functions": {
            "style_enforcer": {
                "description": "Main function to enforce style conventions on code",
                "parameters": {
                    "code": "Code to check for style violations",
                    "config": "Style configuration (.pylintrc, .eslintrc, etc.)",
                    "options": "Optional settings (auto_fix, threshold, language)",
                },
            },
            "invoke": {
                "description": "Skill invocation entry point",
                "parameters": {"payload": "Dict with code, config, and options"},
            },
            "register_skill": {
                "description": "Returns skill metadata for registration"
            },
        },
        "capabilities": [
            "parse_style_config",
            "detect_violations",
            "categorize_violations",
            "auto_fix_issues",
            "generate_summary",
        ],
        "supported_languages": ["python", "javascript", "typescript", "generic"],
        "supported_config_formats": [".pylintrc", ".eslintrc", "JSON"],
    }
