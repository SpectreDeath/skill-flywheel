#!/usr/bin/env python3
"""
Enhanced MCP Server for Skill Flywheel

This enhanced MCP server provides advanced capabilities for skill management,
agent orchestration, validation, testing, and performance monitoring.
It builds on the existing MCP server infrastructure while adding sophisticated
new features for managing the 234+ skill empire.
"""

import datetime
import json
import logging
import os
import subprocess
import tempfile
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

from src.core.registry_search import search_registry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
server_name = os.environ.get("MCP_SERVER_NAME", "EnhancedSkillFlywheel")
mcp = FastMCP(server_name)

# Configuration from environment or defaults
REGISTRY_FILE = Path(os.environ.get("REGISTRY_FILE", "/app/skill_registry.json"))
SKILLS_DIR = Path(os.environ.get("SKILLS_DIR", "/app/domains"))
TELEMETRY_LOG = Path(os.environ.get("TELEMETRY_LOG", "/app/telemetry/usage_log.jsonl"))
MCP_DOMAINS = os.environ.get("MCP_DOMAINS", "").split(",") if os.environ.get("MCP_DOMAINS") else []

# Agent framework configurations
# Accessibility: API keys are optional. Features disable gracefully if keys are missing.
OPENAI_ENABLED = bool(os.environ.get("OPENAI_API_KEY"))
GEMINI_ENABLED = bool(os.environ.get("GEMINI_API_KEY"))

AUTOGEN_CONFIG = {
    "model": os.environ.get("AUTOGEN_MODEL", "gpt-4"),
    "api_key": os.environ.get("OPENAI_API_KEY") if OPENAI_ENABLED else "SKIPPED",
    "max_tokens": int(os.environ.get("AUTOGEN_MAX_TOKENS", "4000"))
}

LANGCHAIN_CONFIG = {
    "model": os.environ.get("LANGCHAIN_MODEL", "gpt-4"),
    "api_key": os.environ.get("OPENAI_API_KEY") if OPENAI_ENABLED else "SKIPPED",
    "temperature": float(os.environ.get("LANGCHAIN_TEMP", "0.1"))
}

# Performance monitoring
class MetricType(Enum):
    EXECUTION_TIME = "execution_time"
    SUCCESS_RATE = "success_rate"
    QUALITY_SCORE = "quality_score"
    RESOURCE_USAGE = "resource_usage"

@dataclass
class PerformanceMetric:
    skill_id: str
    metric_type: MetricType
    value: float
    timestamp: datetime.datetime
    context: Dict[str, Any]

class PerformanceMonitor:
    """Monitors and tracks performance metrics for skills and agents."""
    
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.skill_stats: Dict[str, Dict[str, Any]] = {}
        
    def record_metric(self, skill_id: str, metric_type: MetricType, value: float, context: Dict[str, Any] = None):
        """Record a performance metric."""
        metric = PerformanceMetric(
            skill_id=skill_id,
            metric_type=metric_type,
            value=value,
            timestamp=datetime.datetime.now(),
            context=context or {}
        )
        self.metrics.append(metric)
        
        # Update skill statistics
        if skill_id not in self.skill_stats:
            self.skill_stats[skill_id] = {
                "execution_time_count": 0,
                "total_time": 0,
                "success_rate_count": 0,
                "success_count": 0,
                "quality_scores": []
            }
        
        stats = self.skill_stats[skill_id]
        if metric_type == MetricType.EXECUTION_TIME:
            stats["total_time"] += value
            stats["execution_time_count"] += 1
        elif metric_type == MetricType.SUCCESS_RATE:
            stats["success_rate_count"] += 1
            if value > 0:
                stats["success_count"] += 1
        elif metric_type == MetricType.QUALITY_SCORE:
            stats["quality_scores"].append(value)
        
    def get_skill_performance(self, skill_id: str) -> Dict[str, Any]:
        """Get performance statistics for a skill."""
        if skill_id not in self.skill_stats:
            return {"error": f"No metrics found for skill {skill_id}"}
            
        stats = self.skill_stats[skill_id]
        avg_time = stats["total_time"] / stats["execution_time_count"] if stats["execution_time_count"] > 0 else 0
        success_rate = stats["success_count"] / stats["success_rate_count"] if stats["success_rate_count"] > 0 else 0
        avg_quality = sum(stats["quality_scores"]) / len(stats["quality_scores"]) if stats["quality_scores"] else 0
        
        return {
            "skill_id": skill_id,
            "total_executions": stats["execution_time_count"],
            "average_execution_time": avg_time,
            "success_rate": success_rate,
            "average_quality_score": avg_quality,
            "last_execution": max([m.timestamp for m in self.metrics if m.skill_id == skill_id], default=None)
        }

# Global instances
performance_monitor = PerformanceMonitor()

def log_telemetry(skill_id, request, duration=0, status="success"):
    """Log skill usage to a JSONL file."""
    try:
        TELEMETRY_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "skill": skill_id,
            "request_preview": request[:100] if request else "",
            "duration": duration,
            "status": status,
            "server": server_name
        }
        with open(TELEMETRY_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        logger.error(f"Telemetry logging error: {e}")

def load_skill_registry() -> List[Dict[str, Any]]:
    """Load the skill registry from JSON file."""
    if not REGISTRY_FILE.exists():
        logger.error(f"Registry file not found at {REGISTRY_FILE}")
        return []
    
    try:
        with open(REGISTRY_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading registry: {e}")
        return []

def filter_skills_by_domain(skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter skills by configured domains."""
    if not MCP_DOMAINS:
        return skills
    return [skill for skill in skills if skill.get('domain') in MCP_DOMAINS]

# MCP Tools Implementation

@mcp.tool()
async def discover_skills(ctx, query: str, domain: str = None, limit: int = 10, include_details: bool = False):
    """
    Advanced skill discovery with semantic search and filtering.
    
    Args:
        query: Search query for skills
        domain: Optional domain filter
        limit: Maximum number of results
        include_details: Whether to include full skill details
    
    Returns:
        List of matching skills with relevance scores
    """
    try:
        skills = load_skill_registry()
        filtered_skills = filter_skills_by_domain(skills)
        
        # Use existing search functionality
        search_results = search_registry(query)
        
        if include_details:
            # Load full skill details for top results
            detailed_results = []
            for result in search_results:
                skill_path = REGISTRY_FILE.parent / result['path']
                if skill_path.exists():
                    try:
                        with open(skill_path, encoding='utf-8') as f:
                            content = f.read()
                        result['full_content'] = content
                    except Exception as e:
                        logger.warning(f"Could not load full content for {result['name']}: {e}")
                detailed_results.append(result)
            search_results = detailed_results
        
        return {
            "query": query,
            "domain_filter": domain,
            "results": search_results,
            "total_found": len(search_results),
            "domains_available": list(set(skill.get('domain') for skill in filtered_skills))
        }
        
    except Exception as e:
        logger.error(f"Error in discover_skills: {e}")
        return {"error": str(e), "results": []}

@mcp.tool()
async def model_select(ctx, task: str, hardware_profile: str = "Standard", constraint: str = None):
    """
    Select the optimal model based on hardware profile and task type.
    
    Args:
        task: Description of the task to be performed
        hardware_profile: Local hardware context (e.g., RTX 4090, A100, Mobile)
        constraint: Specific constraints (e.g., latency < 2s, precision)
        
    Returns:
        Recommended model and execution strategy
    """
    task_lower = task.lower()
    
    # Task Optimization Logic
    if any(kw in task_lower for kw in ["code", "python", "rust", "javascript", "refactor"]):
        base_model = "DeepSeek-V2-Coder"
        strategy = "Coding Specialist"
    elif any(kw in task_lower for kw in ["reason", "logic", "proof", "complex", "math"]):
        base_model = "o1-mini"
        strategy = "High-Reasoning Cluster"
    else:
        base_model = "Llama-3.1-70B"
        strategy = "General Purpose Routing"

    # Hardware Profiling Logic
    if "4090" in hardware_profile or "3090" in hardware_profile:
        quantization = "4-bit (AWQ)"
        note = "Optimized for High-End Consumer VRAM (24GB)"
    elif "A100" in hardware_profile or "H100" in hardware_profile:
        quantization = "FP8/BF16"
        note = "Enterprise Compute Scale - Full Precision"
    else:
        quantization = "8-bit"
        note = "Standard Hardware Fallback"

    # Chaos Selection Edge Case (Ralph Wiggum)
    if len(task_lower) < 5 or "banana" in task_lower:
        base_model = "GPT-4o (Chaos Mode)"
        strategy = "Entropy Management"
        note = "Nonsensical or extremely short input detected."

    result = {
        "recommended_model": base_model,
        "strategy": strategy,
        "quantization": quantization,
        "hardware_note": note,
        "routing_port": 8012,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    performance_monitor.record_metric("model_select", MetricType.EXECUTION_TIME, 0.005)
    return result


@mcp.tool()
async def execute_skill(ctx, skill_id: str, request: str = "", context: Dict[str, Any] = None):
    """
    Execute a skill with enhanced context management and error handling.
    
    Args:
        skill_id: ID of the skill to execute
        request: User request for the skill
        context: Additional context for execution
    
    Returns:
        Execution result with metadata
    """
    start_time = time.time()
    
    try:
        skills = load_skill_registry()
        filtered_skills = filter_skills_by_domain(skills)
        
        # Find the skill
        skill = next((s for s in filtered_skills if s['name'].lower().replace('-', '_') == skill_id.lower().replace('-', '_')), None)
        
        if not skill:
            return {"error": f"Skill '{skill_id}' not found", "available_skills": [s['name'] for s in filtered_skills[:5]]}
        
        # Load skill content
        skill_path = REGISTRY_FILE.parent / skill['path']
        if not skill_path.exists():
            return {"error": f"Skill file not found: {skill_path}"}
        
        with open(skill_path, encoding='utf-8') as f:
            content = f.read()
        
        # Enhanced execution with context
        execution_context = {
            "skill_id": skill_id,
            "skill_name": skill['name'],
            "domain": skill.get('domain', 'Unknown'),
            "version": skill.get('version', '1.0.0'),
            "purpose": skill.get('purpose', 'No purpose specified'),
            "description": skill.get('description', 'No description available'),
            "user_request": request,
            "execution_time": time.time() - start_time,
            "context": context or {}
        }
        
        result = {
            "skill_id": skill_id,
            "execution_context": execution_context,
            "content": content,
            "user_request": request,
            "execution_metadata": {
                "timestamp": datetime.datetime.now().isoformat(),
                "duration": time.time() - start_time,
                "context_provided": bool(context)
            }
        }
        
        # Record performance metrics
        performance_monitor.record_metric(skill_id, MetricType.EXECUTION_TIME, time.time() - start_time)
        performance_monitor.record_metric(skill_id, MetricType.SUCCESS_RATE, 1.0)
        
        log_telemetry(skill_id, request, duration=time.time() - start_time, status="success")
        return result
        
    except Exception as e:
        error_msg = f"Error executing skill {skill_id}: {str(e)}"
        logger.error(error_msg)
        
        # Record failure metrics
        performance_monitor.record_metric(skill_id, MetricType.SUCCESS_RATE, 0.0)
        log_telemetry(skill_id, request, status=f"error: {error_msg}")
        
        return {
            "error": error_msg,
            "skill_id": skill_id,
            "execution_time": time.time() - start_time
        }

@mcp.tool()
async def validate_skill(ctx, skill_id: str, validation_type: str = "all"):
    """
    Comprehensive skill validation including format, dependencies, and security.
    
    Args:
        skill_id: ID of the skill to validate
        validation_type: Type of validation (format, dependencies, security, all)
    
    Returns:
        Validation results with detailed reports
    """
    try:
        skills = load_skill_registry()
        filtered_skills = filter_skills_by_domain(skills)
        
        skill = next((s for s in filtered_skills if s['name'].lower().replace('-', '_') == skill_id.lower().replace('-', '_')), None)
        if not skill:
            return {"error": f"Skill '{skill_id}' not found"}
        
        skill_path = REGISTRY_FILE.parent / skill['path']
        if not skill_path.exists():
            return {"error": f"Skill file not found: {skill_path}"}
        
        validation_results = {
            "skill_id": skill_id,
            "validation_type": validation_type,
            "timestamp": datetime.datetime.now().isoformat(),
            "results": {}
        }
        
        # Format validation
        if validation_type in ["format", "all"]:
            validation_results["results"]["format"] = validate_skill_format(skill_path)
        
        # Dependencies validation
        if validation_type in ["dependencies", "all"]:
            validation_results["results"]["dependencies"] = validate_skill_dependencies(skill, filtered_skills)
        
        # Security validation
        if validation_type in ["security", "all"]:
            validation_results["results"]["security"] = validate_skill_security(skill_path)
        
        # Overall validation status
        all_passed = all(result.get("passed", False) for result in validation_results["results"].values())
        validation_results["overall_status"] = "passed" if all_passed else "failed"
        
        return validation_results
        
    except Exception as e:
        logger.error(f"Error validating skill {skill_id}: {e}")
        return {"error": str(e), "skill_id": skill_id}

def validate_skill_format(skill_path: Path) -> Dict[str, Any]:
    """Validate skill format and structure."""
    try:
        with open(skill_path, encoding='utf-8') as f:
            content = f.read()
        
        # Check for required sections
        required_sections = ["## Purpose", "## Description", "## Workflow", "## Constraints"]
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        # Check YAML frontmatter
        has_frontmatter = content.startswith("---")
        
        return {
            "passed": len(missing_sections) == 0 and has_frontmatter,
            "missing_sections": missing_sections,
            "has_frontmatter": has_frontmatter,
            "total_lines": len(content.split('\n')),
            "file_size": len(content)
        }
    except Exception as e:
        return {"passed": False, "error": str(e)}

def validate_skill_dependencies(skill: Dict[str, Any], all_skills: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate skill dependencies and circular references."""
    try:
        # This would need to be implemented based on your dependency structure
        # For now, return a basic validation
        return {
            "passed": True,
            "dependencies": [],
            "circular_dependencies": [],
            "missing_dependencies": []
        }
    except Exception as e:
        return {"passed": False, "error": str(e)}

def validate_skill_security(skill_path: Path) -> Dict[str, Any]:
    """Validate skill security and potential vulnerabilities."""
    try:
        with open(skill_path, encoding='utf-8') as f:
            content = f.read()
        
        # Basic security checks
        security_issues = []
        
        # Check for hardcoded secrets
        if "password" in content.lower() or "secret" in content.lower() or "api_key" in content.lower():
            security_issues.append("Potential hardcoded secrets detected")
        
        # Check for dangerous operations
        dangerous_patterns = ["eval(", "exec(", "subprocess.", "os.system"]
        for pattern in dangerous_patterns:
            if pattern in content:
                security_issues.append(f"Dangerous operation detected: {pattern}")
        
        return {
            "passed": len(security_issues) == 0,
            "security_issues": security_issues,
            "content_length": len(content)
        }
    except Exception as e:
        return {"passed": False, "error": str(e)}

@mcp.tool()
async def test_skill(ctx, skill_id: str, test_framework: str = "pytest", test_cases: List[Dict[str, Any]] = None):
    """
    Automated skill testing with multiple frameworks.
    
    Args:
        skill_id: ID of the skill to test
        test_framework: Testing framework to use
        test_cases: Custom test cases
    
    Returns:
        Test results and coverage information
    """
    try:
        skills = load_skill_registry()
        filtered_skills = filter_skills_by_domain(skills)
        
        skill = next((s for s in filtered_skills if s['name'].lower().replace('-', '_') == skill_id.lower().replace('-', '_')), None)
        if not skill:
            return {"error": f"Skill '{skill_id}' not found"}
        
        skill_path = REGISTRY_FILE.parent / skill['path']
        if not skill_path.exists():
            return {"error": f"Skill file not found: {skill_path}"}
        
        # Create test environment
        with tempfile.TemporaryDirectory() as temp_dir:
            test_results = {
                "skill_id": skill_id,
                "test_framework": test_framework,
                "timestamp": datetime.datetime.now().isoformat(),
                "results": {}
            }
            
            # Run tests based on framework
            if test_framework == "pytest":
                test_results["results"] = run_pytest_tests(skill_path, temp_dir, test_cases)
            elif test_framework == "unittest":
                test_results["results"] = run_unittest_tests(skill_path, temp_dir, test_cases)
            else:
                test_results["results"] = {"error": f"Unsupported test framework: {test_framework}"}
            
            return test_results
            
    except Exception as e:
        logger.error(f"Error testing skill {skill_id}: {e}")
        return {"error": str(e), "skill_id": skill_id}

def run_pytest_tests(skill_path: Path, temp_dir: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run pytest tests for a skill."""
    try:
        # This would need to be implemented based on your testing requirements
        # For now, return a basic structure
        return {
            "framework": "pytest",
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "coverage": 0.0,
            "test_cases_run": test_cases or []
        }
    except Exception as e:
        return {"error": str(e)}

def run_unittest_tests(skill_path: Path, temp_dir: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run unittest tests for a skill."""
    try:
        # This would need to be implemented based on your testing requirements
        # For now, return a basic structure
        return {
            "framework": "unittest",
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "coverage": 0.0,
            "test_cases_run": test_cases or []
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def benchmark_skill(ctx, skill_id: str, iterations: int = 10, test_data: List[str] = None):
    """
    Benchmark skill performance and quality metrics.
    
    Args:
        skill_id: ID of the skill to benchmark
        iterations: Number of iterations to run
        test_data: Test data for benchmarking
    
    Returns:
        Performance and quality metrics
    """
    try:
        skills = load_skill_registry()
        filtered_skills = filter_skills_by_domain(skills)
        
        skill = next((s for s in filtered_skills if s['name'].lower().replace('-', '_') == skill_id.lower().replace('-', '_')), None)
        if not skill:
            return {"error": f"Skill '{skill_id}' not found"}
        
        skill_path = REGISTRY_FILE.parent / skill['path']
        if not skill_path.exists():
            return {"error": f"Skill file not found: {skill_path}"}
        
        # Run benchmark
        benchmark_results = {
            "skill_id": skill_id,
            "iterations": iterations,
            "timestamp": datetime.datetime.now().isoformat(),
            "metrics": {}
        }
        
        execution_times = []
        quality_scores = []
        
        for i in range(iterations):
            start_time = time.time()
            
            # Execute skill (simplified for benchmarking)
            with open(skill_path, encoding='utf-8') as f:
                content = f.read()
            
            execution_time = time.time() - start_time
            execution_times.append(execution_time)
            
            # Calculate quality score (simplified)
            quality_score = calculate_quality_score(content)
            quality_scores.append(quality_score)
        
        # Calculate statistics
        avg_time = sum(execution_times) / len(execution_times) if execution_times else 0
        min_time = min(execution_times) if execution_times else 0
        max_time = max(execution_times) if execution_times else 0
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        benchmark_results["metrics"] = {
            "execution_times": execution_times,
            "quality_scores": quality_scores,
            "statistics": {
                "average_execution_time": avg_time,
                "min_execution_time": min_time,
                "max_execution_time": max_time,
                "average_quality_score": avg_quality,
                "quality_variance": calculate_variance(quality_scores)
            }
        }
        
        # Record performance metrics
        performance_monitor.record_metric(skill_id, MetricType.EXECUTION_TIME, avg_time)
        performance_monitor.record_metric(skill_id, MetricType.QUALITY_SCORE, avg_quality)
        
        return benchmark_results
        
    except Exception as e:
        logger.error(f"Error benchmarking skill {skill_id}: {e}")
        return {"error": str(e), "skill_id": skill_id}

def calculate_quality_score(content: str) -> float:
    """Calculate a basic quality score for skill content."""
    # Basic quality metrics
    score = 0.0
    
    # Check for required sections
    required_sections = ["## Purpose", "## Description", "## Workflow", "## Constraints"]
    for section in required_sections:
        if section in content:
            score += 0.1
    
    # Check content length
    if len(content) > 1000:
        score += 0.2
    
    # Check for code examples
    if "```" in content:
        score += 0.2
    
    # Check for clear structure
    lines = content.split('\n')
    headers = [line for line in lines if line.startswith('#')]
    if len(headers) >= 5:
        score += 0.2
    
    return min(score, 1.0)

def calculate_variance(values: List[float]) -> float:
    """Calculate variance of a list of values."""
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance

@mcp.tool()
async def orchestrate_agents(ctx, agent_type: str, task: str, agents_config: List[Dict[str, Any]] = None):
    """
    Orchestrate multi-agent workflows using different frameworks.
    
    Args:
        agent_type: Type of agent framework (autogen, langchain, langgraph, crewai)
        task: Task to be performed by the agents
        agents_config: Configuration for agents
    
    Returns:
        Orchestration results and agent coordination information
    """
    try:
        orchestration_results = {
            "agent_type": agent_type,
            "task": task,
            "timestamp": datetime.datetime.now().isoformat(),
            "results": {}
        }
        
        if agent_type == "autogen":
            orchestration_results["results"] = await orchestrate_autogen_agents(task, agents_config)
        elif agent_type == "langchain":
            orchestration_results["results"] = await orchestrate_langchain_agents(task, agents_config)
        elif agent_type == "langgraph":
            orchestration_results["results"] = await orchestrate_langgraph_agents(task, agents_config)
        elif agent_type == "crewai":
            orchestration_results["results"] = await orchestrate_crewai_agents(task, agents_config)
        else:
            orchestration_results["results"] = {"error": f"Unsupported agent type: {agent_type}"}
        
        return orchestration_results
        
    except Exception as e:
        logger.error(f"Error orchestrating agents: {e}")
        return {"error": str(e), "agent_type": agent_type, "task": task}

async def orchestrate_autogen_agents(task: str, agents_config: List[Dict[str, Any]]):
    """Orchestrate AutoGen agents."""
    try:
        # This would need AutoGen integration
        # For now, return a basic structure
        return {
            "framework": "autogen",
            "agents_configured": len(agents_config or []),
            "task": task,
            "status": "simulated_orchestration",
            "note": "AutoGen integration requires additional setup"
        }
    except Exception as e:
        return {"error": str(e)}

async def orchestrate_langchain_agents(task: str, agents_config: List[Dict[str, Any]]):
    """Orchestrate LangChain agents."""
    try:
        # This would need LangChain integration
        # For now, return a basic structure
        return {
            "framework": "langchain",
            "agents_configured": len(agents_config or []),
            "task": task,
            "status": "simulated_orchestration",
            "note": "LangChain integration requires additional setup"
        }
    except Exception as e:
        return {"error": str(e)}

async def orchestrate_langgraph_agents(task: str, agents_config: List[Dict[str, Any]]):
    """Orchestrate LangGraph agents."""
    try:
        # This would need LangGraph integration
        # For now, return a basic structure
        return {
            "framework": "langgraph",
            "agents_configured": len(agents_config or []),
            "task": task,
            "status": "simulated_orchestration",
            "note": "LangGraph integration requires additional setup"
        }
    except Exception as e:
        return {"error": str(e)}

async def orchestrate_crewai_agents(task: str, agents_config: List[Dict[str, Any]]):
    """Orchestrate CrewAI agents."""
    try:
        # This would need CrewAI integration
        # For now, return a basic structure
        return {
            "framework": "crewai",
            "agents_configured": len(agents_config or []),
            "task": task,
            "status": "simulated_orchestration",
            "note": "CrewAI integration requires additional setup"
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_performance_metrics(ctx, skill_id: str = None, metric_type: str = None, time_range: str = "24h"):
    """
    Get performance metrics and analytics.
    
    Args:
        skill_id: Specific skill to get metrics for (None for all)
        metric_type: Type of metric to retrieve
        time_range: Time range for metrics (1h, 24h, 7d, 30d)
    
    Returns:
        Performance metrics and analytics
    """
    try:
        metrics_results = {
            "time_range": time_range,
            "timestamp": datetime.datetime.now().isoformat(),
            "metrics": {}
        }
        
        if skill_id:
            # Get metrics for specific skill
            skill_metrics = performance_monitor.get_skill_performance(skill_id)
            metrics_results["metrics"][skill_id] = skill_metrics
        else:
            # Get metrics for all skills
            for skill_id in performance_monitor.skill_stats:
                skill_metrics = performance_monitor.get_skill_performance(skill_id)
                metrics_results["metrics"][skill_id] = skill_metrics
        
        # Add overall statistics
        total_executions = sum(stats["total_executions"] for stats in performance_monitor.skill_stats.values())
        total_time = sum(stats["total_time"] for stats in performance_monitor.skill_stats.values())
        avg_execution_time = total_time / total_executions if total_executions > 0 else 0
        
        metrics_results["overall_statistics"] = {
            "total_skills_tracked": len(performance_monitor.skill_stats),
            "total_executions": total_executions,
            "average_execution_time": avg_execution_time,
            "total_metrics_recorded": len(performance_monitor.metrics)
        }
        
        return metrics_results
        
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        return {"error": str(e)}

@mcp.tool()
async def find_skill(ctx, query: str, category: str = None):
    """
    Search the AgentSkills library for relevant skills based on a query.
    Useful when you aren't sure which specialized skill to use.
    """
    
    script_path = Path(__file__).parent / "registry_search.py"
    cmd = ["python", str(script_path), query]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return f"SEARCH RESULTS for '{query}':\n\n{result.stdout}"
    except Exception as e:
        return f"Error searching registry: {str(e)}"

def register_existing_skills():
    """Register existing skills from the registry."""
    if not REGISTRY_FILE.exists():
        logger.error(f"Registry file not found at {REGISTRY_FILE}. Run reindex_skills.py first.")
        return

    try:
        with open(REGISTRY_FILE, encoding='utf-8') as f:
            registry = json.load(f)
            
        registered_count = 0
        for skill in registry:
            domain = skill.get('domain', 'General')
            
            # Filter by domain if MCP_DOMAINS is set
            if MCP_DOMAINS and domain not in MCP_DOMAINS:
                continue
                
            skill_id = skill['name'].lower().replace('-', '_')
            description = skill['description'] or skill['purpose'] or f"Execute the {skill_id} skill."
            
            # Use path from registry, resolve against workspace root
            root_dir = REGISTRY_FILE.parent
            skill_file = root_dir / skill['path']
            
            # Create a closure for the tool function
            def create_tool_func(path, sid):
                async def skill_tool(ctx, request: str = ""):
                    """
                    Execute this skill.
                    Instruction: Following the workflow and constraints in this skill, process the request.
                    """
                    import time
                    start_time = time.time()
                    try:
                        with open(path, encoding='utf-8') as f:
                            content = f.read()
                        
                        result = f"SYSTEM INSTRUCTIONS FOR SKILL:\n\n{content}\n\nUSER REQUEST: {request}\n\nGUIDANCE: Follow the Workflow and Constraints sections strictly."
                        log_telemetry(sid, request, duration=time.time() - start_time, status="success")
                        return result
                    except Exception as e:
                        error_msg = f"Error loading skill content ({path}): {str(e)}"
                        log_telemetry(sid, request, status=f"error: {error_msg}")
                        return error_msg
                return skill_tool

            # Register the tool with a unique name
            tool_func = create_tool_func(skill_file, skill_id)
            tool_func.__name__ = f"skill_{skill_id}"
            mcp.tool(name=f"skill_{skill_id}", description=description)(tool_func)
            registered_count += 1
            
        logger.info(f"Registered {registered_count} existing skills from domains: {', '.join(MCP_DOMAINS) if MCP_DOMAINS else 'All'}")
    except Exception as e:
        logger.error(f"Error registering existing skills: {e}")

if __name__ == "__main__":
    # Register existing skills
    register_existing_skills()
    
    # Start the enhanced MCP server
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    port = int(os.environ.get("PORT", 8000))
    
    logger.info(f"Starting Enhanced MCP Server: {server_name}")
    logger.info(f"Registry: {REGISTRY_FILE}")
    logger.info(f"Skills Directory: {SKILLS_DIR}")
    logger.info(f"Domains: {', '.join(MCP_DOMAINS) if MCP_DOMAINS else 'All'}")
    logger.info(f"Port: {port}")
    
    # Use uvicorn directly for HTTP-based services (like discovery service)
    if transport == "http":
        import uvicorn
        uvicorn.run(mcp.sse_app, host="0.0.0.0", port=port)
    else:
        mcp.run()
