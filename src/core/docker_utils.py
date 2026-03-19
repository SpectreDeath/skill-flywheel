import asyncio
import logging
from typing import Any, Dict, Optional

import docker
from docker.errors import APIError, NotFound

logger = logging.getLogger(__name__)

class DockerUtils:
    """Consolidated Docker infrastructure management utilities."""
    
    def __init__(self, docker_client: Optional[docker.DockerClient] = None):
        try:
            self.client = docker_client or docker.from_env()
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            self.client = None

    async def scale_service(self, service_name: str, replicas: int) -> Dict[str, Any]:
        """Scale a Docker service to the specified number of replicas."""
        if not self.client:
            return {"success": False, "error": "Docker client not initialized"}
            
        service_key = f"mcp-{service_name}"
        try:
            service = await asyncio.to_thread(self.client.services.get, service_key)
            await asyncio.to_thread(service.scale, replicas)
            logger.info(f"Successfully scaled service {service_key} to {replicas} replicas")
            return {"success": True, "service": service_name, "replicas": replicas}
        except NotFound:
            logger.error(f"Service {service_key} not found")
            return {"success": False, "error": f"Service {service_key} not found"}
        except APIError as e:
            logger.error(f"Docker API error during scaling: {e}")
            return {"success": False, "error": f"Docker API error: {e}"}
        except Exception as e:
            logger.exception(f"Unexpected error scaling {service_name}")
            return {"success": False, "error": str(e)}

    async def get_infrastructure_status(self) -> Dict[str, Any]:
        """Get the current status of all containers in the infrastructure."""
        if not self.client:
            return {"status": "error", "message": "Docker client not initialized"}
            
        try:
            containers = await asyncio.to_thread(self.client.containers.list)
            running_services = [c.name for c in containers]
            return {
                "status": "success",
                "verification": {
                    "services_running": len(running_services),
                    "running_containers": running_services
                }
            }
        except Exception as e:
            logger.error(f"Failed to get infrastructure status: {e}")
            return {"status": "error", "message": str(e)}
