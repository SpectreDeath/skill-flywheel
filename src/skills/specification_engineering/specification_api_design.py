import time
import logging
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


def analyze_api_requirements(requirements: List[str]) -> Dict[str, Any]:
    endpoints = []

    for req in requirements:
        endpoint = {
            "path": "/api/" + req.lower().replace(" ", "-"),
            "method": "GET",
            "description": req,
            "parameters": [],
            "responses": {"200": {"description": "Success"}},
        }

        if "create" in req.lower():
            endpoint["method"] = "POST"
        elif "update" in req.lower():
            endpoint["method"] = "PUT"
        elif "delete" in req.lower():
            endpoint["method"] = "DELETE"

        endpoints.append(endpoint)

    return {"endpoints": endpoints, "total_endpoints": len(endpoints)}


def generate_api_schema(resource: str) -> Dict[str, Any]:
    schema = {"resource": resource, "endpoints": []}

    base_path = "/{}".format(resource.lower())

    schema["endpoints"].append(
        {
            "path": base_path,
            "method": "GET",
            "description": "List all {}".format(resource),
            "parameters": [
                {"name": "page", "type": "integer", "in": "query", "required": False},
                {"name": "limit", "type": "integer", "in": "query", "required": False},
            ],
            "responses": {
                "200": {
                    "description": "Success",
                    "schema": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/{}".format(resource)},
                    },
                }
            },
        }
    )

    schema["endpoints"].append(
        {
            "path": base_path + "/{id}",
            "method": "GET",
            "description": "Get single {}".format(resource),
            "parameters": [
                {"name": "id", "type": "string", "in": "path", "required": True}
            ],
            "responses": {
                "200": {"description": "Success"},
                "404": {"description": "Not found"},
            },
        }
    )

    schema["endpoints"].append(
        {
            "path": base_path,
            "method": "POST",
            "description": "Create {}".format(resource),
            "parameters": [],
            "requestBody": {"$ref": "#/definitions/{}".format(resource)},
            "responses": {
                "201": {"description": "Created"},
                "400": {"description": "Bad request"},
            },
        }
    )

    return schema


def validate_api_design(api_schema: Dict[str, Any]) -> Dict[str, Any]:
    issues = []

    if not api_schema.get("resource"):
        issues.append({"type": "error", "message": "API resource name is required"})

    endpoints = api_schema.get("endpoints", [])
    if not endpoints:
        issues.append({"type": "error", "message": "At least one endpoint is required"})

    methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    for endpoint in endpoints:
        if endpoint.get("method") not in methods:
            issues.append(
                {
                    "type": "error",
                    "message": "Invalid HTTP method: {}".format(endpoint.get("method")),
                }
            )

        if not endpoint.get("path"):
            issues.append({"type": "error", "message": "Endpoint path is required"})

        if not endpoint.get("description"):
            issues.append(
                {"type": "warning", "message": "Endpoint description is recommended"}
            )

    return {
        "valid": len([i for i in issues if i["type"] == "error"]) == 0,
        "issues": issues,
        "score": 100 - len([i for i in issues if i["type"] == "error"]) * 20,
    }


def generate_api_documentation(api_schema: Dict[str, Any]) -> str:
    doc = []

    doc.append("# API Specification: {}".format(api_schema.get("resource", "API")))
    doc.append("")
    doc.append("## Endpoints")
    doc.append("")

    for endpoint in api_schema.get("endpoints", []):
        doc.append(
            "### {} {}".format(endpoint.get("method", "GET"), endpoint.get("path", "/"))
        )
        doc.append("")
        doc.append("_{}_".format(endpoint.get("description", "No description")))
        doc.append("")

        if endpoint.get("parameters"):
            doc.append("**Parameters:**")
            for param in endpoint["parameters"]:
                required = "required" if param.get("required") else "optional"
                doc.append(
                    "- `{}` ({}, {}): {}".format(
                        param.get("name"),
                        param.get("type", "string"),
                        required,
                        param.get("description", ""),
                    )
                )
            doc.append("")

        if endpoint.get("responses"):
            doc.append("**Responses:**")
            for code, resp in endpoint["responses"].items():
                doc.append(
                    "- `{}`: {}".format(code, resp.get("description", "No description"))
                )
            doc.append("")

    doc.append("_Generated on {} _".format(datetime.now().isoformat()))

    return "\n".join(doc)


def generate_openapi_spec(api_schema: Dict[str, Any]) -> Dict[str, Any]:
    openapi = {
        "openapi": "3.0.0",
        "info": {
            "title": api_schema.get("resource", "API"),
            "version": "1.0.0",
            "description": "Auto-generated API specification",
        },
        "servers": [
            {"url": "https://api.example.com", "description": "Production server"}
        ],
        "paths": {},
    }

    for endpoint in api_schema.get("endpoints", []):
        path = endpoint.get("path", "/")
        method = endpoint.get("method", "GET").lower()

        openapi["paths"][path] = {
            method: {
                "summary": endpoint.get("description", ""),
                "parameters": endpoint.get("parameters", []),
                "responses": endpoint.get("responses", {}),
            }
        }

    return openapi


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "design")

    try:
        if action == "design":
            resource = payload.get("resource", "resource")
            api_schema = generate_api_schema(resource)

            return {
                "result": api_schema,
                "metadata": {
                    "action": "design",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "analyze":
            requirements = payload.get("requirements", [])
            result = analyze_api_requirements(requirements)
            return {
                "result": result,
                "metadata": {
                    "action": "analyze",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "generate_schema":
            resource = payload.get("resource", "resource")
            result = generate_api_schema(resource)
            return {
                "result": result,
                "metadata": {
                    "action": "generate_schema",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "validate":
            api_schema = payload.get("api_schema", {})
            result = validate_api_design(api_schema)
            return {
                "result": result,
                "metadata": {
                    "action": "validate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "document":
            api_schema = payload.get("api_schema", {})
            doc = generate_api_documentation(api_schema)
            return {
                "result": {"documentation": doc},
                "metadata": {
                    "action": "document",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "generate_openapi":
            api_schema = payload.get("api_schema", {})
            openapi = generate_openapi_spec(api_schema)
            return {
                "result": openapi,
                "metadata": {
                    "action": "generate_openapi",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": "Unknown action: {}".format(action)},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error("Error in specification_api_design: {}".format(e))
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
