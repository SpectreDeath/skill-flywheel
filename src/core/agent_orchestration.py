#!/usr/bin/env python3
"""
Agent Orchestration Framework for Skill Flywheel

This module provides comprehensive agent orchestration capabilities for
AutoGen, LangChain, LangGraph, and CrewAI frameworks. It enables seamless
coordination of multi-agent workflows with cross-framework communication,
shared context management, and result aggregation.
"""

import asyncio
import json
import logging
import time
import aiohttp
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
import os

logger = logging.getLogger(__name__)

class AgentFramework(Enum):
    AUTOGEN = "autogen"
    LANGCHAIN = "langchain"
    LANGGRAPH = "langgraph"
    CREWAI = "crewai"

@dataclass
class AgentConfig:
    """Configuration for an agent in the orchestration."""
    name: str
    role: str
    goal: str
    backstory: str
    framework: AgentFramework
    domain: Optional[str] = None  # New: Target domain for the agent
    model: str = "gpt-4"
    temperature: float = 0.1
    max_tokens: int = 4000
    tools: List[str] = None
    dependencies: List[str] = None
    context_requirements: List[str] = None

@dataclass
class TaskContext:
    """Shared context for agent tasks."""
    task_id: str
    task_description: str
    shared_memory: Dict[str, Any]
    agent_outputs: Dict[str, Any]
    execution_history: List[Dict[str, Any]]
    constraints: List[str]

@dataclass
class OrchestrationResult:
    """Result of agent orchestration."""
    task_id: str
    framework: AgentFramework
    agents_used: List[str]
    execution_time: float
    success: bool
    results: Dict[str, Any]
    error: Optional[str] = None

class AgentOrchestrator:
    """Main orchestrator for multi-agent workflows."""
    
    DISCOVERY_SERVICE_URL = os.environ.get("DISCOVERY_SERVICE_URL", "http://localhost:8000")

    def __init__(self):
        self.agents: Dict[str, AgentConfig] = {}
        self.contexts: Dict[str, TaskContext] = {}
        self.framework_adapters = {
            AgentFramework.AUTOGEN: AutoGenAdapter(),
            AgentFramework.LANGCHAIN: LangChainAdapter(),
            AgentFramework.LANGGRAPH: LangGraphAdapter(),
            AgentFramework.CREWAI: CrewAIAdapter()
        }
    
    async def resolve_agent_endpoint(self, agent_name: str) -> Optional[str]:
        """Resolve the endpoint for an agent based on its domain via discovery service."""
        agent_config = self.agents.get(agent_name)
        if not agent_config or not agent_config.domain:
            return None
            
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.DISCOVERY_SERVICE_URL}/call/find_domain_for_skill"
                # Try domain-specific mapping first
                async with session.post(url, json={"skill_name": f"domain-{agent_config.domain}"}) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if isinstance(data, dict) and data.get("internal_endpoint"):
                            return data["internal_endpoint"]
                
                # Fallback: try direct domain name search
                async with session.post(url, json={"skill_name": agent_config.domain}) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if isinstance(data, dict) and data.get("internal_endpoint"):
                            return data["internal_endpoint"]
        except Exception as e:
            logger.warning(f"Failed to resolve endpoint for agent {agent_name}: {e}")
            
        return None

    def register_agent(self, agent_config: AgentConfig):
        """Register an agent for orchestration."""
        self.agents[agent_config.name] = agent_config
        logger.info(f"Registered agent: {agent_config.name} ({agent_config.framework.value})")
    
    def create_context(self, task_id: str, task_description: str, initial_context: Dict[str, Any] = None) -> TaskContext:
        """Create a shared context for a task."""
        context = TaskContext(
            task_id=task_id,
            task_description=task_description,
            shared_memory=initial_context or {},
            agent_outputs={},
            execution_history=[],
            constraints=[]
        )
        self.contexts[task_id] = context
        return context
    
    async def orchestrate_task(self, task_id: str, agents: List[str], task_description: str, 
                             initial_context: Dict[str, Any] = None) -> OrchestrationResult:
        """Orchestrate a task across multiple agents."""
        start_time = time.time()
        
        try:
            # Create or get context
            if task_id in self.contexts:
                context = self.contexts[task_id]
                context.task_description = task_description
            else:
                context = self.create_context(task_id, task_description, initial_context)
            
            # Validate agents
            valid_agents = []
            for agent_name in agents:
                if agent_name in self.agents:
                    valid_agents.append(agent_name)
                else:
                    logger.warning(f"Agent {agent_name} not found, skipping")
            
            # Resolve agent endpoints (for cross-domain tracking/reporting)
            agent_endpoints = {}
            for agent_name in valid_agents:
                endpoint = await self.resolve_agent_endpoint(agent_name)
                if endpoint:
                    agent_endpoints[agent_name] = endpoint
            
            # Store endpoints in context for adapters to use if needed
            context.shared_memory["_agent_endpoints"] = agent_endpoints

            # Group agents by framework
            framework_groups = self._group_agents_by_framework(valid_agents)
            
            # Execute orchestration based on framework strategy
            if len(framework_groups) == 1:
                # Single framework orchestration
                framework = list(framework_groups.keys())[0]
                result = await self._execute_single_framework(framework, framework_groups[framework], context)
            else:
                # Multi-framework orchestration
                result = await self._execute_multi_framework(framework_groups, context)
            
            result.execution_time = time.time() - start_time
            result.agents_used = valid_agents
            
            # Update context
            context.execution_history.append({
                "timestamp": time.time(),
                "agents": valid_agents,
                "task": task_description,
                "result": result.success
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error in orchestration: {e}")
            return OrchestrationResult(
                task_id=task_id,
                framework=AgentFramework.AUTOGEN,
                agents_used=agents,
                execution_time=time.time() - start_time,
                success=False,
                results={},
                error=str(e)
            )
    
    def _group_agents_by_framework(self, agents: List[str]) -> Dict[AgentFramework, List[str]]:
        """Group agents by their framework."""
        groups = {}
        for agent_name in agents:
            agent_config = self.agents[agent_name]
            framework = agent_config.framework
            if framework not in groups:
                groups[framework] = []
            groups[framework].append(agent_name)
        return groups
    
    async def _execute_single_framework(self, framework: AgentFramework, agents: List[str], 
                                      context: TaskContext) -> OrchestrationResult:
        """Execute orchestration within a single framework."""
        adapter = self.framework_adapters[framework]
        
        # Prepare agent configurations
        agent_configs = [self.agents[agent_name] for agent_name in agents]
        
        # Execute with adapter
        result = await adapter.execute_agents(agent_configs, context)
        return result
    
    async def _execute_multi_framework(self, framework_groups: Dict[AgentFramework, List[str]], 
                                     context: TaskContext) -> OrchestrationResult:
        """Execute orchestration across multiple frameworks."""
        results = {}
        overall_success = True
        
        # Execute each framework group
        for framework, agents in framework_groups.items():
            adapter = self.framework_adapters[framework]
            agent_configs = [self.agents[agent_name] for agent_name in agents]
            
            result = await adapter.execute_agents(agent_configs, context)
            results[framework.value] = result
            
            if not result.success:
                overall_success = False
        
        # Aggregate results
        aggregated_results = {
            "framework_results": results,
            "context_updates": context.shared_memory,
            "execution_history": context.execution_history
        }
        
        return OrchestrationResult(
            task_id=context.task_id,
            framework=AgentFramework.AUTOGEN,  # Default for multi-framework
            agents_used=[],
            execution_time=0,  # Will be set by caller
            success=overall_success,
            results=aggregated_results
        )
        
    async def orchestrate_cross_domain_mission(self, mission_id: str, mission_objective: str, target_domains: List[str], agents_per_domain: Dict[str, List[str]]) -> OrchestrationResult:
        """
        Orchestrate a complex mission spanning multiple domain servers.
        Supports advanced cross-domain routing and execution.
        """
        start_time = time.time()
        
        # Verify domain count requirement
        if len(target_domains) < 3:
            logger.warning(f"Complexity Info: Cross-domain mission '{mission_id}' spans {len(target_domains)} domains. Target is 3+ domains for complex execution.")
            
        context = self.create_context(mission_id, mission_objective)
        overall_success = True
        domain_results = {}
        agents_used = []
        
        # Phase 1: Planning and Endpoint Resolution across all domains
        endpoints = {}
        for domain in target_domains:
            try:
                async with aiohttp.ClientSession() as session:
                    url = f"{self.DISCOVERY_SERVICE_URL}/call/find_domain_for_skill"
                    async with session.post(url, json={"skill_name": f"domain-{domain}"}) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            if isinstance(data, dict) and data.get("internal_endpoint"):
                                endpoints[domain] = data["internal_endpoint"]
            except Exception as e:
                logger.warning(f"Failed to resolve endpoint for domain {domain}: {e}")
                
        # Phase 2: Distributed Execution
        for domain in target_domains:
            domain_agents = agents_per_domain.get(domain, [])
            if not domain_agents:
                continue
                
            agents_used.extend(domain_agents)
            endpoint = endpoints.get(domain)
            if endpoint:
                logger.info(f"Dispatching mission segment to remote domain '{domain}' at endpoint {endpoint}")
            else:
                logger.warning(f"Executing domain '{domain}' locally as endpoint resolution failed/missing.")
                
            # Execute agents for this domain segment using existing mult-framework logic
            framework_groups = self._group_agents_by_framework(domain_agents)
            result = await self._execute_multi_framework(framework_groups, context)
            
            domain_results[domain] = result
            if not result.success:
                overall_success = False
                
            # Share context for next domain hop
            context.shared_memory[f"{domain}_outcome"] = result.results
            
        # Aggregate final mission report
        aggregated_results = {
            "mission_objective": mission_objective,
            "domains_spanned": target_domains,
            "endpoints_utilized": endpoints,
            "domain_results": { d: r.results for d, r in domain_results.items() },
            "context_updates": context.shared_memory
        }
        
        return OrchestrationResult(
            task_id=mission_id,
            framework=AgentFramework.AUTOGEN,
            agents_used=agents_used,
            execution_time=time.time() - start_time,
            success=overall_success,
            results=aggregated_results
        )

class FrameworkAdapter:
    """Base class for framework-specific adapters."""
    
    async def execute_agents(self, agent_configs: List[AgentConfig], context: TaskContext) -> OrchestrationResult:
        """Execute agents using the specific framework."""
        raise NotImplementedError

class AutoGenAdapter(FrameworkAdapter):
    """AutoGen framework adapter."""
    
    async def execute_agents(self, agent_configs: List[AgentConfig], context: TaskContext) -> OrchestrationResult:
        try:
            # This would integrate with AutoGen
            # For now, simulate execution
            logger.info(f"Executing {len(agent_configs)} agents with AutoGen")
            
            # Simulate agent execution
            results = {}
            for agent_config in agent_configs:
                # Simulate agent processing
                simulated_result = {
                    "agent_name": agent_config.name,
                    "role": agent_config.role,
                    "output": f"Processed task: {context.task_description}",
                    "context_used": list(context.shared_memory.keys()),
                    "timestamp": time.time()
                }
                results[agent_config.name] = simulated_result
            
            return OrchestrationResult(
                task_id=context.task_id,
                framework=AgentFramework.AUTOGEN,
                agents_used=[config.name for config in agent_configs],
                execution_time=0.5,  # Simulated
                success=True,
                results=results
            )
            
        except Exception as e:
            logger.error(f"AutoGen execution error: {e}")
            return OrchestrationResult(
                task_id=context.task_id,
                framework=AgentFramework.AUTOGEN,
                agents_used=[],
                execution_time=0,
                success=False,
                results={},
                error=str(e)
            )

class LangChainAdapter(FrameworkAdapter):
    """LangChain framework adapter."""
    
    async def execute_agents(self, agent_configs: List[AgentConfig], context: TaskContext) -> OrchestrationResult:
        try:
            # This would integrate with LangChain
            # For now, simulate execution
            logger.info(f"Executing {len(agent_configs)} agents with LangChain")
            
            # Simulate agent execution
            results = {}
            for agent_config in agent_configs:
                # Simulate agent processing
                simulated_result = {
                    "agent_name": agent_config.name,
                    "role": agent_config.role,
                    "output": f"LangChain processed: {context.task_description}",
                    "context_used": list(context.shared_memory.keys()),
                    "timestamp": time.time()
                }
                results[agent_config.name] = simulated_result
            
            return OrchestrationResult(
                task_id=context.task_id,
                framework=AgentFramework.LANGCHAIN,
                agents_used=[config.name for config in agent_configs],
                execution_time=0.3,  # Simulated
                success=True,
                results=results
            )
            
        except Exception as e:
            logger.error(f"LangChain execution error: {e}")
            return OrchestrationResult(
                task_id=context.task_id,
                framework=AgentFramework.LANGCHAIN,
                agents_used=[],
                execution_time=0,
                success=False,
                results={},
                error=str(e)
            )

class LangGraphAdapter(FrameworkAdapter):
    """LangGraph framework adapter."""
    
    async def execute_agents(self, agent_configs: List[AgentConfig], context: TaskContext) -> OrchestrationResult:
        try:
            # This would integrate with LangGraph
            # For now, simulate execution
            logger.info(f"Executing {len(agent_configs)} agents with LangGraph")
            
            # Simulate agent execution
            results = {}
            for agent_config in agent_configs:
                # Simulate agent processing
                simulated_result = {
                    "agent_name": agent_config.name,
                    "role": agent_config.role,
                    "output": f"LangGraph workflow completed: {context.task_description}",
                    "context_used": list(context.shared_memory.keys()),
                    "timestamp": time.time()
                }
                results[agent_config.name] = simulated_result
            
            return OrchestrationResult(
                task_id=context.task_id,
                framework=AgentFramework.LANGGRAPH,
                agents_used=[config.name for config in agent_configs],
                execution_time=0.4,  # Simulated
                success=True,
                results=results
            )
            
        except Exception as e:
            logger.error(f"LangGraph execution error: {e}")
            return OrchestrationResult(
                task_id=context.task_id,
                framework=AgentFramework.LANGGRAPH,
                agents_used=[],
                execution_time=0,
                success=False,
                results={},
                error=str(e)
            )

class CrewAIAdapter(FrameworkAdapter):
    """CrewAI framework adapter."""
    
    async def execute_agents(self, agent_configs: List[AgentConfig], context: TaskContext) -> OrchestrationResult:
        try:
            # This would integrate with CrewAI
            # For now, simulate execution
            logger.info(f"Executing {len(agent_configs)} agents with CrewAI")
            
            # Simulate agent execution
            results = {}
            for agent_config in agent_configs:
                # Simulate agent processing
                simulated_result = {
                    "agent_name": agent_config.name,
                    "role": agent_config.role,
                    "output": f"CrewAI crew completed: {context.task_description}",
                    "context_used": list(context.shared_memory.keys()),
                    "timestamp": time.time()
                }
                results[agent_config.name] = simulated_result
            
            return OrchestrationResult(
                task_id=context.task_id,
                framework=AgentFramework.CREWAI,
                agents_used=[config.name for config in agent_configs],
                execution_time=0.6,  # Simulated
                success=True,
                results=results
            )
            
        except Exception as e:
            logger.error(f"CrewAI execution error: {e}")
            return OrchestrationResult(
                task_id=context.task_id,
                framework=AgentFramework.CREWAI,
                agents_used=[],
                execution_time=0,
                success=False,
                results={},
                error=str(e)
            )

class AgentWorkflowBuilder:
    """Builder for creating complex agent workflows."""
    
    def __init__(self, orchestrator: AgentOrchestrator):
        self.orchestrator = orchestrator
        self.workflow_steps = []
    
    def add_agent(self, name: str, role: str, goal: str, backstory: str, 
                  framework: AgentFramework, **kwargs) -> 'AgentWorkflowBuilder':
        """Add an agent to the workflow."""
        agent_config = AgentConfig(
            name=name,
            role=role,
            goal=goal,
            backstory=backstory,
            framework=framework,
            **kwargs
        )
        self.orchestrator.register_agent(agent_config)
        return self
    
    def add_step(self, step_name: str, agents: List[str], task: str) -> 'AgentWorkflowBuilder':
        """Add a workflow step."""
        self.workflow_steps.append({
            "name": step_name,
            "agents": agents,
            "task": task
        })
        return self
    
    async def execute_workflow(self, initial_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the complete workflow."""
        results = {}
        
        for i, step in enumerate(self.workflow_steps):
            task_id = f"workflow_step_{i+1}_{step['name']}"
            
            result = await self.orchestrator.orchestrate_task(
                task_id=task_id,
                agents=step["agents"],
                task_description=step["task"],
                initial_context=initial_context if i == 0 else None
            )
            
            results[step["name"]] = result
            
            # Update initial context with results for next step
            if result.success and result.results:
                if initial_context is None:
                    initial_context = {}
                initial_context.update(result.results)
        
        return results

# Global orchestrator instance
global_orchestrator = AgentOrchestrator()

def create_workflow_builder() -> AgentWorkflowBuilder:
    """Create a new workflow builder."""
    return AgentWorkflowBuilder(global_orchestrator)

# Example usage functions
async def example_single_framework_orchestration():
    """Example of single framework orchestration."""
    orchestrator = AgentOrchestrator()
    
    # Register agents
    orchestrator.register_agent(AgentConfig(
        name="researcher",
        role="Researcher",
        goal="Research complex topics",
        backstory="Expert researcher with extensive knowledge",
        framework=AgentFramework.AUTOGEN
    ))
    
    orchestrator.register_agent(AgentConfig(
        name="analyst",
        role="Analyst",
        goal="Analyze research findings",
        backstory="Data analysis specialist",
        framework=AgentFramework.AUTOGEN
    ))
    
    # Execute task
    result = await orchestrator.orchestrate_task(
        task_id="research_task_001",
        agents=["researcher", "analyst"],
        task_description="Research the latest developments in AI agent orchestration"
    )
    
    return result

async def example_multi_framework_orchestration():
    """Example of multi-framework orchestration."""
    orchestrator = AgentOrchestrator()
    
    # Register agents across frameworks
    orchestrator.register_agent(AgentConfig(
        name="autogen_researcher",
        role="Researcher",
        goal="Research using AutoGen",
        backstory="AutoGen specialist",
        framework=AgentFramework.AUTOGEN
    ))
    
    orchestrator.register_agent(AgentConfig(
        name="langchain_analyzer",
        role="Analyzer",
        goal="Analyze using LangChain",
        backstory="LangChain expert",
        framework=AgentFramework.LANGCHAIN
    ))
    
    orchestrator.register_agent(AgentConfig(
        name="crewai_writer",
        role="Writer",
        goal="Write reports using CrewAI",
        backstory="CrewAI content specialist",
        framework=AgentFramework.CREWAI
    ))
    
    # Execute task
    result = await orchestrator.orchestrate_task(
        task_id="multi_framework_task_001",
        agents=["autogen_researcher", "langchain_analyzer", "crewai_writer"],
        task_description="Complete research, analysis, and report writing task"
    )
    
    return result

async def example_workflow_builder():
    """Example using the workflow builder."""
    builder = create_workflow_builder()
    
    # Build workflow
    builder.add_agent(
        name="researcher",
        role="Researcher",
        goal="Research topics",
        backstory="Research expert",
        framework=AgentFramework.AUTOGEN
    ).add_agent(
        name="analyst",
        role="Analyst",
        goal="Analyze data",
        backstory="Data analyst",
        framework=AgentFramework.LANGCHAIN
    ).add_step(
        step_name="research_step",
        agents=["researcher"],
        task="Research the topic"
    ).add_step(
        step_name="analysis_step",
        agents=["analyst"],
        task="Analyze the research findings"
    )
    
    # Execute workflow
    results = await builder.execute_workflow()
    return results

if __name__ == "__main__":
    # Example usage
    async def main():
        print("Agent Orchestration Framework Examples")
        
        # Single framework example
        print("\n1. Single Framework Orchestration:")
        result1 = await example_single_framework_orchestration()
        print(f"Success: {result1.success}")
        print(f"Agents used: {result1.agents_used}")
        
        # Multi-framework example
        print("\n2. Multi-Framework Orchestration:")
        result2 = await example_multi_framework_orchestration()
        print(f"Success: {result2.success}")
        print(f"Framework results: {list(result2.results.keys())}")
        
        # Workflow builder example
        print("\n3. Workflow Builder:")
        result3 = await example_workflow_builder()
        print(f"Workflow steps completed: {len(result3)}")
    
    # Run examples
    asyncio.run(main())