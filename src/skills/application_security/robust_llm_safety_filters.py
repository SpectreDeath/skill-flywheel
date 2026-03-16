import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def create_adaptive_filter(config: Dict[str, Any]) -> Dict[str, Any]:
    filters = {"rules": [], "ml_model": None}
    filters["rules"].append(
        {"pattern": "ignore.*previous", "action": "block", "weight": 1.0}
    )
    filters["rules"].append(
        {"pattern": "pretend.*different", "action": "block", "weight": 0.9}
    )
    filters["ml_model"] = {"enabled": True, "threshold": config.get("threshold", 0.7)}
    return {"filters": filters, "status": "active"}


def adaptive_defense(prompt: str, filter_config: Dict[str, Any]) -> Dict[str, Any]:
    blocked = any(
        r["pattern"] in prompt.lower()
        for r in filter_config.get("filters", {}).get("rules", [])
    )
    return {
        "blocked": blocked,
        "reason": "rule_match" if blocked else "pass",
        "filter_version": "1.0",
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        action = payload.get("action", "create")
        if action == "create":
            config = payload.get("config", {})
            result = create_adaptive_filter(config)
        elif action == "filter":
            prompt = payload.get("prompt", "")
            filter_config = payload.get("filter_config", {})
            result = adaptive_defend(prompt, filter_config)
        else:
            result = {"error": "Unknown action"}
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
