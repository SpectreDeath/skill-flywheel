import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class MCPTestServer:
    def __init__(self):
        self.tests = []

    def add_test(self, name: str, test_type: str):
        self.tests.append({"name": name, "type": test_type})


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "test")
    try:
        if action == "test":
            server = MCPTestServer()
            server.add_test("basic_test", "unit")
            return {
                "result": {"tests": len(server.tests)},
                "metadata": {"action": action},
            }
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
