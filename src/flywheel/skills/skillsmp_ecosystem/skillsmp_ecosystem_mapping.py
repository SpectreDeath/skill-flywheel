#!/usr/bin/env python3
"""
skillsmp-ecosystem-mapping

Maps Skill Flywheel domains to SkillsMP categories and occupations for skill alignment.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


DOMAIN_TO_CATEGORY = {
    "LLM_INTEGRATION": ("LLM & AI", "Frontend"),
    "ML_AI": ("Machine Learning", "Data Engineering"),
    "META_SKILL_DISCOVERY": ("LLM & AI", "Scripting"),
    "orchestration": ("Backend", "Automation Tools"),
    "DATABASE_ENGINEERING": ("SQL Databases", "Data Engineering"),
    "PRODUCTION_OPERATIONS": ("DevOps", "Monitoring"),
    "SECURITY_RESEARCH": ("Security",),
    "data_engineering": ("Data Engineering", "ETL"),
    "SME_INTEGRATION": ("LLM & AI", "Data Engineering", "Security"),
    "DEVOPS": ("CI/CD", "Cloud"),
}


CATEGORY_TO_OCCUPATION = {
    "LLM & AI": ["Software Developers", "AI Engineers"],
    "Machine Learning": ["Data Scientists", "ML Engineers"],
    "Frontend": ["Web Developers", "UI/UX Designers"],
    "Backend": ["Software Developers", "API Engineers"],
    "Security": ["Information Security Analysts", "Security Engineers"],
    "Data Engineering": ["Data Engineers", "Database Administrators"],
    "DevOps": ["Site Reliability Engineers", "DevOps Engineers"],
    "Automation Tools": ["Software Quality Assurance", "Test Engineers"],
}


def get_category_for_domain(domain: str) -> List[str]:
    """Get SkillsMP categories for a Skill Flywheel domain."""
    return list(DOMAIN_TO_CATEGORY.get(domain.upper(), ["General"]))


def get_occupations_for_category(category: str) -> List[str]:
    """Get relevant occupations for a SkillsMP category."""
    return CATEGORY_TO_OCCUPATION.get(category, [])


def get_skill_gaps(domain: str) -> List[Dict[str, str]]:
    """Identify skill gaps for a domain based on SkillsMP data."""
    gaps = []
    categories = get_category_for_domain(domain)
    for category in categories:
        occupations = get_occupations_for_category(category)
        gaps.append(
            {
                "domain": domain,
                "category": category,
                "target_occupations": occupations,
                "gap_level": "medium",
            }
        )
    return gaps


def skillsmp_ecosystem_mapping(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Core implementation for skillsmp-ecosystem-mapping."""
    action = payload.get("action", "map_domain")

    if action == "map_domain":
        domain = payload.get("domain", "")
        if not domain:
            return {"status": "error", "message": "domain required"}
        categories = get_category_for_domain(domain)
        occupations = []
        for cat in categories:
            occupations.extend(get_occupations_for_category(cat))
        return {
            "status": "success",
            "domain": domain,
            "skillsmp_categories": categories,
            "target_occupations": occupations,
        }

    elif action == "list_categories":
        return {"status": "success", "domain_mapping": DOMAIN_TO_CATEGORY}

    elif action == "analyze_gaps":
        domain = payload.get("domain", "")
        if not domain:
            return {"status": "error", "message": "domain required"}
        gaps = get_skill_gaps(domain)
        return {"status": "success", "gaps": gaps}

    return {"status": "error", "message": f"Unknown action: {action}"}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "map_domain")
    try:
        result = skillsmp_ecosystem_mapping(payload)
        return {
            "result": result,
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
    except Exception as e:
        logger.error(f"Error in skillsmp-ecosystem-mapping: {e}")
        return {"result": {"error": str(e)}, "metadata": {"action": action}}


def register_skill() -> Dict[str, str]:
    """Return skill metadata."""
    return {
        "name": "skillsmp-ecosystem-mapping",
        "description": "Maps Skill Flywheel domains to SkillsMP categories and occupations",
        "version": "1.0.0",
        "domain": "SKILLSMP_ECOSYSTEM",
    }
