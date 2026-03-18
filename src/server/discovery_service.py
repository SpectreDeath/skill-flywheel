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

app = FastAPI(title="Skill Flywheel Discovery Service")


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


@app.get("/health")
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


@app.get("/health/detailed")
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


@app.get("/skills")
async def list_skills(page: int = 1, limit: int = 20):
    """
    List skills with pagination support.

    Args:
        page: Page number (1-based), defaults to 1
        limit: Number of skills per page, defaults to 20

    Returns:
        dict with:
            - "skills": list of skill dicts with keys: skill_id, name, domain, version, health_status
            - "pagination": dict with page, limit, total, total_pages, has_next, has_prev
    """
    if page < 1:
        page = 1
    if limit < 1:
        limit = 20
    elif limit > DEFAULT_LIMIT:
        limit = DEFAULT_LIMIT  # Maximum limit to prevent overwhelming responses

    offset = (page - 1) * limit

    with get_db() as db:
        cursor = db.cursor()

        # Get total count for pagination metadata
        cursor.execute("SELECT COUNT(*) FROM skills")
        total_count = cursor.fetchone()[0]

        # Get paginated skills
        cursor.execute(
            "SELECT skill_id, name, domain, version, health_status FROM skills ORDER BY name LIMIT ? OFFSET ?",
            (limit, offset),
        )
        rows = cursor.fetchall()

        # Calculate pagination metadata
        total_pages = (total_count + limit - 1) // limit  # Ceiling division
        has_next = page < total_pages
        has_prev = page > 1

        return {
            "skills": [dict(row) for row in rows],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "total_pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev,
            },
        }


@app.get("/skills/search")
async def search_skills(q: str = "", domain: str = "", page: int = 1, limit: int = 20):
    """Search skills by name or description"""
    if page < 1:
        page = 1
    if limit < 1:
        limit = 20
    elif limit > DEFAULT_LIMIT:
        limit = DEFAULT_LIMIT

    offset = (page - 1) * limit

    with get_db() as db:
        cursor = db.cursor()

        query = "SELECT skill_id, name, domain, version, health_status, description FROM skills WHERE 1=1"
        params = []

        if q:
            query += " AND (name LIKE ? OR description LIKE ?)"
            search_term = f"%{q}%"
            params.extend([search_term, search_term])

        if domain:
            query += " AND domain = ?"
            params.append(domain)

        count_query = query.replace(
            "SELECT skill_id, name, domain, version, health_status, description",
            "SELECT COUNT(*)",
        )
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]

        query += " ORDER BY name LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()

        total_pages = (total_count + limit - 1) // limit

        return {
            "skills": [dict(row) for row in rows],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
            },
        }


@app.get("/skills/domain/{domain}")
async def get_skills_by_domain(domain: str, page: int = 1, limit: int = 20):
    """Get skills by domain"""
    if page < 1:
        page = 1
    if limit < 1:
        limit = 20
    elif limit > DEFAULT_LIMIT:
        limit = DEFAULT_LIMIT

    offset = (page - 1) * limit

    with get_db() as db:
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(*) FROM skills WHERE domain = ?", (domain,))
        total_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT skill_id, name, domain, version, health_status FROM skills WHERE domain = ? ORDER BY name LIMIT ? OFFSET ?",
            (domain, limit, offset),
        )
        rows = cursor.fetchall()

        total_pages = (total_count + limit - 1) // limit

        return {
            "domain": domain,
            "skills": [dict(row) for row in rows],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
            },
        }


@app.get("/skills/{skill_id}")
async def get_skill(skill_id: str):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM skills WHERE skill_id = ?", (skill_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Skill not found")

        skill = dict(row)
        skill["dependencies"] = (
            json.loads(skill["dependencies"]) if skill["dependencies"] else []
        )

        cursor.execute("SELECT * FROM skill_endpoints WHERE skill_id = ?", (skill_id,))
        endpoints = cursor.fetchall()
        skill["endpoints"] = [dict(ep) for ep in endpoints]

        return skill


@app.post("/skills/{skill_id}/invoke")
async def invoke_skill(skill_id: str, payload: InvokePayload):
    logger.info(f"Invoking skill: {skill_id}")
    start_time = time.time()

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM skills WHERE skill_id = ?", (skill_id,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Skill not found")

        module_path = row["module_path"]
        entry_function = row["entry_function"]
        invocation_count = row["invocation_count"]

        # Determine the absolute python file path
        # Normalize the module_path to find the file
        if module_path.endswith(".py"):
            rel_path = module_path
        else:
            rel_path = module_path.replace(".", os.sep) + ".py"

        abs_path = os.path.join(BASE_DIR, rel_path)

        if not os.path.exists(abs_path):
            raise HTTPException(
                status_code=500, detail=f"Module file not found at {abs_path}"
            )

        module_name = f"skill_{skill_id}"

        try:
            # Check cache
            if module_name in module_cache:
                module = module_cache[module_name]
            else:
                spec = importlib.util.spec_from_file_location(module_name, abs_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

            # Execute entry function
            func = getattr(module, entry_function)

            # Certain functions may be async
            import asyncio

            if asyncio.iscoroutinefunction(func):
                result = await func(*payload.args, **payload.kwargs)
            else:
                result = func(*payload.args, **payload.kwargs)

            # Update DB details incrementally
            new_count = invocation_count + 1
            now = datetime.utcnow().isoformat()
            cursor.execute(
                """
                UPDATE skills 
                SET invocation_count = ?, last_invoked = ? 
                WHERE skill_id = ?
            """,
                (new_count, now, skill_id),
            )
            db.commit()

            # Cache module if invocation_count hits rule threshold
            if new_count > CACHE_THRESHOLD and module_name not in module_cache:
                module_cache[module_name] = module

            duration = time.time() - start_time
            logger.info(f"Skill {skill_id} invoked successfully in {duration:.3f}s")
            return {"status": "success", "result": result}

        except AttributeError as e:
            logger.error(f"Skill {skill_id} attribute error: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Entry function '{entry_function}' not found in {module_path}",
            )
        except Exception as e:
            logger.error(f"Skill {skill_id} execution failed: {e}")
            raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@app.get("/metrics")
async def get_metrics():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT skill_id, name, invocation_count, health_status, last_invoked FROM skills ORDER BY invocation_count DESC"
        )
        rows = cursor.fetchall()
        return {"skills_metrics": [dict(row) for row in rows]}


@app.get("/domains")
async def list_domains():
    """List all available domains with skill counts"""
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT domain, COUNT(*) as skill_count 
            FROM skills 
            GROUP BY domain 
            ORDER BY skill_count DESC
        """)
        rows = cursor.fetchall()
        return {
            "domains": [
                {"name": row["domain"], "skill_count": row["skill_count"]}
                for row in rows
            ]
        }


@app.put("/skills/{skill_id}/health")
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
