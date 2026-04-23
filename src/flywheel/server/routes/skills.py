from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from flywheel.server.config import ServerConfig

router = APIRouter(prefix="", tags=["Discovery"])

config = ServerConfig()


def get_db():
    """Get SQLite database connection"""
    import sqlite3

    db_path = config.config.get("database", {}).get("path", "data/skill_registry.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@router.get("/skills")
async def list_skills(
    domain: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """List skills from the SQLite registry"""
    try:
        with get_db() as db:
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


@router.get("/skills/search")
async def search_skills(q: str = Query(..., min_length=2)):
    """Semantic/Text search for skills in the DB"""
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM skills WHERE name LIKE ? OR description LIKE ? OR purpose LIKE ?",
                (f"%{q}%", f"%{q}%", f"%{q}%"),
            )
            results = [dict(row) for row in cursor.fetchall()]
            return {"query": q, "results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {e}")


@router.get("/domains")
async def list_domains():
    """List all unique domains and their skill counts"""
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT domain, COUNT(*) as count FROM skills GROUP BY domain"
            )
            domains = [dict(row) for row in cursor.fetchall()]
            return {"domains": domains}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
