#!/usr/bin/env python3
"""
ADK Bridge Module

Provides integration between the Skill Flywheel and ADK agents.
Enables progressive disclosure (L1/L2/L3) and skill generation.

Functions:
- list_adk_skills(): Returns L1 metadata for all skills
- generate_adk_skill(): Generates new ADK-compatible skills
- parse_skill_md(): Parses SKILL.md for ADK format
"""

import logging
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
DB_PATH = os.path.join(BASE_DIR, "data", "skill_registry.db")


def get_db() -> sqlite3.Connection:
    """Get SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def list_adk_skills(
    domain: Optional[str] = None, limit: int = 531
) -> List[Dict[str, Any]]:
    """L1: List all skills with metadata for ADK agents.

    Returns name and description (~100 tokens per skill) for skill discovery.
    This is the lightweight metadata loaded at startup.

    Args:
        domain: Optional domain filter
        limit: Maximum number of skills to return

    Returns:
        List of skill metadata dictionaries
    """
    try:
        with get_db() as db:
            cursor = db.cursor()
            query = "SELECT name, description, domain, version FROM skills"
            params = []
            if domain:
                query += " WHERE domain = ?"
                params.append(domain)
            query += " LIMIT ?"
            params.append(limit)
            cursor.execute(query, params)
            rows = cursor.fetchall()

            return [
                {
                    "name": row["name"],
                    "description": row.get("description", "")[:256],
                    "domain": row.get("domain", "general").lower(),
                    "version": row.get("version", "1.0.0"),
                }
                for row in rows
            ]
    except Exception as e:
        logger.error(f"Error listing ADK skills: {e}")
        return []


def get_skill_instructions(skill_name: str) -> Dict[str, Any]:
    """L2: Get full skill instructions for ADK agents.

    Loads the full SKILL.md from domains/ directory.

    Args:
        skill_name: Name of the skill to load

    Returns:
        Dictionary with skill metadata and instructions
    """
    base_dir = BASE_DIR
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
        raise FileNotFoundError(f"Skill not found: {skill_name}")

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
        "name": frontmatter.get("name", skill_name),
        "description": frontmatter.get("description", "")[:1024],
        "domain": frontmatter.get("domain", "general").lower(),
        "version": frontmatter.get("version", "1.0.0"),
        "instructions": body,
        "skill_path": str(skill_path),
    }


def get_skill_resource(skill_name: str, resource_name: str) -> Dict[str, Any]:
    """L3: Load external resource file for a skill.

    Returns content from references/, assets/, or scripts/ directories.

    Args:
        skill_name: Name of the skill
        resource_name: Name of the resource file

    Returns:
        Dictionary with resource content
    """
    base_dir = BASE_DIR
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
                                "name": resource_name,
                                "content": content,
                                "path": str(resource_path.relative_to(base_dir)),
                            }
                        except Exception as e:
                            raise OSError(f"Error reading resource: {e}")

    raise FileNotFoundError(f"Resource not found: {resource_name}")


async def generate_adk_skill(
    name: str,
    description: str,
    domain: str,
    instructions: str,
) -> Dict[str, Any]:
    """Skill Factory: Generate new skill from requirements.

    Creates ADK-compatible skills following the Agent Skills specification.
    Generates both SKILL.md and Python module.

    Args:
        name: Skill name (kebab-case)
        description: Skill description
        domain: Domain category
        instructions: Skill instructions

    Returns:
        Dictionary with generated skill info
    """
    import uuid

    domain_dir = Path(BASE_DIR) / "domains" / f"SKILL.{name}"
    domain_dir.mkdir(parents=True, exist_ok=True)

    skill_md_path = domain_dir / "SKILL.md"
    frontmatter = f"""---
name: {name}
description: {description}
domain: {domain}
version: 1.0.0
---

# {name.replace("-", " ").title()}

{description}

## Instructions

{instructions}
"""
    skill_md_path.write_text(frontmatter, encoding="utf-8")

    skills_dir = Path(BASE_DIR) / "src" / "flywheel" / "skills" / domain.upper()
    skills_dir.mkdir(parents=True, exist_ok=True)

    init_file = skills_dir / "__init__.py"
    if not init_file.exists():
        init_file.touch()

    safe_name_val = name.lower().replace("-", "_")
    py_path = skills_dir / f"{safe_name_val}.py"

    py_code = f'''#!/usr/bin/env python3
"""
{name}

{description}
"""

import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


def {safe_name_val}(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Core implementation for {name}."""
    return {{
        "action": "{name}",
        "status": "success",
        "message": "{name} executed",
    }}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "default")
    try:
        if action == "default":
            result = {{
                "action": action,
                "status": "success",
                "message": "Skill executed successfully",
            }}
        else:
            result = {{
                "error": f"Unknown action: {{action}}",
            }}

        return {{
            "result": result,
            "metadata": {{
                "action": action,
                "timestamp": datetime.now().isoformat(),
            }},
        }}
    except Exception as e:
        logger.error(f"Error in {name}: {{e}}")
        return {{
            "result": {{"error": str(e)}},
            "metadata": {{
                "action": action,
                "timestamp": datetime.now().isoformat(),
            }},
        }}


def register_skill() -> Dict[str, str]:
    """Return skill metadata."""
    return {{
        "name": "{name}",
        "description": "{description}",
        "version": "1.0.0",
        "domain": "{domain.upper()}",
    }}
'''

    py_path.write_text(py_code, encoding="utf-8")

    try:
        with get_db() as db:
            cursor = db.cursor()
            skill_id = str(uuid.uuid4())

            cursor.execute(
                """INSERT OR REPLACE INTO skills
                   (skill_id, name, domain, module_path, entry_function, version, description)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    skill_id,
                    name,
                    domain,
                    f"flywheel.skills.{domain.upper()}.{safe_name_val}",
                    "invoke",
                    "1.0.0",
                    description,
                ),
            )
    except Exception as e:
        logger.warning(f"Could not register skill in DB: {e}")

    return {
        "success": True,
        "name": name,
        "description": description,
        "domain": domain,
        "skill_path": str(skill_md_path),
        "module_path": str(py_path),
        "message": f"Skill '{name}' generated successfully",
    }


def parse_skill_md(content: str) -> Dict[str, Any]:
    """Parse SKILL.md content for ADK format.

    Args:
        content: Raw SKILL.md content

    Returns:
        Dictionary with parsed frontmatter and body
    """
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
        "frontmatter": frontmatter,
        "body": body,
    }


def check_hardware_optimization(
    hardware_hint: Optional[str],
) -> Optional[Dict[str, Any]]:
    """Check if hardware hint suggests predictive preloading.

    Args:
        hardware_hint: Hardware identifier (e.g., 'GTX 1660 Ti')

    Returns:
        Optimization recommendation if applicable
    """
    if not hardware_hint:
        return None

    hw_upper = hardware_hint.upper()

    if "1660" in hw_upper or "GTX" in hw_upper:
        return {
            "gpu": hardware_hint,
            "predictive_preload": True,
            "reason": "GPU-bound domain detected, preloading recommended",
            "optimization_level": "aggressive",
        }

    if "RTX" in hw_upper:
        return {
            "gpu": hardware_hint,
            "predictive_preload": True,
            "reason": "RTX GPU detected, enabling full ML optimization",
            "optimization_level": "full",
        }

    return None


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation for ADK bridge operations.

    Supports actions:
    - list_skills: Return L1 metadata
    - get_skill: Return L2 instructions
    - get_resource: Return L3 resource
    - generate: Create new skill
    """
    action = payload.get("action", "list_skills")
    try:
        if action == "list_skills":
            domain = payload.get("domain")
            limit = payload.get("limit", 531)
            result = list_adk_skills(domain=domain, limit=limit)
            return {
                "result": result,
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        elif action == "get_skill":
            skill_name = payload.get("skill_name")
            if not skill_name:
                return {
                    "result": {"error": "skill_name required"},
                    "metadata": {
                        "action": action,
                        "timestamp": datetime.now().isoformat(),
                    },
                }
            result = get_skill_instructions(skill_name)
            return {
                "result": result,
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        elif action == "get_resource":
            skill_name = payload.get("skill_name")
            resource_name = payload.get("resource_name")
            if not skill_name or not resource_name:
                return {
                    "result": {"error": "skill_name and resource_name required"},
                    "metadata": {
                        "action": action,
                        "timestamp": datetime.now().isoformat(),
                    },
                }
            result = get_skill_resource(skill_name, resource_name)
            return {
                "result": result,
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        elif action == "generate":
            name = payload.get("name")
            description = payload.get("description", "")
            domain = payload.get("domain", "general")
            instructions = payload.get("instructions", "")
            if not name:
                return {
                    "result": {"error": "name required"},
                    "metadata": {
                        "action": action,
                        "timestamp": datetime.now().isoformat(),
                    },
                }
            result = await generate_adk_skill(name, description, domain, instructions)
            return {
                "result": result,
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        elif action == "check_hardware":
            hardware_hint = payload.get("hardware_hint")
            result = check_hardware_optimization(hardware_hint)
            return {
                "result": result or {},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error(f"Error in ADK bridge: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }


def register_skill() -> Dict[str, str]:
    """Return skill metadata."""

if __name__ == "__main__":
    return {
            "name": "adk-bridge",
            "description": "ADK Skills integration bridge with L1/L2/L3 progressive disclosure",
            "version": "1.0.0",
            "domain": "INTEGRATION",
        }