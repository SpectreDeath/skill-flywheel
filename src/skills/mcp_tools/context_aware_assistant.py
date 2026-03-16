import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class ContextAwareAssistant:
    def __init__(self):
        self.context = {}

    def update_context(self, key: str, value: Any):
        self.context[key] = value


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "assist")
    try:
        if action == "assist":
            assistant = ContextAwareAssistant()
            assistant.update_context("user", "test_user")
            return {
                "result": {"context_size": len(assistant.context)},
                "metadata": {"action": action},
            }
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
