import importlib.util
import json
import logging
import os
import sqlite3
import time
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Change default path depending on if run via uvicorn from root or within src/discovery
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DB_PATH = os.path.join(BASE_DIR, "data", "skill_registry.db")

app = FastAPI(
    title="Skill Flywheel Discovery Service",
    description="""
    Skill Flywheel is a unified skill registry system that provides:
    
    - **Skill Discovery**: Find and list available skills
    - **Skill Execution**: Execute skills via MCP protocol
    - **Domain Management**: Organize skills by domain
    - **Metrics**: Monitor skill usage and performance
    
    ## Features
    
    - Multi-agent orchestration with LangChain and CrewAI
    - ML-driven predictive skill loading
    - Resource-aware optimization
    - Container-based scaling
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Module Cache for skills parsed > 10 times
module_cache = {}

# Constants
DEFAULT_LIMIT = 100
CACHE_THRESHOLD = 10
MIN_JWT_SECRET_LENGTH = 32

# Placeholder values that should be replaced in production
INSECURE_SECRET_PATTERNS = [
    "your-openai-api-key-here",
    "your-gemini-api-key-here",
    "your-secure-jwt-secret",
    "your_openai_api_key_here",
    "your_gemini_api_key_here",
    "your_jwt_secret_here",
    "test-key-for-local-development",
    "test-gemini-key-for-local-development",
    "test-jwt-secret-key-for-local-development",
]


def _validate_secrets() -> list:
    """Check for insecure secret values and return warnings"""
    warnings = []
    from dotenv import load_dotenv

    load_dotenv()

    # Check OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY", "")
    if any(pattern in openai_key.lower() for pattern in INSECURE_SECRET_PATTERNS):
        warnings.append("OPENAI_API_KEY appears to be a placeholder value")

    # Check Gemini API key
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    if any(pattern in gemini_key.lower() for pattern in INSECURE_SECRET_PATTERNS):
        warnings.append("GEMINI_API_KEY appears to be a placeholder value")

    # Check JWT secret
    jwt_secret = os.getenv("MCP_JWT_SECRET", "")
    if any(pattern in jwt_secret.lower() for pattern in INSECURE_SECRET_PATTERNS):
        warnings.append("MCP_JWT_SECRET appears to be a placeholder value")
    elif jwt_secret and len(jwt_secret) < MIN_JWT_SECRET_LENGTH:
        warnings.append(
            "MCP_JWT_SECRET is too short (minimum 32 characters recommended)"
        )

    return warnings


class InvokePayload(BaseModel):
    args: list = []
    kwargs: dict = {}


@app.on_event("startup")
async def startup_event():
    # Validate secrets before starting
    secret_warnings = _validate_secrets()
    if secret_warnings:
        for warning in secret_warnings:
            logger.warning(f"Security: {warning}")
        logger.warning("Security: These values should be changed in production!")

    # Load registry from DB (ensure connection works)
    logger.info("Starting Skill Flywheel Discovery Service...")
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM skills")
            skill_count = cursor.fetchone()[0]
            app.state.registry_loaded = True
            logger.info(f"Loaded registry from {DB_PATH}: {skill_count} skills active.")
    except Exception as e:
        logger.error(f"Failed to load registry from {DB_PATH}: {e}")
        app.state.registry_loaded = False


@app.get("/health", tags=["Health"])
async def health():
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM skills")
            total_skills = cursor.fetchone()["total"]

            cursor.execute(
                "SELECT COUNT(*) as healthy FROM skills WHERE health_status = 'healthy'"
            )
            healthy_skills = cursor.fetchone()["healthy"]

        logger.debug(f"Health check: {total_skills} total, {healthy_skills} healthy")
        return {
            "status": "up",
            "registry_stats": {
                "total_skills": total_skills,
                "healthy_skills": healthy_skills,
            },
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "down", "error": str(e)}


@app.get("/health/detailed", tags=["Health"])
async def detailed_health():
    """Detailed health check endpoint that provides comprehensive system status"""
    try:
        with get_db() as db:
            cursor = db.cursor()

            # Get overall system health
            cursor.execute("SELECT COUNT(*) as total FROM skills")
            total_skills = cursor.fetchone()["total"]

            cursor.execute(
                "SELECT COUNT(*) as healthy FROM skills WHERE health_status = 'healthy'"
            )
            healthy_skills = cursor.fetchone()["healthy"]

            cursor.execute(
                "SELECT COUNT(*) as unhealthy FROM skills WHERE health_status = 'unhealthy'"
            )
            unhealthy_skills = cursor.fetchone()["unhealthy"]

            cursor.execute(
                "SELECT COUNT(*) as unknown FROM skills WHERE health_status = 'unknown'"
            )
            unknown_skills = cursor.fetchone()["unknown"]

            # Get recent activity
            cursor.execute(
                "SELECT COUNT(*) as recent_invocations FROM skills WHERE last_invoked > datetime('now', '-1 hour')"
            )
            recent_invocations = cursor.fetchone()["recent_invocations"]

            # Get skill domains
            cursor.execute("SELECT DISTINCT domain FROM skills")
            domains = [row["domain"] for row in cursor.fetchall()]

            # Calculate health percentage
            health_percentage = (
                (healthy_skills / total_skills * 100) if total_skills > 0 else 0
            )

            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "system_overview": {
                    "total_skills": total_skills,
                    "healthy_skills": healthy_skills,
                    "unhealthy_skills": unhealthy_skills,
                    "unknown_skills": unknown_skills,
                    "health_percentage": round(health_percentage, 2),
                },
                "activity": {"recent_invocations_last_hour": recent_invocations},
                "domains": domains,
                "database": {"path": DB_PATH, "accessible": True},
            }

    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "database": {"path": DB_PATH, "accessible": False},
        }


@app.get("/skills", tags=["Skills"])
@app.get("/skills/search", tags=["Skills"])
@app.get("/skills/domain/{domain}", tags=["Skills"])
@app.get("/skills/{skill_id}", tags=["Skills"])
@app.post("/skills/{skill_id}/invoke", tags=["Skills"])
@app.get("/metrics", tags=["Metrics"])
@app.get("/domains", tags=["Domains"])
@app.put("/skills/{skill_id}/health", tags=["Health"])
async def update_health_status(skill_id: str, health_status: str):
    """Update health status for a skill"""
    valid_statuses = ["healthy", "unhealthy", "unknown"]

    if health_status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid health status. Must be one of: {valid_statuses}",
        )

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT skill_id FROM skills WHERE skill_id = ?", (skill_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Skill not found")

        cursor.execute(
            "UPDATE skills SET health_status = ? WHERE skill_id = ?",
            (health_status, skill_id),
        )
        db.commit()

        return {
            "skill_id": skill_id,
            "health_status": health_status,
            "status": "updated",
        }
