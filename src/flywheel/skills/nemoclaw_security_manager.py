"""
NemOClaw Security Configuration Skill

Provides capabilities for configuring and managing NVIDIA NemOClaw
security features including OpenShell guardrails and privacy controls.
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_POLICY = {
    "version": "1.0",
    "rules": [
        {
            "name": "block_data_exfiltration",
            "action": "deny",
            "condition": {
                "type": "regex",
                "pattern": "(api_key|password|secret|token):\\s*\\S+",
            },
        },
        {
            "name": "allow_file_reads",
            "action": "allow",
            "condition": {"type": "operation", "value": "file:read"},
        },
        {
            "name": "allow_api_calls",
            "action": "allow",
            "condition": {"type": "operation", "value": "api:call"},
        },
    ],
    "guardrails": {
        "max_file_size_mb": 100,
        "max_execution_time_seconds": 300,
        "allowed_domains": [],
        "blocked_domains": [],
    },
}


class NemOClawSecurityManager:
    """Manage NemOClaw security and privacy settings."""

    def __init__(self, config_path: str | None = None):
        self.config_path = (
            Path(config_path) if config_path else Path.home() / ".nemoclaw" / "config"
        )

    def get_status(self) -> Dict[str, Any]:
        """Get NemOClaw status."""
        return {
            "status": "checking",
            "openclaw_installed": self._check_openclaw(),
            "nemoclaw_installed": self._check_nemoclaw(),
            "openshell_installed": self._check_openshell(),
        }

    def _check_openclaw(self) -> bool:
        """Check if OpenClaw is installed."""
        result = subprocess.run(
            ["openclaw", "--version"], capture_output=True, text=True, check=False
        )
        return result.returncode == 0

    def _check_nemoclaw(self) -> bool:
        """Check if NemOClaw is installed."""
        result = subprocess.run(["nemo", "--version"], capture_output=True, text=True, check=False)
        return result.returncode == 0

    def _check_openshell(self) -> bool:
        """Check if OpenShell is installed."""
        result = subprocess.run(
            ["openshell", "--version"], capture_output=True, text=True, check=False
        )
        return result.returncode == 0

    async def install(self, model: str = "nemotron") -> Dict[str, Any]:
        """Install NemOClaw with security features."""
        try:
            result = subprocess.run(
                ["nemo", "install", "--model", model],
                capture_output=True,
                text=True,
                timeout=300, check=False,
            )

            if result.returncode == 0:
                return {
                    "status": "success",
                    "message": "NemOClaw installed successfully",
                    "model": model,
                }
            else:
                return {"status": "error", "message": result.stderr}
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Installation timeout"}
        except FileNotFoundError:
            return {"status": "error", "message": "nemo CLI not found"}

    def create_policy(
        self,
        name: str,
        rules: List[Dict[str, Any]] | None = None,
        guardrails: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Create a security policy."""
        policy = {
            "version": "1.0",
            "name": name,
            "rules": rules or DEFAULT_POLICY["rules"],
            "guardrails": guardrails or DEFAULT_POLICY["guardrails"],
        }

        policy_dir = self.config_path / "policies"
        policy_dir.mkdir(parents=True, exist_ok=True)

        policy_file = policy_dir / f"{name}.json"

        try:
            policy_file.write_text(json.dumps(policy, indent=2))
            return {"status": "success", "policy": name, "path": str(policy_file)}
        except Exception as e:
            return {"error": str(e)}

    def list_policies(self) -> List[Dict[str, Any]]:
        """List all security policies."""
        policy_dir = self.config_path / "policies"

        if not policy_dir.exists():
            return []

        policies = []
        for file in policy_dir.glob("*.json"):
            try:
                policy = json.loads(file.read_text())
                policies.append(
                    {
                        "name": policy.get("name", file.stem),
                        "version": policy.get("version", "unknown"),
                        "rules_count": len(policy.get("rules", [])),
                        "path": str(file),
                    }
                )
            except json.JSONDecodeError:
                policies.append({"name": file.stem, "error": "Invalid JSON"})

        return policies

    def get_policy(self, name: str) -> Dict[str, Any]:
        """Get a specific policy."""
        policy_file = self.config_path / "policies" / f"{name}.json"

        if not policy_file.exists():
            return {"error": f"Policy '{name}' not found"}

        try:
            return json.loads(policy_file.read_text())
        except json.JSONDecodeError as e:
            return {"error": f"Invalid policy: {e}"}

    def update_policy(self, name: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing policy."""
        policy_file = self.config_path / "policies" / f"{name}.json"

        if not policy_file.exists():
            return {"error": f"Policy '{name}' not found"}

        try:
            policy = json.loads(policy_file.read_text())
            policy.update(updates)
            policy_file.write_text(json.dumps(policy, indent=2))

            return {"status": "success", "policy": policy}
        except Exception as e:
            return {"error": str(e)}

    def apply_policy(self, policy_name: str) -> Dict[str, Any]:
        """Apply a policy to the agent."""
        policy_file = self.config_path / "policies" / f"{policy_name}.json"

        if not policy_file.exists():
            return {"error": f"Policy '{policy_name}' not found"}

        try:
            result = subprocess.run(
                ["nemo", "policy", "apply", policy_name], capture_output=True, text=True, check=False
            )

            if result.returncode == 0:
                return {
                    "status": "success",
                    "policy": policy_name,
                    "message": "Policy applied",
                }
            else:
                return {"error": result.stderr}
        except FileNotFoundError:
            return {"error": "nemo CLI not found"}

    def configure_guardrails(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Configure guardrail settings."""
        guardrail_file = self.config_path / "guardrails.json"

        guardrail_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            existing = {}
            if guardrail_file.exists():
                existing = json.loads(guardrail_file.read_text())

            existing.update(settings)
            guardrail_file.write_text(json.dumps(existing, indent=2))

            return {"status": "success", "guardrails": existing}
        except Exception as e:
            return {"error": str(e)}

    def get_guardrails(self) -> Dict[str, Any]:
        """Get current guardrail settings."""
        guardrail_file = self.config_path / "guardrails.json"

        if not guardrail_file.exists():
            return DEFAULT_POLICY["guardrails"]

        try:
            return json.loads(guardrail_file.read_text())
        except json.JSONDecodeError:
            return DEFAULT_POLICY["guardrails"]

    def set_allowed_domains(self, domains: List[str]) -> Dict[str, Any]:
        """Set allowed domains for API calls."""
        return self.configure_guardrails({"allowed_domains": domains})

    def set_blocked_domains(self, domains: List[str]) -> Dict[str, Any]:
        """Set blocked domains."""
        return self.configure_guardrails({"blocked_domains": domains})

    def enable_privacy_router(self, enabled: bool = True) -> Dict[str, Any]:
        """Enable or disable privacy router."""
        return self.configure_guardrails({"privacy_router_enabled": enabled})

    def get_security_audit(self) -> Dict[str, Any]:
        """Get security audit log."""
        audit_file = self.config_path / "audit.log"

        if not audit_file.exists():
            return {"events": []}

        try:
            content = audit_file.read_text()
            events = [json.loads(line) for line in content.strip().split("\n") if line]

            return {"total_events": len(events), "recent_events": events[-10:]}
        except Exception as e:
            return {"error": str(e)}


MANIFEST = {
    "name": "nemoclaw_security_manager",
    "description": "Configure and manage NVIDIA NemOClaw security features and OpenShell guardrails",
    "version": "1.0.0",
    "author": "Skill Flywheel",
    "capabilities": [
        "get_status",
        "install",
        "create_policy",
        "list_policies",
        "get_policy",
        "update_policy",
        "apply_policy",
        "configure_guardrails",
        "get_guardrails",
        "set_allowed_domains",
        "set_blocked_domains",
        "enable_privacy_router",
        "get_security_audit",
    ],
    "requirements": {"nemo_cli": "NVIDIA nemo CLI", "openclaw": "OpenClaw installed"},
}


async def handle_request(action: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle incoming requests."""

if __name__ == "__main__":
    manager = NemOClawSecurityManager(params.get("config_path"))

        handlers = {
            "get_status": manager.get_status,
            "install": lambda: manager.install(params.get("model", "nemotron")),
            "create_policy": lambda: manager.create_policy(
                params.get("name"), params.get("rules"), params.get("guardrails")
            ),
            "list_policies": manager.list_policies,
            "get_policy": lambda: manager.get_policy(params.get("name")),
            "update_policy": lambda: manager.update_policy(
                params.get("name"), params.get("updates", {})
            ),
            "apply_policy": lambda: manager.apply_policy(params.get("policy_name")),
            "configure_guardrails": lambda: manager.configure_guardrails(
                params.get("settings", {})
            ),
            "get_guardrails": manager.get_guardrails,
            "set_allowed_domains": lambda: manager.set_allowed_domains(
                params.get("domains", [])
            ),
            "set_blocked_domains": lambda: manager.set_blocked_domains(
                params.get("domains", [])
            ),
            "enable_privacy_router": lambda: manager.enable_privacy_router(
                params.get("enabled", True)
            ),
            "get_security_audit": manager.get_security_audit,
        }

        handler = handlers.get(action)
        if handler:
            return await handler() if action in ["install"] else handler()

        return {"error": f"Unknown action: {action}"}