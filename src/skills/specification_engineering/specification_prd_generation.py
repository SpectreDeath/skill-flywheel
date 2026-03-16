import time
import logging
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


def generate_prd_sections(project_info: Dict[str, Any]) -> Dict[str, Any]:
    sections = {
        "title": project_info.get("title", "Product Requirements Document"),
        "version": "1.0.0",
        "date": datetime.now().isoformat(),
    }

    sections["executive_summary"] = project_info.get(
        "description", "This document outlines the requirements for the project."
    )

    sections["problem_statement"] = project_info.get(
        "problem", "Address the following challenges:"
    )
    sections["opportunity"] = project_info.get(
        "opportunity", "This project provides an opportunity to:"
    )

    sections["stakeholders"] = [
        {"name": "Product Owner", "role": "Defines requirements"},
        {"name": "Development Team", "role": "Implements features"},
        {"name": "Quality Assurance", "role": "Tests functionality"},
    ]

    sections["user_personas"] = [
        {
            "name": "Primary User",
            "goals": "Accomplish tasks efficiently",
            "pain_points": "Current solutions are too slow",
        }
    ]

    sections["functional_requirements"] = []
    requirements = project_info.get("requirements", [])
    for req in requirements:
        sections["functional_requirements"].append(
            {
                "id": "REQ-{:03d}".format(len(sections["functional_requirements"]) + 1),
                "description": req,
                "priority": "High",
                "status": "Proposed",
            }
        )

    sections["non_functional_requirements"] = [
        {"category": "Performance", "requirement": "System responds within 2 seconds"},
        {
            "category": "Security",
            "requirement": "Data encrypted at rest and in transit",
        },
        {"category": "Usability", "requirement": "User-friendly interface"},
    ]

    sections["user_stories"] = [
        {
            "id": "US-001",
            "story": "As a user, I want to",
            "acceptance_criteria": "Given when then format",
        }
    ]

    sections["milestones"] = [
        {"name": "Alpha Release", "date": "TBD", "deliverables": "Core features"},
        {"name": "Beta Release", "date": "TBD", "deliverables": "Full feature set"},
        {
            "name": "Production Release",
            "date": "TBD",
            "deliverables": "Production-ready system",
        },
    ]

    sections["risks"] = [
        {
            "risk": "Technical complexity",
            "mitigation": "Proof of concept before full implementation",
        },
        {"risk": "Timeline delays", "mitigation": "Regular progress reviews"},
    ]

    return sections


def format_prd_document(sections: Dict[str, Any]) -> str:
    doc = []

    doc.append("# {}".format(sections.get("title", "Product Requirements Document")))
    doc.append("")
    doc.append("**Version:** {}".format(sections.get("version", "1.0.0")))
    doc.append("**Date:** {}".format(sections.get("date", datetime.now().isoformat())))
    doc.append("")

    doc.append("## Executive Summary")
    doc.append("")
    doc.append(sections.get("executive_summary", ""))
    doc.append("")

    doc.append("## Problem Statement")
    doc.append("")
    doc.append(sections.get("problem_statement", ""))
    doc.append("")

    doc.append("## Stakeholders")
    doc.append("")
    for stakeholder in sections.get("stakeholders", []):
        doc.append(
            "- **{}**: {}".format(
                stakeholder.get("name", ""), stakeholder.get("role", "")
            )
        )
    doc.append("")

    doc.append("## Functional Requirements")
    doc.append("")
    for req in sections.get("functional_requirements", []):
        doc.append("### {} {}".format(req.get("id", ""), req.get("description", "")))
        doc.append("- Priority: {}".format(req.get("priority", "")))
        doc.append("")

    doc.append("## Non-Functional Requirements")
    doc.append("")
    for req in sections.get("non_functional_requirements", []):
        doc.append(
            "- **{}**: {}".format(req.get("category", ""), req.get("requirement", ""))
        )
    doc.append("")

    return "\n".join(doc)


def validate_prd_completeness(prd: Dict[str, Any]) -> Dict[str, Any]:
    required_sections = [
        "title",
        "executive_summary",
        "functional_requirements",
        "non_functional_requirements",
        "milestones",
    ]

    missing = []
    for section in required_sections:
        if section not in prd or not prd[section]:
            missing.append(section)

    completeness = (
        (len(required_sections) - len(missing)) / len(required_sections) * 100
    )

    return {
        "complete": len(missing) == 0,
        "missing_sections": missing,
        "completeness_score": round(completeness, 2),
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "generate")

    try:
        if action == "generate":
            project_info = payload.get("project_info", {})
            sections = generate_prd_sections(project_info)

            return {
                "result": sections,
                "metadata": {
                    "action": "generate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "format":
            sections = payload.get("sections", {})
            doc = format_prd_document(sections)
            return {
                "result": {"document": doc},
                "metadata": {
                    "action": "format",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "validate":
            prd = payload.get("prd", {})
            result = validate_prd_completeness(prd)
            return {
                "result": result,
                "metadata": {
                    "action": "validate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": "Unknown action: {}".format(action)},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error("Error in specification_prd_generation: {}".format(e))
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
