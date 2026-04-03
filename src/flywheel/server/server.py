"""
Enhanced MCP Server Module

Contains EnhancedMCPServerV3 class with advanced ML-driven optimization.
"""

import asyncio
import logging
import os
import sys
import time
from dataclasses import asdict
from typing import Any, Dict

import uvicorn
from celery import Celery
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import start_http_server

from flywheel.core.cache import AdvancedCache
from flywheel.core.containers import ContainerManager
from flywheel.core.ml_models import MLModelManager
from flywheel.core.resource_optimizer import ResourceOptimizer
from flywheel.core.skills import EnhancedSkillManager
from flywheel.core.telemetry import (
    REQUEST_COUNT,
    REQUEST_DURATION,
    AdvancedTelemetryManager,
)

from flywheel.server.config import ServerConfig

logger = logging.getLogger(__name__)


from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    server = app.state.server
    server.background_tasks = []
    server.background_tasks.append(
        asyncio.create_task(server._advanced_monitoring_loop())
    )
    server.background_tasks.append(asyncio.create_task(server._ml_optimization_loop()))
    server.background_tasks.append(
        asyncio.create_task(server._container_scaling_loop())
    )
    await server.skill_manager.discover_skills()
    logger.info("Enhanced MCP Server v3 started successfully")
    yield
    for task in server.background_tasks:
        task.cancel()
    logger.info("Enhanced MCP Server v3 shutting down")


class EnhancedMCPServerV3:
    """Enhanced MCP Server v3 with advanced ML-driven optimization"""

    def __init__(self):
        self.config = ServerConfig()
        self.app = FastAPI(
            title="Enhanced MCP Server v3",
            description="""
            Advanced Multi-Agent Orchestration Server with ML-Driven Optimization.
            
            ## Features
            
            - **ML-driven predictive loading**: Uses time-series analysis to predict skill usage
            - **Resource-aware optimization**: Real-time adaptation to system resources
            - **Multi-agent orchestration**: Intelligent task distribution across agents
            - **Container optimization**: Docker/Kubernetes-based scaling
            - **Prometheus metrics**: Built-in observability
            """,
            version="3.0.0",
            docs_url="/docs",
            redoc_url="/redoc",
            openapi_url="/openapi.json",
            lifespan=lifespan,
        )

        self.app.state.server = self

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.config["server"]["cors_origins"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.ml_manager = MLModelManager(self.config.config)
        self.resource_optimizer = ResourceOptimizer(self.config.config)
        self.telemetry = AdvancedTelemetryManager(
            self.config.config, self.ml_manager, self.resource_optimizer
        )
        self.cache = AdvancedCache(self.config.config)
        self.container_manager = ContainerManager(self.config.config)

        self.skill_manager = EnhancedSkillManager(
            config=self.config.config,
            cache=self.cache,
            telemetry=self.telemetry,
            container_manager=self.container_manager,
        )

        self.celery_app = Celery(
            "enhanced_mcp_server_v3",
            broker=self.config.config["celery"]["broker_url"],
            backend=self.config.config["celery"]["result_backend"],
        )

        self._setup_routes()

        self.background_tasks = []

        if self.config.config["monitoring"]["prometheus_port"]:
            start_http_server(self.config.config["monitoring"]["prometheus_port"])

    def _setup_routes(self):
        """Setup advanced API routes"""

        @self.app.get("/")
        async def root():
            return {"message": "Enhanced MCP Server v3 is running", "version": "3.0.0"}

        @self.app.get("/health")
        async def health_check():
            return self.telemetry.get_advanced_health_status()

        @self.app.get("/metrics")
        async def get_metrics():
            return {
                "system_metrics": [
                    asdict(m) for m in self.telemetry.metrics_history[-10:]
                ],
                "skill_metrics": {
                    k: asdict(v) for k, v in self.telemetry.skill_metrics.items()
                },
                "skills": {k: asdict(v) for k, v in self.skill_manager.skills.items()},
                "cache_stats": self.skill_manager.skill_cache.get_stats(),
                "optimization": self.telemetry.get_advanced_optimization_recommendations(),
                "ml_insights": {
                    "model_accuracy": self.telemetry._calculate_ml_accuracy(),
                    "anomaly_count": len(
                        [
                            m
                            for m in self.telemetry.skill_metrics.values()
                            if m.anomaly_detected
                        ]
                    ),
                    "optimization_score": self.telemetry.resource_optimizer.calculate_utilization_score(
                        self.telemetry.metrics_history[-1].cpu_usage
                        if self.telemetry.metrics_history
                        else 0,
                        self.telemetry.metrics_history[-1].memory_usage
                        if self.telemetry.metrics_history
                        else 0,
                        self.telemetry.metrics_history[-1].disk_usage
                        if self.telemetry.metrics_history
                        else 0,
                    ),
                },
            }

        @self.app.post("/skills/discover")
        async def discover_skills():
            skills = await self.skill_manager.discover_skills()
            return {
                "discovered_skills": skills,
                "total": len(skills),
                "dependencies": {
                    k: v.dependencies for k, v in self.skill_manager.skills.items()
                },
                "ml_prioritization": [],
            }

        @self.app.post("/skills/execute")
        async def execute_skill(request: Dict[str, Any]):
            skill_name = request.get("skill_name")
            args = request.get("args", [])
            kwargs = request.get("kwargs", {})

            if not skill_name:
                raise HTTPException(status_code=400, detail="skill_name is required")

            if skill_name not in self.skill_manager.skills:
                raise HTTPException(
                    status_code=400,
                    detail=f"skill_name '{skill_name}' is not registered. Available skills: {list(self.skill_manager.skills.keys())[:20]}",
                )

            REQUEST_COUNT.labels(method="POST", endpoint="/skills/execute").inc()

            start_time = time.time()
            try:
                result = await self.skill_manager.execute_skill(
                    skill_name, *args, **kwargs
                )
                duration = time.time() - start_time
                REQUEST_DURATION.observe(duration)

                return {"success": True, "result": result, "execution_time": duration}
            except Exception as e:
                duration = time.time() - start_time
                REQUEST_DURATION.observe(duration)
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/skills/optimize")
        async def optimize_skills():
            suggestions = (
                self.skill_manager.telemetry.get_advanced_optimization_recommendations()
            )

            for skill_info in suggestions["skills_to_preload"][:5]:
                try:
                    await self.skill_manager.load_skill_dynamically(skill_info["skill"])
                except Exception as e:
                    logger.warning(
                        f"Failed to preload skill {skill_info['skill']}: {str(e)}"
                    )

            for skill_info in suggestions["skills_to_unload"][:5]:
                try:
                    await self.skill_manager.unload_skill(skill_info["skill"])
                except Exception as e:
                    logger.warning(
                        f"Failed to unload skill {skill_info['skill']}: {str(e)}"
                    )

            return {
                "success": True,
                "optimization": suggestions,
                "message": "Advanced skill optimization completed",
            }

        @self.app.get("/skills/status")
        async def get_skill_status():
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
                        "priority_score": self.telemetry.calculate_advanced_priority_score(
                            name
                        ),
                        "predicted_usage": self.telemetry.skill_metrics[
                            name
                        ].predicted_usage
                        if name in self.telemetry.skill_metrics
                        else 0.0,
                        "anomaly_detected": self.telemetry.skill_metrics[
                            name
                        ].anomaly_detected
                        if name in self.telemetry.skill_metrics
                        else False,
                        "last_accessed": skill.last_accessed.isoformat()
                        if skill.last_accessed
                        else None,
                    }
                    for name, skill in self.skill_manager.skills.items()
                },
            }

    async def _advanced_monitoring_loop(self):
        """Advanced monitoring loop with ML analytics"""
        while True:
            try:
                self.telemetry.collect_advanced_metrics()

                if hasattr(self.skill_manager.skill_cache, "cleanup"):
                    self.skill_manager.skill_cache.cleanup()

                health = self.telemetry.get_advanced_health_status()
                if health["status"] != "healthy":
                    logger.warning(f"System health warning: {health}")

                await asyncio.sleep(
                    self.config.config["monitoring"]["metrics_interval"]
                )
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Advanced monitoring loop error: {str(e)}")
                await asyncio.sleep(10)

    async def _ml_optimization_loop(self):
        """ML-based optimization loop"""
        while True:
            try:
                suggestions = self.skill_manager.telemetry.get_advanced_optimization_recommendations()

                for skill_info in suggestions["skills_to_preload"][:3]:
                    if (
                        skill_info["priority"] > 0.9
                        and skill_info["ml_confidence"] > 0.8
                    ):
                        try:
                            await self.skill_manager.load_skill_dynamically(
                                skill_info["skill"]
                            )
                        except Exception as e:
                            logger.warning(
                                f"Failed to auto-preload skill {skill_info['skill']}: {e}"
                            )

                for skill_info in suggestions["skills_to_unload"][:3]:
                    if skill_info["priority"] < 0.1:
                        try:
                            await self.skill_manager.unload_skill(skill_info["skill"])
                        except Exception as e:
                            logger.warning(
                                f"Failed to auto-unload skill {skill_info['skill']}: {e}"
                            )

                await asyncio.sleep(300)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"ML optimization loop error: {e}")
                await asyncio.sleep(60)

    async def _container_scaling_loop(self):
        """Container auto-scaling loop"""
        while True:
            try:
                latest_metrics = (
                    self.telemetry.metrics_history[-1]
                    if self.telemetry.metrics_history
                    else None
                )
                if latest_metrics:
                    current_load = latest_metrics.resource_utilization_score

                    await self.skill_manager.container_manager.scale_containers(
                        current_load
                    )

                await asyncio.sleep(60)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Container scaling loop error: {e}")
                await asyncio.sleep(60)

    def run(self):
        """Run the advanced server"""
        config = self.config.config["server"]
        uvicorn.run(
            self.app,
            host=config["host"],
            port=config["port"],
            debug=config["debug"],
            log_level="info",
            workers=config.get("workers", 1),
        )


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Enhanced MCP Server v3")
    parser.add_argument(
        "--config", default="mcp_config.yaml", help="Configuration file path"
    )
    parser.add_argument("--host", default=None, help="Server host")
    parser.add_argument("--port", type=int, default=None, help="Server port")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--prometheus-port", type=int, default=8001, help="Prometheus metrics port"
    )

    args = parser.parse_args()

    if args.config:
        os.environ["MCP_CONFIG"] = args.config
    if args.host:
        os.environ["MCP_HOST"] = args.host
    if args.port:
        os.environ["MCP_PORT"] = str(args.port)
    if args.debug:
        os.environ["MCP_DEBUG"] = "true"
    if args.prometheus_port:
        os.environ["PROMETHEUS_PORT"] = str(args.prometheus_port)

    server = EnhancedMCPServerV3()
    server.run()


if __name__ == "__main__":
    main()
