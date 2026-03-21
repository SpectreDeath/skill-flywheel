import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def calculate_evolution_score(
    spec: Dict[str, Any], history: List[Dict[str, Any]]
) -> Dict[str, Any]:
    if not history:
        return {
            "evolution_score": 0,
            "stability_rating": "unknown",
            "maturity_level": 1,
            "recommendations": ["Add more version history for accurate analysis"],
        }

    version_count = len(history)
    breaking_count = sum(1 for h in history if h.get("breaking", False))
    bug_fixes = sum(1 for h in history if h.get("type") == "fix")

    evolution_score = min(100, version_count * 5 + bug_fixes * 2 - breaking_count * 10)
    evolution_score = max(0, evolution_score)

    if evolution_score >= 80:
        maturity = 5
        rating = "highly_mature"
    elif evolution_score >= 60:
        maturity = 4
        rating = "mature"
    elif evolution_score >= 40:
        maturity = 3
        rating = "developing"
    elif evolution_score >= 20:
        maturity = 2
        rating = "early"
    else:
        maturity = 1
        rating = "nascent"

    recommendations = []
    if breaking_count > 3:
        recommendations.append("Reduce breaking changes to improve stability")
    if version_count < 5:
        recommendations.append("Add more incremental versions")
    if evolution_score < 40:
        recommendations.append(
            "Focus on stability and bug fixes before adding features"
        )

    return {
        "evolution_score": evolution_score,
        "stability_rating": rating,
        "maturity_level": maturity,
        "version_count": version_count,
        "breaking_changes": breaking_count,
        "recommendations": recommendations,
    }


def suggest_evolution_path(
    current_spec: Dict[str, Any], target_spec: Dict[str, Any]
) -> Dict[str, Any]:
    current_version = current_spec.get("version", "1.0.0")
    target_version = target_spec.get("version", "2.0.0")

    current_parts = [int(x) for x in current_version.split(".")]
    target_parts = [int(x) for x in target_version.split(".")]

    major_changes = target_parts[0] - current_parts[0]
    minor_changes = (
        target_parts[1] - current_parts[1] if major_changes == 0 else target_parts[1]
    )
    patch_changes = (
        target_parts[2] - current_parts[2]
        if major_changes == 0 and minor_changes == 0
        else target_parts[2]
    )

    migration_steps = []

    if major_changes > 0:
        migration_steps.append(
            {
                "phase": "major_migration",
                "description": "Major version upgrade - breaking changes expected",
                "risk": "high",
                "steps": [
                    "Review breaking changes documentation",
                    "Update dependent systems",
                    "Migrate data formats",
                    "Update API contracts",
                    "Run comprehensive tests",
                ],
            }
        )

    if minor_changes > 0:
        migration_steps.append(
            {
                "phase": "feature_addition",
                "description": "New features and enhancements",
                "risk": "medium",
                "steps": [
                    "Review new feature specifications",
                    "Update documentation",
                    "Add new test cases",
                    "Deploy incrementally",
                ],
            }
        )

    if patch_changes > 0:
        migration_steps.append(
            {
                "phase": "patch_application",
                "description": "Bug fixes and optimizations",
                "risk": "low",
                "steps": [
                    "Review patch notes",
                    "Apply update",
                    "Verify existing functionality",
                ],
            }
        )

    if not migration_steps:
        migration_steps.append(
            {
                "phase": "no_change",
                "description": "Versions are already synchronized",
                "risk": "none",
                "steps": [],
            }
        )

    return {
        "current_version": current_version,
        "target_version": target_version,
        "migration_path": migration_steps,
        "estimated_complexity": "high"
        if major_changes > 0
        else "medium"
        if minor_changes > 0
        else "low",
    }


def validate_evolution_compliance(
    new_spec: Dict[str, Any], contracts: List[Dict[str, Any]]
) -> Dict[str, Any]:
    violations = []
    warnings = []

    new_fields = set(new_spec.get("fields", {}).keys())

    for contract in contracts:
        required_fields = set(contract.get("required_fields", []))
        deprecated_fields = set(contract.get("deprecated_fields", []))

        missing_required = required_fields - new_fields
        if missing_required:
            violations.append(
                {
                    "type": "missing_required_fields",
                    "fields": list(missing_required),
                    "contract": contract.get("name", "unknown"),
                }
            )

        used_deprecated = new_fields & deprecated_fields
        if used_deprecated:
            warnings.append(
                {
                    "type": "deprecated_fields_used",
                    "fields": list(used_deprecated),
                    "contract": contract.get("name", "unknown"),
                }
            )

    backward_compatible = len(violations) == 0

    return {
        "backward_compatible": backward_compatible,
        "violations": violations,
        "warnings": warnings,
        "compliance_score": 100 - len(violations) * 20 - len(warnings) * 5,
    }


def track_evolution_metrics(versions: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not versions:
        return {"metrics": {}, "summary": "No version history available"}

    metrics = {
        "total_versions": len(versions),
        "versions_by_type": {"major": 0, "minor": 0, "patch": 0},
        "average_time_between_versions_days": 0,
        "contributors": set(),
        "change_types": {},
    }

    for v in versions:
        vtype = v.get("version_type", "patch")
        metrics["versions_by_type"][vtype] = (
            metrics["versions_by_type"].get(vtype, 0) + 1
        )

        change_type = v.get("type", "unknown")
        metrics["change_types"][change_type] = (
            metrics["change_types"].get(change_type, 0) + 1
        )

    metrics["contributors"] = list(metrics["contributors"])

    if len(versions) > 1:
        try:
            dates = [
                datetime.fromisoformat(v.get("date", ""))
                for v in versions
                if v.get("date")
            ]
            if len(dates) > 1:
                total_days = (max(dates) - min(dates)).days
                metrics["average_time_between_versions_days"] = round(
                    total_days / (len(versions) - 1), 2
                )
        except:
            pass

    return {
        "metrics": metrics,
        "summary": f"Evolution metrics calculated for {len(versions)} versions",
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "evolve")

    try:
        if action == "evolve":
            spec = payload.get("spec", {})
            history = payload.get("history", [])

            evolution_score = calculate_evolution_score(spec, history)

            return {
                "result": evolution_score,
                "metadata": {
                    "action": "evolve",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "suggest_path":
            current_spec = payload.get("current_spec", {})
            target_spec = payload.get("target_spec", {})
            result = suggest_evolution_path(current_spec, target_spec)
            return {
                "result": result,
                "metadata": {
                    "action": "suggest_path",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "validate_compliance":
            new_spec = payload.get("new_spec", {})
            contracts = payload.get("contracts", [])
            result = validate_evolution_compliance(new_spec, contracts)
            return {
                "result": result,
                "metadata": {
                    "action": "validate_compliance",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "track_metrics":
            versions = payload.get("versions", [])
            result = track_evolution_metrics(versions)
            return {
                "result": result,
                "metadata": {
                    "action": "track_metrics",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "calculate_score":
            spec = payload.get("spec", {})
            history = payload.get("history", [])
            result = calculate_evolution_score(spec, history)
            return {
                "result": result,
                "metadata": {
                    "action": "calculate_score",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error(f"Error in spec_evolution_engine: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
