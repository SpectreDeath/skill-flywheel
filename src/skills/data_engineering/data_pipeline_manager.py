#!/usr/bin/env python3
"""
Skill: data-pipeline-manager
Domain: data_engineering
Description: Data pipeline management system for ETL/ELT processes and data workflows
"""

import asyncio
import logging
import time
import uuid
import json
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import hashlib

logger = logging.getLogger(__name__)

class PipelineStatus(Enum):
    """Pipeline execution statuses"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskStatus(Enum):
    """Task execution statuses"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class DataSourceType(Enum):
    """Types of data sources"""
    DATABASE = "database"
    FILE = "file"
    API = "api"
    STREAM = "stream"
    MESSAGE_QUEUE = "message_queue"

@dataclass
class DataSource:
    """Represents a data source"""
    source_id: str
    name: str
    source_type: DataSourceType
    connection_config: Dict[str, Any]
    query: Optional[str]
    file_path: Optional[str]
    api_endpoint: Optional[str]
    created_at: float
    last_accessed: float

@dataclass
class DataTransformation:
    """Represents a data transformation"""
    transform_id: str
    name: str
    transform_type: str  # sql, python, pandas, spark
    code: str
    dependencies: List[str]
    created_at: float

@dataclass
class DataSink:
    """Represents a data sink"""
    sink_id: str
    name: str
    sink_type: str  # database, file, api
    connection_config: Dict[str, Any]
    table_name: Optional[str]
    file_path: Optional[str]
    api_endpoint: Optional[str]
    created_at: float

@dataclass
class PipelineTask:
    """Represents a task in a pipeline"""
    task_id: str
    name: str
    task_type: str  # extract, transform, load
    source_id: Optional[str]
    transform_id: Optional[str]
    sink_id: Optional[str]
    dependencies: List[str]
    retry_count: int
    max_retries: int
    timeout: int  # seconds
    created_at: float

@dataclass
class DataPipeline:
    """Represents a data pipeline"""
    pipeline_id: str
    name: str
    description: str
    tasks: List[PipelineTask]
    schedule: Optional[str]  # cron expression
    parallel_execution: bool
    created_at: float
    last_modified: float

@dataclass
class PipelineExecution:
    """Represents a pipeline execution"""
    execution_id: str
    pipeline_id: str
    status: PipelineStatus
    started_at: float
    completed_at: Optional[float]
    tasks_executed: int
    tasks_completed: int
    tasks_failed: int
    total_duration: float
    logs: List[Dict[str, Any]]

class DataPipelineManager:
    """Data pipeline management system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the data pipeline manager
        
        Args:
            config: Configuration dictionary with:
                - max_parallel_tasks: Maximum parallel task execution
                - default_timeout: Default task timeout
                - retry_attempts: Default retry attempts
        """
        self.max_parallel_tasks = config.get("max_parallel_tasks", 5)
        self.default_timeout = config.get("default_timeout", 3600)
        self.retry_attempts = config.get("retry_attempts", 3)
        
        self.data_sources: Dict[str, DataSource] = {}
        self.transformations: Dict[str, DataTransformation] = {}
        self.data_sinks: Dict[str, DataSink] = {}
        self.pipelines: Dict[str, DataPipeline] = {}
        self.executions: Dict[str, PipelineExecution] = {}
        
        self.active_executions = 0
        self.total_executions = 0
        self.execution_stats = {
            "total_pipelines": 0,
            "active_executions": 0,
            "completed_executions": 0,
            "failed_executions": 0,
            "average_execution_time": 0.0
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Start background scheduler
        self._scheduler_task = asyncio.create_task(self._scheduler_loop())
    
    def create_data_source(self,
                          name: str,
                          source_type: DataSourceType,
                          connection_config: Dict[str, Any],
                          query: Optional[str] = None,
                          file_path: Optional[str] = None,
                          api_endpoint: Optional[str] = None) -> str:
        """
        Create a data source
        
        Args:
            name: Source name
            source_type: Type of data source
            connection_config: Connection configuration
            query: SQL query (for database sources)
            file_path: File path (for file sources)
            api_endpoint: API endpoint (for API sources)
            
        Returns:
            Source ID
        """
        source_id = str(uuid.uuid4())
        
        source = DataSource(
            source_id=source_id,
            name=name,
            source_type=source_type,
            connection_config=connection_config,
            query=query,
            file_path=file_path,
            api_endpoint=api_endpoint,
            created_at=time.time(),
            last_accessed=0.0
        )
        
        self.data_sources[source_id] = source
        self.logger.info(f"Created data source: {source_id}")
        
        return source_id
    
    def create_transformation(self,
                             name: str,
                             transform_type: str,
                             code: str,
                             dependencies: Optional[List[str]] = None) -> str:
        """
        Create a data transformation
        
        Args:
            name: Transformation name
            transform_type: Type of transformation
            code: Transformation code
            dependencies: List of dependency transformation IDs
            
        Returns:
            Transformation ID
        """
        transform_id = str(uuid.uuid4())
        
        transformation = DataTransformation(
            transform_id=transform_id,
            name=name,
            transform_type=transform_type,
            code=code,
            dependencies=dependencies or [],
            created_at=time.time()
        )
        
        self.transformations[transform_id] = transformation
        self.logger.info(f"Created transformation: {transform_id}")
        
        return transform_id
    
    def create_data_sink(self,
                        name: str,
                        sink_type: str,
                        connection_config: Dict[str, Any],
                        table_name: Optional[str] = None,
                        file_path: Optional[str] = None,
                        api_endpoint: Optional[str] = None) -> str:
        """
        Create a data sink
        
        Args:
            name: Sink name
            sink_type: Type of data sink
            connection_config: Connection configuration
            table_name: Table name (for database sinks)
            file_path: File path (for file sinks)
            api_endpoint: API endpoint (for API sinks)
            
        Returns:
            Sink ID
        """
        sink_id = str(uuid.uuid4())
        
        sink = DataSink(
            sink_id=sink_id,
            name=name,
            sink_type=sink_type,
            connection_config=connection_config,
            table_name=table_name,
            file_path=file_path,
            api_endpoint=api_endpoint,
            created_at=time.time()
        )
        
        self.data_sinks[sink_id] = sink
        self.logger.info(f"Created data sink: {sink_id}")
        
        return sink_id
    
    def create_pipeline(self,
                       name: str,
                       description: str,
                       tasks: List[Dict[str, Any]],
                       schedule: Optional[str] = None,
                       parallel_execution: bool = False) -> str:
        """
        Create a data pipeline
        
        Args:
            name: Pipeline name
            description: Pipeline description
            tasks: List of task configurations
            schedule: Cron schedule expression
            parallel_execution: Whether to execute tasks in parallel
            
        Returns:
            Pipeline ID
        """
        pipeline_id = str(uuid.uuid4())
        
        # Parse and create tasks
        pipeline_tasks = []
        for task_config in tasks:
            task_id = str(uuid.uuid4())
            
            task = PipelineTask(
                task_id=task_id,
                name=task_config.get("name", f"Task-{task_id[:8]}"),
                task_type=task_config.get("task_type", "extract"),
                source_id=task_config.get("source_id"),
                transform_id=task_config.get("transform_id"),
                sink_id=task_config.get("sink_id"),
                dependencies=task_config.get("dependencies", []),
                retry_count=0,
                max_retries=task_config.get("max_retries", self.retry_attempts),
                timeout=task_config.get("timeout", self.default_timeout),
                created_at=time.time()
            )
            
            pipeline_tasks.append(task)
        
        pipeline = DataPipeline(
            pipeline_id=pipeline_id,
            name=name,
            description=description,
            tasks=pipeline_tasks,
            schedule=schedule,
            parallel_execution=parallel_execution,
            created_at=time.time(),
            last_modified=time.time()
        )
        
        self.pipelines[pipeline_id] = pipeline
        self.execution_stats["total_pipelines"] += 1
        
        self.logger.info(f"Created pipeline: {pipeline_id}")
        return pipeline_id
    
    async def invoke_pipeline(self, pipeline_id: str) -> str:
        """
        Execute a data pipeline
        
        Args:
            pipeline_id: ID of pipeline to execute
            
        Returns:
            Execution ID
        """
        if pipeline_id not in self.pipelines:
            raise ValueError(f"Pipeline {pipeline_id} not found")
        
        if self.active_executions >= self.max_parallel_tasks:
            raise ValueError("Maximum parallel executions reached")
        
        pipeline = self.pipelines[pipeline_id]
        
        execution_id = str(uuid.uuid4())
        
        execution = PipelineExecution(
            execution_id=execution_id,
            pipeline_id=pipeline_id,
            status=PipelineStatus.PENDING,
            started_at=time.time(),
            completed_at=None,
            tasks_executed=0,
            tasks_completed=0,
            tasks_failed=0,
            total_duration=0.0,
            logs=[]
        )
        
        self.executions[execution_id] = execution
        self.active_executions += 1
        self.total_executions += 1
        
        # Execute pipeline asynchronously
        asyncio.create_task(self._execute_pipeline_async(execution_id, pipeline))
        
        self.logger.info(f"Started pipeline execution: {execution_id}")
        return execution_id
    
    async def _execute_pipeline_async(self, execution_id: str, pipeline: DataPipeline):
        """Execute pipeline asynchronously"""
        execution = self.executions[execution_id]
        execution.status = PipelineStatus.RUNNING
        
        start_time = time.time()
        
        try:
            # Sort tasks by dependencies
            sorted_tasks = self._topological_sort(pipeline.tasks)
            
            if pipeline.parallel_execution:
                await self._execute_parallel_tasks(execution, sorted_tasks)
            else:
                await self._execute_sequential_tasks(execution, sorted_tasks)
            
            # Complete successfully
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
    
    async def _execute_sequential_tasks(self, execution: PipelineExecution, tasks: List[PipelineTask]):
        """Execute tasks sequentially"""
        for task in tasks:
            await self._execute_task(execution, task)
    
    async def _execute_parallel_tasks(self, execution: PipelineExecution, tasks: List[PipelineTask]):
        """Execute tasks in parallel where possible"""
        # Group tasks by dependency level
        task_groups = self._group_tasks_by_dependency(tasks)
        
        for task_group in task_groups:
            # Execute tasks in current group in parallel
            tasks_coroutines = [self._execute_task(execution, task) for task in task_group]
            await asyncio.gather(*tasks_coroutines, return_exceptions=True)
    
    async def _execute_task(self, execution: PipelineExecution, task: PipelineTask):
        """Execute a single task"""
        execution.tasks_executed += 1
        execution.logs.append({
            "timestamp": time.time(),
            "level": "INFO",
            "message": f"Starting task: {task.name}"
        })
        
        start_time = time.time()
        
        try:
            # Execute task based on type
            if task.task_type == "extract":
                await self._execute_extract_task(task)
            elif task.task_type == "transform":
                await self._execute_transform_task(task)
            elif task.task_type == "load":
                await self._execute_load_task(task)
            
            # Task completed successfully
            execution.tasks_completed += 1
            execution.logs.append({
                "timestamp": time.time(),
                "level": "INFO",
                "message": f"Task completed: {task.name} ({time.time() - start_time:.2f}s)"
            })
            
        except Exception as e:
            execution.tasks_failed += 1
            execution.logs.append({
                "timestamp": time.time(),
                "level": "ERROR",
                "message": f"Task failed: {task.name} - {str(e)}"
            })
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                execution.logs.append({
                    "timestamp": time.time(),
                    "level": "INFO",
                    "message": f"Retrying task: {task.name} (attempt {task.retry_count})"
                })
                await asyncio.sleep(2 ** task.retry_count)  # Exponential backoff
                await self._execute_task(execution, task)
    
    async def _execute_extract_task(self, task: PipelineTask):
        """Execute extract task"""
        if not task.source_id or task.source_id not in self.data_sources:
            raise ValueError(f"Invalid source ID: {task.source_id}")
        
        source = self.data_sources[task.source_id]
        source.last_accessed = time.time()
        
        # Simulate data extraction
        await asyncio.sleep(1)
        
        # In a real implementation, this would connect to the actual data source
        if source.source_type == DataSourceType.DATABASE:
            # Simulate database query
            pass
        elif source.source_type == DataSourceType.FILE:
            # Simulate file reading
            pass
        elif source.source_type == DataSourceType.API:
            # Simulate API call
            pass
    
    async def _execute_transform_task(self, task: PipelineTask):
        """Execute transform task"""
        if not task.transform_id or task.transform_id not in self.transformations:
            raise ValueError(f"Invalid transform ID: {task.transform_id}")
        
        transformation = self.transformations[task.transform_id]
        
        # Simulate transformation execution
        await asyncio.sleep(2)
        
        # In a real implementation, this would execute the actual transformation code
        if transformation.transform_type == "python":
            # Execute Python code
            pass
        elif transformation.transform_type == "sql":
            # Execute SQL query
            pass
        elif transformation.transform_type == "pandas":
            # Execute pandas operations
            pass
    
    async def _execute_load_task(self, task: PipelineTask):
        """Execute load task"""
        if not task.sink_id or task.sink_id not in self.data_sinks:
            raise ValueError(f"Invalid sink ID: {task.sink_id}")
        
        sink = self.data_sinks[task.sink_id]
        
        # Simulate data loading
        await asyncio.sleep(1)
        
        # In a real implementation, this would connect to the actual data sink
        if sink.sink_type == "database":
            # Load to database
            pass
        elif sink.sink_type == "file":
            # Write to file
            pass
        elif sink.sink_type == "api":
            # Send to API
            pass
    
    def get_pipeline_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get pipeline execution status"""
        if execution_id not in self.executions:
            return None
        
        execution = self.executions[execution_id]
        
        return {
            "execution_id": execution.execution_id,
            "pipeline_id": execution.pipeline_id,
            "status": execution.status.value,
            "started_at": datetime.fromtimestamp(execution.started_at).isoformat(),
            "completed_at": datetime.fromtimestamp(execution.completed_at).isoformat() if execution.completed_at else None,
            "tasks_executed": execution.tasks_executed,
            "tasks_completed": execution.tasks_completed,
            "tasks_failed": execution.tasks_failed,
            "total_duration": execution.total_duration,
            "progress": execution.tasks_completed / len(self.pipelines[execution.pipeline_id].tasks) if execution.pipeline_id in self.pipelines else 0
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
            "average_execution_time": self.execution_stats["average_execution_time"],
            "max_parallel_tasks": self.max_parallel_tasks,
            "data_sources": len(self.data_sources),
            "transformations": len(self.transformations),
            "data_sinks": len(self.data_sinks)
        }
    
    def _topological_sort(self, tasks: List[PipelineTask]) -> List[PipelineTask]:
        """Sort tasks topologically based on dependencies"""
        # Create task lookup
        task_lookup = {t.task_id: t for t in tasks}
        
        # Calculate in-degrees
        in_degree = {t.task_id: 0 for t in tasks}
        for task in tasks:
            for dep in task.dependencies:
                in_degree[dep] += 1
        
        # Kahn's algorithm for topological sorting
        queue = [t_id for t_id, degree in in_degree.items() if degree == 0]
        sorted_tasks = []
        
        while queue:
            current = queue.pop(0)
            sorted_tasks.append(task_lookup[current])
            
            # Remove current from dependencies
            for task in tasks:
                if current in task.dependencies:
                    task.dependencies.remove(current)
                    in_degree[task.task_id] -= 1
                    
                    if in_degree[task.task_id] == 0:
                        queue.append(task.task_id)
        
        return sorted_tasks
    
    def _group_tasks_by_dependency(self, tasks: List[PipelineTask]) -> List[List[PipelineTask]]:
        """Group tasks by dependency level for parallel execution"""
        task_groups = []
        remaining_tasks = set(task.task_id for task in tasks)
        task_lookup = {t.task_id: t for t in tasks}
        
        while remaining_tasks:
            # Find tasks with no remaining dependencies
            current_group = []
            for task_id in list(remaining_tasks):
                task = task_lookup[task_id]
                if not any(dep in remaining_tasks for dep in task.dependencies):
                    current_group.append(task)
            
            if not current_group:
                break  # Circular dependency detected
            
            task_groups.append(current_group)
            remaining_tasks -= {t.task_id for t in current_group}
        
        return task_groups
    
    def _update_execution_stats(self):
        """Update execution statistics"""
        completed_executions = [e for e in self.executions.values() if e.status == PipelineStatus.COMPLETED]
        
        if completed_executions:
            total_time = sum(e.total_duration for e in completed_executions)
            self.execution_stats["average_execution_time"] = total_time / len(completed_executions)
    
    async def _scheduler_loop(self):
        """Background scheduler for scheduled pipelines"""
        while True:
            try:
                self._check_scheduled_pipelines()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(60)
    
    def _check_scheduled_pipelines(self):
        """Check for pipelines that should be executed based on schedule"""
        current_time = datetime.now()
        
        for pipeline in self.pipelines.values():
            if pipeline.schedule and self._should_execute_pipeline(pipeline.schedule, current_time):
                try:
                    asyncio.create_task(self.execute_pipeline(pipeline.pipeline_id))
                except Exception as e:
                    self.logger.error(f"Failed to schedule pipeline {pipeline.pipeline_id}: {e}")
    
    def _should_execute_pipeline(self, schedule: str, current_time: datetime) -> bool:
        """Check if pipeline should be executed based on schedule"""
        # Simple cron-like schedule parsing (simplified)
        # In a real implementation, you'd use a proper cron parser
        try:
            # For now, just check if it's a simple interval
            if schedule == "*/5 * * * *":  # Every 5 minutes
                return current_time.minute % 5 == 0
            elif schedule == "0 * * * *":  # Every hour
                return current_time.minute == 0
            elif schedule == "0 0 * * *":  # Daily at midnight
                return current_time.hour == 0 and current_time.minute == 0
            else:
                return False
        except:
            return False

# Global pipeline manager instance
_pipeline_manager = DataPipelineManager({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "create_source", "create_transformation", "create_sink", 
                     "create_pipeline", "execute", "get_status", "get_logs", "get_stats"
            - source_data: Data source configuration
            - transform_data: Transformation configuration
            - sink_data: Data sink configuration
            - pipeline_data: Pipeline configuration
            - execution_data: Execution parameters
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "create_source":
            source_data = payload.get("source_data", {})
            
            source_id = _pipeline_manager.create_data_source(
                name=source_data.get("name", "Data Source"),
                source_type=DataSourceType(source_data.get("source_type", "database")),
                connection_config=source_data.get("connection_config", {}),
                query=source_data.get("query"),
                file_path=source_data.get("file_path"),
                api_endpoint=source_data.get("api_endpoint")
            )
            
            return {
                "result": {
                    "source_id": source_id,
                    "message": f"Created data source: {source_id}"
                },
                "metadata": {
                    "action": "create_source",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_transformation":
            transform_data = payload.get("transform_data", {})
            
            transform_id = _pipeline_manager.create_transformation(
                name=transform_data.get("name", "Transformation"),
                transform_type=transform_data.get("transform_type", "python"),
                code=transform_data.get("code", ""),
                dependencies=transform_data.get("dependencies", [])
            )
            
            return {
                "result": {
                    "transform_id": transform_id,
                    "message": f"Created transformation: {transform_id}"
                },
                "metadata": {
                    "action": "create_transformation",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_sink":
            sink_data = payload.get("sink_data", {})
            
            sink_id = _pipeline_manager.create_data_sink(
                name=sink_data.get("name", "Data Sink"),
                sink_type=sink_data.get("sink_type", "database"),
                connection_config=sink_data.get("connection_config", {}),
                table_name=sink_data.get("table_name"),
                file_path=sink_data.get("file_path"),
                api_endpoint=sink_data.get("api_endpoint")
            )
            
            return {
                "result": {
                    "sink_id": sink_id,
                    "message": f"Created data sink: {sink_id}"
                },
                "metadata": {
                    "action": "create_sink",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_pipeline":
            pipeline_data = payload.get("pipeline_data", {})
            
            pipeline_id = _pipeline_manager.create_pipeline(
                name=pipeline_data.get("name", "Data Pipeline"),
                description=pipeline_data.get("description", ""),
                tasks=pipeline_data.get("tasks", []),
                schedule=pipeline_data.get("schedule"),
                parallel_execution=pipeline_data.get("parallel_execution", False)
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
        
        elif action == "execute":
            execution_data = payload.get("execution_data", {})
            
            execution_id = await _pipeline_manager.execute_pipeline(
                pipeline_id=execution_data.get("pipeline_id", "")
            )
            
            return {
                "result": {
                    "execution_id": execution_id,
                    "message": f"Started pipeline execution: {execution_id}"
                },
                "metadata": {
                    "action": "execute",
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
        logger.error(f"Error in data_pipeline_manager: {e}")
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
    """Example of how to use the data pipeline manager skill"""
    
    # Create data sources
    source_id = await invoke({
        "action": "create_source",
        "source_data": {
            "name": "Sales Database",
            "source_type": "database",
            "connection_config": {
                "host": "localhost",
                "port": 5432,
                "database": "sales",
                "user": "admin",
                "password": "password"
            },
            "query": "SELECT * FROM sales_data WHERE date >= CURRENT_DATE - INTERVAL '30 days'"
        }
    })
    
    print(f"Created data source: {source_id['result']['source_id']}")
    
    # Create transformation
    transform_id = await invoke({
        "action": "create_transformation",
        "transform_data": {
            "name": "Sales Aggregation",
            "transform_type": "python",
            "code": """
import pandas as pd

def transform(data):
    # Aggregate sales by region
    aggregated = data.groupby('region')['amount'].sum().reset_index()
    return aggregated
""",
            "dependencies": []
        }
    })
    
    print(f"Created transformation: {transform_id['result']['transform_id']}")
    
    # Create data sink
    sink_id = await invoke({
        "action": "create_sink",
        "sink_data": {
            "name": "Analytics Database",
            "sink_type": "database",
            "connection_config": {
                "host": "localhost",
                "port": 5432,
                "database": "analytics",
                "user": "admin",
                "password": "password"
            },
            "table_name": "aggregated_sales"
        }
    })
    
    print(f"Created data sink: {sink_id['result']['sink_id']}")
    
    # Create pipeline
    pipeline_id = await invoke({
        "action": "create_pipeline",
        "pipeline_data": {
            "name": "Sales Analytics Pipeline",
            "description": "ETL pipeline for sales data analytics",
            "tasks": [
                {
                    "name": "Extract Sales Data",
                    "task_type": "extract",
                    "source_id": source_id['result']['source_id'],
                    "dependencies": []
                },
                {
                    "name": "Aggregate Sales",
                    "task_type": "transform",
                    "transform_id": transform_id['result']['transform_id'],
                    "dependencies": ["Extract Sales Data"]
                },
                {
                    "name": "Load to Analytics",
                    "task_type": "load",
                    "sink_id": sink_id['result']['sink_id'],
                    "dependencies": ["Aggregate Sales"]
                }
            ],
            "schedule": "0 2 * * *",  # Daily at 2 AM
            "parallel_execution": False
        }
    })
    
    print(f"Created pipeline: {pipeline_id['result']['pipeline_id']}")
    
    # Execute pipeline
    execution_id = await invoke({
        "action": "execute",
        "execution_data": {
            "pipeline_id": pipeline_id['result']['pipeline_id']
        }
    })
    
    print(f"Started execution: {execution_id['result']['execution_id']}")
    
    # Get pipeline statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Pipeline stats: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())