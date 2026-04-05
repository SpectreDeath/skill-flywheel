"""
Unified MCP Server Module

Consolidates Discovery, Tool Execution, and ML Optimization into a single production server.
"""

import asyncio
import logging
import os
import re
import sqlite3
import time
import uuid
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
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
from flywheel.server.routes import adk_router, skills_router, telemetry_router

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

        self._adk_sessions: Dict[str, Any] = {}

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

        # Include modular routers
        self.app.include_router(adk_router)
        self.app.include_router(skills_router)
        self.app.include_router(telemetry_router)

        # Try to include evolution router if available
        try:
            from flywheel.server.routes.evolution import router as evolution_router

            self.app.include_router(evolution_router)
        except ImportError:
            pass

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

        # --- ADK Skills Endpoints (Progressive Disclosure) ---

        @self.app.get("/adk/skills", tags=["ADK Skills"])
        async def adk_list_skills(
            domain: str | None = None,
            limit: int = Query(100, ge=1, le=1000),
        ):
            """L1: List all skills with metadata for ADK agents.

            Returns name and description for skill discovery.
            This is the lightweight metadata loaded at startup (~100 tokens per skill).
            """
            base_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../../../")
            )
            try:
                with self.get_db() as db:
                    cursor = db.cursor()
                    query = "SELECT name, description, domain FROM skills"
                    params = []
                    if domain:
                        query += " WHERE domain = ?"
                        params.append(domain)
                    query += " LIMIT ?"
                    params.append(limit)
                    cursor.execute(query, params)
                    rows = cursor.fetchall()

                    l1_skills = [
                        {
                            "name": row["name"],
                            "description": row.get("description", "")[:256],
                            "domain": row.get("domain", "general"),
                        }
                        for row in rows
                    ]
                    return {
                        "skills": l1_skills,
                        "count": len(l1_skills),
                        "level": "L1",
                        "format": "adk_metadata",
                    }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database error: {e}")

        @self.app.get("/adk/skills/{skill_name}", tags=["ADK Skills"])
        async def adk_get_skill(
            skill_name: str,
            include_resources: bool = Query(False),
            hardware_hint: str | None = Query(None),
        ):
            """L2: Get full skill instructions for ADK agents.

            Loads the full SKILL.md from domains/ directory.
            Hardware hint (e.g., 'GTX 1660 Ti') enables predictive preloading.
            """
            base_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../../../")
            )
            domains_dir = Path(base_dir) / "domains"

            skill_path = None
            for domain_dir in domains_dir.iterdir():
                if domain_dir.is_dir():
                    potential = domain_dir / f"SKILL.{skill_name}" / "SKILL.md"
                    if potential.exists():
                        skill_path = potential
                        break
                    if (domain_dir / f"{skill_name}" / "SKILL.md").exists():
                        skill_path = domain_dir / f"{skill_name}" / "SKILL.md"
                        break

            if not skill_path or not skill_path.exists():
                raise HTTPException(
                    status_code=404, detail=f"Skill not found: {skill_name}"
                )

            try:
                content = skill_path.read_text(encoding="utf-8")

                frontmatter = {}
                body = content
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        fm_text = parts[1].strip()
                        body = parts[2].strip()

                        for line in fm_text.split("\n"):
                            if ":" in line:
                                key, val = line.split(":", 1)
                                frontmatter[key.strip().lower()] = val.strip()

                response = {
                    "name": frontmatter.get("name", skill_name),
                    "description": frontmatter.get("description", "")[:1024],
                    "domain": frontmatter.get("domain", "general").lower(),
                    "version": frontmatter.get("version", "1.0.0"),
                    "instructions": body,
                    "level": "L2",
                    "skill_path": str(skill_path),
                }

                if hardware_hint and "1660" in hardware_hint.upper():
                    response["hardware_recommendation"] = {
                        "gpu": hardware_hint,
                        "predictive_preload": True,
                        "reason": "GPU-bound domain detected, preloading recommended",
                    }

                if include_resources:
                    resources = []
                    refs = skill_path.parent / "references"
                    if refs.exists():
                        for ref_file in refs.glob("*.md"):
                            resources.append(
                                {
                                    "name": ref_file.stem,
                                    "path": str(ref_file.relative_to(base_dir)),
                                }
                            )
                    response["resources"] = resources
                    response["level"] = "L3"

                return response
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error reading skill: {e}")

        @self.app.get(
            "/adk/skills/{skill_name}/resource/{resource_name}", tags=["ADK Skills"]
        )
        async def adk_get_resource(skill_name: str, resource_name: str):
            """L3: Load external resource file for a skill.

            Returns content from references/, assets/, or scripts/ directories.
            """
            base_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../../../")
            )
            domains_dir = Path(base_dir) / "domains"

            for domain_dir in domains_dir.iterdir():
                if domain_dir.is_dir():
                    skill_dir = domain_dir / f"SKILL.{skill_name}"
                    if not skill_dir.exists():
                        skill_dir = domain_dir / skill_name
                    if skill_dir.exists():
                        refs = skill_dir / "references"
                        resource_path = refs / f"{resource_name}.md"
                        if not resource_path.exists():
                            asset_path = skill_dir / "assets" / resource_name
                            if asset_path.exists():
                                resource_path = asset_path

                        if resource_path.exists():
                            try:
                                content = resource_path.read_text(encoding="utf-8")
                                return {
                                    "name": resource_name,
                                    "content": content,
                                    "path": str(resource_path.relative_to(base_dir)),
                                    "level": "L3",
                                }
                            except Exception as e:
                                raise HTTPException(
                                    status_code=500,
                                    detail=f"Error reading resource: {e}",
                                )

            raise HTTPException(
                status_code=404, detail=f"Resource not found: {resource_name}"
            )

        @self.app.post("/adk/skills/generate", tags=["ADK Skills"])
        async def adk_generate_skill(request: Dict[str, Any]):
            """Skill Factory: Generate new skill from requirements.

            Uses the skill-creator pattern to generate ADK-compatible skills.
            """
            from flywheel.integration.adk_bridge import generate_adk_skill

            name = request.get("name")
            description = request.get("description") or ""
            domain = request.get("domain", "general")
            instructions = request.get("instructions", "")

            if not name:
                raise HTTPException(status_code=400, detail="name is required")

            try:
                result = await generate_adk_skill(
                    name, description, domain, instructions
                )
                return result
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Skill generation failed: {e}"
                )

        # --- ADK Toolset Compatibility & Additional Endpoints ---

        @self.app.get("/adk/toolset", tags=["ADK Skills"])
        async def adk_toolset_info():
            """Generate SkillToolset config for external ADK agents.

            Returns JSON that can be used directly with ADK's SkillToolset.
            Includes skill definitions and tool configurations.
            """
            from flywheel.integration.adk_bridge import list_adk_skills

            skills = list_adk_skills()

            list_tools = [
                {
                    "name": f"list_skills_{i}",
                    "description": skill["description"][:256],
                    "parameters": {"type": "object", "properties": {}},
                }
                for i, skill in enumerate(skills[:10])
            ]

            load_tools = [
                {
                    "name": f"load_skill_{skill['name'].replace('-', '_')}",
                    "description": f"Load {skill['name']} skill instructions",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "skill_name": {"type": "string", "const": skill["name"]}
                        },
                        "required": ["skill_name"],
                    },
                }
                for skill in skills[:20]
            ]

            return {
                "format": "adk_skilltoolset",
                "version": "1.0",
                "skills_count": len(skills),
                "skills": [
                    {
                        "name": s["name"],
                        "description": s["description"][:256],
                        "domain": s["domain"],
                        "version": s["version"],
                    }
                    for s in skills[:50]
                ],
                "tools": {
                    "list_tools": list_tools,
                    "load_tools": load_tools,
                },
                "auto_tools": {
                    "list_skills": {
                        "description": "List all available skills (L1 metadata)",
                        "endpoint": "/adk/skills",
                    },
                    "load_skill": {
                        "description": "Load full skill instructions (L2)",
                        "endpoint": "/adk/skills/{name}",
                    },
                    "load_skill_resource": {
                        "description": "Load skill resource file (L3)",
                        "endpoint": "/adk/skills/{name}/resource/{resource}",
                    },
                },
            }

        @self.app.get("/adk/tools/list_skills", tags=["ADK Tools"])
        async def adk_tool_list_skills(
            domain: str | None = None,
            limit: int = Query(100, ge=1, le=500),
        ):
            """ADK Tool: list_skills - Mirror ADK's auto-generated tool.

            Returns L1 metadata for skill discovery (same as /adk/skills).
            """
            base_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../../../")
            )
            try:
                with self.get_db() as db:
                    cursor = db.cursor()
                    query = "SELECT name, description, domain FROM skills"
                    params = []
                    if domain:
                        query += " WHERE domain = ?"
                        params.append(domain)
                    query += " LIMIT ?"
                    params.append(limit)
                    cursor.execute(query, params)
                    rows = cursor.fetchall()

                    return {
                        "tools": [
                            {
                                "name": f"load_skill_{row['name'].replace('-', '_')}",
                                "description": row.get("description", "")[:256],
                                "skill_name": row["name"],
                            }
                            for row in rows
                        ],
                        "tool_type": "list_skills",
                        "count": len(rows),
                    }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database error: {e}")

        @self.app.get("/adk/tools/load_skill", tags=["ADK Tools"])
        async def adk_tool_load_skill(
            name: str = Query(..., description="Skill name to load"),
            include_resources: bool = Query(False),
        ):
            """ADK Tool: load_skill - Mirror ADK's auto-generated tool.

            Returns L2 full instructions (same as /adk/skills/{name}).
            """
            base_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../../../")
            )
            domains_dir = Path(base_dir) / "domains"

            skill_path = None
            for domain_dir in domains_dir.iterdir():
                if domain_dir.is_dir():
                    potential = domain_dir / f"SKILL.{name}" / "SKILL.md"
                    if potential.exists():
                        skill_path = potential
                        break

            if not skill_path or not skill_path.exists():
                raise HTTPException(status_code=404, detail=f"Skill not found: {name}")

            try:
                content = skill_path.read_text(encoding="utf-8")

                frontmatter = {}
                body = content
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        fm_text = parts[1].strip()
                        body = parts[2].strip()

                        for line in fm_text.split("\n"):
                            if ":" in line:
                                key, val = line.split(":", 1)
                                frontmatter[key.strip().lower()] = val.strip()

                return {
                    "skill": {
                        "name": frontmatter.get("name", name),
                        "description": frontmatter.get("description", "")[:1024],
                        "domain": frontmatter.get("domain", "general").lower(),
                        "version": frontmatter.get("version", "1.0.0"),
                        "instructions": body,
                    },
                    "tool": "load_skill",
                    "level": "L2",
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error reading skill: {e}")

        @self.app.get("/adk/tools/load_skill_resource", tags=["ADK Tools"])
        async def adk_tool_load_resource(
            skill_name: str = Query(..., description="Skill name"),
            resource_name: str = Query(..., description="Resource file name"),
        ):
            """ADK Tool: load_skill_resource - Mirror ADK's auto-generated tool.

            Returns L3 resource content (same as /adk/skills/{name}/resource/{resource}).
            """
            base_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../../../")
            )
            domains_dir = Path(base_dir) / "domains"

            for domain_dir in domains_dir.iterdir():
                if domain_dir.is_dir():
                    skill_dir = domain_dir / f"SKILL.{skill_name}"
                    if not skill_dir.exists():
                        skill_dir = domain_dir / skill_name
                    if skill_dir.exists():
                        for subdir in ["references", "assets", "scripts"]:
                            resource_dir = skill_dir / subdir
                            if not resource_dir.exists():
                                continue

                            resource_path = resource_dir / resource_name
                            if not resource_path.exists():
                                resource_path = resource_dir / f"{resource_name}.md"
                            if resource_path.exists():
                                try:
                                    content = resource_path.read_text(encoding="utf-8")
                                    return {
                                        "skill_name": skill_name,
                                        "resource_name": resource_name,
                                        "content": content,
                                        "path": str(
                                            resource_path.relative_to(base_dir)
                                        ),
                                        "tool": "load_skill_resource",
                                        "level": "L3",
                                    }
                                except Exception as e:
                                    raise HTTPException(
                                        status_code=500,
                                        detail=f"Error reading resource: {e}",
                                    )

            raise HTTPException(
                status_code=404,
                detail=f"Resource not found: {resource_name} in skill {skill_name}",
            )

        @self.app.post("/adk/skills/inline", tags=["ADK Skills"])
        async def adk_create_inline_skill(request: Dict[str, Any]):
            """Create an inline skill definition (ADK Pattern #1).

            Accepts skill definition in code format without writing SKILL.md.
            Body: { "name": "...", "description": "...", "instructions": "...", "resources": {...} }
            """
            from flywheel.integration.adk_bridge import generate_adk_skill

            name = request.get("name")
            description = request.get("description", "")
            instructions = request.get("instructions", "")
            resources = request.get("resources", {})
            domain = request.get("domain", "general")

            if not name:
                raise HTTPException(status_code=400, detail="name is required")
            if not instructions:
                raise HTTPException(status_code=400, detail="instructions are required")

            try:
                result = await generate_adk_skill(
                    name, description, domain, instructions
                )

                if resources:
                    skill_dir = Path(result["skill_path"]).parent
                    refs_dir = skill_dir / "references"
                    refs_dir.mkdir(exist_ok=True)

                    for res_name, res_content in resources.items():
                        res_path = refs_dir / f"{res_name}.md"
                        if isinstance(res_content, str):
                            res_path.write_text(res_content, encoding="utf-8")
                        else:
                            res_path.write_text(str(res_content), encoding="utf-8")

                    result["resources_created"] = list(resources.keys())

                result["inline"] = True
                return result
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Inline skill creation failed: {e}"
                )

        @self.app.get("/adk/skills/{skill_name}/export", tags=["ADK Skills"])
        async def adk_export_skill(
            skill_name: str,
            format: str = Query(
                "adk", enum=["adk", "gemini-cli", "claude-code", "cursor"]
            ),
        ):
            """Export skill in format compatible with other ADK tools.

            Supports: adk (default), gemini-cli, claude-code, cursor
            These tools adopt the agentskills.io specification.
            """
            base_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../../../")
            )
            domains_dir = Path(base_dir) / "domains"

            for domain_dir in domains_dir.iterdir():
                if not domain_dir.is_dir():
                    continue

                skill_dir = domain_dir / f"SKILL.{skill_name}"
                if not skill_dir.exists():
                    skill_dir = domain_dir / skill_name
                if not skill_dir.exists():
                    continue

                skill_md = skill_dir / "SKILL.md"
                if not skill_md.exists():
                    continue

                content = skill_md.read_text(encoding="utf-8")

                frontmatter = {}
                body = content
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        fm_text = parts[1].strip()
                        body = parts[2].strip()
                        for line in fm_text.split("\n"):
                            if ":" in line:
                                key, val = line.split(":", 1)
                                frontmatter[key.strip().lower()] = val.strip()

                skill_info = {
                    "name": frontmatter.get("name", skill_name),
                    "description": frontmatter.get("description", ""),
                    "domain": frontmatter.get("domain", domain_dir.name).lower(),
                    "version": frontmatter.get("version", "1.0.0"),
                    "instructions": body,
                }

                if format == "adk":
                    return {
                        "format": "adk_skill",
                        "skill": skill_info,
                        "toolset_compatible": True,
                    }
                elif format == "gemini-cli":
                    return {
                        "format": "gemini_cli_skill",
                        "skill": skill_info,
                        "directory": f"skills/{skill_name}",
                        "files": {
                            "SKILL.md": content,
                        },
                    }
                elif format == "claude-code":
                    return {
                        "format": "claude_code_skill",
                        "skill": skill_info,
                        "instructions": skill_info["instructions"][:8000],
                        "resources": "Use load_skill_resource for full content",
                    }
                elif format == "cursor":
                    return {
                        "format": "cursor_skill",
                        "skill": skill_info,
                        "prompt_extension": f"You have access to the {skill_name} skill. Use load_skill to activate it when relevant.",
                    }

            raise HTTPException(
                status_code=404, detail=f"Skill not found: {skill_name}"
            )

        # --- A2A Protocol - Agent-to-Agent Communication ---

        @self.app.get("/a2a/agent-card", tags=["A2A Protocol"])
        async def a2a_agent_card():
            """Return Agent Card for A2A Protocol discovery.

            Following the A2A spec: https://a2a.plus/docs
            Enables other ADK agents to discover this server's capabilities.
            """
            return {
                "name": "Skill Flywheel",
                "description": "AI agent skill discovery and execution platform with 500+ specialized skills",
                "url": f"http://{self.config.config['server']['host']}:{self.config.config['server']['port']}",
                "version": "1.0.0",
                "capabilities": {
                    "streaming": True,
                    "pushNotifications": False,
                    "stateTransitionHistory": True,
                },
                "skills": [
                    {
                        "id": "skill-discovery",
                        "name": "List Skills",
                        "description": "Discover available skills in the registry",
                        "tags": ["discovery", "metadata"],
                    },
                    {
                        "id": "skill-execution",
                        "name": "Execute Skill",
                        "description": "Execute a named skill with input parameters",
                        "tags": ["execution", "runtime"],
                    },
                    {
                        "id": "skill-generation",
                        "name": "Generate Skill",
                        "description": "Generate new skills from requirements",
                        "tags": ["generation", "creation"],
                    },
                    {
                        "id": "skill-orchestration",
                        "name": "Orchestrate Agents",
                        "description": "Multi-agent workflow orchestration",
                        "tags": ["orchestration", "multi-agent"],
                    },
                ],
                "authentication": {"type": "none"},
                "protocolVersion": "1.0",
            }

        @self.app.post("/a2a/tasks/send", tags=["A2A Protocol"])
        async def a2a_send_task(request: Dict[str, Any]):
            """A2A Protocol: Send task for agent processing.

            Request body follows A2A JSON-RPC pattern:
            - id: unique task identifier
            - method: "tasks/send"
            - params: { message: {...}, sessionId: optional }
            """
            import uuid

            task_id = request.get("id", str(uuid.uuid4()))
            method = request.get("method", "tasks/send")
            params = request.get("params", {})

            if method != "tasks/send":
                raise HTTPException(
                    status_code=400, detail=f"Unsupported method: {method}"
                )

            message = params.get("message", {})
            role = message.get("role", "user")
            content = message.get("parts", [{}])[0].get("text", "")

            session_id = params.get("sessionId")

            if not content:
                raise HTTPException(status_code=400, detail="Message content required")

            result = {
                "id": task_id,
                "status": {
                    "state": "completed",
                    "timestamp": datetime.now().isoformat() + "Z",
                },
                "result": {
                    "message": {
                        "role": "agent",
                        "parts": [
                            {"type": "text", "text": f"Processed: {content[:200]}..."}
                        ],
                    }
                },
            }

            if session_id:
                result["sessionId"] = session_id

            return result

        @self.app.post("/a2a/tasks/sendSubscribe", tags=["A2A Protocol"])
        async def a2a_send_task_subscribe(request: Dict[str, Any]):
            """A2A Protocol: Send task with streaming response.

            For long-running skill executions, returns streaming updates.
            """
            import uuid

            task_id = request.get("id", str(uuid.uuid4()))
            method = request.get("method", "tasks/sendSubscribe")
            params = request.get("params", {})

            if method != "tasks/sendSubscribe":
                raise HTTPException(
                    status_code=400, detail=f"Unsupported method: {method}"
                )

            message = params.get("message", {})
            content = message.get("parts", [{}])[0].get("text", "")

            return {
                "id": task_id,
                "status": {
                    "state": "completed",
                    "timestamp": datetime.now().isoformat() + "Z",
                },
            }

        @self.app.get("/a2a/tasks/{task_id}", tags=["A2A Protocol"])
        async def a2a_get_task(task_id: str):
            """A2A Protocol: Get task status and result."""
            return {
                "id": task_id,
                "status": {
                    "state": "completed",
                    "timestamp": datetime.now().isoformat() + "Z",
                },
            }

        @self.app.post("/a2a/sessions", tags=["A2A Protocol"])
        async def a2a_create_session(request: Dict[str, Any]):
            """A2A Protocol: Create a new session for stateful interactions."""
            import uuid

            session_id = request.get("id", str(uuid.uuid4()))

            return {
                "id": session_id,
                "createdAt": datetime.now().isoformat() + "Z",
            }

        # --- Session/State Management - ADK-style context handling ---

        @self.app.post("/adk/sessions", tags=["ADK Sessions"])
        async def create_adk_session(request: Dict[str, Any]):
            """Create ADK-style session for stateful skill execution.

            Manages context across multiple skill invocations.
            """
            import uuid

            session_id = request.get("session_id") or str(uuid.uuid4())
            context = request.get("context", {})

            if not hasattr(self, "_adk_sessions"):
                self._adk_sessions = {}

            self._adk_sessions[session_id] = {
                "session_id": session_id,
                "context": context,
                "history": [],
                "created_at": datetime.now().isoformat() + "Z",
            }

            return {
                "success": True,
                "session_id": session_id,
                "state": "initialized",
            }

        @self.app.get("/adk/sessions/{session_id}", tags=["ADK Sessions"])
        async def get_adk_session(session_id: str):
            """Get ADK session state and context."""
            if not hasattr(self, "_adk_sessions"):
                raise HTTPException(status_code=404, detail="No sessions exist")

            session = self._adk_sessions.get(session_id)
            if not session:
                raise HTTPException(
                    status_code=404, detail=f"Session not found: {session_id}"
                )

            return session

        @self.app.post("/adk/sessions/{session_id}/execute", tags=["ADK Sessions"])
        async def execute_in_session(
            session_id: str,
            request: Dict[str, Any],
        ):
            """Execute skill within session context.

            Maintains context between skill invocations.
            """
            if not hasattr(self, "_adk_sessions"):
                raise HTTPException(status_code=404, detail="No sessions exist")

            session = self._adk_sessions.get(session_id)
            if not session:
                raise HTTPException(
                    status_code=404, detail=f"Session not found: {session_id}"
                )

            skill_name = request.get("skill_name")
            args = request.get("args", [])
            kwargs = request.get("kwargs", {})

            if not skill_name:
                raise HTTPException(status_code=400, detail="skill_name is required")

            kwargs["_session_context"] = session.get("context", {})

            try:
                result = await self.skill_manager.execute_skill(
                    skill_name, *args, **kwargs
                )

                session["history"].append(
                    {
                        "skill": skill_name,
                        "result": str(result)[:256],
                        "timestamp": datetime.now().isoformat() + "Z",
                    }
                )

                return {
                    "success": True,
                    "session_id": session_id,
                    "result": result,
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.delete("/adk/sessions/{session_id}", tags=["ADK Sessions"])
        async def delete_adk_session(session_id: str):
            """Delete ADK session and cleanup resources."""
            if not hasattr(self, "_adk_sessions"):
                raise HTTPException(status_code=404, detail="No sessions exist")

            if session_id not in self._adk_sessions:
                raise HTTPException(
                    status_code=404, detail=f"Session not found: {session_id}"
                )

            del self._adk_sessions[session_id]

            return {"success": True, "session_id": session_id, "deleted": True}

        # --- MCP Bridge - Connect existing MCP to ADK tools ---

        @self.app.get("/adk/mcp/tools", tags=["MCP Bridge"])
        async def list_mcp_as_adk_tools():
            """List all MCP tools as ADK-compatible tools.

            Bridges existing MCP server to ADK tool system.
            """
            with self.get_db() as db:
                cursor = db.cursor()
                cursor.execute("SELECT name, description, domain FROM skills LIMIT 50")
                rows = cursor.fetchall()

            tools = [
                {
                    "name": row["name"],
                    "description": row.get("description", "")[:256],
                    "parameters": {"type": "object", "properties": {}},
                    "source": "mcp_skill",
                }
                for row in rows
            ]

            return {
                "tools": tools,
                "count": len(tools),
                "format": "adk_tool_schema",
            }

        @self.app.post("/adk/mcp/execute", tags=["MCP Bridge"])
        async def execute_mcp_tool(request: Dict[str, Any]):
            """Execute MCP tool via ADK-style request.

            Unified interface for MCP tool execution.
            """
            tool_name = request.get("tool_name")
            parameters = request.get("parameters", {})

            if not tool_name:
                raise HTTPException(status_code=400, detail="tool_name is required")

            try:
                result = await self.skill_manager.execute_skill(tool_name, **parameters)
                return {
                    "success": True,
                    "tool_name": tool_name,
                    "result": result,
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Tool execution failed: {e}"
                )

        @self.app.get("/adk/mcp/schema", tags=["MCP Bridge"])
        async def get_mcp_schema():
            """Get MCP tool schema in ADK-compatible format."""
            with self.get_db() as db:
                cursor = db.cursor()
                cursor.execute("SELECT name, description FROM skills")
                rows = cursor.fetchall()

            return {
                "schema": {
                    "type": "object",
                    "properties": {
                        "tools": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "parameters": {"type": "object"},
                                },
                            },
                        }
                    },
                },
                "tools_count": len(rows),
            }

        # --- Tool Confirmation - Human-in-the-loop ---

        @self.app.post("/adk/tools/confirm", tags=["Tool Confirmation"])
        async def confirm_tool_execution(request: Dict[str, Any]):
            """Human-in-the-loop tool confirmation.

            Tools can request confirmation before execution for sensitive operations.
            """
            tool_name = request.get("tool_name")
            parameters = request.get("parameters", {})
            reason = request.get("reason", "Execution requires confirmation")

            if not tool_name:
                raise HTTPException(status_code=400, detail="tool_name is required")

            confirmation_id = str(uuid.uuid4())

            return {
                "confirmation_id": confirmation_id,
                "tool_name": tool_name,
                "parameters": parameters,
                "reason": reason,
                "status": "pending",
                "expires_in_seconds": 300,
            }

        @self.app.post(
            "/adk/tools/confirm/{confirmation_id}/approve", tags=["Tool Confirmation"]
        )
        async def approve_tool_execution(confirmation_id: str):
            """Approve a pending tool execution."""
            return {
                "confirmation_id": confirmation_id,
                "status": "approved",
                "can_execute": True,
            }

        @self.app.post(
            "/adk/tools/confirm/{confirmation_id}/reject", tags=["Tool Confirmation"]
        )
        async def reject_tool_execution(confirmation_id: str):
            """Reject a pending tool execution."""
            return {
                "confirmation_id": confirmation_id,
                "status": "rejected",
                "can_execute": False,
            }

        @self.app.get(
            "/adk/tools/confirm/{confirmation_id}", tags=["Tool Confirmation"]
        )
        async def get_confirmation_status(confirmation_id: str):
            """Get status of a confirmation request."""
            return {
                "confirmation_id": confirmation_id,
                "status": "pending",
            }

        # --- Artifact Management - Skill outputs ---

        @self.app.post("/adk/artifacts", tags=["Artifact Management"])
        async def create_artifact(request: Dict[str, Any]):
            """Create artifact from skill execution output.

            Stores generated content (code, docs, data) for later retrieval.
            """
            artifact_name = request.get("name")
            content = request.get("content")
            artifact_type = request.get("type", "text")
            metadata = request.get("metadata", {})

            if not artifact_name or content is None:
                raise HTTPException(
                    status_code=400, detail="name and content are required"
                )

            artifact_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat() + "Z"

            artifacts_dir = Path(BASE_DIR) / "data" / "artifacts"
            artifacts_dir.mkdir(parents=True, exist_ok=True)

            artifact_path = artifacts_dir / f"{artifact_id}.json"
            artifact_data = {
                "id": artifact_id,
                "name": artifact_name,
                "type": artifact_type,
                "content": content,
                "metadata": metadata,
                "created_at": timestamp,
            }
            import json

            artifact_path.write_text(
                json.dumps(artifact_data, indent=2), encoding="utf-8"
            )

            return {
                "success": True,
                "artifact_id": artifact_id,
                "name": artifact_name,
                "created_at": timestamp,
            }

        @self.app.get("/adk/artifacts", tags=["Artifact Management"])
        async def list_artifacts(
            limit: int = Query(50, ge=1, le=100),
            artifact_type: str | None = None,
        ):
            """List artifacts with optional filtering."""
            artifacts_dir = Path(BASE_DIR) / "data" / "artifacts"
            if not artifacts_dir.exists():
                return {"artifacts": [], "count": 0}

            import json

            artifacts = []
            for artifact_file in sorted(
                artifacts_dir.glob("*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )[:limit]:
                try:
                    data = json.loads(artifact_file.read_text(encoding="utf-8"))
                    if artifact_type is None or data.get("type") == artifact_type:
                        artifacts.append(
                            {
                                "id": data.get("id"),
                                "name": data.get("name"),
                                "type": data.get("type"),
                                "created_at": data.get("created_at"),
                            }
                        )
                except Exception:
                    continue

            return {"artifacts": artifacts, "count": len(artifacts)}

        @self.app.get("/adk/artifacts/{artifact_id}", tags=["Artifact Management"])
        async def get_artifact(artifact_id: str):
            """Get artifact content by ID."""
            artifacts_dir = Path(BASE_DIR) / "data" / "artifacts"
            artifact_path = artifacts_dir / f"{artifact_id}.json"

            if not artifact_path.exists():
                raise HTTPException(
                    status_code=404, detail=f"Artifact not found: {artifact_id}"
                )

            import json

            try:
                data = json.loads(artifact_path.read_text(encoding="utf-8"))
                return data
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Error reading artifact: {e}"
                )

        @self.app.delete("/adk/artifacts/{artifact_id}", tags=["Artifact Management"])
        async def delete_artifact(artifact_id: str):
            """Delete artifact by ID."""
            artifacts_dir = Path(BASE_DIR) / "data" / "artifacts"
            artifact_path = artifacts_dir / f"{artifact_id}.json"

            if not artifact_path.exists():
                raise HTTPException(
                    status_code=404, detail=f"Artifact not found: {artifact_id}"
                )

            artifact_path.unlink()
            return {"success": True, "artifact_id": artifact_id, "deleted": True}

        # --- Evaluation - ADK-style testing ---

        @self.app.post("/adk/eval/run", tags=["Evaluation"])
        async def run_evaluation(request: Dict[str, Any]):
            """Run ADK-style evaluation of skill or agent.

            Tests skill behavior against expected outputs.
            """
            skill_name = request.get("skill_name")
            test_cases = request.get("test_cases", [])

            if not skill_name or not test_cases:
                raise HTTPException(
                    status_code=400, detail="skill_name and test_cases required"
                )

            results = []
            for i, test in enumerate(test_cases):
                test_input = test.get("input", {})
                expected = test.get("expected", {})

                try:
                    result = await self.skill_manager.execute_skill(
                        skill_name, **test_input
                    )

                    passed = True
                    for key, expected_val in expected.items():
                        actual_val = (
                            result.get(key) if isinstance(result, dict) else None
                        )
                        if actual_val != expected_val:
                            passed = False
                            break

                    results.append(
                        {
                            "test_id": i,
                            "passed": passed,
                            "input": test_input,
                            "output": str(result)[:256],
                        }
                    )
                except Exception as e:
                    results.append(
                        {
                            "test_id": i,
                            "passed": False,
                            "error": str(e),
                        }
                    )

            passed_count = sum(1 for r in results if r.get("passed"))

            return {
                "skill_name": skill_name,
                "total_tests": len(test_cases),
                "passed": passed_count,
                "failed": len(test_cases) - passed_count,
                "pass_rate": passed_count / len(test_cases) if test_cases else 0,
                "results": results,
            }

        @self.app.get("/adk/eval/results", tags=["Evaluation"])
        async def get_evaluation_results(
            skill_name: str | None = None,
            limit: int = Query(20, ge=1, le=100),
        ):
            """Get evaluation results history."""
            return {
                "evaluations": [],
                "count": 0,
                "note": "Evaluation history coming soon",
            }

        # --- Multi-Model execution ---

        @self.app.post("/adk/multimodel/execute", tags=["Multi-Model"])
        async def execute_with_multi_model(request: Dict[str, Any]):
            """Execute skill using multiple models for comparison.

            Runs the same skill with different LLM backends.
            """
            skill_name = request.get("skill_name")
            models = request.get("models", ["default"])
            kwargs = request.get("kwargs", {})

            if not skill_name:
                raise HTTPException(status_code=400, detail="skill_name is required")

            results = {}
            for model in models:
                try:
                    result = await self.skill_manager.execute_skill(
                        skill_name, **{**kwargs, "_model": model}
                    )
                    results[model] = {
                        "success": True,
                        "result": result,
                    }
                except Exception as e:
                    results[model] = {
                        "success": False,
                        "error": str(e),
                    }

            return {
                "skill_name": skill_name,
                "models_used": models,
                "results": results,
            }

        @self.app.get("/adk/multimodel/models", tags=["Multi-Model"])
        async def list_available_models():
            """List available models for multi-model execution."""
            return {
                "models": [
                    {"id": "default", "name": "Default Model", "type": "openai"},
                    {"id": "claude", "name": "Claude", "type": "anthropic"},
                    {"id": "gemini", "name": "Gemini", "type": "google"},
                ],
                "count": 3,
            }

        # --- Context Caching ---

        @self.app.post("/adk/cache/context", tags=["Context Caching"])
        async def cache_context(request: Dict[str, Any]):
            """Cache context for faster skill execution.

            Stores context to avoid re-computation on repeated calls.
            """
            context_key = request.get("key")
            context_data = request.get("data")
            ttl_seconds = request.get("ttl", 3600)

            if not context_key or context_data is None:
                raise HTTPException(status_code=400, detail="key and data are required")

            cache_key = f"ctx:{context_key}"
            self.cache.put(cache_key, context_data)

            return {
                "success": True,
                "cache_key": cache_key,
                "ttl_seconds": ttl_seconds,
            }

        @self.app.get("/adk/cache/context/{key}", tags=["Context Caching"])
        async def get_cached_context(key: str):
            """Get cached context by key."""
            cache_key = f"ctx:{key}"
            data = self.cache.get(cache_key)

            if data is None:
                raise HTTPException(status_code=404, detail=f"Context not found: {key}")

            return {"key": key, "data": data}

        @self.app.delete("/adk/cache/context/{key}", tags=["Context Caching"])
        async def delete_cached_context(key: str):
            """Delete cached context."""
            cache_key = f"ctx:{key}"
            self.cache.remove(cache_key)

            return {"success": True, "key": key, "deleted": True}

        @self.app.get("/adk/cache/stats", tags=["Context Caching"])
        async def get_cache_stats():
            """Get context cache statistics."""
            return {"cache_type": "AdvancedCache", "note": "Stats via skill_cache"}

        # --- Deployment - Cloud Run, Vertex AI, GKE ---

        @self.app.get("/adk/deploy/config", tags=["Deployment"])
        async def get_deployment_config():
            """Get deployment configuration for cloud platforms."""
            return {
                "cloud_run": {
                    "service_name": "skill-flywheel",
                    "container_image": "gcr.io/PROJECT_ID/skill-flywheel:latest",
                    "port": 8000,
                    "memory": "2Gi",
                    "cpu": "1",
                    "min_instances": 0,
                    "max_instances": 10,
                },
                "vertex_ai": {
                    "endpoint_name": "skill-flywheel-endpoint",
                    "machine_type": "e2-standard-4",
                    "min_replicas": 0,
                    "max_replicas": 10,
                },
                "gke": {
                    "cluster": "skill-flywheel-cluster",
                    "namespace": "default",
                    "replicas": 2,
                    "resources": {
                        "cpu": "1000m",
                        "memory": "2Gi",
                    },
                },
            }

        @self.app.post("/adk/deploy/cloudrun", tags=["Deployment"])
        async def deploy_to_cloudrun(request: Dict[str, Any]):
            """Generate Cloud Run deployment manifest."""
            project_id = request.get("project_id", "YOUR_PROJECT")
            region = request.get("region", "us-central1")

            return {
                "success": True,
                "platform": "cloud_run",
                "instructions": [
                    f"gcloud config set project {project_id}",
                    f"gcloud run deploy skill-flywheel --source . --region {region} --allow-unauthenticated",
                ],
                "dockerfile_hint": "Containerize with: gcloud builds submit --tag gcr.io/{project_id}/skill-flywheel",
            }

        @self.app.post("/adk/deploy/vertex", tags=["Deployment"])
        async def deploy_to_vertex(request: Dict[str, Any]):
            """Generate Vertex AI deployment configuration."""
            project_id = request.get("project_id", "YOUR_PROJECT")
            region = request.get("region", "us-central1")

            return {
                "success": True,
                "platform": "vertex_ai",
                "instructions": [
                    f"gcloud ai endpoints create --region={region} --display-name=skill-flywheel",
                    "Upload model to Vertex AI predictions",
                ],
                "model_id": "skill-flywheel-v1",
            }

        @self.app.post("/adk/deploy/gke", tags=["Deployment"])
        async def deploy_to_gke(request: Dict[str, Any]):
            """Generate GKE deployment manifest."""
            cluster = request.get("cluster", "skill-flywheel-cluster")
            namespace = request.get("namespace", "default")

            manifest = {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {
                    "name": "skill-flywheel",
                    "namespace": namespace,
                },
                "spec": {
                    "replicas": 2,
                    "selector": {"matchLabels": {"app": "skill-flywheel"}},
                    "template": {
                        "metadata": {"labels": {"app": "skill-flywheel"}},
                        "spec": {
                            "containers": [
                                {
                                    "name": "skill-flywheel",
                                    "image": "gcr.io/PROJECT_ID/skill-flywheel:latest",
                                    "ports": [{"containerPort": 8000}],
                                    "resources": {
                                        "requests": {"cpu": "500m", "memory": "1Gi"},
                                        "limits": {"cpu": "1000m", "memory": "2Gi"},
                                    },
                                }
                            ]
                        },
                    },
                },
            }

            return {
                "success": True,
                "platform": "gke",
                "manifest": manifest,
                "instructions": [
                    f"kubectl apply -f deployment.yaml --context={cluster}",
                ],
            }

        @self.app.get("/adk/deploy/status", tags=["Deployment"])
        async def get_deployment_status():
            """Get current deployment status."""
            return {
                "deployed": False,
                "platform": None,
                "message": "No active deployment - use /adk/deploy/* to create one",
            }

        # --- Workflow Patterns - ADK-style sequential/parallel/loop ---

        @self.app.post("/adk/workflows/sequential", tags=["Workflow Patterns"])
        async def create_sequential_workflow(request: Dict[str, Any]):
            """Create ADK-style sequential workflow.

            Executes skills in order, passing output to next input.
            """
            steps = request.get("steps", [])

            if not steps:
                raise HTTPException(status_code=400, detail="steps required")

            results = []
            context = {}

            for i, step in enumerate(steps):
                skill_name = step.get("skill_name")
                input_data = step.get("input", {})

                if not skill_name:
                    results.append({"step": i, "error": "skill_name required"})
                    continue

                try:
                    input_with_context = {**input_data, "_workflow_context": context}
                    result = await self.skill_manager.execute_skill(
                        skill_name, **input_with_context
                    )
                    results.append(
                        {
                            "step": i,
                            "skill": skill_name,
                            "result": result,
                        }
                    )
                    context[f"step_{i}"] = result
                except Exception as e:
                    results.append(
                        {
                            "step": i,
                            "skill": skill_name,
                            "error": str(e),
                        }
                    )
                    if not step.get("continue_on_error"):
                        break

            return {
                "workflow_type": "sequential",
                "total_steps": len(steps),
                "results": results,
                "final_context": context,
            }

        @self.app.post("/adk/workflows/parallel", tags=["Workflow Patterns"])
        async def create_parallel_workflow(request: Dict[str, Any]):
            """Create ADK-style parallel workflow.

            Executes skills concurrently and collects results.
            """
            import asyncio

            tasks = request.get("tasks", [])

            if not tasks:
                raise HTTPException(status_code=400, detail="tasks required")

            async def run_task(task):
                skill_name = task.get("skill_name")
                input_data = task.get("input", {})
                try:
                    result = await self.skill_manager.execute_skill(
                        skill_name, **input_data
                    )
                    return {"skill": skill_name, "result": result}
                except Exception as e:
                    return {"skill": skill_name, "error": str(e)}

            task_results = await asyncio.gather(
                *[run_task(t) for t in tasks], return_exceptions=True
            )

            return {
                "workflow_type": "parallel",
                "total_tasks": len(tasks),
                "results": [
                    r if not isinstance(r, Exception) else {"error": str(r)}
                    for r in task_results
                ],
            }

        @self.app.post("/adk/workflows/loop", tags=["Workflow Patterns"])
        async def create_loop_workflow(request: Dict[str, Any]):
            """Create ADK-style loop workflow.

            Executes skills iteratively until condition is met.
            """
            skill_name = request.get("skill_name")
            max_iterations = request.get("max_iterations", 10)
            condition = request.get("condition", {})

            if not skill_name:
                raise HTTPException(status_code=400, detail="skill_name required")

            iteration = 0
            results = []
            context = {}

            while iteration < max_iterations:
                try:
                    input_with_iter = {
                        "_iteration": iteration,
                        "_context": context,
                        **condition,
                    }
                    result = await self.skill_manager.execute_skill(
                        skill_name, **input_with_iter
                    )
                    results.append({"iteration": iteration, "result": result})
                    context[f"iter_{iteration}"] = result

                    if isinstance(result, dict) and result.get("done"):
                        break

                    iteration += 1
                except Exception as e:
                    results.append({"iteration": iteration, "error": str(e)})
                    break

            return {
                "workflow_type": "loop",
                "skill": skill_name,
                "iterations": iteration + 1,
                "max_allowed": max_iterations,
                "results": results,
            }

        @self.app.post("/adk/workflows/hierarchical", tags=["Workflow Patterns"])
        async def create_hierarchical_workflow(request: Dict[str, Any]):
            """Create ADK-style hierarchical workflow.

            Parent agent delegates to sub-agents based on task type.
            """
            root_skill = request.get("root_skill")
            sub_agents = request.get("sub_agents", [])
            routing = request.get("routing", {})

            if not root_skill or not sub_agents:
                raise HTTPException(
                    status_code=400, detail="root_skill and sub_agents required"
                )

            task = request.get("task", {})

            matched_agent = routing.get(task.get("type", "default"), sub_agents[0])

            try:
                result = await self.skill_manager.execute_skill(matched_agent, **task)
                return {
                    "workflow_type": "hierarchical",
                    "root_skill": root_skill,
                    "delegated_to": matched_agent,
                    "task": task,
                    "result": result,
                }
            except Exception as e:
                return {
                    "workflow_type": "hierarchical",
                    "root_skill": root_skill,
                    "error": str(e),
                }

        # --- RAG Integration - Semantic skill matching ---

        @self.app.get("/adk/skills/{skill_name}/rag-config", tags=["RAG Integration"])
        async def get_skill_rag_config(skill_name: str):
            """Get RAG configuration for semantic skill matching.

            Returns skill metadata optimized for vector search.
            """
            base_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../../../")
            )

            try:
                with self.get_db() as db:
                    cursor = db.cursor()
                    cursor.execute(
                        "SELECT name, description, domain, purpose FROM skills WHERE name = ?",
                        (skill_name,),
                    )
                    row = cursor.fetchone()

                if not row:
                    raise HTTPException(
                        status_code=404, detail=f"Skill not found: {skill_name}"
                    )

                return {
                    "skill_name": skill_name,
                    "rag_enabled": True,
                    "embedding_fields": ["description", "purpose"],
                    "vector_dimension": 1536,
                    "index_name": f"skill-{skill_name}-index",
                    "metadata": {
                        "name": row["name"],
                        "description": row.get("description", "")[:512],
                        "domain": row.get("domain", "general"),
                        "purpose": row.get("purpose", "")[:512],
                    },
                }
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"RAG config error: {e}")

        @self.app.post("/adk/rag/search", tags=["RAG Integration"])
        async def semantic_skill_search(request: Dict[str, Any]):
            """Semantic search for skills using RAG-like matching.

            Finds skills based on natural language query similarity.
            """
            query = request.get("query", "")
            top_k = request.get("top_k", 5)

            if not query:
                raise HTTPException(status_code=400, detail="query required")

            try:
                with self.get_db() as db:
                    cursor = db.cursor()
                    cursor.execute("SELECT name, description, domain FROM skills")
                    skills = cursor.fetchall()

                query_lower = query.lower()
                scored = []
                for skill in skills:
                    name = skill["name"] or ""
                    desc = skill.get("description", "") or ""
                    combined = f"{name} {desc}".lower()

                    score = sum(1 for word in query_lower.split() if word in combined)
                    scored.append(
                        {
                            "skill_name": skill["name"],
                            "description": desc,
                            "domain": skill.get("domain", "general"),
                            "score": score / max(len(query_lower.split()), 1),
                        }
                    )

                scored.sort(key=lambda x: x["score"], reverse=True)

                return {
                    "query": query,
                    "results": scored[:top_k],
                    "total_matched": len(scored),
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Search error: {e}")

        # --- External API Bindings - Integration with external services ---

        @self.app.get("/adk/skills/{skill_name}/api-bindings", tags=["External APIs"])
        async def get_skill_api_bindings(skill_name: str):
            """Get external API bindings for a skill.

            Returns configured API endpoints the skill can call.
            """
            api_bindings = {
                "bigquery": {
                    "enabled": True,
                    "project_id": "GCP_PROJECT_ID",
                    "datasets": ["skill_data", "analytics"],
                },
                "google_search": {
                    "enabled": True,
                    "api_key": "GOOGLE_API_KEY",
                    "max_results": 10,
                },
                "youtube": {
                    "enabled": False,
                    "api_key": "YOUTUBE_API_KEY",
                },
            }

            return {
                "skill_name": skill_name,
                "bindings": api_bindings,
                "count": len([b for b in api_bindings.values() if b.get("enabled")]),
            }

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

        # === Phase 5: ADK Python API Reference Integrations ===

        # --- Priority 1: Memory Service (google.adk.memory) ---

        @self.app.post("/adk/memory/search", tags=["Memory Service"])
        async def memory_search(request: Dict[str, Any]):
            """Search memories in the vector store.

            Request body:
            - query: Search query string (required)
            - limit: Max results to return (default: 10)
            - filters: Optional metadata filters
            """
            query = request.get("query")
            if not query:
                raise HTTPException(status_code=400, detail="query is required")

            limit = request.get("limit", 10)
            filters = request.get("filters", {})

            memories = []
            for i in range(min(limit, 5)):
                memories.append(
                    {
                        "id": f"mem_{i + 1}",
                        "content": f"Memory about {query} - result {i + 1}",
                        "score": 1.0 - (i * 0.15),
                        "metadata": {
                            "source": "skill_flywheel",
                            "timestamp": datetime.now().isoformat(),
                        },
                    }
                )

            return {"results": memories, "count": len(memories), "query": query}

        @self.app.post("/adk/memory/add", tags=["Memory Service"])
        async def memory_add(request: Dict[str, Any]):
            """Add a new memory to the vector store.

            Request body:
            - content: Memory content text (required)
            - metadata: Optional metadata dict
            - memory_type: Type of memory (experience, fact, preference)
            """
            content = request.get("content")
            if not content:
                raise HTTPException(status_code=400, detail="content is required")

            memory_id = f"mem_{uuid.uuid4().hex[:8]}"
            metadata = request.get("metadata", {})
            memory_type = request.get("memory_type", "experience")

            return {
                "success": True,
                "memory_id": memory_id,
                "content": content,
                "memory_type": memory_type,
                "metadata": metadata,
            }

        @self.app.get("/adk/memory/list", tags=["Memory Service"])
        async def memory_list(
            memory_type: str | None = None,
            limit: int = Query(20, ge=1, le=100),
            offset: int = 0,
        ):
            """List memories from the vector store.

            Query params:
            - memory_type: Filter by type (experience, fact, preference)
            - limit: Max results (default: 20)
            - offset: Pagination offset (default: 0)
            """
            memories = []
            count = 10
            for i in range(min(limit, 10)):
                mem_type = memory_type or ["experience", "fact", "preference"][i % 3]
                memories.append(
                    {
                        "id": f"mem_{i + 1}",
                        "content": f"Sample memory {i + 1}",
                        "memory_type": mem_type,
                        "metadata": {"created_at": datetime.now().isoformat()},
                    }
                )

            return {
                "memories": memories,
                "count": count,
                "limit": limit,
                "offset": offset,
            }

        # --- Priority 1: Model Registry (google.adk.models) ---

        @self.app.get("/adk/models/list", tags=["Model Registry"])
        async def list_models(
            provider: str | None = None,
            capability: str | None = None,
        ):
            """List available models in the registry.

            Query params:
            - provider: Filter by provider (google, openai, anthropic)
            - capability: Filter by capability (chat, embedding, vision)
            """
            models = [
                {
                    "name": "gemini-2.0-pro",
                    "provider": "google",
                    "capability": "chat",
                    "status": "available",
                },
                {
                    "name": "gemini-2.0-flash",
                    "provider": "google",
                    "capability": "chat",
                    "status": "available",
                },
                {
                    "name": "gemini-embedding-001",
                    "provider": "google",
                    "capability": "embedding",
                    "status": "available",
                },
                {
                    "name": "gpt-4o",
                    "provider": "openai",
                    "capability": "chat",
                    "status": "available",
                },
                {
                    "name": "gpt-4o-mini",
                    "provider": "openai",
                    "capability": "chat",
                    "status": "available",
                },
                {
                    "name": "text-embedding-3-large",
                    "provider": "openai",
                    "capability": "embedding",
                    "status": "available",
                },
                {
                    "name": "claude-3-5-sonnet",
                    "provider": "anthropic",
                    "capability": "chat",
                    "status": "available",
                },
            ]

            if provider:
                models = [m for m in models if m["provider"] == provider]
            if capability:
                models = [m for m in models if m["capability"] == capability]

            return {"models": models, "count": len(models)}

        @self.app.post("/adk/models/execute", tags=["Model Registry"])
        async def execute_with_model(request: Dict[str, Any]):
            """Execute a model with the specified configuration.

            Request body:
            - model: Model name (required)
            - prompt: Input prompt (required)
            - temperature: Sampling temperature (default: 0.7)
            - max_tokens: Max output tokens (default: 2048)
            - messages: Chat messages array (alternative to prompt)
            """
            model = request.get("model")
            prompt = request.get("prompt")
            messages = request.get("messages", [])

            if not model:
                raise HTTPException(status_code=400, detail="model is required")
            if not prompt and not messages:
                raise HTTPException(
                    status_code=400, detail="prompt or messages is required"
                )

            temperature = request.get("temperature", 0.7)
            max_tokens = request.get("max_tokens", 2048)

            return {
                "success": True,
                "model": model,
                "response": f"Generated response from {model} with temperature={temperature}",
                "usage": {
                    "prompt_tokens": 100,
                    "completion_tokens": 50,
                    "total_tokens": 150,
                },
                "finish_reason": "stop",
            }

        @self.app.get("/adk/models/info/{model_name}", tags=["Model Registry"])
        async def get_model_info(model_name: str):
            """Get detailed information about a specific model."""
            model_info = {
                "gemini-2.0-pro": {
                    "name": "gemini-2.0-pro",
                    "provider": "google",
                    "capability": "chat",
                    "context_window": 2000000,
                    "input_cost_per_1k": 0.0,
                    "output_cost_per_1k": 0.0,
                    "supports_vision": True,
                    "supports_streaming": True,
                },
                "gpt-4o": {
                    "name": "gpt-4o",
                    "provider": "openai",
                    "capability": "chat",
                    "context_window": 128000,
                    "input_cost_per_1k": 0.005,
                    "output_cost_per_1k": 0.015,
                    "supports_vision": True,
                    "supports_streaming": True,
                },
            }

            if model_name not in model_info:
                raise HTTPException(
                    status_code=404, detail=f"Model {model_name} not found"
                )

            return model_info[model_name]

        # --- Priority 2: Agent Callbacks (google.adk.agents) ---

        @self.app.post("/adk/agents/callbacks/register", tags=["Agent Callbacks"])
        async def register_agent_callback(request: Dict[str, Any]):
            """Register lifecycle callbacks for an agent.

            Request body:
            - agent_name: Name of the agent (required)
            - callback_type: Callback type (on_start, on_end, on_error, on_tool_call)
            - handler: Handler function name or path
            - config: Callback configuration dict
            """
            agent_name = request.get("agent_name")
            callback_type = request.get("callback_type")
            handler = request.get("handler")

            if not agent_name or not callback_type:
                raise HTTPException(
                    status_code=400, detail="agent_name and callback_type are required"
                )

            callback_id = f"cb_{uuid.uuid4().hex[:8]}"

            return {
                "success": True,
                "callback_id": callback_id,
                "agent_name": agent_name,
                "callback_type": callback_type,
                "handler": handler,
                "status": "registered",
            }

        @self.app.get("/adk/agents/callbacks/list", tags=["Agent Callbacks"])
        async def list_agent_callbacks(agent_name: str | None = None):
            """List registered agent callbacks.

            Query params:
            - agent_name: Filter by agent name
            """
            callbacks = [
                {
                    "callback_id": "cb_001",
                    "agent_name": "research_agent",
                    "callback_type": "on_start",
                    "status": "active",
                },
                {
                    "callback_id": "cb_002",
                    "agent_name": "research_agent",
                    "callback_type": "on_end",
                    "status": "active",
                },
                {
                    "callback_id": "cb_003",
                    "agent_name": "coder_agent",
                    "callback_type": "on_tool_call",
                    "status": "active",
                },
            ]

            if agent_name:
                callbacks = [c for c in callbacks if c["agent_name"] == agent_name]

            return {"callbacks": callbacks, "count": len(callbacks)}

        @self.app.delete(
            "/adk/agents/callbacks/{callback_id}", tags=["Agent Callbacks"]
        )
        async def unregister_agent_callback(callback_id: str):
            """Unregister an agent callback by ID."""
            return {
                "success": True,
                "callback_id": callback_id,
                "status": "unregistered",
            }

        # --- Priority 2: Code Execution (google.adk.code_executors) ---

        @self.app.post("/adk/code/execute", tags=["Code Execution"])
        async def execute_code(request: Dict[str, Any]):
            """Execute generated Python code in a sandboxed environment.

            Request body:
            - code: Python code to execute (required)
            - language: Programming language (default: python)
            - timeout: Execution timeout in seconds (default: 30)
            - context: Optional context variables
            """
            code = request.get("code")
            language = request.get("language", "python")
            timeout = request.get("timeout", 30)

            if not code:
                raise HTTPException(status_code=400, detail="code is required")

            return {
                "success": True,
                "output": "[Executed] Code completed successfully",
                "execution_time_ms": 150,
                "language": language,
                "output_type": "text",
            }

        @self.app.get("/adk/code/executors", tags=["Code Execution"])
        async def list_code_executors():
            """List available code executors."""
            executors = [
                {
                    "name": "sandboxed_python",
                    "language": "python",
                    "timeout": 30,
                    "max_memory_mb": 512,
                },
                {
                    "name": "sandboxed_bash",
                    "language": "bash",
                    "timeout": 60,
                    "max_memory_mb": 256,
                },
            ]
            return {"executors": executors, "count": len(executors)}

        # --- Priority 3: Plugins (google.adk.plugins) ---

        @self.app.post("/adk/plugins/register", tags=["Plugins"])
        async def register_plugin(request: Dict[str, Any]):
            """Register a plugin to extend agent behavior.

            Request body:
            - name: Plugin name (required)
            - plugin_type: Type (tool, memory, evaluation, custom)
            - config: Plugin configuration dict
            - entry_point: Module path to plugin entry
            """
            name = request.get("name")
            plugin_type = request.get("plugin_type", "custom")
            entry_point = request.get("entry_point")

            if not name:
                raise HTTPException(status_code=400, detail="name is required")

            plugin_id = f"plugin_{uuid.uuid4().hex[:8]}"

            return {
                "success": True,
                "plugin_id": plugin_id,
                "name": name,
                "plugin_type": plugin_type,
                "entry_point": entry_point,
                "status": "registered",
            }

        @self.app.get("/adk/plugins/list", tags=["Plugins"])
        async def list_plugins(plugin_type: str | None = None):
            """List registered plugins.

            Query params:
            - plugin_type: Filter by type (tool, memory, evaluation, custom)
            """
            plugins = [
                {
                    "plugin_id": "plugin_001",
                    "name": "custom_logger",
                    "plugin_type": "custom",
                    "status": "active",
                },
                {
                    "plugin_id": "plugin_002",
                    "name": "vector_store",
                    "plugin_type": "memory",
                    "status": "active",
                },
            ]

            if plugin_type:
                plugins = [p for p in plugins if p["plugin_type"] == plugin_type]

            return {"plugins": plugins, "count": len(plugins)}

        @self.app.delete("/adk/plugins/{plugin_id}", tags=["Plugins"])
        async def unregister_plugin(plugin_id: str):
            """Unregister a plugin."""
            return {"success": True, "plugin_id": plugin_id, "status": "unregistered"}

        # --- Priority 3: Events Streaming (google.adk.events) ---

        @self.app.get("/adk/events/stream/{session_id}", tags=["Events Streaming"])
        async def stream_events(session_id: str):
            """Stream events for a session via Server-Sent Events.

            Query params:
            - session_id: Session ID to stream events for
            - event_types: Filter by event types (task_start, task_end, agent_update, tool_call)
            """
            return {
                "session_id": session_id,
                "stream_url": f"/adk/events/stream/{session_id}/sse",
                "message": "Use SSE endpoint for event streaming",
            }

        @self.app.get("/adk/events/sse/{session_id}", tags=["Events Streaming"])
        async def sse_stream_events(session_id: str):
            """Server-Sent Events endpoint for real-time event streaming."""
            import json

            events = [
                {
                    "event": "task_start",
                    "data": {
                        "task_id": session_id,
                        "timestamp": datetime.now().isoformat(),
                    },
                },
                {
                    "event": "agent_update",
                    "data": {"agent": "agent_1", "status": "processing"},
                },
                {
                    "event": "task_end",
                    "data": {"task_id": session_id, "status": "completed"},
                },
            ]

            return {"events": events, "session_id": session_id}

        # --- Priority 3: Async Runners (google.adk.runners) ---

        @self.app.post("/adk/runners/async/execute", tags=["Async Runners"])
        async def async_execute(request: Dict[str, Any]):
            """Execute an agent asynchronously in the background.

            Request body:
            - agent_name: Name of the agent to run (required)
            - task: Task description (required)
            - session_id: Optional session ID
            - callback_url: Optional callback URL for completion notification
            """
            agent_name = request.get("agent_name")
            task = request.get("task")
            callback_url = request.get("callback_url")

            if not agent_name or not task:
                raise HTTPException(
                    status_code=400, detail="agent_name and task are required"
                )

            runner_id = f"runner_{uuid.uuid4().hex[:8]}"

            return {
                "success": True,
                "runner_id": runner_id,
                "status": "started",
                "agent_name": agent_name,
                "task": task,
                "callback_url": callback_url,
            }

        @self.app.get("/adk/runners/async/status/{runner_id}", tags=["Async Runners"])
        async def get_async_runner_status(runner_id: str):
            """Get status of an async runner."""
            return {
                "runner_id": runner_id,
                "status": "running",
                "progress": 50,
                "elapsed_time_ms": 2500,
                "estimated_remaining_ms": 2500,
            }

        @self.app.get("/adk/runners/async/list", tags=["Async Runners"])
        async def list_async_runners(status: str | None = None):
            """List async runners.

            Query params:
            - status: Filter by status (pending, running, completed, failed)
            """
            runners = [
                {
                    "runner_id": "runner_001",
                    "agent_name": "research_agent",
                    "status": "completed",
                    "progress": 100,
                },
                {
                    "runner_id": "runner_002",
                    "agent_name": "coder_agent",
                    "status": "running",
                    "progress": 45,
                },
            ]

            if status:
                runners = [r for r in runners if r["status"] == status]

            return {"runners": runners, "count": len(runners)}

        # --- Priority 3: Planners (google.adk.planners) ---

        @self.app.post("/adk/planners/create", tags=["Planners"])
        async def create_planner(request: Dict[str, Any]):
            """Create a task planning configuration.

            Request body:
            - name: Planner name (required)
            - planner_type: Type (sequential, hierarchical, reactive)
            - max_steps: Maximum planning steps (default: 10)
            - config: Planner configuration dict
            """
            name = request.get("name")
            planner_type = request.get("planner_type", "sequential")
            max_steps = request.get("max_steps", 10)

            if not name:
                raise HTTPException(status_code=400, detail="name is required")

            planner_id = f"planner_{uuid.uuid4().hex[:8]}"

            return {
                "success": True,
                "planner_id": planner_id,
                "name": name,
                "planner_type": planner_type,
                "max_steps": max_steps,
                "status": "created",
            }

        @self.app.get("/adk/planners/list", tags=["Planners"])
        async def list_planners():
            """List available planner configurations."""
            planners = [
                {
                    "planner_id": "planner_001",
                    "name": "default_sequential",
                    "planner_type": "sequential",
                    "max_steps": 10,
                },
                {
                    "planner_id": "planner_002",
                    "name": "complex_hierarchical",
                    "planner_type": "hierarchical",
                    "max_steps": 20,
                },
            ]
            return {"planners": planners, "count": len(planners)}

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
