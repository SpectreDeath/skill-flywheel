#!/usr/bin/env python3
"""
Skill: deployment-automation
Domain: devops
Description: Automated deployment system for applications and infrastructure
"""

import asyncio
import hashlib
import logging
import os
import shutil
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import requests
import yaml

logger = logging.getLogger(__name__)

class DeploymentStatus(Enum):
    """Deployment execution statuses"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    CANCELLED = "cancelled"

class DeploymentType(Enum):
    """Types of deployments"""
    BLUE_GREEN = "blue_green"
    ROLLING = "rolling"
    CANARY = "canary"
    RECREATE = "recreate"

class EnvironmentType(Enum):
    """Types of deployment environments"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

class DeploymentStrategy(Enum):
    """Deployment strategies"""
    CONTAINER = "container"
    VM = "vm"
    SERVERLESS = "serverless"
    HYBRID = "hybrid"

@dataclass
class DeploymentTarget:
    """Represents a deployment target"""
    target_id: str
    name: str
    environment: EnvironmentType
    target_type: str  # kubernetes, docker, vm, etc.
    connection_config: Dict[str, Any]
    health_check_url: Optional[str]
    created_at: float

@dataclass
class DeploymentPackage:
    """Represents a deployment package"""
    package_id: str
    name: str
    version: str
    package_type: str  # docker, zip, tar, etc.
    artifact_path: str
    checksum: str
    size: int
    dependencies: List[str]
    created_at: float

@dataclass
class Deployment:
    """Represents a deployment configuration"""
    deployment_id: str
    name: str
    description: str
    deployment_type: DeploymentType
    strategy: DeploymentStrategy
    targets: List[str]
    package_id: str
    rollback_enabled: bool
    health_check_enabled: bool
    created_at: float
    last_modified: float

@dataclass
class DeploymentExecution:
    """Represents a deployment execution"""
    execution_id: str
    deployment_id: str
    status: DeploymentStatus
    environment: EnvironmentType
    package_version: str
    started_at: float
    completed_at: Optional[float]
    targets_deployed: int
    targets_failed: int
    total_duration: float
    rollback_available: bool
    logs: List[Dict[str, Any]]

@dataclass
class HealthCheck:
    """Represents a health check result"""
    check_id: str
    target_id: str
    status: str  # healthy, unhealthy, degraded
    response_time: float
    error_message: Optional[str]
    checked_at: float

class DeploymentAutomation:
    """Automated deployment system for applications and infrastructure"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the deployment automation system
        
        Args:
            config: Configuration dictionary with:
                - deployments_path: Path to deployment configurations
                - packages_path: Path to deployment packages
                - max_concurrent_deployments: Maximum concurrent deployments
                - health_check_interval: Health check interval in seconds
        """
        self.deployments_path = config.get("deployments_path", "./deployments")
        self.packages_path = config.get("packages_path", "./packages")
        self.max_concurrent_deployments = config.get("max_concurrent_deployments", 3)
        self.health_check_interval = config.get("health_check_interval", 30)
        
        self.deployments: Dict[str, Deployment] = {}
        self.deployment_targets: Dict[str, DeploymentTarget] = {}
        self.deployment_packages: Dict[str, DeploymentPackage] = {}
        self.executions: Dict[str, DeploymentExecution] = {}
        self.health_checks: Dict[str, HealthCheck] = {}
        
        self.active_deployments = 0
        self.total_deployments = 0
        self.deployment_stats = {
            "total_deployments": 0,
            "successful_deployments": 0,
            "failed_deployments": 0,
            "rolled_back_deployments": 0,
            "average_deployment_time": 0.0,
            "success_rate": 0.0
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Ensure directories exist
        os.makedirs(self.deployments_path, exist_ok=True)
        os.makedirs(self.packages_path, exist_ok=True)
        
        # Start background services
        self._deployment_task = asyncio.create_task(self._deployment_loop())
        self._health_check_task = asyncio.create_task(self._health_check_loop())
    
    def create_deployment_target(self,
                                name: str,
                                environment: EnvironmentType,
                                target_type: str,
                                connection_config: Dict[str, Any],
                                health_check_url: Optional[str] = None) -> str:
        """
        Create a deployment target
        
        Args:
            name: Target name
            environment: Environment type
            target_type: Target type (kubernetes, docker, vm, etc.)
            connection_config: Connection configuration
            health_check_url: Health check URL (optional)
            
        Returns:
            Target ID
        """
        target_id = str(uuid.uuid4())
        
        target = DeploymentTarget(
            target_id=target_id,
            name=name,
            environment=environment,
            target_type=target_type,
            connection_config=connection_config,
            health_check_url=health_check_url,
            created_at=time.time()
        )
        
        self.deployment_targets[target_id] = target
        self.logger.info(f"Created deployment target: {target_id}")
        return target_id
    
    def create_deployment_package(self,
                                 name: str,
                                 version: str,
                                 package_type: str,
                                 artifact_path: str,
                                 dependencies: Optional[List[str]] = None) -> str:
        """
        Create a deployment package
        
        Args:
            name: Package name
            version: Package version
            package_type: Package type (docker, zip, tar, etc.)
            artifact_path: Path to package artifact
            dependencies: List of package dependencies
            
        Returns:
            Package ID
        """
        if not os.path.exists(artifact_path):
            raise ValueError(f"Artifact file {artifact_path} does not exist")
        
        package_id = str(uuid.uuid4())
        file_size = os.path.getsize(artifact_path)
        checksum = self._calculate_file_checksum(artifact_path)
        
        # Move package to packages directory
        package_path = os.path.join(self.packages_path, f"{package_id}_{name}_{version}.{package_type}")
        shutil.copy2(artifact_path, package_path)
        
        package = DeploymentPackage(
            package_id=package_id,
            name=name,
            version=version,
            package_type=package_type,
            artifact_path=package_path,
            checksum=checksum,
            size=file_size,
            dependencies=dependencies or [],
            created_at=time.time()
        )
        
        self.deployment_packages[package_id] = package
        self.logger.info(f"Created deployment package: {package_id}")
        return package_id
    
    def create_deployment(self,
                         name: str,
                         description: str,
                         deployment_type: DeploymentType,
                         strategy: DeploymentStrategy,
                         targets: List[str],
                         package_id: str,
                         rollback_enabled: bool = True,
                         health_check_enabled: bool = True) -> str:
        """
        Create a deployment configuration
        
        Args:
            name: Deployment name
            description: Deployment description
            deployment_type: Type of deployment
            strategy: Deployment strategy
            targets: List of target IDs
            package_id: Package ID
            rollback_enabled: Whether rollback is enabled
            health_check_enabled: Whether health checks are enabled
            
        Returns:
            Deployment ID
        """
        deployment_id = str(uuid.uuid4())
        
        deployment = Deployment(
            deployment_id=deployment_id,
            name=name,
            description=description,
            deployment_type=deployment_type,
            strategy=strategy,
            targets=targets,
            package_id=package_id,
            rollback_enabled=rollback_enabled,
            health_check_enabled=health_check_enabled,
            created_at=time.time(),
            last_modified=time.time()
        )
        
        self.deployments[deployment_id] = deployment
        self.deployment_stats["total_deployments"] += 1
        
        # Save deployment configuration
        self._save_deployment_config(deployment)
        
        self.logger.info(f"Created deployment: {deployment_id}")
        return deployment_id
    
    async def invoke_deployment(self,
                                deployment_id: str,
                                environment: EnvironmentType,
                                package_version: Optional[str] = None) -> str:
        """
        Execute a deployment
        
        Args:
            deployment_id: Deployment ID
            environment: Target environment
            package_version: Specific package version (optional)
            
        Returns:
            Execution ID
        """
        if deployment_id not in self.deployments:
            raise ValueError(f"Deployment {deployment_id} not found")
        
        if self.active_deployments >= self.max_concurrent_deployments:
            raise ValueError("Maximum concurrent deployments reached")
        
        deployment = self.deployments[deployment_id]
        package = self.deployment_packages[deployment.package_id]
        
        execution_id = str(uuid.uuid4())
        
        execution = DeploymentExecution(
            execution_id=execution_id,
            deployment_id=deployment_id,
            status=DeploymentStatus.PENDING,
            environment=environment,
            package_version=package_version or package.version,
            started_at=time.time(),
            completed_at=None,
            targets_deployed=0,
            targets_failed=0,
            total_duration=0.0,
            rollback_available=deployment.rollback_enabled,
            logs=[]
        )
        
        self.executions[execution_id] = execution
        self.active_deployments += 1
        self.total_deployments += 1
        
        # Execute deployment asynchronously
        asyncio.create_task(self._execute_deployment_async(execution_id, deployment, environment))
        
        self.logger.info(f"Started deployment execution: {execution_id}")
        return execution_id
    
    async def rollback_deployment(self, execution_id: str) -> bool:
        """
        Rollback a deployment
        
        Args:
            execution_id: Execution ID to rollback
            
        Returns:
            Success status
        """
        if execution_id not in self.executions:
            return False
        
        execution = self.executions[execution_id]
        deployment = self.deployments[execution.deployment_id]
        
        if not deployment.rollback_enabled:
            self.logger.warning(f"Rollback not enabled for deployment {deployment.deployment_id}")
            return False
        
        try:
            execution.status = DeploymentStatus.ROLLING_BACK
            execution.logs.append({
                "timestamp": time.time(),
                "level": "INFO",
                "message": "Starting deployment rollback"
            })
            
            # Execute rollback based on deployment type
            if deployment.deployment_type == DeploymentType.BLUE_GREEN:
                await self._rollback_blue_green(execution, deployment)
            elif deployment.deployment_type == DeploymentType.ROLLING:
                await self._rollback_rolling(execution, deployment)
            elif deployment.deployment_type == DeploymentType.CANARY:
                await self._rollback_canary(execution, deployment)
            else:
                await self._rollback_recreate(execution, deployment)
            
            execution.status = DeploymentStatus.ROLLED_BACK
            execution.completed_at = time.time()
            execution.total_duration = execution.completed_at - execution.started_at
            self.deployment_stats["rolled_back_deployments"] += 1
            
            self.active_deployments -= 1
            self.logger.info(f"Deployment rollback completed: {execution_id}")
            return True
            
        except Exception as e:
            execution.status = DeploymentStatus.FAILED
            execution.logs.append({
                "timestamp": time.time(),
                "level": "ERROR",
                "message": f"Rollback failed: {str(e)}"
            })
            
            self.active_deployments -= 1
            self.logger.error(f"Deployment rollback failed: {execution_id} - {e}")
            return False
    
    def get_deployment_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get deployment execution status"""
        if execution_id not in self.executions:
            return None
        
        execution = self.executions[execution_id]
        
        return {
            "execution_id": execution.execution_id,
            "deployment_id": execution.deployment_id,
            "status": execution.status.value,
            "environment": execution.environment.value,
            "package_version": execution.package_version,
            "started_at": datetime.fromtimestamp(execution.started_at).isoformat(),
            "completed_at": datetime.fromtimestamp(execution.completed_at).isoformat() if execution.completed_at else None,
            "targets_deployed": execution.targets_deployed,
            "targets_failed": execution.targets_failed,
            "total_duration": execution.total_duration,
            "rollback_available": execution.rollback_available
        }
    
    def get_deployment_stats(self) -> Dict[str, Any]:
        """Get deployment statistics"""
        total_executions = len(self.executions)
        successful_executions = len([e for e in self.executions.values() if e.status == DeploymentStatus.COMPLETED])
        failed_executions = len([e for e in self.executions.values() if e.status == DeploymentStatus.FAILED])
        
        return {
            "total_deployments": self.deployment_stats["total_deployments"],
            "active_deployments": self.active_deployments,
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "rolled_back_executions": self.deployment_stats["rolled_back_deployments"],
            "success_rate": successful_executions / total_executions if total_executions > 0 else 0.0,
            "average_deployment_time": self.deployment_stats["average_deployment_time"],
            "max_concurrent_deployments": self.max_concurrent_deployments,
            "total_targets": len(self.deployment_targets),
            "total_packages": len(self.deployment_packages)
        }
    
    async def _execute_deployment_async(self, execution_id: str, deployment: Deployment, environment: EnvironmentType):
        """Execute deployment asynchronously"""
        execution = self.executions[execution_id]
        execution.status = DeploymentStatus.RUNNING
        
        start_time = time.time()
        
        try:
            # Execute deployment based on type
            if deployment.deployment_type == DeploymentType.BLUE_GREEN:
                await self._execute_blue_green(execution, deployment, environment)
            elif deployment.deployment_type == DeploymentType.ROLLING:
                await self._execute_rolling(execution, deployment, environment)
            elif deployment.deployment_type == DeploymentType.CANARY:
                await self._execute_canary(execution, deployment, environment)
            else:
                await self._execute_recreate(execution, deployment, environment)
            
            # Complete successfully
            execution.status = DeploymentStatus.COMPLETED
            execution.completed_at = time.time()
            execution.total_duration = time.time() - start_time
            self.deployment_stats["successful_deployments"] += 1
            
            self.logger.info(f"Deployment execution {execution_id} completed successfully")
            
        except Exception as e:
            execution.status = DeploymentStatus.FAILED
            execution.completed_at = time.time()
            execution.total_duration = time.time() - start_time
            self.deployment_stats["failed_deployments"] += 1
            
            execution.logs.append({
                "timestamp": time.time(),
                "level": "ERROR",
                "message": f"Deployment execution failed: {str(e)}"
            })
            
            self.logger.error(f"Deployment execution {execution_id} failed: {e}")
        
        finally:
            self.active_deployments -= 1
            self._update_deployment_stats()
    
    async def _execute_blue_green(self, execution: DeploymentExecution, deployment: Deployment, environment: EnvironmentType):
        """Execute blue-green deployment"""
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": "Starting blue-green deployment"
        })
        
        # Deploy to green environment
        green_targets = [t for t in deployment.targets if "green" in self.deployment_targets[t].name.lower()]
        
        for target_id in green_targets:
            await self._deploy_to_target(execution, target_id, deployment)
            execution.targets_deployed += 1
        
        # Health check green environment
        if deployment.health_check_enabled:
            await self._health_check_targets(execution, green_targets)
        
        # Switch traffic to green
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": "Switching traffic to green environment"
        })
        
        # Cleanup blue environment
        blue_targets = [t for t in deployment.targets if "blue" in self.deployment_targets[t].name.lower()]
        for target_id in blue_targets:
            await self._cleanup_target(execution, target_id)
    
    async def _execute_rolling(self, execution: DeploymentExecution, deployment: Deployment, environment: EnvironmentType):
        """Execute rolling deployment"""
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": "Starting rolling deployment"
        })
        
        # Deploy to targets one by one
        for target_id in deployment.targets:
            await self._deploy_to_target(execution, target_id, deployment)
            execution.targets_deployed += 1
            
            # Health check
            if deployment.health_check_enabled:
                await self._health_check_targets(execution, [target_id])
            
            # Wait between deployments
            await asyncio.sleep(10)
    
    async def _execute_canary(self, execution: DeploymentExecution, deployment: Deployment, environment: EnvironmentType):
        """Execute canary deployment"""
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": "Starting canary deployment"
        })
        
        # Deploy to canary targets first
        canary_targets = deployment.targets[:2]  # Deploy to first 2 targets as canary
        
        for target_id in canary_targets:
            await self._deploy_to_target(execution, target_id, deployment)
            execution.targets_deployed += 1
        
        # Health check canary targets
        if deployment.health_check_enabled:
            await self._health_check_targets(execution, canary_targets)
        
        # Deploy to remaining targets
        remaining_targets = deployment.targets[2:]
        for target_id in remaining_targets:
            await self._deploy_to_target(execution, target_id, deployment)
            execution.targets_deployed += 1
    
    async def _execute_recreate(self, execution: DeploymentExecution, deployment: Deployment, environment: EnvironmentType):
        """Execute recreate deployment"""
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": "Starting recreate deployment"
        })
        
        # Stop current services
        for target_id in deployment.targets:
            await self._stop_service(execution, target_id)
        
        # Deploy to all targets
        for target_id in deployment.targets:
            await self._deploy_to_target(execution, target_id, deployment)
            execution.targets_deployed += 1
        
        # Start services
        for target_id in deployment.targets:
            await self._start_service(execution, target_id)
    
    async def _deploy_to_target(self, execution: DeploymentExecution, target_id: str, deployment: Deployment):
        """Deploy to a specific target"""
        target = self.deployment_targets[target_id]
        package = self.deployment_packages[deployment.package_id]
        
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": f"Deploying to target {target.name}"
        })
        
        try:
            # Deploy based on target type
            if target.target_type == "kubernetes":
                await self._deploy_kubernetes(execution, target, package)
            elif target.target_type == "docker":
                await self._deploy_docker(execution, target, package)
            elif target.target_type == "vm":
                await self._deploy_vm(execution, target, package)
            else:
                await self._deploy_generic(execution, target, package)
            
            execution.logs.append({
                "timestamp": time.time(),
                "level": "INFO",
                "message": f"Successfully deployed to target {target.name}"
            })
            
        except Exception as e:
            execution.targets_failed += 1
            execution.logs.append({
                "timestamp": time.time(),
                "level": "ERROR",
                "message": f"Failed to deploy to target {target.name}: {str(e)}"
            })
            raise
    
    async def _deploy_kubernetes(self, execution: DeploymentExecution, target: DeploymentTarget, package: DeploymentPackage):
        """Deploy to Kubernetes cluster"""
        # In a real implementation, this would use kubectl or Kubernetes API
        # For now, simulate deployment
        await asyncio.sleep(5)
        self.logger.info(f"Deployed {package.name} to Kubernetes cluster {target.name}")
    
    async def _deploy_docker(self, execution: DeploymentExecution, target: DeploymentTarget, package: DeploymentPackage):
        """Deploy using Docker"""
        # In a real implementation, this would use Docker API
        # For now, simulate deployment
        await asyncio.sleep(3)
        self.logger.info(f"Deployed {package.name} using Docker on {target.name}")
    
    async def _deploy_vm(self, execution: DeploymentExecution, target: DeploymentTarget, package: DeploymentPackage):
        """Deploy to VM"""
        # In a real implementation, this would use SSH or VM management API
        # For now, simulate deployment
        await asyncio.sleep(8)
        self.logger.info(f"Deployed {package.name} to VM {target.name}")
    
    async def _deploy_generic(self, execution: DeploymentExecution, target: DeploymentTarget, package: DeploymentPackage):
        """Generic deployment method"""
        # In a real implementation, this would use the appropriate deployment method
        # For now, simulate deployment
        await asyncio.sleep(4)
        self.logger.info(f"Deployed {package.name} to {target.name}")
    
    async def _health_check_targets(self, execution: DeploymentExecution, target_ids: List[str]):
        """Perform health checks on targets"""
        for target_id in target_ids:
            target = self.deployment_targets[target_id]
            
            if target.health_check_url:
                try:
                    response = requests.get(target.health_check_url, timeout=10)
                    status = "healthy" if response.status_code == 200 else "unhealthy"
                    response_time = response.elapsed.total_seconds()
                    
                    health_check = HealthCheck(
                        check_id=str(uuid.uuid4()),
                        target_id=target_id,
                        status=status,
                        response_time=response_time,
                        error_message=None,
                        checked_at=time.time()
                    )
                    
                    self.health_checks[health_check.check_id] = health_check
                    
                    execution.logs.append({
                        "timestamp": time.time(),
                        "level": "INFO",
                        "message": f"Health check for {target.name}: {status} ({response_time:.2f}s)"
                    })
                    
                    if status != "healthy":
                        raise Exception(f"Health check failed for {target.name}")
                
                except Exception as e:
                    execution.logs.append({
                        "timestamp": time.time(),
                        "level": "ERROR",
                        "message": f"Health check failed for {target.name}: {str(e)}"
                    })
                    raise
    
    async def _stop_service(self, execution: DeploymentExecution, target_id: str):
        """Stop service on target"""
        target = self.deployment_targets[target_id]
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": f"Stopping service on {target.name}"
        })
        await asyncio.sleep(2)
    
    async def _start_service(self, execution: DeploymentExecution, target_id: str):
        """Start service on target"""
        target = self.deployment_targets[target_id]
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": f"Starting service on {target.name}"
        })
        await asyncio.sleep(3)
    
    async def _cleanup_target(self, execution: DeploymentExecution, target_id: str):
        """Cleanup target after deployment"""
        target = self.deployment_targets[target_id]
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": f"Cleaning up {target.name}"
        })
        await asyncio.sleep(1)
    
    async def _rollback_blue_green(self, execution: DeploymentExecution, deployment: Deployment):
        """Rollback blue-green deployment"""
        # Switch traffic back to blue environment
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": "Rolling back blue-green deployment - switching traffic to blue"
        })
        await asyncio.sleep(2)
    
    async def _rollback_rolling(self, execution: DeploymentExecution, deployment: Deployment):
        """Rollback rolling deployment"""
        # Redeploy previous version to all targets
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": "Rolling back rolling deployment"
        })
        await asyncio.sleep(5)
    
    async def _rollback_canary(self, execution: DeploymentExecution, deployment: Deployment):
        """Rollback canary deployment"""
        # Stop deployment to remaining targets and rollback canary
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": "Rolling back canary deployment"
        })
        await asyncio.sleep(3)
    
    async def _rollback_recreate(self, execution: DeploymentExecution, deployment: Deployment):
        """Rollback recreate deployment"""
        # Redeploy previous version
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": "Rolling back recreate deployment"
        })
        await asyncio.sleep(4)
    
    async def _deployment_loop(self):
        """Background deployment monitoring loop"""
        while True:
            try:
                await self._monitor_deployments()
                await asyncio.sleep(30)
            except Exception as e:
                self.logger.error(f"Error in deployment loop: {e}")
                await asyncio.sleep(30)
    
    async def _monitor_deployments(self):
        """Monitor active deployments"""
        # Check for completed deployments and update stats
        for execution_id, execution in list(self.executions.items()):
            if execution.status in [DeploymentStatus.COMPLETED, DeploymentStatus.FAILED, DeploymentStatus.ROLLED_BACK]:
                if execution.completed_at and execution.started_at:
                    duration = execution.completed_at - execution.started_at
                    self.deployment_stats["average_deployment_time"] = duration
    
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
        """Perform health checks on all targets"""
        for target_id, target in self.deployment_targets.items():
            if target.health_check_url:
                try:
                    response = requests.get(target.health_check_url, timeout=10)
                    status = "healthy" if response.status_code == 200 else "unhealthy"
                    response_time = response.elapsed.total_seconds()
                    
                    health_check = HealthCheck(
                        check_id=str(uuid.uuid4()),
                        target_id=target_id,
                        status=status,
                        response_time=response_time,
                        error_message=None,
                        checked_at=time.time()
                    )
                    
                    self.health_checks[health_check.check_id] = health_check
                    
                except Exception as e:
                    health_check = HealthCheck(
                        check_id=str(uuid.uuid4()),
                        target_id=target_id,
                        status="unhealthy",
                        response_time=0.0,
                        error_message=str(e),
                        checked_at=time.time()
                    )
                    
                    self.health_checks[health_check.check_id] = health_check
    
    def _calculate_file_checksum(self, file_path: str) -> str:
        """Calculate SHA256 checksum of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def _save_deployment_config(self, deployment: Deployment):
        """Save deployment configuration to file"""
        filename = f"{deployment.name.replace(' ', '_').lower()}.yaml"
        filepath = os.path.join(self.deployments_path, filename)
        
        deployment_data = {
            "deployment_id": deployment.deployment_id,
            "name": deployment.name,
            "description": deployment.description,
            "deployment_type": deployment.deployment_type.value,
            "strategy": deployment.strategy.value,
            "targets": deployment.targets,
            "package_id": deployment.package_id,
            "rollback_enabled": deployment.rollback_enabled,
            "health_check_enabled": deployment.health_check_enabled,
            "created_at": deployment.created_at,
            "last_modified": deployment.last_modified
        }
        
        with open(filepath, 'w') as f:
            yaml.dump(deployment_data, f, default_flow_style=False)
    
    def _update_deployment_stats(self):
        """Update deployment statistics"""
        successful_executions = [e for e in self.executions.values() if e.status == DeploymentStatus.COMPLETED]
        
        if successful_executions:
            total_time = sum(e.total_duration for e in successful_executions)
            self.deployment_stats["average_deployment_time"] = total_time / len(successful_executions)
            
            success_count = len(successful_executions)
            total_count = len(self.executions)
            self.deployment_stats["success_rate"] = success_count / total_count if total_count > 0 else 0.0

# Global deployment automation instance
_deployment_automation = DeploymentAutomation({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "create_target", "create_package", "create_deployment", 
                     "execute_deployment", "rollback_deployment", "get_status", "get_stats"
            - target_data: Target configuration
            - package_data: Package information
            - deployment_data: Deployment configuration
            - execution_data: Execution parameters
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "create_target":
            target_data = payload.get("target_data", {})
            
            target_id = _deployment_automation.create_deployment_target(
                name=target_data.get("name", "Deployment Target"),
                environment=EnvironmentType(target_data.get("environment", "development")),
                target_type=target_data.get("target_type", "kubernetes"),
                connection_config=target_data.get("connection_config", {}),
                health_check_url=target_data.get("health_check_url")
            )
            
            return {
                "result": {
                    "target_id": target_id,
                    "message": f"Created deployment target: {target_id}"
                },
                "metadata": {
                    "action": "create_target",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_package":
            package_data = payload.get("package_data", {})
            
            package_id = _deployment_automation.create_deployment_package(
                name=package_data.get("name", "Deployment Package"),
                version=package_data.get("version", "1.0.0"),
                package_type=package_data.get("package_type", "docker"),
                artifact_path=package_data.get("artifact_path", ""),
                dependencies=package_data.get("dependencies", [])
            )
            
            return {
                "result": {
                    "package_id": package_id,
                    "message": f"Created deployment package: {package_id}"
                },
                "metadata": {
                    "action": "create_package",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_deployment":
            deployment_data = payload.get("deployment_data", {})
            
            deployment_id = _deployment_automation.create_deployment(
                name=deployment_data.get("name", "Deployment"),
                description=deployment_data.get("description", ""),
                deployment_type=DeploymentType(deployment_data.get("deployment_type", "rolling")),
                strategy=DeploymentStrategy(deployment_data.get("strategy", "container")),
                targets=deployment_data.get("targets", []),
                package_id=deployment_data.get("package_id", ""),
                rollback_enabled=deployment_data.get("rollback_enabled", True),
                health_check_enabled=deployment_data.get("health_check_enabled", True)
            )
            
            return {
                "result": {
                    "deployment_id": deployment_id,
                    "message": f"Created deployment: {deployment_id}"
                },
                "metadata": {
                    "action": "create_deployment",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "execute_deployment":
            execution_data = payload.get("execution_data", {})
            
            execution_id = await _deployment_automation.execute_deployment(
                deployment_id=execution_data.get("deployment_id", ""),
                environment=EnvironmentType(execution_data.get("environment", "development")),
                package_version=execution_data.get("package_version")
            )
            
            return {
                "result": {
                    "execution_id": execution_id,
                    "message": f"Started deployment execution: {execution_id}"
                },
                "metadata": {
                    "action": "execute_deployment",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "rollback_deployment":
            execution_id = payload.get("execution_id", "")
            success = await _deployment_automation.rollback_deployment(execution_id)
            
            return {
                "result": {
                    "success": success,
                    "message": f"Deployment rollback: {'successful' if success else 'failed'}"
                },
                "metadata": {
                    "action": "rollback_deployment",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_status":
            execution_id = payload.get("execution_id", "")
            status = _deployment_automation.get_deployment_status(execution_id)
            
            return {
                "result": status,
                "metadata": {
                    "action": "get_status",
                    "timestamp": datetime.now().isoformat(),
                    "execution_id": execution_id
                }
            }
        
        elif action == "get_stats":
            stats = _deployment_automation.get_deployment_stats()
            
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
        logger.error(f"Error in deployment_automation: {e}")
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
    """Example of how to use the deployment automation skill"""
    
    # Create deployment targets
    staging_target = await invoke({
        "action": "create_target",
        "target_data": {
            "name": "Staging Cluster",
            "environment": "staging",
            "target_type": "kubernetes",
            "connection_config": {
                "kubeconfig": "~/.kube/config",
                "context": "staging"
            },
            "health_check_url": "http://staging.example.com/health"
        }
    })
    
    prod_target = await invoke({
        "action": "create_target",
        "target_data": {
            "name": "Production Cluster",
            "environment": "production",
            "target_type": "kubernetes",
            "connection_config": {
                "kubeconfig": "~/.kube/config",
                "context": "production"
            },
            "health_check_url": "http://prod.example.com/health"
        }
    })
    
    print(f"Created targets: {staging_target['result']['target_id']}, {prod_target['result']['target_id']}")
    
    # Create deployment package
    package_id = await invoke({
        "action": "create_package",
        "package_data": {
            "name": "Web Application",
            "version": "1.2.0",
            "package_type": "docker",
            "artifact_path": "./app.tar.gz",
            "dependencies": ["nginx", "nodejs"]
        }
    })
    
    print(f"Created package: {package_id['result']['package_id']}")
    
    # Create deployment
    deployment_id = await invoke({
        "action": "create_deployment",
        "deployment_data": {
            "name": "Web App Deployment",
            "description": "Deploy web application to staging and production",
            "deployment_type": "blue_green",
            "strategy": "container",
            "targets": [staging_target['result']['target_id'], prod_target['result']['target_id']],
            "package_id": package_id['result']['package_id'],
            "rollback_enabled": True,
            "health_check_enabled": True
        }
    })
    
    print(f"Created deployment: {deployment_id['result']['deployment_id']}")
    
    # Execute deployment
    execution_id = await invoke({
        "action": "execute_deployment",
        "execution_data": {
            "deployment_id": deployment_id['result']['deployment_id'],
            "environment": "staging",
            "package_version": "1.2.0"
        }
    })
    
    print(f"Started execution: {execution_id['result']['execution_id']}")
    
    # Get deployment status
    status = await invoke({
        "action": "get_status",
        "execution_id": execution_id['result']['execution_id']
    })
    
    print(f"Deployment status: {status['result']}")
    
    # Get deployment statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Deployment stats: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
