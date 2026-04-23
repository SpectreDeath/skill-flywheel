import hashlib
import logging
import time
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def generate_architecture_decisions(context: Dict[str, Any]) -> List[Dict[str, Any]]:
    decisions = []

    requirements = context.get("requirements", [])

    for req in requirements:
        decision = {
            "id": f"adr-{len(decisions) + 1:03d}",
            "title": req.get("title", "Architecture Decision"),
            "status": "proposed",
            "context": req.get("description", ""),
            "decision": "To be determined based on analysis",
            "consequences": [],
        }

        if "performance" in req.get("title", "").lower():
            decision["decision"] = "Use caching layer and async processing"
            decision["consequences"] = [
                "Increased complexity",
                "Better performance under load",
            ]

        if "scalability" in req.get("title", "").lower():
            decision["decision"] = (
                """Implement horizontal scaling with stateless services"""
            )
            decision["consequences"] = ["Requires load balancer", "Better scalability"]

        if "security" in req.get("title", "").lower():
            decision["decision"] = "Implement multi-layer security with encryption"
            decision["consequences"] = [
                "Additional processing overhead",
                "Better data protection",
            ]

        if not decision["consequences"]:
            decision["consequences"] = [
                "Positive: Improved system",
                "Negative: Additional complexity",
            ]

        decisions.append(decision)

    if not decisions:
        decisions.append(
            {
                "id": "adr-001",
                "title": "Default Architecture Decision",
                "status": "proposed",
                "context": "No specific requirements provided",
                "decision": "Use modular, service-oriented architecture",
                "consequences": [
                    "Flexible design",
                    "May require additional coordination",
                ],
            }
        )

    return decisions


def evaluate_decision(decision: Dict[str, Any], criteria: List[str]) -> Dict[str, Any]:
    scores = {}

    decision_text = decision.get("decision", "").lower()

    for criterion in criteria:
        score = 5

        if "performance" in criterion:
            if "cache" in decision_text or "async" in decision_text:
                score = 8
            elif "sync" in decision_text:
                score = 4

        if "cost" in criterion:
            if "simple" in decision_text or "basic" in decision_text:
                score = 8
            elif "multiple" in decision_text or "complex" in decision_text:
                score = 3

        if "security" in criterion:
            score = 9 if "encrypt" in decision_text or "layer" in decision_text else 4

        if "maintainability" in criterion:
            if "modular" in decision_text or "simple" in decision_text:
                score = 8
            elif "complex" in decision_text:
                score = 3

        scores[criterion] = score

    avg_score = sum(scores.values()) / len(scores) if scores else 0

    return {
        "decision_id": decision.get("id"),
        "scores": scores,
        "average_score": round(avg_score, 2),
        "recommended": avg_score >= 6,
    }


def create_decision_record(
    decision: Dict[str, Any], context: Dict[str, Any]
) -> Dict[str, Any]:
    record = {
        "record_id": f"record-{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}",
        "decision": decision,
        "context": context,
        "created_at": datetime.now().isoformat(),
        "expires_at": None,
        "status": "active",
    }

    return record


def track_decision_history(decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
    status_counts = {"proposed": 0, "accepted": 0, "deprecated": 0, "rejected": 0}

    for decision in decisions:
        status = decision.get("status", "proposed")
        if status in status_counts:
            status_counts[status] += 1

    return {
        "total_decisions": len(decisions),
        "status_breakdown": status_counts,
        "latest_decision": decisions[-1].get("id") if decisions else None,
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "decide")

    try:
        if action == "decide":
            context = payload.get("context", {})
            decisions = generate_architecture_decisions(context)

            return {
                "result": {"decisions": decisions},
                "metadata": {
                    "action": "decide",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "evaluate":
            decision = payload.get("decision", {})
            criteria = payload.get(
                "criteria", ["performance", "cost", "security", "maintainability"]
            )
            result = evaluate_decision(decision, criteria)
            return {
                "result": result,
                "metadata": {
                    "action": "evaluate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "record":
            decision = payload.get("decision", {})
            context = payload.get("context", {})
            result = create_decision_record(decision, context)
            return {
                "result": result,
                "metadata": {
                    "action": "record",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "track_history":
            decisions = payload.get("decisions", [])
            result = track_decision_history(decisions)
            return {
                "result": result,
                "metadata": {
                    "action": "track_history",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "generate":
            context = payload.get("context", {})
            decisions = generate_architecture_decisions(context)
            return {
                "result": {"decisions": decisions},
                "metadata": {
                    "action": "generate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error(f"Error in specification_architecture_decisions: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
