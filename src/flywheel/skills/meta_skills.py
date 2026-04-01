"""
Meta-Skills: Skill Drafting and Critiquing

This module provides meta-skills for creating and improving other skills:
- skill_drafting: Turn messy intent into structured skills
- skill_critiquing: Review and refine existing skills
"""

import os
import re
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime

SKILL_TEMPLATE = """---
Domain: {domain}
Version: 1.0.0
Complexity: {complexity}
Type: {skill_type}
Category: {category}
Estimated Execution Time: {execution_time}
name: {skill_name}
---

## Description

{description}

## Usage Examples

### Basic Usage

"{basic_usage}"

### Advanced Usage

"{advanced_usage}"

## Purpose

{purpose}

## Input Format

### {skill_name} Request

```yaml
{input_format}
```

## Output Format

### {skill_name} Response

```yaml
{output_format}
```

## Implementation Notes

{implementation_notes}

## When to Use

- {when_to_use_1}
- {when_to_use_2}

## When NOT to Use

- {when_not_to_use_1}
- {when_not_to_use_2}

## Capabilities

1. **{capability_1}**: {capability_1_desc}
2. **{capability_2}**: {capability_2_desc}
3. **{capability_3}**: {capability_3_desc}

## Constraints

- {constraint_1}
- {constraint_2}

## Examples

### Example 1: {example_1_title}

**Input**: {example_1_input}
**Output**: {example_1_output}

## Error Handling

- **{error_1}**: {error_1_handling}
- **{error_2}**: {error_2_handling}

## Configuration Options

- `{config_option_1}`: {config_option_1_desc}
- `{config_option_2}`: {config_option_2_desc}

## Performance Optimization

- {performance_note}

## Integration Examples

### Pipeline Integration

Run `{skill_name}` as part of your workflow.

## Best Practices

- {best_practice_1}
- {best_practice_2}

## Troubleshooting

- **Issue 1**: {troubleshoot_1}
- **Issue 2**: {troubleshoot_2}

## Monitoring and Metrics

- **{metric_1}**: {metric_1_desc}

## Dependencies

- **{dependency_1}**: {dependency_1_desc}

## Version History

- **1.0.0**: Initial generation via Skill Flywheel

## License

MIT License - Part of the Open AgentSkills Library.
"""

REQUIRED_SECTIONS = [
    "Domain",
    "Description",
    "Purpose",
    "Input Format",
    "Output Format",
    "Capabilities",
    "When to Use",
    "When NOT to Use",
    "Examples",
    "Error Handling",
]

VALID_DOMAINS = [
    "APPLICATION_SECURITY",
    "AI_AGENT_DEVELOPMENT",
    "ML_AI",
    "DATA_ENGINEERING",
    "CLOUD_ENGINEERING",
    "DEVOPS",
    "FRONTEND",
    "MOBILE_DEVELOPMENT",
    "WEB3",
    "GAME_DEV",
    "DATABASE_ENGINEERING",
    "SPECIFICATION_ENGINEERING",
    "ORCHESTRATION",
    "META_SKILL_DISCOVERY",
    "QUANTUM_COMPUTING",
]

VALID_COMPLEXITY = ["Basic", "Intermediate", "Advanced"]
VALID_TYPES = ["Process", "Tool", "Strategy", "Meta-Process", "Tutorial"]


def skill_drafting(
    intent: str,
    domain: str = "META_SKILL_DISCOVERY",
    complexity: str = "Intermediate",
    **kwargs,
) -> Dict[str, Any]:
    """
    Turn messy intent into structured skill definitions.

    Args:
        intent: Unstructured skill idea or description
        domain: Target domain for the skill
        complexity: Skill complexity level (Basic, Intermediate, Advanced)
        **kwargs: Additional parameters

    Returns:
        Dictionary with skill definition and template
    """
    try:
        intent_lower = intent.lower()

        skill_type = _determine_skill_type(intent_lower)
        category = _determine_category(intent_lower, domain)
        purpose = _extract_purpose(intent)
        description = purpose
        input_format = _generate_input_format(skill_type, intent)
        output_format = _generate_output_format(skill_type)
        execution_time = _estimate_execution_time(complexity)
        capabilities = _generate_capabilities(intent, skill_type)
        skill_name = _generate_skill_name(intent)

        skill_definition = {
            "skill_name": skill_name,
            "domain": domain,
            "complexity": complexity,
            "skill_type": skill_type,
            "category": category,
            "description": description,
            "purpose": purpose,
            "input_format": input_format,
            "output_format": output_format,
            "capabilities": capabilities,
            "execution_time": execution_time,
            "estimated_sections": REQUIRED_SECTIONS,
        }

        template = SKILL_TEMPLATE.format(
            domain=domain,
            complexity=complexity,
            skill_type=skill_type,
            category=category,
            execution_time=execution_time,
            skill_name=skill_name,
            description=description,
            basic_usage=f"Run {skill_name} on my data",
            advanced_usage=f"Run {skill_name} with custom parameters",
            purpose=purpose,
            input_format=input_format,
            output_format=output_format,
            implementation_notes="- Implementation should follow best practices",
            when_to_use_1=f"When you need to {intent_lower[:50]}",
            when_to_use_2="During automated workflows",
            when_not_to_use_1="When manual processing is required",
            when_not_to_use_2="When dealing with sensitive data",
            capability_1=capabilities[0]
            if len(capabilities) > 0
            else "Primary capability",
            capability_1_desc=capabilities[0]
            if len(capabilities) > 0
            else "Main functionality",
            capability_2=capabilities[1]
            if len(capabilities) > 1
            else "Secondary capability",
            capability_2_desc=capabilities[1]
            if len(capabilities) > 1
            else "Additional functionality",
            capability_3=capabilities[2]
            if len(capabilities) > 2
            else "Tertiary capability",
            capability_3_desc=capabilities[2]
            if len(capabilities) > 2
            else "Additional functionality",
            constraint_1="Follow input format specifications",
            constraint_2="Handle errors gracefully",
            example_1_title="Basic Usage",
            example_1_input=f'{{"action": "{skill_name}"}}',
            example_1_output='{"status": "success", "result": {}}',
            error_1="Invalid Input",
            error_1_handling="Return error message with details",
            error_2="Processing Error",
            error_2_handling="Log error and return error status",
            config_option_1="timeout",
            config_option_1_desc="Maximum execution time in seconds",
            config_option_2="verbose",
            config_option_2_desc="Enable verbose output",
            performance_note="Optimize for parallel processing when possible",
            best_practice_1="Validate input before processing",
            best_practice_2="Return structured results",
            troubleshoot_1="Empty results: Check input format",
            troubleshoot_2="Slow execution: Reduce complexity",
            metric_1="Success Rate",
            metric_1_desc="Percentage of successful executions",
            dependency_1="Python 3.10+",
            dependency_1_desc="Required Python runtime",
        )

        return {
            "status": "success",
            "skill_definition": skill_definition,
            "template": template,
            "skill_name": skill_name,
            "domain": domain,
            "complexity": complexity,
            "suggested_improvements": [
                "Add specific usage examples",
                "Define error handling for edge cases",
                "Add integration examples",
            ],
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to generate skill definition",
        }


def skill_critiquing(
    skill_path: str, focus_areas: List[str] | None = None, **kwargs
) -> Dict[str, Any]:
    """
    Review and refine existing skills.

    Args:
        skill_path: Path to skill file or skill name
        focus_areas: Specific areas to focus on during critique
        **kwargs: Additional parameters

    Returns:
        Dictionary with critique and recommendations
    """
    try:
        if os.path.isfile(skill_path) or skill_path.endswith(".md"):
            if os.path.exists(skill_path):
                with open(skill_path, encoding="utf-8") as f:
                    content = f.read()
            else:
                return {"status": "error", "error": f"File not found: {skill_path}"}
        else:
            skill_file = _find_skill_file(skill_path)
            if skill_file and os.path.exists(skill_file):
                with open(skill_file, encoding="utf-8") as f:
                    content = f.read()
            else:
                return {"status": "error", "error": f"Skill not found: {skill_path}"}

        critique = _perform_critique(content, focus_areas or [])

        return {
            "status": "success",
            "skill_name": skill_path,
            "critique": critique,
            "recommendations": critique.get("recommendations", []),
            "overall_score": critique.get("overall_score", 0),
            "missing_sections": critique.get("missing_sections", []),
            "strengths": critique.get("strengths", []),
            "improvements_needed": critique.get("improvements_needed", []),
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to perform skill critique",
        }


def _determine_skill_type(intent_lower: str) -> str:
    if any(word in intent_lower for word in ["create", "generate", "build", "make"]):
        return "Process"
    elif any(word in intent_lower for word in ["find", "search", "detect", "analyze"]):
        return "Tool"
    elif any(word in intent_lower for word in ["plan", "strategy", "optimize"]):
        return "Strategy"
    elif any(word in intent_lower for word in ["learn", "improve", "evolve"]):
        return "Meta-Process"
    else:
        return "Process"


def _determine_category(intent_lower: str, domain: str) -> str:
    if domain in ["ML_AI", "AI_AGENT_DEVELOPMENT"]:
        return "AI/ML Engineering"
    elif domain in ["APPLICATION_SECURITY", "SECURITY"]:
        return "Security"
    elif domain in ["DEVOPS", "CLOUD_ENGINEERING"]:
        return "DevOps"
    elif domain in ["FRONTEND", "MOBILE_DEVELOPMENT"]:
        return "Development"
    else:
        return "Engineering"


def _extract_purpose(intent: str) -> str:
    purpose = intent.strip()
    if not purpose.endswith("."):
        purpose += "."
    return purpose


def _generate_input_format(skill_type: str, intent: str) -> str:
    if skill_type == "Process":
        return """input_data:
  data: string        # Input data to process
  options:            # Optional parameters
    format: json"""
    elif skill_type == "Tool":
        return """query:
  term: string        # Search term
  filters:            # Optional filters
    domain: string"""
    else:
        return """request:
  action: string      # Action to perform
  parameters: object  # Action parameters"""


def _generate_output_format(skill_type: str) -> str:
    return """result:
  status: string      # success or error
  data: object        # Result data
  metadata: object   # Execution metadata"""


def _estimate_execution_time(complexity: str) -> str:
    mapping = {
        "Basic": "100ms - 1 second",
        "Intermediate": "1-5 seconds",
        "Advanced": "5 seconds - 1 minute",
    }
    return mapping.get(complexity, "1-5 seconds")


def _generate_capabilities(intent: str, skill_type: str) -> List[str]:
    return [
        "Process input data efficiently",
        "Handle errors gracefully",
        "Return structured results",
    ]


def _generate_skill_name(intent: str) -> str:
    name = intent.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    name = re.sub(r"-+", "-", name)
    if len(name) > 50:
        name = name[:50].rsplit("-", 1)[0]
    return name


def _find_skill_file(skill_name: str) -> str | None:
    base_dir = Path("domains")
    if not base_dir.exists():
        base_dir = Path(".")

    for md_file in base_dir.rglob("SKILL.md"):
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            if skill_name.lower() in content.lower():
                return str(md_file)
        except Exception:
            continue

    return None


def _perform_critique(content: str, focus_areas: List[str]) -> Dict[str, Any]:
    critique = {
        "overall_score": 0,
        "missing_sections": [],
        "strengths": [],
        "improvements_needed": [],
        "recommendations": [],
    }

    for section in REQUIRED_SECTIONS:
        if section.lower() in content.lower():
            critique["strengths"].append(f"Has {section} section")
        else:
            critique["missing_sections"].append(section)

    section_score = (len(critique["strengths"]) / len(REQUIRED_SECTIONS)) * 100

    if "example" in content.lower():
        critique["strengths"].append("Includes examples")
    else:
        critique["improvements_needed"].append("Add usage examples")

    if "error" in content.lower() or "handling" in content.lower():
        critique["strengths"].append("Has error handling")
    else:
        critique["improvements_needed"].append("Add error handling")

    if "constraint" in content.lower():
        critique["strengths"].append("Documents constraints")

    critique["overall_score"] = int(section_score)

    if critique["missing_sections"]:
        critique["recommendations"].append(
            f"Add missing sections: {', '.join(critique['missing_sections'][:3])}"
        )

    if critique["improvements_needed"]:
        critique["recommendations"].extend(critique["improvements_needed"])

    return critique


def validate_skill_definition(skill_definition: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a skill definition.

    Args:
        skill_definition: Dictionary containing skill definition

    Returns:
        Validation result
    """
    errors = []
    warnings = []

    required_fields = ["name", "domain", "purpose"]
    for field in required_fields:
        if field not in skill_definition:
            errors.append(f"Missing required field: {field}")

    if "domain" in skill_definition:
        if skill_definition["domain"] not in VALID_DOMAINS:
            warnings.append(
                f"Domain '{skill_definition['domain']}' not in standard domains"
            )

    if "complexity" in skill_definition:
        if skill_definition["complexity"] not in VALID_COMPLEXITY:
            errors.append(f"Invalid complexity: {skill_definition['complexity']}")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


async def invoke(payload: dict) -> dict:
    """Main entry point for MCP skill invocation"""
    action = payload.get("action", "draft")

    if action == "draft":
        intent = payload.get("intent", "")
        domain = payload.get("domain", "META_SKILL_DISCOVERY")
        complexity = payload.get("complexity", "Intermediate")
        result = skill_drafting(intent, domain, complexity)
    elif action == "critique":
        skill_path = payload.get("skill_path", "")
        focus_areas = payload.get("focus_areas", [])
        result = skill_critiquing(skill_path, focus_areas)
    elif action == "validate":
        skill_definition = payload.get("skill_definition", {})
        result = validate_skill_definition(skill_definition)
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return{
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
def register_skill():
    """Return skill metadata for MCP registration"""
    return {
        "name": "meta-skills",
        "description": "Meta-skills for creating and improving other skills",
        "version": "1.0.0",
        "domain": "META_SKILL_DISCOVERY",
    }
