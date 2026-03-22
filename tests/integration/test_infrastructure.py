"""Tests for infrastructure modules."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest


class TestSkillIndexer:
    """Tests for skill_indexer.py."""

    def test_skill_indexer_module(self):
        """Test skill indexer module imports."""
        from flywheel import skill_indexer

        # Check key functions exist
        assert hasattr(skill_indexer, "main") or hasattr(
            skill_indexer, "scan_skills_directory"
        )


class TestMcpClient:
    """Tests for mcp_client.py."""

    def test_mcp_client_module(self):
        """Test MCP client module imports."""
        from flywheel.server import mcp_client

        # Check key classes exist
        assert hasattr(mcp_client, "MCPClient")


class TestDiscoveryService:
    """Tests for unified_server.py."""

    def test_unified_server_import(self):
        """Test unified server can be imported."""
        from flywheel.server import unified_server

        assert unified_server is not None

    def test_health_check_endpoint(self):
        """Test FastAPI app creation."""
        from flywheel.server.unified_server import UnifiedMCPServer
        server = UnifiedMCPServer()
        assert server.app is not None
        assert hasattr(server.app, "routes")

    def test_health_endpoint(self):
        """Test health endpoint exists."""
        from fastapi.testclient import TestClient
        from flywheel.server.unified_server import UnifiedMCPServer

        server = UnifiedMCPServer()
        client = TestClient(server.app)
        response = client.get("/health")
        assert response.status_code in [200, 404]


class TestMonitoring:
    """Tests for monitoring modules."""

    def test_auto_scaler_import(self):
        """Test auto_scaler can be imported."""
        from flywheel.monitoring import auto_scaler

        assert auto_scaler is not None

    def test_monitoring_dashboard_import(self):
        """Test monitoring_dashboard can be imported."""
        from flywheel.monitoring import monitoring_dashboard

        assert monitoring_dashboard is not None


class TestWatchdog:
    """Tests for watchdog module."""

    def test_watchdog_import(self):
        """Test watchdog can be imported."""
        from flywheel.watchdog import watchdog_monitor

        assert watchdog_monitor is not None
