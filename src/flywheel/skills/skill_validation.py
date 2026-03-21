"""
Skill Validation Framework

This module provides validation for skill definitions and implementations:
- validate_skill_metadata: Validate skill metadata structure
- validate_skill_implementation: Validate skill can be loaded and executed
"""

import importlib.util
import json
import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ValidationResult:
    """Result of skill validation"""

    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)


REQUIRED_METADATA_FIELDS = ["name", "domain", "description"]
OPTIONAL_METADATA_FIELDS = ["version", "author", "complexity", "type", "category"]
VALID_DOMAINS = [
    "APPLICATION_SECURITY",
    "AI_AGENT_DEVELOPMENT",
    "ML_AI",
    "DATA_ENGINEERING",
    "CLOUD_ENGINEERING",
    "DEVOPS",
    "FRONTEND",
    "MOBILE_DEVELOPMENT",
    "WEB3",
    "GAME_DEV",
    "DATABASE_ENGINEERING",
    "SPECIFICATION_ENGINEERING",
    "ORCHESTRATION",
    "META_SKILL_DISCOVERY",
    "QUANTUM_COMPUTING",
]
VALID_COMPLEXITY = ["Basic", "Intermediate", "Advanced"]
VALID_TYPES = ["Process", "Tool", "Strategy", "Meta-Process", "Tutorial"]


def validate_metadata_structure(metadata: Dict[str, Any]) -> ValidationResult:
    """
    Validate skill metadata structure.

    Args:
        metadata: Skill metadata dictionary

    Returns:
        ValidationResult with errors, warnings, and info
    """
    result = ValidationResult(valid=True)

    # Check required fields
    for field in REQUIRED_METADATA_FIELDS:
        if field not in metadata or not metadata[field]:
            result.errors.append(f"Missing required field: {field}")
            result.valid = False

    # Validate domain
    if "domain" in metadata and metadata["domain"] not in VALID_DOMAINS:
        result.warnings.append(f"Non-standard domain: {metadata['domain']}")

    # Validate complexity
    if "complexity" in metadata and metadata["complexity"] not in VALID_COMPLEXITY:
        result.errors.append(f"Invalid complexity: {metadata['complexity']}")
        result.valid = False

    # Validate type
    if "type" in metadata and metadata["type"] not in VALID_TYPES:
        result.warnings.append(f"Non-standard type: {metadata['type']}")

    # Validate version format
    if "version" in metadata:
        version = metadata["version"]
        if not re.match(r"^\d+\.\d+\.\d+$", version):
            result.warnings.append(f"Non-standard version format: {version}")

    return result


def validate_skill_file(skill_path: str) -> ValidationResult:
    """
    Validate skill file exists and has required functions.

    Args:
        skill_path: Path to skill file

    Returns:
        ValidationResult
    """
    result = ValidationResult(valid=True)

    # Check file exists
    if not os.path.exists(skill_path):
        result.errors.append(f"Skill file not found: {skill_path}")
        result.valid = False
        return result

    # Check file is readable
    try:
        with open(skill_path, encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        result.errors.append(f"Cannot read skill file: {str(e)}")
        result.valid = False
        return result

    # Check for required functions
    if "def invoke(" not in content:
        result.warnings.append("Missing invoke() function")

    if "def register_skill(" not in content:
        result.warnings.append("Missing register_skill() function")

    return result


def validate_skill_implementation(skill_path: str) -> ValidationResult:
    """
    Validate skill can be loaded and executed.

    Args:
        skill_path: Path to skill file

    Returns:
        ValidationResult
    """
    result = ValidationResult(valid=True)

    # First validate file structure
    file_result = validate_skill_file(skill_path)
    result.errors.extend(file_result.errors)
    result.warnings.extend(file_result.warnings)

    if not file_result.valid:
        result.valid = False
        return result

    # Try to import the module
    try:
        spec = importlib.util.spec_from_file_location("skill_module", skill_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check for invoke function
            if not hasattr(module, "invoke"):
                result.warnings.append("Module missing invoke() function")
            else:
                result.info.append("invoke() function found")

            # Check for register_skill function
            if not hasattr(module, "register_skill"):
                result.warnings.append("Module missing register_skill() function")
            else:
                result.info.append("register_skill() function found")

                # Try to call register_skill
                try:
                    metadata = module.register_skill()
                    if not isinstance(metadata, dict):
                        result.errors.append(
                            "register_skill() must return a dictionary"
                        )
                        result.valid = False
                    else:
                        result.info.append("register_skill() returns valid metadata")
                except Exception as e:
                    result.errors.append(f"register_skill() failed: {str(e)}")
                    result.valid = False
    except Exception as e:
        result.errors.append(f"Failed to load module: {str(e)}")
        result.valid = False

    return result


def validate_skill_definition(skill_definition: Dict[str, Any]) -> ValidationResult:
    """
    Validate complete skill definition.

    Args:
        skill_definition: Complete skill definition

    Returns:
        ValidationResult
    """
    result = ValidationResult(valid=True)

    # Validate metadata
    metadata = skill_definition.get("metadata", {})
    if metadata:
        metadata_result = validate_metadata_structure(metadata)
        result.errors.extend([f"metadata.{e}" for e in metadata_result.errors])
        result.warnings.extend([f"metadata.{w}" for w in metadata_result.warnings])
        if not metadata_result.valid:
            result.valid = False

    # Validate input schema if present
    input_schema = skill_definition.get("input_schema")
    if input_schema and not isinstance(input_schema, dict):
        result.errors.append("input_schema must be a dictionary")
        result.valid = False

    # Validate output schema if present
    output_schema = skill_definition.get("output_schema")
    if output_schema and not isinstance(output_schema, dict):
        result.errors.append("output_schema must be a dictionary")
        result.valid = False

    return result


def validate_skill_catalog(catalog_path: str) -> Dict[str, ValidationResult]:
    """
    Validate all skills in a catalog.

    Args:
        catalog_path: Path to skill catalog (JSON)

    Returns:
        Dictionary mapping skill names to ValidationResults
    """
    results = {}

    if not os.path.exists(catalog_path):
        return {
            "_error": ValidationResult(
                valid=False, errors=[f"Catalog not found: {catalog_path}"]
            )
        }

    try:
        with open(catalog_path, encoding="utf-8") as f:
            catalog = json.load(f)
    except Exception as e:
        return {
            "_error": ValidationResult(
                valid=False, errors=[f"Failed to load catalog: {str(e)}"]
            )
        }

    skills = catalog.get("skills", [])

    for skill in skills:
        skill_name = skill.get("name", "unknown")

        # Validate metadata
        metadata = skill.get("metadata", {})
        results[skill_name] = validate_metadata_structure(metadata)

    return results


def generate_validation_report(results: Dict[str, ValidationResult]) -> str:
    """
    Generate a human-readable validation report.

    Args:
        results: Dictionary of validation results

    Returns:
        Formatted report string
    """
    lines = ["Skill Validation Report", "=" * 50, ""]

    total = len(results)
    valid = sum(1 for r in results.values() if r.valid)
    invalid = total - valid

    lines.append(f"Total Skills: {total}")
    lines.append(f"Valid: {valid}")
    lines.append(f"Invalid: {invalid}")
    lines.append("")

    if invalid > 0:
        lines.append("Issues Found:")
        lines.append("-" * 30)

        for name, result in results.items():
            if not result.valid:
                lines.append(f"\n{name}:")
                for error in result.errors:
                    lines.append(f"  ERROR: {error}")
                for warning in result.warnings:
                    lines.append(f"  WARNING: {warning}")

    return "\n".join(lines)


def invoke(payload: dict) -> dict:
    """Main entry point for MCP skill invocation"""
    action = payload.get("action", "validate")

    if action == "validate":
        skill_path = payload.get("skill_path", "")
        result = validate_skill_implementation(skill_path)
        return {
            "result": {
                "valid": result.valid,
                "errors": result.errors,
                "warnings": result.warnings,
                "info": result.info,
            }
        }
    elif action == "validate_catalog":
        catalog_path = payload.get("catalog_path", "")
        results = validate_skill_catalog(catalog_path)
        report = generate_validation_report(results)
        return {
            "result": {
                "results": {
                    k: {"valid": v.valid, "errors": v.errors}
                    for k, v in results.items()
                },
                "report": report,
            }
        }
    elif action == "validate_definition":
        definition = payload.get("skill_definition", {})
        result = validate_skill_definition(definition)
        return {
            "result": {
                "valid": result.valid,
                "errors": result.errors,
                "warnings": result.warnings,
            }
        }
    else:
        return {"result": {"status": "error", "message": f"Unknown action: {action}"}}


def register_skill():
    """Return skill metadata for MCP registration"""
    return {
        "name": "skill-validation",
        "description": "Framework for validating skill definitions and implementations",
        "version": "1.0.0",
        "domain": "META_SKILL_DISCOVERY",
    }
