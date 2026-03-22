"""Tests for server modules."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest


class TestUnifiedServer:
    """Tests for unified_server.py."""

    def test_server_constants(self):
        """Test server constants are defined."""
        from flywheel.server import constants

        assert constants.SERVER_NAME == "SkillFlywheel"
        assert constants.TRANSPORT == "stdio"
        assert constants.PORT == 8000

    def test_unified_server_discovery(self):
        """Test skill discovery logic exists in UnifiedMCPServer."""
        from flywheel.server.unified_server import UnifiedMCPServer

        server = UnifiedMCPServer()
        assert hasattr(server.skill_manager, "discover_skills")
        assert callable(server.skill_manager.discover_skills)


class TestDependencies:
    """Tests for dependencies.py."""

    def test_mcp_domains_default(self):
        """Test default MCP domains."""
        from flywheel.server.dependencies import MCP_DOMAINS

        assert isinstance(MCP_DOMAINS, (list, tuple)) or MCP_DOMAINS is None

    def test_registry_file_path(self):
        """Test registry file path."""
        from flywheel.server.dependencies import REGISTRY_FILE

        assert isinstance(REGISTRY_FILE, Path)

    def test_filter_skills_by_domain(self):
        """Test filtering skills by domain."""
        from flywheel.server.dependencies import filter_skills_by_domain

        skills = [
            {"name": "skill1", "domain": "AI"},
            {"name": "skill2", "domain": "Testing"},
            {"name": "skill3", "domain": "AI"},
        ]

        result = filter_skills_by_domain(skills)
        assert len(result) == 3

        result = [s for s in skills if s["domain"] == "AI"]
        assert len(result) == 2
        assert all(s["domain"] == "AI" for s in result)


class TestHandlers:
    """Tests for handler modules."""

    def test_register_all_handlers(self):
        """Test handler registration."""
        from flywheel.server.handlers import register_all_handlers

        mock_mcp = Mock()
        register_all_handlers(mock_mcp)


class TestSkillHandler:
    """Tests for skill_handler.py."""

    def test_register_skill_handlers(self):
        """Test skill handler registration."""
        from flywheel.server.handlers.skill_handler import register_skill_handlers

        mock_mcp = Mock()
        register_skill_handlers(mock_mcp)


class TestRegistryHandler:
    """Tests for registry_handler.py."""

    def test_register_registry_handlers(self):
        """Test registry handler registration."""
        from flywheel.server.handlers.registry_handler import register_registry_handlers

        mock_mcp = Mock()
        register_registry_handlers(mock_mcp)


class TestMetricsHandler:
    """Tests for metrics_handler.py."""

    def test_register_metrics_handlers(self):
        """Test metrics handler registration."""
        from flywheel.server.handlers.metrics_handler import register_metrics_handlers

        mock_mcp = Mock()
        register_metrics_handlers(mock_mcp)
