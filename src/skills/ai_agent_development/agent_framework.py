#!/usr/bin/env python3
"""
Skill: agent-framework
Domain: ai_agent_development
Description: Framework for building and managing AI agents with standardized interfaces
"""

import asyncio
import logging
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from collections.abc import Callable

logger = logging.getLogger(__name__)

class AgentState(Enum):
    """Agent states"""
    INITIALIZING = "initializing"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    SHUTDOWN = "shutdown"

class AgentCapability(Enum):
    """Agent capabilities"""
    REASONING = "reasoning"
    MEMORY = "memory"
    COMMUNICATION = "communication"
    TOOL_USE = "tool_use"
    LEARNING = "learning"
    PLANNING = "planning"

@dataclass
class AgentConfig:
    """Agent configuration"""
    agent_id: str
    name: str
    description: str
    capabilities: List[AgentCapability]
    memory_size: int = 1000
    max_concurrent_tasks: int = 5
    timeout: int = 300
    retry_attempts: int = 3

@dataclass
class AgentTask:
    """Represents a task for an agent"""
    task_id: str
    task_type: str
    input_data: Dict[str, Any]
    priority: int
    created_at: float
    assigned_at: Optional[float]
    completed_at: Optional[float]
    status: str  # pending, assigned, completed, failed
    result: Optional[Dict[str, Any]]
    error: Optional[str]

@dataclass
class AgentMessage:
    """Represents a message to/from an agent"""
    message_id: str
    sender: str
    receiver: str
    content: Dict[str, Any]
    message_type: str  # request, response, notification
    timestamp: float

class AgentFramework:
    """Framework for building and managing AI agents"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the agent framework
        
        Args:
            config: Framework configuration
        """
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, AgentTask] = {}
        self.message_queue: List[AgentMessage] = []
        self.capability_registry: Dict[AgentCapability, List[str]] = {}
        self.logger = logging.getLogger(__name__)
        
    def create_agent(self, config: AgentConfig) -> str:
        """
        Create a new agent
        
        Args:
            config: Agent configuration
            
        Returns:
            Agent ID
        """
        agent = Agent(config, self)
        self.agents[agent.agent_id] = agent
        
        # Register capabilities
        for capability in config.capabilities:
            if capability not in self.capability_registry:
                self.capability_registry[capability] = []
            self.capability_registry[capability].append(agent.agent_id)
        
        self.logger.info(f"Created agent: {agent.agent_id} ({agent.name})")
        return agent.agent_id
    
    def get_agents_by_capability(self, capability: AgentCapability) -> List[str]:
        """Get all agents with a specific capability"""
        return self.capability_registry.get(capability, [])
    
    def assign_task(self, agent_id: str, task: AgentTask) -> bool:
        """Assign a task to an agent"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        if agent.state != AgentState.READY:
            return False
        
        # Check if agent has capacity
        if len(agent.active_tasks) >= agent.config.max_concurrent_tasks:
            return False
        
        task.assigned_at = time.time()
        task.status = "assigned"
        self.tasks[task.task_id] = task
        agent.active_tasks.append(task.task_id)
        agent.state = AgentState.BUSY
        
        # Execute task asynchronously
        asyncio.create_task(agent.execute_task(task))
        
        return True
    
    def broadcast_message(self, message: AgentMessage):
        """Broadcast a message to all agents"""
        self.message_queue.append(message)
        
        # Deliver to matching agents
        for agent in self.agents.values():
            if agent.agent_id == message.receiver or message.receiver == "all":
                asyncio.create_task(agent.receive_message(message))
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent status information"""
        if agent_id not in self.agents:
            return None
        
        agent = self.agents[agent_id]
        return {
            "agent_id": agent.agent_id,
            "name": agent.name,
            "state": agent.state.value,
            "capabilities": [c.value for c in agent.config.capabilities],
            "active_tasks": len(agent.active_tasks),
            "total_tasks": agent.total_tasks,
            "success_rate": agent.success_rate,
            "memory_usage": len(agent.memory),
            "last_activity": agent.last_activity
        }
    
    def shutdown_agent(self, agent_id: str) -> bool:
        """Shutdown an agent"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        agent.state = AgentState.SHUTDOWN
        agent.shutdown()
        
        # Remove from registries
        del self.agents[agent_id]
        for capability_list in self.capability_registry.values():
            if agent_id in capability_list:
                capability_list.remove(agent_id)
        
        self.logger.info(f"Shutdown agent: {agent_id}")
        return True

class Agent:
    """Base agent class with standardized interfaces"""
    
    def __init__(self, config: AgentConfig, framework: AgentFramework):
        self.config = config
        self.framework = framework
        self.state = AgentState.INITIALIZING
        self.memory: List[Dict[str, Any]] = []
        self.active_tasks: List[str] = []
        self.total_tasks = 0
        self.successful_tasks = 0
        self.last_activity = time.time()
        self.logger = logging.getLogger(f"{__name__}.{config.name}")
        
        # Initialize capabilities
        self.capabilities: Dict[AgentCapability, Any] = {}
        for capability in config.capabilities:
            self.capabilities[capability] = self._initialize_capability(capability)
        
        self.state = AgentState.READY
        self.logger.info(f"Agent {config.name} initialized and ready")
    
    def _initialize_capability(self, capability: AgentCapability):
        """Initialize a specific capability"""
        if capability == AgentCapability.MEMORY:
            return MemoryModule(self.config.memory_size)
        elif capability == AgentCapability.REASONING:
            return ReasoningModule()
        elif capability == AgentCapability.COMMUNICATION:
            return CommunicationModule()
        elif capability == AgentCapability.TOOL_USE:
            return ToolUseModule()
        elif capability == AgentCapability.LEARNING:
            return LearningModule()
        elif capability == AgentCapability.PLANNING:
            return PlanningModule()
        else:
            return None
    
    async def invoke_task(self, task: AgentTask):
        """Execute a task"""
        self.state = AgentState.BUSY
        self.last_activity = time.time()
        
        try:
            # Process task through capabilities
            result = await self._process_task(task)
            
            # Store result in memory
            self.memory.append({
                "task_id": task.task_id,
                "input": task.input_data,
                "output": result,
                "timestamp": time.time()
            })
            
            # Maintain memory size
            if len(self.memory) > self.config.memory_size:
                self.memory.pop(0)
            
            # Update task status
            task.status = "completed"
            task.completed_at = time.time()
            task.result = result
            self.successful_tasks += 1
            
            self.logger.info(f"Task {task.task_id} completed successfully")
            
        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            self.logger.error(f"Task {task.task_id} failed: {e}")
        
        finally:
            # Clean up
            if task.task_id in self.active_tasks:
                self.active_tasks.remove(task.task_id)
            
            self.total_tasks += 1
            self.state = AgentState.READY if not self.active_tasks else AgentState.BUSY
    
    async def _process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Process a task through the agent's capabilities"""
        result = {
            "task_id": task.task_id,
            "task_type": task.task_type,
            "input": task.input_data,
            "output": None,
            "metadata": {
                "agent_id": self.config.agent_id,
                "timestamp": time.time(),
                "capabilities_used": []
            }
        }
        
        # Use appropriate capabilities based on task type
        if task.task_type == "reasoning":
            if AgentCapability.REASONING in self.capabilities:
                reasoning_result = await self.capabilities[AgentCapability.REASONING].reason(task.input_data)
                result["output"] = reasoning_result
                result["metadata"]["capabilities_used"].append("reasoning")
        
        elif task.task_type == "memory":
            if AgentCapability.MEMORY in self.capabilities:
                memory_result = await self.capabilities[AgentCapability.MEMORY].retrieve(task.input_data)
                result["output"] = memory_result
                result["metadata"]["capabilities_used"].append("memory")
        
        elif task.task_type == "tool_use":
            if AgentCapability.TOOL_USE in self.capabilities:
                tool_result = await self.capabilities[AgentCapability.TOOL_USE].execute(task.input_data)
                result["output"] = tool_result
                result["metadata"]["capabilities_used"].append("tool_use")
        
        elif task.task_type == "learning":
            if AgentCapability.LEARNING in self.capabilities:
                learning_result = await self.capabilities[AgentCapability.LEARNING].learn(task.input_data)
                result["output"] = learning_result
                result["metadata"]["capabilities_used"].append("learning")
        
        elif task.task_type == "planning":
            if AgentCapability.PLANNING in self.capabilities:
                planning_result = await self.capabilities[AgentCapability.PLANNING].plan(task.input_data)
                result["output"] = planning_result
                result["metadata"]["capabilities_used"].append("planning")
        
        else:
            # Default processing
            result["output"] = {"message": f"Task processed by {self.config.name}", "input": task.input_data}
        
        return result
    
    async def receive_message(self, message: AgentMessage):
        """Receive and process a message"""
        self.last_activity = time.time()
        
        if message.message_type == "request":
            # Process request
            response = await self._handle_request(message.content)
            response_message = AgentMessage(
                message_id=str(uuid.uuid4()),
                sender=self.config.agent_id,
                receiver=message.sender,
                content=response,
                message_type="response",
                timestamp=time.time()
            )
            self.framework.broadcast_message(response_message)
        
        elif message.message_type == "notification":
            # Handle notification
            await self._handle_notification(message.content)
    
    async def _handle_request(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming request"""
        request_type = content.get("type", "unknown")
        
        if request_type == "status":
            return self.get_status()
        elif request_type == "capabilities":
            return {"capabilities": [c.value for c in self.config.capabilities]}
        elif request_type == "memory_query":
            if AgentCapability.MEMORY in self.capabilities:
                return await self.capabilities[AgentCapability.MEMORY].query(content.get("query", ""))
        
        return {"error": f"Unknown request type: {request_type}"}
    
    async def _handle_notification(self, content: Dict[str, Any]):
        """Handle incoming notification"""
        notification_type = content.get("type", "unknown")
        self.logger.debug(f"Received notification: {notification_type}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        self.success_rate = self.successful_tasks / self.total_tasks if self.total_tasks > 0 else 0.0
        
        return {
            "agent_id": self.config.agent_id,
            "name": self.config.name,
            "state": self.state.value,
            "memory_usage": len(self.memory),
            "active_tasks": len(self.active_tasks),
            "total_tasks": self.total_tasks,
            "successful_tasks": self.successful_tasks,
            "success_rate": self.success_rate,
            "last_activity": self.last_activity
        }
    
    def shutdown(self):
        """Shutdown the agent"""
        self.state = AgentState.SHUTDOWN
        self.logger.info(f"Agent {self.config.name} shutting down")

class MemoryModule:
    """Memory management capability"""
    
    def __init__(self, memory_size: int):
        self.memory_size = memory_size
        self.memory: List[Dict[str, Any]] = []
    
    async def store(self, data: Dict[str, Any]) -> bool:
        """Store data in memory"""
        self.memory.append({
            "data": data,
            "timestamp": time.time(),
            "id": str(uuid.uuid4())
        })
        
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)
        
        return True
    
    async def retrieve(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retrieve data from memory based on query"""
        # Simple keyword matching for now
        query_text = query.get("text", "").lower()
        results = []
        
        for item in self.memory:
            if query_text in str(item["data"]).lower():
                results.append(item)
        
        return results
    
    async def query(self, query_text: str) -> List[Dict[str, Any]]:
        """Query memory for specific information"""
        return await self.retrieve({"text": query_text})
    
    async def clear(self) -> bool:
        """Clear all memory"""
        self.memory.clear()
        return True

class ReasoningModule:
    """Reasoning capability"""
    
    async def reason(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform reasoning on input data"""
        # Simulate reasoning process
        await asyncio.sleep(0.5)
        
        return {
            "reasoning_result": "reasoning_completed",
            "conclusion": f"Based on input {input_data}, the reasoning is complete",
            "confidence": 0.85,
            "steps": ["analyze_input", "apply_logic", "generate_conclusion"]
        }

class CommunicationModule:
    """Communication capability"""
    
    async def send_message(self, recipient: str, content: Dict[str, Any]) -> bool:
        """Send a message to another agent"""
        # This would integrate with the framework's messaging system
        return True
    
    async def broadcast(self, content: Dict[str, Any]) -> bool:
        """Broadcast a message to all agents"""
        return True

class ToolUseModule:
    """Tool usage capability"""
    
    def __init__(self):
        self.available_tools: Dict[str, Callable] = {}
    
    def register_tool(self, tool_name: str, tool_function: Callable):
        """Register a tool that can be used"""
        self.available_tools[tool_name] = tool_function
    
    async def invoke(self, tool_request: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool"""
        tool_name = tool_request.get("tool_name")
        parameters = tool_request.get("parameters", {})
        
        if tool_name not in self.available_tools:
            return {"error": f"Tool {tool_name} not available"}
        
        try:
            result = await self.available_tools[tool_name](**parameters)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

class LearningModule:
    """Learning capability"""
    
    async def learn(self, experience: Dict[str, Any]) -> Dict[str, Any]:
        """Learn from experience"""
        # Simulate learning process
        await asyncio.sleep(0.3)
        
        return {
            "learning_completed": True,
            "improvements": ["pattern_recognition", "efficiency_gain"],
            "knowledge_gained": f"Learned from {experience}"
        }

class PlanningModule:
    """Planning capability"""
    
    async def plan(self, goal: Dict[str, Any]) -> Dict[str, Any]:
        """Create a plan to achieve a goal"""
        # Simulate planning process
        await asyncio.sleep(0.4)
        
        return {
            "plan_created": True,
            "steps": [
                {"step": 1, "action": "analyze_goal", "priority": 1},
                {"step": 2, "action": "gather_resources", "priority": 2},
                {"step": 3, "action": "execute_plan", "priority": 3}
            ],
            "estimated_duration": "2 hours",
            "success_probability": 0.85
        }

# Global agent framework instance
_framework = AgentFramework({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "create_agent", "assign_task", "get_status", "broadcast", "shutdown"
            - agent_config: Agent configuration data
            - task_data: Task data
            - message_data: Message data
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_status")
    
    try:
        if action == "create_agent":
            agent_config_data = payload.get("agent_config", {})
            
            config = AgentConfig(
                agent_id=agent_config_data.get("agent_id", str(uuid.uuid4())),
                name=agent_config_data.get("name", "Agent"),
                description=agent_config_data.get("description", ""),
                capabilities=[AgentCapability(c) for c in agent_config_data.get("capabilities", [])],
                memory_size=agent_config_data.get("memory_size", 1000),
                max_concurrent_tasks=agent_config_data.get("max_concurrent_tasks", 5),
                timeout=agent_config_data.get("timeout", 300),
                retry_attempts=agent_config_data.get("retry_attempts", 3)
            )
            
            agent_id = _framework.create_agent(config)
            
            return {
                "result": {
                    "agent_id": agent_id,
                    "message": f"Created agent: {agent_id}"
                },
                "metadata": {
                    "action": "create_agent",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "assign_task":
            task_data = payload.get("task_data", {})
            
            task = AgentTask(
                task_id=task_data.get("task_id", str(uuid.uuid4())),
                task_type=task_data.get("task_type", "general"),
                input_data=task_data.get("input_data", {}),
                priority=task_data.get("priority", 5),
                created_at=time.time(),
                assigned_at=None,
                completed_at=None,
                status="pending",
                result=None,
                error=None
            )
            
            agent_id = task_data.get("agent_id", "")
            success = _framework.assign_task(agent_id, task)
            
            return {
                "result": {
                    "task_id": task.task_id,
                    "agent_id": agent_id,
                    "success": success,
                    "message": f"Assigned task to agent: {agent_id}" if success else f"Failed to assign task to agent: {agent_id}"
                },
                "metadata": {
                    "action": "assign_task",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_status":
            agent_id = payload.get("agent_id")
            if agent_id:
                status = _framework.get_agent_status(agent_id)
                return {
                    "result": status,
                    "metadata": {
                        "action": "get_status",
                        "timestamp": datetime.now().isoformat(),
                        "agent_id": agent_id
                    }
                }
            else:
                # Get all agent statuses
                statuses = {}
                for agent_id in _framework.agents:
                    statuses[agent_id] = _framework.get_agent_status(agent_id)
                
                return {
                    "result": statuses,
                    "metadata": {
                        "action": "get_status",
                        "timestamp": datetime.now().isoformat(),
                        "all_agents": True
                    }
                }
        
        elif action == "broadcast":
            message_data = payload.get("message_data", {})
            
            message = AgentMessage(
                message_id=message_data.get("message_id", str(uuid.uuid4())),
                sender=message_data.get("sender", "system"),
                receiver=message_data.get("receiver", "all"),
                content=message_data.get("content", {}),
                message_type=message_data.get("message_type", "notification"),
                timestamp=time.time()
            )
            
            _framework.broadcast_message(message)
            
            return {
                "result": {
                    "message_id": message.message_id,
                    "message": "Message broadcasted"
                },
                "metadata": {
                    "action": "broadcast",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "shutdown":
            agent_id = payload.get("agent_id", "")
            success = _framework.shutdown_agent(agent_id)
            
            return {
                "result": {
                    "agent_id": agent_id,
                    "success": success,
                    "message": f"Shutdown agent: {agent_id}" if success else f"Failed to shutdown agent: {agent_id}"
                },
                "metadata": {
                    "action": "shutdown",
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
        logger.error(f"Error in agent_framework: {e}")
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
    """Example of how to use the agent framework skill"""
    
    # Create an agent
    agent_id = await invoke({
        "action": "create_agent",
        "agent_config": {
            "name": "ReasoningAgent",
            "description": "Agent specialized in reasoning tasks",
            "capabilities": ["reasoning", "memory", "communication"],
            "memory_size": 500
        }
    })
    
    print(f"Created agent: {agent_id['result']['agent_id']}")
    
    # Assign a task
    task_result = await invoke({
        "action": "assign_task",
        "task_data": {
            "agent_id": agent_id['result']['agent_id'],
            "task_type": "reasoning",
            "input_data": {"problem": "How to solve complex problems systematically?"},
            "priority": 8
        }
    })
    
    print(f"Task assigned: {task_result['result']['success']}")
    
    # Get agent status
    status = await invoke({
        "action": "get_status",
        "agent_id": agent_id['result']['agent_id']
    })
    
    print(f"Agent status: {status['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
