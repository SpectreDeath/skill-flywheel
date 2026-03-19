#!/usr/bin/env python3
"""
Skill: microservices-orchestrator
Domain: modern_backend
Description: Microservices orchestration and coordination system
"""

import asyncio
import json
import logging
import random
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class ServiceStatus(Enum):
    """Service status"""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"

class LoadBalancingStrategy(Enum):
    """Load balancing strategies"""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    IP_HASH = "ip_hash"
    RANDOM = "random"

class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class HealthCheckType(Enum):
    """Health check types"""
    HTTP = "http"
    TCP = "tcp"
    GRPC = "grpc"
    COMMAND = "command"

@dataclass
class ServiceInstance:
    """Represents a service instance"""
    instance_id: str
    service_id: str
    host: str
    port: int
    status: ServiceStatus
    weight: int
    metadata: Dict[str, Any]
    last_health_check: float
    health_check_url: Optional[str]
    connections: int
    response_time: float
    created_at: float

@dataclass
class Service:
    """Represents a microservice"""
    service_id: str
    name: str
    version: str
    description: str
    instances: List[str]
    load_balancing: LoadBalancingStrategy
    circuit_breaker: bool
    timeout: int
    retries: int
    health_check_interval: int
    created_at: float

@dataclass
class CircuitBreaker:
    """Represents a circuit breaker"""
    service_id: str
    failure_threshold: int
    recovery_timeout: int
    state: CircuitState
    failure_count: int
    last_failure_time: float
    success_count: int
    created_at: float

@dataclass
class ServiceDependency:
    """Represents a service dependency"""
    dependency_id: str
    source_service: str
    target_service: str
    dependency_type: str  # sync, async, event
    timeout: int
    retry_policy: Dict[str, Any]
    created_at: float

@dataclass
class ServiceMesh:
    """Represents a service mesh configuration"""
    mesh_id: str
    name: str
    services: List[str]
    policies: Dict[str, Any]
    created_at: float

class MicroservicesOrchestrator:
    """Microservices orchestration and coordination system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the microservices orchestrator
        
        Args:
            config: Configuration dictionary with:
                - service_registry_path: Path to service registry
                - default_timeout: Default service timeout
                - health_check_interval: Health check interval
                - circuit_breaker_threshold: Failure threshold
        """
        self.service_registry_path = config.get("service_registry_path", "./service_registry")
        self.default_timeout = config.get("default_timeout", 30)
        self.health_check_interval = config.get("health_check_interval", 30)
        self.circuit_breaker_threshold = config.get("circuit_breaker_threshold", 5)
        
        self.services: Dict[str, Service] = {}
        self.service_instances: Dict[str, ServiceInstance] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.dependencies: Dict[str, ServiceDependency] = {}
        self.service_meshes: Dict[str, ServiceMesh] = {}
        
        self.load_balancer_state: Dict[str, int] = defaultdict(int)
        self.connection_pools: Dict[str, List[str]] = defaultdict(list)
        
        self.orchestrator_stats = {
            "total_services": 0,
            "healthy_instances": 0,
            "unhealthy_instances": 0,
            "total_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0,
            "circuit_breaker_trips": 0
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Ensure directories exist
        os.makedirs(self.service_registry_path, exist_ok=True)
        
        # Start background services
        self._orchestrator_task = asyncio.create_task(self._orchestrator_loop())
        self._health_check_task = asyncio.create_task(self._health_check_loop())
        self._circuit_breaker_task = asyncio.create_task(self._circuit_breaker_loop())
    
    def register_service(self,
                        name: str,
                        version: str,
                        description: str,
                        load_balancing: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN,
                        circuit_breaker: bool = True,
                        timeout: int = 30,
                        retries: int = 3,
                        health_check_interval: int = 30) -> str:
        """
        Register a new service
        
        Args:
            name: Service name
            version: Service version
            description: Service description
            load_balancing: Load balancing strategy
            circuit_breaker: Enable circuit breaker
            timeout: Service timeout
            retries: Number of retries
            health_check_interval: Health check interval
            
        Returns:
            Service ID
        """
        service_id = str(uuid.uuid4())
        
        service = Service(
            service_id=service_id,
            name=name,
            version=version,
            description=description,
            instances=[],
            load_balancing=load_balancing,
            circuit_breaker=circuit_breaker,
            timeout=timeout,
            retries=retries,
            health_check_interval=health_check_interval,
            created_at=time.time()
        )
        
        self.services[service_id] = service
        self.orchestrator_stats["total_services"] += 1
        
        # Create circuit breaker
        if circuit_breaker:
            circuit_breaker = CircuitBreaker(
                service_id=service_id,
                failure_threshold=self.circuit_breaker_threshold,
                recovery_timeout=60,
                state=CircuitState.CLOSED,
                failure_count=0,
                last_failure_time=0.0,
                success_count=0,
                created_at=time.time()
            )
            self.circuit_breakers[service_id] = circuit_breaker
        
        self.logger.info(f"Registered service: {service_id} ({name})")
        return service_id
    
    def register_instance(self,
                         service_id: str,
                         host: str,
                         port: int,
                         weight: int = 1,
                         metadata: Optional[Dict[str, Any]] = None,
                         health_check_url: Optional[str] = None) -> str:
        """
        Register a service instance
        
        Args:
            service_id: Service ID
            host: Instance host
            port: Instance port
            weight: Instance weight for load balancing
            metadata: Instance metadata
            health_check_url: Health check URL
            
        Returns:
            Instance ID
        """
        if service_id not in self.services:
            raise ValueError(f"Service {service_id} not found")
        
        instance_id = str(uuid.uuid4())
        
        instance = ServiceInstance(
            instance_id=instance_id,
            service_id=service_id,
            host=host,
            port=port,
            status=ServiceStatus.HEALTHY,
            weight=weight,
            metadata=metadata or {},
            last_health_check=time.time(),
            health_check_url=health_check_url,
            connections=0,
            response_time=0.0,
            created_at=time.time()
        )
        
        self.service_instances[instance_id] = instance
        self.services[service_id].instances.append(instance_id)
        self.orchestrator_stats["healthy_instances"] += 1
        
        self.logger.info(f"Registered instance: {instance_id} for service {service_id}")
        return instance_id
    
    def add_dependency(self,
                      source_service: str,
                      target_service: str,
                      dependency_type: str = "sync",
                      timeout: int = 30,
                      retry_policy: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a service dependency
        
        Args:
            source_service: Source service ID
            target_service: Target service ID
            dependency_type: Type of dependency (sync, async, event)
            timeout: Timeout for dependency call
            retry_policy: Retry policy configuration
            
        Returns:
            Dependency ID
        """
        dependency_id = str(uuid.uuid4())
        
        dependency = ServiceDependency(
            dependency_id=dependency_id,
            source_service=source_service,
            target_service=target_service,
            dependency_type=dependency_type,
            timeout=timeout,
            retry_policy=retry_policy or {"max_retries": 3, "backoff_factor": 1.0},
            created_at=time.time()
        )
        
        self.dependencies[dependency_id] = dependency
        self.logger.info(f"Added dependency: {dependency_id} ({source_service} -> {target_service})")
        return dependency_id
    
    def create_service_mesh(self,
                           name: str,
                           services: List[str],
                           policies: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a service mesh
        
        Args:
            name: Mesh name
            services: List of service IDs
            policies: Mesh policies
            
        Returns:
            Mesh ID
        """
        mesh_id = str(uuid.uuid4())
        
        mesh = ServiceMesh(
            mesh_id=mesh_id,
            name=name,
            services=services,
            policies=policies or {},
            created_at=time.time()
        )
        
        self.service_meshes[mesh_id] = mesh
        self.logger.info(f"Created service mesh: {mesh_id} ({name})")
        return mesh_id
    
    def get_service_instance(self, service_id: str) -> Optional[ServiceInstance]:
        """
        Get a service instance using load balancing
        
        Args:
            service_id: Service ID
            
        Returns:
            Service instance or None
        """
        if service_id not in self.services:
            return None
        
        service = self.services[service_id]
        
        # Check circuit breaker
        if service.circuit_breaker and service_id in self.circuit_breakers:
            circuit_breaker = self.circuit_breakers[service_id]
            if circuit_breaker.state == CircuitState.OPEN:
                self.logger.warning(f"Circuit breaker open for service {service_id}")
                return None
        
        # Get healthy instances
        healthy_instances = [
            instance for instance_id, instance in self.service_instances.items()
            if instance.service_id == service_id and instance.status == ServiceStatus.HEALTHY
        ]
        
        if not healthy_instances:
            return None
        
        # Apply load balancing
        if service.load_balancing == LoadBalancingStrategy.ROUND_ROBIN:
            return self._round_robin(healthy_instances, service_id)
        elif service.load_balancing == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return self._least_connections(healthy_instances)
        elif service.load_balancing == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
            return self._weighted_round_robin(healthy_instances, service_id)
        elif service.load_balancing == LoadBalancingStrategy.IP_HASH:
            return self._ip_hash(healthy_instances, "127.0.0.1")
        elif service.load_balancing == LoadBalancingStrategy.RANDOM:
            return self._random(healthy_instances)
        else:
            return healthy_instances[0]
    
    def record_service_call(self,
                           service_id: str,
                           instance_id: str,
                           success: bool,
                           response_time: float):
        """
        Record a service call for metrics and circuit breaker
        
        Args:
            service_id: Service ID
            instance_id: Instance ID
            success: Whether the call was successful
            response_time: Response time in milliseconds
        """
        if instance_id in self.service_instances:
            instance = self.service_instances[instance_id]
            instance.connections += 1 if success else 0
            instance.response_time = response_time
        
        # Update circuit breaker
        if service_id in self.circuit_breakers:
            circuit_breaker = self.circuit_breakers[service_id]
            
            if success:
                circuit_breaker.success_count += 1
                circuit_breaker.failure_count = 0
                if circuit_breaker.state == CircuitState.HALF_OPEN:
                    circuit_breaker.state = CircuitState.CLOSED
                    circuit_breaker.success_count = 0
            else:
                circuit_breaker.failure_count += 1
                circuit_breaker.last_failure_time = time.time()
                
                if (circuit_breaker.state == CircuitState.CLOSED and 
                    circuit_breaker.failure_count >= circuit_breaker.failure_threshold):
                    circuit_breaker.state = CircuitState.OPEN
                    self.orchestrator_stats["circuit_breaker_trips"] += 1
                    self.logger.warning(f"Circuit breaker opened for service {service_id}")
        
        # Update statistics
        self.orchestrator_stats["total_requests"] += 1
        if not success:
            self.orchestrator_stats["failed_requests"] += 1
        
        # Update average response time
        total_time = self.orchestrator_stats["average_response_time"] * (self.orchestrator_stats["total_requests"] - 1)
        self.orchestrator_stats["average_response_time"] = (total_time + response_time) / self.orchestrator_stats["total_requests"]
    
    def get_service_stats(self, service_id: str) -> Dict[str, Any]:
        """Get service statistics"""
        if service_id not in self.services:
            return {}
        
        service = self.services[service_id]
        instances = [self.service_instances[iid] for iid in service.instances]
        
        healthy_count = sum(1 for i in instances if i.status == ServiceStatus.HEALTHY)
        degraded_count = sum(1 for i in instances if i.status == ServiceStatus.DEGRADED)
        unhealthy_count = sum(1 for i in instances if i.status == ServiceStatus.UNHEALTHY)
        
        avg_response_time = sum(i.response_time for i in instances) / len(instances) if instances else 0
        
        return {
            "service_id": service_id,
            "name": service.name,
            "version": service.version,
            "total_instances": len(instances),
            "healthy_instances": healthy_count,
            "degraded_instances": degraded_count,
            "unhealthy_instances": unhealthy_count,
            "load_balancing": service.load_balancing.value,
            "circuit_breaker_enabled": service.circuit_breaker,
            "average_response_time": avg_response_time,
            "dependencies": [
                dep.dependency_id for dep in self.dependencies.values()
                if dep.source_service == service_id
            ]
        }
    
    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            "total_services": self.orchestrator_stats["total_services"],
            "healthy_instances": self.orchestrator_stats["healthy_instances"],
            "unhealthy_instances": self.orchestrator_stats["unhealthy_instances"],
            "total_requests": self.orchestrator_stats["total_requests"],
            "failed_requests": self.orchestrator_stats["failed_requests"],
            "average_response_time": self.orchestrator_stats["average_response_time"],
            "circuit_breaker_trips": self.orchestrator_stats["circuit_breaker_trips"],
            "total_dependencies": len(self.dependencies),
            "total_meshes": len(self.service_meshes)
        }
    
    def _round_robin(self, instances: List[ServiceInstance], service_id: str) -> ServiceInstance:
        """Round robin load balancing"""
        index = self.load_balancer_state[service_id] % len(instances)
        self.load_balancer_state[service_id] += 1
        return instances[index]
    
    def _least_connections(self, instances: List[ServiceInstance]) -> ServiceInstance:
        """Least connections load balancing"""
        return min(instances, key=lambda i: i.connections)
    
    def _weighted_round_robin(self, instances: List[ServiceInstance], service_id: str) -> ServiceInstance:
        """Weighted round robin load balancing"""
        # Simple implementation - in practice, this would be more sophisticated
        total_weight = sum(i.weight for i in instances)
        if total_weight == 0:
            return self._round_robin(instances, service_id)
        
        # Select based on cumulative weights
        target_weight = random.randint(1, total_weight)
        cumulative_weight = 0
        
        for instance in instances:
            cumulative_weight += instance.weight
            if cumulative_weight >= target_weight:
                return instance
        
        return instances[0]
    
    def _ip_hash(self, instances: List[ServiceInstance], client_ip: str) -> ServiceInstance:
        """IP hash load balancing"""
        hash_value = hash(client_ip) % len(instances)
        return instances[hash_value]
    
    def _random(self, instances: List[ServiceInstance]) -> ServiceInstance:
        """Random load balancing"""
        return random.choice(instances)
    
    async def _orchestrator_loop(self):
        """Background orchestrator monitoring loop"""
        while True:
            try:
                await self._monitor_services()
                await asyncio.sleep(30)
            except Exception as e:
                self.logger.error(f"Error in orchestrator loop: {e}")
                await asyncio.sleep(30)
    
    async def _monitor_services(self):
        """Monitor service health and update statistics"""
        # Update instance counts
        healthy_count = sum(1 for i in self.service_instances.values() if i.status == ServiceStatus.HEALTHY)
        unhealthy_count = sum(1 for i in self.service_instances.values() if i.status == ServiceStatus.UNHEALTHY)
        
        self.orchestrator_stats["healthy_instances"] = healthy_count
        self.orchestrator_stats["unhealthy_instances"] = unhealthy_count
    
    async def _health_check_loop(self):
        """Background health check loop"""
        while True:
            try:
                await self._perform_health_checks()
                await asyncio.sleep(self.health_check_interval)
            except Exception as e:
                self.logger.error(f"Error in health check loop: {e}")
                await asyncio.sleep(self.health_check_interval)
    
    async def _perform_health_checks(self):
        """Perform health checks on all instances"""
        current_time = time.time()
        
        for instance_id, instance in self.service_instances.items():
            # Check if health check is due
            if current_time - instance.last_health_check >= instance.service.health_check_interval:
                await self._health_check_instance(instance)
    
    async def _health_check_instance(self, instance: ServiceInstance):
        """Perform health check on a specific instance"""
        try:
            if instance.health_check_url:
                # In a real implementation, this would make HTTP requests
                # For now, simulate health check
                import random
                is_healthy = random.choices([True, False], weights=[90, 10])[0]
                
                if is_healthy:
                    instance.status = ServiceStatus.HEALTHY
                else:
                    instance.status = ServiceStatus.UNHEALTHY
                
                instance.last_health_check = time.time()
                
        except Exception as e:
            self.logger.error(f"Health check failed for instance {instance.instance_id}: {e}")
            instance.status = ServiceStatus.UNHEALTHY
            instance.last_health_check = time.time()
    
    async def _circuit_breaker_loop(self):
        """Background circuit breaker monitoring loop"""
        while True:
            try:
                await self._monitor_circuit_breakers()
                await asyncio.sleep(10)
            except Exception as e:
                self.logger.error(f"Error in circuit breaker loop: {e}")
                await asyncio.sleep(10)
    
    async def _monitor_circuit_breakers(self):
        """Monitor circuit breakers and transition states"""
        current_time = time.time()
        
        for service_id, circuit_breaker in self.circuit_breakers.items():
            if circuit_breaker.state == CircuitState.OPEN:
                # Check if recovery timeout has passed
                if current_time - circuit_breaker.last_failure_time >= circuit_breaker.recovery_timeout:
                    circuit_breaker.state = CircuitState.HALF_OPEN
                    self.logger.info(f"Circuit breaker half-open for service {service_id}")
    
    def _save_service_registry(self):
        """Save service registry to file"""
        registry_data = {
            "services": {
                sid: {
                    "service_id": s.service_id,
                    "name": s.name,
                    "version": s.version,
                    "description": s.description,
                    "instances": s.instances,
                    "load_balancing": s.load_balancing.value,
                    "circuit_breaker": s.circuit_breaker,
                    "timeout": s.timeout,
                    "retries": s.retries,
                    "health_check_interval": s.health_check_interval,
                    "created_at": s.created_at
                }
                for sid, s in self.services.items()
            },
            "instances": {
                iid: {
                    "instance_id": i.instance_id,
                    "service_id": i.service_id,
                    "host": i.host,
                    "port": i.port,
                    "status": i.status.value,
                    "weight": i.weight,
                    "metadata": i.metadata,
                    "last_health_check": i.last_health_check,
                    "health_check_url": i.health_check_url,
                    "connections": i.connections,
                    "response_time": i.response_time,
                    "created_at": i.created_at
                }
                for iid, i in self.service_instances.items()
            },
            "circuit_breakers": {
                sid: {
                    "service_id": cb.service_id,
                    "failure_threshold": cb.failure_threshold,
                    "recovery_timeout": cb.recovery_timeout,
                    "state": cb.state.value,
                    "failure_count": cb.failure_count,
                    "last_failure_time": cb.last_failure_time,
                    "success_count": cb.success_count,
                    "created_at": cb.created_at
                }
                for sid, cb in self.circuit_breakers.items()
            }
        }
        
        registry_file = os.path.join(self.service_registry_path, "registry.json")
        with open(registry_file, 'w') as f:
            json.dump(registry_data, f, indent=2)
    
    def _load_service_registry(self):
        """Load service registry from file"""
        registry_file = os.path.join(self.service_registry_path, "registry.json")
        
        if os.path.exists(registry_file):
            with open(registry_file) as f:
                registry_data = json.load(f)
            
            # Load services
            for sid, s_data in registry_data.get("services", {}).items():
                service = Service(
                    service_id=s_data["service_id"],
                    name=s_data["name"],
                    version=s_data["version"],
                    description=s_data["description"],
                    instances=s_data["instances"],
                    load_balancing=LoadBalancingStrategy(s_data["load_balancing"]),
                    circuit_breaker=s_data["circuit_breaker"],
                    timeout=s_data["timeout"],
                    retries=s_data["retries"],
                    health_check_interval=s_data["health_check_interval"],
                    created_at=s_data["created_at"]
                )
                self.services[sid] = service
            
            # Load instances
            for iid, i_data in registry_data.get("instances", {}).items():
                instance = ServiceInstance(
                    instance_id=i_data["instance_id"],
                    service_id=i_data["service_id"],
                    host=i_data["host"],
                    port=i_data["port"],
                    status=ServiceStatus(i_data["status"]),
                    weight=i_data["weight"],
                    metadata=i_data["metadata"],
                    last_health_check=i_data["last_health_check"],
                    health_check_url=i_data["health_check_url"],
                    connections=i_data["connections"],
                    response_time=i_data["response_time"],
                    created_at=i_data["created_at"]
                )
                self.service_instances[iid] = instance
            
            # Load circuit breakers
            for sid, cb_data in registry_data.get("circuit_breakers", {}).items():
                circuit_breaker = CircuitBreaker(
                    service_id=cb_data["service_id"],
                    failure_threshold=cb_data["failure_threshold"],
                    recovery_timeout=cb_data["recovery_timeout"],
                    state=CircuitState(cb_data["state"]),
                    failure_count=cb_data["failure_count"],
                    last_failure_time=cb_data["last_failure_time"],
                    success_count=cb_data["success_count"],
                    created_at=cb_data["created_at"]
                )
                self.circuit_breakers[sid] = circuit_breaker

# Global microservices orchestrator instance
_orchestrator = MicroservicesOrchestrator({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "register_service", "register_instance", "add_dependency", 
                     "create_mesh", "get_instance", "record_call", "get_service_stats", "get_stats"
            - service_data: Service configuration
            - instance_data: Instance configuration
            - dependency_data: Dependency configuration
            - mesh_data: Mesh configuration
            - call_data: Call recording data
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "register_service":
            service_data = payload.get("service_data", {})
            
            service_id = _orchestrator.register_service(
                name=service_data.get("name", "Service"),
                version=service_data.get("version", "1.0.0"),
                description=service_data.get("description", ""),
                load_balancing=LoadBalancingStrategy(service_data.get("load_balancing", "round_robin")),
                circuit_breaker=service_data.get("circuit_breaker", True),
                timeout=service_data.get("timeout", 30),
                retries=service_data.get("retries", 3),
                health_check_interval=service_data.get("health_check_interval", 30)
            )
            
            return {
                "result": {
                    "service_id": service_id,
                    "message": f"Registered service: {service_id}"
                },
                "metadata": {
                    "action": "register_service",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "register_instance":
            instance_data = payload.get("instance_data", {})
            
            instance_id = _orchestrator.register_instance(
                service_id=instance_data.get("service_id", ""),
                host=instance_data.get("host", "localhost"),
                port=instance_data.get("port", 8080),
                weight=instance_data.get("weight", 1),
                metadata=instance_data.get("metadata"),
                health_check_url=instance_data.get("health_check_url")
            )
            
            return {
                "result": {
                    "instance_id": instance_id,
                    "message": f"Registered instance: {instance_id}"
                },
                "metadata": {
                    "action": "register_instance",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "add_dependency":
            dependency_data = payload.get("dependency_data", {})
            
            dependency_id = _orchestrator.add_dependency(
                source_service=dependency_data.get("source_service", ""),
                target_service=dependency_data.get("target_service", ""),
                dependency_type=dependency_data.get("dependency_type", "sync"),
                timeout=dependency_data.get("timeout", 30),
                retry_policy=dependency_data.get("retry_policy")
            )
            
            return {
                "result": {
                    "dependency_id": dependency_id,
                    "message": f"Added dependency: {dependency_id}"
                },
                "metadata": {
                    "action": "add_dependency",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_mesh":
            mesh_data = payload.get("mesh_data", {})
            
            mesh_id = _orchestrator.create_service_mesh(
                name=mesh_data.get("name", "Service Mesh"),
                services=mesh_data.get("services", []),
                policies=mesh_data.get("policies")
            )
            
            return {
                "result": {
                    "mesh_id": mesh_id,
                    "message": f"Created service mesh: {mesh_id}"
                },
                "metadata": {
                    "action": "create_mesh",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_instance":
            service_id = payload.get("service_id", "")
            instance = _orchestrator.get_service_instance(service_id)
            
            if instance:
                return {
                    "result": {
                        "instance_id": instance.instance_id,
                        "host": instance.host,
                        "port": instance.port,
                        "status": instance.status.value,
                        "response_time": instance.response_time
                    },
                    "metadata": {
                        "action": "get_instance",
                        "timestamp": datetime.now().isoformat(),
                        "service_id": service_id
                    }
                }
            else:
                return {
                    "result": None,
                    "metadata": {
                        "action": "get_instance",
                        "timestamp": datetime.now().isoformat(),
                        "service_id": service_id
                    }
                }
        
        elif action == "record_call":
            call_data = payload.get("call_data", {})
            
            _orchestrator.record_service_call(
                service_id=call_data.get("service_id", ""),
                instance_id=call_data.get("instance_id", ""),
                success=call_data.get("success", True),
                response_time=call_data.get("response_time", 0.0)
            )
            
            return {
                "result": {
                    "message": "Service call recorded"
                },
                "metadata": {
                    "action": "record_call",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_service_stats":
            service_id = payload.get("service_id", "")
            stats = _orchestrator.get_service_stats(service_id)
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_service_stats",
                    "timestamp": datetime.now().isoformat(),
                    "service_id": service_id
                }
            }
        
        elif action == "get_stats":
            stats = _orchestrator.get_orchestrator_stats()
            
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
        logger.error(f"Error in microservices_orchestrator: {e}")
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
    """Example of how to use the microservices orchestrator skill"""
    
    # Register services
    user_service = await invoke({
        "action": "register_service",
        "service_data": {
            "name": "User Service",
            "version": "1.0.0",
            "description": "User management service",
            "load_balancing": "round_robin",
            "circuit_breaker": True,
            "timeout": 30,
            "retries": 3,
            "health_check_interval": 30
        }
    })
    
    order_service = await invoke({
        "action": "register_service",
        "service_data": {
            "name": "Order Service",
            "version": "1.0.0",
            "description": "Order management service",
            "load_balancing": "least_connections",
            "circuit_breaker": True,
            "timeout": 30,
            "retries": 3,
            "health_check_interval": 30
        }
    })
    
    print(f"Registered services: {user_service['result']['service_id']}, {order_service['result']['service_id']}")
    
    # Register instances
    user_instance1 = await invoke({
        "action": "register_instance",
        "instance_data": {
            "service_id": user_service['result']['service_id'],
            "host": "localhost",
            "port": 3001,
            "weight": 1,
            "metadata": {"region": "us-east-1"},
            "health_check_url": "http://localhost:3001/health"
        }
    })
    
    user_instance2 = await invoke({
        "action": "register_instance",
        "instance_data": {
            "service_id": user_service['result']['service_id'],
            "host": "localhost",
            "port": 3002,
            "weight": 1,
            "metadata": {"region": "us-west-1"},
            "health_check_url": "http://localhost:3002/health"
        }
    })
    
    order_instance1 = await invoke({
        "action": "register_instance",
        "instance_data": {
            "service_id": order_service['result']['service_id'],
            "host": "localhost",
            "port": 3003,
            "weight": 1,
            "metadata": {"region": "us-east-1"},
            "health_check_url": "http://localhost:3003/health"
        }
    })
    
    print(f"Registered instances: {user_instance1['result']['instance_id']}, {user_instance2['result']['instance_id']}, {order_instance1['result']['instance_id']}")
    
    # Add dependencies
    dependency1 = await invoke({
        "action": "add_dependency",
        "dependency_data": {
            "source_service": order_service['result']['service_id'],
            "target_service": user_service['result']['service_id'],
            "dependency_type": "sync",
            "timeout": 30,
            "retry_policy": {"max_retries": 3, "backoff_factor": 1.0}
        }
    })
    
    print(f"Added dependency: {dependency1['result']['dependency_id']}")
    
    # Create service mesh
    mesh = await invoke({
        "action": "create_mesh",
        "mesh_data": {
            "name": "E-commerce Mesh",
            "services": [user_service['result']['service_id'], order_service['result']['service_id']],
            "policies": {
                "traffic_splitting": {"user_service": 0.7, "order_service": 0.3},
                "security": {"mtls": True, "auth": "jwt"}
            }
        }
    })
    
    print(f"Created service mesh: {mesh['result']['mesh_id']}")
    
    # Get service instances
    user_instance = await invoke({
        "action": "get_instance",
        "service_id": user_service['result']['service_id']
    })
    
    print(f"Selected user instance: {user_instance['result']}")
    
    # Record service calls
    await invoke({
        "action": "record_call",
        "call_data": {
            "service_id": user_service['result']['service_id'],
            "instance_id": user_instance['result']['instance_id'],
            "success": True,
            "response_time": 150.0
        }
    })
    
    await invoke({
        "action": "record_call",
        "call_data": {
            "service_id": order_service['result']['service_id'],
            "instance_id": order_instance1['result']['instance_id'],
            "success": False,
            "response_time": 500.0
        }
    })
    
    # Get service statistics
    user_stats = await invoke({
        "action": "get_service_stats",
        "service_id": user_service['result']['service_id']
    })
    
    print(f"User service stats: {user_stats['result']}")
    
    # Get orchestrator statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Orchestrator stats: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
