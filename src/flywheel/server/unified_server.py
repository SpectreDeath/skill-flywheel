"""
Unified MCP Server Module

Consolidates Discovery, Tool Execution, and ML Optimization into a single production server.
"""

import asyncio
import logging
import os
import sqlite3
import time
from dataclasses import asdict
from typing import Any, Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import start_http_server

from flywheel.core.cache import AdvancedCache
from flywheel.core.containers import ContainerManager
from flywheel.core.ml_models import (
    MLModelManager,
    PredictivePreloader,
    AdaptiveCacheEviction,
)
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
    server.monitoring_task = asyncio.create_task(server._monitoring_loop())
    await server.skill_manager.discover_skills()
    logger.info("Unified Skill Flywheel Server started successfully")
    yield
    for task in server.background_tasks:
        task.cancel()
    logger.info("Unified Skill Flywheel Server shutting down")


# Constants for Discovery
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
DB_PATH = os.path.join(BASE_DIR, "data", "skill_registry.db")


class UnifiedMCPServer:
    """Unified MCP Server consolidating Discovery and Enhanced features"""

    def __init__(self):
        self.config = ServerConfig()
        self.app = FastAPI(
            title="Unified Skill Flywheel Server",
            description="""
            Consolidated Skill Discovery and Orchestration Server.
            
            - **Discovery**: SQLite-backed skill searching and domain listing.
            - **Execution**: Functional Python skill execution via MCP.
            - **Optimization**: ML-driven predictive loading and resource adaptive scaling.
            """,
            version="1.0.0 (Unified)",
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

        # Core Components
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

        # ML Optimization Components
        self.preloader = PredictivePreloader(self.ml_manager, self.skill_manager)
        self.cache_eviction = AdaptiveCacheEviction(self.ml_manager)

        self._setup_routes()
        self.background_tasks = []

        if self.config.config["monitoring"]["prometheus_port"]:
            try:
                start_http_server(self.config.config["monitoring"]["prometheus_port"])
            except Exception as e:
                logger.warning(f"Prometheus server failed to start: {e}")

    def get_db(self):
        """Get SQLite database connection"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def _setup_routes(self):
        """Setup unified API routes"""

        @self.app.get("/", tags=["General"])
        async def root():
            return {
                "message": "Unified Skill Flywheel Server is running",
                "version": "1.0.0",
            }

        # --- Discovery Routes (Ported from discovery_service.py) ---

        @self.app.get("/health", tags=["Health"])
        async def health_check():
            """Detailed health check combining telemetry and DB status"""
            telemetry_health = self.telemetry.get_advanced_health_status()
            try:
                with self.get_db() as db:
                    cursor = db.cursor()
                    cursor.execute("SELECT COUNT(*) FROM skills")
                    db_count = cursor.fetchone()[0]
                telemetry_health["database_accessible"] = True
                telemetry_health["active_skills_in_db"] = db_count
            except Exception as e:
                telemetry_health["database_accessible"] = False
                telemetry_health["database_error"] = str(e)

            return telemetry_health

        @self.app.get("/skills", tags=["Discovery"])
        async def list_skills(
            domain: str | None = None,
            limit: int = Query(100, ge=1, le=1000),
            offset: int = 0,
        ):
            """List skills from the SQLite registry"""
            try:
                with self.get_db() as db:
                    cursor = db.cursor()
                    query = "SELECT * FROM skills"
                    params = []
                    if domain:
                        query += " WHERE domain = ?"
                        params.append(domain)

                    query += " LIMIT ? OFFSET ?"
                    params.extend([limit, offset])

                    cursor.execute(query, params)
                    skills = [dict(row) for row in cursor.fetchall()]
                    return {
                        "skills": skills,
                        "limit": limit,
                        "offset": offset,
                        "count": len(skills),
                    }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database error: {e}")

        @self.app.get("/skills/search", tags=["Discovery"])
        async def search_skills(q: str = Query(..., min_length=2)):
            """Semantic/Text search for skills in the DB"""
            try:
                with self.get_db() as db:
                    cursor = db.cursor()
                    cursor.execute(
                        "SELECT * FROM skills WHERE name LIKE ? OR description LIKE ? OR purpose LIKE ?",
                        (f"%{q}%", f"%{q}%", f"%{q}%"),
                    )
                    results = [dict(row) for row in cursor.fetchall()]
                    return {"query": q, "results": results, "count": len(results)}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Search error: {e}")

        @self.app.get("/domains", tags=["Discovery"])
        async def list_domains():
            """List all unique domains and their skill counts"""
            try:
                with self.get_db() as db:
                    cursor = db.cursor()
                    cursor.execute(
                        "SELECT domain, COUNT(*) as count FROM skills GROUP BY domain"
                    )
                    domains = [dict(row) for row in cursor.fetchall()]
                    return {"domains": domains}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database error: {e}")

        # --- Execution & Optimization Routes (Ported from server.py) ---

        @self.app.post("/skills/execute", tags=["Execution"])
        async def execute_skill(request: Dict[str, Any]):
            skill_name = request.get("skill_name")
            args = request.get("args", [])
            kwargs = request.get("kwargs", {})

            if not skill_name:
                raise HTTPException(status_code=400, detail="skill_name is required")

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
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/metrics", tags=["Performance"])
        async def get_metrics():
            metrics = {
                "system_metrics": [
                    asdict(m) for m in self.telemetry.metrics_history[-10:]
                ],
                "skill_metrics": {
                    k: asdict(v) for k, v in self.telemetry.skill_metrics.items()
                },
                "cache_stats": self.skill_manager.skill_cache.get_stats(),
            }
            if self.telemetry.metrics_history:
                latest = self.telemetry.metrics_history[-1]
                metrics["ml_insights"] = {
                    "optimization_score": self.telemetry.resource_optimizer.calculate_utilization_score(
                        latest.cpu_usage, latest.memory_usage, latest.disk_usage
                    )
                }
            return metrics

        @self.app.post("/skills/optimize", tags=["Optimization"])
        async def optimize_skills():
            suggestions = self.telemetry.get_advanced_optimization_recommendations()
            # Trigger predictive preloading
            await self.preloader.preload_skills()
            return {"success": True, "optimization": suggestions}

        @self.app.get("/skills/predict", tags=["Optimization"])
        async def predict_skill_usage(skill_name: str):
            """Predict usage probability for a skill."""
            confidence = self.preloader.predict_next_usage(skill_name)
            return {"skill": skill_name, "usage_probability": confidence}

        @self.app.get("/skills/preload", tags=["Optimization"])
        async def get_preload_candidates():
            """Get skills recommended for preloading."""
            candidates = self.preloader.get_skills_to_preload()
            return {"candidates": candidates, "count": len(candidates)}

        @self.app.post("/skills/evolve", tags=["Evolution"])
        async def evolve_skills(request: Dict[str, Any]):
            """Trigger skill evolution for a given skill group.

            Request body:
            - group: Name of the evolvable skill group (required)
            - iterations: Number of evolution iterations (default: 10)
            - population_size: Population size (default: 5)
            - output_dir: Output directory for results (default: "evolution_output")
            """
            from flywheel.evolution.runner import create_runner, list_evolvable_groups

            group_name = request.get("group")
            if not group_name:
                raise HTTPException(
                    status_code=400,
                    detail="group is required. Use GET /skills/evolve/groups to list available groups.",
                )

            available_groups = list_evolvable_groups()
            if group_name not in available_groups:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unknown group: {group_name}. Available: {', '.join(available_groups)}",
                )

            iterations = request.get("iterations", 10)
            population_size = request.get("population_size", 5)
            output_dir = request.get("output_dir", "evolution_output")

            from flywheel.evolution.config import EvolutionConfig

            config = EvolutionConfig(
                population_size=population_size,
                num_parents_per_iteration=min(3, population_size - 1),
                max_iterations=iterations,
            )

            try:
                runner = create_runner(
                    group_name=group_name,
                    config=config,
                    output_dir=output_dir,
                )

                runner.initialize()
                results = runner.run_all(iterations=iterations)

                best_genome = runner.get_best_genome()
                best_fitness = runner.get_best_fitness()
                stats = runner.get_statistics()

                return {
                    "success": True,
                    "group": group_name,
                    "iterations_completed": len(results),
                    "best_score": best_fitness.score if best_fitness else None,
                    "best_genome": best_genome.model_dump() if best_genome else None,
                    "statistics": stats,
                    "output_dir": output_dir,
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Evolution failed: {str(e)}",
                )

        @self.app.get("/skills/evolve/groups", tags=["Evolution"])
        async def list_evolve_groups():
            """List all available evolvable skill groups."""
            from flywheel.evolution.runner import list_evolvable_groups

            groups = list_evolvable_groups()
            return {"groups": groups, "count": len(groups)}

        @self.app.post("/skills/orchestrate", tags=["Orchestration"])
        async def orchestrate_agents(request: Dict[str, Any]):
            """Orchestrate multi-agent workflows using LangChain/LangGraph.

            Request body:
            - task_description: Description of the task (required)
            - agents: List of agent configs (required)
            - framework: Framework to use ("autogen", "langchain", "langgraph", "crewai") (default: "langgraph")
            - context: Optional initial context
            """
            from flywheel.core.agent_orchestration import (
                AgentOrchestrator,
                AgentConfig,
                AgentFramework,
            )

            task_description = request.get("task_description")
            agents_data = request.get("agents", [])
            framework_str = request.get("framework", "langgraph")
            initial_context = request.get("context", {})

            if not task_description:
                raise HTTPException(
                    status_code=400,
                    detail="task_description is required",
                )

            if not agents_data:
                raise HTTPException(
                    status_code=400,
                    detail="agents list is required",
                )

            try:
                framework = AgentFramework(framework_str.lower())
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid framework: {framework_str}. Use: autogen, langchain, langgraph, crewai",
                )

            orchestrator = AgentOrchestrator()
            agent_names = []

            for agent_data in agents_data:
                agent_config = AgentConfig(
                    name=agent_data.get("name", "agent"),
                    role=agent_data.get("role", "Worker"),
                    goal=agent_data.get("goal", task_description),
                    backstory=agent_data.get("backstory", ""),
                    framework=framework,
                    domain=agent_data.get("domain"),
                )
                orchestrator.register_agent(agent_config)
                agent_names.append(agent_config.name)

            try:
                result = await orchestrator.orchestrate_task(
                    task_id=f"api_{int(time.time())}",
                    agents=agent_names,
                    task_description=task_description,
                    initial_context=initial_context,
                )

                return {
                    "success": result.success,
                    "task_id": result.task_id,
                    "framework": result.framework.value,
                    "agents_used": result.agents_used,
                    "execution_time": result.execution_time,
                    "results": result.results,
                    "error": result.error,
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Orchestration failed: {str(e)}",
                )

        @self.app.post("/skills/scan", tags=["Security"])
        async def scan_skill_security(request: Dict[str, Any]):
            """Scan a skill for security vulnerabilities.

            Request body:
            - skill_path: Path to the skill file (required)
            """
            from flywheel.core.enhanced_security import scan_skill_security
            from pathlib import Path

            skill_path = request.get("skill_path")
            if not skill_path:
                raise HTTPException(
                    status_code=400,
                    detail="skill_path is required",
                )

            try:
                path = Path(skill_path)
                if not path.exists():
                    raise HTTPException(
                        status_code=404,
                        detail=f"Skill file not found: {skill_path}",
                    )

                scan_result = await scan_skill_security(path)

                return {
                    "success": True,
                    "scan_id": scan_result.scan_id,
                    "skill_id": scan_result.skill_id,
                    "security_level": scan_result.security_level.value,
                    "vulnerabilities": scan_result.vulnerabilities,
                    "compliance_issues": scan_result.compliance_issues,
                    "recommendations": scan_result.recommendations,
                    "risk_score": scan_result.risk_score,
                    "ml_threat_score": scan_result.ml_threat_score,
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Security scan failed: {str(e)}",
                )

        @self.app.get("/skills/scan/all", tags=["Security"])
        async def scan_all_skills():
            """Scan all skills in the skills directory for security vulnerabilities."""
            from flywheel.core.enhanced_security import scan_skill_security
            from pathlib import Path

            skills_dir = Path("src/flywheel/skills")
            if not skills_dir.exists():
                raise HTTPException(
                    status_code=404,
                    detail="Skills directory not found",
                )

            results = []
            skill_files = list(skills_dir.rglob("*.py"))

            for skill_file in skill_files[:10]:  # Limit to 10 skills for performance
                try:
                    scan_result = await scan_skill_security(skill_file)
                    results.append(
                        {
                            "skill_id": scan_result.skill_id,
                            "security_level": scan_result.security_level.value,
                            "risk_score": scan_result.risk_score,
                            "vulnerability_count": len(scan_result.vulnerabilities),
                        }
                    )
                except Exception as e:
                    results.append(
                        {
                            "skill_id": skill_file.stem,
                            "error": str(e),
                        }
                    )

            return {
                "success": True,
                "total_scanned": len(results),
                "results": results,
            }

        @self.app.get("/security/summary", tags=["Security"])
        async def get_security_summary(days: int = Query(7, ge=1, le=30)):
            """Get security monitoring summary."""
            from flywheel.core.enhanced_security import get_security_summary

            try:
                summary = get_security_summary(days)
                return {"success": True, "summary": summary}
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to get security summary: {str(e)}",
                )

    async def _monitoring_loop(self):
        """Unified background monitoring"""
        while True:
            try:
                self.telemetry.collect_advanced_metrics()
                await asyncio.sleep(
                    self.config.config["monitoring"]["metrics_interval"]
                )
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Monitoring loop error: {str(e)}")
                await asyncio.sleep(10)

    def run(self):
        """Run the unified server"""
        config = self.config.config["server"]
        logger.info(f"Starting server on {config['host']}:{config['port']}")
        uvicorn.run(
            self.app, host=config["host"], port=config["port"], log_level="info"
        )


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Unified Skill Flywheel Server")
    parser.add_argument("--host", default=None, help="Server host")
    parser.add_argument("--port", type=int, default=None, help="Server port")
    args = parser.parse_args()

    server = UnifiedMCPServer()
    if args.host:
        server.config.config["server"]["host"] = args.host
    if args.port:
        server.config.config["server"]["port"] = args.port

    server.run()


if __name__ == "__main__":
    main()
