"""
Local LLM Client for Primordial.
Supports: Ollama, LM Studio, or any compatible local LLM API.
"""

import os
from typing import Optional


class LocalLLMClient:
    """Client for local LLM models."""

    def __init__(
        self,
        model: str = "codellama",
        base_url: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ):
        self.model = model
        self.base_url = (
            base_url or os.environ.get("LLM_BASE_URL", "http://localhost:11434")
        ).rstrip("/")
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, prompt: str, system: str | None = None) -> str:
        """Generate a response using the local model."""

if __name__ == "__main__":
    import requests

            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "stream": False,
            }

            if system:
                payload["system"] = system

            # Try Ollama format first
            try:
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=120,
                )
                response.raise_for_status()
                return response.json().get("response", "")
            except requests.exceptions.RequestException:
                pass

            # Try OpenAI-compatible format
            try:
                response = requests.post(
                    f"{self.base_url}/v1/completions",
                    json=payload,
                    timeout=120,
                )
                response.raise_for_status()
                return response.json().get("choices", [{}])[0].get("text", "")
            except requests.exceptions.RequestException:
                pass

            raise RuntimeError(f"Failed to connect to local LLM at {self.base_url}")