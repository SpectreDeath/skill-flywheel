#!/usr/bin/env python3
"""
Skill: workflow-orchestrator
Domain: orchestration
Description: Workflow orchestration and task management system
"""

import asyncio
import logging
import time
import uuid
import json
import yaml
from typing import Dict, Any, List, Optional, Union, Callable, Awaitable
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict, deque
import hashlib
import random
from pathlib import Path

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    """Task execution statuses"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"

class TaskType(Enum):
    """Task types"""
    COMPUTE = "compute"
    IO = "io"
    API_CALL = "api_call"
    TRANSFORMATION = "transformation"
    VALIDATION = "validation"
    NOTIFICATION = "notification"

class WorkflowStatus(Enum):
    """Workflow execution statuses"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class DependencyType(Enum):
    """Dependency types"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    DYNAMIC = "dynamic"

@dataclass
class Task:
    """Represents a workflow task"""
    task_id: str
    name: str
    task_type: TaskType
    function: str  # Function name to execute
    parameters: Dict[str, Any]
    dependencies: List[str]
    retry_count: int
    max_retries: int
    timeout: int
    priority: int
    created_at: float

@dataclass
class TaskExecution:
    """Represents a task execution"""
    execution_id: str
    task_id: str
    status: TaskStatus
    started_at: float
    completed_at: Optional[float]
    duration: float
    result: Optional[Any]
    error_message: Optional[str]
    retry_attempt: int
    created_at: float

@dataclass
class Workflow:
    """Represents a workflow definition"""
    workflow_id: str
    name: str
    description: str
    tasks: List[str]
    entry_points: List[str]
    exit_points: List[str]
    parallelism: int
    timeout: int
    retry_policy: Dict[str, Any]
    created_at: float

@dataclass
class WorkflowExecution:
    """Represents a workflow execution"""
    execution_id: str
    workflow_id: str
    status: WorkflowStatus
    started_at: float
    completed_at: Optional[float]
    duration: float
    tasks_executed: int
    tasks_completed: int
    tasks_failed: int
    tasks_cancelled: int
    result: Optional[Any]
    error_message: Optional[str]
    created_at: float

@dataclass
class TaskQueue:
    """Represents a task queue"""
    queue_id: str
    name: str
    tasks: deque
    max_concurrency: int
    active_tasks: int
    created_at: float

class WorkflowOrchestrator:
    """Workflow orchestration and task management system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the workflow orchestrator
        
        Args:
            config: Configuration dictionary with:
                - max_concurrent_workflows: Maximum concurrent workflows
                - max_concurrent_tasks: Maximum concurrent tasks per workflow
                - default_task_timeout: Default task timeout
                - retry_backoff_factor: Retry backoff factor
        """
        self.max_concurrent_workflows = config.get("max_concurrent_workflows", 10)
        self.max_concurrent_tasks = config.get("max_concurrent_tasks", 50)
        self.default_task_timeout = config.get("default_task_timeout", 300)
        self.retry_backoff_factor = config.get("retry_backoff_factor", 2.0)
        
        self.workflows: Dict[str, Workflow] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_executions: Dict[str, TaskExecution] = {}
        self.workflow_executions: Dict[str, WorkflowExecution] = {}
        self.task_queues: Dict[str, TaskQueue] = {}
        
        self.active_workflows = 0
        self.total_workflows = 0
        self.orchestrator_stats = {
            "total_workflows": 0,
            "completed_workflows": 0,
            "failed_workflows": 0,
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "average_workflow_time": 0.0,
            "average_task_time": 0.0
        }
        
        self.task_registry: Dict[str, Callable] = {}
        self.execution_context: Dict[str, Any] = {}
        
        self.logger = logging.getLogger(__name__)
        
        # Start background services
        self._orchestrator_task = asyncio.create_task(self._orchestrator_loop())
        self._task_monitor_task = asyncio.create_task(self._task_monitor_loop())
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    def register_task_function(self, name: str, function: Callable):
        """Register a task function"""
        self.task_registry[name] = function
        self.logger.info(f"Registered task function: {name}")
    
    def create_workflow(self,
                       name: str,
                       description: str,
                       tasks: List[Dict[str, Any]],
                       entry_points: List[str],
                       exit_points: List[str],
                       parallelism: int = 1,
                       timeout: int = 3600,
                       retry_policy: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a workflow definition
        
        Args:
            name: Workflow name
            description: Workflow description
            tasks: List of task definitions
            entry_points: Entry point task IDs
            exit_points: Exit point task IDs
            parallelism: Maximum parallel tasks
            timeout: Workflow timeout in seconds
            retry_policy: Retry policy configuration
            
        Returns:
            Workflow ID
        """
        workflow_id = str(uuid.uuid4())
        
        # Create tasks
        task_ids = []
        for task_config in tasks:
            task_id = self._create_task(task_config)
            task_ids.append(task_id)
        
        workflow = Workflow(
            workflow_id=workflow_id,
            name=name,
            description=description,
            tasks=task_ids,
            entry_points=entry_points,
            exit_points=exit_points,
            parallelism=parallelism,
            timeout=timeout,
            retry_policy=retry_policy or {"max_retries": 3, "backoff_factor": 2.0},
            created_at=time.time()
        )
        
        self.workflows[workflow_id] = workflow
        self.orchestrator_stats["total_workflows"] += 1
        
        self.logger.info(f"Created workflow: {workflow_id} ({name})")
        return workflow_id
    
    def _create_task(self, task_config: Dict[str, Any]) -> str:
        """Create a task"""
        task_id = str(uuid.uuid4())
        
        task = Task(
            task_id=task_id,
            name=task_config.get("name", f"Task-{task_id[:8]}"),
            task_type=TaskType(task_config.get("task_type", "compute")),
            function=task_config.get("function", ""),
            parameters=task_config.get("parameters", {}),
            dependencies=task_config.get("dependencies", []),
            retry_count=0,
            max_retries=task_config.get("max_retries", 3),
            timeout=task_config.get("timeout", self.default_task_timeout),
            priority=task_config.get("priority", 0),
            created_at=time.time()
        )
        
        self.tasks[task_id] = task
        self.orchestrator_stats["total_tasks"] += 1
        
        return task_id
    
    async def execute_workflow(self,
                              workflow_id: str,
                              context: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute a workflow
        
        Args:
            workflow_id: Workflow ID
            context: Execution context
            
        Returns:
            Execution ID
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        if self.active_workflows >= self.max_concurrent_workflows:
            raise ValueError("Maximum concurrent workflows reached")
        
        workflow = self.workflows[workflow_id]
        
        execution_id = str(uuid.uuid4())
        
        execution = WorkflowExecution(
            execution_id=execution_id,
            workflow_id=workflow_id,
            status=WorkflowStatus.PENDING,
            started_at=time.time(),
            completed_at=None,
            duration=0.0,
            tasks_executed=0,
            tasks_completed=0,
            tasks_failed=0,
            tasks_cancelled=0,
            result=None,
            error_message=None,
            created_at=time.time()
        )
        
        self.workflow_executions[execution_id] = execution
        self.active_workflows += 1
        self.total_workflows += 1
        
        # Execute workflow asynchronously
        asyncio.create_task(self._execute_workflow_async(execution_id, workflow, context))
        
        self.logger.info(f"Started workflow execution: {execution_id}")
        return execution_id
    
    def get_workflow_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow execution status"""
        if execution_id not in self.workflow_executions:
            return None
        
        execution = self.workflow_executions[execution_id]
        
        return {
            "execution_id": execution.execution_id,
            "workflow_id": execution.workflow_id,
            "status": execution.status.value,
            "started_at": datetime.fromtimestamp(execution.started_at).isoformat(),
            "completed_at": datetime.fromtimestamp(execution.completed_at).isoformat() if execution.completed_at else None,
            "duration": execution.duration,
            "tasks_executed": execution.tasks_executed,
            "tasks_completed": execution.tasks_completed,
            "tasks_failed": execution.tasks_failed,
            "tasks_cancelled": execution.tasks_cancelled,
            "progress": execution.tasks_completed / len(self.workflows[execution.workflow_id].tasks) if execution.workflow_id in self.workflows else 0
        }
    
    def get_task_status(self, execution_id: str, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task execution status"""
        # Find task execution for this workflow execution
        for exec_id, task_exec in self.task_executions.items():
            if task_exec.task_id == task_id and exec_id.startswith(execution_id):
                return {
                    "execution_id": exec_id,
                    "task_id": task_exec.task_id,
                    "status": task_exec.status.value,
                    "started_at": datetime.fromtimestamp(task_exec.started_at).isoformat(),
                    "completed_at": datetime.fromtimestamp(task_exec.completed_at).isoformat() if task_exec.completed_at else None,
                    "duration": task_exec.duration,
                    "retry_attempt": task_exec.retry_attempt,
                    "result": task_exec.result,
                    "error_message": task_exec.error_message
                }
        return None
    
    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            "total_workflows": self.orchestrator_stats["total_workflows"],
            "active_workflows": self.active_workflows,
            "completed_workflows": self.orchestrator_stats["completed_workflows"],
            "failed_workflows": self.orchestrator_stats["failed_workflows"],
            "total_tasks": self.orchestrator_stats["total_tasks"],
            "completed_tasks": self.orchestrator_stats["completed_tasks"],
            "failed_tasks": self.orchestrator_stats["failed_tasks"],
            "average_workflow_time": self.orchestrator_stats["average_workflow_time"],
            "average_task_time": self.orchestrator_stats["average_task_time"],
            "total_queues": len(self.task_queues),
            "registered_functions": len(self.task_registry)
        }
    
    async def _execute_workflow_async(self, execution_id: str, workflow: Workflow, context: Optional[Dict[str, Any]]):
        """Execute workflow asynchronously"""
        execution = self.workflow_executions[execution_id]
        execution.status = WorkflowStatus.RUNNING
        
        start_time = time.time()
        
        try:
            # Build execution graph
            execution_graph = self._build_execution_graph(workflow)
            
            # Execute workflow
            await self._execute_execution_graph(execution, execution_graph, context)
            
            # Complete successfully
            execution.status = WorkflowStatus.COMPLETED
            execution.completed_at = time.time()
            execution.duration = time.time() - start_time
            self.orchestrator_stats["completed_workflows"] += 1
            
            # Update average workflow time
            total_time = self.orchestrator_stats["average_workflow_time"] * (self.orchestrator_stats["completed_workflows"] - 1)
            self.orchestrator_stats["average_workflow_time"] = (total_time + execution.duration) / self.orchestrator_stats["completed_workflows"]
            
            self.logger.info(f"Workflow execution {execution_id} completed successfully")
            
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.completed_at = time.time()
            execution.duration = time.time() - start_time
            execution.error_message = str(e)
            self.orchestrator_stats["failed_workflows"] += 1
            
            self.logger.error(f"Workflow execution {execution_id} failed: {e}")
        
        finally:
            self.active_workflows -= 1
    
    def _build_execution_graph(self, workflow: Workflow) -> Dict[str, List[str]]:
        """Build execution dependency graph"""
        graph = defaultdict(list)
        
        for task_id in workflow.tasks:
            task = self.tasks[task_id]
            for dep_id in task.dependencies:
                graph[dep_id].append(task_id)
        
        return dict(graph)
    
    async def _execute_execution_graph(self,
                                     execution: WorkflowExecution,
                                     graph: Dict[str, List[str]],
                                     context: Optional[Dict[str, Any]]):
        """Execute workflow execution graph"""
        # Track task dependencies
        dependency_count = defaultdict(int)
        for task_id in execution.workflow_id in self.workflows and self.workflows[execution.workflow_id].tasks or []:
            dependency_count[task_id] = len(self.tasks[task_id].dependencies)
        
        # Find ready tasks (no dependencies)
        ready_tasks = [
            task_id for task_id in (execution.workflow_id in self.workflows and self.workflows[execution.workflow_id].tasks or [])
            if dependency_count[task_id] == 0
        ]
        
        # Execute tasks
        while ready_tasks:
            # Execute tasks in parallel up to workflow parallelism limit
            concurrent_tasks = min(len(ready_tasks), execution.workflow_id in self.workflows and self.workflows[execution.workflow_id].parallelism or 1)
            
            task_coroutines = []
            for _ in range(concurrent_tasks):
                task_id = ready_tasks.pop(0)
                task_coroutines.append(self._execute_task(execution, task_id, context))
            
            # Wait for current batch to complete
            results = await asyncio.gather(*task_coroutines, return_exceptions=True)
            
            # Update dependency counts and add new ready tasks
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    # Task failed
                    execution.tasks_failed += 1
                    self.orchestrator_stats["failed_tasks"] += 1
                    self.logger.error(f"Task failed: {result}")
                else:
                    # Task completed successfully
                    task_id = result
                    execution.tasks_completed += 1
                    self.orchestrator_stats["completed_tasks"] += 1
                    
                    # Update dependencies
                    for dependent_task in graph.get(task_id, []):
                        dependency_count[dependent_task] -= 1
                        if dependency_count[dependent_task] == 0:
                            ready_tasks.append(dependent_task)
            
            execution.tasks_executed += len(task_coroutines)
    
    async def _execute_task(self,
                           execution: WorkflowExecution,
                           task_id: str,
                           context: Optional[Dict[str, Any]]) -> str:
        """Execute a single task"""
        task = self.tasks[task_id]
        
        execution_id = f"{execution.execution_id}_{task_id}"
        
        task_execution = TaskExecution(
            execution_id=execution_id,
            task_id=task_id,
            status=TaskStatus.PENDING,
            started_at=time.time(),
            completed_at=None,
            duration=0.0,
            result=None,
            error_message=None,
            retry_attempt=0,
            created_at=time.time()
        )
        
        self.task_executions[execution_id] = task_execution
        
        # Execute task with retries
        for attempt in range(task.max_retries + 1):
            task_execution.retry_attempt = attempt
            task_execution.status = TaskStatus.RUNNING
            
            try:
                # Execute task function
                if task.function in self.task_registry:
                    func = self.task_registry[task.function]
                    result = await asyncio.wait_for(
                        func(task.parameters, context),
                        timeout=task.timeout
                    )
                    task_execution.result = result
                    task_execution.status = TaskStatus.COMPLETED
                    task_execution.completed_at = time.time()
                    task_execution.duration = task_execution.completed_at - task_execution.started_at
                    
                    # Update average task time
                    total_time = self.orchestrator_stats["average_task_time"] * (self.orchestrator_stats["completed_tasks"] - 1)
                    self.orchestrator_stats["average_task_time"] = (total_time + task_execution.duration) / self.orchestrator_stats["completed_tasks"]
                    
                    self.logger.info(f"Task {task_id} completed successfully")
                    return task_id
                    
                else:
                    raise ValueError(f"Task function {task.function} not registered")
            
            except Exception as e:
                task_execution.error_message = str(e)
                task_execution.status = TaskStatus.FAILED
                
                if attempt < task.max_retries:
                    # Wait before retry
                    await asyncio.sleep(self.retry_backoff_factor ** attempt)
                    continue
                else:
                    # Max retries exceeded
                    self.logger.error(f"Task {task_id} failed after {task.max_retries} retries: {e}")
                    raise e
    
    async def _orchestrator_loop(self):
        """Background orchestrator monitoring loop"""
        while True:
            try:
                await self._monitor_workflows()
                await asyncio.sleep(30)
            except Exception as e:
                self.logger.error(f"Error in orchestrator loop: {e}")
                await asyncio.sleep(30)
    
    async def _monitor_workflows(self):
        """Monitor workflow health and performance"""
        # Check for timed-out workflows
        current_time = time.time()
        
        for execution_id, execution in list(self.workflow_executions.items()):
            if execution.status == WorkflowStatus.RUNNING:
                workflow = self.workflows[execution.workflow_id]
                if current_time - execution.started_at > workflow.timeout:
                    execution.status = WorkflowStatus.FAILED
                    execution.error_message = "Workflow timed out"
                    self.active_workflows -= 1
                    self.logger.warning(f"Workflow {execution_id} timed out")
    
    async def _task_monitor_loop(self):
        """Background task monitor loop"""
        while True:
            try:
                await self._monitor_tasks()
                await asyncio.sleep(10)
            except Exception as e:
                self.logger.error(f"Error in task monitor loop: {e}")
                await asyncio.sleep(10)
    
    async def _monitor_tasks(self):
        """Monitor task health and performance"""
        # Check for timed-out tasks
        current_time = time.time()
        
        for execution_id, task_exec in list(self.task_executions.items()):
            if task_exec.status == TaskStatus.RUNNING:
                task = self.tasks[task_exec.task_id]
                if current_time - task_exec.started_at > task.timeout:
                    task_exec.status = TaskStatus.FAILED
                    task_exec.error_message = "Task timed out"
                    self.logger.warning(f"Task {execution_id} timed out")
    
    async def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            try:
                await self._cleanup_old_executions()
                await asyncio.sleep(3600)  # Run every hour
            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(3600)
    
    async def _cleanup_old_executions(self):
        """Clean up old execution records"""
        cutoff_time = time.time() - (24 * 3600)  # 24 hours ago
        
        # Clean up old workflow executions
        for execution_id, execution in list(self.workflow_executions.items()):
            if execution.created_at < cutoff_time:
                del self.workflow_executions[execution_id]
        
        # Clean up old task executions
        for execution_id, task_exec in list(self.task_executions.items()):
            if task_exec.created_at < cutoff_time:
                del self.task_executions[execution_id]

# Global workflow orchestrator instance
_workflow_orchestrator = WorkflowOrchestrator({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "register_function", "create_workflow", "execute_workflow", 
                     "get_status", "get_task_status", "get_stats"
            - function_data: Function registration data
            - workflow_data: Workflow definition
            - execution_data: Execution parameters
            - context_data: Execution context
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "register_function":
            function_data = payload.get("function_data", {})
            
            # In a real implementation, this would register the function
            # For now, simulate registration
            function_name = function_data.get("name", "test_function")
            _workflow_orchestrator.register_task_function(function_name, lambda x, y: None)
            
            return {
                "result": {
                    "function_name": function_name,
                    "message": f"Registered function: {function_name}"
                },
                "metadata": {
                    "action": "register_function",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_workflow":
            workflow_data = payload.get("workflow_data", {})
            
            workflow_id = _workflow_orchestrator.create_workflow(
                name=workflow_data.get("name", "Workflow"),
                description=workflow_data.get("description", ""),
                tasks=workflow_data.get("tasks", []),
                entry_points=workflow_data.get("entry_points", []),
                exit_points=workflow_data.get("exit_points", []),
                parallelism=workflow_data.get("parallelism", 1),
                timeout=workflow_data.get("timeout", 3600),
                retry_policy=workflow_data.get("retry_policy")
            )
            
            return {
                "result": {
                    "workflow_id": workflow_id,
                    "message": f"Created workflow: {workflow_id}"
                },
                "metadata": {
                    "action": "create_workflow",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "execute_workflow":
            execution_data = payload.get("execution_data", {})
            
            execution_id = await _workflow_orchestrator.execute_workflow(
                workflow_id=execution_data.get("workflow_id", ""),
                context=execution_data.get("context")
            )
            
            return {
                "result": {
                    "execution_id": execution_id,
                    "message": f"Started workflow execution: {execution_id}"
                },
                "metadata": {
                    "action": "execute_workflow",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_status":
            execution_id = payload.get("execution_id", "")
            status = _workflow_orchestrator.get_workflow_status(execution_id)
            
            return {
                "result": status,
                "metadata": {
                    "action": "get_status",
                    "timestamp": datetime.now().isoformat(),
                    "execution_id": execution_id
                }
            }
        
        elif action == "get_task_status":
            execution_id = payload.get("execution_id", "")
            task_id = payload.get("task_id", "")
            status = _workflow_orchestrator.get_task_status(execution_id, task_id)
            
            return {
                "result": status,
                "metadata": {
                    "action": "get_task_status",
                    "timestamp": datetime.now().isoformat(),
                    "execution_id": execution_id,
                    "task_id": task_id
                }
            }
        
        elif action == "get_stats":
            stats = _workflow_orchestrator.get_orchestrator_stats()
            
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
        logger.error(f"Error in workflow_orchestrator: {e}")
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
    """Example of how to use the workflow orchestrator skill"""
    
    # Register task functions
    def process_data(params, context):
        """Simulate data processing task"""
        import time
        time.sleep(1)  # Simulate processing time
        return {"processed": True, "data": params.get("data", [])}
    
    def validate_data(params, context):
        """Simulate data validation task"""
        import time
        time.sleep(0.5)  # Simulate validation time
        return {"valid": True, "errors": []}
    
    def send_notification(params, context):
        """Simulate notification task"""
        import time
        time.sleep(0.2)  # Simulate notification time
        return {"notified": True, "method": params.get("method", "email")}
    
    _workflow_orchestrator.register_task_function("process_data", process_data)
    _workflow_orchestrator.register_task_function("validate_data", validate_data)
    _workflow_orchestrator.register_task_function("send_notification", send_notification)
    
    print("Registered task functions")
    
    # Create workflow
    workflow_id = await invoke({
        "action": "create_workflow",
        "workflow_data": {
            "name": "Data Processing Workflow",
            "description": "Process and validate data, then send notification",
            "tasks": [
                {
                    "name": "Data Validation",
                    "task_type": "validation",
                    "function": "validate_data",
                    "parameters": {"data": [1, 2, 3, 4, 5]},
                    "dependencies": [],
                    "max_retries": 2,
                    "timeout": 60,
                    "priority": 1
                },
                {
                    "name": "Data Processing",
                    "task_type": "compute",
                    "function": "process_data",
                    "parameters": {"data": [1, 2, 3, 4, 5]},
                    "dependencies": ["Data Validation"],
                    "max_retries": 3,
                    "timeout": 120,
                    "priority": 2
                },
                {
                    "name": "Send Notification",
                    "task_type": "notification",
                    "function": "send_notification",
                    "parameters": {"method": "email", "message": "Processing complete"},
                    "dependencies": ["Data Processing"],
                    "max_retries": 1,
                    "timeout": 30,
                    "priority": 3
                }
            ],
            "entry_points": ["Data Validation"],
            "exit_points": ["Send Notification"],
            "parallelism": 2,
            "timeout": 300,
            "retry_policy": {"max_retries": 3, "backoff_factor": 2.0}
        }
    })
    
    print(f"Created workflow: {workflow_id['result']['workflow_id']}")
    
    # Execute workflow
    execution_id = await invoke({
        "action": "execute_workflow",
        "execution_data": {
            "workflow_id": workflow_id['result']['workflow_id'],
            "context": {"user_id": "user123", "timestamp": time.time()}
        }
    })
    
    print(f"Started execution: {execution_id['result']['execution_id']}")
    
    # Monitor workflow execution
    import time as t
    for i in range(10):
        status = await invoke({
            "action": "get_status",
            "execution_id": execution_id['result']['execution_id']
        })
        
        if status['result']:
            print(f"Workflow status: {status['result']['status']} - {status['result']['tasks_completed']}/{status['result']['tasks_executed']} tasks completed")
            
            if status['result']['status'] in ['completed', 'failed']:
                break
        
        t.sleep(1)
    
    # Get task status
    task_status = await invoke({
        "action": "get_task_status",
        "execution_id": execution_id['result']['execution_id'],
        "task_id": "Data Processing"
    })
    
    print(f"Task status: {task_status['result']}")
    
    # Get orchestrator statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Orchestrator stats: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())