"""
Secrets Manager Module

Provides a unified interface for managing secrets across different backends:
- Environment variables (development)
- AWS Secrets Manager (production)
- HashiCorp Vault (production)
"""

import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class SecretsBackend(ABC):
    """Abstract base class for secrets backends."""

    @abstractmethod
    def get_secret(self, name: str) -> Optional[str]:
        """Get a secret by name."""
        pass

    @abstractmethod
    def set_secret(self, name: str, value: str) -> None:
        """Set a secret by name."""
        pass

    @abstractmethod
    def delete_secret(self, name: str) -> None:
        """Delete a secret by name."""
        pass

    @abstractmethod
    def list_secrets(self) -> list[str]:
        """List all secret names."""
        pass


class EnvironmentSecretsBackend(SecretsBackend):
    """Secrets backend using environment variables."""

    def __init__(self, prefix: str = ""):
        self.prefix = prefix

    def get_secret(self, name: str) -> Optional[str]:
        key = f"{self.prefix}{name}" if self.prefix else name
        return os.environ.get(key)

    def set_secret(self, name: str, value: str) -> None:
        key = f"{self.prefix}{name}" if self.prefix else name
        os.environ[key] = value

    def delete_secret(self, name: str) -> None:
        key = f"{self.prefix}{name}" if self.prefix else name
        os.environ.pop(key, None)

    def list_secrets(self) -> list[str]:
        prefix = self.prefix if self.prefix else ""
        return [k for k in os.environ if k.startswith(prefix)]


class AWSSecretsManagerBackend(SecretsBackend):
    """AWS Secrets Manager backend."""

    def __init__(self, region_name: str = "us-east-1"):
        self.region_name = region_name
        self._client = None

    @property
    def client(self):
        """Lazy-load AWS client."""
        if self._client is None:
            try:
                import boto3

                self._client = boto3.client(
                    "secretsmanager", region_name=self.region_name
                )
            except ImportError:
                logger.warning("boto3 not installed, AWS secrets unavailable")
                return None
        return self._client

    def get_secret(self, name: str) -> Optional[str]:
        if self.client is None:
            return None
        try:
            response = self.client.get_secret_value(SecretId=name)
            return response.get("SecretString")
        except Exception as e:
            logger.error(f"Failed to get secret {name}: {e}")
            return None

    def set_secret(self, name: str, value: str) -> None:
        if self.client is None:
            return
        try:
            self.client.put_secret_value(SecretId=name, SecretString=value)
        except Exception as e:
            logger.error(f"Failed to set secret {name}: {e}")

    def delete_secret(self, name: str) -> None:
        if self.client is None:
            return
        try:
            self.client.delete_secret(SecretId=name, ForceDeleteWithoutRecovery=True)
        except Exception as e:
            logger.error(f"Failed to delete secret {name}: {e}")

    def list_secrets(self) -> list[str]:
        if self.client is None:
            return []
        try:
            response = self.client.list_secrets()
            return [s["Name"] for s in response.get("SecretList", [])]
        except Exception as e:
            logger.error(f"Failed to list secrets: {e}")
            return []


class VaultSecretsBackend(SecretsBackend):
    """HashiCorp Vault backend."""

    def __init__(
        self,
        url: str = "http://localhost:8200",
        token: Optional[str] = None,
        mount_point: str = "secret",
    ):
        self.url = url
        self.token = token or os.environ.get("VAULT_TOKEN")
        self.mount_point = mount_point
        self._client = None

    @property
    def client(self):
        """Lazy-load Vault client."""
        if self._client is None:
            try:
                import hvac

                self._client = hvac.Client(url=self.url, token=self.token)
            except ImportError:
                logger.warning("hvac not installed, Vault secrets unavailable")
                return None
        return self._client

    def get_secret(self, name: str) -> Optional[str]:
        if self.client is None:
            return None
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=name, mount_point=self.mount_point
            )
            return response.get("data", {}).get("data")
        except Exception as e:
            logger.error(f"Failed to get secret {name}: {e}")
            return None

    def set_secret(self, name: str, value: str) -> None:
        if self.client is None:
            return
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=name, secret={"value": value}, mount_point=self.mount_point
            )
        except Exception as e:
            logger.error(f"Failed to set secret {name}: {e}")

    def delete_secret(self, name: str) -> None:
        if self.client is None:
            return
        try:
            self.client.secrets.kv.v2.delete_metadata_and_all_versions(
                path=name, mount_point=self.mount_point
            )
        except Exception as e:
            logger.error(f"Failed to delete secret {name}: {e}")

    def list_secrets(self) -> list[str]:
        if self.client is None:
            return []
        try:
            response = self.client.secrets.kv.v2.list_secrets(
                mount_point=self.mount_point
            )
            return response.get("data", {}).get("keys", [])
        except Exception as e:
            logger.error(f"Failed to list secrets: {e}")
            return []


class SecretsManager:
    """Unified secrets manager with backend selection."""

    def __init__(self, backend: Optional[SecretsBackend] = None):
        if backend is not None:
            self.backend = backend
        else:
            backend_type = os.environ.get("SECRETS_BACKEND", "env")
            if backend_type == "aws":
                self.backend = AWSSecretsManagerBackend()
            elif backend_type == "vault":
                self.backend = VaultSecretsBackend()
            else:
                self.backend = EnvironmentSecretsBackend()

    def get(self, name: str, default: Optional[str] = None) -> Optional[str]:
        """Get a secret with optional default."""
        return self.backend.get_secret(name) or default

    def get_required(self, name: str) -> str:
        """Get a required secret, raises if not found."""
        value = self.backend.get_secret(name)
        if value is None:
            raise ValueError(f"Required secret {name} not found")
        return value

    def set(self, name: str, value: str) -> None:
        """Set a secret."""
        self.backend.set_secret(name, value)

    def delete(self, name: str) -> None:
        """Delete a secret."""
        self.backend.delete_secret(name)

    def list_all(self) -> list[str]:
        """List all secrets."""
        return self.backend.list_secrets()


secrets_manager = SecretsManager()
