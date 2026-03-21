from __future__ import annotations

import os
from typing import Any, Dict, Optional


class LocalLLMClient:
    """Client for local LLM models (Ollama, LM Studio, etc.)."""

    def __init__(
        self,
        model: str = "llama2",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, prompt: str) -> str:
        """Generate a response using the local model."""
        try:
            import requests

            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "stream": False,
                },
                timeout=120,
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except ImportError:
            raise RuntimeError(
                "requests library required for LocalLLMClient. Install with: pip install requests"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to connect to local LLM: {e}")

    def complete(self, prompt: str) -> str:
        """Alias for generate."""
        return self.generate(prompt)


class OllamaClient(LocalLLMClient):
    """Client specifically for Ollama."""

    def __init__(
        self,
        model: str = "llama2",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
    ):
        super().__init__(
            model=model,
            base_url=base_url,
            temperature=temperature,
        )


class LMStudioClient(LocalLLMClient):
    """Client for LM Studio local models."""

    def __init__(
        self,
        model: str = "local-model",
        base_url: str = "http://localhost:1234/v1",
        temperature: float = 0.7,
    ):
        super().__init__(
            model=model,
            base_url=base_url,
            temperature=temperature,
        )


def create_local_llm_client(
    provider: str = "ollama",
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> LocalLLMClient:
    """Factory function to create a local LLM client.

    Args:
        provider: "ollama", "lmstudio", or "local"
        model: Model name (defaults to environment LLM_MODEL or "llama2")
        base_url: Base URL (defaults to environment LLM_BASE_URL)
        api_key: API key if required (for some local servers)

    Returns:
        LocalLLMClient instance
    """
    model = model or os.environ.get("LLM_MODEL", "llama2")
    base_url = base_url or os.environ.get("LLM_BASE_URL", "http://localhost:11434")

    if provider == "ollama":
        return OllamaClient(model=model, base_url=base_url)
    elif provider == "lmstudio":
        return LMStudioClient(model=model, base_url=base_url)
    else:
        return LocalLLMClient(model=model, base_url=base_url)
