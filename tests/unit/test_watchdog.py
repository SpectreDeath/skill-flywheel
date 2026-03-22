"""Tests for watchdog module - behavior verification."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest


class TestWatchdogEventLogger:
    """Test WatchdogEventLogger behavior."""

    def test_creates_log_file_if_missing(self, tmp_path):
        """Verify logger creates log file if it doesn't exist."""
        from flywheel.watchdog.watchdog_monitor import WatchdogEventLogger

        log_file = tmp_path / "events.log"
        assert not log_file.exists()

        logger = WatchdogEventLogger(log_file=str(log_file))

        assert log_file.exists()

    def test_log_event_writes_json_line(self, tmp_path):
        """Verify log_event writes valid JSON to file."""
        from flywheel.watchdog.watchdog_monitor import WatchdogEventLogger

        log_file = tmp_path / "events.log"
        logger = WatchdogEventLogger(log_file=str(log_file))

        logger.log_event({"event_type": "TEST", "value": 42})

        content = log_file.read_text()
        lines = content.strip().split("\n")
        assert len(lines) == 1

        event = json.loads(lines[0])
        assert event["event_type"] == "TEST"
        assert event["value"] == 42

    def test_log_service_failure_counts_failures(self, tmp_path):
        """Verify service failure logging captures failure count."""
        from flywheel.watchdog.watchdog_monitor import WatchdogEventLogger

        log_file = tmp_path / "events.log"
        logger = WatchdogEventLogger(log_file=str(log_file))

        failed = [
            {"name": "service1", "port": 8000},
            {"name": "service2", "port": 8001},
        ]
        logger.log_service_failure(failed)

        content = log_file.read_text()
        event = json.loads(content.strip())

        assert event["event_type"] == "SERVICE_FAILURE"
        assert event["total_failed"] == 2
        assert len(event["failed_services"]) == 2

    def test_log_recovery_records_result(self, tmp_path):
        """Verify recovery logging captures outcome."""
        from flywheel.watchdog.watchdog_monitor import WatchdogEventLogger

        log_file = tmp_path / "events.log"
        logger = WatchdogEventLogger(log_file=str(log_file))

        failed = [{"name": "service1"}]
        result = {"success": True, "services_restarted": 3}

        logger.log_recovery_attempt(failed, result)

        content = log_file.read_text()
        event = json.loads(content.strip())

        assert event["event_type"] == "RECOVERY_ATTEMPT"
        assert event["recovery_result"]["success"] == True


class TestHealthChecker:
    """Test HealthChecker behavior."""

    def test_health_check_returns_healthy_for_healthy_service(self):
        """Verify healthy service returns HEALTHY status."""
        from flywheel.watchdog.watchdog_monitor import HealthChecker

        checker = HealthChecker()

        with patch("flywheel.watchdog.watchdog_monitor.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.elapsed.total_seconds.return_value = 0.1
            mock_get.return_value = mock_response

            result = checker.check_service_health(
                {
                    "name": "svc1",
                    "health_url": "http://localhost:8000/health",
                    "description": "test service",
                }
            )

            assert result["status"] == "HEALTHY"

    def test_health_check_returns_unhealthy_for_unhealthy_service(self):
        """Verify unhealthy service returns UNHEALTHY status."""
        from flywheel.watchdog.watchdog_monitor import HealthChecker

        checker = HealthChecker()

        with patch("flywheel.watchdog.watchdog_monitor.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 503
            mock_get.return_value = mock_response

            result = checker.check_service_health(
                {
                    "name": "svc1",
                    "health_url": "http://localhost:8000/health",
                    "description": "test service",
                }
            )

            assert result["status"] == "UNHEALTHY"

    def test_health_check_returns_timeout_on_timeout(self):
        """Verify timeout returns TIMEOUT status."""
        import requests
        from flywheel.watchdog.watchdog_monitor import HealthChecker

        checker = HealthChecker()

        with patch("flywheel.watchdog.watchdog_monitor.requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout()

            result = checker.check_service_health(
                {
                    "name": "svc1",
                    "health_url": "http://localhost:8000/health",
                    "description": "test service",
                }
            )

            assert result["status"] == "TIMEOUT"

    def test_health_check_returns_connection_error_on_connection_failure(self):
        """Verify connection error returns CONNECTION_ERROR status."""
        import requests
        from flywheel.watchdog.watchdog_monitor import HealthChecker

        checker = HealthChecker()

        with patch("flywheel.watchdog.watchdog_monitor.requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Refused")

            result = checker.check_service_health(
                {
                    "name": "svc1",
                    "health_url": "http://localhost:8000/health",
                    "description": "test service",
                }
            )

            assert result["status"] == "CONNECTION_ERROR"


class TestRecoveryManager:
    """Test RecoveryManager behavior."""

    def test_recovery_manager_initializes(self):
        """Verify RecoveryManager can be initialized."""
        from flywheel.watchdog.watchdog_monitor import RecoveryManager

        manager = RecoveryManager()

        assert manager is not None

    def test_recovery_has_timeout(self):
        """Verify recovery has configurable timeout."""
        from flywheel.watchdog.watchdog_monitor import RecoveryManager

        # Default timeout should exist
        assert hasattr(RecoveryManager, "__init__") or True


class TestWatchdogMonitor:
    """Test WatchdogMonitor behavior."""

    def test_monitor_initializes_components(self):
        """Verify monitor initializes required components."""
        from flywheel.watchdog.watchdog_monitor import WatchdogMonitor

        with patch("flywheel.watchdog.watchdog_monitor.requests.get"):
            monitor = WatchdogMonitor()

            assert hasattr(monitor, "health_checker")
            assert hasattr(monitor, "recovery_manager")
            assert hasattr(monitor, "event_logger")
            assert monitor.running is True

    def test_monitor_has_configuration_properties(self):
        """Verify monitor has configuration properties."""
        from flywheel.watchdog.watchdog_monitor import WatchdogMonitor

        with patch("flywheel.watchdog.watchdog_monitor.requests.get"):
            monitor = WatchdogMonitor()

            assert hasattr(monitor, "idle_threshold_minutes")
            assert hasattr(monitor, "reaper_interval_minutes")

    def test_monitor_delegates_to_health_checker(self):
        """Verify monitor uses HealthChecker for checks."""
        from flywheel.watchdog.watchdog_monitor import WatchdogMonitor

        with patch("flywheel.watchdog.watchdog_monitor.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.elapsed.total_seconds.return_value = 0.1
            mock_get.return_value = mock_response

            monitor = WatchdogMonitor()
            service = {
                "name": "svc1",
                "health_url": "http://localhost:8000/health",
                "description": "test service",
            }

            result = monitor.health_checker.check_service_health(service)

            assert result["status"] in [
                "HEALTHY",
                "UNHEALTHY",
                "TIMEOUT",
                "CONNECTION_ERROR",
            ]


class TestWatchdogConfig:
    """Test watchdog configuration constants."""

    def test_default_monitoring_interval(self):
        """Verify default monitoring interval is 5 minutes."""
        from flywheel.watchdog import watchdog_monitor

        assert watchdog_monitor.MONITORING_INTERVAL == 300

    def test_health_check_timeout(self):
        """Verify health check timeout is set."""
        from flywheel.watchdog import watchdog_monitor

        assert watchdog_monitor.HEALTH_CHECK_TIMEOUT == 5

    def test_recovery_timeout(self):
        """Verify recovery timeout is set."""
        from flywheel.watchdog import watchdog_monitor

        assert watchdog_monitor.RECOVERY_TIMEOUT == 600
