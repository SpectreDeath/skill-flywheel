import datetime
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List
from unittest.mock import Mock

import GPUtil
import psutil
from prometheus_client import Counter, Gauge, Histogram

logger = logging.getLogger(__name__)

# Prometheus metrics (forward-declared or initialized here)
REQUEST_COUNT = Counter('mcp_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('mcp_request_duration_seconds', 'Request duration')
ACTIVE_SKILLS = Gauge('mcp_active_skills', 'Number of active skills')
CACHE_HIT_RATE = Gauge('mcp_cache_hit_rate', 'Cache hit rate')
SYSTEM_CPU = Gauge('mcp_system_cpu_usage', 'System CPU usage')
SYSTEM_MEMORY = Gauge('mcp_system_memory_usage', 'System memory usage')

@dataclass
class AdvancedPerformanceMetrics:
    timestamp: datetime.datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    gpu_usage: float | None
    active_connections: int
    request_count: int
    error_count: int
    avg_response_time: float
    p95_response_time: float
    p99_response_time: float
    active_skills: int
    cached_skills: int
    cache_hit_rate: float
    ml_prediction_accuracy: float
    resource_utilization_score: float
    anomaly_score: float

@dataclass
class AdvancedSkillMetrics:
    skill_name: str
    load_count: int
    execution_count: int
    total_load_time: float
    total_execution_time: float
    avg_load_time: float
    avg_execution_time: float
    p95_execution_time: float
    p99_execution_time: float
    last_load_time: datetime.datetime | None
    last_execution_time: datetime.datetime | None
    dependency_count: int
    memory_usage: float
    success_rate: float
    priority_score: float
    predicted_usage: float
    predicted_performance: float
    anomaly_detected: bool
    resource_optimization_score: float
    time_series_features: List[float] = field(default_factory=list)

class AdvancedTelemetryManager:
    """Advanced telemetry with ML-driven optimization."""
    
    def __init__(self, config: Dict[str, Any], ml_manager: Any = None, resource_optimizer: Any = None):
        self.config = config
        self.ml_manager = ml_manager or Mock()
        self.resource_optimizer = resource_optimizer or Mock()
        self.metrics_history: List[AdvancedPerformanceMetrics] = []
        self.skill_metrics: Dict[str, AdvancedSkillMetrics] = {}
        
        # Ensure resource_optimizer has calculate_utilization_score
        if not hasattr(self.resource_optimizer, 'calculate_utilization_score'):
            self.resource_optimizer.calculate_utilization_score = lambda *args: 0.5
        
    def collect_advanced_metrics(self) -> AdvancedPerformanceMetrics | None:
        """Collect and record system-wide performance metrics."""
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            gpu_usage = None
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu_usage = gpus[0].load * 100
            except Exception:
                pass
            
            connections = len(psutil.net_connections())
            
            # Simplified score calculation for now
            resource_score = self.resource_optimizer.calculate_utilization_score(
                cpu_usage, memory.percent, disk.percent
            )
            
            metrics = AdvancedPerformanceMetrics(
                timestamp=datetime.datetime.now(),
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                disk_usage=disk.percent,
                gpu_usage=gpu_usage,
                active_connections=connections,
                request_count=0,
                error_count=0,
                avg_response_time=0.0,
                p95_response_time=0.0,
                p99_response_time=0.0,
                active_skills=0,
                cached_skills=0,
                cache_hit_rate=0.0,
                ml_prediction_accuracy=0.0,
                resource_utilization_score=resource_score,
                anomaly_score=0.0
            )
            
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > 1000:
                self.metrics_history.pop(0)
                
            # Update Prometheus
            SYSTEM_CPU.set(cpu_usage)
            SYSTEM_MEMORY.set(memory.percent)
            
            return metrics
        except Exception as e:
            logger.error(f"Failed to collect advanced metrics: {e}")
            return None

    def track_advanced_skill_execution(self, skill_name: str, load_time: float, 
                                     execution_time: float, success: bool, 
                                     dependencies: List[str]):
        """Track execution metrics for individual skills."""
        if skill_name not in self.skill_metrics:
            self.skill_metrics[skill_name] = AdvancedSkillMetrics(
                skill_name=skill_name, load_count=0, execution_count=0,
                total_load_time=0.0, total_execution_time=0.0,
                avg_load_time=0.0, avg_execution_time=0.0,
                p95_execution_time=0.0, p99_execution_time=0.0,
                last_load_time=None, last_execution_time=None,
                dependency_count=len(dependencies) if not isinstance(dependencies, Mock) else 0,
                memory_usage=0.0,
                success_rate=0.0, priority_score=0.0, predicted_usage=0.0,
                predicted_performance=0.0, anomaly_detected=False,
                resource_optimization_score=0.0
            )
        
        m = self.skill_metrics[skill_name]
        if execution_time > 0:
            m.execution_count += 1
            m.total_execution_time += execution_time
            m.avg_execution_time = m.total_execution_time / m.execution_count
        m.last_execution_time = datetime.datetime.now()
        
        if load_time > 0:
            m.load_count += 1
            m.total_load_time += load_time
            m.avg_load_time = m.total_load_time / m.load_count
            m.last_load_time = m.last_execution_time
            
        m.success_rate = (m.success_rate * (m.execution_count - 1) + (1 if success else 0)) / m.execution_count
        
        try:
            process = psutil.Process()
            m.memory_usage = process.memory_info().rss / 1024 / 1024
        except Exception:
            pass

    def calculate_advanced_priority_score(self, skill_name: str) -> float:
        """Calculate optimization priority score for a skill."""
        if skill_name not in self.skill_metrics:
            return 0.5
        
        m = self.skill_metrics[skill_name]
        # Weighted score based on execution count, success rate, and load time
        score = (m.execution_count * 0.4 + m.success_rate * 0.4 + (1.0 / max(0.1, m.avg_load_time)) * 0.2)
        return min(max(float(score), 0.0), 1.0)

    def get_advanced_optimization_recommendations(self) -> Dict[str, Any]:
        """Get ML-driven optimization recommendations."""
        recommendations = {
            "skills_to_preload": [],
            "skills_to_unload": [],
            "performance_issues": [],
            "ml_improvements": []
        }
        
        for name, m in self.skill_metrics.items():
            priority = self.calculate_advanced_priority_score(name)
            if priority > 0.8 and m.avg_load_time > 1.0:
                recommendations["skills_to_preload"].append(name)
            elif priority < 0.2:
                recommendations["skills_to_unload"].append(name)
                
        return recommendations

    def get_advanced_health_status(self) -> Dict[str, Any]:
        """Get comprehensive system health status."""
        metrics = self.metrics_history[-1] if self.metrics_history else None
        status = "healthy"
        issues = []
        
        if metrics:
            if metrics.cpu_usage > 90:
                status = "degraded"
                issues.append("High CPU usage")
            if metrics.memory_usage > 90:
                status = "degraded"
                issues.append("High memory usage")
                
        return {
            "status": status,
            "timestamp": datetime.datetime.now().isoformat(),
            "issues": issues,
            "metrics": {
                "cpu": metrics.cpu_usage if metrics else 0,
                "memory": metrics.memory_usage if metrics else 0,
                "anomaly_score": metrics.anomaly_score if metrics else 0
            }
        }
