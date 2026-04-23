#!/usr/bin/env python3
"""
Cost Tracker for LLM API Sessions

Tracks and reports:
- Token usage (input, output, cache read/write)
- USD cost per model
- API duration and wall time
- Code change metrics (lines added/removed)
- Session cost persistence

Pattern extracted from Claude Code's cost-tracker.ts.
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ModelUsage:
    """Usage tracking for a single model."""
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0
    web_search_requests: int = 0
    cost_usd: float = 0.0
    context_window: int = 0
    max_output_tokens: int = 0


@dataclass
class SessionCosts:
    """Accumulated costs for a session."""
    total_cost_usd: float = 0.0
    total_api_duration: float = 0.0
    total_wall_duration: float = 0.0
    total_tool_duration: float = 0.0
    total_lines_added: int = 0
    total_lines_removed: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cache_read_tokens: int = 0
    total_cache_write_tokens: int = 0
    total_web_search_requests: int = 0
    model_usage: Dict[str, ModelUsage] = field(default_factory=dict)
    session_id: str = ""


# Global cost state
_cost_state = SessionCosts()


def reset_cost_state() -> None:
    """Reset all cost tracking state."""
    global _cost_state
    _cost_state = SessionCosts()


def add_usage(
    model: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    cache_read: int = 0,
    cache_write: int = 0,
    web_searches: int = 0,
    cost_usd: float = 0.0
) -> None:
    """Add usage for a model."""
    if model not in _cost_state.model_usage:
        _cost_state.model_usage[model] = ModelUsage()

    usage = _cost_state.model_usage[model]
    usage.input_tokens += input_tokens
    usage.output_tokens += output_tokens
    usage.cache_read_input_tokens += cache_read
    usage.cache_creation_input_tokens += cache_write
    usage.web_search_requests += web_searches
    usage.cost_usd += cost_usd

    _cost_state.total_input_tokens += input_tokens
    _cost_state.total_output_tokens += output_tokens
    _cost_state.total_cache_read_tokens += cache_read
    _cost_state.total_cache_write_tokens += cache_write
    _cost_state.total_web_search_requests += web_searches
    _cost_state.total_cost_usd += cost_usd


def add_api_duration(seconds: float) -> None:
    """Add API call duration."""
    _cost_state.total_api_duration += seconds


def add_wall_duration(seconds: float) -> None:
    """Add wall clock duration."""
    _cost_state.total_wall_duration += seconds


def add_tool_duration(seconds: float) -> None:
    """Add tool execution duration."""
    _cost_state.total_tool_duration += seconds


def add_code_changes(lines_added: int = 0, lines_removed: int = 0) -> None:
    """Track code changes."""
    _cost_state.total_lines_added += lines_added
    _cost_state.total_lines_removed += lines_removed


def format_cost(cost: float, max_decimal: int = 4) -> str:
    """Format cost with appropriate precision."""
    if cost > 0.5:
        return f"${cost:.2f}"
    return f"${cost:.{max_decimal}f}"


def format_number(n: int) -> str:
    """Format number with commas."""
    return f"{n:,}"


def format_duration(seconds: float) -> str:
    """Format duration as human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}m {secs}s"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{hours}h {mins}m"


def get_cost_summary() -> Dict[str, Any]:
    """Get complete cost summary."""
    model_usages = {}
    for model, usage in _cost_state.model_usage.items():
        model_usages[model] = {
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "cache_read": usage.cache_read_input_tokens,
            "cache_write": usage.cache_creation_input_tokens,
            "web_searches": usage.web_search_requests,
            "cost_usd": round(usage.cost_usd, 6)
        }

    return {
        "total_cost_usd": round(_cost_state.total_cost_usd, 6),
        "total_api_duration": format_duration(_cost_state.total_api_duration),
        "total_wall_duration": format_duration(_cost_state.total_wall_duration),
        "total_tool_duration": format_duration(_cost_state.total_tool_duration),
        "lines_added": _cost_state.total_lines_added,
        "lines_removed": _cost_state.total_lines_removed,
        "total_input_tokens": _cost_state.total_input_tokens,
        "total_output_tokens": _cost_state.total_output_tokens,
        "total_cache_read": _cost_state.total_cache_read_tokens,
        "total_cache_write": _cost_state.total_cache_write_tokens,
        "model_usage": model_usages
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "summary")

    if action == "add_usage":
        add_usage(
            model=payload.get("model", "unknown"),
            input_tokens=payload.get("input_tokens", 0),
            output_tokens=payload.get("output_tokens", 0),
            cache_read=payload.get("cache_read", 0),
            cache_write=payload.get("cache_write", 0),
            web_searches=payload.get("web_searches", 0),
            cost_usd=payload.get("cost_usd", 0.0)
        )
        return {
            "result": {"status": "added"},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "add_duration":
        dtype = payload.get("type", "api")
        seconds = payload.get("seconds", 0.0)

        if dtype == "api":
            add_api_duration(seconds)
        elif dtype == "wall":
            add_wall_duration(seconds)
        elif dtype == "tool":
            add_tool_duration(seconds)

        return {
            "result": {"status": "added"},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "add_code_changes":
        add_code_changes(
            lines_added=payload.get("lines_added", 0),
            lines_removed=payload.get("lines_removed", 0)
        )
        return {
            "result": {"status": "added"},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "summary":
        return {
            "result": get_cost_summary(),
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "reset":
        reset_cost_state()
        return {
            "result": {"status": "reset"},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "format_cost":
        cost = payload.get("cost", 0.0)
        return {
            "result": {"formatted": format_cost(cost)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    else:
        return {
            "result": {"error": f"Unknown action: {action}"},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }


def register_skill():
    """Return skill metadata."""
    return {
        "name": "cost-tracker",
        "description": "Track and report LLM API session costs including token usage, USD cost per model, API duration, and code change metrics",
        "version": "1.0.0",
        "domain": "MODERN_BACKEND",
    }