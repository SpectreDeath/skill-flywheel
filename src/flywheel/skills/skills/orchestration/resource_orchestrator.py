#!/usr/bin/env python3
"""
Skill: resource-orchestrator
Domain: orchestration
Description: Resource orchestration and allocation system
"""

import asyncio
import logging
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class ResourceType(Enum):
    """Resource types"""
    CPU = "cpu"
    MEMORY = "memory"
    STORAGE = "storage"
    NETWORK = "network"
    GPU = "gpu"
    LICENSE = "license"

class ResourceStatus(Enum):
    """Resource status"""
    AVAILABLE = "available"
    ALLOCATED = "allocated"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"
    FAILED = "failed"

class AllocationType(Enum):
    """Allocation types"""
    EXCLUSIVE = "exclusive"
    SHARED = "shared"
    DYNAMIC = "dynamic"
    PRIORITY = "priority"

class ResourcePoolType(Enum):
    """Resource pool types"""
    COMPUTE = "compute"
    STORAGE = "storage"
    NETWORK = "network"
    SPECIALIZED = "specialized"

@dataclass
class Resource:
    """Represents a resource"""
    resource_id: str
    resource_type: ResourceType
    name: str
    capacity: float
    available: float
    allocated: float
    status: ResourceStatus
    location: str
    tags: Dict[str, str]
    metadata: Dict[str, Any]
    created_at: float

@dataclass
class ResourceAllocation:
    """Represents a resource allocation"""
    allocation_id: str
    resource_id: str
    consumer_id: str
    allocation_type: AllocationType
    amount: float
    start_time: float
    end_time: float | None
    priority: int
    status: str  # pending, active, expired, cancelled
    metadata: Dict[str, Any]
    created_at: float

@dataclass
class ResourcePool:
    """Represents a resource pool"""
    pool_id: str
    name: str
    pool_type: ResourcePoolType
    resources: List[str]
    total_capacity: float
    available_capacity: float
    allocation_policy: Dict[str, Any]
    created_at: float

@dataclass
class ResourceRequest:
    """Represents a resource request"""
    request_id: str
    consumer_id: str
    resource_type: ResourceType
    amount: float
    duration: int  # seconds
    priority: int
    allocation_type: AllocationType
    constraints: Dict[str, Any]
    status: str  # pending, approved, rejected, fulfilled
    created_at: float

@dataclass
class ResourceConsumer:
    """Represents a resource consumer"""
    consumer_id: str
    name: str
    consumer_type: str  # service, application, user, system
    priority: int
    allocated_resources: List[str]
    resource_usage: Dict[str, float]
    created_at: float

class ResourceOrchestrator:
    """Resource orchestration and allocation system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the resource orchestrator
        
        Args:
            config: Configuration dictionary with:
                - max_allocation_time: Maximum allocation time
                - resource_monitoring_interval: Monitoring interval
                - auto_scaling_enabled: Enable auto-scaling
                - allocation_timeout: Allocation timeout
        """
        self.max_allocation_time = config.get("max_allocation_time", 300)
        self.resource_monitoring_interval = config.get("resource_monitoring_interval", 30)
        self.auto_scaling_enabled = config.get("auto_scaling_enabled", True)
        self.allocation_timeout = config.get("allocation_timeout", 60)
        
        self.resources: Dict[str, Resource] = {}
        self.allocations: Dict[str, ResourceAllocation] = {}
        self.resource_pools: Dict[str, ResourcePool] = {}
        self.resource_requests: Dict[str, ResourceRequest] = {}
        self.resource_consumers: Dict[str, ResourceConsumer] = {}
        
        self.orchestrator_stats = {
            "total_resources": 0,
            "allocated_resources": 0,
            "available_resources": 0,
            "total_allocations": 0,
            "active_allocations": 0,
            "failed_allocations": 0,
            "utilization_rate": 0.0
        }
        
        self.allocation_policies = {
            "first_come_first_served": self._allocate_first_come_first_served,
            "priority_based": self._allocate_priority_based,
            "round_robin": self._allocate_round_robin,
            "best_fit": self._allocate_best_fit,
            "worst_fit": self._allocate_worst_fit
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Start background services
        self._resource_monitor_task = asyncio.create_task(self._resource_monitor_loop())
        self._allocation_processor_task = asyncio.create_task(self._allocation_processor_loop())
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    def register_resource(self,
                         resource_type: ResourceType,
                         name: str,
                         capacity: float,
                         location: str = "default",
                         tags: Dict[str, str] | None = None,
                         metadata: Dict[str, Any] | None = None) -> str:
        """
        Register a resource
        
        Args:
            resource_type: Type of resource
            name: Resource name
            capacity: Total capacity
            location: Resource location
            tags: Resource tags
            metadata: Resource metadata
            
        Returns:
            Resource ID
        """
        resource_id = str(uuid.uuid4())
        
        resource = Resource(
            resource_id=resource_id,
            resource_type=resource_type,
            name=name,
            capacity=capacity,
            available=capacity,
            allocated=0.0,
            status=ResourceStatus.AVAILABLE,
            location=location,
            tags=tags or {},
            metadata=metadata or {},
            created_at=time.time()
        )
        
        self.resources[resource_id] = resource
        self.orchestrator_stats["total_resources"] += 1
        self.orchestrator_stats["available_resources"] += capacity
        
        self.logger.info(f"Registered resource: {resource_id} ({name})")
        return resource_id
    
    def create_resource_pool(self,
                            name: str,
                            pool_type: ResourcePoolType,
                            resource_ids: List[str],
                            allocation_policy: Dict[str, Any] | None = None) -> str:
        """
        Create a resource pool
        
        Args:
            name: Pool name
            pool_type: Pool type
            resource_ids: List of resource IDs
            allocation_policy: Allocation policy
            
        Returns:
            Pool ID
        """
        pool_id = str(uuid.uuid4())
        
        total_capacity = sum(
            self.resources[rid].available 
            for rid in resource_ids 
            if rid in self.resources
        )
        
        pool = ResourcePool(
            pool_id=pool_id,
            name=name,
            pool_type=pool_type,
            resources=resource_ids,
            total_capacity=total_capacity,
            available_capacity=total_capacity,
            allocation_policy=allocation_policy or {"policy": "first_come_first_served"},
            created_at=time.time()
        )
        
        self.resource_pools[pool_id] = pool
        self.logger.info(f"Created resource pool: {pool_id} ({name})")
        return pool_id
    
    def register_consumer(self,
                         name: str,
                         consumer_type: str = "application",
                         priority: int = 1) -> str:
        """
        Register a resource consumer
        
        Args:
            name: Consumer name
            consumer_type: Type of consumer
            priority: Consumer priority
            
        Returns:
            Consumer ID
        """
        consumer_id = str(uuid.uuid4())
        
        consumer = ResourceConsumer(
            consumer_id=consumer_id,
            name=name,
            consumer_type=consumer_type,
            priority=priority,
            allocated_resources=[],
            resource_usage={},
            created_at=time.time()
        )
        
        self.resource_consumers[consumer_id] = consumer
        self.logger.info(f"Registered consumer: {consumer_id} ({name})")
        return consumer_id
    
    def request_resource(self,
                        consumer_id: str,
                        resource_type: ResourceType,
                        amount: float,
                        duration: int = 3600,
                        priority: int = 1,
                        allocation_type: AllocationType = AllocationType.SHARED,
                        constraints: Dict[str, Any] | None = None) -> str:
        """
        Request resource allocation
        
        Args:
            consumer_id: Consumer ID
            resource_type: Type of resource
            amount: Amount needed
            duration: Duration in seconds
            priority: Request priority
            allocation_type: Type of allocation
            constraints: Additional constraints
            
        Returns:
            Request ID
        """
        if consumer_id not in self.resource_consumers:
            raise ValueError(f"Consumer {consumer_id} not registered")
        
        request_id = str(uuid.uuid4())
        
        request = ResourceRequest(
            request_id=request_id,
            consumer_id=consumer_id,
            resource_type=resource_type,
            amount=amount,
            duration=duration,
            priority=priority,
            allocation_type=allocation_type,
            constraints=constraints or {},
            status="pending",
            created_at=time.time()
        )
        
        self.resource_requests[request_id] = request
        self.logger.info(f"Resource request: {request_id} ({amount} {resource_type.value})")
        return request_id
    
    async def allocate_resource(self, request_id: str) -> str | None:
        """
        Allocate resources for a request
        
        Args:
            request_id: Request ID
            
        Returns:
            Allocation ID or None
        """
        if request_id not in self.resource_requests:
            return None
        
        request = self.resource_requests[request_id]
        request.status = "approved"
        
        # Find suitable resources
        suitable_resources = self._find_suitable_resources(request)
        
        if not suitable_resources:
            request.status = "rejected"
            self.logger.warning(f"No suitable resources for request {request_id}")
            return None
        
        # Allocate resources
        allocation_id = await self._create_allocation(request, suitable_resources)
        
        if allocation_id:
            request.status = "fulfilled"
            self.logger.info(f"Resource allocated: {allocation_id}")
        else:
            request.status = "rejected"
        
        return allocation_id
    
    def get_resource_status(self, resource_id: str) -> Dict[str, Any] | None:
        """Get resource status"""
        if resource_id not in self.resources:
            return None
        
        resource = self.resources[resource_id]
        
        return {
            "resource_id": resource.resource_id,
            "name": resource.name,
            "type": resource.resource_type.value,
            "capacity": resource.capacity,
            "available": resource.available,
            "allocated": resource.allocated,
            "status": resource.status.value,
            "location": resource.location,
            "utilization": (resource.allocated / resource.capacity) * 100 if resource.capacity > 0 else 0
        }
    
    def get_allocation_status(self, allocation_id: str) -> Dict[str, Any] | None:
        """Get allocation status"""
        if allocation_id not in self.allocations:
            return None
        
        allocation = self.allocations[allocation_id]
        
        return {
            "allocation_id": allocation.allocation_id,
            "resource_id": allocation.resource_id,
            "consumer_id": allocation.consumer_id,
            "type": allocation.allocation_type.value,
            "amount": allocation.amount,
            "start_time": datetime.fromtimestamp(allocation.start_time).isoformat(),
            "end_time": datetime.fromtimestamp(allocation.end_time).isoformat() if allocation.end_time else None,
            "priority": allocation.priority,
            "status": allocation.status
        }
    
    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            "total_resources": self.orchestrator_stats["total_resources"],
            "allocated_resources": self.orchestrator_stats["allocated_resources"],
            "available_resources": self.orchestrator_stats["available_resources"],
            "total_allocations": self.orchestrator_stats["total_allocations"],
            "active_allocations": self.orchestrator_stats["active_allocations"],
            "failed_allocations": self.orchestrator_stats["failed_allocations"],
            "utilization_rate": self.orchestrator_stats["utilization_rate"],
            "total_pools": len(self.resource_pools),
            "total_consumers": len(self.resource_consumers),
            "pending_requests": len([r for r in self.resource_requests.values() if r.status == "pending"])
        }
    
    def release_allocation(self, allocation_id: str) -> bool:
        """Release a resource allocation"""
        if allocation_id not in self.allocations:
            return False
        
        allocation = self.allocations[allocation_id]
        
        # Update resource availability
        if allocation.resource_id in self.resources:
            resource = self.resources[allocation.resource_id]
            resource.available += allocation.amount
            resource.allocated -= allocation.amount
            resource.status = ResourceStatus.AVAILABLE if resource.allocated == 0 else ResourceStatus.ALLOCATED
        
        # Update consumer allocations
        if allocation.consumer_id in self.resource_consumers:
            consumer = self.resource_consumers[allocation.consumer_id]
            if allocation_id in consumer.allocated_resources:
                consumer.allocated_resources.remove(allocation_id)
        
        # Update allocation status
        allocation.status = "expired"
        allocation.end_time = time.time()
        
        self.orchestrator_stats["active_allocations"] -= 1
        
        self.logger.info(f"Released allocation: {allocation_id}")
        return True
    
    def _find_suitable_resources(self, request: ResourceRequest) -> List[str]:
        """Find suitable resources for a request"""
        suitable_resources = []
        
        # Filter resources by type and availability
        for resource_id, resource in self.resources.items():
            if (resource.resource_type == request.resource_type and
                resource.status == ResourceStatus.AVAILABLE and
                resource.available >= request.amount):
                
                # Check constraints
                if self._check_constraints(resource, request.constraints):
                    suitable_resources.append(resource_id)
        
        # Sort by allocation policy
        policy = request.allocation_type.value
        if policy in self.allocation_policies:
            suitable_resources = self.allocation_policies[policy](suitable_resources, request)
        
        return suitable_resources
    
    def _check_constraints(self, resource: Resource, constraints: Dict[str, Any]) -> bool:
        """Check if resource meets constraints"""
        for key, value in constraints.items():
            if key in resource.tags:
                if resource.tags[key] != value:
                    return False
            elif key in resource.metadata:
                if resource.metadata[key] != value:
                    return False
            else:
                return False
        return True
    
    async def _create_allocation(self,
                               request: ResourceRequest,
                               resource_ids: List[str]) -> str | None:
        """Create resource allocation"""
        if not resource_ids:
            return None
        
        allocation_id = str(uuid.uuid4())
        
        # Allocate from first suitable resource
        resource_id = resource_ids[0]
        resource = self.resources[resource_id]
        
        # Update resource
        resource.available -= request.amount
        resource.allocated += request.amount
        resource.status = ResourceStatus.ALLOCATED
        
        # Create allocation
        allocation = ResourceAllocation(
            allocation_id=allocation_id,
            resource_id=resource_id,
            consumer_id=request.consumer_id,
            allocation_type=request.allocation_type,
            amount=request.amount,
            start_time=time.time(),
            end_time=time.time() + request.duration,
            priority=request.priority,
            status="active",
            metadata={"request_id": request.request_id},
            created_at=time.time()
        )
        
        self.allocations[allocation_id] = allocation
        
        # Update consumer
        if request.consumer_id in self.resource_consumers:
            consumer = self.resource_consumers[request.consumer_id]
            consumer.allocated_resources.append(allocation_id)
        
        # Update statistics
        self.orchestrator_stats["total_allocations"] += 1
        self.orchestrator_stats["active_allocations"] += 1
        self.orchestrator_stats["allocated_resources"] += request.amount
        self.orchestrator_stats["available_resources"] -= request.amount
        
        # Schedule deallocation
        asyncio.create_task(self._schedule_deallocation(allocation_id, request.duration))
        
        return allocation_id
    
    async def _schedule_deallocation(self, allocation_id: str, duration: int):
        """Schedule allocation deallocation"""
        await asyncio.sleep(duration)
        self.release_allocation(allocation_id)
    
    def _allocate_first_come_first_served(self, resource_ids: List[str], request: ResourceRequest) -> List[str]:
        """First come, first served allocation"""
        return resource_ids
    
    def _allocate_priority_based(self, resource_ids: List[str], request: ResourceRequest) -> List[str]:
        """Priority-based allocation"""
        # Sort by resource priority (if available)
        return sorted(resource_ids, key=lambda rid: self.resources[rid].metadata.get("priority", 0), reverse=True)
    
    def _allocate_round_robin(self, resource_ids: List[str], request: ResourceRequest) -> List[str]:
        """Round robin allocation"""
        # Simple round robin based on resource ID
        return sorted(resource_ids, key=hash)
    
    def _allocate_best_fit(self, resource_ids: List[str], request: ResourceRequest) -> List[str]:
        """Best fit allocation"""
        # Sort by available capacity (smallest first)
        return sorted(resource_ids, key=lambda rid: self.resources[rid].available)
    
    def _allocate_worst_fit(self, resource_ids: List[str], request: ResourceRequest) -> List[str]:
        """Worst fit allocation"""
        # Sort by available capacity (largest first)
        return sorted(resource_ids, key=lambda rid: self.resources[rid].available, reverse=True)
    
    async def _resource_monitor_loop(self):
        """Background resource monitor loop"""
        while True:
            try:
                await self._monitor_resources()
                await asyncio.sleep(self.resource_monitoring_interval)
            except Exception as e:
                self.logger.error(f"Error in resource monitor loop: {e}")
                await asyncio.sleep(self.resource_monitoring_interval)
    
    async def _monitor_resources(self):
        """Monitor resource health and utilization"""
        total_capacity = 0
        total_allocated = 0
        
        for resource_id, resource in self.resources.items():
            # Update utilization statistics
            total_capacity += resource.capacity
            total_allocated += resource.allocated
            
            # Check for resource failures
            if resource.status == ResourceStatus.ALLOCATED and resource.available < 0:
                resource.status = ResourceStatus.FAILED
                self.logger.warning(f"Resource {resource_id} failed: negative availability")
        
        # Update utilization rate
        if total_capacity > 0:
            self.orchestrator_stats["utilization_rate"] = (total_allocated / total_capacity) * 100
    
    async def _allocation_processor_loop(self):
        """Background allocation processor loop"""
        while True:
            try:
                await self._process_pending_requests()
                await asyncio.sleep(5)
            except Exception as e:
                self.logger.error(f"Error in allocation processor loop: {e}")
                await asyncio.sleep(5)
    
    async def _process_pending_requests(self):
        """Process pending resource requests"""
        pending_requests = [
            req for req in self.resource_requests.values()
            if req.status == "pending"
        ]
        
        # Sort by priority and creation time
        pending_requests.sort(key=lambda r: (-r.priority, r.created_at))
        
        for request in pending_requests:
            if time.time() - request.created_at > self.allocation_timeout:
                request.status = "rejected"
                continue
            
            await self.allocate_resource(request.request_id)
    
    async def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            try:
                await self._cleanup_expired_allocations()
                await asyncio.sleep(300)  # Run every 5 minutes
            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(300)
    
    async def _cleanup_expired_allocations(self):
        """Clean up expired allocations"""
        current_time = time.time()
        
        for allocation_id, allocation in list(self.allocations.items()):
            if allocation.status == "active" and allocation.end_time and current_time > allocation.end_time:
                self.release_allocation(allocation_id)

# Global resource orchestrator instance
_resource_orchestrator = ResourceOrchestrator({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "register_resource", "create_pool", "register_consumer", 
                     "request_resource", "allocate_resource", "release_allocation", 
                     "get_status", "get_allocation_status", "get_stats"
            - resource_data: Resource configuration
            - pool_data: Pool configuration
            - consumer_data: Consumer configuration
            - request_data: Request configuration
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "register_resource":
            resource_data = payload.get("resource_data", {})
            
            resource_id = _resource_orchestrator.register_resource(
                resource_type=ResourceType(resource_data.get("resource_type", "cpu")),
                name=resource_data.get("name", "Resource"),
                capacity=resource_data.get("capacity", 100.0),
                location=resource_data.get("location", "default"),
                tags=resource_data.get("tags"),
                metadata=resource_data.get("metadata")
            )
            
            return {
                "result": {
                    "resource_id": resource_id,
                    "message": f"Registered resource: {resource_id}"
                },
                "metadata": {
                    "action": "register_resource",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_pool":
            pool_data = payload.get("pool_data", {})
            
            pool_id = _resource_orchestrator.create_resource_pool(
                name=pool_data.get("name", "Resource Pool"),
                pool_type=ResourcePoolType(pool_data.get("pool_type", "compute")),
                resource_ids=pool_data.get("resource_ids", []),
                allocation_policy=pool_data.get("allocation_policy")
            )
            
            return {
                "result": {
                    "pool_id": pool_id,
                    "message": f"Created resource pool: {pool_id}"
                },
                "metadata": {
                    "action": "create_pool",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "register_consumer":
            consumer_data = payload.get("consumer_data", {})
            
            consumer_id = _resource_orchestrator.register_consumer(
                name=consumer_data.get("name", "Consumer"),
                consumer_type=consumer_data.get("consumer_type", "application"),
                priority=consumer_data.get("priority", 1)
            )
            
            return {
                "result": {
                    "consumer_id": consumer_id,
                    "message": f"Registered consumer: {consumer_id}"
                },
                "metadata": {
                    "action": "register_consumer",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "request_resource":
            request_data = payload.get("request_data", {})
            
            request_id = _resource_orchestrator.request_resource(
                consumer_id=request_data.get("consumer_id", ""),
                resource_type=ResourceType(request_data.get("resource_type", "cpu")),
                amount=request_data.get("amount", 10.0),
                duration=request_data.get("duration", 3600),
                priority=request_data.get("priority", 1),
                allocation_type=AllocationType(request_data.get("allocation_type", "shared")),
                constraints=request_data.get("constraints")
            )
            
            return {
                "result": {
                    "request_id": request_id,
                    "message": f"Resource request created: {request_id}"
                },
                "metadata": {
                    "action": "request_resource",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "allocate_resource":
            request_id = payload.get("request_id", "")
            allocation_id = await _resource_orchestrator.allocate_resource(request_id)
            
            return {
                "result": {
                    "allocation_id": allocation_id,
                    "message": f"Resource allocated: {allocation_id}" if allocation_id else "Allocation failed"
                },
                "metadata": {
                    "action": "allocate_resource",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "release_allocation":
            allocation_id = payload.get("allocation_id", "")
            success = _resource_orchestrator.release_allocation(allocation_id)
            
            return {
                "result": {
                    "success": success,
                    "message": f"Allocation released: {allocation_id}" if success else "Release failed"
                },
                "metadata": {
                    "action": "release_allocation",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_status":
            resource_id = payload.get("resource_id", "")
            status = _resource_orchestrator.get_resource_status(resource_id)
            
            return {
                "result": status,
                "metadata": {
                    "action": "get_status",
                    "timestamp": datetime.now().isoformat(),
                    "resource_id": resource_id
                }
            }
        
        elif action == "get_allocation_status":
            allocation_id = payload.get("allocation_id", "")
            status = _resource_orchestrator.get_allocation_status(allocation_id)
            
            return {
                "result": status,
                "metadata": {
                    "action": "get_allocation_status",
                    "timestamp": datetime.now().isoformat(),
                    "allocation_id": allocation_id
                }
            }
        
        elif action == "get_stats":
            stats = _resource_orchestrator.get_orchestrator_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        else:
            return {
                "result": {
                    "error": f"Unknown action: {action}"
                },
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat()
                }
            }
    
    except Exception as e:
        logger.error(f"Error in resource_orchestrator: {e}")
        return {
            "result": {
                "error": str(e)
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat()
            }
        }

# Example usage function
async def example_usage():
    """Example of how to use the resource orchestrator skill"""
    
    # Register resources
    cpu_resource = await invoke({
        "action": "register_resource",
        "resource_data": {
            "resource_type": "cpu",
            "name": "CPU Cluster",
            "capacity": 100.0,
            "location": "datacenter-1",
            "tags": {"type": "compute", "priority": "high"},
            "metadata": {"cores": 32, "speed": "3.5GHz"}
        }
    })
    
    memory_resource = await invoke({
        "action": "register_resource",
        "resource_data": {
            "resource_type": "memory",
            "name": "Memory Pool",
            "capacity": 512.0,
            "location": "datacenter-1",
            "tags": {"type": "memory", "priority": "medium"},
            "metadata": {"type": "RAM", "speed": "3200MHz"}
        }
    })
    
    storage_resource = await invoke({
        "action": "register_resource",
        "resource_data": {
            "resource_type": "storage",
            "name": "SSD Storage",
            "capacity": 1000.0,
            "location": "datacenter-2",
            "tags": {"type": "storage", "priority": "low"},
            "metadata": {"type": "SSD", "interface": "NVMe"}
        }
    })
    
    print(f"Registered resources: {cpu_resource['result']['resource_id']}, {memory_resource['result']['resource_id']}, {storage_resource['result']['resource_id']}")
    
    # Create resource pools
    compute_pool = await invoke({
        "action": "create_pool",
        "pool_data": {
            "name": "Compute Pool",
            "pool_type": "compute",
            "resource_ids": [cpu_resource['result']['resource_id'], memory_resource['result']['resource_id']],
            "allocation_policy": {"policy": "priority_based"}
        }
    })
    
    storage_pool = await invoke({
        "action": "create_pool",
        "pool_data": {
            "name": "Storage Pool",
            "pool_type": "storage",
            "resource_ids": [storage_resource['result']['resource_id']],
            "allocation_policy": {"policy": "first_come_first_served"}
        }
    })
    
    print(f"Created pools: {compute_pool['result']['pool_id']}, {storage_pool['result']['pool_id']}")
    
    # Register consumers
    app_consumer = await invoke({
        "action": "register_consumer",
        "consumer_data": {
            "name": "Web Application",
            "consumer_type": "application",
            "priority": 3
        }
    })
    
    db_consumer = await invoke({
        "action": "register_consumer",
        "consumer_data": {
            "name": "Database Service",
            "consumer_type": "service",
            "priority": 5
        }
    })
    
    print(f"Registered consumers: {app_consumer['result']['consumer_id']}, {db_consumer['result']['consumer_id']}")
    
    # Request resources
    cpu_request = await invoke({
        "action": "request_resource",
        "request_data": {
            "consumer_id": app_consumer['result']['consumer_id'],
            "resource_type": "cpu",
            "amount": 20.0,
            "duration": 1800,
            "priority": 2,
            "allocation_type": "shared",
            "constraints": {"priority": "high"}
        }
    })
    
    memory_request = await invoke({
        "action": "request_resource",
        "request_data": {
            "consumer_id": db_consumer['result']['consumer_id'],
            "resource_type": "memory",
            "amount": 100.0,
            "duration": 3600,
            "priority": 4,
            "allocation_type": "exclusive",
            "constraints": {"priority": "medium"}
        }
    })
    
    print(f"Resource requests: {cpu_request['result']['request_id']}, {memory_request['result']['request_id']}")
    
    # Allocate resources
    cpu_allocation = await invoke({
        "action": "allocate_resource",
        "request_id": cpu_request['result']['request_id']
    })
    
    memory_allocation = await invoke({
        "action": "allocate_resource",
        "request_id": memory_request['result']['request_id']
    })
    
    print(f"Allocations: {cpu_allocation['result']['allocation_id']}, {memory_allocation['result']['allocation_id']}")
    
    # Get resource status
    cpu_status = await invoke({
        "action": "get_status",
        "resource_id": cpu_resource['result']['resource_id']
    })
    
    memory_status = await invoke({
        "action": "get_status",
        "resource_id": memory_resource['result']['resource_id']
    })
    
    print(f"Resource status - CPU: {cpu_status['result']['utilization']:.1f}%, Memory: {memory_status['result']['utilization']:.1f}%")
    
    # Get allocation status
    allocation_status = await invoke({
        "action": "get_allocation_status",
        "allocation_id": cpu_allocation['result']['allocation_id']
    })
    
    print(f"Allocation status: {allocation_status['result']}")
    
    # Get orchestrator statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Orchestrator stats: {stats['result']}")
    
    # Release allocation
    await invoke({
        "action": "release_allocation",
        "allocation_id": cpu_allocation['result']['allocation_id']
    })
    
    print("Released CPU allocation")

if __name__ == "__main__":
    asyncio.run(example_usage())
