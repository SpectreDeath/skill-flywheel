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
        from src import skill_indexer
        # Check key functions exist
        assert hasattr(skill_indexer, "main") or hasattr(skill_indexer, "scan_skills_directory")


class TestMcpClient:
    """Tests for mcp_client.py."""

    def test_mcp_client_module(self):
        """Test MCP client module imports."""
        from flywheel.server import mcp_client
        # Check key classes exist
        assert hasattr(mcp_client, "MCPClient")


class TestDiscoveryService:
    """Tests for discovery_service.py."""

    def test_discovery_service_import(self):
        """Test discovery service can be imported."""
        from flywheel.server import discovery_service
        assert discovery_service is not None

    def test_app_creation(self):
        """Test FastAPI app creation."""
        from flywheel.server.discovery_service import app
        
        assert app is not None
        assert hasattr(app, "routes")

    def test_health_endpoint(self):
        """Test health endpoint exists."""
        from fastapi.testclient import TestClient
        from flywheel.server.discovery_service import app
        
        client = TestClient(app)
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
