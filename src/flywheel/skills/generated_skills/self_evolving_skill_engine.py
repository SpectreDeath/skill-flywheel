"""
Self-Evolving Skill Engine

Domain: generated_skills
Description: A skill engine that tracks skills with in-memory storage,
supports 3 evolution modes (FIX, DERIVED, CAPTURED), and tracks quality
metrics (applied_count, success_count, completion_rate).
"""

import math
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

EVOLUTION_MODES = ("FIX", "DERIVED", "CAPTURED")


class SkillRecord:
    def __init__(
        self,
        name: str,
        description: str,
        origin: str = "manual",
        triggers: Optional[List[str]] = None,
        skill_id: Optional[str] = None,
    ):
        self.skill_id = skill_id or str(uuid.uuid4())[:8]
        self.name = name
        self.description = description
        self.origin = origin
        self.triggers = triggers or []
        self.applied_count = 0
        self.success_count = 0
        self.evolution_mode: Optional[str] = None
        self.parent_id: Optional[str] = None
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    @property
    def completion_rate(self) -> float:
        if self.applied_count == 0:
            return 0.0
        return round(self.success_count / self.applied_count, 4)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "origin": self.origin,
            "triggers": self.triggers,
            "applied_count": self.applied_count,
            "success_count": self.success_count,
            "completion_rate": self.completion_rate,
            "evolution_mode": self.evolution_mode,
            "parent_id": self.parent_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class SkillEngine:
    def __init__(self):
        self._skills: Dict[str, SkillRecord] = {}

    def add_skill(
        self,
        name: str,
        description: str,
        origin: str = "manual",
        triggers: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        record = SkillRecord(name, description, origin, triggers)
        self._skills[record.skill_id] = record
        return record.to_dict()

    def get_skill(self, identifier: str) -> Optional[Dict[str, Any]]:
        if identifier in self._skills:
            return self._skills[identifier].to_dict()
        for rec in self._skills.values():
            if rec.name == identifier:
                return rec.to_dict()
        return None

    def list_skills(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self._skills.values()]

    def evolve_skill(
        self, skill_id: str, mode: str, trigger_event: str
    ) -> Dict[str, Any]:
        if skill_id not in self._skills:
            raise ValueError(f"Skill {skill_id} not found")
        if mode not in EVOLUTION_MODES:
            raise ValueError(f"Invalid mode {mode}. Must be one of {EVOLUTION_MODES}")
        parent = self._skills[skill_id]
        child = SkillRecord(
            name=f"{parent.name}_evolved_{mode.lower()}",
            description=f"[{mode}] {parent.description} | trigger: {trigger_event}",
            origin=mode,
            triggers=parent.triggers + [trigger_event],
        )
        child.evolution_mode = mode
        child.parent_id = skill_id
        self._skills[child.skill_id] = child
        return child.to_dict()

    def record_usage(self, skill_id: str, success: bool) -> Dict[str, Any]:
        if skill_id not in self._skills:
            raise ValueError(f"Skill {skill_id} not found")
        rec = self._skills[skill_id]
        rec.applied_count += 1
        if success:
            rec.success_count += 1
        rec.updated_at = datetime.now().isoformat()
        return rec.to_dict()

    def get_metrics(self, skill_id: str) -> Dict[str, Any]:
        if skill_id not in self._skills:
            raise ValueError(f"Skill {skill_id} not found")
        rec = self._skills[skill_id]
        return {
            "skill_id": rec.skill_id,
            "name": rec.name,
            "applied_count": rec.applied_count,
            "success_count": rec.success_count,
            "completion_rate": rec.completion_rate,
        }

    def search_skills(self, keyword: str) -> List[Dict[str, Any]]:
        keyword_lower = keyword.lower()
        scored: List[tuple] = []
        for rec in self._skills.values():
            text = f"{rec.name} {rec.description} {' '.join(rec.triggers)}".lower()
            tf = text.count(keyword_lower)
            if tf == 0:
                continue
            idf = math.log((1 + len(self._skills)) / (1 + tf)) + 1
            score = round(tf * idf, 4)
            scored.append((score, rec))
        scored.sort(key=lambda x: -x[0])
        return [{"score": s, **r.to_dict()} for s, r in scored]


_engine = SkillEngine()


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "list_skills")

    if action == "list_skills":
        result = _engine.list_skills()
    elif action == "add_skill":
        result = _engine.add_skill(
            name=payload["name"],
            description=payload.get("description", ""),
            origin=payload.get("origin", "manual"),
            triggers=payload.get("triggers"),
        )
    elif action == "evolve_skill":
        result = _engine.evolve_skill(
            skill_id=payload["skill_id"],
            mode=payload["mode"],
            trigger_event=payload.get("trigger_event", ""),
        )
    elif action == "get_skill":
        result = _engine.get_skill(payload["identifier"])
    elif action == "record_usage":
        result = _engine.record_usage(
            skill_id=payload["skill_id"], success=payload.get("success", True)
        )
    elif action == "get_metrics":
        result = _engine.get_metrics(payload["skill_id"])
    elif action == "search_skills":
        result = _engine.search_skills(payload["keyword"])
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

    async def demo():
        r1 = await invoke(
            {
                "action": "add_skill",
                "name": "test_gen",
                "description": "Generate unit tests",
                "triggers": ["test", "unit"],
            }
        )
        sid = r1["result"]["skill_id"]
        await invoke({"action": "record_usage", "skill_id": sid, "success": True})
        await invoke({"action": "record_usage", "skill_id": sid, "success": False})
        print(await invoke({"action": "get_metrics", "skill_id": sid}))
        print(await invoke({"action": "search_skills", "keyword": "test"}))

    asyncio.run(demo())
