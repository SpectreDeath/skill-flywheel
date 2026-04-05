from dataclasses import asdict
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from flywheel.server.config import ServerConfig

router = APIRouter(prefix="", tags=["Health", "Performance"])

config = ServerConfig()


def get_telemetry():
    """Get telemetry manager instance"""
    from flywheel.core.telemetry import AdvancedTelemetryManager
    from flywheel.core.ml_models import MLModelManager
    from flywheel.core.resource_optimizer import ResourceOptimizer

    ml_manager = MLModelManager(config.config)
    resource_optimizer = ResourceOptimizer(config.config)
    return AdvancedTelemetryManager(config.config, ml_manager, resource_optimizer)


def get_db():
    """Get SQLite database connection"""
    import sqlite3

    db_path = config.config.get("database", {}).get("path", "data/skill_registry.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@router.get("/health")
async def health_check():
    """Detailed health check combining telemetry and DB status"""
    telemetry = get_telemetry()
    telemetry_health = telemetry.get_advanced_health_status()
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM skills")
            db_count = cursor.fetchone()[0]
        telemetry_health["database_accessible"] = True
        telemetry_health["active_skills_in_db"] = db_count
    except Exception as e:
        telemetry_health["database_accessible"] = False
        telemetry_health["database_error"] = str(e)

    return telemetry_health


@router.get("/metrics")
async def get_metrics():
    """Get performance metrics from telemetry"""
    telemetry = get_telemetry()

    try:
        metrics = {
            "history": [asdict(m) for m in telemetry.metrics_history[-10:]],
            "skill_metrics": {k: asdict(v) for k, v in telemetry.skill_metrics.items()},
        }

        if telemetry.metrics_history:
            latest = telemetry.metrics_history[-1]
            metrics["system"] = {
                "cpu_usage": latest.cpu_usage,
                "memory_usage": latest.memory_usage,
                "disk_usage": latest.disk_usage,
                "optimization_score": telemetry.resource_optimizer.calculate_utilization_score(
                    latest.cpu_usage, latest.memory_usage, latest.disk_usage
                ),
            }

        metrics["optimization"] = telemetry.get_advanced_optimization_recommendations()

        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics error: {e}")
