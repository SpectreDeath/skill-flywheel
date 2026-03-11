#!/usr/bin/env python3
"""
Enhanced MCP Server v2 with Dynamic Lazy Loading and Self-Optimization

This server provides:
- Dynamic lazy loading with intelligent caching
- Self-optimization based on usage patterns
- Advanced dependency management
- Performance monitoring and analytics
- Resource-aware optimization
- Multi-agent orchestration
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
from typing import Any, Dict, List, Optional, Tuple, Union, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict, deque
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
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pickle

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_mcp_server_v2.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Enhanced Configuration
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
                "max_skill_size": 1024 * 1024,  # 1MB
                "lazy_loading": {
                    "enabled": True,
                    "cache_size": 50,
                    "ttl_seconds": 1800,  # 30 minutes
                    "pre_load_threshold": 0.8,
                    "unload_threshold": 0.2
                },
                "optimization": {
                    "enabled": True,
                    "learning_rate": 0.1,
                    "prediction_window": 100,
                    "resource_aware": True,
                    "adaptive_thresholds": True
                }
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

# Enhanced Telemetry and Monitoring
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
    active_skills: int
    cached_skills: int

@dataclass
class SkillMetrics:
    """Skill-specific metrics for optimization"""
    skill_name: str
    load_count: int
    execution_count: int
    total_load_time: float
    total_execution_time: float
    avg_load_time: float
    avg_execution_time: float
    last_load_time: Optional[datetime]
    last_execution_time: Optional[datetime]
    dependency_count: int
    memory_usage: float
    success_rate: float
    priority_score: float = 0.0
    predicted_usage: float = 0.0

@dataclass
class UsagePattern:
    """Usage pattern for predictive loading"""
    skill_name: str
    hour_of_day: int
    day_of_week: int
    frequency: int
    co_occurrence_skills: List[str]
    time_since_last_use: int

class TelemetryManager:
    """Advanced telemetry and monitoring system with ML capabilities"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.metrics_history: List[PerformanceMetrics] = []
        self.skill_metrics: Dict[str, SkillMetrics] = {}
        self.usage_patterns: Dict[str, List[UsagePattern]] = defaultdict(list)
        self.start_time = datetime.now()
        
        # ML models for prediction
        self.load_time_predictor = LinearRegression()
        self.usage_predictor = LinearRegression()
        self.scaler = StandardScaler()
        
        # Pattern learning
        self.pattern_window = config["skills"]["optimization"]["prediction_window"]
        self.learning_data = []
        
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
                avg_response_time=0.0,  # Will be updated by response time tracking
                active_skills=len([m for m in self.skill_metrics.values() if m.load_count > 0]),
                cached_skills=len([m for m in self.skill_metrics.values() if m.priority_score > 0.5])
            )
            
            self.metrics_history.append(metrics)
            
            # Keep only last 1000 metrics to prevent memory bloat
            if len(self.metrics_history) > 1000:
                self.metrics_history.pop(0)
                
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            return None
    
    def track_skill_execution(self, skill_name: str, load_time: float, 
                            execution_time: float, success: bool, dependencies: List[str]):
        """Track skill execution metrics for optimization"""
        if skill_name not in self.skill_metrics:
            self.skill_metrics[skill_name] = SkillMetrics(
                skill_name=skill_name,
                load_count=0,
                execution_count=0,
                total_load_time=0.0,
                total_execution_time=0.0,
                avg_load_time=0.0,
                avg_execution_time=0.0,
                last_load_time=None,
                last_execution_time=None,
                dependency_count=len(dependencies),
                memory_usage=0.0,
                success_rate=0.0
            )
        
        metrics = self.skill_metrics[skill_name]
        
        # Update execution metrics
        metrics.execution_count += 1
        metrics.total_execution_time += execution_time
        metrics.avg_execution_time = metrics.total_execution_time / metrics.execution_count
        metrics.last_execution_time = datetime.now()
        
        # Update load metrics if skill was loaded
        if load_time > 0:
            metrics.load_count += 1
            metrics.total_load_time += load_time
            metrics.avg_load_time = metrics.total_load_time / metrics.load_count
            metrics.last_load_time = datetime.now()
        
        # Update success rate
        if success:
            metrics.success_rate = (metrics.success_rate * (metrics.execution_count - 1) + 1) / metrics.execution_count
        else:
            metrics.success_rate = (metrics.success_rate * (metrics.execution_count - 1)) / metrics.execution_count
        
        # Update memory usage (approximation)
        process = psutil.Process()
        metrics.memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        
        # Learn usage patterns
        self._learn_usage_pattern(skill_name)
    
    def _learn_usage_pattern(self, skill_name: str):
        """Learn usage patterns for predictive loading"""
        now = datetime.now()
        pattern = UsagePattern(
            skill_name=skill_name,
            hour_of_day=now.hour,
            day_of_week=now.weekday(),
            frequency=1,
            co_occurrence_skills=self._get_co_occurrence_skills(skill_name),
            time_since_last_use=self._get_time_since_last_use(skill_name)
        )
        
        self.usage_patterns[skill_name].append(pattern)
        
        # Keep only recent patterns
        if len(self.usage_patterns[skill_name]) > self.pattern_window:
            self.usage_patterns[skill_name].pop(0)
    
    def _get_co_occurrence_skills(self, skill_name: str) -> List[str]:
        """Get skills that are frequently used together"""
        # This is a simplified version - in practice, you'd track co-occurrence
        # from actual usage patterns
        return []
    
    def _get_time_since_last_use(self, skill_name: str) -> int:
        """Get time since last use in minutes"""
        if skill_name in self.skill_metrics:
            last_use = self.skill_metrics[skill_name].last_execution_time
            if last_use:
                return int((datetime.now() - last_use).total_seconds() / 60)
        return 0
    
    def predict_skill_usage(self, skill_name: str) -> float:
        """Predict likelihood of skill usage based on patterns"""
        if skill_name not in self.usage_patterns:
            return 0.1  # Low priority for unknown skills
        
        patterns = self.usage_patterns[skill_name]
        if not patterns:
            return 0.1
        
        # Simple prediction based on recent usage
        now = datetime.now()
        recent_patterns = [p for p in patterns if (now - datetime.fromtimestamp(p.last_execution_time.timestamp() if p.last_execution_time else now.timestamp())).days < 7]
        
        if not recent_patterns:
            return 0.1
        
        # Calculate usage frequency
        total_frequency = sum(p.frequency for p in recent_patterns)
        avg_time_since_last = sum(p.time_since_last_use for p in recent_patterns) / len(recent_patterns)
        
        # Simple scoring
        usage_score = min(total_frequency / 10.0, 1.0)
        recency_score = max(0.0, 1.0 - (avg_time_since_last / 1440.0))  # Normalize to 1 day
        
        return (usage_score + recency_score) / 2.0
    
    def calculate_priority_score(self, skill_name: str) -> float:
        """Calculate priority score for skill caching"""
        if skill_name not in self.skill_metrics:
            return 0.1
        
        metrics = self.skill_metrics[skill_name]
        
        # Factors for priority calculation
        usage_factor = min(metrics.execution_count / 100.0, 1.0)
        speed_factor = max(0.0, 1.0 - (metrics.avg_execution_time / 10.0))  # Normalize to 10s
        success_factor = metrics.success_rate
        dependency_factor = 1.0 - (metrics.dependency_count / 50.0)  # Normalize to 50 dependencies
        
        # Predictive factor
        predictive_factor = self.predict_skill_usage(skill_name)
        
        # Calculate weighted score
        priority = (
            usage_factor * 0.3 +
            speed_factor * 0.2 +
            success_factor * 0.25 +
            dependency_factor * 0.15 +
            predictive_factor * 0.1
        )
        
        # Update metrics
        metrics.priority_score = priority
        metrics.predicted_usage = predictive_factor
        
        return priority
    
    def get_optimization_recommendations(self) -> Dict[str, Any]:
        """Get optimization recommendations based on telemetry data"""
        recommendations = {
            "skills_to_preload": [],
            "skills_to_unload": [],
            "performance_issues": [],
            "resource_optimizations": []
        }
        
        # Analyze skill metrics
        for skill_name, metrics in self.skill_metrics.items():
            priority = self.calculate_priority_score(skill_name)
            
            # Skills to preload (high priority, not currently loaded)
            if priority > self.config["skills"]["lazy_loading"]["pre_load_threshold"]:
                recommendations["skills_to_preload"].append({
                    "skill": skill_name,
                    "priority": priority,
                    "avg_load_time": metrics.avg_load_time,
                    "avg_execution_time": metrics.avg_execution_time
                })
            
            # Skills to unload (low priority, currently loaded)
            elif priority < self.config["skills"]["lazy_loading"]["unload_threshold"]:
                if metrics.load_count > 0:  # Currently loaded
                    recommendations["skills_to_unload"].append({
                        "skill": skill_name,
                        "priority": priority,
                        "last_used": metrics.last_execution_time
                    })
        
        # Sort recommendations
        recommendations["skills_to_preload"].sort(key=lambda x: x["priority"], reverse=True)
        recommendations["skills_to_unload"].sort(key=lambda x: x["priority"])
        
        # Performance issues
        latest_metrics = self.metrics_history[-1] if self.metrics_history else None
        if latest_metrics:
            if latest_metrics.cpu_usage > 80:
                recommendations["performance_issues"].append("High CPU usage detected")
            if latest_metrics.memory_usage > 80:
                recommendations["performance_issues"].append("High memory usage detected")
            if latest_metrics.avg_response_time > 5.0:
                recommendations["performance_issues"].append("Slow response times detected")
        
        return recommendations
    
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
                    "response_time": latest.avg_response_time,
                    "active_skills": latest.active_skills,
                    "cached_skills": latest.cached_skills
                },
                "optimization": self.get_optimization_recommendations()
            }
        
        return {
            "status": "healthy",
            "uptime": str(datetime.now() - self.start_time),
            "metrics": {
                "cpu": latest.cpu_usage,
                "memory": latest.memory_usage,
                "disk": latest.disk_usage,
                "gpu": latest.gpu_usage,
                "response_time": latest.avg_response_time,
                "active_skills": latest.active_skills,
                "cached_skills": latest.cached_skills
            },
            "optimization": self.get_optimization_recommendations()
        }

# Enhanced Skill Management with Lazy Loading
class SkillStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    DEPRECATED = "deprecated"
    LOADING = "loading"
    UNLOADING = "unloading"

@dataclass
class SkillMetadata:
    """Metadata for skills with enhanced information"""
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
    memory_usage: float
    load_time: float
    is_loaded: bool = False
    last_accessed: Optional[datetime] = None

class LRUCache:
    """LRU Cache implementation for skill management"""
    
    def __init__(self, max_size: int = 50, ttl_seconds: int = 1800):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: Dict[str, Any] = {}
        self.access_order: deque = deque()
        self.timestamps: Dict[str, datetime] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache with LRU and TTL management"""
        if key not in self.cache:
            return None
        
        # Check TTL
        if (datetime.now() - self.timestamps[key]).total_seconds() > self.ttl_seconds:
            self._remove(key)
            return None
        
        # Update access order
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)
        
        return self.cache[key]
    
    def put(self, key: str, value: Any):
        """Put item in cache with LRU eviction"""
        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_size:
            # Evict LRU item
            lru_key = self.access_order.popleft()
            del self.cache[lru_key]
            del self.timestamps[lru_key]
        
        self.cache[key] = value
        self.timestamps[key] = datetime.now()
        self.access_order.append(key)
    
    def remove(self, key: str):
        """Remove item from cache"""
        self._remove(key)
    
    def _remove(self, key: str):
        """Internal remove method"""
        if key in self.cache:
            del self.cache[key]
        if key in self.timestamps:
            del self.timestamps[key]
        if key in self.access_order:
            self.access_order.remove(key)
    
    def cleanup(self):
        """Clean up expired items"""
        now = datetime.now()
        expired_keys = [
            key for key, timestamp in self.timestamps.items()
            if (now - timestamp).total_seconds() > self.ttl_seconds
        ]
        
        for key in expired_keys:
            self._remove(key)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hit_rate": 0.0,  # Would need to track hits/misses
            "expired_count": len([k for k, t in self.timestamps.items() 
                                if (datetime.now() - t).total_seconds() > self.ttl_seconds])
        }

class DependencyGraph:
    """Dependency graph for skill management"""
    
    def __init__(self):
        self.graph: Dict[str, List[str]] = {}
        self.reverse_graph: Dict[str, List[str]] = {}
    
    def add_skill(self, skill_name: str, dependencies: List[str]):
        """Add skill and its dependencies to graph"""
        self.graph[skill_name] = dependencies
        for dep in dependencies:
            if dep not in self.reverse_graph:
                self.reverse_graph[dep] = []
            self.reverse_graph[dep].append(skill_name)
    
    def get_dependencies(self, skill_name: str) -> List[str]:
        """Get all dependencies for a skill"""
        if skill_name not in self.graph:
            return []
        
        dependencies = []
        visited = set()
        
        def dfs(skill: str):
            if skill in visited:
                return
            visited.add(skill)
            for dep in self.graph.get(skill, []):
                dependencies.append(dep)
                dfs(dep)
        
        dfs(skill_name)
        return dependencies
    
    def get_dependents(self, skill_name: str) -> List[str]:
        """Get all skills that depend on this skill"""
        return self.reverse_graph.get(skill_name, [])
    
    def has_cycle(self) -> bool:
        """Check if dependency graph has cycles"""
        visited = set()
        rec_stack = set()
        
        def has_cycle_util(skill: str) -> bool:
            visited.add(skill)
            rec_stack.add(skill)
            
            for neighbor in self.graph.get(skill, []):
                if neighbor not in visited:
                    if has_cycle_util(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(skill)
            return False
        
        for skill in self.graph:
            if skill not in visited:
                if has_cycle_util(skill):
                    return True
        
        return False

class EnhancedSkillManager:
    """Enhanced skill lifecycle management with lazy loading and optimization"""
    
    def __init__(self, skills_dir: str = "skills", skill_registry: str = "skill_registry.json"):
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(exist_ok=True)
        self.skill_registry_path = Path(skill_registry)
        
        # Skill management
        self.skills: Dict[str, SkillMetadata] = {}
        self.skill_cache = LRUCache(
            max_size=self.config["skills"]["lazy_loading"]["cache_size"],
            ttl_seconds=self.config["skills"]["lazy_loading"]["ttl_seconds"]
        )
        self.dependency_graph = DependencyGraph()
        
        # Loading state
        self.loading_locks: Dict[str, asyncio.Lock] = {}
        self.loaded_skills: Set[str] = set()
        
        # Telemetry
        self.telemetry = TelemetryManager(self.config)
        
    @property
    def config(self) -> Dict[str, Any]:
        """Get configuration"""
        return ServerConfig().config
    
    def discover_skills(self) -> List[str]:
        """Auto-discover skills from registry and directory"""
        discovered = []
        
        # Load from skill registry
        if self.skill_registry_path.exists():
            try:
                with open(self.skill_registry_path, 'r') as f:
                    registry_data = json.load(f)
                
                for skill_data in registry_data:
                    skill_name = skill_data.get("name")
                    if skill_name:
                        metadata = self._create_metadata_from_registry(skill_data)
                        self.skills[skill_name] = metadata
                        self.dependency_graph.add_skill(skill_name, metadata.dependencies)
                        discovered.append(skill_name)
                        logger.info(f"Discovered skill from registry: {skill_name}")
            except Exception as e:
                logger.error(f"Failed to load skills from registry: {e}")
        
        # Auto-discover from directory
        for skill_file in self.skills_dir.glob("*.py"):
            skill_name = skill_file.stem
            if skill_name not in self.skills:
                try:
                    metadata = self._extract_metadata(skill_file)
                    self.skills[skill_name] = metadata
                    discovered.append(skill_name)
                    logger.info(f"Discovered skill from directory: {skill_name}")
                except Exception as e:
                    logger.error(f"Failed to load skill {skill_file}: {e}")
        
        # Check for cycles in dependency graph
        if self.dependency_graph.has_cycle():
            logger.warning("Circular dependencies detected in skill graph")
        
        return discovered
    
    def _create_metadata_from_registry(self, skill_data: Dict[str, Any]) -> SkillMetadata:
        """Create metadata from skill registry data"""
        return SkillMetadata(
            name=skill_data.get("name", ""),
            version=skill_data.get("version", "1.0.0"),
            description=skill_data.get("description", ""),
            author=skill_data.get("author", "Unknown"),
            dependencies=skill_data.get("dependencies", []),
            created_at=datetime.fromisoformat(skill_data.get("created_at", datetime.now().isoformat())),
            last_modified=datetime.fromisoformat(skill_data.get("last_modified", datetime.now().isoformat())),
            status=SkillStatus.INACTIVE,
            execution_count=0,
            avg_execution_time=0.0,
            memory_usage=0.0,
            load_time=0.0
        )
    
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
            status=SkillStatus.INACTIVE,
            execution_count=0,
            avg_execution_time=0.0,
            memory_usage=0.0,
            load_time=0.0
        )
    
    async def load_skill_dynamically(self, skill_name: str) -> Any:
        """Load skill dynamically with dependency management and caching"""
        if skill_name not in self.skills:
            raise ValueError(f"Skill {skill_name} not found")
        
        # Check if already loaded
        if skill_name in self.loaded_skills:
            return self.skill_cache.get(skill_name)
        
        # Get or create loading lock
        if skill_name not in self.loading_locks:
            self.loading_locks[skill_name] = asyncio.Lock()
        
        async with self.loading_locks[skill_name]:
            # Double-check after acquiring lock
            if skill_name in self.loaded_skills:
                return self.skill_cache.get(skill_name)
            
            start_time = time.time()
            
            try:
                # Load dependencies first
                dependencies = self.dependency_graph.get_dependencies(skill_name)
                for dep in dependencies:
                    if dep not in self.loaded_skills:
                        await self.load_skill_dynamically(dep)
                
                # Load the skill
                skill_file = self.skills_dir / f"{skill_name}.py"
                if not skill_file.exists():
                    raise FileNotFoundError(f"Skill file not found: {skill_file}")
                
                with open(skill_file, 'r') as f:
                    code = compile(f.read(), skill_file, 'exec')
                    namespace = {}
                    exec(code, namespace)
                
                # Cache the skill
                self.skill_cache.put(skill_name, namespace)
                self.loaded_skills.add(skill_name)
                
                # Update metadata
                metadata = self.skills[skill_name]
                metadata.status = SkillStatus.ACTIVE
                metadata.is_loaded = True
                metadata.last_accessed = datetime.now()
                metadata.load_time = time.time() - start_time
                
                # Track telemetry
                self.telemetry.track_skill_execution(
                    skill_name, metadata.load_time, 0.0, True, dependencies
                )
                
                logger.info(f"Loaded skill: {skill_name} in {metadata.load_time:.2f}s")
                return namespace
                
            except Exception as e:
                # Update metadata on failure
                metadata = self.skills[skill_name]
                metadata.status = SkillStatus.ERROR
                metadata.load_time = time.time() - start_time
                
                # Track telemetry
                self.telemetry.track_skill_execution(
                    skill_name, metadata.load_time, 0.0, False, dependencies
                )
                
                logger.error(f"Failed to load skill {skill_name}: {e}")
                raise
    
    async def unload_skill(self, skill_name: str):
        """Unload skill and its unused dependencies"""
        if skill_name not in self.skills:
            return
        
        if skill_name not in self.loaded_skills:
            return
        
        # Check if skill is still in use
        dependents = self.dependency_graph.get_dependents(skill_name)
        if any(dep in self.loaded_skills for dep in dependents):
            logger.debug(f"Skill {skill_name} still in use by other skills, not unloading")
            return
        
        # Unload the skill
        self.skill_cache.remove(skill_name)
        self.loaded_skills.discard(skill_name)
        
        # Update metadata
        metadata = self.skills[skill_name]
        metadata.status = SkillStatus.INACTIVE
        metadata.is_loaded = False
        
        logger.info(f"Unloaded skill: {skill_name}")
        
        # Recursively unload unused dependencies
        dependencies = self.dependency_graph.get_dependencies(skill_name)
        for dep in dependencies:
            await self.unload_skill(dep)
    
    async def execute_skill(self, skill_name: str, *args, **kwargs) -> Any:
        """Execute a skill with monitoring and optimization"""
        if skill_name not in self.skills:
            raise ValueError(f"Skill {skill_name} not found")
        
        metadata = self.skills[skill_name]
        start_time = time.time()
        
        try:
            # Load skill if not already loaded
            skill_namespace = await self.load_skill_dynamically(skill_name)
            
            # Execute the skill function
            skill_func = skill_namespace.get(skill_name)
            if not skill_func:
                raise ValueError(f"Skill function {skill_name} not found in {skill_name}.py")
            
            result = skill_func(*args, **kwargs)
            
            # Update execution metrics
            execution_time = time.time() - start_time
            metadata.execution_count += 1
            metadata.total_execution_time = (metadata.total_execution_time * (metadata.execution_count - 1) + execution_time) / metadata.execution_count
            metadata.last_accessed = datetime.now()
            
            # Track telemetry
            dependencies = self.dependency_graph.get_dependencies(skill_name)
            self.telemetry.track_skill_execution(
                skill_name, 0.0, execution_time, True, dependencies
            )
            
            logger.info(f"Skill {skill_name} executed successfully in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # Track telemetry for failure
            dependencies = self.dependency_graph.get_dependencies(skill_name)
            self.telemetry.track_skill_execution(
                skill_name, 0.0, execution_time, False, dependencies
            )
            
            logger.error(f"Skill {skill_name} execution failed: {e}")
            raise
    
    def get_optimization_suggestions(self) -> Dict[str, Any]:
        """Get optimization suggestions based on usage patterns"""
        suggestions = {
            "preload_skills": [],
            "unload_skills": [],
            "dependency_optimizations": [],
            "performance_recommendations": []
        }
        
        # Analyze skill metrics
        for skill_name, metadata in self.skills.items():
            priority = self.telemetry.calculate_priority_score(skill_name)
            
            if priority > 0.8 and not metadata.is_loaded:
                suggestions["preload_skills"].append({
                    "skill": skill_name,
                    "priority": priority,
                    "avg_execution_time": metadata.avg_execution_time,
                    "dependencies": metadata.dependencies
                })
            elif priority < 0.2 and metadata.is_loaded:
                suggestions["unload_skills"].append({
                    "skill": skill_name,
                    "priority": priority,
                    "last_accessed": metadata.last_accessed
                })
        
        # Sort suggestions
        suggestions["preload_skills"].sort(key=lambda x: x["priority"], reverse=True)
        suggestions["unload_skills"].sort(key=lambda x: x["priority"])
        
        return suggestions

# FastAPI Server with Enhanced Features
class EnhancedMCPServerV2:
    """Enhanced MCP Server v2 with dynamic lazy loading and self-optimization"""
    
    def __init__(self):
        self.config = ServerConfig()
        self.app = FastAPI(
            title="Enhanced MCP Server v2",
            description="Multi-Agent Orchestration Server with Dynamic Lazy Loading and Self-Optimization",
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
        self.skill_manager = EnhancedSkillManager()
        
        # Setup routes
        self._setup_routes()
        
        # Background tasks
        self.background_tasks = []
        
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/")
        async def root():
            return {"message": "Enhanced MCP Server v2 is running", "version": "2.0.0"}
        
        @self.app.get("/health")
        async def health_check():
            """Enhanced health check with optimization recommendations"""
            return self.telemetry.get_health_status()
        
        @self.app.get("/metrics")
        async def get_metrics():
            """Get comprehensive performance metrics"""
            return {
                "system_metrics": [asdict(m) for m in self.telemetry.metrics_history[-10:]],
                "skill_metrics": {k: asdict(v) for k, v in self.telemetry.skill_metrics.items()},
                "skills": {k: asdict(v) for k, v in self.skill_manager.skills.items()},
                "cache_stats": self.skill_manager.skill_cache.get_stats(),
                "optimization": self.telemetry.get_optimization_recommendations()
            }
        
        @self.app.post("/skills/discover")
        async def discover_skills():
            """Discover available skills with dependency analysis"""
            skills = self.skill_manager.discover_skills()
            return {
                "discovered_skills": skills, 
                "total": len(skills),
                "dependencies": {k: v.dependencies for k, v in self.skill_manager.skills.items()}
            }
        
        @self.app.post("/skills/execute")
        async def execute_skill(request: Dict[str, Any]):
            """Execute a skill with dynamic loading"""
            skill_name = request.get("skill_name")
            args = request.get("args", [])
            kwargs = request.get("kwargs", {})
            
            if not skill_name:
                raise HTTPException(status_code=400, detail="skill_name is required")
            
            try:
                result = await self.skill_manager.execute_skill(skill_name, *args, **kwargs)
                return {"success": True, "result": result}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/skills/optimize")
        async def optimize_skills():
            """Trigger skill optimization based on usage patterns"""
            suggestions = self.skill_manager.get_optimization_suggestions()
            
            # Preload high-priority skills
            for skill_info in suggestions["preload_skills"][:5]:  # Preload top 5
                try:
                    await self.skill_manager.load_skill_dynamically(skill_info["skill"])
                except Exception as e:
                    logger.warning(f"Failed to preload skill {skill_info['skill']}: {e}")
            
            # Unload low-priority skills
            for skill_info in suggestions["unload_skills"][:5]:  # Unload top 5
                try:
                    await self.skill_manager.unload_skill(skill_info["skill"])
                except Exception as e:
                    logger.warning(f"Failed to unload skill {skill_info['skill']}: {e}")
            
            return {
                "success": True,
                "optimization": suggestions,
                "message": "Skill optimization completed"
            }
        
        @self.app.get("/skills/status")
        async def get_skill_status():
            """Get detailed skill status and loading information"""
            return {
                "loaded_skills": list(self.skill_manager.loaded_skills),
                "total_skills": len(self.skill_manager.skills),
                "cache_stats": self.skill_manager.skill_cache.get_stats(),
                "skill_details": {
                    name: {
                        "status": skill.status.value,
                        "is_loaded": skill.is_loaded,
                        "execution_count": skill.execution_count,
                        "avg_execution_time": skill.avg_execution_time,
                        "priority_score": self.telemetry.calculate_priority_score(name),
                        "last_accessed": skill.last_accessed.isoformat() if skill.last_accessed else None
                    }
                    for name, skill in self.skill_manager.skills.items()
                }
            }
        
        @self.app.on_event("startup")
        async def startup_event():
            """Startup tasks"""
            # Start background monitoring and optimization
            self.background_tasks.append(
                asyncio.create_task(self._monitoring_loop())
            )
            self.background_tasks.append(
                asyncio.create_task(self._optimization_loop())
            )
            
            # Discover skills on startup
            self.skill_manager.discover_skills()
            
            logger.info("Enhanced MCP Server v2 started successfully")
        
        @self.app.on_event("shutdown")
        async def shutdown_event():
            """Shutdown tasks"""
            for task in self.background_tasks:
                task.cancel()
            
            logger.info("Enhanced MCP Server v2 shutting down")
    
    async def _monitoring_loop(self):
        """Background monitoring loop with enhanced metrics"""
        while True:
            try:
                # Collect system metrics
                self.telemetry.collect_system_metrics()
                
                # Clean up cache
                self.skill_manager.skill_cache.cleanup()
                
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
    
    async def _optimization_loop(self):
        """Background optimization loop"""
        while True:
            try:
                # Get optimization suggestions
                suggestions = self.skill_manager.get_optimization_suggestions()
                
                # Auto-preload high-priority skills
                for skill_info in suggestions["preload_skills"][:3]:  # Preload top 3
                    if skill_info["priority"] > 0.9:  # Very high priority
                        try:
                            await self.skill_manager.load_skill_dynamically(skill_info["skill"])
                        except Exception as e:
                            logger.warning(f"Failed to auto-preload skill {skill_info['skill']}: {e}")
                
                # Auto-unload low-priority skills
                for skill_info in suggestions["unload_skills"][:3]:  # Unload top 3
                    if skill_info["priority"] < 0.1:  # Very low priority
                        try:
                            await self.skill_manager.unload_skill(skill_info["skill"])
                        except Exception as e:
                            logger.warning(f"Failed to auto-unload skill {skill_info['skill']}: {e}")
                
                await asyncio.sleep(300)  # Run every 5 minutes
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Optimization loop error: {e}")
                await asyncio.sleep(60)
    
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
    
    parser = argparse.ArgumentParser(description="Enhanced MCP Server v2")
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
    server = EnhancedMCPServerV2()
    server.run()

if __name__ == "__main__":
    main()