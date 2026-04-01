"""
Cold-Warm Transition

Domain: generated_skills
Description: Measures token savings when reusing skills vs starting cold.
Tracks cold_start() and warm_start() simulations, computes savings percentages.
Uses text length as a proxy for token count (len(text) / 4 approximation).
"""

from datetime import datetime
from typing import Any, Dict, List


TOKEN_DIVISOR = 4.0


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // int(TOKEN_DIVISOR))


def cold_start(task: str) -> Dict[str, Any]:
    cold_prompt = (
        f"You are an expert assistant. Solve this task from scratch with no prior context.\n"
        f"Provide a detailed, step-by-step solution.\n"
        f"Task: {task}\n"
        f"Requirements: explain reasoning, show code, validate approach."
    )
    tokens = estimate_tokens(cold_prompt)
    return {
        "approach": "cold",
        "task": task,
        "estimated_tokens": tokens,
        "prompt_length": len(cold_prompt),
    }


def warm_start(task: str, skill_context: str = "") -> Dict[str, Any]:
    context = skill_context or f"Proven pattern for: {task[:60]}"
    warm_prompt = (
        f"Using the following validated skill context:\n{context}\nApply it to: {task}"
    )
    tokens = estimate_tokens(warm_prompt)
    return {
        "approach": "warm",
        "task": task,
        "estimated_tokens": tokens,
        "prompt_length": len(warm_prompt),
    }


class TransitionTracker:
    def __init__(self):
        self._history: List[Dict[str, Any]] = []

    def measure(self, task: str, skill_context: str = "") -> Dict[str, Any]:
        cold = cold_start(task)
        warm = warm_start(task, skill_context)
        saved = cold["estimated_tokens"] - warm["estimated_tokens"]
        pct = (
            round((saved / cold["estimated_tokens"]) * 100, 2)
            if cold["estimated_tokens"] > 0
            else 0.0
        )
        entry = {
            "task": task,
            "cold_tokens": cold["estimated_tokens"],
            "warm_tokens": warm["estimated_tokens"],
            "tokens_saved": saved,
            "savings_pct": pct,
            "timestamp": datetime.now().isoformat(),
        }
        self._history.append(entry)
        return entry

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self._history)

    def get_summary(self) -> Dict[str, Any]:
        if not self._history:
            return {"count": 0, "avg_savings_pct": 0.0, "total_tokens_saved": 0}
        total_saved = sum(e["tokens_saved"] for e in self._history)
        avg_pct = round(
            sum(e["savings_pct"] for e in self._history) / len(self._history), 2
        )
        return {
            "count": len(self._history),
            "avg_savings_pct": avg_pct,
            "total_tokens_saved": total_saved,
            "min_savings_pct": min(e["savings_pct"] for e in self._history),
            "max_savings_pct": max(e["savings_pct"] for e in self._history),
        }

    def benchmark(self, tasks: List[str], skill_context: str = "") -> Dict[str, Any]:
        results = [self.measure(t, skill_context) for t in tasks]
        avg_saved = round(sum(r["tokens_saved"] for r in results) / len(results), 2)
        avg_pct = round(sum(r["savings_pct"] for r in results) / len(results), 2)
        return {
            "task_count": len(tasks),
            "results": results,
            "avg_tokens_saved": avg_saved,
            "avg_savings_pct": avg_pct,
        }


_tracker = TransitionTracker()


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "measure")

    if action == "measure":
        result = _tracker.measure(
            task=payload["task"],
            skill_context=payload.get("skill_context", ""),
        )
    elif action == "get_history":
        result = _tracker.get_history()
    elif action == "get_summary":
        result = _tracker.get_summary()
    elif action == "benchmark":
        result = _tracker.benchmark(
            tasks=payload["tasks"],
            skill_context=payload.get("skill_context", ""),
        )
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
        print(
            await invoke(
                {"action": "measure", "task": "Build a REST API with authentication"}
            )
        )
        print(
            await invoke(
                {
                    "action": "benchmark",
                    "tasks": ["Sort a list", "Parse JSON", "Connect to DB"],
                }
            )
        )
        print(await invoke({"action": "get_summary"}))

    asyncio.run(demo())
