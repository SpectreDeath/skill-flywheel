"""
Skill Evolution Metadata

Skill: skill-evolution-metadata
Domain: generated_skills
Description: Manages extended SKILL.md metadata with evolution tracking
(origin, version, triggers, quality metrics).

Actions:
- create_skill_meta: Create new skill metadata entry
- update_version: Increment version on DERIVED/FIX evolution
- add_trigger: Add a trigger keyword to a skill
- update_quality: Update applied_count, success_count, completion_rate
- get_evolution_history: Return version lineage
- validate_metadata: Check required fields are present
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


class SkillEvolutionMetadata:
    """Tracks evolution metadata for a skill over its lifecycle."""

    REQUIRED_FIELDS = [
        "skill_name",
        "domain",
        "description",
        "version",
        "evolution_type",
    ]

    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def create_skill_meta(
        self,
        skill_name: str,
        domain: str,
        description: str,
        origin: str = "user",
        version: str = "1.0.0",
        evolution_type: str = "ORIGINAL",
        triggers: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create a new skill metadata entry."""
        meta = {
            "skill_name": skill_name,
            "domain": domain,
            "description": description,
            "origin": origin,
            "version": version,
            "evolution_type": evolution_type,
            "triggers": triggers or [],
            "applied_count": 0,
            "success_count": 0,
            "completion_rate": 0.0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "history": [
                {
                    "version": version,
                    "type": evolution_type,
                    "timestamp": datetime.now().isoformat(),
                }
            ],
        }
        self._store[skill_name] = meta
        return meta

    def update_version(
        self,
        skill_name: str,
        evolution_type: str = "DERIVED",
    ) -> Dict[str, Any]:
        """Increment version on DERIVED/FIX evolution."""
        meta = self._store.get(skill_name)
        if not meta:
            return {"error": f"Skill '{skill_name}' not found"}
        parts = meta["version"].split(".")
        if evolution_type == "FIX":
            parts[2] = str(int(parts[2]) + 1)
        else:
            parts[1] = str(int(parts[1]) + 1)
            parts[2] = "0"
        new_version = ".".join(parts)
        meta["version"] = new_version
        meta["evolution_type"] = evolution_type
        meta["updated_at"] = datetime.now().isoformat()
        meta["history"].append(
            {
                "version": new_version,
                "type": evolution_type,
                "timestamp": datetime.now().isoformat(),
            }
        )
        return {
            "skill_name": skill_name,
            "new_version": new_version,
            "evolution_type": evolution_type,
        }

    def add_trigger(self, skill_name: str, trigger: str) -> Dict[str, Any]:
        """Add a trigger keyword to a skill."""
        meta = self._store.get(skill_name)
        if not meta:
            return {"error": f"Skill '{skill_name}' not found"}
        if trigger not in meta["triggers"]:
            meta["triggers"].append(trigger)
        meta["updated_at"] = datetime.now().isoformat()
        return {"skill_name": skill_name, "triggers": meta["triggers"]}

    def update_quality(
        self,
        skill_name: str,
        applied_count: int,
        success_count: int,
    ) -> Dict[str, Any]:
        """Update applied_count, success_count, completion_rate."""
        meta = self._store.get(skill_name)
        if not meta:
            return {"error": f"Skill '{skill_name}' not found"}
        meta["applied_count"] = applied_count
        meta["success_count"] = success_count
        meta["completion_rate"] = (
            round(success_count / applied_count, 4) if applied_count > 0 else 0.0
        )
        meta["updated_at"] = datetime.now().isoformat()
        return {
            "skill_name": skill_name,
            "applied_count": applied_count,
            "success_count": success_count,
            "completion_rate": meta["completion_rate"],
        }

    def get_evolution_history(self, skill_name: str) -> List[Dict[str, Any]]:
        """Return version lineage for a skill."""
        meta = self._store.get(skill_name)
        if not meta:
            return []
        return meta["history"]

    def validate_metadata(self, skill_name: str) -> Dict[str, Any]:
        """Check that all required fields are present."""
        meta = self._store.get(skill_name)
        if not meta:
            return {"valid": False, "errors": [f"Skill '{skill_name}' not found"]}
        missing = [f for f in self.REQUIRED_FIELDS if f not in meta or not meta[f]]
        return {"valid": len(missing) == 0, "missing_fields": missing}


_instance = SkillEvolutionMetadata()


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Entry point for skill-evolution-metadata skill."""
    action = payload.get("action", "validate_metadata")

    if action == "create_skill_meta":
        result = _instance.create_skill_meta(
            skill_name=payload.get("skill_name", ""),
            domain=payload.get("domain", ""),
            description=payload.get("description", ""),
            origin=payload.get("origin", "user"),
            version=payload.get("version", "1.0.0"),
            evolution_type=payload.get("evolution_type", "ORIGINAL"),
            triggers=payload.get("triggers"),
        )
    elif action == "update_version":
        result = _instance.update_version(
            payload.get("skill_name", ""), payload.get("evolution_type", "DERIVED")
        )
    elif action == "add_trigger":
        result = _instance.add_trigger(
            payload.get("skill_name", ""), payload.get("trigger", "")
        )
    elif action == "update_quality":
        result = _instance.update_quality(
            payload.get("skill_name", ""),
            payload.get("applied_count", 0),
            payload.get("success_count", 0),
        )
    elif action == "get_evolution_history":
        result = {
            "history": _instance.get_evolution_history(payload.get("skill_name", ""))
        }
    elif action == "validate_metadata":
        result = _instance.validate_metadata(payload.get("skill_name", ""))
    else:
        result = {"error": f"Unknown action: {action}"}

    return {
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }


if __name__ == "__main__":
    import asyncio

    asyncio.run(
        invoke(
            {
                "action": "create_skill_meta",
                "skill_name": "demo-skill",
                "domain": "generated_skills",
                "description": "Demo skill for testing metadata",
                "triggers": ["demo", "test"],
            }
        )
    )
    asyncio.run(
        invoke(
            {
                "action": "update_version",
                "skill_name": "demo-skill",
                "evolution_type": "DERIVED",
            }
        )
    )
    asyncio.run(
        invoke(
            {"action": "add_trigger", "skill_name": "demo-skill", "trigger": "new_tag"}
        )
    )
    asyncio.run(
        invoke(
            {
                "action": "update_quality",
                "skill_name": "demo-skill",
                "applied_count": 10,
                "success_count": 8,
            }
        )
    )
    print(
        asyncio.run(
            invoke({"action": "get_evolution_history", "skill_name": "demo-skill"})
        )
    )
    print(
        asyncio.run(invoke({"action": "validate_metadata", "skill_name": "demo-skill"}))
    )
