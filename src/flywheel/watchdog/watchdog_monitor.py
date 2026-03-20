#!/usr/bin/env python3
"""
Self-Healing Watchdog for MCP Infrastructure

This script monitors all 11 MCP services (ports 8000-8012) every 5 minutes.
If any service fails health checks, it automatically triggers the master_flywheel()
function to re-provision the entire infrastructure.

Features:
- Health check monitoring for all MCP services
- Automatic recovery via master_flywheel()
- Comprehensive logging to flywheel_events.log
- Configurable monitoring intervals
- Robust error handling and timeout management
"""

import asyncio
import datetime
import json
import logging
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import requests

from src.core.docker_utils import DockerUtils

# Configure logging for the watchdog itself
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("watchdog_monitor.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Services will be loaded from mcp_config.json
SERVICES: List[Dict[str, Any]] = []

# Configuration
MONITORING_INTERVAL = 300  # 5 minutes in seconds
HEALTH_CHECK_TIMEOUT = 5  # 5 seconds timeout for health checks
RECOVERY_TIMEOUT = 600  # 10 minutes timeout for recovery process
LOG_FILE = "flywheel_events.log"
WATCHDOG_LOG_FILE = "watchdog_monitor.log"


class WatchdogEventLogger:
    """Handles logging of watchdog events to flywheel_events.log"""

    def __init__(self, log_file: str = LOG_FILE):
        self.log_file = log_file
        self.ensure_log_file_exists()

    def ensure_log_file_exists(self):
        """Ensure the log file exists and create it if it doesn't"""
        log_path = Path(self.log_file)
        if not log_path.exists():
            log_path.touch()
            logger.info(f"Created new log file: {self.log_file}")

    def log_event(self, event_data: Dict[str, Any]):
        """Log an event to the flywheel_events.log file"""
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(event_data) + "\n")
        except Exception as e:
            logger.error(f"Failed to write to log file {self.log_file}: {e}")

    def log_service_failure(self, failed_services: List[Dict[str, Any]]):
        """Log service failure event"""
        timestamp = datetime.datetime.now().isoformat()
        event = {
            "timestamp": timestamp,
            "event_type": "SERVICE_FAILURE",
            "failed_services": failed_services,
            "total_failed": len(failed_services),
        }
        self.log_event(event)
        logger.warning(
            f"Service failure detected: {len(failed_services)} services down"
        )

    def log_recovery_attempt(
        self, failed_services: List[Dict[str, Any]], recovery_result: Dict[str, Any]
    ):
        """Log recovery attempt event"""
        timestamp = datetime.datetime.now().isoformat()
        event = {
            "timestamp": timestamp,
            "event_type": "RECOVERY_ATTEMPT",
            "failed_services": failed_services,
            "recovery_result": recovery_result,
            "recovery_successful": recovery_result.get("success", False),
        }
        self.log_event(event)
        if recovery_result.get("success", False):
            logger.info("Recovery attempt successful")
        else:
            logger.error("Recovery attempt failed")

    def log_recovery_success(self, recovered_services: List[str]):
        """Log successful recovery event"""
        timestamp = datetime.datetime.now().isoformat()
        event = {
            "timestamp": timestamp,
            "event_type": "RECOVERY_SUCCESS",
            "recovered_services": recovered_services,
            "total_recovered": len(recovered_services),
        }
        self.log_event(event)
        logger.info(
            f"Recovery successful: {len(recovered_services)} services recovered"
        )

    def log_recovery_failure(self, failed_services: List[Dict[str, Any]], error: str):
        """Log recovery failure event"""
        timestamp = datetime.datetime.now().isoformat()
        event = {
            "timestamp": timestamp,
            "event_type": "RECOVERY_FAILURE",
            "failed_services": failed_services,
            "error": error,
        }
        self.log_event(event)
        logger.error(f"Recovery failed: {error}")


class HealthChecker:
    """Handles health checking of MCP services"""

    def __init__(self, timeout: int = HEALTH_CHECK_TIMEOUT):
        self.timeout = timeout

    def check_service_health(self, service: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check the health of a single service
        Returns a dict with status information
        """
        try:
            response = requests.get(service["health_url"], timeout=self.timeout)

            if response.status_code == 200:
                return {
                    "service": service["name"],
                    "status": "HEALTHY",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "description": service["description"],
                }
            else:
                return {
                    "service": service["name"],
                    "status": "UNHEALTHY",
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}",
                    "description": service["description"],
                }

        except requests.exceptions.Timeout:
            return {
                "service": service["name"],
                "status": "TIMEOUT",
                "error": f"Request timed out after {self.timeout} seconds",
                "description": service["description"],
            }
        except requests.exceptions.ConnectionError:
            return {
                "service": service["name"],
                "status": "CONNECTION_ERROR",
                "error": "Unable to connect to service",
                "description": service["description"],
            }
        except requests.exceptions.RequestException as e:
            return {
                "service": service["name"],
                "status": "ERROR",
                "error": str(e),
                "description": service["description"],
            }


class RecoveryManager:
    """Handles the recovery process via master_flywheel()"""

    def __init__(self, timeout: int = RECOVERY_TIMEOUT):
        self.timeout = timeout

    def trigger_recovery(self, failed_services: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Trigger the master_flywheel recovery process
        Returns a dict with recovery result information
        """
        try:
            logger.info(
                f"Triggering recovery for {len(failed_services)} failed services"
            )

            # Construct the command to call master_flywheel
            recovery_command = [
                sys.executable,
                "-c",
                """
import asyncio
import sys
import os

# Add current directory to Python path to import discovery_service
sys.path.insert(0, os.getcwd())

try:
    from discovery_service import master_flywheel
    
    async def run_recovery():
        result = await master_flywheel()
        print(json.dumps(result))
    
    asyncio.run(run_recovery())
except ImportError as e:
    print(json.dumps({"success": false, "error": f"Import error: {e}"}))
except Exception as e:
    print(json.dumps({"success": false, "error": f"Recovery error: {e}"}))
""",
            ]

            # Execute the recovery command
            result = subprocess.run(
                recovery_command, capture_output=True, text=True, timeout=self.timeout
            )

            recovery_data = {
                "success": result.returncode == 0,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "failed_services": failed_services,
            }

            if result.returncode == 0:
                logger.info("Recovery process completed successfully")
            else:
                logger.error(
                    f"Recovery process failed with return code {result.returncode}"
                )
                logger.error(f"Recovery stderr: {result.stderr}")

            return recovery_data

        except subprocess.TimeoutExpired:
            error_msg = f"Recovery process timed out after {self.timeout} seconds"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "failed_services": failed_services,
            }
        except Exception as e:
            error_msg = f"Recovery process failed with exception: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "failed_services": failed_services,
            }


class WatchdogMonitor:
    """Main watchdog monitoring class with dynamic lazy loading support"""

    def __init__(self):
        self.health_checker = HealthChecker()
        self.recovery_manager = RecoveryManager()
        self.event_logger = WatchdogEventLogger()
        self.running = True

        # Initialize Docker client and utils
        self.docker_utils = DockerUtils()
        self.docker_client = self.docker_utils.client

        # Dynamic lazy loading configuration
        self.idle_threshold_minutes = int(
            os.environ.get("IDLE_THRESHOLD_MINUTES", "30")
        )
        self.reaper_interval_minutes = int(
            os.environ.get("REAPER_INTERVAL_MINUTES", "10")
        )
        # Configuration paths
        self.docker_compose_file = Path(
            os.environ.get("DOCKER_COMPOSE_FILE", "../../docker-compose.yml")
        )
        self.mcp_config_file = Path(
            os.environ.get("MCP_CONFIG_FILE", "../../data/mcp_config.json")
        )
        self.registry_file = Path(
            os.environ.get("SKILL_REGISTRY_PATH", "../../data/skill_registry.json")
        )

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down watchdog...")
        self.running = False

    async def monitor_services(self):
        """Main monitoring loop with dynamic lazy loading support"""
        # Load configuration on startup
        self._load_services_config()

        logger.info("Starting MCP infrastructure watchdog monitoring")
        logger.info(
            f"Monitoring {len(SERVICES)} services every {MONITORING_INTERVAL} seconds"
        )
        logger.info(f"Idle threshold: {self.idle_threshold_minutes} minutes")
        logger.info(f"Reaper interval: {self.reaper_interval_minutes} minutes")
        logger.info("Press Ctrl+C to stop the watchdog")

        # Track time for reaper checks
        last_reaper_check = time.time()

        while self.running:
            try:
                # Check health of all services
                failed_services = await self.check_all_services()

                if failed_services:
                    logger.warning(f"Detected {len(failed_services)} failed services")
                    await self.handle_service_failures(failed_services)
                else:
                    logger.debug("All services are healthy")

                # Check if it's time to run the reaper (idle service detection)
                current_time = time.time()
                if current_time - last_reaper_check >= (
                    self.reaper_interval_minutes * 60
                ):
                    logger.info("Running reaper: checking for idle services...")
                    await self.check_service_activity_and_idle()
                    last_reaper_check = current_time

                # Wait for next monitoring cycle
                await asyncio.sleep(MONITORING_INTERVAL)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying

        logger.info("Watchdog monitoring stopped")

    def _load_services_config(self):
        """Load service configuration from mcp_config.json"""
        global SERVICES
        config_path = os.environ.get("MCP_CONFIG_FILE", "data/mcp_config.json")
        try:
            if os.path.exists(config_path):
                with open(config_path) as f:
                    config = json.load(f)
                    new_services = []
                    for key, svc in config.get("services", {}).items():
                        new_services.append(
                            {
                                "name": svc["name"],
                                "port": int(svc["url"].split(":")[-1]),
                                "health_url": svc.get(
                                    "health_check", f"{svc['url']}/health"
                                ),
                                "description": f"{key.capitalize()} service",
                            }
                        )
                    SERVICES = new_services
                    logger.info(f"Loaded {len(SERVICES)} services from configuration")
            else:
                logger.error(f"Configuration file not found: {config_path}")
        except Exception as e:
            logger.error(f"Failed to load service configuration: {str(e)}")

    async def check_all_services(self) -> List[Dict[str, Any]]:
        """Check health of all services concurrently"""
        tasks = []
        for service in SERVICES:
            task = asyncio.to_thread(self.health_checker.check_service_health, service)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        failed_services = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Handle exceptions from health checks
                failed_services.append(
                    {
                        "service": SERVICES[i]["name"],
                        "status": "EXCEPTION",
                        "error": str(result),
                        "description": SERVICES[i]["description"],
                    }
                )
            elif result["status"] != "HEALTHY":
                failed_services.append(result)

        return failed_services

    async def handle_service_failures(self, failed_services: List[Dict[str, Any]]):
        """Handle service failures and trigger recovery"""
        # Log the failure
        self.event_logger.log_service_failure(failed_services)

        # Trigger recovery
        recovery_result = self.recovery_manager.trigger_recovery(failed_services)

        # Log the recovery attempt
        self.event_logger.log_recovery_attempt(failed_services, recovery_result)

        if recovery_result.get("success", False):
            # Wait a bit for services to come back online
            await asyncio.sleep(30)

            # Verify recovery by checking services again
            remaining_failures = await self.check_all_services()

            if not remaining_failures:
                recovered_services = [svc["service"] for svc in failed_services]
                self.event_logger.log_recovery_success(recovered_services)
                logger.info("All services successfully recovered")
            else:
                failed_recovery = [svc["service"] for svc in remaining_failures]
                self.event_logger.log_recovery_failure(
                    remaining_failures,
                    f"Some services still failing after recovery: {failed_recovery}",
                )
                logger.warning(
                    f"Some services still failing after recovery: {failed_recovery}"
                )
        else:
            self.event_logger.log_recovery_failure(
                failed_services, recovery_result.get("error", "Unknown recovery error")
            )

    async def check_service_activity_and_idle(self):
        """Check service activity and idle status for dynamic lazy loading"""
        try:
            # Get activity status from discovery service
            activity_result = await self._get_service_activity_from_discovery()

            if not activity_result or "service_status" not in activity_result:
                logger.warning(
                    "Could not get service activity status from discovery service"
                )
                return

            idle_services = []
            for service_name, status in activity_result["service_status"].items():
                if status.get("is_idle", False):
                    idle_services.append(
                        {
                            "service_name": service_name,
                            "idle_time_minutes": status.get("idle_time_minutes", 0),
                            "threshold_minutes": status.get("threshold_minutes", 30),
                        }
                    )

            if idle_services:
                logger.info(
                    f"Found {len(idle_services)} idle services: {[s['service_name'] for s in idle_services]}"
                )
                await self.handle_idle_services(idle_services)
            else:
                logger.debug("No idle services found")

        except Exception as e:
            logger.error(f"Error checking service activity: {e}")

    async def _get_service_activity_from_discovery(self) -> Dict[str, Any] | None:
        """Get service activity status from discovery service"""
        try:
            # Call discovery service to get activity status

            # Note: This would need to be implemented as a proper HTTP call
            # For now, we'll simulate the call or use a different approach
            # since the discovery service tools are not directly accessible via HTTP

            # Alternative: Read from a shared state file or use docker exec
            # For this implementation, we'll use a simpler approach

            return None  # Placeholder - would need proper implementation

        except Exception as e:
            logger.error(f"Failed to get activity from discovery service: {e}")
            return None

    async def handle_idle_services(self, idle_services: List[Dict[str, Any]]):
        """Handle idle services by spinning them down"""
        for service_info in idle_services:
            service_name = service_info["service_name"]
            idle_time = service_info["idle_time_minutes"]

            logger.info(
                f"Reaper: Service {service_name} has been idle for {idle_time:.1f} minutes, spinning down"
            )

            # Spin down the service
            spin_down_result = await self.spin_down_service(service_name)

            if spin_down_result["success"]:
                logger.info(f"Reaper: Successfully spun down {service_name}")
                self.event_logger.log_event(
                    {
                        "timestamp": datetime.datetime.now().isoformat(),
                        "event_type": "SERVICE_SPIN_DOWN",
                        "service": service_name,
                        "idle_time_minutes": idle_time,
                        "result": "SUCCESS",
                    }
                )
            else:
                logger.error(
                    f"Reaper: Failed to spin down {service_name}: {spin_down_result['error']}"
                )
                self.event_logger.log_event(
                    {
                        "timestamp": datetime.datetime.now().isoformat(),
                        "event_type": "SERVICE_SPIN_DOWN",
                        "service": service_name,
                        "idle_time_minutes": idle_time,
                        "result": "FAILED",
                        "error": spin_down_result["error"],
                    }
                )

    async def spin_down_service(self, service_name: str) -> Dict[str, Any]:
        """Spin down a service by setting its replicas to 0"""
        try:
            # Update docker-compose.yml to set replicas to 0
            update_result = await self.update_service_replicas(service_name, 0)
            if not update_result["success"]:
                return {
                    "success": False,
                    "error": f"Failed to update replicas: {update_result['error']}",
                }

            # Deploy infrastructure
            deploy_result = await self.deploy_infrastructure()
            if deploy_result.get("status") != "success":
                return {
                    "success": False,
                    "error": f"Failed to deploy infrastructure: {deploy_result.get('message', 'Unknown error')}",
                }

            return {"success": True, "service": service_name, "action": "spun_down"}

        except Exception as e:
            return {"success": False, "error": f"Spin down failed: {str(e)}"}

    async def update_service_replicas(
        self, service_name: str, replicas: int
    ) -> Dict[str, Any]:
        """Update the replica count via DockerUtils."""
        return await self.docker_utils.scale_service(service_name, replicas)

    async def deploy_infrastructure(self) -> Dict[str, Any]:
        """Verify infrastructure status via DockerUtils."""
        return await self.docker_utils.get_infrastructure_status()


def main():
    """Main entry point"""
    # Create the watchdog monitor
    watchdog = WatchdogMonitor()

    print("=== MCP Infrastructure Self-Healing Watchdog ===")
    print(f"Health check interval: {MONITORING_INTERVAL} seconds")
    print(f"Log file: {LOG_FILE}")
    print("Starting watchdog... (Press Ctrl+C to stop)")
    print("-" * 60)

    try:
        # Run the monitoring loop
        asyncio.run(watchdog.monitor_services())
    except KeyboardInterrupt:
        logger.info("Watchdog stopped by user")
    except Exception as e:
        logger.error(f"Watchdog failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
