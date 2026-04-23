"""
Shared dependencies for the Skill Flywheel MCP server.

This module provides singleton instances and factory functions for
common server dependencies like the skill registry loader, performance
monitor, and telemetry logger.
"""

import datetime
import json
import logging
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# Configuration from environment or defaults
REGISTRY_FILE = Path(os.environ.get("REGISTRY_FILE", "/app/skill_registry.json"))
SKILLS_DIR = Path(os.environ.get("SKILLS_DIR", "/app/domains"))
TELEMETRY_LOG = Path(os.environ.get("TELEMETRY_LOG", "/app/telemetry/usage_log.jsonl"))
MCP_DOMAINS = (
    os.environ.get("MCP_DOMAINS", "").split(",")
    if os.environ.get("MCP_DOMAINS")
    else []
)


class MetricType(Enum):
    """Types of performance metrics tracked by the monitor."""

    EXECUTION_TIME = "execution_time"
    SUCCESS_RATE = "success_rate"
    QUALITY_SCORE = "quality_score"
    RESOURCE_USAGE = "resource_usage"


@dataclass
class PerformanceMetric:
    """A single performance metric entry."""

    skill_id: str
    metric_type: MetricType
    value: float
    timestamp: datetime.datetime
    context: Dict[str, Any]


class PerformanceMonitor:
    """
    Monitors and tracks performance metrics for skills and agents.

    This class maintains an in-memory record of all performance metrics
    and provides aggregation methods for querying skill statistics.
    """

    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.skill_stats: Dict[str, Dict[str, Any]] = {}

    def record_metric(
        self,
        skill_id: str,
        metric_type: MetricType,
        value: float,
        context: Dict[str, Any] = None,
    ):
        """Record a performance metric."""
        # IMPLEMENTATION: See enhanced_mcp_server.py:80-110
        metric = PerformanceMetric(
            skill_id=skill_id,
            metric_type=metric_type,
            value=value,
            timestamp=datetime.datetime.now(),
            context=context or {},
        )
        self.metrics.append(metric)

        if skill_id not in self.skill_stats:
            self.skill_stats[skill_id] = {
                "execution_time_count": 0,
                "total_time": 0,
                "success_rate_count": 0,
                "success_count": 0,
                "quality_scores": [],
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
        # IMPLEMENTATION: See enhanced_mcp_server.py:112-129
        if skill_id not in self.skill_stats:
            return {"error": f"No metrics found for skill {skill_id}"}

        stats = self.skill_stats[skill_id]
        avg_time = (
            stats["total_time"] / stats["execution_time_count"]
            if stats["execution_time_count"] > 0
            else 0
        )
        success_rate = (
            stats["success_count"] / stats["success_rate_count"]
            if stats["success_rate_count"] > 0
            else 0
        )
        avg_quality = (
            sum(stats["quality_scores"]) / len(stats["quality_scores"])
            if stats["quality_scores"]
            else 0
        )

        return {
            "skill_id": skill_id,
            "total_executions": stats["execution_time_count"],
            "average_execution_time": avg_time,
            "success_rate": success_rate,
            "average_quality_score": avg_quality,
            "last_execution": max(
                [m.timestamp for m in self.metrics if m.skill_id == skill_id],
                default=None,
            ),
        }


# =============================================================================
# Singleton Instances
# =============================================================================

_performance_monitor: PerformanceMonitor | None = None
_skill_registry: List[Dict[str, Any]] | None = None


def get_performance_monitor() -> PerformanceMonitor:
    """
    Get the singleton PerformanceMonitor instance.

    Returns:
        The global PerformanceMonitor instance.
    """
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor


def get_skill_registry() -> List[Dict[str, Any]]:
    """
    Load and cache the skill registry.

    Returns:
        List of skill dictionaries from the registry file.
    """
    # IMPLEMENTATION: See enhanced_mcp_server.py:151-162
    global _skill_registry
    if _skill_registry is not None:
        return _skill_registry

    if not REGISTRY_FILE.exists():
        logger.error(f"Registry file not found at {REGISTRY_FILE}")
        return []

    try:
        with open(REGISTRY_FILE, encoding="utf-8") as f:
            _skill_registry = json.load(f)
        return _skill_registry
    except Exception as e:
        logger.error(f"Error loading registry: {e}")
        return []


def reload_skill_registry() -> List[Dict[str, Any]]:
    """Force reload the skill registry from disk."""
    global _skill_registry
    _skill_registry = None
    return get_skill_registry()


def filter_skills_by_domain(skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter skills by configured domains."""
    # IMPLEMENTATION: See enhanced_mcp_server.py:164-168
    if not MCP_DOMAINS:
        return skills
    return [skill for skill in skills if skill.get("domain") in MCP_DOMAINS]


def log_skill_usage(
    skill_id: str, request: str, duration: float = 0, status: str = "success"
) -> None:
    """
    Log skill usage to the telemetry file.

    Args:
        skill_id: The ID of the skill that was executed.
        request: The user request that was processed.
        duration: How long the execution took in seconds.
        status: Status of the execution (success, error, etc.)
    """
    # IMPLEMENTATION: See enhanced_mcp_server.py:134-149
    try:
        TELEMETRY_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "skill": skill_id,
            "request_preview": request[:100] if request else "",
            "duration": duration,
            "status": status,
            "server": os.environ.get("MCP_SERVER_NAME", "SkillFlywheel"),
        }
        with open(TELEMETRY_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        logger.error(f"Telemetry logging error: {e}")


# =============================================================================
# Dependency Factories
# =============================================================================


def skill_registry_loader() -> List[Dict[str, Any]]:
    """
    Factory function for dependency injection.

    Returns:
        The skill registry loader function.
    """
    return get_skill_registry()


def telemetry_logger() -> callable:
    """
    Factory function for dependency injection.

    Returns:
        The telemetry logging function.
    """

if __name__ == "__main__":
    return log_skill_usage