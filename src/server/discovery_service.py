from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import importlib.util
import time
from datetime import datetime
import json
import os
import sys

# Change default path depending on if run via uvicorn from root or within src/discovery
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DB_PATH = os.path.join(BASE_DIR, 'data', 'skill_registry.db')

app = FastAPI(title="Skill Flywheel Discovery Service")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Module Cache for skills parsed > 10 times
module_cache = {}

class InvokePayload(BaseModel):
    args: list = []
    kwargs: dict = {}

@app.on_event("startup")
async def startup_event():
    # Load registry from DB (ensure connection works)
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM skills")
            app.state.registry_loaded = True
            print(f"Loaded registry from {DB_PATH}: {cursor.fetchone()[0]} skills active.")
    except Exception as e:
        print(f"Failed to load registry from {DB_PATH}: {e}")
        app.state.registry_loaded = False

@app.get("/health")
async def health():
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM skills")
            total_skills = cursor.fetchone()["total"]
            
            cursor.execute("SELECT COUNT(*) as healthy FROM skills WHERE health_status = 'healthy'")
            healthy_skills = cursor.fetchone()["healthy"]
            
        return {
            "status": "up",
            "registry_stats": {
                "total_skills": total_skills,
                "healthy_skills": healthy_skills
            }
        }
    except Exception as e:
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
            
            cursor.execute("SELECT COUNT(*) as healthy FROM skills WHERE health_status = 'healthy'")
            healthy_skills = cursor.fetchone()["healthy"]
            
            cursor.execute("SELECT COUNT(*) as unhealthy FROM skills WHERE health_status = 'unhealthy'")
            unhealthy_skills = cursor.fetchone()["unhealthy"]
            
            cursor.execute("SELECT COUNT(*) as unknown FROM skills WHERE health_status = 'unknown'")
            unknown_skills = cursor.fetchone()["unknown"]
            
            # Get recent activity
            cursor.execute("SELECT COUNT(*) as recent_invocations FROM skills WHERE last_invoked > datetime('now', '-1 hour')")
            recent_invocations = cursor.fetchone()["recent_invocations"]
            
            # Get skill domains
            cursor.execute("SELECT DISTINCT domain FROM skills")
            domains = [row["domain"] for row in cursor.fetchall()]
            
            # Calculate health percentage
            health_percentage = (healthy_skills / total_skills * 100) if total_skills > 0 else 0
            
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "system_overview": {
                    "total_skills": total_skills,
                    "healthy_skills": healthy_skills,
                    "unhealthy_skills": unhealthy_skills,
                    "unknown_skills": unknown_skills,
                    "health_percentage": round(health_percentage, 2)
                },
                "activity": {
                    "recent_invocations_last_hour": recent_invocations
                },
                "domains": domains,
                "database": {
                    "path": DB_PATH,
                    "accessible": True
                }
            }
            
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "database": {
                "path": DB_PATH,
                "accessible": False
            }
        }

@app.get("/skills")
async def list_skills(page: int = 1, limit: int = 20):
    """
    List skills with pagination support.
    
    Args:
        page: Page number (1-based), defaults to 1
        limit: Number of skills per page, defaults to 20
    
    Returns:
        Paginated list of skills with metadata
    """
    if page < 1:
        page = 1
    if limit < 1:
        limit = 20
    elif limit > 100:
        limit = 100  # Maximum limit to prevent overwhelming responses
        
    offset = (page - 1) * limit
    
    with get_db() as db:
        cursor = db.cursor()
        
        # Get total count for pagination metadata
        cursor.execute("SELECT COUNT(*) FROM skills")
        total_count = cursor.fetchone()[0]
        
        # Get paginated skills
        cursor.execute(
            "SELECT skill_id, name, domain, version, health_status FROM skills ORDER BY name LIMIT ? OFFSET ?",
            (limit, offset)
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
                "has_prev": has_prev
            }
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
        skill["dependencies"] = json.loads(skill["dependencies"]) if skill["dependencies"] else []
        
        cursor.execute("SELECT * FROM skill_endpoints WHERE skill_id = ?", (skill_id,))
        endpoints = cursor.fetchall()
        skill["endpoints"] = [dict(ep) for ep in endpoints]
        
        return skill

@app.post("/skills/{skill_id}/invoke")
async def invoke_skill(skill_id: str, payload: InvokePayload):
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
        if module_path.endswith('.py'):
            rel_path = module_path
        else:
            rel_path = module_path.replace('.', os.sep) + '.py'
            
        abs_path = os.path.join(BASE_DIR, rel_path)
        
        if not os.path.exists(abs_path):
            raise HTTPException(status_code=500, detail=f"Module file not found at {abs_path}")
            
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
            cursor.execute('''
                UPDATE skills 
                SET invocation_count = ?, last_invoked = ? 
                WHERE skill_id = ?
            ''', (new_count, now, skill_id))
            db.commit()
            
            # Cache module if invocation_count hits rule threshold requirement > 10
            if new_count > 10 and module_name not in module_cache:
                module_cache[module_name] = module
                
            return {"status": "success", "result": result}
            
        except AttributeError:
             raise HTTPException(status_code=500, detail=f"Entry function '{entry_function}' not found in {module_path}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")

@app.get("/metrics")
async def get_metrics():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT skill_id, name, invocation_count, health_status, last_invoked FROM skills ORDER BY invocation_count DESC")
        rows = cursor.fetchall()
        return {"skills_metrics": [dict(row) for row in rows]}
