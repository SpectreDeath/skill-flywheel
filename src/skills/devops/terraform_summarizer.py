"""
Terraform Plan Summarizer

Parses and summarizes Terraform plans to identify changes, risks,
and provide human-readable explanations of infrastructure modifications.

Supports: JSON and text format Terraform plans
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


DESTRUCTIVE_RESOURCE_TYPES = {
    "aws_instance": "EC2 instance deletion",
    "aws_ebs_volume": "EBS volume deletion",
    "aws_s3_bucket": "S3 bucket deletion (with data loss)",
    "aws_db_instance": "Database instance deletion",
    "aws_rds_cluster": "RDS cluster deletion",
    "aws_lambda_function": "Lambda function deletion",
    "aws_vpc": "VPC deletion (cascading effects)",
    "aws_subnet": "Subnet deletion",
    "aws_security_group": "Security group deletion",
    "aws_route_table": "Route table deletion",
    "aws_iam_role": "IAM role deletion",
    "aws_iam_user": "IAM user deletion",
    "aws_iam_policy": "IAM policy deletion",
    "aws_load_balancer": "Load balancer deletion",
    "azurerm_virtual_machine": "Azure VM deletion",
    "azurerm_storage_account": "Azure storage account deletion",
    "azurerm_sql_database": "Azure SQL database deletion",
    "google_compute_instance": "GCP compute instance deletion",
    "google_storage_bucket": "GCP storage bucket deletion",
    "google_sql_database": "GCP Cloud SQL deletion",
}

COST_IMPACT_PATTERNS = {
    "aws_instance": {
        "t3.micro": 0.01,
        "t3.small": 0.02,
        "t3.medium": 0.04,
        "t3.large": 0.08,
        "t3.xlarge": 0.16,
    },
    "aws_db_instance": {
        "db.t3.micro": 0.017,
        "db.t3.small": 0.034,
        "db.t3.medium": 0.068,
        "db.t3.large": 0.136,
    },
    "aws_elb": {"application": 0.0225, "network": 0.0225},
    "google_compute_instance": {
        "n1-standard-1": 0.0475,
        "n1-standard-2": 0.095,
        "n1-standard-4": 0.19,
    },
}


@dataclass
class ResourceChange:
    address: str
    action: str
    resource_type: str
    name: str
    provider: str
    before: Optional[Dict] = None
    after: Optional[Dict] = None
    requires_new: bool = False


def detect_plan_format(plan: str) -> str:
    """Detect whether the plan is in JSON or text format."""
    plan = plan.strip()
    if plan.startswith("{") or plan.startswith("["):
        try:
            json.loads(plan)
            return "json"
        except json.JSONDecodeError:
            pass
    return "text"


def parse_json_plan(plan: str) -> Dict[str, Any]:
    """Parse Terraform plan in JSON format."""
    try:
        plan_data = json.loads(plan)
        return plan_data
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {str(e)}"}


def parse_text_plan(plan: str) -> List[ResourceChange]:
    """Parse Terraform plan in text format."""
    changes = []
    current_action = None
    current_resource = None

    lines = plan.split("\n")
    for line in lines:
        line = line.rstrip()

        if line.startswith("Terraform:"):
            continue

        if line.startswith("Plan:"):
            continue

        action_match = re.match(r"^([+\-~])", line)
        if action_match:
            current_action = {"+": "add", "-": "destroy", "~": "change"}.get(
                action_match.group(1)
            )
            continue

        resource_match = re.match(r"^  # ([\w._\-]+)\.(.+)$", line)
        if resource_match and current_action:
            resource_type = resource_match.group(1)
            name = resource_match.group(2)
            provider = (
                resource_type.split("_")[0] if "_" in resource_type else "unknown"
            )

            changes.append(
                ResourceChange(
                    address=f"{resource_type}.{name}",
                    action=current_action,
                    resource_type=resource_type,
                    name=name,
                    provider=provider,
                )
            )

            if "must be replaced" in line:
                changes[-1].requires_new = True

    return changes


def extract_resource_changes(plan_data: Dict[str, Any]) -> List[ResourceChange]:
    """Extract resource changes from JSON plan."""
    changes = []

    if "resource_changes" not in plan_data:
        return changes

    for rc in plan_data.get("resource_changes", []):
        address = rc.get("address", "")
        action = rc.get("action", "no-op")

        if action == "no-op":
            continue

        resource_type = rc.get("type", "")
        if "." in address:
            resource_type = address.split(".")[0]

        name = rc.get("name", address.split(".")[-1] if "." in address else address)

        provider = rc.get("provider_name", "")
        if "." in resource_type:
            provider = resource_type.split(".")[0]
        elif "_" in resource_type:
            provider = resource_type.split("_")[0]

        before = rc.get("change", {}).get("before", None)
        after = rc.get("change", {}).get("after", None)

        requires_new = False
        if "change" in rc and "actions" in rc["change"]:
            requires_new = (
                "create" in rc["change"]["actions"]
                and "delete" in rc["change"]["actions"]
            )

        changes.append(
            ResourceChange(
                address=address,
                action=action,
                resource_type=resource_type,
                name=name,
                provider=provider,
                before=before,
                after=after,
                requires_new=requires_new,
            )
        )

    return changes


def categorize_changes(changes: List[ResourceChange]) -> Dict[str, List[Dict]]:
    """Categorize changes into add, change, and destroy."""
    categorized = {"add": [], "change": [], "destroy": [], "replace": []}

    for change in changes:
        change_dict = {
            "address": change.address,
            "type": change.resource_type,
            "name": change.name,
            "provider": change.provider,
        }

        if change.action == "create":
            categorized["add"].append(change_dict)
        elif change.action == "delete":
            categorized["destroy"].append(change_dict)
        elif change.action == "update":
            categorized["change"].append(change_dict)
        elif change.requires_new:
            categorized["replace"].append(change_dict)
        else:
            categorized["change"].append(change_dict)

    return categorized


def identify_risks(changes: List[ResourceChange]) -> List[Dict[str, Any]]:
    """Identify potential risks in the changes."""
    risks = []

    for change in changes:
        risk_level = "low"
        risk_type = None
        description = None

        if change.action == "delete":
            if change.resource_type in DESTRUCTIVE_RESOURCE_TYPES:
                risk_level = "high"
                risk_type = "destructive"
                description = DESTRUCTIVE_RESOURCE_TYPES.get(
                    change.resource_type, f"{change.resource_type} will be deleted"
                )
            else:
                risk_level = "medium"
                risk_type = "deletion"
                description = f"Resource {change.name} will be deleted"

        elif change.requires_new:
            risk_level = "high"
            risk_type = "replacement"
            description = f"Resource {change.name} will be replaced (old resource destroyed, new created)"

        if change.resource_type in COST_IMPACT_PATTERNS:
            if risk_level == "low":
                risk_level = "medium"
            if not risk_type:
                risk_type = "cost"
            description = (
                description or f"{change.resource_type} changes may impact costs"
            )

        if risk_type:
            risks.append(
                {
                    "level": risk_level,
                    "type": risk_type,
                    "resource": change.address,
                    "description": description,
                    "action": change.action,
                }
            )

    return sorted(
        risks, key=lambda r: {"high": 0, "medium": 1, "low": 2}.get(r["level"], 3)
    )


def estimate_cost_impact(
    changes: List[ResourceChange], include_cost: bool = False
) -> Dict[str, Any]:
    """Estimate cost impact of changes."""
    if not include_cost:
        return {"estimated": False, "message": "Cost estimation disabled"}

    monthly_cost_change = 0.0
    affected_resources = []

    for change in changes:
        if change.action in ("delete", "destroy"):
            continue

        if change.after and isinstance(change.after, dict):
            resource_type = change.resource_type
            costs = COST_IMPACT_PATTERNS.get(resource_type, {})

            if not costs:
                continue

            if resource_type == "aws_instance":
                instance_type = change.after.get("instance_type", "t3.micro")
                cost = costs.get(instance_type, 0.01)
                monthly_cost_change += cost * 730
                affected_resources.append(
                    {
                        "resource": change.name,
                        "type": resource_type,
                        "monthly_cost": cost * 730,
                    }
                )

            elif resource_type == "aws_db_instance":
                instance_class = change.after.get("instance_class", "db.t3.micro")
                cost = costs.get(instance_class, 0.017)
                monthly_cost_change += cost * 730
                affected_resources.append(
                    {
                        "resource": change.name,
                        "type": resource_type,
                        "monthly_cost": cost * 730,
                    }
                )

            elif resource_type == "aws_elb":
                lb_type = change.after.get("type", "application")
                cost = costs.get(lb_type, 0.0225)
                monthly_cost_change += cost * 730
                affected_resources.append(
                    {
                        "resource": change.name,
                        "type": resource_type,
                        "monthly_cost": cost * 730,
                    }
                )

            elif resource_type == "google_compute_instance":
                machine_type = change.after.get("machine_type", "n1-standard-1")
                cost = costs.get(machine_type, 0.0475)
                monthly_cost_change += cost * 730
                affected_resources.append(
                    {
                        "resource": change.name,
                        "type": resource_type,
                        "monthly_cost": cost * 730,
                    }
                )

    return {
        "estimated": True,
        "monthly_change": round(monthly_cost_change, 2),
        "yearly_change": round(monthly_cost_change * 12, 2),
        "affected_resources": affected_resources,
        "currency": "USD",
    }


def generate_summary(
    categorized: Dict[str, List[Dict]], risks: List[Dict], cost_impact: Dict
) -> str:
    """Generate human-readable summary of the plan."""
    total_changes = (
        len(categorized["add"])
        + len(categorized["change"])
        + len(categorized["destroy"])
        + len(categorized["replace"])
    )

    if total_changes == 0:
        return "No changes detected in this plan. The infrastructure will remain unchanged."

    summary_parts = []

    summary_parts.append(f"Total changes: {total_changes}")

    if categorized["add"]:
        summary_parts.append(f"  + {len(categorized['add'])} to add")
    if categorized["change"]:
        summary_parts.append(f"  ~ {len(categorized['change'])} to change")
    if categorized["destroy"]:
        summary_parts.append(f"  - {len(categorized['destroy'])} to destroy")
    if categorized["replace"]:
        summary_parts.append(f"  ~ {len(categorized['replace'])} to replace")

    high_risks = [r for r in risks if r["level"] == "high"]
    if high_risks:
        summary_parts.append(f"\nHigh-risk changes: {len(high_risks)}")
        for risk in high_risks[:3]:
            summary_parts.append(f"  - {risk['description']} ({risk['resource']})")

    if cost_impact.get("estimated") and cost_impact.get("monthly_change", 0) != 0:
        cost_change = cost_impact["monthly_change"]
        direction = "increase" if cost_change > 0 else "decrease"
        summary_parts.append(
            f"\nEstimated cost impact: ${abs(cost_change):.2f}/month ({direction})"
        )

    return "\n".join(summary_parts)


def explain_change(change: ResourceChange) -> str:
    """Explain what a specific change means."""
    explanations = []

    if change.action == "create" or change.action == "add":
        explanations.append(
            f"Creating new {change.resource_type} resource named '{change.name}'"
        )

        if change.after:
            if "instance_type" in change.after:
                explanations.append(
                    f"  - Instance type: {change.after['instance_type']}"
                )
            if "size" in change.after:
                explanations.append(f"  - Size: {change.after['size']}")
            if "instance_class" in change.after:
                explanations.append(
                    f"  - Instance class: {change.after['instance_class']}"
                )

    elif change.action == "delete" or change.action == "destroy":
        explanations.append(
            f"Deleting {change.resource_type} resource named '{change.name}'"
        )

        if change.resource_type in DESTRUCTIVE_RESOURCE_TYPES:
            explanations.append(
                f"  ⚠️  {DESTRUCTIVE_RESOURCE_TYPES[change.resource_type]}"
            )

    elif change.action == "update" or change.action == "change":
        explanations.append(
            f"Updating {change.resource_type} resource named '{change.name}'"
        )

        if change.before and change.after:
            changed_attrs = []
            for key in change.after:
                if key in change.before:
                    if change.before[key] != change.after[key]:
                        changed_attrs.append(key)
                else:
                    changed_attrs.append(key)

            if changed_attrs:
                explanations.append(
                    f"  - Changed attributes: {', '.join(changed_attrs)}"
                )

    if change.requires_new:
        explanations.append(
            "  ⚠️  This change requires resource replacement (cannot be updated in place)"
        )

    return "\n".join(explanations)


def get_resources_affected(changes: List[ResourceChange]) -> Dict[str, List[str]]:
    """Get list of affected resources grouped by provider."""
    resources = {}

    for change in changes:
        provider = change.provider
        if provider not in resources:
            resources[provider] = []
        resources[provider].append(
            {
                "address": change.address,
                "type": change.resource_type,
                "action": change.action,
            }
        )

    return resources


def terraform_summarizer(plan: str, options: dict = None) -> dict:
    """
    Summarize a Terraform plan.

    Args:
        plan: Terraform plan output (JSON or text format)
        options: Optional configuration:
            - format: "json" or "text" (auto-detected if not specified)
            - include_cost: Boolean to include cost estimation

    Returns:
        Dictionary containing:
            - status: "success" or "error"
            - changes: Categorized changes (add, change, destroy, replace)
            - resources: Resources affected grouped by provider
            - risks: Identified risks
            - summary: Human-readable summary
            - cost_impact: Estimated cost change
    """
    if options is None:
        options = {}

    if not plan or not plan.strip():
        return {"status": "error", "error": "No Terraform plan provided"}

    format_type = options.get("format", detect_plan_format(plan))
    include_cost = options.get("include_cost", False)

    if format_type == "json":
        plan_data = parse_json_plan(plan)
        if "error" in plan_data:
            return {"status": "error", "error": plan_data["error"]}
        changes = extract_resource_changes(plan_data)
    else:
        changes = parse_text_plan(plan)

    categorized = categorize_changes(changes)
    risks = identify_risks(changes)
    resources = get_resources_affected(changes)
    cost_impact = estimate_cost_impact(changes, include_cost)
    summary = generate_summary(categorized, risks, cost_impact)

    explanations = {}
    for change in changes:
        explanations[change.address] = explain_change(change)

    return {
        "status": "success",
        "changes": categorized,
        "resources": resources,
        "risks": risks,
        "summary": summary,
        "cost_impact": cost_impact,
        "explanations": explanations,
        "format_detected": format_type,
        "total_changes": sum(len(v) for v in categorized.values()),
    }


def invoke(payload: dict) -> dict:
    """MCP skill invocation."""
    plan = payload.get("plan", "")
    options = payload.get("options", {})

    result = terraform_summarizer(plan, options)

    return {"result": result}


def register_skill():
    """Return skill metadata."""
    return {
        "name": "terraform-summarizer",
        "description": "Summarize Terraform plans to identify changes, risks, and provide human-readable explanations of infrastructure modifications",
        "version": "1.0.0",
        "domain": "DEVOPS",
    }
