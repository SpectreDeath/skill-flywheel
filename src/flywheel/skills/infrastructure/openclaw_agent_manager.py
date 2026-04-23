"
OpenClaw Agent Management Skill

Provides capabilities for creating, configuring, and managing OpenClaw agents.
"

import asyncio
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List


class OpenClawAgentManager:
    "Manages OpenClaw agents."

    def __init__(self, openclaw_path: str | None = None):
        self.openclaw_path = (
            Path(openclaw_path) if openclaw_path else Path.home() / ".openclaw"
        )

    async def list_agents(self) -> List[Dict[str, Any]]:
        "List all configured agents."
        try:
            result = await self._run_command(["openclaw", "agent", "list", "--json"])
            if result.returncode == 0:
                return json.loads(result.stdout).get("agents", [])
            return []
        except FileNotFoundError:
            return [
                {
                    "error": "OpenClaw CLI not found. Install with: npm i -g @openclaw/cli"
                }
            ]

    async def create_agent(
        self,
        name: str,
        model: str = "gpt-4",
        description: str = ",
        system_prompt: str | None = None,
    ) -> Dict[str, Any]:
        "Create a new OpenClaw agent."
        cmd = ["openclaw", "agent", "create", name, "--model", model]

        if description:
            cmd.extend(["--description", description])

        try:
            result = await self._run_command(cmd, input_text=system_prompt)

            if result.returncode == 0:
                return {
                    "status": "success",
                    "agent": name,
                    "model": model,
                    "message": "Agent created successfully",
                }
            else:
                return {"status": "error", "message": result.stderr}
        except FileNotFoundError:
            return {"error": "OpenClaw CLI not found"}

    async def configure_agent(
        self, agent_name: str, settings: Dict[str, Any]
    ) -> Dict[str, Any]:
        "Configure an existing agent."
        config_path = self.openclaw_path / "agents" / agent_name / "config.json"

        if not config_path.exists():
            return {"error": f"Agent '{agent_name}' not found"}

        with open(config_path) as f:
            config = json.load(f)

        config.update(settings)

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        return {"status": "success", "config": config}

    async def start_agent(
        self, agent_name: str, platform: str = "cli", port: int = 18789
    ) -> Dict[str, Any]:
        "Start an OpenClaw agent."
        cmd = ["openclaw", "agent", "start", agent_name, "--platform", platform]

        try:
            result = await self._run_command(cmd)

            if result.returncode == 0:
                return {
                    "status": "success",
                    "agent": agent_name,
                    "platform": platform,
                    "port": port,
                }
            else:
                return {"status": "error", "message": result.stderr}
        except FileNotFoundError:
            return {"error": "OpenClaw CLI not found"}

    async def stop_agent(self, agent_name: str) -> Dict[str, Any]:
        "Stop a running agent."
        cmd = ["openclaw", "agent", "stop", agent_name]

        try:
            result = await self._run_command(cmd)

            if result.returncode == 0:
                return {"status": "success", "agent": agent_name}
            else:
                return {"status": "error", "message": result.stderr}
        except FileNotFoundError:
            return {"error": "OpenClaw CLI not found"}

    async def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        "Get status of an agent."
        cmd = ["openclaw", "agent", "status", agent_name]

        try:
            result = await self._run_command(cmd)

            if result.returncode == 0:
                return {
                    "status": "running",
                    "agent": agent_name,
                    "output": result.stdout,
                }
            else:
                return {"status": "stopped", "agent": agent_name}
        except FileNotFoundError:
            return {"error": "OpenClaw CLI not found"}

    async def delete_agent(
        self, agent_name: str, force: bool = False
    ) -> Dict[str, Any]:
        "Delete an agent."
        cmd = ["openclaw", "agent", "delete", agent_name]
        if force:
            cmd.append("--force")

        try:
            result = await self._run_command(cmd)

            if result.returncode == 0:
                return {"status": "success", "agent": agent_name}
            else:
                return {"status": "error", "message": result.stderr}
        except FileNotFoundError:
            return {"error": "OpenClaw CLI not found"}

    async def _run_command(
        self, cmd: List[str], input_text: str | None = None
    ) -> subprocess.CompletedProcess:
        "Run a command asynchronously."
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE if input_text else None,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate(
            input=input_text.encode() if input_text else None
        )

        return subprocess.CompletedProcess(
            args=cmd,
            returncode=process.returncode,
            stdout=stdout.decode(),
            stderr=stderr.decode(),
        )


MANIFEST = {
    "name": "openclaw_agent_manager",
    "description": "Manage OpenClaw AI agents - create, configure, start, stop, and monitor agents",
    "version": "1.0.0",
    "author": "Skill Flywheel",
    "capabilities": [
        "list_agents",
        "create_agent",
        "configure_agent",
        "start_agent",
        "stop_agent",
        "get_agent_status",
        "delete_agent",
    ],
    "requirements": {"openclaw_cli": "npm i -g @openclaw/cli"},
}


async def handle_request(action: str, params: Dict[str, Any]) -> Dict[str, Any]:
    "Handle incoming requests."
    manager = OpenClawAgentManager(params.get("openclaw_path"))

    handlers = {
        "list_agents": manager.list_agents,
        "create_agent": lambda: manager.create_agent(
            params.get("name"),
            params.get("model", "gpt-4"),
            params.get("description", "),
            params.get("system_prompt"),
        ),
        "configure_agent": lambda: manager.configure_agent(
            params.get("agent_name"), params.get("settings", {})
        ),
        "start_agent": lambda: manager.start_agent(
            params.get("agent_name"),
            params.get("platform", "cli"),
            params.get("port", 18789),
        ),
        "stop_agent": lambda: manager.stop_agent(params.get("agent_name")),
        "get_agent_status": lambda: manager.get_agent_status(params.get("agent_name")),
        "delete_agent": lambda: manager.delete_agent(
            params.get("agent_name"), params.get("force", False)
        ),
    }

    handler = handlers.get(action)
    if handler:
        return await handler()

    return {"error": f"Unknown action: {action}"}


if __name__ == "__main__":

    async def test():
        manager = OpenClawAgentManager()
        print("Testing list_agents...")
        result = await manager.list_agents()
        print(f"Result: {result}")

    asyncio.run(test())


def register_skill() -> dict:
    "Return skill metadata."
    return {
        "name": "openclaw_agent_manager",
        "domain": "infrastructure",
        "version": "1.0.0",
    }
