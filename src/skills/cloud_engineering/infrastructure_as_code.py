#!/usr/bin/env python3
"""
Skill: infrastructure-as-code
Domain: cloud_engineering
Description: Infrastructure as Code management for cloud resources and deployments
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

class CloudProvider(Enum):
    """Cloud providers"""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ALIBABA = "alibaba"
    ORACLE = "oracle"

class ResourceType(Enum):
    """Resource types"""
    COMPUTE = "compute"
    STORAGE = "storage"
    NETWORK = "network"
    DATABASE = "database"
    SECURITY = "security"
    MONITORING = "monitoring"
    CONTAINER = "container"

class DeploymentStatus(Enum):
    """Deployment statuses"""
    PENDING = "pending"
    DEPLOYING = "deploying"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLING_BACK = "rolling_back"
    ROLLED_BACK = "rolled_back"

@dataclass
class CloudResource:
    """Represents a cloud resource"""
    resource_id: str
    name: str
    resource_type: ResourceType
    provider: CloudProvider
    configuration: Dict[str, Any]
    dependencies: List[str]
    tags: Dict[str, str]
    created_at: float
    last_modified: float
    status: str

@dataclass
class DeploymentPlan:
    """Represents a deployment plan"""
    plan_id: str
    name: str
    description: str
    resources: List[CloudResource]
    dependencies: Dict[str, List[str]]
    estimated_cost: float
    created_at: float
    last_modified: float

@dataclass
class DeploymentExecution:
    """Represents a deployment execution"""
    execution_id: str
    plan_id: str
    status: DeploymentStatus
    started_at: float
    completed_at: float | None
    resources_created: List[str]
    resources_failed: List[str]
    total_cost: float
    logs: List[Dict[str, Any]]

class InfrastructureAsCode:
    """Infrastructure as Code management system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the IaC system
        
        Args:
            config: Configuration dictionary with:
                - providers: List of configured cloud providers
                - cost_threshold: Maximum allowed deployment cost
                - parallel_deployments: Number of parallel deployments
        """
        self.providers: Dict[CloudProvider, Dict[str, Any]] = config.get("providers", {})
        self.cost_threshold = config.get("cost_threshold", 1000.0)
        self.parallel_deployments = config.get("parallel_deployments", 3)
        
        self.plans: Dict[str, DeploymentPlan] = {}
        self.executions: Dict[str, DeploymentExecution] = {}
        self.resources: Dict[str, CloudResource] = {}
        
        self.active_deployments = 0
        self.total_deployments = 0
        self.total_cost = 0.0
        
        self.logger = logging.getLogger(__name__)
        
        # Initialize providers
        for provider in CloudProvider:
            if provider not in self.providers:
                self.providers[provider] = {"configured": False, "credentials": None}
    
    def create_deployment_plan(self, 
                              name: str,
                              description: str,
                              resources: List[Dict[str, Any]]) -> str:
        """
        Create a deployment plan
        
        Args:
            name: Plan name
            description: Plan description
            resources: List of resource configurations
            
        Returns:
            Plan ID
        """
        plan_id = str(uuid.uuid4())
        
        # Parse and validate resources
        cloud_resources = []
        total_estimated_cost = 0.0
        
        for resource_config in resources:
            resource = self._parse_resource_config(resource_config)
            cloud_resources.append(resource)
            total_estimated_cost += self._estimate_resource_cost(resource)
        
        # Build dependency graph
        dependencies = self._build_dependency_graph(cloud_resources)
        
        plan = DeploymentPlan(
            plan_id=plan_id,
            name=name,
            description=description,
            resources=cloud_resources,
            dependencies=dependencies,
            estimated_cost=total_estimated_cost,
            created_at=time.time(),
            last_modified=time.time()
        )
        
        self.plans[plan_id] = plan
        self.logger.info(f"Created deployment plan: {plan_id}")
        
        return plan_id
    
    async def invoke_deployment(self, plan_id: str,
                               provider: CloudProvider,
                               dry_run: bool = False) -> str:
        """
        Execute a deployment plan
        
        Args:
            plan_id: ID of the plan to execute
            provider: Cloud provider to use
            dry_run: Whether to perform a dry run
            
        Returns:
            Execution ID
        """
        if plan_id not in self.plans:
            raise ValueError(f"Plan {plan_id} not found")
        
        if self.active_deployments >= self.parallel_deployments:
            raise ValueError("Maximum parallel deployments reached")
        
        plan = self.plans[plan_id]
        
        # Check cost threshold
        if plan.estimated_cost > self.cost_threshold:
            raise ValueError(f"Plan cost {plan.estimated_cost} exceeds threshold {self.cost_threshold}")
        
        # Check provider configuration
        if not self.providers[provider]["configured"]:
            raise ValueError(f"Provider {provider.value} not configured")
        
        execution_id = str(uuid.uuid4())
        
        execution = DeploymentExecution(
            execution_id=execution_id,
            plan_id=plan_id,
            status=DeploymentStatus.PENDING,
            started_at=time.time(),
            completed_at=None,
            resources_created=[],
            resources_failed=[],
            total_cost=0.0,
            logs=[]
        )
        
        self.executions[execution_id] = execution
        self.active_deployments += 1
        self.total_deployments += 1
        
        # Execute deployment asynchronously
        asyncio.create_task(self._execute_deployment_async(execution_id, plan, provider, dry_run))
        
        self.logger.info(f"Started deployment: {execution_id}")
        return execution_id
    
    async def _execute_deployment_async(self, 
                                      execution_id: str,
                                      plan: DeploymentPlan,
                                      provider: CloudProvider,
                                      dry_run: bool):
        """Execute deployment asynchronously"""
        execution = self.executions[execution_id]
        execution.status = DeploymentStatus.DEPLOYING
        
        try:
            # Sort resources by dependencies
            sorted_resources = self._topological_sort(plan.resources, plan.dependencies)
            
            total_cost = 0.0
            
            for resource in sorted_resources:
                execution.logs.append({
                    "timestamp": time.time(),
                    "level": "INFO",
                    "message": f"Creating resource: {resource.name}"
                })
                
                if dry_run:
                    # Simulate resource creation
                    await asyncio.sleep(0.5)
                    resource_id = f"dry-run-{resource.name}-{uuid.uuid4().hex[:8]}"
                    cost = self._estimate_resource_cost(resource)
                else:
                    # Actually create resource
                    resource_id = await self._create_cloud_resource(resource, provider)
                    cost = await self._get_actual_resource_cost(resource_id, provider)
                
                # Track created resources
                execution.resources_created.append(resource_id)
                self.resources[resource_id] = resource
                total_cost += cost
                
                execution.logs.append({
                    "timestamp": time.time(),
                    "level": "INFO",
                    "message": f"Created resource {resource.name}: {resource_id}"
                })
            
            # Complete successfully
            execution.status = DeploymentStatus.SUCCESS
            execution.completed_at = time.time()
            execution.total_cost = total_cost
            self.total_cost += total_cost
            
            self.logger.info(f"Deployment {execution_id} completed successfully")
            
        except Exception as e:
            execution.status = DeploymentStatus.FAILED
            execution.completed_at = time.time()
            execution.logs.append({
                "timestamp": time.time(),
                "level": "ERROR",
                "message": f"Deployment failed: {str(e)}"
            })
            
            # Rollback on failure
            await self._rollback_deployment(execution)
            
            self.logger.error(f"Deployment {execution_id} failed: {e}")
        
        finally:
            self.active_deployments -= 1
    
    async def _create_cloud_resource(self, resource: CloudResource, provider: CloudProvider) -> str:
        """Create a cloud resource"""
        # Simulate API calls to cloud providers
        await asyncio.sleep(1)  # Simulate API latency
        
        # In a real implementation, this would make actual API calls
        if provider == CloudProvider.AWS:
            return await self._create_aws_resource(resource)
        elif provider == CloudProvider.AZURE:
            return await self._create_azure_resource(resource)
        elif provider == CloudProvider.GCP:
            return await self._create_gcp_resource(resource)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    async def _create_aws_resource(self, resource: CloudResource) -> str:
        """Create AWS resource (simulated)"""
        # Simulate AWS API call
        resource_id = f"aws-{resource.resource_type.value}-{uuid.uuid4().hex[:12]}"
        
        # Simulate different resource creation times
        if resource.resource_type == ResourceType.COMPUTE:
            await asyncio.sleep(2)  # EC2 instances take longer
        elif resource.resource_type == ResourceType.DATABASE:
            await asyncio.sleep(3)  # RDS takes even longer
        
        return resource_id
    
    async def _create_azure_resource(self, resource: CloudResource) -> str:
        """Create Azure resource (simulated)"""
        resource_id = f"azure-{resource.resource_type.value}-{uuid.uuid4().hex[:12]}"
        await asyncio.sleep(1.5)
        return resource_id
    
    async def _create_gcp_resource(self, resource: CloudResource) -> str:
        """Create GCP resource (simulated)"""
        resource_id = f"gcp-{resource.resource_type.value}-{uuid.uuid4().hex[:12]}"
        await asyncio.sleep(1.2)
        return resource_id
    
    async def _get_actual_resource_cost(self, resource_id: str, provider: CloudProvider) -> float:
        """Get actual resource cost from cloud provider"""
        # Simulate cost calculation based on resource type and provider
        base_costs = {
            ResourceType.COMPUTE: 0.1,
            ResourceType.STORAGE: 0.01,
            ResourceType.NETWORK: 0.05,
            ResourceType.DATABASE: 0.2,
            ResourceType.SECURITY: 0.02,
            ResourceType.MONITORING: 0.03,
            ResourceType.CONTAINER: 0.08
        }
        
        provider_multipliers = {
            CloudProvider.AWS: 1.0,
            CloudProvider.AZURE: 1.1,
            CloudProvider.GCP: 0.9
        }
        
        # Find the resource
        resource = None
        for res in self.resources.values():
            if any(res.name in resource_id for _ in range(1)):  # Simple matching
                resource = res
                break
        
        if resource:
            base_cost = base_costs.get(resource.resource_type, 0.05)
            multiplier = provider_multipliers.get(provider, 1.0)
            return base_cost * multiplier * 24  # Daily cost
        
        return 0.0
    
    def _parse_resource_config(self, config: Dict[str, Any]) -> CloudResource:
        """Parse resource configuration into CloudResource"""
        resource_id = str(uuid.uuid4())
        
        return CloudResource(
            resource_id=resource_id,
            name=config.get("name", f"resource-{resource_id[:8]}"),
            resource_type=ResourceType(config.get("type", "compute")),
            provider=CloudProvider(config.get("provider", "aws")),
            configuration=config.get("configuration", {}),
            dependencies=config.get("dependencies", []),
            tags=config.get("tags", {}),
            created_at=time.time(),
            last_modified=time.time(),
            status="pending"
        )
    
    def _estimate_resource_cost(self, resource: CloudResource) -> float:
        """Estimate monthly cost for a resource"""
        # Simple cost estimation based on resource type
        cost_estimates = {
            ResourceType.COMPUTE: 50.0,      # EC2, VMs
            ResourceType.STORAGE: 10.0,      # S3, Blob Storage
            ResourceType.NETWORK: 5.0,       # Load Balancers, VPN
            ResourceType.DATABASE: 100.0,    # RDS, Cloud SQL
            ResourceType.SECURITY: 20.0,     # IAM, Security Groups
            ResourceType.MONITORING: 15.0,   # CloudWatch, Monitoring
            ResourceType.CONTAINER: 30.0     # ECS, AKS, GKE
        }
        
        return cost_estimates.get(resource.resource_type, 10.0)
    
    def _build_dependency_graph(self, resources: List[CloudResource]) -> Dict[str, List[str]]:
        """Build dependency graph from resources"""
        dependencies = {}
        
        for resource in resources:
            dependencies[resource.resource_id] = resource.dependencies
        
        return dependencies
    
    def _topological_sort(self, resources: List[CloudResource], 
                         dependencies: Dict[str, List[str]]) -> List[CloudResource]:
        """Sort resources topologically based on dependencies"""
        # Create resource lookup
        resource_lookup = {r.resource_id: r for r in resources}
        
        # Calculate in-degrees
        in_degree = {r.resource_id: 0 for r in resources}
        for resource_id, deps in dependencies.items():
            for dep in deps:
                in_degree[dep] += 1
        
        # Kahn's algorithm for topological sorting
        queue = [r_id for r_id, degree in in_degree.items() if degree == 0]
        sorted_resources = []
        
        while queue:
            current = queue.pop(0)
            sorted_resources.append(resource_lookup[current])
            
            # Remove current from dependencies
            for resource_id, deps in dependencies.items():
                if current in deps:
                    deps.remove(current)
                    in_degree[resource_id] -= 1
                    
                    if in_degree[resource_id] == 0:
                        queue.append(resource_id)
        
        return sorted_resources
    
    async def _rollback_deployment(self, execution: DeploymentExecution):
        """Rollback failed deployment"""
        execution.status = DeploymentStatus.ROLLING_BACK
        
        # Delete created resources in reverse order
        for resource_id in reversed(execution.resources_created):
            try:
                await self._delete_cloud_resource(resource_id)
                execution.logs.append({
                    "timestamp": time.time(),
                    "level": "INFO",
                    "message": f"Rolled back resource: {resource_id}"
                })
            except Exception as e:
                execution.logs.append({
                    "timestamp": time.time(),
                    "level": "ERROR",
                    "message": f"Failed to rollback resource {resource_id}: {str(e)}"
                })
        
        execution.status = DeploymentStatus.ROLLED_BACK
        self.logger.info(f"Deployment {execution.execution_id} rolled back")
    
    async def _delete_cloud_resource(self, resource_id: str):
        """Delete a cloud resource"""
        # Simulate resource deletion
        await asyncio.sleep(0.5)
        
        if resource_id in self.resources:
            del self.resources[resource_id]
    
    def get_deployment_status(self, execution_id: str) -> Dict[str, Any] | None:
        """Get deployment execution status"""
        if execution_id not in self.executions:
            return None
        
        execution = self.executions[execution_id]
        
        return {
            "execution_id": execution.execution_id,
            "plan_id": execution.plan_id,
            "status": execution.status.value,
            "started_at": datetime.fromtimestamp(execution.started_at).isoformat(),
            "completed_at": datetime.fromtimestamp(execution.completed_at).isoformat() if execution.completed_at else None,
            "resources_created": len(execution.resources_created),
            "resources_failed": len(execution.resources_failed),
            "total_cost": execution.total_cost,
            "progress": len(execution.resources_created) / len(self.plans[execution.plan_id].resources) if execution.plan_id in self.plans else 0
        }
    
    def get_deployment_logs(self, execution_id: str) -> List[Dict[str, Any]]:
        """Get deployment execution logs"""
        if execution_id not in self.executions:
            return []
        
        return self.executions[execution_id].logs
    
    def get_resource_inventory(self, provider: CloudProvider | None = None) -> List[Dict[str, Any]]:
        """Get inventory of all resources"""
        inventory = []
        
        for resource_id, resource in self.resources.items():
            if provider is None or resource.provider == provider:
                inventory.append({
                    "resource_id": resource_id,
                    "name": resource.name,
                    "type": resource.resource_type.value,
                    "provider": resource.provider.value,
                    "status": resource.status,
                    "tags": resource.tags,
                    "created_at": datetime.fromtimestamp(resource.created_at).isoformat()
                })
        
        return sorted(inventory, key=lambda x: x["created_at"], reverse=True)
    
    def get_deployment_stats(self) -> Dict[str, Any]:
        """Get deployment statistics"""
        total_executions = len(self.executions)
        successful_executions = len([e for e in self.executions.values() if e.status == DeploymentStatus.SUCCESS])
        failed_executions = len([e for e in self.executions.values() if e.status == DeploymentStatus.FAILED])
        
        return {
            "total_deployments": self.total_deployments,
            "active_deployments": self.active_deployments,
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "success_rate": successful_executions / total_executions if total_executions > 0 else 0.0,
            "total_cost": self.total_cost,
            "average_cost": self.total_cost / successful_executions if successful_executions > 0 else 0.0,
            "configured_providers": [p.value for p, config in self.providers.items() if config["configured"]]
        }

# Global IaC system instance
_iac_system = InfrastructureAsCode({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "create_plan", "execute", "get_status", "get_logs", 
                     "get_inventory", "get_stats", "configure_provider"
            - plan_data: Plan configuration data
            - execution_data: Execution parameters
            - provider_data: Provider configuration
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "create_plan":
            plan_data = payload.get("plan_data", {})
            
            plan_id = _iac_system.create_deployment_plan(
                name=plan_data.get("name", "Deployment Plan"),
                description=plan_data.get("description", ""),
                resources=plan_data.get("resources", [])
            )
            
            return {
                "result": {
                    "plan_id": plan_id,
                    "message": f"Created deployment plan: {plan_id}"
                },
                "metadata": {
                    "action": "create_plan",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "execute":
            execution_data = payload.get("execution_data", {})
            
            execution_id = await _iac_system.execute_deployment(
                plan_id=execution_data.get("plan_id", ""),
                provider=CloudProvider(execution_data.get("provider", "aws")),
                dry_run=execution_data.get("dry_run", False)
            )
            
            return {
                "result": {
                    "execution_id": execution_id,
                    "message": f"Started deployment: {execution_id}"
                },
                "metadata": {
                    "action": "execute",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_status":
            execution_id = payload.get("execution_id", "")
            status = _iac_system.get_deployment_status(execution_id)
            
            return {
                "result": status,
                "metadata": {
                    "action": "get_status",
                    "timestamp": datetime.now().isoformat(),
                    "execution_id": execution_id
                }
            }
        
        elif action == "get_logs":
            execution_id = payload.get("execution_id", "")
            logs = _iac_system.get_deployment_logs(execution_id)
            
            return {
                "result": logs,
                "metadata": {
                    "action": "get_logs",
                    "timestamp": datetime.now().isoformat(),
                    "execution_id": execution_id
                }
            }
        
        elif action == "get_inventory":
            provider = payload.get("provider")
            if provider:
                provider = CloudProvider(provider)
            
            inventory = _iac_system.get_resource_inventory(provider)
            
            return {
                "result": inventory,
                "metadata": {
                    "action": "get_inventory",
                    "timestamp": datetime.now().isoformat(),
                    "provider": provider.value if provider else None
                }
            }
        
        elif action == "get_stats":
            stats = _iac_system.get_deployment_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "configure_provider":
            provider_data = payload.get("provider_data", {})
            
            provider = CloudProvider(provider_data.get("provider", "aws"))
            credentials = provider_data.get("credentials", {})
            
            _iac_system.providers[provider] = {
                "configured": True,
                "credentials": credentials,
                "configured_at": time.time()
            }
            
            return {
                "result": {
                    "provider": provider.value,
                    "configured": True,
                    "message": f"Configured provider: {provider.value}"
                },
                "metadata": {
                    "action": "configure_provider",
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
        logger.error(f"Error in infrastructure_as_code: {e}")
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
    """Example of how to use the infrastructure as code skill"""
    
    # Configure providers
    await invoke({
        "action": "configure_provider",
        "provider_data": {
            "provider": "aws",
            "credentials": {"access_key": "fake-key", "secret_key": "fake-secret"}
        }
    })
    
    # Create a deployment plan
    plan_id = await invoke({
        "action": "create_plan",
        "plan_data": {
            "name": "Web Application Stack",
            "description": "Complete web application infrastructure",
            "resources": [
                {
                    "name": "web-server",
                    "type": "compute",
                    "provider": "aws",
                    "configuration": {"instance_type": "t3.micro", "ami": "ami-12345"},
                    "dependencies": [],
                    "tags": {"environment": "production"}
                },
                {
                    "name": "database",
                    "type": "database",
                    "provider": "aws",
                    "configuration": {"engine": "mysql", "size": "db.t3.micro"},
                    "dependencies": [],
                    "tags": {"environment": "production"}
                }
            ]
        }
    })
    
    print(f"Created plan: {plan_id['result']['plan_id']}")
    
    # Execute deployment
    execution_id = await invoke({
        "action": "execute",
        "execution_data": {
            "plan_id": plan_id['result']['plan_id'],
            "provider": "aws",
            "dry_run": False
        }
    })
    
    print(f"Started execution: {execution_id['result']['execution_id']}")
    
    # Get deployment status
    import time as t
    t.sleep(2)  # Wait for execution
    
    status = await invoke({
        "action": "get_status",
        "execution_id": execution_id['result']['execution_id']
    })
    
    print(f"Deployment status: {status['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
