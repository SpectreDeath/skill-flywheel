#!/usr/bin/env python3
"""
Skill: tool-integration-system
Domain: ai_agent_development
Description: System for integrating and managing external tools for AI agents
"""

import asyncio
import logging
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

class ToolStatus(Enum):
    """Tool status states"""
    REGISTERED = "registered"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    DEPRECATED = "deprecated"

class ToolCategory(Enum):
    """Tool categories"""
    API = "api"              # External API calls
    FILE = "file"            # File system operations
    COMPUTATION = "computation"  # Mathematical computations
    SEARCH = "search"        # Search and retrieval
    COMMUNICATION = "communication"  # Communication tools
    DATA_PROCESSING = "data_processing"  # Data manipulation
    MACHINE_LEARNING = "machine_learning"  # ML/AI operations

@dataclass
class ToolSignature:
    """Tool signature and metadata"""
    name: str
    description: str
    category: ToolCategory
    input_schema: Dict[str, Any]  # JSON schema for input
    output_schema: Dict[str, Any]  # JSON schema for output
    required_params: List[str]
    optional_params: List[str]
    version: str
    author: str
    dependencies: List[str]

@dataclass
class ToolExecution:
    """Tool execution record"""
    execution_id: str
    tool_name: str
    input_params: Dict[str, Any]
    output_result: Optional[Dict[str, Any]]
    execution_time: float
    status: str  # success, failed, timeout
    error_message: Optional[str]
    timestamp: float

class ToolIntegrationSystem:
    """System for integrating and managing external tools for AI agents"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the tool integration system
        
        Args:
            config: Configuration dictionary
        """
        self.tools: Dict[str, Callable] = {}
        self.tool_signatures: Dict[str, ToolSignature] = {}
        self.execution_history: List[ToolExecution] = []
        self.active_tools: List[str] = []
        self.tool_dependencies: Dict[str, List[str]] = {}
        self.logger = logging.getLogger(__name__)
        
    def register_tool(self, 
                     tool_function: Callable,
                     signature: ToolSignature) -> bool:
        """
        Register a tool with the system
        
        Args:
            tool_function: The actual tool function
            signature: Tool signature and metadata
            
        Returns:
            True if successfully registered, False otherwise
        """
        try:
            # Validate signature
            if not self._validate_signature(signature):
                self.logger.error(f"Invalid signature for tool: {signature.name}")
                return False
            
            # Check dependencies
            if not self._check_dependencies(signature.dependencies):
                self.logger.warning(f"Missing dependencies for tool: {signature.name}")
                return False
            
            # Register tool
            self.tools[signature.name] = tool_function
            self.tool_signatures[signature.name] = signature
            self.active_tools.append(signature.name)
            
            self.logger.info(f"Registered tool: {signature.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register tool {signature.name}: {e}")
            return False
    
    def invoke_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a registered tool
        
        Args:
            tool_name: Name of the tool to execute
            params: Parameters for the tool
            
        Returns:
            Execution result
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool {tool_name} not found",
                "result": None
            }
        
        if tool_name not in self.active_tools:
            return {
                "success": False,
                "error": f"Tool {tool_name} is not active",
                "result": None
            }
        
        # Validate parameters
        signature = self.tool_signatures[tool_name]
        validation_result = self._validate_params(params, signature)
        if not validation_result["valid"]:
            return {
                "success": False,
                "error": f"Invalid parameters: {validation_result['errors']}",
                "result": None
            }
        
        # Execute tool
        execution_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            # Execute the tool function
            result = self.tools[tool_name](**params)
            
            execution_time = time.time() - start_time
            
            # Record execution
            execution = ToolExecution(
                execution_id=execution_id,
                tool_name=tool_name,
                input_params=params,
                output_result=result,
                execution_time=execution_time,
                status="success",
                error_message=None,
                timestamp=time.time()
            )
            self.execution_history.append(execution)
            
            return {
                "success": True,
                "result": result,
                "execution_id": execution_id,
                "execution_time": execution_time
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            execution = ToolExecution(
                execution_id=execution_id,
                tool_name=tool_name,
                input_params=params,
                output_result=None,
                execution_time=execution_time,
                status="failed",
                error_message=str(e),
                timestamp=time.time()
            )
            self.execution_history.append(execution)
            
            return {
                "success": False,
                "error": str(e),
                "execution_id": execution_id,
                "execution_time": execution_time
            }
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool"""
        if tool_name not in self.tool_signatures:
            return None
        
        signature = self.tool_signatures[tool_name]
        return {
            "name": signature.name,
            "description": signature.description,
            "category": signature.category.value,
            "input_schema": signature.input_schema,
            "output_schema": signature.output_schema,
            "required_params": signature.required_params,
            "optional_params": signature.optional_params,
            "version": signature.version,
            "author": signature.author,
            "dependencies": signature.dependencies,
            "status": "active" if tool_name in self.active_tools else "inactive"
        }
    
    def list_tools(self, category: Optional[ToolCategory] = None) -> List[Dict[str, Any]]:
        """List all registered tools, optionally filtered by category"""
        tools_info = []
        
        for tool_name in self.tools:
            info = self.get_tool_info(tool_name)
            if info and (category is None or info["category"] == category.value):
                tools_info.append(info)
        
        return sorted(tools_info, key=lambda x: x["name"])
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        total_executions = len(self.execution_history)
        successful_executions = len([e for e in self.execution_history if e.status == "success"])
        failed_executions = len([e for e in self.execution_history if e.status == "failed"])
        
        # Calculate average execution time
        if self.execution_history:
            avg_execution_time = sum(e.execution_time for e in self.execution_history) / len(self.execution_history)
        else:
            avg_execution_time = 0.0
        
        # Tool usage statistics
        tool_usage = {}
        for execution in self.execution_history:
            tool_name = execution.tool_name
            if tool_name not in tool_usage:
                tool_usage[tool_name] = 0
            tool_usage[tool_name] += 1
        
        return {
            "total_tools": len(self.tools),
            "active_tools": len(self.active_tools),
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "success_rate": successful_executions / total_executions if total_executions > 0 else 0.0,
            "average_execution_time": avg_execution_time,
            "tool_usage": tool_usage,
            "recent_executions": [
                {
                    "execution_id": e.execution_id,
                    "tool_name": e.tool_name,
                    "status": e.status,
                    "execution_time": e.execution_time,
                    "timestamp": datetime.fromtimestamp(e.timestamp).isoformat()
                }
                for e in self.execution_history[-10:]  # Last 10 executions
            ]
        }
    
    def deactivate_tool(self, tool_name: str) -> bool:
        """Deactivate a tool"""
        if tool_name in self.active_tools:
            self.active_tools.remove(tool_name)
            self.logger.info(f"Deactivated tool: {tool_name}")
            return True
        return False
    
    def activate_tool(self, tool_name: str) -> bool:
        """Activate a tool"""
        if tool_name in self.tools and tool_name not in self.active_tools:
            self.active_tools.append(tool_name)
            self.logger.info(f"Activated tool: {tool_name}")
            return True
        return False
    
    def remove_tool(self, tool_name: str) -> bool:
        """Remove a tool from the system"""
        if tool_name in self.tools:
            del self.tools[tool_name]
            del self.tool_signatures[tool_name]
            if tool_name in self.active_tools:
                self.active_tools.remove(tool_name)
            self.logger.info(f"Removed tool: {tool_name}")
            return True
        return False
    
    def _validate_signature(self, signature: ToolSignature) -> bool:
        """Validate tool signature"""
        required_fields = ["name", "description", "category", "input_schema", "output_schema"]
        for field in required_fields:
            if not hasattr(signature, field) or getattr(signature, field) is None:
                return False
        return True
    
    def _check_dependencies(self, dependencies: List[str]) -> bool:
        """Check if all dependencies are available"""
        for dep in dependencies:
            if dep not in self.tools:
                return False
        return True
    
    def _validate_params(self, params: Dict[str, Any], signature: ToolSignature) -> Dict[str, Any]:
        """Validate input parameters against schema"""
        errors = []
        
        # Check required parameters
        for required_param in signature.required_params:
            if required_param not in params:
                errors.append(f"Missing required parameter: {required_param}")
        
        # Check parameter types (basic validation)
        for param_name, param_value in params.items():
            if param_name in signature.input_schema.get("properties", {}):
                expected_type = signature.input_schema["properties"][param_name].get("type")
                if expected_type == "string" and not isinstance(param_value, str):
                    errors.append(f"Parameter {param_name} should be string, got {type(param_value).__name__}")
                elif expected_type == "number" and not isinstance(param_value, (int, float)):
                    errors.append(f"Parameter {param_name} should be number, got {type(param_value).__name__}")
                elif expected_type == "boolean" and not isinstance(param_value, bool):
                    errors.append(f"Parameter {param_name} should be boolean, got {type(param_value).__name__}")
                elif expected_type == "array" and not isinstance(param_value, list):
                    errors.append(f"Parameter {param_name} should be array, got {type(param_value).__name__}")
                elif expected_type == "object" and not isinstance(param_value, dict):
                    errors.append(f"Parameter {param_name} should be object, got {type(param_value).__name__}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

# Pre-built tool functions

def create_file_tool():
    """Create a file system tool"""
    def write_file(path: str, content: str, mode: str = "w") -> Dict[str, Any]:
        """Write content to a file"""
        try:
            with open(path, mode) as f:
                f.write(content)
            return {"success": True, "message": f"Successfully wrote to {path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def read_file(path: str) -> Dict[str, Any]:
        """Read content from a file"""
        try:
            with open(path) as f:
                content = f.read()
            return {"success": True, "content": content}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    return {"write_file": write_file, "read_file": read_file}

def create_math_tool():
    """Create mathematical computation tools"""
    import math
    
    def calculate(operation: str, a: float, b: float = 0) -> Dict[str, Any]:
        """Perform mathematical calculations"""
        try:
            if operation == "add":
                result = a + b
            elif operation == "subtract":
                result = a - b
            elif operation == "multiply":
                result = a * b
            elif operation == "divide":
                if b == 0:
                    return {"success": False, "error": "Division by zero"}
                result = a / b
            elif operation == "sqrt":
                result = math.sqrt(a)
            elif operation == "power":
                result = math.pow(a, b)
            else:
                return {"success": False, "error": f"Unknown operation: {operation}"}
            
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    return {"calculate": calculate}

def create_search_tool():
    """Create search tools"""
    def search_web(query: str, max_results: int = 10) -> Dict[str, Any]:
        """Simulate web search"""
        # This would integrate with actual search APIs in a real implementation
        return {
            "success": True,
            "query": query,
            "results": [
                {"title": f"Result {i+1}", "url": f"https://example.com/result{i+1}", "snippet": f"Snippet for result {i+1}"}
                for i in range(max_results)
            ],
            "total_results": 1000
        }
    
    def search_local(query: str, path: str = ".") -> Dict[str, Any]:
        """Search local files"""
        import glob
        
        try:
            files = glob.glob(f"{path}/**/*", recursive=True)
            matching_files = [f for f in files if query.lower() in f.lower()]
            
            return {
                "success": True,
                "query": query,
                "path": path,
                "matching_files": matching_files[:20],  # Limit results
                "total_matches": len(matching_files)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    return {"search_web": search_web, "search_local": search_local}

# Global tool integration system instance
_tool_system = ToolIntegrationSystem({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "register_tool", "execute_tool", "list_tools", "get_info", 
                     "get_stats", "deactivate", "activate", "remove"
            - tool_data: Tool data for registration
            - execution_data: Execution parameters
            - tool_name: Tool identifier
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "list_tools")
    
    try:
        if action == "register_tool":
            tool_data = payload.get("tool_data", {})
            
            # Create tool signature
            signature = ToolSignature(
                name=tool_data.get("name", ""),
                description=tool_data.get("description", ""),
                category=ToolCategory(tool_data.get("category", "computation")),
                input_schema=tool_data.get("input_schema", {}),
                output_schema=tool_data.get("output_schema", {}),
                required_params=tool_data.get("required_params", []),
                optional_params=tool_data.get("optional_params", []),
                version=tool_data.get("version", "1.0.0"),
                author=tool_data.get("author", "system"),
                dependencies=tool_data.get("dependencies", [])
            )
            
            # Get tool function (this is simplified - in practice you'd have the actual function)
            # For now, we'll use pre-built tools
            tool_functions = {}
            if signature.category == ToolCategory.FILE:
                tool_functions = create_file_tool()
            elif signature.category == ToolCategory.COMPUTATION:
                tool_functions = create_math_tool()
            elif signature.category == ToolCategory.SEARCH:
                tool_functions = create_search_tool()
            
            success = False
            for tool_name, tool_func in tool_functions.items():
                if tool_name == signature.name:
                    success = _tool_system.register_tool(tool_func, signature)
                    break
            
            return {
                "result": {
                    "tool_name": signature.name,
                    "success": success,
                    "message": f"Registered tool: {signature.name}" if success else f"Failed to register tool: {signature.name}"
                },
                "metadata": {
                    "action": "register_tool",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "execute_tool":
            execution_data = payload.get("execution_data", {})
            tool_name = execution_data.get("tool_name", "")
            params = execution_data.get("params", {})
            
            result = _tool_system.execute_tool(tool_name, params)
            
            return {
                "result": result,
                "metadata": {
                    "action": "execute_tool",
                    "timestamp": datetime.now().isoformat(),
                    "tool_name": tool_name
                }
            }
        
        elif action == "list_tools":
            category = payload.get("category")
            if category:
                category = ToolCategory(category)
            
            tools = _tool_system.list_tools(category)
            
            return {
                "result": tools,
                "metadata": {
                    "action": "list_tools",
                    "timestamp": datetime.now().isoformat(),
                    "category": category.value if category else None
                }
            }
        
        elif action == "get_info":
            tool_name = payload.get("tool_name", "")
            info = _tool_system.get_tool_info(tool_name)
            
            return {
                "result": info,
                "metadata": {
                    "action": "get_info",
                    "timestamp": datetime.now().isoformat(),
                    "tool_name": tool_name
                }
            }
        
        elif action == "get_stats":
            stats = _tool_system.get_execution_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "deactivate":
            tool_name = payload.get("tool_name", "")
            success = _tool_system.deactivate_tool(tool_name)
            
            return {
                "result": {
                    "tool_name": tool_name,
                    "success": success,
                    "message": f"Deactivated tool: {tool_name}" if success else f"Failed to deactivate tool: {tool_name}"
                },
                "metadata": {
                    "action": "deactivate",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "activate":
            tool_name = payload.get("tool_name", "")
            success = _tool_system.activate_tool(tool_name)
            
            return {
                "result": {
                    "tool_name": tool_name,
                    "success": success,
                    "message": f"Activated tool: {tool_name}" if success else f"Failed to activate tool: {tool_name}"
                },
                "metadata": {
                    "action": "activate",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "remove":
            tool_name = payload.get("tool_name", "")
            success = _tool_system.remove_tool(tool_name)
            
            return {
                "result": {
                    "tool_name": tool_name,
                    "success": success,
                    "message": f"Removed tool: {tool_name}" if success else f"Failed to remove tool: {tool_name}"
                },
                "metadata": {
                    "action": "remove",
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
        logger.error(f"Error in tool_integration_system: {e}")
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
    """Example of how to use the tool integration system skill"""
    
    # Register some tools
    await invoke({
        "action": "register_tool",
        "tool_data": {
            "name": "calculate",
            "description": "Perform mathematical calculations",
            "category": "computation",
            "input_schema": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string"},
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["operation", "a"]
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "result": {"type": "number"}
                }
            },
            "required_params": ["operation", "a"],
            "optional_params": ["b"],
            "version": "1.0.0",
            "author": "system"
        }
    })
    
    # Execute a tool
    result = await invoke({
        "action": "execute_tool",
        "execution_data": {
            "tool_name": "calculate",
            "params": {
                "operation": "add",
                "a": 10,
                "b": 5
            }
        }
    })
    
    print(f"Tool execution result: {result['result']}")
    
    # Get tool statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Tool statistics: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
