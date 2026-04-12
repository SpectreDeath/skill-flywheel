#!/usr/bin/env python3
"""Mock LLM for testing Primordial without a local model."""

from typing import Optional


class MockLLMClient:
    """Mock client that generates sample code for testing."""

    GENERATED_TEMPLATES = {
        "a-coding-guide-to-acp-systems": '''"""ACP Systems Implementation."""


class ACPSystem:
    """Adaptive Computation Proxy system for AI/ML workflows."""

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.components = []
        self.initialized = False

    def initialize(self) -> bool:
        """Initialize the ACP system."""
        try:
            self._setup_components()
            self.initialized = True
            return True
        except Exception:
            return False

    def _setup_components(self):
        """Set up required components."""
        # Core components
        from pathlib import Path
        
        # Validate environment
        required = ["python", "pip"]
        for cmd in required:
            import subprocess
            try:
                subprocess.run([cmd, "--version"], capture_output=True, check=True)
            except FileNotFoundError:
                raise RuntimeError(f"Required command not found: {cmd}")

    def execute(self, input_data: dict) -> dict:
        """Execute the ACP workflow."""
        if not self.initialized:
            raise RuntimeError("System not initialized")

        results = {
            "status": "completed",
            "output": input_data.get("data", []),
            "metrics": {
                "processing_time": 0.0,
                "components_used": len(self.components)
            }
        }
        return results

    def cleanup(self):
        """Clean up resources."""
        self.initialized = False
        self.components.clear()


def create_acp_system(config: Optional[dict] = None) -> ACPSystem:
    """Factory function to create ACP system."""
    return ACPSystem(config)


if __name__ == "__main__":
    system = create_acp_system()
    if system.initialize():
        result = system.execute({"data": [1, 2, 3]})
        print(f"Result: {result}")
''',
    }

    def __init__(self, model: str = "mock", base_url: str = "", **kwargs):
        self.model = model
        self.base_url = base_url
        self._call_count = 0

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """Generate mock response based on prompt content."""
        self._call_count += 1

        # Extract skill name from prompt
        import re

        name_match = re.search(r"## Name\s*\n(\w+)", prompt)
        skill_name = name_match.group(1) if name_match else "unknown"

        # Return generated template or default
        if skill_name in self.GENERATED_TEMPLATES:
            return f"```python\n{self.GENERATED_TEMPLATES[skill_name]}\n```"

        # Default generated code
        return f'''```python
# Generated from skill: {skill_name}

class GeneratedSkill:
    """Auto-generated skill implementation."""

    def __init__(self):
        self.name = "{skill_name}"
        self.version = "1.0.0"

    def execute(self, input_data):
        """Execute the skill logic."""
        return {{"status": "success", "skill": self.name, "data": input_data}}

def main():
    skill = GeneratedSkill()
    return skill.execute({{"test": True}})

if __name__ == "__main__":
    main()
```'''


def get_mock_client():
    """Get a mock LLM client."""
    return MockLLMClient
