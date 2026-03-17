import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class AgenticZettelkastenMemory:
    def __init__(self):
        self.notes = []

    def create_note(self, title: str, content: str) -> Dict:
        note = {
            "title": title,
            "content": content,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.notes.append(note)
        return note


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "create")
    try:
        if action == "create":
            memory = AgenticZettelkastenMemory()
            result = memory.create_note(
                payload.get("title", "note"), payload.get("content", "")
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
