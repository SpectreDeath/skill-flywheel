"""MCP request handlers."""

from .metrics_handler import register_metrics_handlers
from .registry_handler import register_registry_handlers
from .skill_handler import register_skill_handlers


def register_all_handlers(mcp):
    """Register all MCP handlers with the server."""
    register_skill_handlers(mcp)
    register_registry_handlers(mcp)
    register_metrics_handlers(mcp)
