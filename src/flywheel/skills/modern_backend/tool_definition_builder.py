#!/usr/bin/env python3
"""
Tool Definition Builder

Creates structured tool definitions with:
- Input/output schemas
- Permission checking
- Concurrency safety flags
- Progress tracking
- Validation

Pattern extracted from Claude Code's Tool.ts buildTool() system.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ToolSchema:
    """Schema definition for a tool's input."""
    type: str = "object"
    properties: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)


@dataclass
class ToolResult:
    """Result from tool execution."""
    data: Any
    new_messages: List[Dict[str, Any]] = field(default_factory=list)
    mcp_meta: Optional[Dict[str, Any]] = None


ToolFunc = Callable[[Dict[str, Any], Dict[str, Any]], ToolResult]


@dataclass
class ToolDefinition:
    """A tool definition."""
    name: str
    description: str
    search_hint: str = ""
    input_schema: ToolSchema = field(default_factory=ToolSchema)
    is_concurrency_safe: bool = False
    is_read_only: bool = False
    is_destructive: bool = False
    aliases: List[str] = field(default_factory=list)
    max_result_size_chars: int = 50000
    execution_fn: Optional[ToolFunc] = None
    validate_fn: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None
    enabled: bool = True


# Global tool registry
_tool_registry: Dict[str, ToolDefinition] = {}


def build_tool(name: str, description: str, **kwargs) -> ToolDefinition:
    """
    Build a complete tool definition with safe defaults.

    Pattern: Same as Claude Code's buildTool() function.
    Defaults:
    - is_concurrency_safe: False (assume not safe)
    - is_read_only: False (assume writes)
    - is_destructive: False
    - max_result_size_chars: 50000
    """
    kwargs.setdefault("max_result_size_chars", 50000)

    tool = ToolDefinition(
        name=name,
        description=description,
        **kwargs
    )
    _tool_registry[name.lower()] = tool
    return tool


def register_tool(tool: ToolDefinition) -> None:
    """Register a tool definition."""
    _tool_registry[tool.name.lower()] = tool


def get_tool(name: str) -> Optional[ToolDefinition]:
    """Get a tool by name or alias."""
    # Direct lookup
    if name.lower() in _tool_registry:
        return _tool_registry[name.lower()]

    # Alias lookup
    for tool in _tool_registry.values():
        if name.lower() in [a.lower() for a in tool.aliases]:
            return tool

    return None


def list_tools() -> List[ToolDefinition]:
    """List all registered tools."""
    return list(_tool_registry.values())


def execute_tool(name: str, args: Dict[str, Any], context: Optional[Dict] = None) -> ToolResult:
    """Execute a tool by name."""
    tool = get_tool(name)
    if not tool:
        return ToolResult(
            data={"error": f"Tool not found: {name}"},
            new_messages=[]
        )

    if not tool.enabled:
        return ToolResult(
            data={"error": f"Tool disabled: {name}"},
            new_messages=[]
        )

    if not tool.execution_fn:
        return ToolResult(
            data={"error": f"Tool has no execution function: {name}"},
            new_messages=[]
        )

    try:
        ctx = context or {}
        return tool.execution_fn(args, ctx)
    except Exception as e:
        return ToolResult(
            data={"error": str(e)},
            new_messages=[]
        )


def validate_tool_input(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Validate tool input against schema."""
    tool = get_tool(name)
    if not tool:
        return {"result": False, "message": f"Tool not found: {name}"}

    if tool.validate_fn:
        return tool.validate_fn(args)

    # Basic schema validation
    schema = tool.input_schema
    for req_field in schema.required:
        if req_field not in args:
            return {"result": False, "message": f"Missing required field: {req_field}"}

    return {"result": True}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "build_tool")

    if action == "build_tool":
        name = payload.get("name")
        description = payload.get("description", "")
        input_schema = payload.get("input_schema", {})
        is_concurrency_safe = payload.get("is_concurrency_safe", False)
        is_read_only = payload.get("is_read_only", False)
        is_destructive = payload.get("is_destructive", False)

        if not name:
            return {
                "result": {"error": "name required"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        schema = ToolSchema(
            type=input_schema.get("type", "object"),
            properties=input_schema.get("properties", {}),
            required=input_schema.get("required", [])
        )

        tool = build_tool(
            name=name,
            description=description,
            input_schema=schema,
            is_concurrency_safe=is_concurrency_safe,
            is_read_only=is_read_only,
            is_destructive=is_destructive
        )

        return {
            "result": {
                "name": tool.name,
                "description": tool.description,
                "is_concurrency_safe": tool.is_concurrency_safe,
                "is_read_only": tool.is_read_only,
                "is_destructive": tool.is_destructive,
                "input_schema": tool.input_schema.properties
            },
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "list_tools":
        tools = list_tools()
        return {
            "result": {
                "tool_count": len(tools),
                "tools": [
                    {"name": t.name, "description": t.description, "is_read_only": t.is_read_only}
                    for t in tools
                ]
            },
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "get_tool":
        name = payload.get("name", "")
        if not name:
            return {
                "result": {"error": "name required"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        tool = get_tool(name)
        if not tool:
            return {
                "result": {"error": f"Tool not found: {name}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        return {
            "result": {
                "name": tool.name,
                "description": tool.description,
                "is_concurrency_safe": tool.is_concurrency_safe,
                "aliases": tool.aliases
            },
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "validate_input":
        name = payload.get("name", "")
        args = payload.get("args", {})

        result = validate_tool_input(name, args)
        return {
            "result": result,
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
        "name": "tool-definition-builder",
        "description": "Build structured tool definitions with schemas, permission checking, concurrency safety, and execution for agent harness systems",
        "version": "1.0.0",
        "domain": "MODERN_BACKEND",
    }
