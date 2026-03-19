"""
OpenClaw Deployment Skill

Provides capabilities for deploying and managing OpenClaw across
different platforms including local, VPS, Docker, and cloud environments.
"""

import asyncio
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

DOCKER_COMPOSE_TEMPLATE = """version: '3.8'

services:
  openclaw:
    image: openclaw/openclaw:latest
    container_name: openclaw
    ports:
      - "18789:18789"
      - "3030:3030"
    volumes:
      - ./data:/home/openclaw/.openclaw
      - ./skills:/home/openclaw/.openclaw/skills
    environment:
      - MODEL_PROVIDER={model_provider}
      - MODEL_NAME={model_name}
      - API_KEY=${{API_KEY}}
    restart: unless-stopped

  # Optional: Add reverse proxy
  # nginx:
  #   image: nginx:latest
  #   ports:
  #     - "80:80"
  #     - "443:443"
  #   volumes:
  #     - ./nginx.conf:/etc/nginx/nginx.conf:ro
"""


class OpenClawDeployer:
    """Deploy and manage OpenClaw installations."""

    def __init__(self, deployment_path: Optional[str] = None):
        self.deployment_path = (
            Path(deployment_path) if deployment_path else Path.cwd() / "openclaw_deploy"
        )

    def check_requirements(self) -> Dict[str, Any]:
        """Check deployment requirements."""
        requirements = {
            "docker": self._check_command("docker"),
            "docker_compose": self._check_command("docker-compose")
            or self._check_command("docker"),
            "node": self._check_command("node"),
            "npm": self._check_command("npm"),
        }

        all_met = all(requirements.values())

        return {
            "requirements_met": all_met,
            "details": requirements,
            "missing": [k for k, v in requirements.items() if not v],
        }

    def _check_command(self, cmd: str) -> bool:
        """Check if a command is available."""
        result = subprocess.run(
            ["which", cmd] if os.name != "nt" else ["where", cmd], capture_output=True, check=False
        )
        return result.returncode == 0

    async def deploy_local(self, model: str = "gpt-4") -> Dict[str, Any]:
        """Deploy OpenClaw locally."""
        try:
            result = await self._run_command(["npm", "install", "-g", "@openclaw/cli"])

            if result.returncode != 0:
                return {
                    "error": "Failed to install OpenClaw CLI",
                    "details": result.stderr,
                }

            result = await self._run_command(["openclaw", "init"])

            if result.returncode != 0:
                return {
                    "error": "Failed to initialize OpenClaw",
                    "details": result.stderr,
                }

            env_file = self.deployment_path / ".env"
            env_content = f"""MODEL_PROVIDER=openai
MODEL_NAME={model}
OPENAI_API_KEY=$OPENAI_API_KEY
"""
            env_file.write_text(env_content)

            return {
                "status": "success",
                "message": "OpenClaw deployed locally",
                "next_steps": [
                    "Set your OPENAI_API_KEY in .env",
                    "Run 'openclaw agent start' to start",
                ],
            }
        except Exception as e:
            return {"error": str(e)}

    async def deploy_docker(
        self, model_provider: str = "openai", model_name: str = "gpt-4"
    ) -> Dict[str, Any]:
        """Deploy using Docker."""
        try:
            self.deployment_path.mkdir(parents=True, exist_ok=True)

            docker_compose = DOCKER_COMPOSE_TEMPLATE.format(
                model_provider=model_provider, model_name=model_name
            )

            (self.deployment_path / "docker-compose.yml").write_text(docker_compose)
            (self.deployment_path / ".env").write_text("API_KEY=your_api_key_here\n")

            result = await self._run_command(
                ["docker-compose", "up", "-d"], cwd=str(self.deployment_path)
            )

            if result.returncode != 0:
                return {
                    "error": "Failed to start Docker containers",
                    "details": result.stderr,
                }

            return {
                "status": "success",
                "message": "OpenClaw deployed with Docker",
                "ports": {"gateway": "18789", "web": "3030"},
                "files_created": ["docker-compose.yml", ".env"],
            }
        except Exception as e:
            return {"error": str(e)}

    async def deploy_vps(
        self, host: str, user: str = "root", key_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Deploy to a VPS."""
        try:
            ssh_cmd = ["ssh"]
            if key_path:
                ssh_cmd.extend(["-i", key_path])
            ssh_cmd.append(f"{user}@{host}")

            commands = [
                "curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -",
                "sudo apt-get install -y nodejs",
                "npm install -g @openclaw/cli",
                "openclaw init",
            ]

            for cmd in commands:
                full_cmd = ssh_cmd + [cmd]
                result = await self._run_command(full_cmd)

                if result.returncode != 0:
                    return {"error": f"Command failed: {cmd}", "details": result.stderr}

            return {
                "status": "success",
                "message": f"OpenClaw deployed to {user}@{host}",
                "next_steps": [
                    f"SSH to {host}",
                    "Configure .env with API keys",
                    "Run 'openclaw agent start'",
                ],
            }
        except Exception as e:
            return {"error": str(e)}

    async def get_status(self) -> Dict[str, Any]:
        """Get deployment status."""
        status = {
            "local": self._check_local_running(),
            "docker": self._check_docker_running(),
        }

        if self.deployment_path.exists():
            status["deployment_path"] = str(self.deployment_path)

        return status

    def _check_local_running(self) -> Dict[str, Any]:
        """Check if local OpenClaw is running."""
        result = subprocess.run(["pgrep", "-f", "openclaw"], capture_output=True, check=False)

        return {
            "running": result.returncode == 0,
            "pid": result.stdout.decode().strip() if result.returncode == 0 else None,
        }

    def _check_docker_running(self) -> Dict[str, Any]:
        """Check if Docker containers are running."""
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=openclaw", "--format", "{{.Names}}"],
            capture_output=True, check=False,
        )

        containers = result.stdout.decode().strip().split("\n") if result.stdout else []

        return {
            "running": len([c for c in containers if c]) > 0,
            "containers": [c for c in containers if c],
        }

    async def stop(self, mode: str = "all") -> Dict[str, Any]:
        """Stop OpenClaw."""
        if mode in ["local", "all"]:
            result = await self._run_command(["pkill", "-f", "openclaw"])

        if mode in ["docker", "all"]:
            result = await self._run_command(
                ["docker-compose", "down"], cwd=str(self.deployment_path)
            )

        return {"status": "success", "stopped": mode}

    async def restart(self, mode: str = "docker") -> Dict[str, Any]:
        """Restart OpenClaw."""
        if mode == "docker":
            result = await self._run_command(
                ["docker-compose", "restart"], cwd=str(self.deployment_path)
            )
        else:
            await self.stop(mode="local")
            result = await self.deploy_local()

        return {"status": "success", "restarted": mode}

    async def update(self) -> Dict[str, Any]:
        """Update OpenClaw to latest version."""
        result = await self._run_command(["npm", "update", "-g", "@openclaw/cli"])

        if result.returncode == 0:
            return {"status": "success", "message": "OpenClaw updated"}
        else:
            return {"error": "Update failed", "details": result.stderr}

    def generate_nginx_config(self, domain: str, ssl: bool = True) -> Dict[str, Any]:
        """Generate Nginx configuration."""
        config = f"""server {{
    listen 80;
    {"listen 443 ssl http2;" if ssl else ""}
    server_name {domain};
    
    location / {{
        proxy_pass http://localhost:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }}
"""
        if ssl:
            config += f"""
    ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;
"""

        config_path = self.deployment_path / "nginx.conf"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(config)

        return {"status": "success", "config_path": str(config_path)}

    async def _run_command(
        self, cmd: List[str], cwd: Optional[str] = None
    ) -> subprocess.CompletedProcess:
        """Run a command."""
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )

        stdout, stderr = await process.communicate()

        return subprocess.CompletedProcess(
            args=cmd,
            returncode=process.returncode,
            stdout=stdout.decode(),
            stderr=stderr.decode(),
        )


MANIFEST = {
    "name": "openclaw_deployer",
    "description": "Deploy and manage OpenClaw across local, Docker, VPS, and cloud environments",
    "version": "1.0.0",
    "author": "Skill Flywheel",
    "capabilities": [
        "check_requirements",
        "deploy_local",
        "deploy_docker",
        "deploy_vps",
        "get_status",
        "stop",
        "restart",
        "update",
        "generate_nginx_config",
    ],
    "requirements": {"docker": "Docker installed", "node": "Node.js 22+"},
}


async def handle_request(action: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle incoming requests."""
    deployer = OpenClawDeployer(params.get("deployment_path"))

    handlers = {
        "check_requirements": deployer.check_requirements,
        "deploy_local": lambda: deployer.deploy_local(params.get("model", "gpt-4")),
        "deploy_docker": lambda: deployer.deploy_docker(
            params.get("model_provider", "openai"), params.get("model_name", "gpt-4")
        ),
        "deploy_vps": lambda: deployer.deploy_vps(
            params.get("host"), params.get("user", "root"), params.get("key_path")
        ),
        "get_status": deployer.get_status,
        "stop": lambda: deployer.stop(params.get("mode", "all")),
        "restart": lambda: deployer.restart(params.get("mode", "docker")),
        "update": deployer.update,
        "generate_nginx_config": lambda: deployer.generate_nginx_config(
            params.get("domain"), params.get("ssl", True)
        ),
    }

    handler = handlers.get(action)
    if handler:
        return await handler()

    return {"error": f"Unknown action: {action}"}
