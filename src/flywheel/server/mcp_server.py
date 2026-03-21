"""
Modular Skill Flywheel MCP Server - Bootstrap Entry Point

This is the main entry point for the Skill Flywheel MCP server.
It initializes the FastMCP server and registers all handler modules.

The server is organized into modular components:
- handlers/: Skill, registry, and metrics MCP handlers
- dependencies.py: Shared dependencies and configuration
"""

import logging
import os

from mcp.server.fastmcp import FastMCP

from flywheel.server.dependencies import (
    MCP_DOMAINS,
    REGISTRY_FILE,
    filter_skills_by_domain,
)
from flywheel.server.handlers import register_all_handlers

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

SERVER_NAME = os.environ.get("MCP_SERVER_NAME", "SkillFlywheel")
TRANSPORT = os.environ.get("MCP_TRANSPORT", "stdio")
PORT = int(os.environ.get("PORT", 8000))


def create_server() -> FastMCP:
    """
    Create and configure the FastMCP server.

    Returns:
        Configured FastMCP instance
    """
    mcp = FastMCP(SERVER_NAME)
    register_all_handlers(mcp)
    return mcp


def register_existing_skills(mcp: FastMCP):
    """
    Register individual skill tools from the registry.

    For each skill in the registry, creates a dynamic tool
    that can execute that specific skill.

    Args:
        mcp: The FastMCP server instance
    """
    import json

    if not REGISTRY_FILE.exists():
        logger.warning(f"Registry file not found at {REGISTRY_FILE}")
        return

    try:
        with open(REGISTRY_FILE, encoding="utf-8") as f:
            registry = json.load(f)

        skills = filter_skills_by_domain(registry)
        registered = 0

        for skill in skills:
            domain = skill.get("domain", "General")
            if MCP_DOMAINS and domain not in MCP_DOMAINS:
                continue

            skill_id = skill["name"].lower().replace("-", "_")
            description = (
                skill.get("description")
                or skill.get("purpose")
                or f"Execute {skill_id}"
            )

            root_dir = REGISTRY_FILE.parent
            skill_file = root_dir / skill["path"]

            def make_tool(path, sid):
                async def tool(ctx, request: str = ""):
                    try:
                        with open(path, encoding="utf-8") as f:
                            content = f.read()
                        return f"SKILL: {sid}\n\n{content}\n\n---\nRequest: {request}"
                    except Exception as e:
                        return f"Error: {e}"

                tool.__name__ = f"skill_{sid}"
                return tool

            tool_func = make_tool(skill_file, skill_id)
            mcp.tool(name=f"skill_{skill_id}", description=description)(tool_func)
            registered += 1

        logger.info(
            f"Registered {registered} skills from domains: {MCP_DOMAINS or 'All'}"
        )

    except Exception as e:
        logger.error(f"Error registering skills: {e}")


def main():
    """Main entry point for the MCP server."""
    logger.info(f"Starting {SERVER_NAME} MCP Server")
    logger.info(f"Registry: {REGISTRY_FILE}")
    logger.info(f"Transport: {TRANSPORT}")

    mcp = create_server()
    register_existing_skills(mcp)

    logger.info(f"Server ready, starting on {TRANSPORT}")

    if TRANSPORT == "http":
        import uvicorn

        uvicorn.run(mcp.sse_app, host="0.0.0.0", port=PORT)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
