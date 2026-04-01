"""
Pipeline Skill Accumulation

Skill: pipeline-skill-accumulation
Domain: generated_skills
Description: Tracks skill library growth and reuse rate across sequential task pipelines.

Actions:
- start_pipeline: Initialize a new pipeline run
- record_task: Record task execution with skills_before, skills_after, evolved, reused
- get_summary: Return pipeline summary (total time, total evolved, total reused)
- get_accumulation_curve: Return data for plotting skill accumulation over tasks
- get_reuse_trend: Return reuse rate trend across tasks
"""

import time
from datetime import datetime
from typing import Any, Dict, List


class PipelineSkillAccumulation:
    """Tracks skill growth and reuse across a pipeline of tasks."""

    def __init__(self) -> None:
        self._current: Dict[str, Any] = {}
        self._completed: List[Dict[str, Any]] = []

    def start_pipeline(self, pipeline_id: str) -> Dict[str, Any]:
        """Initialize a new pipeline run."""
        self._current = {
            "pipeline_id": pipeline_id,
            "start_time": time.monotonic(),
            "tasks": [],
            "total_evolved": 0,
            "total_reused": 0,
            "initial_skill_count": 0,
        }
        return {"pipeline_id": pipeline_id, "status": "started"}

    def record_task(
        self,
        task_name: str,
        skills_before: int,
        skills_after: int,
        evolved: int = 0,
        reused: int = 0,
    ) -> Dict[str, Any]:
        """Record a single task execution within the active pipeline."""
        if not self._current:
            return {"error": "No active pipeline. Call start_pipeline first."}
        entry = {
            "task_name": task_name,
            "skills_before": skills_before,
            "skills_after": skills_after,
            "evolved": evolved,
            "reused": reused,
            "timestamp": time.monotonic(),
        }
        self._current["tasks"].append(entry)
        self._current["total_evolved"] += evolved
        self._current["total_reused"] += reused
        if not self._current["tasks"] or len(self._current["tasks"]) == 1:
            self._current["initial_skill_count"] = skills_before
        return {
            "task_name": task_name,
            "skills_delta": skills_after - skills_before,
            "cumulative_evolved": self._current["total_evolved"],
            "cumulative_reused": self._current["total_reused"],
        }

    def get_summary(self) -> Dict[str, Any]:
        """Return pipeline summary metrics."""
        if not self._current:
            return {"error": "No active pipeline"}
        elapsed = time.monotonic() - self._current["start_time"]
        tasks = self._current["tasks"]
        final_skills = (
            tasks[-1]["skills_after"] if tasks else self._current["initial_skill_count"]
        )
        return {
            "pipeline_id": self._current["pipeline_id"],
            "total_tasks": len(tasks),
            "total_time_seconds": round(elapsed, 3),
            "total_evolved": self._current["total_evolved"],
            "total_reused": self._current["total_reused"],
            "initial_skills": self._current["initial_skill_count"],
            "final_skills": final_skills,
            "net_growth": final_skills - self._current["initial_skill_count"],
        }

    def get_accumulation_curve(self) -> Dict[str, List[Any]]:
        """Return cumulative skill count at each task step for plotting."""
        tasks = self._current.get("tasks", [])
        indices = list(range(len(tasks)))
        counts = [t["skills_after"] for t in tasks]
        return {"task_indices": indices, "skill_counts": counts}

    def get_reuse_trend(self) -> Dict[str, List[Any]]:
        """Return per-task reuse rate trend."""
        tasks = self._current.get("tasks", [])
        indices = list(range(len(tasks)))
        rates = [
            round(t["reused"] / t["skills_before"], 4)
            if t["skills_before"] > 0
            else 0.0
            for t in tasks
        ]
        return {"task_indices": indices, "reuse_rates": rates}

    def archive_pipeline(self) -> None:
        """Move current pipeline to completed list."""
        if self._current:
            self._completed.append(self._current)
            self._current = {}


_instance = PipelineSkillAccumulation()


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Entry point for pipeline-skill-accumulation skill."""
    action = payload.get("action", "get_summary")

    if action == "start_pipeline":
        result = _instance.start_pipeline(payload.get("pipeline_id", "default"))
    elif action == "record_task":
        result = _instance.record_task(
            task_name=payload.get("task_name", ""),
            skills_before=payload.get("skills_before", 0),
            skills_after=payload.get("skills_after", 0),
            evolved=payload.get("evolved", 0),
            reused=payload.get("reused", 0),
        )
    elif action == "get_summary":
        result = _instance.get_summary()
    elif action == "get_accumulation_curve":
        result = _instance.get_accumulation_curve()
    elif action == "get_reuse_trend":
        result = _instance.get_reuse_trend()
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

    asyncio.run(invoke({"action": "start_pipeline", "pipeline_id": "demo-pipeline"}))
    for i, (sb, sa, ev, ru) in enumerate(
        [
            (10, 11, 1, 0),
            (11, 13, 2, 3),
            (13, 14, 1, 5),
            (14, 16, 2, 8),
        ]
    ):
        asyncio.run(
            invoke(
                {
                    "action": "record_task",
                    "task_name": f"task-{i + 1}",
                    "skills_before": sb,
                    "skills_after": sa,
                    "evolved": ev,
                    "reused": ru,
                }
            )
        )
    print(asyncio.run(invoke({"action": "get_summary"})))
    print(asyncio.run(invoke({"action": "get_accumulation_curve"})))
    print(asyncio.run(invoke({"action": "get_reuse_trend"})))
