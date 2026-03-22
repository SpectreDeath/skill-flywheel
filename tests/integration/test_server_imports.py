"""Tests for server dependencies module."""

import pytest


class TestDependencies:
    """Tests for dependencies.py."""

    def test_mcp_domains_default(self):
        """Test default MCP domains."""
        from flywheel.server.dependencies import MCP_DOMAINS

        # Just check it's either a list/tuple or None
        assert isinstance(MCP_DOMAINS, (list, tuple)) or MCP_DOMAINS is None

    def test_registry_file_path(self):
        """Test registry file path."""
        from flywheel.server.dependencies import REGISTRY_FILE
        from pathlib import Path

        assert isinstance(REGISTRY_FILE, Path)

    def test_filter_skills_by_domain_function(self):
        """Test filter_skills_by_domain function exists."""
        from flywheel.server.dependencies import filter_skills_by_domain

        assert callable(filter_skills_by_domain)


class TestHandlers:
    """Tests for handler modules."""

    def test_skill_handler_import(self):
        """Test skill handler module can be imported."""
        from flywheel.server.handlers import skill_handler

        assert skill_handler is not None

    def test_registry_handler_import(self):
        """Test registry handler module can be imported."""
        from flywheel.server.handlers import registry_handler

        assert registry_handler is not None

    def test_metrics_handler_import(self):
        """Test metrics handler module can be imported."""
        from flywheel.server.handlers import metrics_handler

        assert metrics_handler is not None


class TestMcpClient:
    """Tests for MCP client module."""

    def test_mcp_client_class_exists(self):
        """Test MCPClient class exists."""
        from flywheel.server.mcp_client import MCPClient

        assert MCPClient is not None


class TestSkillIndexer:
    """Tests for skill indexer module."""

    def test_skill_indexer_import(self):
        """Test skill indexer can be imported."""
        from flywheel import skill_indexer

        assert skill_indexer is not None


class TestDiscoveryService:
    """Tests for discovery service module."""

    def test_discovery_service_import(self):
        """Test discovery service can be imported."""
        from flywheel.server import discovery_service

        assert discovery_service is not None

    def test_app_exists(self):
        """Test FastAPI app exists."""
        from flywheel.server.discovery_service import app

        assert app is not None
        assert hasattr(app, "routes")


class TestMcpServer:
    """Tests for MCP server module."""

    def test_mcp_server_import(self):
        """Test MCP server can be imported."""
        from flywheel.server import mcp_server

        assert mcp_server is not None

    def test_server_constants(self):
        """Test server constants exist."""
        from flywheel.server.mcp_server import SERVER_NAME, TRANSPORT, PORT

        assert SERVER_NAME == "SkillFlywheel"
        assert TRANSPORT == "stdio"
        assert PORT == 8000
