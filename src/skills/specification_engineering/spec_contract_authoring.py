import time
import logging
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


def extract_contracts_from_spec(spec_text: str) -> List[Dict[str, Any]]:
    contracts = []

    sections = re.split(r"\n##\s+", spec_text)

    for i, section in enumerate(sections):
        if (
            "contract" in section.lower()
            or "api" in section.lower()
            or "interface" in section.lower()
        ):
            contract_id = "contract-{:03d}".format(i)
            contracts.append(
                {
                    "contract_id": contract_id,
                    "name": "Contract {}".format(i),
                    "description": section[:200],
                    "type": "api",
                    "version": "1.0.0",
                }
            )

    if not contracts:
        contracts.append(
            {
                "contract_id": "contract-default",
                "name": "Default Contract",
                "description": "Main specification contract",
                "type": "general",
                "version": "1.0.0",
            }
        )

    return contracts


def validate_contract_syntax(contract: Dict[str, Any]) -> Dict[str, Any]:
    errors = []
    warnings = []

    if not contract.get("name"):
        errors.append("Contract name is required")

    if not contract.get("contract_id"):
        errors.append("Contract ID is required")

    fields = contract.get("fields", [])
    if not fields:
        warnings.append("No fields defined in contract")

    required_types = ["string", "number", "boolean", "object", "array"]
    for field in fields:
        if field.get("type") not in required_types:
            warnings.append(
                "Field '{}' has non-standard type".format(field.get("name", "unknown"))
            )

    valid = len(errors) == 0

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "validation_score": 100 - len(errors) * 20 - len(warnings) * 5,
    }


def generate_contract_template(contract_type: str) -> Dict[str, Any]:
    templates = {
        "api": {
            "name": "API Contract",
            "fields": [
                {"name": "endpoint", "type": "string", "required": True},
                {
                    "name": "method",
                    "type": "string",
                    "required": True,
                    "enum": ["GET", "POST", "PUT", "DELETE"],
                },
                {"name": "parameters", "type": "object", "required": False},
                {"name": "response", "type": "object", "required": True},
                {"name": "status_codes", "type": "array", "required": False},
            ],
            "version": "1.0.0",
        },
        "data": {
            "name": "Data Contract",
            "fields": [
                {"name": "id", "type": "string", "required": True},
                {"name": "type", "type": "string", "required": True},
                {"name": "attributes", "type": "object", "required": True},
                {"name": "metadata", "type": "object", "required": False},
            ],
            "version": "1.0.0",
        },
        "event": {
            "name": "Event Contract",
            "fields": [
                {"name": "event_id", "type": "string", "required": True},
                {"name": "event_type", "type": "string", "required": True},
                {"name": "timestamp", "type": "string", "required": True},
                {"name": "payload", "type": "object", "required": True},
            ],
            "version": "1.0.0",
        },
    }

    template = templates.get(contract_type, templates["api"])
    template["contract_id"] = "contract-{}".format(
        hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    )

    return template


def check_contract_compatibility(
    contract_a: Dict[str, Any], contract_b: Dict[str, Any]
) -> Dict[str, Any]:
    fields_a = {f["name"]: f for f in contract_a.get("fields", [])}
    fields_b = {f["name"]: f for f in contract_b.get("fields", [])}

    common_fields = set(fields_a.keys()) & set(fields_b.keys())

    breaking_changes = []
    compatible_changes = []

    for field in common_fields:
        type_a = fields_a[field].get("type")
        type_b = fields_b[field].get("type")

        if type_a != type_b:
            breaking_changes.append(
                {
                    "field": field,
                    "old_type": type_a,
                    "new_type": type_b,
                    "severity": "breaking",
                }
            )

        required_a = fields_a[field].get("required", False)
        required_b = fields_b[field].get("required", False)

        if not required_a and required_b:
            breaking_changes.append(
                {"field": field, "change": "made_required", "severity": "breaking"}
            )

    new_required = set(fields_b.keys()) - set(fields_a.keys())
    for field in new_required:
        if fields_b[field].get("required", False):
            breaking_changes.append(
                {"field": field, "change": "new_required_field", "severity": "breaking"}
            )
        else:
            compatible_changes.append({"field": field, "change": "new_optional_field"})

    deprecated_fields = set(fields_a.keys()) - set(fields_b.keys())
    for field in deprecated_fields:
        compatible_changes.append(
            {"field": field, "change": "removed_field", "severity": "warning"}
        )

    backward_compatible = len(breaking_changes) == 0

    return {
        "backward_compatible": backward_compatible,
        "breaking_changes": breaking_changes,
        "compatible_changes": compatible_changes,
        "compatibility_score": 100 - len(breaking_changes) * 25,
    }


def generate_contract_documentation(contract: Dict[str, Any]) -> str:
    doc = []

    doc.append("# {}".format(contract.get("name", "Contract")))
    doc.append("")
    doc.append("**Contract ID**: {}".format(contract.get("contract_id", "N/A")))
    doc.append("**Version**: {}".format(contract.get("version", "1.0.0")))
    doc.append("**Type**: {}".format(contract.get("type", "general")))
    doc.append("")

    if contract.get("description"):
        doc.append("## Description")
        doc.append(contract["description"])
        doc.append("")

    doc.append("## Fields")
    doc.append("")

    for field in contract.get("fields", []):
        required_marker = " (required)" if field.get("required") else " (optional)"
        doc.append(
            "- **{}**{}: {}".format(
                field.get("name", "unknown"), required_marker, field.get("type", "any")
            )
        )

        if field.get("description"):
            doc.append("  - {}".format(field["description"]))

        if field.get("enum"):
            doc.append("  - Allowed values: {}".format(", ".join(field["enum"])))

    doc.append("")
    doc.append("*Generated on {}*".format(datetime.now().isoformat()))

    return "\n".join(doc)


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "author")

    try:
        if action == "author":
            spec_text = payload.get("spec_text", "")
            contracts = extract_contracts_from_spec(spec_text)

            return {
                "result": {"contracts": contracts},
                "metadata": {
                    "action": "author",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "validate":
            contract = payload.get("contract", {})
            result = validate_contract_syntax(contract)
            return {
                "result": result,
                "metadata": {
                    "action": "validate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "generate_template":
            contract_type = payload.get("contract_type", "api")
            result = generate_contract_template(contract_type)
            return {
                "result": result,
                "metadata": {
                    "action": "generate_template",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "check_compatibility":
            contract_a = payload.get("contract_a", {})
            contract_b = payload.get("contract_b", {})
            result = check_contract_compatibility(contract_a, contract_b)
            return {
                "result": result,
                "metadata": {
                    "action": "check_compatibility",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "document":
            contract = payload.get("contract", {})
            doc = generate_contract_documentation(contract)
            return {
                "result": {"documentation": doc},
                "metadata": {
                    "action": "document",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "extract":
            spec_text = payload.get("spec_text", "")
            result = extract_contracts_from_spec(spec_text)
            return {
                "result": {"contracts": result},
                "metadata": {
                    "action": "extract",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": "Unknown action: {}".format(action)},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error("Error in spec_contract_authoring: {}".format(e))
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
