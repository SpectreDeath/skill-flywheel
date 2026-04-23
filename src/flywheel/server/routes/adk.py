from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Query
from flywheel.server.config import ServerConfig

router = APIRouter(prefix="/adk", tags=["ADK Skills"])

config = ServerConfig()


def get_db():
    """Get SQLite database connection"""
    import sqlite3

    db_path = config.config.get("database", {}).get("path", "data/skill_registry.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@router.get("/skills")
async def adk_list_skills(
    domain: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
):
    """L1: List all skills with metadata for ADK agents."""
    base_dir = Path(config.config.get("base_dir", ""))
    try:
        with get_db() as db:
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


@router.get("/skills/{skill_name}")
async def adk_get_skill(
    skill_name: str,
    include_resources: bool = Query(False),
    hardware_hint: Optional[str] = Query(None),
):
    """L2: Get full skill instructions for ADK agents."""
    base_dir = Path(config.config.get("base_dir", ""))
    domains_dir = base_dir / "domains"

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
        raise HTTPException(status_code=404, detail=f"Skill not found: {skill_name}")

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


@router.get("/skills/{skill_name}/resource/{resource_name}")
async def adk_get_resource(skill_name: str, resource_name: str):
    """L3: Load external resource file for a skill."""
    base_dir = Path(config.config.get("base_dir", ""))
    domains_dir = base_dir / "domains"

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
                            status_code=500, detail=f"Error reading resource: {e}"
                        )

    raise HTTPException(status_code=404, detail=f"Resource not found: {resource_name}")


@router.post("/skills/generate")
async def adk_generate_skill(request: Dict[str, Any]):
    """Skill Factory: Generate new skill from requirements."""
    try:
        from flywheel.integration.adk_bridge import generate_adk_skill
    except ImportError:
        raise HTTPException(status_code=500, detail="ADK bridge not available")

    name = request.get("name")
    description = request.get("description") or ""
    domain = request.get("domain", "general")
    instructions = request.get("instructions", "")

    if not name:
        raise HTTPException(status_code=400, detail="name is required")

    try:
        result = await generate_adk_skill(name, description, domain, instructions)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skill generation failed: {e}")


@router.get("/toolset")
async def adk_toolset_info():
    """Generate SkillToolset config for external ADK agents."""
    try:
        from flywheel.integration.adk_bridge import list_adk_skills
    except ImportError:
        raise HTTPException(status_code=500, detail="ADK bridge not available")

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


@router.get("/tools/list_skills")
async def adk_tool_list_skills(
    domain: Optional[str] = None,
    limit: int = Query(100, ge=1, le=500),
):
    """ADK Tool: list_skills"""
    try:
        with get_db() as db:
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


@router.get("/tools/load_skill")
async def adk_tool_load_skill(
    name: str = Query(..., description="Skill name to load"),
    include_resources: bool = Query(False),
):
    """ADK Tool: load_skill"""
    base_dir = Path(config.config.get("base_dir", ""))
    domains_dir = base_dir / "domains"

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


@router.get("/tools/load_skill_resource")
async def adk_tool_load_resource(
    skill_name: str = Query(..., description="Skill name"),
    resource_name: str = Query(..., description="Resource file name"),
):
    """ADK Tool: load_skill_resource"""

if __name__ == "__main__":
    base_dir = Path(config.config.get("base_dir", ""))
        domains_dir = base_dir / "domains"

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
                                "resource": {
                                    "name": resource_name,
                                    "content": content,
                                    "path": str(resource_path.relative_to(base_dir)),
                                },
                                "tool": "load_skill_resource",
                                "level": "L3",
                            }
                        except Exception as e:
                            raise HTTPException(
                                status_code=500, detail=f"Error reading resource: {e}"
                            )

        raise HTTPException(status_code=404, detail=f"Resource not found: {resource_name}")