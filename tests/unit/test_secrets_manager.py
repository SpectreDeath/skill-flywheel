"""Tests for secrets manager module."""

import os
from unittest.mock import Mock, patch

import pytest


class TestEnvironmentSecretsBackend:
    """Tests for environment secrets backend."""

    def test_get_secret_exists(self):
        """Test getting an existing secret."""
        os.environ["TEST_SECRET"] = "test_value"

        from flywheel.core.secrets_manager import EnvironmentSecretsBackend

        backend = EnvironmentSecretsBackend()

        result = backend.get_secret("TEST_SECRET")
        assert result == "test_value"

        del os.environ["TEST_SECRET"]

    def test_get_secret_not_exists(self):
        """Test getting a non-existent secret."""
        from flywheel.core.secrets_manager import EnvironmentSecretsBackend

        backend = EnvironmentSecretsBackend()

        result = backend.get_secret("NONEXISTENT")
        assert result is None

    def test_set_secret(self):
        """Test setting a secret."""
        from flywheel.core.secrets_manager import EnvironmentSecretsBackend

        backend = EnvironmentSecretsBackend()

        backend.set_secret("NEW_SECRET", "new_value")
        assert os.environ.get("NEW_SECRET") == "new_value"

        del os.environ["NEW_SECRET"]

    def test_delete_secret(self):
        """Test deleting a secret."""
        os.environ["TO_DELETE"] = "delete_me"

        from flywheel.core.secrets_manager import EnvironmentSecretsBackend

        backend = EnvironmentSecretsBackend()

        backend.delete_secret("TO_DELETE")
        assert "TO_DELETE" not in os.environ

    def test_list_secrets(self):
        """Test listing secrets with prefix."""
        os.environ["PREFIX_TEST1"] = "val1"
        os.environ["PREFIX_TEST2"] = "val2"
        os.environ["OTHER"] = "val3"

        from flywheel.core.secrets_manager import EnvironmentSecretsBackend

        backend = EnvironmentSecretsBackend(prefix="PREFIX_")

        result = backend.list_secrets()
        assert "PREFIX_TEST1" in result
        assert "PREFIX_TEST2" in result
        assert "OTHER" not in result

        del os.environ["PREFIX_TEST1"]
        del os.environ["PREFIX_TEST2"]
        del os.environ["OTHER"]


class TestSecretsManager:
    """Tests for SecretsManager class."""

    def test_get_with_default(self):
        """Test getting a secret with default value."""
        from flywheel.core.secrets_manager import SecretsManager

        with patch.object(SecretsManager, "__init__", lambda x, y=None: None):
            manager = SecretsManager.__new__(SecretsManager)
            manager.backend = Mock()
            manager.backend.get_secret.return_value = None

            result = manager.get("TEST", "default_value")
            assert result == "default_value"

    def test_get_required_found(self):
        """Test getting a required secret that exists."""
        from flywheel.core.secrets_manager import SecretsManager

        with patch.object(SecretsManager, "__init__", lambda x, y=None: None):
            manager = SecretsManager.__new__(SecretsManager)
            manager.backend = Mock()
            manager.backend.get_secret.return_value = "secret_value"

            result = manager.get_required("TEST")
            assert result == "secret_value"

    def test_get_required_not_found(self):
        """Test getting a required secret that doesn't exist."""
        from flywheel.core.secrets_manager import SecretsManager

        with patch.object(SecretsManager, "__init__", lambda x, y=None: None):
            manager = SecretsManager.__new__(SecretsManager)
            manager.backend = Mock()
            manager.backend.get_secret.return_value = None

            with pytest.raises(ValueError, match="Required secret TEST not found"):
                manager.get_required("TEST")
