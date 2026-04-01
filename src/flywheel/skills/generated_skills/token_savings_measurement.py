"""
Token Savings Measurement

Domain: generated_skills
Description: Structured framework for measuring economic impact of skill reuse.
Computes cost estimates with configurable per-token pricing for cold vs warm starts.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

DEFAULT_PRICING = {
    "input_per_1k": 0.003,
    "output_per_1k": 0.015,
}

TOKEN_DIVISOR = 4.0


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // int(TOKEN_DIVISOR))


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    pricing: Optional[Dict[str, float]] = None,
) -> Dict[str, float]:
    p = pricing or DEFAULT_PRICING
    input_cost = (input_tokens / 1000.0) * p["input_per_1k"]
    output_cost = (output_tokens / 1000.0) * p["output_per_1k"]
    return {
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(input_cost + output_cost, 6),
    }


class SavingsMeasurement:
    def __init__(self, pricing: Optional[Dict[str, float]] = None):
        self.pricing = pricing or DEFAULT_PRICING
        self._runs: List[Dict[str, Any]] = []

    def measure(self, task: str, skill_context: str = "") -> Dict[str, Any]:
        cold_text = (
            f"Solve from scratch with full reasoning: {task}. "
            f"Explain every step, provide code, validate output."
        )
        warm_text = f"Apply known pattern: {skill_context or task[:50]}. Task: {task}"
        cold_tokens = estimate_tokens(cold_text)
        warm_tokens = estimate_tokens(warm_text)
        output_est = estimate_tokens(task)

        cold_cost = estimate_cost(cold_tokens, output_est, self.pricing)
        warm_cost = estimate_cost(warm_tokens, output_est, self.pricing)
        saved_tokens = cold_tokens - warm_tokens
        saved_cost = round(cold_cost["total_cost"] - warm_cost["total_cost"], 6)
        pct = round((saved_tokens / cold_tokens) * 100, 2) if cold_tokens else 0.0

        entry = {
            "task": task,
            "cold_tokens": cold_tokens,
            "warm_tokens": warm_tokens,
            "tokens_saved": saved_tokens,
            "savings_pct": pct,
            "cold_cost": cold_cost["total_cost"],
            "warm_cost": warm_cost["total_cost"],
            "cost_saved": saved_cost,
            "timestamp": datetime.now().isoformat(),
        }
        self._runs.append(entry)
        return entry

    def batch_benchmark(
        self, tasks: List[str], skill_context: str = ""
    ) -> Dict[str, Any]:
        results = [self.measure(t, skill_context) for t in tasks]
        n = len(results)
        return {
            "task_count": n,
            "avg_tokens_saved": round(sum(r["tokens_saved"] for r in results) / n, 2),
            "avg_savings_pct": round(sum(r["savings_pct"] for r in results) / n, 2),
            "total_cost_saved": round(sum(r["cost_saved"] for r in results), 6),
            "results": results,
        }

    def get_report(self) -> Dict[str, Any]:
        if not self._runs:
            return {"message": "No measurements recorded yet."}
        n = len(self._runs)
        total_tokens = sum(r["tokens_saved"] for r in self._runs)
        total_cost = sum(r["cost_saved"] for r in self._runs)
        avg_pct = round(sum(r["savings_pct"] for r in self._runs) / n, 2)
        return {
            "report_date": datetime.now().isoformat(),
            "total_runs": n,
            "total_tokens_saved": total_tokens,
            "total_cost_saved": round(total_cost, 6),
            "avg_savings_pct": avg_pct,
            "pricing_model": self.pricing,
            "per_run": self._runs[-5:],
        }


_instance = SavingsMeasurement()


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "measure")

    if action == "measure":
        result = _instance.measure(
            task=payload["task"],
            skill_context=payload.get("skill_context", ""),
        )
    elif action == "estimate_cost":
        result = estimate_cost(
            input_tokens=payload.get("input_tokens", 0),
            output_tokens=payload.get("output_tokens", 0),
            pricing=payload.get("pricing"),
        )
    elif action == "batch_benchmark":
        result = _instance.batch_benchmark(
            tasks=payload["tasks"],
            skill_context=payload.get("skill_context", ""),
        )
    elif action == "get_report":
        result = _instance.get_report()
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
                {"action": "estimate_cost", "input_tokens": 500, "output_tokens": 200}
            )
        )
        print(
            await invoke({"action": "measure", "task": "Implement binary search tree"})
        )
        print(await invoke({"action": "get_report"}))

    asyncio.run(demo())
