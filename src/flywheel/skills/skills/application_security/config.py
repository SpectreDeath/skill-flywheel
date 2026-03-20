import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


def analyze_config(config: Dict[str, Any]) -> Dict[str, Any]:
    issues = []
    if config.get("debug"):
        issues.append({"type": "debug_enabled", "severity": "high"})
    if config.get("CORS", {}).get("allow_origins") == ["*"]:
        issues.append({"type": " permissive_cors", "severity": "medium"})
    if not config.get("SSL", False):
        issues.append({"type": "no_ssl", "severity": "high"})
    return {"issues": issues, "score": 100 - len(issues) * 20}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "analyze")
    try:
        config = payload.get("config", {})
        result = analyze_config(config)
        return {
            "result": result,
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
