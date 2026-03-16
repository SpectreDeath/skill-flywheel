import time
import logging
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


def analyze_task_complexity(task_text: str) -> Dict[str, Any]:
    complexity_score = 0
    risk_factors = []

    complexity_indicators = {
        r"\bcomplex\b": 2,
        r"\badvanced\b": 2,
        r"\bdifficult\b": 2,
        r"\bmultiple\b": 1,
        r"\bintegrat\w+\b": 2,
        r"\bdepend\w+\b": 1,
        r"\boptimiz\w+\b": 2,
        r"\bsecurity\b": 2,
        r"\bscale\w+\b": 2,
        r"\breal-time\b": 3,
        r"\bconcurrent\w+\b": 2,
    }

    for pattern, weight in complexity_indicators.items():
        if re.search(pattern, task_text, re.IGNORECASE):
            complexity_score += weight
            risk_factors.append(pattern.strip(r"\b"))

    complexity_score = min(10, complexity_score)

    if complexity_score >= 7:
        risk_level = "high"
    elif complexity_score >= 4:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "complexity_score": complexity_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
    }


def predict_failure_probability(task_data: Dict[str, Any]) -> float:
    base_probability = 0.1

    complexity = task_data.get("complexity_score", 0)
    if complexity >= 7:
        base_probability += 0.3
    elif complexity >= 4:
        base_probability += 0.15

    has_dependencies = task_data.get("dependencies", [])
    if len(has_dependencies) > 3:
        base_probability += 0.15

    vague_terms = ["TBD", "to be determined", "flexible", "as needed"]
    description = task_data.get("task_description", "").lower()
    for term in vague_terms:
        if term in description:
            base_probability += 0.1

    return min(0.95, base_probability)


def analyze_emotional_tone(text: str) -> Dict[str, Any]:
    emotional_indicators = {
        "urgent": {"weight": 0.8, "emotion": "anxiety"},
        "critical": {"weight": 0.9, "emotion": "stress"},
        "important": {"weight": 0.6, "emotion": "concern"},
        "must": {"weight": 0.7, "emotion": "pressure"},
        "should": {"weight": 0.4, "emotion": "recommendation"},
        "may": {"weight": 0.2, "emotion": "flexibility"},
        "optional": {"weight": 0.1, "emotion": "relaxation"},
    }

    emotional_charge = 0.0
    detected_emotions = []

    text_lower = text.lower()
    for term, data in emotional_indicators.items():
        if term in text_lower:
            emotional_charge += data["weight"]
            detected_emotions.append(data["emotion"])

    emotional_charge = min(1.0, emotional_charge / 3)

    return {
        "emotional_charge": emotional_charge,
        "detected_emotions": list(set(detected_emotions)),
        "tone": "high"
        if emotional_charge > 0.6
        else "medium"
        if emotional_charge > 0.3
        else "low",
    }


def reverse_engineer_dependencies(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    dependencies = []

    for i, task in enumerate(tasks):
        task_deps = []
        task_text = task.get("task_description", "").lower()

        keywords = [
            "before",
            "after",
            "requires",
            "dependent",
            "prerequisite",
            "following",
        ]
        for j, prev_task in enumerate(tasks[:i]):
            prev_text = prev_task.get("task_description", "").lower()
            for kw in keywords:
                if kw in task_text and kw in prev_text:
                    task_deps.append(prev_task.get("task_id"))

        if not task_deps and i > 0:
            task_deps.append(tasks[i - 1].get("task_id"))

        dependencies.append(
            {
                "task_id": task.get("task_id"),
                "discovered_dependencies": list(set(task_deps)),
                "analysis_method": "reverse_engineering",
            }
        )

    return dependencies


def decompose_specification(spec_data: Dict[str, Any]) -> Dict[str, Any]:
    specification = spec_data.get("specification", {})
    specification_text = specification.get("text", "")
    specification_id = specification.get(
        "id", "spec-" + hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    )

    analysis_params = spec_data.get("analysis_parameters", {})
    failure_prediction_enabled = analysis_params.get("failure_prediction_enabled", True)
    emotional_analysis_enabled = analysis_params.get("emotional_analysis_enabled", True)
    reverse_engineering_enabled = analysis_params.get(
        "reverse_engineering_enabled", True
    )

    sentences = re.split(r"[.!?]+", specification_text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        sentences = [
            "Implement core functionality",
            "Handle edge cases",
            "Add error handling",
            "Write tests",
            "Deploy to production",
        ]

    tasks = []
    for i, sentence in enumerate(sentences):
        task_id = "task-{:03d}".format(i + 1)

        complexity = analyze_task_complexity(sentence)
        failure_prob = (
            predict_failure_probability(complexity)
            if failure_prediction_enabled
            else 0.0
        )
        emotional = (
            analyze_emotional_tone(sentence)
            if emotional_analysis_enabled
            else {"emotional_charge": 0.0, "detected_emotions": [], "tone": "low"}
        )

        task = {
            "task_id": task_id,
            "task_name": sentence[:50] + ("..." if len(sentence) > 50 else ""),
            "task_description": sentence,
            "complexity_score": complexity["complexity_score"],
            "risk_level": complexity["risk_level"],
            "failure_probability": failure_prob,
            "emotional_impact": emotional,
        }
        tasks.append(task)

    discovered_deps = (
        reverse_engineer_dependencies(tasks) if reverse_engineering_enabled else []
    )
    for i, dep in enumerate(discovered_deps):
        if i < len(tasks):
            tasks[i]["discovered_dependencies"] = dep.get("discovered_dependencies", [])

    critical_path = [t["task_id"] for t in tasks if t.get("risk_level") == "high"]

    parallel_tasks = []
    for i, task in enumerate(tasks):
        if task.get("risk_level") == "low" and not task.get("discovered_dependencies"):
            parallel_tasks.append(task["task_id"])

    high_risk = [t for t in tasks if t.get("risk_level") == "high"]
    mitigation_strategies = []
    for task in high_risk:
        strategies = [
            "Break down into smaller subtasks",
            "Add additional review checkpoints",
            "Allocate extra time for testing",
            "Prepare fallback implementation",
        ]
        mitigation_strategies.append(
            {"task_id": task["task_id"], "strategies": strategies[:2]}
        )

    total_effort = sum([t.get("complexity_score", 1) * 2 for t in tasks])
    estimated_hours = max(1, total_effort)

    return {
        "specification_metadata": {
            "specification_id": specification_id,
            "decomposition_date": datetime.now().isoformat(),
            "analysis_approach": [
                "predictive_failure_analysis" if failure_prediction_enabled else None,
                "emotional_tone_analysis" if emotional_analysis_enabled else None,
                "reverse_engineering" if reverse_engineering_enabled else None,
            ],
        },
        "task_hierarchy": tasks,
        "task_timeline": {
            "total_tasks": len(tasks),
            "estimated_duration_hours": estimated_hours,
            "critical_path": critical_path,
            "parallelizable_tasks": parallel_tasks,
        },
        "risk_analysis": {
            "high_risk_tasks": [t["task_id"] for t in high_risk],
            "mitigation_strategies": mitigation_strategies,
            "total_risk_score": sum([t.get("complexity_score", 0) for t in tasks]),
        },
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "decompose")

    try:
        if action == "decompose":
            result = decompose_specification(payload)
            return {
                "result": result,
                "metadata": {
                    "action": "decompose",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "analyze_complexity":
            task_text = payload.get("task_text", "")
            complexity = analyze_task_complexity(task_text)
            return {
                "result": complexity,
                "metadata": {
                    "action": "analyze_complexity",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "predict_failure":
            task_data = payload.get("task_data", {})
            prediction = predict_failure_probability(task_data)
            return {
                "result": {"failure_probability": prediction},
                "metadata": {
                    "action": "predict_failure",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "analyze_emotions":
            text = payload.get("text", "")
            emotional = analyze_emotional_tone(text)
            return {
                "result": emotional,
                "metadata": {
                    "action": "analyze_emotions",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "reverse_engineer":
            tasks = payload.get("tasks", [])
            deps = reverse_engineer_dependencies(tasks)
            return {
                "result": {"dependencies": deps},
                "metadata": {
                    "action": "reverse_engineer",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": "Unknown action: {}".format(action)},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error("Error in spec_to_task_decomposition: {}".format(e))
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
