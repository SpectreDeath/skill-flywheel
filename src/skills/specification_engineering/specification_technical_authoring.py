import time
import logging
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


def generate_technical_document(spec: Dict[str, Any]) -> Dict[str, Any]:
    doc = {
        "title": spec.get("title", "Technical Specification"),
        "version": spec.get("version", "1.0.0"),
        "created_at": datetime.now().isoformat(),
    }

    doc["overview"] = spec.get("description", "Technical specification document.")

    doc["architecture"] = {
        "components": [],
        "data_flow": "One-way flow from client to server",
        "dependencies": [],
    }

    components = spec.get("components", ["Core System"])
    for comp in components:
        doc["architecture"]["components"].append(
            {
                "name": comp.get("name", "Component"),
                "description": comp.get("description", ""),
                "responsibilities": comp.get("responsibilities", ["Processing"]),
            }
        )

    doc["api_specification"] = {
        "endpoints": [],
        "authentication": "Bearer token",
        "rate_limiting": "100 requests per minute",
    }

    doc["data_model"] = {"entities": [], "relationships": []}

    entities = spec.get("entities", [])
    for entity in entities:
        doc["data_model"]["entities"].append(
            {
                "name": entity.get("name", "Entity"),
                "fields": entity.get("fields", [{"name": "id", "type": "string"}]),
            }
        )

    doc["security"] = {
        "authentication": "JWT-based",
        "authorization": "Role-based access control",
        "encryption": "TLS 1.3 for transit, AES-256 for at rest",
    }

    doc["deployment"] = {
        "environment": "Cloud-based",
        "infrastructure": "Containerized with Kubernetes",
        "monitoring": "Prometheus and Grafana",
    }

    return doc


def format_technical_document(
    doc: Dict[str, Any], format_type: str = "markdown"
) -> str:
    if format_type == "markdown":
        output = []

        output.append("# {}".format(doc.get("title", "Technical Specification")))
        output.append("")
        output.append("**Version:** {}".format(doc.get("version", "1.0.0")))
        output.append("**Created:** {}".format(doc.get("created_at", "")))
        output.append("")

        output.append("## Overview")
        output.append("")
        output.append(doc.get("overview", ""))
        output.append("")

        output.append("## Architecture")
        output.append("")
        output.append("### Components")
        for comp in doc.get("architecture", {}).get("components", []):
            output.append("#### {}".format(comp.get("name", "")))
            output.append(comp.get("description", ""))
            output.append("")

        output.append("## API Specification")
        output.append("")
        api_spec = doc.get("api_specification", {})
        output.append("- Authentication: {}".format(api_spec.get("authentication", "")))
        output.append("- Rate Limiting: {}".format(api_spec.get("rate_limiting", "")))
        output.append("")

        output.append("## Data Model")
        output.append("")
        for entity in doc.get("data_model", {}).get("entities", []):
            output.append("### {}".format(entity.get("name", "")))
            for field in entity.get("fields", []):
                output.append(
                    "- {} ({})".format(
                        field.get("name", ""), field.get("type", "string")
                    )
                )
            output.append("")

        output.append("## Security")
        output.append("")
        security = doc.get("security", {})
        for key, value in security.items():
            output.append("- **{}**: {}".format(key, value))
        output.append("")

        output.append("## Deployment")
        output.append("")
        deployment = doc.get("deployment", {})
        for key, value in deployment.items():
            output.append("- **{}**: {}".format(key, value))
        output.append("")

        return "\n".join(output)

    return json.dumps(doc, indent=2)


def validate_technical_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    issues = []

    required = ["title", "overview", "architecture", "api_specification", "data_model"]
    for field in required:
        if field not in doc:
            issues.append(
                {"type": "warning", "message": "Missing section: {}".format(field)}
            )

    arch = doc.get("architecture", {})
    if "components" in arch and not arch["components"]:
        issues.append(
            {
                "type": "error",
                "message": "Architecture must have at least one component",
            }
        )

    data_model = doc.get("data_model", {})
    if "entities" in data_model and not data_model["entities"]:
        issues.append(
            {"type": "warning", "message": "No entities defined in data model"}
        )

    return {
        "valid": len([i for i in issues if i["type"] == "error"]) == 0,
        "issues": issues,
        "score": 100 - len([i for i in issues if i["type"] == "error"]) * 20,
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "author")

    try:
        if action == "author":
            spec = payload.get("spec", {})
            doc = generate_technical_document(spec)

            return {
                "result": doc,
                "metadata": {
                    "action": "author",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "format":
            doc = payload.get("document", {})
            format_type = payload.get("format_type", "markdown")
            result = format_technical_document(doc, format_type)
            return {
                "result": {"formatted": result},
                "metadata": {
                    "action": "format",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "validate":
            doc = payload.get("document", {})
            result = validate_technical_document(doc)
            return {
                "result": result,
                "metadata": {
                    "action": "validate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "generate":
            spec = payload.get("spec", {})
            doc = generate_technical_document(spec)
            return {
                "result": doc,
                "metadata": {
                    "action": "generate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": "Unknown action: {}".format(action)},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error("Error in specification_technical_authoring: {}".format(e))
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
