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
        )

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
            return {"message": "Unified Skill Flywheel Server is running", "version": "1.0.0"}

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
            domain: str = None, 
            limit: int = Query(100, ge=1, le=1000), 
            offset: int = 0
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
                    return {"skills": skills, "limit": limit, "offset": offset, "count": len(skills)}
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
                        (f"%{q}%", f"%{q}%", f"%{q}%")
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
                    cursor.execute("SELECT domain, COUNT(*) as count FROM skills GROUP BY domain")
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
                result = await self.skill_manager.execute_skill(skill_name, *args, **kwargs)
                duration = time.time() - start_time
                REQUEST_DURATION.observe(duration)
                return {"success": True, "result": result, "execution_time": duration}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/metrics", tags=["Performance"])
        async def get_metrics():
            metrics = {
                "system_metrics": [asdict(m) for m in self.telemetry.metrics_history[-10:]],
                "skill_metrics": {k: asdict(v) for k, v in self.telemetry.skill_metrics.items()},
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
            # In a real implementation, this would trigger background preloading
            return {"success": True, "optimization": suggestions}

        # --- Lifecycle Events ---

        @self.app.on_event("startup")
        async def startup_event():
            self.background_tasks.append(asyncio.create_task(self._monitoring_loop()))
            await self.skill_manager.discover_skills()
            logger.info("Unified Skill Flywheel Server started successfully")

        @self.app.on_event("shutdown")
        async def shutdown_event():
            for task in self.background_tasks:
                task.cancel()
            logger.info("Unified Skill Flywheel Server shutting down")

    async def _monitoring_loop(self):
        """Unified background monitoring"""
        while True:
            try:
                self.telemetry.collect_advanced_metrics()
                await asyncio.sleep(self.config.config["monitoring"]["metrics_interval"])
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Monitoring loop error: {str(e)}")
                await asyncio.sleep(10)

    def run(self):
        """Run the unified server"""
        config = self.config.config["server"]
        logger.info(f"Starting server on {config['host']}:{config['port']}")
        uvicorn.run(self.app, host=config["host"], port=config["port"], log_level="info")

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
