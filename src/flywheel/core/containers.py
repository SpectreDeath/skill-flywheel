import asyncio
import logging
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

import docker

logger = logging.getLogger(__name__)


class ContainerState(Enum):
    """Container lifecycle states."""

    IDLE = "idle"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class ContainerSlot:
    """Represents a managed container slot."""

    container_id: str
    skill_name: str
    state: ContainerState = ContainerState.IDLE
    created_at: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)
    execution_count: int = 0
    resource_limits: Dict[str, Any] = field(default_factory=dict)


class ContainerPool:
    """Pool of reusable containers for skill execution."""

    def __init__(
        self,
        docker_client: docker.DockerClient,
        max_pool_size: int = 10,
        max_idle_time: int = 300,
        image: str = "python:3.12-slim",
    ):
        self.docker_client = docker_client
        self.max_pool_size = max_pool_size
        self.max_idle_time = max_idle_time
        self.image = image
        self.slots: Dict[str, ContainerSlot] = {}
        self._lock = asyncio.Lock()

    async def acquire(
        self, skill_name: str, resource_limits: Dict[str, Any] | None = None
    ) -> str:
        """Acquire a container for skill execution."""
        async with self._lock:
            # Try to find an idle container for this skill
            for slot_id, slot in self.slots.items():
                if slot.skill_name == skill_name and slot.state == ContainerState.IDLE:
                    slot.state = ContainerState.RUNNING
                    slot.last_used = time.time()
                    slot.execution_count += 1
                    logger.info(f"Reusing container {slot_id} for {skill_name}")
                    return slot_id

            # Create new container if pool not full
            if len(self.slots) < self.max_pool_size:
                return await self._create_container(skill_name, resource_limits or {})

            # Evict oldest idle container
            oldest_idle = self._find_oldest_idle()
            if oldest_idle:
                await self._remove_container(oldest_idle)
                return await self._create_container(skill_name, resource_limits or {})

            raise RuntimeError("Container pool exhausted")

    async def release(self, slot_id: str):
        """Release a container back to the pool."""
        async with self._lock:
            if slot_id in self.slots:
                slot = self.slots[slot_id]
                slot.state = ContainerState.IDLE
                slot.last_used = time.time()
                logger.info(f"Released container {slot_id}")

    async def _create_container(
        self, skill_name: str, resource_limits: Dict[str, Any]
    ) -> str:
        """Create a new container with resource limits."""
        mem_limit = resource_limits.get("memory", "512m")
        cpu_quota = resource_limits.get("cpu_quota", 50000)  # 50% CPU by default
        cpu_period = resource_limits.get("cpu_period", 100000)

        try:
            container = self.docker_client.containers.run(
                self.image,
                command=["sleep", "3600"],  # Keep container alive
                detach=True,
                labels={"mcp_skill": skill_name, "mcp_pool": "true"},
                mem_limit=mem_limit,
                cpu_quota=cpu_quota,
                cpu_period=cpu_period,
                network_mode="none",  # Isolated network
                read_only=True,  # Read-only filesystem
                security_opt=["no-new-privileges"],
            )

            slot = ContainerSlot(
                container_id=container.id,
                skill_name=skill_name,
                state=ContainerState.RUNNING,
                resource_limits=resource_limits,
            )
            self.slots[container.id] = slot
            logger.info(f"Created container {container.id[:12]} for {skill_name}")
            return container.id

        except Exception as e:
            logger.error(f"Failed to create container: {e}")
            raise

    async def _remove_container(self, slot_id: str):
        """Remove a container from the pool."""
        if slot_id in self.slots:
            slot = self.slots[slot_id]
            slot.state = ContainerState.STOPPING
            try:
                container = self.docker_client.containers.get(slot_id)
                container.stop(timeout=5)
                container.remove(force=True)
            except Exception as e:
                logger.warning(f"Error removing container {slot_id}: {e}")
            finally:
                del self.slots[slot_id]

    def _find_oldest_idle(self) -> Optional[str]:
        """Find the oldest idle container."""
        idle_slots = [
            (sid, slot)
            for sid, slot in self.slots.items()
            if slot.state == ContainerState.IDLE
        ]
        if not idle_slots:
            return None
        return min(idle_slots, key=lambda x: x[1].last_used)[0]

    async def cleanup_idle(self):
        """Remove containers that have been idle too long."""
        now = time.time()
        to_remove = []
        for slot_id, slot in self.slots.items():
            if (
                slot.state == ContainerState.IDLE
                and now - slot.last_used > self.max_idle_time
            ):
                to_remove.append(slot_id)

        for slot_id in to_remove:
            await self._remove_container(slot_id)
            logger.info(f"Cleaned up idle container {slot_id}")

    def get_stats(self) -> Dict[str, Any]:
        """Get pool statistics."""
        total = len(self.slots)
        idle = sum(1 for s in self.slots.values() if s.state == ContainerState.IDLE)
        running = sum(
            1 for s in self.slots.values() if s.state == ContainerState.RUNNING
        )
        return {
            "total": total,
            "idle": idle,
            "running": running,
            "max_pool_size": self.max_pool_size,
        }


class ContainerManager:
    """Container management for sandboxed skill execution and auto-scaling."""

    DEFAULT_RESOURCE_LIMITS = {
        "memory": "512m",
        "cpu_quota": 50000,
        "cpu_period": 100000,
    }

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.container_enabled = config.get("containers", {}).get("enabled", False)
        self.docker_client: Optional[docker.DockerClient] = None
        self.pool: Optional[ContainerPool] = None

        if self.container_enabled:
            try:
                self.docker_client = docker.from_env()
                pool_size = config.get("containers", {}).get("max_containers", 10)
                idle_timeout = config.get("containers", {}).get("max_idle_time", 300)
                self.pool = ContainerPool(
                    self.docker_client,
                    max_pool_size=pool_size,
                    max_idle_time=idle_timeout,
                )
                logger.info("Container manager initialized with pool")
            except Exception as e:
                logger.error(f"Failed to connect to Docker: {str(e)}")
                self.container_enabled = False

    async def execute_in_container(
        self,
        skill_name: str,
        command: List[str],
        resource_limits: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Execute a skill in an isolated container."""
        if not self.container_enabled or not self.pool:
            return {"status": "disabled", "message": "Containers not available"}

        limits = resource_limits or self.DEFAULT_RESOURCE_LIMITS
        slot_id = None

        try:
            slot_id = await self.pool.acquire(skill_name, limits)
            container = self.docker_client.containers.get(slot_id)

            exec_result = container.exec_run(
                command,
                stdout=True,
                stderr=True,
                workdir="/tmp",
            )

            return {
                "status": "success",
                "exit_code": exec_result.exit_code,
                "output": exec_result.output.decode("utf-8", errors="replace"),
                "container_id": slot_id[:12],
            }

        except Exception as e:
            logger.error(f"Container execution failed: {e}")
            return {"status": "error", "message": str(e)}

        finally:
            if slot_id:
                await self.pool.release(slot_id)

    async def scale_containers(self, current_load: float):
        """Scale containers based on current load."""
        if not self.container_enabled:
            logger.debug("Container scaling disabled - containers.enabled is false")
            return {"status": "disabled", "message": "Container scaling not enabled"}

        try:
            containers = self.docker_client.containers.list(
                filters={"label": "mcp_server=true"}
            )
            current_count = len(containers)

            scaling_config = self.config.get("agents", {}).get("auto_scaling", {})
            scale_up_threshold = scaling_config.get("scale_up_threshold", 0.8)
            scale_down_threshold = scaling_config.get("scale_down_threshold", 0.3)
            max_containers = self.config.get("containers", {}).get("max_containers", 10)
            min_containers = scaling_config.get("min_agents", 1)

            target_count = current_count

            if current_load > scale_up_threshold:
                target_count = min(current_count + 1, max_containers)
            elif current_load < scale_down_threshold:
                target_count = max(current_count - 1, min_containers)

            if target_count != current_count:
                logger.info(
                    f"Scaling containers from {current_count} to {target_count}"
                )
                return {
                    "status": "not_implemented",
                    "current_count": current_count,
                    "target_count": target_count,
                    "message": "Scaling calculation complete but execution not implemented",
                }

            return {
                "status": "unchanged",
                "current_count": current_count,
                "target_count": target_count,
            }
        except Exception as e:
            logger.error(f"Error during container scaling: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def cleanup_idle_containers(self):
        """Clean up idle containers from the pool."""
        if self.pool:
            await self.pool.cleanup_idle()

    def get_pool_stats(self) -> Dict[str, Any]:
        """Get container pool statistics."""

if __name__ == "__main__":
    if self.pool:
                return self.pool.get_stats()
            return {"status": "disabled"}