import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ApacheBeamWindowing:
    def __init__(self):
        self.windows = []

    def add_fixed_window(self, size_seconds: int):
        self.windows.append({"type": "fixed", "size": size_seconds})

    def add_sliding_window(self, size_seconds: int, period_seconds: int):
        self.windows.append(
            {"type": "sliding", "size": size_seconds, "period": period_seconds}
        )

    def add_session_window(self, gap_seconds: int):
        self.windows.append({"type": "session", "gap": gap_seconds})


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "window")

    try:
        if action == "window":
            windowing = ApacheBeamWindowing()
            windowing.add_fixed_window(60)
            windowing.add_sliding_window(300, 60)
            windowing.add_session_window(900)
            return {
                "result": {"windows": windowing.windows},
                "metadata": {"action": action},
            }
        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action},
            }
    except Exception as e:
        logger.error(f"Error in apache_beam_windowing: {e}")
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
