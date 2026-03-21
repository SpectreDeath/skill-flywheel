#!/usr/bin/env python3
"""
Skill: ci-cd-pipeline-manager
Domain: devops
Description: CI/CD pipeline management and automation system
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
from typing import Any, Dict, List

import yaml

logger = logging.getLogger(__name__)

class PipelineStatus(Enum):
    """Pipeline execution statuses"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class StageStatus(Enum):
    """Stage execution statuses"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class JobStatus(Enum):
    """Job execution statuses"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    QUEUED = "queued"

class BuildType(Enum):
    """Types of builds"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    RELEASE = "release"

@dataclass
class PipelineStage:
    """Represents a pipeline stage"""
    stage_id: str
    name: str
    description: str
    jobs: List[str]
    dependencies: List[str]
    parallel: bool
    timeout: int  # seconds
    created_at: float

@dataclass
class PipelineJob:
    """Represents a pipeline job"""
    job_id: str
    name: str
    stage: str
    script: List[str]
    environment: Dict[str, str]
    artifacts: List[str]
    dependencies: List[str]
    retry_count: int
    max_retries: int
    timeout: int  # seconds
    created_at: float

@dataclass
class Pipeline:
    """Represents a CI/CD pipeline"""
    pipeline_id: str
    name: str
    description: str
    stages: List[PipelineStage]
    jobs: List[PipelineJob]
    triggers: List[Dict[str, Any]]
    variables: Dict[str, str]
    created_at: float
    last_modified: float

@dataclass
class PipelineExecution:
    """Represents a pipeline execution"""
    execution_id: str
    pipeline_id: str
    status: PipelineStatus
    build_type: BuildType
    triggered_by: str
    started_at: float
    completed_at: float | None
    stages_executed: int
    stages_completed: int
    stages_failed: int
    total_duration: float
    artifacts_path: str | None
    logs: List[Dict[str, Any]]

@dataclass
class BuildArtifact:
    """Represents a build artifact"""
    artifact_id: str
    name: str
    path: str
    size: int
    checksum: str
    created_at: float

class CICDPipelineManager:
    """CI/CD pipeline management and automation system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the CI/CD pipeline manager
        
        Args:
            config: Configuration dictionary with:
                - pipelines_path: Path to pipeline definitions
                - artifacts_path: Path to store build artifacts
                - max_concurrent_builds: Maximum concurrent builds
                - default_timeout: Default job timeout in seconds
        """
        self.pipelines_path = config.get("pipelines_path", "./pipelines")
        self.artifacts_path = config.get("artifacts_path", "./artifacts")
        self.max_concurrent_builds = config.get("max_concurrent_builds", 5)
        self.default_timeout = config.get("default_timeout", 3600)
        
        self.pipelines: Dict[str, Pipeline] = {}
        self.executions: Dict[str, PipelineExecution] = {}
        self.build_artifacts: Dict[str, BuildArtifact] = {}
        
        self.active_executions = 0
        self.total_executions = 0
        self.execution_stats = {
            "total_pipelines": 0,
            "active_executions": 0,
            "completed_executions": 0,
            "failed_executions": 0,
            "average_build_time": 0.0,
            "success_rate": 0.0
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Ensure directories exist
        os.makedirs(self.pipelines_path, exist_ok=True)
        os.makedirs(self.artifacts_path, exist_ok=True)
        
        # Start background executor
        self._executor_task = asyncio.create_task(self._executor_loop())
    
    def create_pipeline(self,
                       name: str,
                       description: str,
                       stages: List[Dict[str, Any]],
                       jobs: List[Dict[str, Any]],
                       triggers: List[Dict[str, Any]] | None = None,
                       variables: Dict[str, str] | None = None) -> str:
        """
        Create a new CI/CD pipeline
        
        Args:
            name: Pipeline name
            description: Pipeline description
            stages: List of stage configurations
            jobs: List of job configurations
            triggers: Pipeline triggers (optional)
            variables: Pipeline variables (optional)
            
        Returns:
            Pipeline ID
        """
        pipeline_id = str(uuid.uuid4())
        
        # Create stages
        pipeline_stages = []
        for stage_config in stages:
            stage_id = str(uuid.uuid4())
            
            stage = PipelineStage(
                stage_id=stage_id,
                name=stage_config.get("name", f"Stage-{stage_id[:8]}"),
                description=stage_config.get("description", ""),
                jobs=stage_config.get("jobs", []),
                dependencies=stage_config.get("dependencies", []),
                parallel=stage_config.get("parallel", False),
                timeout=stage_config.get("timeout", self.default_timeout),
                created_at=time.time()
            )
            
            pipeline_stages.append(stage)
        
        # Create jobs
        pipeline_jobs = []
        for job_config in jobs:
            job_id = str(uuid.uuid4())
            
            job = PipelineJob(
                job_id=job_id,
                name=job_config.get("name", f"Job-{job_id[:8]}"),
                stage=job_config.get("stage", ""),
                script=job_config.get("script", []),
                environment=job_config.get("environment", {}),
                artifacts=job_config.get("artifacts", []),
                dependencies=job_config.get("dependencies", []),
                retry_count=0,
                max_retries=job_config.get("max_retries", 3),
                timeout=job_config.get("timeout", self.default_timeout),
                created_at=time.time()
            )
            
            pipeline_jobs.append(job)
        
        pipeline = Pipeline(
            pipeline_id=pipeline_id,
            name=name,
            description=description,
            stages=pipeline_stages,
            jobs=pipeline_jobs,
            triggers=triggers or [],
            variables=variables or {},
            created_at=time.time(),
            last_modified=time.time()
        )
        
        self.pipelines[pipeline_id] = pipeline
        self.execution_stats["total_pipelines"] += 1
        
        # Save pipeline definition
        self._save_pipeline_definition(pipeline)
        
        self.logger.info(f"Created pipeline: {pipeline_id}")
        return pipeline_id
    
    async def trigger_pipeline(self,
                              pipeline_id: str,
                              build_type: BuildType,
                              triggered_by: str = "manual") -> str:
        """
        Trigger a pipeline execution
        
        Args:
            pipeline_id: Pipeline ID
            build_type: Type of build
            triggered_by: Who/what triggered the build
            
        Returns:
            Execution ID
        """
        if pipeline_id not in self.pipelines:
            raise ValueError(f"Pipeline {pipeline_id} not found")
        
        if self.active_executions >= self.max_concurrent_builds:
            raise ValueError("Maximum concurrent builds reached")
        
        pipeline = self.pipelines[pipeline_id]
        
        execution_id = str(uuid.uuid4())
        
        execution = PipelineExecution(
            execution_id=execution_id,
            pipeline_id=pipeline_id,
            status=PipelineStatus.PENDING,
            build_type=build_type,
            triggered_by=triggered_by,
            started_at=time.time(),
            completed_at=None,
            stages_executed=0,
            stages_completed=0,
            stages_failed=0,
            total_duration=0.0,
            artifacts_path=None,
            logs=[]
        )
        
        self.executions[execution_id] = execution
        self.active_executions += 1
        self.total_executions += 1
        
        # Execute pipeline asynchronously
        asyncio.create_task(self._execute_pipeline_async(execution_id, pipeline))
        
        self.logger.info(f"Triggered pipeline execution: {execution_id}")
        return execution_id
    
    async def cancel_execution(self, execution_id: str):
        """Cancel a running pipeline execution"""
        if execution_id in self.executions:
            execution = self.executions[execution_id]
            if execution.status == PipelineStatus.RUNNING:
                execution.status = PipelineStatus.CANCELLED
                execution.completed_at = time.time()
                self.active_executions -= 1
                self.logger.info(f"Cancelled pipeline execution: {execution_id}")
    
    def get_pipeline_status(self, execution_id: str) -> Dict[str, Any] | None:
        """Get pipeline execution status"""
        if execution_id not in self.executions:
            return None
        
        execution = self.executions[execution_id]
        
        return {
            "execution_id": execution.execution_id,
            "pipeline_id": execution.pipeline_id,
            "status": execution.status.value,
            "build_type": execution.build_type.value,
            "triggered_by": execution.triggered_by,
            "started_at": datetime.fromtimestamp(execution.started_at).isoformat(),
            "completed_at": datetime.fromtimestamp(execution.completed_at).isoformat() if execution.completed_at else None,
            "stages_executed": execution.stages_executed,
            "stages_completed": execution.stages_completed,
            "stages_failed": execution.stages_failed,
            "total_duration": execution.total_duration,
            "progress": execution.stages_completed / len(self.pipelines[execution.pipeline_id].stages) if execution.pipeline_id in self.pipelines else 0
        }
    
    def get_pipeline_logs(self, execution_id: str) -> List[Dict[str, Any]]:
        """Get pipeline execution logs"""
        if execution_id not in self.executions:
            return []
        
        return self.executions[execution_id].logs
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get pipeline execution statistics"""
        total_executions = len(self.executions)
        completed_executions = len([e for e in self.executions.values() if e.status == PipelineStatus.COMPLETED])
        failed_executions = len([e for e in self.executions.values() if e.status == PipelineStatus.FAILED])
        
        return {
            "total_pipelines": self.execution_stats["total_pipelines"],
            "active_executions": self.active_executions,
            "total_executions": total_executions,
            "completed_executions": completed_executions,
            "failed_executions": failed_executions,
            "success_rate": completed_executions / total_executions if total_executions > 0 else 0.0,
            "average_build_time": self.execution_stats["average_build_time"],
            "max_concurrent_builds": self.max_concurrent_builds,
            "total_artifacts": len(self.build_artifacts)
        }
    
    def create_build_artifact(self,
                            name: str,
                            path: str,
                            execution_id: str) -> str:
        """
        Create a build artifact
        
        Args:
            name: Artifact name
            path: Path to artifact file
            execution_id: Execution ID
            
        Returns:
            Artifact ID
        """
        if not os.path.exists(path):
            raise ValueError(f"Artifact file {path} does not exist")
        
        artifact_id = str(uuid.uuid4())
        file_size = os.path.getsize(path)
        checksum = self._calculate_file_checksum(path)
        
        # Move artifact to artifacts directory
        artifact_path = os.path.join(self.artifacts_path, f"{artifact_id}_{name}")
        shutil.copy2(path, artifact_path)
        
        artifact = BuildArtifact(
            artifact_id=artifact_id,
            name=name,
            path=artifact_path,
            size=file_size,
            checksum=checksum,
            created_at=time.time()
        )
        
        self.build_artifacts[artifact_id] = artifact
        
        # Update execution with artifact path
        if execution_id in self.executions:
            self.executions[execution_id].artifacts_path = artifact_path
        
        self.logger.info(f"Created build artifact: {artifact_id}")
        return artifact_id
    
    def get_artifact(self, artifact_id: str) -> Dict[str, Any] | None:
        """Get artifact information"""
        if artifact_id not in self.build_artifacts:
            return None
        
        artifact = self.build_artifacts[artifact_id]
        
        return {
            "artifact_id": artifact.artifact_id,
            "name": artifact.name,
            "path": artifact.path,
            "size": artifact.size,
            "checksum": artifact.checksum,
            "created_at": datetime.fromtimestamp(artifact.created_at).isoformat()
        }
    
    async def _execute_pipeline_async(self, execution_id: str, pipeline: Pipeline):
        """Execute pipeline asynchronously"""
        execution = self.executions[execution_id]
        execution.status = PipelineStatus.RUNNING
        
        start_time = time.time()
        
        try:
            # Sort stages by dependencies
            sorted_stages = self._topological_sort_stages(pipeline.stages)
            
            # Execute stages
            for stage in sorted_stages:
                await self._execute_stage(execution, stage, pipeline)
                
                if execution.status == PipelineStatus.FAILED:
                    break
            
            # Complete successfully
            if execution.status != PipelineStatus.FAILED:
                execution.status = PipelineStatus.COMPLETED
                execution.completed_at = time.time()
                execution.total_duration = time.time() - start_time
                self.execution_stats["completed_executions"] += 1
                
                self.logger.info(f"Pipeline execution {execution_id} completed successfully")
            
        except Exception as e:
            execution.status = PipelineStatus.FAILED
            execution.completed_at = time.time()
            execution.total_duration = time.time() - start_time
            self.execution_stats["failed_executions"] += 1
            
            execution.logs.append({
                "timestamp": time.time(),
                "level": "ERROR",
                "message": f"Pipeline execution failed: {str(e)}"
            })
            
            self.logger.error(f"Pipeline execution {execution_id} failed: {e}")
        
        finally:
            self.active_executions -= 1
            self._update_execution_stats()
    
    async def _execute_stage(self, execution: PipelineExecution, stage: PipelineStage, pipeline: Pipeline):
        """Execute a pipeline stage"""
        execution.stages_executed += 1
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": f"Starting stage: {stage.name}"
        })
        
        stage_jobs = [job for job in pipeline.jobs if job.stage == stage.name]
        
        if stage.parallel:
            # Execute jobs in parallel
            job_coroutines = [self._execute_job(execution, job) for job in stage_jobs]
            results = await asyncio.gather(*job_coroutines, return_exceptions=True)
            
            failed_jobs = [r for r in results if isinstance(r, Exception)]
            if failed_jobs:
                execution.status = PipelineStatus.FAILED
                execution.stages_failed += 1
                execution.logs.append({
                    "timestamp": time.time(),
                    "level": "ERROR",
                    "message": f"Stage {stage.name} failed: {len(failed_jobs)} jobs failed"
                })
            else:
                execution.stages_completed += 1
                execution.logs.append({
                    "timestamp": time.time(),
                    "level": "INFO",
                    "message": f"Stage {stage.name} completed successfully"
                })
        else:
            # Execute jobs sequentially
            for job in stage_jobs:
                await self._execute_job(execution, job)
                
                if execution.status == PipelineStatus.FAILED:
                    execution.stages_failed += 1
                    break
            
            if execution.status != PipelineStatus.FAILED:
                execution.stages_completed += 1
                execution.logs.append({
                    "timestamp": time.time(),
                    "level": "INFO",
                    "message": f"Stage {stage.name} completed successfully"
                })
    
    async def _execute_job(self, execution: PipelineExecution, job: PipelineJob):
        """Execute a pipeline job"""
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": f"Starting job: {job.name}"
        })
        
        start_time = time.time()
        
        try:
            # Set up job environment
            job_env = os.environ.copy()
            job_env.update(execution.pipeline_id in self.pipelines and self.pipelines[execution.pipeline_id].variables or {})
            job_env.update(job.environment)
            
            # Execute job script
            for script_line in job.script:
                if execution.status == PipelineStatus.CANCELLED:
                    raise Exception("Job cancelled")
                
                # Execute script line
                process = await asyncio.create_subprocess_shell(
                    script_line,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env=job_env
                )
                
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=job.timeout
                )
                
                if process.returncode != 0:
                    raise Exception(f"Script failed: {stderr.decode()}")
                
                execution.logs.append({
                    "timestamp": time.time(),
                    "level": "INFO",
                    "message": f"Job {job.name}: {stdout.decode().strip()}"
                })
            
            # Handle artifacts
            for artifact_pattern in job.artifacts:
                self._collect_artifacts(execution.execution_id, artifact_pattern)
            
            execution.logs.append({
                "timestamp": time.time(),
                "level": "INFO",
                "message": f"Job {job.name} completed successfully ({time.time() - start_time:.2f}s)"
            })
            
        except Exception as e:
            job.retry_count += 1
            
            if job.retry_count <= job.max_retries:
                execution.logs.append({
                    "timestamp": time.time(),
                    "level": "WARNING",
                    "message": f"Job {job.name} failed, retrying ({job.retry_count}/{job.max_retries}): {str(e)}"
                })
                await asyncio.sleep(2 ** job.retry_count)  # Exponential backoff
                await self._execute_job(execution, job)
            else:
                execution.status = PipelineStatus.FAILED
                execution.logs.append({
                    "timestamp": time.time(),
                    "level": "ERROR",
                    "message": f"Job {job.name} failed after {job.max_retries} retries: {str(e)}"
                })
    
    def _collect_artifacts(self, execution_id: str, pattern: str):
        """Collect build artifacts"""
        # In a real implementation, this would use glob patterns
        # For now, just log the artifact collection
        self.logger.info(f"Collecting artifacts for execution {execution_id}: {pattern}")
    
    def _topological_sort_stages(self, stages: List[PipelineStage]) -> List[PipelineStage]:
        """Sort stages topologically based on dependencies"""
        # Create stage lookup
        stage_lookup = {s.stage_id: s for s in stages}
        
        # Calculate in-degrees
        in_degree = {s.stage_id: 0 for s in stages}
        for stage in stages:
            for dep in stage.dependencies:
                in_degree[dep] += 1
        
        # Kahn's algorithm for topological sorting
        queue = [s_id for s_id, degree in in_degree.items() if degree == 0]
        sorted_stages = []
        
        while queue:
            current = queue.pop(0)
            sorted_stages.append(stage_lookup[current])
            
            # Remove current from dependencies
            for stage in stages:
                if current in stage.dependencies:
                    stage.dependencies.remove(current)
                    in_degree[stage.stage_id] -= 1
                    
                    if in_degree[stage.stage_id] == 0:
                        queue.append(stage.stage_id)
        
        return sorted_stages
    
    def _calculate_file_checksum(self, file_path: str) -> str:
        """Calculate SHA256 checksum of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def _save_pipeline_definition(self, pipeline: Pipeline):
        """Save pipeline definition to file"""
        filename = f"{pipeline.name.replace(' ', '_').lower()}.yaml"
        filepath = os.path.join(self.pipelines_path, filename)
        
        pipeline_data = {
            "pipeline_id": pipeline.pipeline_id,
            "name": pipeline.name,
            "description": pipeline.description,
            "stages": [
                {
                    "stage_id": s.stage_id,
                    "name": s.name,
                    "description": s.description,
                    "jobs": s.jobs,
                    "dependencies": s.dependencies,
                    "parallel": s.parallel,
                    "timeout": s.timeout
                }
                for s in pipeline.stages
            ],
            "jobs": [
                {
                    "job_id": j.job_id,
                    "name": j.name,
                    "stage": j.stage,
                    "script": j.script,
                    "environment": j.environment,
                    "artifacts": j.artifacts,
                    "dependencies": j.dependencies,
                    "max_retries": j.max_retries,
                    "timeout": j.timeout
                }
                for j in pipeline.jobs
            ],
            "triggers": pipeline.triggers,
            "variables": pipeline.variables,
            "created_at": pipeline.created_at,
            "last_modified": pipeline.last_modified
        }
        
        with open(filepath, 'w') as f:
            yaml.dump(pipeline_data, f, default_flow_style=False)
    
    def _update_execution_stats(self):
        """Update execution statistics"""
        completed_executions = [e for e in self.executions.values() if e.status == PipelineStatus.COMPLETED]
        
        if completed_executions:
            total_time = sum(e.total_duration for e in completed_executions)
            self.execution_stats["average_build_time"] = total_time / len(completed_executions)
            
            success_count = len(completed_executions)
            total_count = len(self.executions)
            self.execution_stats["success_rate"] = success_count / total_count if total_count > 0 else 0.0

# Global CI/CD pipeline manager instance
_pipeline_manager = CICDPipelineManager({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "create_pipeline", "trigger_pipeline", "cancel_execution", 
                     "get_status", "get_logs", "get_stats", "create_artifact"
            - pipeline_data: Pipeline configuration
            - execution_data: Execution parameters
            - artifact_data: Artifact information
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "create_pipeline":
            pipeline_data = payload.get("pipeline_data", {})
            
            pipeline_id = _pipeline_manager.create_pipeline(
                name=pipeline_data.get("name", "CI/CD Pipeline"),
                description=pipeline_data.get("description", ""),
                stages=pipeline_data.get("stages", []),
                jobs=pipeline_data.get("jobs", []),
                triggers=pipeline_data.get("triggers"),
                variables=pipeline_data.get("variables")
            )
            
            return {
                "result": {
                    "pipeline_id": pipeline_id,
                    "message": f"Created pipeline: {pipeline_id}"
                },
                "metadata": {
                    "action": "create_pipeline",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "trigger_pipeline":
            execution_data = payload.get("execution_data", {})
            
            execution_id = await _pipeline_manager.trigger_pipeline(
                pipeline_id=execution_data.get("pipeline_id", ""),
                build_type=BuildType(execution_data.get("build_type", "development")),
                triggered_by=execution_data.get("triggered_by", "manual")
            )
            
            return {
                "result": {
                    "execution_id": execution_id,
                    "message": f"Triggered pipeline execution: {execution_id}"
                },
                "metadata": {
                    "action": "trigger_pipeline",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "cancel_execution":
            execution_id = payload.get("execution_id", "")
            await _pipeline_manager.cancel_execution(execution_id)
            
            return {
                "result": {
                    "execution_id": execution_id,
                    "message": f"Cancelled pipeline execution: {execution_id}"
                },
                "metadata": {
                    "action": "cancel_execution",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_status":
            execution_id = payload.get("execution_id", "")
            status = _pipeline_manager.get_pipeline_status(execution_id)
            
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
            logs = _pipeline_manager.get_pipeline_logs(execution_id)
            
            return {
                "result": logs,
                "metadata": {
                    "action": "get_logs",
                    "timestamp": datetime.now().isoformat(),
                    "execution_id": execution_id
                }
            }
        
        elif action == "get_stats":
            stats = _pipeline_manager.get_pipeline_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_artifact":
            artifact_data = payload.get("artifact_data", {})
            
            artifact_id = _pipeline_manager.create_build_artifact(
                name=artifact_data.get("name", "artifact"),
                path=artifact_data.get("path", ""),
                execution_id=artifact_data.get("execution_id", "")
            )
            
            return {
                "result": {
                    "artifact_id": artifact_id,
                    "message": f"Created build artifact: {artifact_id}"
                },
                "metadata": {
                    "action": "create_artifact",
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
        logger.error(f"Error in ci_cd_pipeline_manager: {e}")
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
    """Example of how to use the CI/CD pipeline manager skill"""
    
    # Create a pipeline
    pipeline_id = await invoke({
        "action": "create_pipeline",
        "pipeline_data": {
            "name": "Web Application Pipeline",
            "description": "CI/CD pipeline for web application",
            "stages": [
                {
                    "name": "build",
                    "description": "Build application",
                    "jobs": ["build_app"],
                    "dependencies": [],
                    "parallel": False,
                    "timeout": 600
                },
                {
                    "name": "test",
                    "description": "Run tests",
                    "jobs": ["test_app"],
                    "dependencies": ["build"],
                    "parallel": False,
                    "timeout": 300
                },
                {
                    "name": "deploy",
                    "description": "Deploy to staging",
                    "jobs": ["deploy_staging"],
                    "dependencies": ["test"],
                    "parallel": False,
                    "timeout": 600
                }
            ],
            "jobs": [
                {
                    "name": "build_app",
                    "stage": "build",
                    "script": [
                        "npm install",
                        "npm run build"
                    ],
                    "environment": {
                        "NODE_ENV": "production"
                    },
                    "artifacts": ["dist/"],
                    "dependencies": [],
                    "max_retries": 2,
                    "timeout": 600
                },
                {
                    "name": "test_app",
                    "stage": "test",
                    "script": [
                        "npm test",
                        "npm run lint"
                    ],
                    "environment": {},
                    "artifacts": [],
                    "dependencies": ["build_app"],
                    "max_retries": 1,
                    "timeout": 300
                },
                {
                    "name": "deploy_staging",
                    "stage": "deploy",
                    "script": [
                        "echo 'Deploying to staging...'",
                        "rsync -av dist/ staging-server:/var/www/app/"
                    ],
                    "environment": {
                        "DEPLOY_ENV": "staging"
                    },
                    "artifacts": [],
                    "dependencies": ["test_app"],
                    "max_retries": 3,
                    "timeout": 600
                }
            ],
            "triggers": [
                {
                    "type": "push",
                    "branches": ["main", "develop"]
                },
                {
                    "type": "schedule",
                    "cron": "0 2 * * *"
                }
            ],
            "variables": {
                "BUILD_VERSION": "1.0.0",
                "NODE_VERSION": "18"
            }
        }
    })
    
    print(f"Created pipeline: {pipeline_id['result']['pipeline_id']}")
    
    # Trigger pipeline
    execution_id = await invoke({
        "action": "trigger_pipeline",
        "execution_data": {
            "pipeline_id": pipeline_id['result']['pipeline_id'],
            "build_type": "development",
            "triggered_by": "manual"
        }
    })
    
    print(f"Triggered execution: {execution_id['result']['execution_id']}")
    
    # Get pipeline status
    status = await invoke({
        "action": "get_status",
        "execution_id": execution_id['result']['execution_id']
    })
    
    print(f"Pipeline status: {status['result']}")
    
    # Get pipeline statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Pipeline stats: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
