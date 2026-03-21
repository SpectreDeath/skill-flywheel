import hashlib
import logging
import time
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def assess_migration_complexity(
    source: Dict[str, Any], target: Dict[str, Any]
) -> Dict[str, Any]:
    complexity_score = 0
    factors = []

    source_db = source.get("type", "")
    target_db = target.get("type", "")

    if source_db != target_db:
        complexity_score += 30
        factors.append(
            f"Cross-database migration ({source_db} to {target_db})"
        )

    source_version = source.get("version", "1.0")
    target_version = target.get("version", "1.0")

    if source_version != target_version:
        complexity_score += 15
        factors.append("Version upgrade required")

    tables = source.get("tables", [])
    if len(tables) > 50:
        complexity_score += 20
        factors.append(f"Large number of tables ({len(tables)})")

    size_gb = source.get("size_gb", 0)
    if size_gb > 100:
        complexity_score += 25
        factors.append(f"Large database size ({size_gb} GB)")

    if source.get("has_stored_procedures"):
        complexity_score += 15
        factors.append("Stored procedures need conversion")

    if source.get("has_triggers"):
        complexity_score += 10
        factors.append("Triggers need conversion")

    if complexity_score >= 70:
        complexity_level = "very_high"
    elif complexity_score >= 50:
        complexity_level = "high"
    elif complexity_score >= 30:
        complexity_level = "medium"
    else:
        complexity_level = "low"

    return {
        "complexity_score": complexity_score,
        "complexity_level": complexity_level,
        "factors": factors,
        "estimated_duration_days": max(1, complexity_score // 10),
    }


def generate_migration_phases(complexity: Dict[str, Any]) -> List[Dict[str, Any]]:
    phases = []

    phases.append(
        {
            "phase": 1,
            "name": "Assessment & Planning",
            "duration_days": 3,
            "activities": [
                "Analyze source database schema",
                "Identify migration paths",
                "Create data mapping rules",
                "Estimate resource requirements",
            ],
            "deliverables": ["Migration assessment report", "Detailed migration plan"],
        }
    )

    phases.append(
        {
            "phase": 2,
            "name": "Schema Migration",
            "duration_days": 5,
            "activities": [
                "Create target database schema",
                "Convert stored procedures",
                "Migrate views and triggers",
                "Set up indexes",
            ],
            "deliverables": ["Migrated schema", "Converted code objects"],
        }
    )

    if complexity.get("complexity_level") in ["high", "very_high"]:
        phases.append(
            {
                "phase": 3,
                "name": "Data Migration (Pilot)",
                "duration_days": 7,
                "activities": [
                    "Migrate subset of data",
                    "Validate data integrity",
                    "Test application connectivity",
                    "Benchmark performance",
                ],
                "deliverables": ["Pilot migration results", "Performance benchmarks"],
            }
        )

    phases.append(
        {
            "phase": 4,
            "name": "Full Data Migration",
            "duration_days": complexity.get("estimated_duration_days", 10),
            "activities": [
                "Perform full data migration",
                "Verify data completeness",
                "Run validation scripts",
                "Test all interfaces",
            ],
            "deliverables": ["Complete migrated database", "Validation report"],
        }
    )

    phases.append(
        {
            "phase": 5,
            "name": "Cutover & Validation",
            "duration_days": 2,
            "activities": [
                "Plan cutover window",
                "Final backup of source",
                "Switch to target database",
                "Validate all systems",
            ],
            "deliverables": ["Successful cutover", "Post-migration validation report"],
        }
    )

    return phases


def generate_data_mapping_rules(
    source_schema: Dict[str, Any], target_schema: Dict[str, Any]
) -> List[Dict[str, Any]]:
    rules = []

    source_tables = source_schema.get("tables", [])
    target_tables = target_schema.get("tables", [])

    target_table_names = [t.get("name") for t in target_tables]

    for source_table in source_tables:
        source_name = source_table.get("name")

        if source_name in target_table_names:
            rules.append(
                {
                    "source_table": source_name,
                    "target_table": source_name,
                    "mapping_type": "direct",
                    "status": "mapped",
                }
            )
        else:
            for target_table in target_tables:
                if source_name.lower() == target_table.get("name", "").lower():
                    rules.append(
                        {
                            "source_table": source_name,
                            "target_table": target_table.get("name"),
                            "mapping_type": "case_sensitive",
                            "status": "mapped",
                        }
                    )
                    break
            else:
                rules.append(
                    {
                        "source_table": source_name,
                        "target_table": None,
                        "mapping_type": "unmapped",
                        "status": "requires_review",
                    }
                )

    return rules


def create_rollback_plan(migration: Dict[str, Any]) -> Dict[str, Any]:
    rollback = {
        "plan_id": f"rollback-{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}",
        "created_at": datetime.now().isoformat(),
    }

    rollback["prerequisites"] = [
        "Full backup of source database before migration",
        "Backup of target database at each phase",
        "Rollback scripts prepared in advance",
    ]

    rollback["steps"] = [
        {"step": 1, "action": "Stop all application connections", "order": "first"},
        {"step": 2, "action": "Restore source database from backup", "order": "second"},
        {
            "step": 3,
            "action": "Update application connection strings",
            "order": "third",
        },
        {"step": 4, "action": "Verify application functionality", "order": "fourth"},
        {"step": 5, "action": "Document rollback incident", "order": "fifth"},
    ]

    rollback["estimated_time_minutes"] = 120

    rollback["warnings"] = [
        "Ensure source database has not been modified during rollback",
        "All data written to target since last backup will be lost",
        "Coordinate with all stakeholders before initiating rollback",
    ]

    return rollback


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "plan")

    try:
        if action == "plan":
            source = payload.get("source", {})
            target = payload.get("target", {})

            complexity = assess_migration_complexity(source, target)
            phases = generate_migration_phases(complexity)

            return {
                "result": {"complexity": complexity, "phases": phases},
                "metadata": {"action": "plan", "timestamp": datetime.now().isoformat()},
            }

        elif action == "assess":
            source = payload.get("source", {})
            target = payload.get("target", {})
            result = assess_migration_complexity(source, target)
            return {
                "result": result,
                "metadata": {
                    "action": "assess",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "map":
            source_schema = payload.get("source_schema", {})
            target_schema = payload.get("target_schema", {})
            rules = generate_data_mapping_rules(source_schema, target_schema)
            return {
                "result": {"mapping_rules": rules},
                "metadata": {"action": "map", "timestamp": datetime.now().isoformat()},
            }

        elif action == "rollback":
            migration = payload.get("migration", {})
            plan = create_rollback_plan(migration)
            return {
                "result": plan,
                "metadata": {
                    "action": "rollback",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "phases":
            complexity = payload.get("complexity", {})
            phases = generate_migration_phases(complexity)
            return {
                "result": {"phases": phases},
                "metadata": {
                    "action": "phases",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error(f"Error in data_migration_strategy: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
