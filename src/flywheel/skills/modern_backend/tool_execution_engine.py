#!/usr/bin/env python3
"""
Tool Execution Engine

Manages tool discovery, filtering, permission checking, and execution
for agent harness systems. Pattern extracted from Claw Code's tools.py.

Features:
- Tool registry with metadata
- Permission context filtering
- Tool name search and discovery
- Mock execution shim for testing
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ToolDefinition:
    """Definition of a tool in the execution engine."""
    name: str
    responsibility: str
    source_hint: str
    status: str = "active"
    requires_permission: bool = False
    blocked_prefixes: List[str] = field(default_factory=list)


@dataclass
class ToolExecution:
    """Result of executing a tool."""
    name: str
    source_hint: str
    payload: str
    handled: bool
    message: str


@dataclass
class PermissionContext:
    """Context for permission checks on tools."""
    denied_tools: List[str] = field(default_factory=list)
    denied_prefixes: List[str] = field(default_factory=list)

    def blocks(self, tool_name: str) -> bool:
        """Check if a tool is blocked by this context."""
        name_lower = tool_name.lower()
        if name_lower in [d.lower() for d in self.denied_tools]:
            return True
        return any(
            name_lower.startswith(p.lower())
            for p in self.denied_prefixes
        )


# Global tool registry
_tool_registry: List[ToolDefinition] = []


def register_tool(name: str, responsibility: str, source_hint: str, **kwargs) -> None:
    """Register a tool in the global registry."""
    _tool_registry.append(ToolDefinition(
        name=name,
        responsibility=responsibility,
        source_hint=source_hint,
        **kwargs
    ))


def get_tool_registry() -> List[ToolDefinition]:
    """Get the current tool registry."""
    return list(_tool_registry)


def filter_tools_by_permission(
    tools: List[ToolDefinition],
    context: Optional[PermissionContext] = None
) -> List[ToolDefinition]:
    """Filter tools by permission context."""
    if context is None:
        return tools
    return [t for t in tools if not context.blocks(t.name)]


def find_tools(query: str, limit: int = 20) -> List[ToolDefinition]:
    """Find tools matching a query string."""
    needle = query.lower()
    matches = [
        t for t in _tool_registry
        if needle in t.name.lower() or needle in t.source_hint.lower()
    ]
    return matches[:limit]


def execute_tool_shim(
    name: str,
    payload: str = "",
    registry: Optional[List[ToolDefinition]] = None
) -> ToolExecution:
    """Execute a tool by name (shim implementation)."""
    tools = registry or _tool_registry
    needle = name.lower()

    for tool in tools:
        if tool.name.lower() == needle:
            return ToolExecution(
                name=tool.name,
                source_hint=tool.source_hint,
                payload=payload,
                handled=True,
                message=f"Tool '{tool.name}' executed with payload: {payload}"
            )

    return ToolExecution(
        name=name,
        source_hint="",
        payload=payload,
        handled=False,
        message=f"Unknown tool: {name}"
    )


def build_tool_inventory(
    simple_mode: bool = False,
    include_mcp: bool = True,
    permission_context: Optional[PermissionContext] = None
) -> List[ToolDefinition]:
    """Build filtered tool inventory."""
    tools = list(_tool_registry)

    if simple_mode:
        core_tools = {'BashTool', 'FileReadTool', 'FileEditTool'}
        tools = [t for t in tools if t.name in core_tools]

    if not include_mcp:
        tools = [
            t for t in tools
            if 'mcp' not in t.name.lower() and 'mcp' not in t.source_hint.lower()
        ]

    return filter_tools_by_permission(tools, permission_context)


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "build_inventory")

    if action == "build_inventory":
        simple_mode = payload.get("simple_mode", False)
        include_mcp = payload.get("include_mcp", True)
        denied_tools = payload.get("denied_tools", [])
        denied_prefixes = payload.get("denied_prefixes", [])

        ctx = PermissionContext(denied_tools, denied_prefixes)
        tools = build_tool_inventory(simple_mode, include_mcp, ctx)

        return {
            "result": {
                "tool_count": len(tools),
                "tools": [
                    {"name": t.name, "responsibility": t.responsibility, "source_hint": t.source_hint}
                    for t in tools
                ]
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }

    elif action == "find_tools":
        query = payload.get("query", "")
        limit = payload.get("limit", 20)

        if not query:
            tools = _tool_registry[:limit]
        else:
            tools = find_tools(query, limit)

        return {
            "result": {
                "query": query,
                "match_count": len(tools),
                "matches": [
                    {"name": t.name, "responsibility": t.responsibility, "source_hint": t.source_hint}
                    for t in tools
                ]
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }

    elif action == "execute":
        tool_name = payload.get("tool_name")
        tool_payload = payload.get("payload", "")

        if not tool_name:
            return {
                "result": {"status": "error", "error": "tool_name required"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        result = execute_tool_shim(tool_name, tool_payload)

        return {
            "result": {
                "handled": result.handled,
                "message": result.message,
                "tool_name": result.name,
                "source_hint": result.source_hint
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }

    elif action == "register_tools":
        tools_data = payload.get("tools", [])
        registered = []

        for t in tools_data:
            register_tool(
                name=t.get("name", ""),
                responsibility=t.get("responsibility", ""),
                source_hint=t.get("source_hint", "")
            )
            registered.append(t.get("name", ""))

        return {
            "result": {
                "registered_count": len(registered),
                "total_in_registry": len(_tool_registry),
                "tools": registered
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }

    else:
        return {
            "result": {"error": f"Unknown action: {action}"},
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }


def register_skill():
    """Return skill metadata."""
    return {
        "name": "tool-execution-engine",
        "description": "Tool discovery, filtering, permission checking, and execution engine for agent harness systems",
        "version": "1.0.0",
        "domain": "MODERN_BACKEND",
    }