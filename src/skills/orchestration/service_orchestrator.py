#!/usr/bin/env python3
"""
Skill: service-orchestrator
Domain: orchestration
Description: Service orchestration and microservice management system
"""

import asyncio
import logging
import random
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class ServiceStatus(Enum):
    """Service statuses"""
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"
    DEGRADED = "degraded"

class ServiceType(Enum):
    """Service types"""
    API = "api"
    WORKER = "worker"
    DATABASE = "database"
    CACHE = "cache"
    MESSAGE_QUEUE = "message_queue"
    LOAD_BALANCER = "load_balancer"

class DeploymentStrategy(Enum):
    """Deployment strategies"""
    ROLLING = "rolling"
    BLUE_GREEN = "blue_green"
    CANARY = "canary"
    RECREATE = "recreate"

class HealthCheckType(Enum):
    """Health check types"""
    HTTP = "http"
    TCP = "tcp"
    COMMAND = "command"
    GRPC = "grpc"

@dataclass
class Service:
    """Represents a service"""
    service_id: str
    name: str
    service_type: ServiceType
    version: str
    image: str
    replicas: int
    ports: List[Dict[str, Any]]
    environment: Dict[str, str]
    resources: Dict[str, Any]
    health_check: Dict[str, Any]
    dependencies: List[str]
    status: ServiceStatus
    created_at: float

@dataclass
class ServiceInstance:
    """Represents a service instance"""
    instance_id: str
    service_id: str
    host: str
    port: int
    status: ServiceStatus
    health_score: float
    last_health_check: float
    created_at: float

@dataclass
class ServiceDeployment:
    """Represents a service deployment"""
    deployment_id: str
    service_id: str
    version: str
    strategy: DeploymentStrategy
    replicas: int
    status: str  # pending, in_progress, completed, failed
    started_at: float
    completed_at: Optional[float]
    created_at: float

@dataclass
class ServiceDependency:
    """Represents a service dependency"""
    dependency_id: str
    source_service_id: str
    target_service_id: str
    dependency_type: str  # hard, soft, optional
    timeout: int
    created_at: float

@dataclass
class ServiceMetric:
    """Represents service metrics"""
    metric_id: str
    service_id: str
    instance_id: Optional[str]
    metric_type: str  # cpu, memory, network, response_time, error_rate
    value: float
    timestamp: float
    created_at: float

class ServiceOrchestrator:
    """Service orchestration and microservice management system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the service orchestrator
        
        Args:
            config: Configuration dictionary with:
                - max_services: Maximum number of services
                - health_check_interval: Health check interval
                - deployment_timeout: Deployment timeout
                - auto_scaling_enabled: Enable auto-scaling
        """
        self.max_services = config.get("max_services", 100)
        self.health_check_interval = config.get("health_check_interval", 30)
        self.deployment_timeout = config.get("deployment_timeout", 600)
        self.auto_scaling_enabled = config.get("auto_scaling_enabled", True)
        
        self.services: Dict[str, Service] = {}
        self.service_instances: Dict[str, ServiceInstance] = {}
        self.service_deployments: Dict[str, ServiceDeployment] = {}
        self.service_dependencies: Dict[str, ServiceDependency] = {}
        self.service_metrics: Dict[str, List[ServiceMetric]] = {}
        
        self.orchestrator_stats = {
            "total_services": 0,
            "running_services": 0,
            "failed_services": 0,
            "total_instances": 0,
            "healthy_instances": 0,
            "total_deployments": 0,
            "completed_deployments": 0,
            "failed_deployments": 0
        }
        
        self.service_registry: Dict[str, Dict[str, Any]] = {}
        self.load_balancers: Dict[str, Dict[str, Any]] = {}
        
        self.logger = logging.getLogger(__name__)
        
        # Start background services
        self._service_monitor_task = asyncio.create_task(self._service_monitor_loop())
        self._health_checker_task = asyncio.create_task(self._health_checker_loop())
        self._deployment_processor_task = asyncio.create_task(self._deployment_processor_loop())
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    def register_service(self,
                        name: str,
                        service_type: ServiceType,
                        version: str,
                        image: str,
                        replicas: int = 1,
                        ports: Optional[List[Dict[str, Any]]] = None,
                        environment: Optional[Dict[str, str]] = None,
                        resources: Optional[Dict[str, Any]] = None,
                        health_check: Optional[Dict[str, Any]] = None,
                        dependencies: Optional[List[str]] = None) -> str:
        """
        Register a service
        
        Args:
            name: Service name
            service_type: Type of service
            version: Service version
            image: Docker image
            replicas: Number of replicas
            ports: Port configurations
            environment: Environment variables
            resources: Resource limits
            health_check: Health check configuration
            dependencies: Service dependencies
            
        Returns:
            Service ID
        """
        if len(self.services) >= self.max_services:
            raise ValueError("Maximum number of services reached")
        
        service_id = str(uuid.uuid4())
        
        service = Service(
            service_id=service_id,
            name=name,
            service_type=service_type,
            version=version,
            image=image,
            replicas=replicas,
            ports=ports or [],
            environment=environment or {},
            resources=resources or {},
            health_check=health_check or {},
            dependencies=dependencies or [],
            status=ServiceStatus.STOPPED,
            created_at=time.time()
        )
        
        self.services[service_id] = service
        self.orchestrator_stats["total_services"] += 1
        
        # Create initial instances
        for i in range(replicas):
            instance_id = str(uuid.uuid4())
            instance = ServiceInstance(
                instance_id=instance_id,
                service_id=service_id,
                host=f"service-{service_id[:8]}-{i}",
                port=8080 + i,
                status=ServiceStatus.STOPPED,
                health_score=0.0,
                last_health_check=0.0,
                created_at=time.time()
            )
            self.service_instances[instance_id] = instance
        
        self.orchestrator_stats["total_instances"] += replicas
        
        self.logger.info(f"Registered service: {service_id} ({name})")
        return service_id
    
    def start_service(self, service_id: str) -> bool:
        """Start a service"""
        if service_id not in self.services:
            return False
        
        service = self.services[service_id]
        service.status = ServiceStatus.STARTING
        
        # Start all instances
        for instance_id, instance in self.service_instances.items():
            if instance.service_id == service_id:
                instance.status = ServiceStatus.STARTING
                # Simulate startup time
                asyncio.create_task(self._simulate_service_startup(instance_id))
        
        self.logger.info(f"Starting service: {service_id}")
        return True
    
    def stop_service(self, service_id: str) -> bool:
        """Stop a service"""
        if service_id not in self.services:
            return False
        
        service = self.services[service_id]
        service.status = ServiceStatus.STOPPING
        
        # Stop all instances
        for instance_id, instance in self.service_instances.items():
            if instance.service_id == service_id:
                instance.status = ServiceStatus.STOPPING
                # Simulate shutdown time
                asyncio.create_task(self._simulate_service_shutdown(instance_id))
        
        self.logger.info(f"Stopping service: {service_id}")
        return True
    
    def deploy_service(self,
                      service_id: str,
                      version: str,
                      strategy: DeploymentStrategy = DeploymentStrategy.ROLLING,
                      replicas: Optional[int] = None) -> str:
        """
        Deploy a service
        
        Args:
            service_id: Service ID
            version: New version
            strategy: Deployment strategy
            replicas: New replica count
            
        Returns:
            Deployment ID
        """
        if service_id not in self.services:
            raise ValueError(f"Service {service_id} not found")
        
        deployment_id = str(uuid.uuid4())
        
        deployment = ServiceDeployment(
            deployment_id=deployment_id,
            service_id=service_id,
            version=version,
            strategy=strategy,
            replicas=replicas or self.services[service_id].replicas,
            status="pending",
            started_at=time.time(),
            completed_at=None,
            created_at=time.time()
        )
        
        self.service_deployments[deployment_id] = deployment
        self.orchestrator_stats["total_deployments"] += 1
        
        # Execute deployment
        asyncio.create_task(self._execute_deployment(deployment_id, deployment))
        
        self.logger.info(f"Started deployment: {deployment_id} for service {service_id}")
        return deployment_id
    
    def get_service_status(self, service_id: str) -> Optional[Dict[str, Any]]:
        """Get service status"""
        if service_id not in self.services:
            return None
        
        service = self.services[service_id]
        instances = [
            inst for inst in self.service_instances.values()
            if inst.service_id == service_id
        ]
        
        healthy_count = sum(1 for inst in instances if inst.status == ServiceStatus.RUNNING and inst.health_score > 0.8)
        
        return {
            "service_id": service.service_id,
            "name": service.name,
            "type": service.service_type.value,
            "version": service.version,
            "status": service.status.value,
            "replicas": service.replicas,
            "healthy_instances": healthy_count,
            "total_instances": len(instances),
            "dependencies": service.dependencies,
            "created_at": datetime.fromtimestamp(service.created_at).isoformat()
        }
    
    def get_service_metrics(self, service_id: str, metric_type: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get service metrics"""
        if service_id not in self.service_metrics:
            return []
        
        metrics = self.service_metrics[service_id]
        
        if metric_type:
            metrics = [m for m in metrics if m.metric_type == metric_type]
        
        # Return last N metrics
        return [
            {
                "metric_id": m.metric_id,
                "type": m.metric_type,
                "value": m.value,
                "timestamp": datetime.fromtimestamp(m.timestamp).isoformat(),
                "instance_id": m.instance_id
            }
            for m in sorted(metrics, key=lambda x: x.timestamp, reverse=True)[:limit]
        ]
    
    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            "total_services": self.orchestrator_stats["total_services"],
            "running_services": self.orchestrator_stats["running_services"],
            "failed_services": self.orchestrator_stats["failed_services"],
            "total_instances": self.orchestrator_stats["total_instances"],
            "healthy_instances": self.orchestrator_stats["healthy_instances"],
            "total_deployments": self.orchestrator_stats["total_deployments"],
            "completed_deployments": self.orchestrator_stats["completed_deployments"],
            "failed_deployments": self.orchestrator_stats["failed_deployments"],
            "total_dependencies": len(self.service_dependencies),
            "registered_services": len(self.service_registry)
        }
    
    def add_service_dependency(self,
                              source_service_id: str,
                              target_service_id: str,
                              dependency_type: str = "hard",
                              timeout: int = 30) -> str:
        """
        Add service dependency
        
        Args:
            source_service_id: Source service ID
            target_service_id: Target service ID
            dependency_type: Type of dependency
            timeout: Timeout in seconds
            
        Returns:
            Dependency ID
        """
        dependency_id = str(uuid.uuid4())
        
        dependency = ServiceDependency(
            dependency_id=dependency_id,
            source_service_id=source_service_id,
            target_service_id=target_service_id,
            dependency_type=dependency_type,
            timeout=timeout,
            created_at=time.time()
        )
        
        self.service_dependencies[dependency_id] = dependency
        self.logger.info(f"Added dependency: {source_service_id} -> {target_service_id}")
        return dependency_id
    
    def register_service_endpoint(self,
                                 service_id: str,
                                 endpoint: str,
                                 instance_id: str,
                                 port: int) -> bool:
        """Register service endpoint"""
        if service_id not in self.service_registry:
            self.service_registry[service_id] = {}
        
        self.service_registry[service_id][instance_id] = {
            "endpoint": endpoint,
            "port": port,
            "registered_at": time.time()
        }
        
        self.logger.info(f"Registered endpoint for service {service_id}: {endpoint}:{port}")
        return True
    
    async def _simulate_service_startup(self, instance_id: str):
        """Simulate service startup"""
        instance = self.service_instances[instance_id]
        service = self.services[instance.service_id]
        
        # Simulate startup time
        await asyncio.sleep(2)
        
        instance.status = ServiceStatus.RUNNING
        instance.health_score = 1.0
        instance.last_health_check = time.time()
        
        # Update service status
        service.status = ServiceStatus.RUNNING
        self.orchestrator_stats["running_services"] += 1
        self.orchestrator_stats["healthy_instances"] += 1
        
        self.logger.info(f"Service instance {instance_id} started")
    
    async def _simulate_service_shutdown(self, instance_id: str):
        """Simulate service shutdown"""
        instance = self.service_instances[instance_id]
        service = self.services[instance.service_id]
        
        # Simulate shutdown time
        await asyncio.sleep(1)
        
        instance.status = ServiceStatus.STOPPED
        instance.health_score = 0.0
        
        # Update service status
        service.status = ServiceStatus.STOPPED
        self.orchestrator_stats["running_services"] -= 1
        self.orchestrator_stats["healthy_instances"] -= 1
        
        self.logger.info(f"Service instance {instance_id} stopped")
    
    async def _execute_deployment(self, deployment_id: str, deployment: ServiceDeployment):
        """Execute service deployment"""
        deployment.status = "in_progress"
        
        service = self.services[deployment.service_id]
        old_version = service.version
        
        try:
            # Update service version
            service.version = deployment.version
            
            if deployment.replicas != service.replicas:
                # Scale service
                await self._scale_service(deployment.service_id, deployment.replicas)
            
            # Simulate deployment time
            await asyncio.sleep(5)
            
            deployment.status = "completed"
            deployment.completed_at = time.time()
            self.orchestrator_stats["completed_deployments"] += 1
            
            self.logger.info(f"Deployment {deployment_id} completed successfully")
            
        except Exception as e:
            deployment.status = "failed"
            deployment.completed_at = time.time()
            service.version = old_version  # Rollback
            self.orchestrator_stats["failed_deployments"] += 1
            
            self.logger.error(f"Deployment {deployment_id} failed: {e}")
    
    async def _scale_service(self, service_id: str, new_replicas: int):
        """Scale service up or down"""
        service = self.services[service_id]
        current_replicas = service.replicas
        
        if new_replicas > current_replicas:
            # Scale up
            for i in range(current_replicas, new_replicas):
                instance_id = str(uuid.uuid4())
                instance = ServiceInstance(
                    instance_id=instance_id,
                    service_id=service_id,
                    host=f"service-{service_id[:8]}-{i}",
                    port=8080 + i,
                    status=ServiceStatus.STOPPED,
                    health_score=0.0,
                    last_health_check=0.0,
                    created_at=time.time()
                )
                self.service_instances[instance_id] = instance
                await self._simulate_service_startup(instance_id)
        elif new_replicas < current_replicas:
            # Scale down
            instances = [
                inst for inst in self.service_instances.values()
                if inst.service_id == service_id
            ]
            instances_to_remove = instances[new_replicas:]
            
            for instance in instances_to_remove:
                await self._simulate_service_shutdown(instance.instance_id)
                del self.service_instances[instance.instance_id]
        
        service.replicas = new_replicas
        self.orchestrator_stats["total_instances"] = len(self.service_instances)
    
    async def _service_monitor_loop(self):
        """Background service monitor loop"""
        while True:
            try:
                await self._monitor_services()
                await asyncio.sleep(30)
            except Exception as e:
                self.logger.error(f"Error in service monitor loop: {e}")
                await asyncio.sleep(30)
    
    async def _monitor_services(self):
        """Monitor service health and status"""
        for service_id, service in self.services.items():
            instances = [
                inst for inst in self.service_instances.values()
                if inst.service_id == service_id
            ]
            
            running_count = sum(1 for inst in instances if inst.status == ServiceStatus.RUNNING)
            healthy_count = sum(1 for inst in instances if inst.health_score > 0.8)
            
            # Update service status
            if running_count == 0:
                service.status = ServiceStatus.STOPPED
            elif healthy_count < len(instances) * 0.8:
                service.status = ServiceStatus.DEGRADED
            else:
                service.status = ServiceStatus.RUNNING
    
    async def _health_checker_loop(self):
        """Background health checker loop"""
        while True:
            try:
                await self._check_health()
                await asyncio.sleep(self.health_check_interval)
            except Exception as e:
                self.logger.error(f"Error in health checker loop: {e}")
                await asyncio.sleep(self.health_check_interval)
    
    async def _check_health(self):
        """Check service health"""
        for instance_id, instance in self.service_instances.items():
            if instance.status == ServiceStatus.RUNNING:
                # Simulate health check
                health_score = random.uniform(0.7, 1.0)
                instance.health_score = health_score
                instance.last_health_check = time.time()
                
                # Record metrics
                self._record_metric(instance.service_id, instance_id, "health_score", health_score)
    
    def _record_metric(self, service_id: str, instance_id: str, metric_type: str, value: float):
        """Record service metric"""
        if service_id not in self.service_metrics:
            self.service_metrics[service_id] = []
        
        metric = ServiceMetric(
            metric_id=str(uuid.uuid4()),
            service_id=service_id,
            instance_id=instance_id,
            metric_type=metric_type,
            value=value,
            timestamp=time.time(),
            created_at=time.time()
        )
        
        self.service_metrics[service_id].append(metric)
        
        # Keep only last 1000 metrics per service
        if len(self.service_metrics[service_id]) > 1000:
            self.service_metrics[service_id] = self.service_metrics[service_id][-1000:]
    
    async def _deployment_processor_loop(self):
        """Background deployment processor loop"""
        while True:
            try:
                await self._process_deployments()
                await asyncio.sleep(10)
            except Exception as e:
                self.logger.error(f"Error in deployment processor loop: {e}")
                await asyncio.sleep(10)
    
    async def _process_deployments(self):
        """Process pending deployments"""
        current_time = time.time()
        
        for deployment_id, deployment in list(self.service_deployments.items()):
            if deployment.status == "pending":
                if current_time - deployment.started_at > self.deployment_timeout:
                    deployment.status = "failed"
                    deployment.completed_at = current_time
                    self.orchestrator_stats["failed_deployments"] += 1
    
    async def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            try:
                await self._cleanup_old_metrics()
                await asyncio.sleep(3600)  # Run every hour
            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(3600)
    
    async def _cleanup_old_metrics(self):
        """Clean up old metrics"""
        cutoff_time = time.time() - (24 * 3600)  # 24 hours ago
        
        for service_id, metrics in self.service_metrics.items():
            self.service_metrics[service_id] = [
                m for m in metrics if m.timestamp > cutoff_time
            ]

# Global service orchestrator instance
_service_orchestrator = ServiceOrchestrator({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "register_service", "start_service", "stop_service", 
                     "deploy_service", "get_status", "get_metrics", "get_stats",
                     "add_dependency", "register_endpoint"
            - service_data: Service configuration
            - deployment_data: Deployment configuration
            - dependency_data: Dependency configuration
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "register_service":
            service_data = payload.get("service_data", {})
            
            service_id = _service_orchestrator.register_service(
                name=service_data.get("name", "Service"),
                service_type=ServiceType(service_data.get("service_type", "api")),
                version=service_data.get("version", "1.0.0"),
                image=service_data.get("image", "nginx:latest"),
                replicas=service_data.get("replicas", 1),
                ports=service_data.get("ports"),
                environment=service_data.get("environment"),
                resources=service_data.get("resources"),
                health_check=service_data.get("health_check"),
                dependencies=service_data.get("dependencies")
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
        
        elif action == "start_service":
            service_id = payload.get("service_id", "")
            success = _service_orchestrator.start_service(service_id)
            
            return {
                "result": {
                    "success": success,
                    "message": f"Service started: {service_id}" if success else "Start failed"
                },
                "metadata": {
                    "action": "start_service",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "stop_service":
            service_id = payload.get("service_id", "")
            success = _service_orchestrator.stop_service(service_id)
            
            return {
                "result": {
                    "success": success,
                    "message": f"Service stopped: {service_id}" if success else "Stop failed"
                },
                "metadata": {
                    "action": "stop_service",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "deploy_service":
            deployment_data = payload.get("deployment_data", {})
            
            deployment_id = _service_orchestrator.deploy_service(
                service_id=deployment_data.get("service_id", ""),
                version=deployment_data.get("version", "1.0.1"),
                strategy=DeploymentStrategy(deployment_data.get("strategy", "rolling")),
                replicas=deployment_data.get("replicas")
            )
            
            return {
                "result": {
                    "deployment_id": deployment_id,
                    "message": f"Started deployment: {deployment_id}"
                },
                "metadata": {
                    "action": "deploy_service",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_status":
            service_id = payload.get("service_id", "")
            status = _service_orchestrator.get_service_status(service_id)
            
            return {
                "result": status,
                "metadata": {
                    "action": "get_status",
                    "timestamp": datetime.now().isoformat(),
                    "service_id": service_id
                }
            }
        
        elif action == "get_metrics":
            service_id = payload.get("service_id", "")
            metric_type = payload.get("metric_type")
            limit = payload.get("limit", 100)
            metrics = _service_orchestrator.get_service_metrics(service_id, metric_type, limit)
            
            return {
                "result": metrics,
                "metadata": {
                    "action": "get_metrics",
                    "timestamp": datetime.now().isoformat(),
                    "service_id": service_id
                }
            }
        
        elif action == "get_stats":
            stats = _service_orchestrator.get_orchestrator_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "add_dependency":
            dependency_data = payload.get("dependency_data", {})
            
            dependency_id = _service_orchestrator.add_service_dependency(
                source_service_id=dependency_data.get("source_service_id", ""),
                target_service_id=dependency_data.get("target_service_id", ""),
                dependency_type=dependency_data.get("dependency_type", "hard"),
                timeout=dependency_data.get("timeout", 30)
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
        
        elif action == "register_endpoint":
            service_id = payload.get("service_id", "")
            endpoint = payload.get("endpoint", "")
            instance_id = payload.get("instance_id", "")
            port = payload.get("port", 8080)
            success = _service_orchestrator.register_service_endpoint(service_id, endpoint, instance_id, port)
            
            return {
                "result": {
                    "success": success,
                    "message": f"Endpoint registered: {endpoint}:{port}" if success else "Registration failed"
                },
                "metadata": {
                    "action": "register_endpoint",
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
        logger.error(f"Error in service_orchestrator: {e}")
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
    """Example of how to use the service orchestrator skill"""
    
    # Register services
    api_service = await invoke({
        "action": "register_service",
        "service_data": {
            "name": "API Gateway",
            "service_type": "api",
            "version": "1.0.0",
            "image": "nginx:latest",
            "replicas": 3,
            "ports": [{"port": 80, "target_port": 8080}],
            "environment": {"ENV": "production"},
            "resources": {"cpu": "100m", "memory": "128Mi"},
            "health_check": {"type": "http", "path": "/health", "interval": 30},
            "dependencies": []
        }
    })
    
    db_service = await invoke({
        "action": "register_service",
        "service_data": {
            "name": "Database",
            "service_type": "database",
            "version": "1.0.0",
            "image": "postgres:13",
            "replicas": 1,
            "ports": [{"port": 5432, "target_port": 5432}],
            "environment": {"POSTGRES_DB": "app"},
            "resources": {"cpu": "200m", "memory": "256Mi"},
            "health_check": {"type": "tcp", "port": 5432, "interval": 30},
            "dependencies": []
        }
    })
    
    cache_service = await invoke({
        "action": "register_service",
        "service_data": {
            "name": "Redis Cache",
            "service_type": "cache",
            "version": "1.0.0",
            "image": "redis:6",
            "replicas": 2,
            "ports": [{"port": 6379, "target_port": 6379}],
            "environment": {},
            "resources": {"cpu": "50m", "memory": "64Mi"},
            "health_check": {"type": "tcp", "port": 6379, "interval": 30},
            "dependencies": []
        }
    })
    
    print(f"Registered services: {api_service['result']['service_id']}, {db_service['result']['service_id']}, {cache_service['result']['service_id']}")
    
    # Add dependencies
    api_db_dep = await invoke({
        "action": "add_dependency",
        "dependency_data": {
            "source_service_id": api_service['result']['service_id'],
            "target_service_id": db_service['result']['service_id'],
            "dependency_type": "hard",
            "timeout": 30
        }
    })
    
    api_cache_dep = await invoke({
        "action": "add_dependency",
        "dependency_data": {
            "source_service_id": api_service['result']['service_id'],
            "target_service_id": cache_service['result']['service_id'],
            "dependency_type": "soft",
            "timeout": 10
        }
    })
    
    print(f"Added dependencies: {api_db_dep['result']['dependency_id']}, {api_cache_dep['result']['dependency_id']}")
    
    # Start services
    await invoke({"action": "start_service", "service_id": db_service['result']['service_id']})
    await invoke({"action": "start_service", "service_id": cache_service['result']['service_id']})
    await invoke({"action": "start_service", "service_id": api_service['result']['service_id']})
    
    print("Started all services")
    
    # Register endpoints
    await invoke({
        "action": "register_endpoint",
        "service_id": api_service['result']['service_id'],
        "endpoint": "api.example.com",
        "instance_id": "instance-1",
        "port": 80
    })
    
    await invoke({
        "action": "register_endpoint",
        "service_id": db_service['result']['service_id'],
        "endpoint": "db.example.com",
        "instance_id": "instance-1",
        "port": 5432
    })
    
    print("Registered service endpoints")
    
    # Get service status
    api_status = await invoke({
        "action": "get_status",
        "service_id": api_service['result']['service_id']
    })
    
    print(f"API Service status: {api_status['result']['status']} - {api_status['result']['healthy_instances']}/{api_status['result']['total_instances']} instances healthy")
    
    # Deploy new version
    deployment = await invoke({
        "action": "deploy_service",
        "deployment_data": {
            "service_id": api_service['result']['service_id'],
            "version": "1.1.0",
            "strategy": "rolling",
            "replicas": 5
        }
    })
    
    print(f"Started deployment: {deployment['result']['deployment_id']}")
    
    # Monitor deployment
    import time as t
    for i in range(10):
        status = await invoke({
            "action": "get_status",
            "service_id": api_service['result']['service_id']
        })
        
        if status['result']:
            print(f"Deployment progress: {status['result']['version']} - {status['result']['healthy_instances']}/{status['result']['total_instances']} instances")
            
            if status['result']['version'] == "1.1.0":
                break
        
        t.sleep(1)
    
    # Get service metrics
    metrics = await invoke({
        "action": "get_metrics",
        "service_id": api_service['result']['service_id'],
        "metric_type": "health_score",
        "limit": 10
    })
    
    print(f"Health metrics: {len(metrics['result'])} data points")
    
    # Get orchestrator statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Orchestrator stats: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
