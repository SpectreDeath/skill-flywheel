#!/usr/bin/env python3
"""
Enhanced MCP Server with Advanced Features

This server provides:
- Multi-agent orchestration with LangChain and CrewAI
- Advanced performance monitoring and telemetry
- Skill lifecycle management
- Production deployment features
- Enhanced configuration system
"""

import asyncio
import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import yaml
import psutil
import GPUtil
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_mcp_server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuration
class ServerConfig:
    """Enhanced server configuration with validation and defaults"""
    
    def __init__(self, config_path: str = "mcp_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file with defaults"""
        default_config = {
            "server": {
                "host": "0.0.0.0",
                "port": 8000,
                "debug": False,
                "cors_origins": ["*"],
                "max_concurrent_requests": 100,
                "request_timeout": 300
            },
            "monitoring": {
                "enabled": True,
                "metrics_interval": 60,
                "log_level": "INFO",
                "telemetry_endpoint": None,
                "performance_thresholds": {
                    "cpu_warning": 80.0,
                    "memory_warning": 80.0,
                    "response_time_warning": 5.0
                }
            },
            "agents": {
                "max_agents": 50,
                "agent_timeout": 300,
                "retry_attempts": 3,
                "parallel_execution": True
            },
            "skills": {
                "auto_discovery": True,
                "validation_enabled": True,
                "cache_ttl": 3600,
                "max_skill_size": 1024 * 1024  # 1MB
            },
            "security": {
                "api_key_required": False,
                "allowed_ips": [],
                "rate_limit": 1000  # requests per minute
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    user_config = yaml.safe_load(f)
                    self._merge_config(default_config, user_config)
            except Exception as e:
                logger.warning(f"Failed to load config from {self.config_path}: {e}")
        
        return default_config
    
    def _merge_config(self, default: Dict, user: Dict) -> None:
        """Recursively merge user config with defaults"""
        for key, value in user.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._merge_config(default[key], value)
            else:
                default[key] = value

# Telemetry and Monitoring
@dataclass
class PerformanceMetrics:
    """Performance metrics for monitoring"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    gpu_usage: Optional[float]
    active_connections: int
    request_count: int
    error_count: int
    avg_response_time: float

@dataclass
class AgentMetrics:
    """Agent-specific metrics"""
    agent_id: str
    skill_name: str
    execution_time: float
    success_rate: float
    error_count: int
    last_execution: datetime

class TelemetryManager:
    """Advanced telemetry and monitoring system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.metrics_history: List[PerformanceMetrics] = []
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.start_time = datetime.now()
        
    def collect_system_metrics(self) -> PerformanceMetrics:
        """Collect comprehensive system metrics"""
        try:
            # CPU and Memory
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # GPU (if available)
            gpu_usage = None
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu_usage = gpus[0].load * 100
            except:
                pass
            
            # Network and Process stats
            connections = len(psutil.net_connections())
            
            metrics = PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                disk_usage=disk.percent,
                gpu_usage=gpu_usage,
                active_connections=connections,
                request_count=0,  # Will be updated by request tracking
                error_count=0,    # Will be updated by error tracking
                avg_response_time=0.0  # Will be updated by response time tracking
            )
            
            self.metrics_history.append(metrics)
            
            # Keep only last 1000 metrics to prevent memory bloat
            if len(self.metrics_history) > 1000:
                self.metrics_history.pop(0)
                
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            return None
    
    def track_agent_execution(self, agent_id: str, skill_name: str, 
                            execution_time: float, success: bool):
        """Track agent execution metrics"""
        if agent_id not in self.agent_metrics:
            self.agent_metrics[agent_id] = AgentMetrics(
                agent_id=agent_id,
                skill_name=skill_name,
                execution_time=0.0,
                success_rate=0.0,
                error_count=0,
                last_execution=datetime.now()
            )
        
        metrics = self.agent_metrics[agent_id]
        metrics.last_execution = datetime.now()
        metrics.execution_time = execution_time
        
        if success:
            # Update success rate (simple moving average)
            total_executions = metrics.success_rate * 100 + 1
            metrics.success_rate = (metrics.success_rate * 99 + 1) / 100
        else:
            metrics.error_count += 1
            metrics.success_rate = (metrics.success_rate * 99) / 100
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall system health status"""
        if not self.metrics_history:
            return {"status": "unknown", "reason": "No metrics available"}
        
        latest = self.metrics_history[-1]
        thresholds = self.config["monitoring"]["performance_thresholds"]
        
        issues = []
        
        if latest.cpu_usage > thresholds["cpu_warning"]:
            issues.append(f"High CPU usage: {latest.cpu_usage:.1f}%")
        
        if latest.memory_usage > thresholds["memory_warning"]:
            issues.append(f"High memory usage: {latest.memory_usage:.1f}%")
        
        if latest.disk_usage > 90.0:
            issues.append(f"High disk usage: {latest.disk_usage:.1f}%")
        
        if latest.gpu_usage and latest.gpu_usage > thresholds["cpu_warning"]:
            issues.append(f"High GPU usage: {latest.gpu_usage:.1f}%")
        
        if latest.avg_response_time > thresholds["response_time_warning"]:
            issues.append(f"Slow response time: {latest.avg_response_time:.2f}s")
        
        if issues:
            return {
                "status": "warning",
                "issues": issues,
                "metrics": {
                    "cpu": latest.cpu_usage,
                    "memory": latest.memory_usage,
                    "disk": latest.disk_usage,
                    "gpu": latest.gpu_usage,
                    "response_time": latest.avg_response_time
                }
            }
        
        return {
            "status": "healthy",
            "uptime": str(datetime.now() - self.start_time),
            "metrics": {
                "cpu": latest.cpu_usage,
                "memory": latest.memory_usage,
                "disk": latest.disk_usage,
                "gpu": latest.gpu_usage,
                "response_time": latest.avg_response_time
            }
        }

# Skill Management
class SkillStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    DEPRECATED = "deprecated"

@dataclass
class SkillMetadata:
    """Metadata for skills"""
    name: str
    version: str
    description: str
    author: str
    dependencies: List[str]
    created_at: datetime
    last_modified: datetime
    status: SkillStatus
    execution_count: int
    avg_execution_time: float

class SkillManager:
    """Advanced skill lifecycle management"""
    
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(exist_ok=True)
        self.skills: Dict[str, SkillMetadata] = {}
        self.skill_cache: Dict[str, Any] = {}
        
    def discover_skills(self) -> List[str]:
        """Auto-discover skills in the skills directory"""
        discovered = []
        
        for skill_file in self.skills_dir.glob("*.py"):
            try:
                skill_name = skill_file.stem
                metadata = self._extract_metadata(skill_file)
                self.skills[skill_name] = metadata
                discovered.append(skill_name)
                logger.info(f"Discovered skill: {skill_name}")
            except Exception as e:
                logger.error(f"Failed to load skill {skill_file}: {e}")
        
        return discovered
    
    def _extract_metadata(self, skill_file: Path) -> SkillMetadata:
        """Extract metadata from skill file"""
        # This is a simplified version - in practice, you'd parse the file
        # to extract actual metadata from docstrings or decorators
        return SkillMetadata(
            name=skill_file.stem,
            version="1.0.0",
            description="Auto-discovered skill",
            author="Auto-discovered",
            dependencies=[],
            created_at=datetime.now(),
            last_modified=datetime.fromtimestamp(skill_file.stat().st_mtime),
            status=SkillStatus.ACTIVE,
            execution_count=0,
            avg_execution_time=0.0
        )
    
    def validate_skill(self, skill_name: str) -> bool:
        """Validate a skill"""
        if skill_name not in self.skills:
            return False
        
        # Basic validation - check if file exists and is readable
        skill_file = self.skills_dir / f"{skill_name}.py"
        return skill_file.exists() and skill_file.is_file()
    
    def execute_skill(self, skill_name: str, *args, **kwargs) -> Any:
        """Execute a skill with monitoring"""
        if skill_name not in self.skills:
            raise ValueError(f"Skill {skill_name} not found")
        
        if not self.validate_skill(skill_name):
            raise ValueError(f"Skill {skill_name} is invalid")
        
        skill_file = self.skills_dir / f"{skill_name}.py"
        metadata = self.skills[skill_name]
        
        start_time = time.time()
        
        try:
            # Load and execute skill
            if skill_name not in self.skill_cache:
                with open(skill_file, 'r') as f:
                    code = compile(f.read(), skill_file, 'exec')
                    namespace = {}
                    exec(code, namespace)
                    self.skill_cache[skill_name] = namespace
            
            # Execute the skill function (assuming it's named after the skill)
            skill_func = self.skill_cache[skill_name].get(skill_name)
            if not skill_func:
                raise ValueError(f"Skill function {skill_name} not found in {skill_file}")
            
            result = skill_func(*args, **kwargs)
            
            # Update metrics
            execution_time = time.time() - start_time
            metadata.execution_count += 1
            metadata.avg_execution_time = (
                (metadata.avg_execution_time * (metadata.execution_count - 1) + execution_time) 
                / metadata.execution_count
            )
            
            logger.info(f"Skill {skill_name} executed successfully in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Skill {skill_name} execution failed: {e}")
            metadata.status = SkillStatus.ERROR
            raise

# Multi-Agent Orchestration
class AgentOrchestrator:
    """Advanced multi-agent orchestration with LangChain and CrewAI"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.agents: Dict[str, Agent] = {}
        self.crews: Dict[str, Crew] = {}
        self.telemetry = TelemetryManager(config)
        
    def create_agent(self, agent_id: str, role: str, goal: str, 
                    backstory: str, tools: List[BaseTool] = None,
                    llm_config: Dict[str, Any] = None) -> Agent:
        """Create a new agent"""
        if agent_id in self.agents:
            raise ValueError(f"Agent {agent_id} already exists")
        
        # Default LLM configuration
        if llm_config is None:
            llm_config = {
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 2000
            }
        
        # Create LLM instance
        llm = ChatOpenAI(**llm_config)
        
        # Create agent
        agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            llm=llm,
            tools=tools or [],
            verbose=True,
            max_iter=self.config["agents"]["retry_attempts"]
        )
        
        self.agents[agent_id] = agent
        logger.info(f"Created agent: {agent_id}")
        return agent
    
    def create_crew(self, crew_id: str, agents: List[str], 
                   process: str = "sequential") -> Crew:
        """Create a new crew of agents"""
        if crew_id in self.crews:
            raise ValueError(f"Crew {crew_id} already exists")
        
        # Get agent instances
        agent_instances = []
        for agent_id in agents:
            if agent_id not in self.agents:
                raise ValueError(f"Agent {agent_id} not found")
            agent_instances.append(self.agents[agent_id])
        
        # Create crew
        process_type = Process.sequential if process == "sequential" else Process.hierarchical
        crew = Crew(
            agents=agent_instances,
            process=process_type,
            verbose=True,
            max_rpm=self.config["agents"]["rate_limit"]
        )
        
        self.crews[crew_id] = crew
        logger.info(f"Created crew: {crew_id} with {len(agents)} agents")
        return crew
    
    async def execute_task(self, agent_id: str, task_description: str, 
                          context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a task with a specific agent"""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
        
        agent = self.agents[agent_id]
        start_time = time.time()
        
        try:
            # Create task
            task = Task(
                description=task_description,
                agent=agent,
                context=context or {},
                expected_output="Detailed response with analysis and recommendations"
            )
            
            # Execute task
            result = await asyncio.to_thread(task.execute)
            
            execution_time = time.time() - start_time
            self.telemetry.track_agent_execution(agent_id, task_description, execution_time, True)
            
            return {
                "success": True,
                "agent_id": agent_id,
                "result": result,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.telemetry.track_agent_execution(agent_id, task_description, execution_time, False)
            
            return {
                "success": False,
                "agent_id": agent_id,
                "error": str(e),
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
    
    async def execute_crew_task(self, crew_id: str, task_description: str,
                               context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a task with a crew of agents"""
        if crew_id not in self.crews:
            raise ValueError(f"Crew {crew_id} not found")
        
        crew = self.crews[crew_id]
        start_time = time.time()
        
        try:
            # Create task
            task = Task(
                description=task_description,
                expected_output="Comprehensive analysis and solution",
                context=context or {}
            )
            
            # Execute with crew
            result = await asyncio.to_thread(crew.kickoff, inputs={"task": task_description})
            
            execution_time = time.time() - start_time
            
            # Track metrics for all agents in the crew
            for agent in crew.agents:
                self.telemetry.track_agent_execution(agent.role, task_description, execution_time, True)
            
            return {
                "success": True,
                "crew_id": crew_id,
                "result": result,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # Track metrics for all agents in the crew
            for agent in crew.agents:
                self.telemetry.track_agent_execution(agent.role, task_description, execution_time, False)
            
            return {
                "success": False,
                "crew_id": crew_id,
                "error": str(e),
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }

# FastAPI Server
class EnhancedMCPServer:
    """Enhanced MCP Server with advanced features"""
    
    def __init__(self):
        self.config = ServerConfig()
        self.app = FastAPI(
            title="Enhanced MCP Server",
            description="Multi-Agent Orchestration Server with Advanced Features",
            version="2.0.0"
        )
        
        # Setup CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.config["server"]["cors_origins"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Initialize components
        self.telemetry = TelemetryManager(self.config.config)
        self.skill_manager = SkillManager()
        self.orchestrator = AgentOrchestrator(self.config.config)
        
        # Setup routes
        self._setup_routes()
        
        # Background tasks
        self.background_tasks = []
        
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/")
        async def root():
            return {"message": "Enhanced MCP Server is running", "version": "2.0.0"}
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return self.telemetry.get_health_status()
        
        @self.app.get("/metrics")
        async def get_metrics():
            """Get performance metrics"""
            return {
                "system_metrics": [asdict(m) for m in self.telemetry.metrics_history[-10:]],
                "agent_metrics": {k: asdict(v) for k, v in self.orchestrator.telemetry.agent_metrics.items()},
                "skills": {k: asdict(v) for k, v in self.skill_manager.skills.items()}
            }
        
        @self.app.post("/skills/discover")
        async def discover_skills():
            """Discover available skills"""
            skills = self.skill_manager.discover_skills()
            return {"discovered_skills": skills, "total": len(skills)}
        
        @self.app.post("/skills/execute")
        async def execute_skill(request: Dict[str, Any]):
            """Execute a skill"""
            skill_name = request.get("skill_name")
            args = request.get("args", [])
            kwargs = request.get("kwargs", {})
            
            if not skill_name:
                raise HTTPException(status_code=400, detail="skill_name is required")
            
            try:
                result = self.skill_manager.execute_skill(skill_name, *args, **kwargs)
                return {"success": True, "result": result}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/agents/create")
        async def create_agent(request: Dict[str, Any]):
            """Create a new agent"""
            agent_id = request.get("agent_id")
            role = request.get("role")
            goal = request.get("goal")
            backstory = request.get("backstory")
            tools = request.get("tools", [])
            llm_config = request.get("llm_config")
            
            if not all([agent_id, role, goal, backstory]):
                raise HTTPException(status_code=400, detail="agent_id, role, goal, and backstory are required")
            
            try:
                agent = self.orchestrator.create_agent(agent_id, role, goal, backstory, tools, llm_config)
                return {"success": True, "agent_id": agent_id}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/agents/execute")
        async def execute_agent_task(request: Dict[str, Any]):
            """Execute a task with an agent"""
            agent_id = request.get("agent_id")
            task_description = request.get("task_description")
            context = request.get("context", {})
            
            if not agent_id or not task_description:
                raise HTTPException(status_code=400, detail="agent_id and task_description are required")
            
            try:
                result = await self.orchestrator.execute_task(agent_id, task_description, context)
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/crews/create")
        async def create_crew(request: Dict[str, Any]):
            """Create a new crew"""
            crew_id = request.get("crew_id")
            agents = request.get("agents", [])
            process = request.get("process", "sequential")
            
            if not crew_id or not agents:
                raise HTTPException(status_code=400, detail="crew_id and agents are required")
            
            try:
                crew = self.orchestrator.create_crew(crew_id, agents, process)
                return {"success": True, "crew_id": crew_id, "agents": agents}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/crews/execute")
        async def execute_crew_task(request: Dict[str, Any]):
            """Execute a task with a crew"""
            crew_id = request.get("crew_id")
            task_description = request.get("task_description")
            context = request.get("context", {})
            
            if not crew_id or not task_description:
                raise HTTPException(status_code=400, detail="crew_id and task_description are required")
            
            try:
                result = await self.orchestrator.execute_crew_task(crew_id, task_description, context)
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.on_event("startup")
        async def startup_event():
            """Startup tasks"""
            # Start background monitoring
            self.background_tasks.append(
                asyncio.create_task(self._monitoring_loop())
            )
            
            # Discover skills on startup
            self.skill_manager.discover_skills()
            
            logger.info("Enhanced MCP Server started successfully")
        
        @self.app.on_event("shutdown")
        async def shutdown_event():
            """Shutdown tasks"""
            for task in self.background_tasks:
                task.cancel()
            
            logger.info("Enhanced MCP Server shutting down")
    
    async def _monitoring_loop(self):
        """Background monitoring loop"""
        while True:
            try:
                # Collect system metrics
                self.telemetry.collect_system_metrics()
                
                # Log health status periodically
                health = self.telemetry.get_health_status()
                if health["status"] != "healthy":
                    logger.warning(f"System health warning: {health}")
                
                await asyncio.sleep(self.config.config["monitoring"]["metrics_interval"])
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                await asyncio.sleep(10)
    
    def run(self):
        """Run the server"""
        config = self.config.config["server"]
        uvicorn.run(
            self.app,
            host=config["host"],
            port=config["port"],
            debug=config["debug"],
            log_level="info"
        )

# CLI Interface
def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced MCP Server")
    parser.add_argument("--config", default="mcp_config.yaml", help="Configuration file path")
    parser.add_argument("--host", default=None, help="Server host")
    parser.add_argument("--port", type=int, default=None, help="Server port")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Update config if CLI args provided
    if args.config:
        os.environ["MCP_CONFIG"] = args.config
    if args.host:
        os.environ["MCP_HOST"] = args.host
    if args.port:
        os.environ["MCP_PORT"] = str(args.port)
    if args.debug:
        os.environ["MCP_DEBUG"] = "true"
    
    # Start server
    server = EnhancedMCPServer()
    server.run()

if __name__ == "__main__":
    main()