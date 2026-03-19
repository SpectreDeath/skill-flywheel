"""
Diagram Generator

Generates architecture diagrams from code using:
- Component detection (services, databases, APIs, queues)
- Relationship identification
- Mermaid and PlantUML output formats
- Styling with colors and labels
"""

import ast
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Component:
    name: str
    type: str
    description: Optional[str] = None
    protocols: List[str] = field(default_factory=list)
    styling: Dict[str, str] = field(default_factory=dict)


@dataclass
class Relationship:
    source: str
    target: str
    type: str
    label: Optional[str] = None
    protocol: Optional[str] = None


COMPONENT_PATTERNS = {
    "service": [
        r"class\s+(\w+Service)",
        r"@app\.(get|post|put|patch|delete)",
        r"@router\.(get|post|put|patch|delete)",
        r"def\s+(\w+_service|handle_\w+|process_\w+)",
        r"FastAPI\(\)",
        r"Flask\(\)",
        r"@app\.route",
    ],
    "database": [
        r"sqlite3\.connect",
        r"psycopg2\.connect",
        r"mysql\.connector",
        r"MongoClient",
        r"redis\.Redis",
        r"Redis\(",
        r"@table",
        r"class\s+\w+Model",
        r"SQLAlchemy",
        r"create_engine",
    ],
    "api": [
        r"requests\.(get|post|put|patch|delete)",
        r"httpx\.(get|post|put|patch|delete)",
        r"axios\.",
        r"fetch\(",
        r"@api_view",
        r"APIView",
        r"rest_framework",
    ],
    "queue": [
        r"pika\.Connection",
        r"kombu\.Queue",
        r"celery",
        r"RabbitMQ",
        r"KafkaProducer",
        r"KafkaConsumer",
        r"asyncio\.Queue",
    ],
    "cache": [
        r"redis\.Redis",
        r"Redis\(",
        r"@cache",
        r"memcached",
        r"cachetools",
    ],
    "storage": [
        r"boto3\.s3",
        r"S3Client",
        r"google\.cloud\.storage",
        r"azure\.storage",
    ],
    "auth": [
        r"OAuth",
        r"JWT",
        r"Auth0",
        r"@login_required",
        r"@authenticated",
    ],
    "gateway": [
        r"APIGateway",
        r"API Gateway",
        r"nginx",
        r"gateway",
    ],
}

COMPONENT_STYLES = {
    "service": {"fill": "e1f5fe", "stroke": "0277bd", "color": "01579b"},
    "database": {"fill": "fce4ec", "stroke": "c2185b", "color": "880e4f"},
    "api": {"fill": "e8f5e9", "stroke": "2e7d32", "color": "1b5e20"},
    "queue": {"fill": "fff3e0", "stroke": "ef6c00", "color": "e65100"},
    "cache": {"fill": "f3e5f5", "stroke": "7b1fa2", "color": "4a148c"},
    "storage": {"fill": "e0f7fa", "stroke": "00838f", "color": "006064"},
    "auth": {"fill": "ffebee", "stroke": "c62828", "color": "b71c1c"},
    "gateway": {"fill": "eceff1", "stroke": "546e7a", "color": "37474f"},
}

RELATIONSHIP_PATTERNS = {
    "calls": [
        r"(\w+)\.(\w+)\(",
        r"await\s+(\w+)\.(\w+)",
    ],
    "connects": [
        r"connect\(['\"](\w+)['\"]\)",
        r"ConnectionPool\(['\"](\w+)['\"]",
    ],
    "sends": [
        r"\.send\(",
        r"\.publish\(",
        r"\.put\(",
    ],
    "receives": [
        r"\.receive\(",
        r"\.consume\(",
        r"\.get\(",
    ],
    "authenticates": [
        r"\.authenticate\(",
        r"JWT\.",
        r"OAuth\.",
    ],
}


def parse_code_structure(code: str) -> List[str]:
    """Extract code structure using AST"""
    try:
        tree = ast.parse(code)
        classes = []
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)

        return classes + functions
    except:
        return []


def detect_components(code: str) -> List[Component]:
    """Detect architectural components from code"""
    components = []
    detected = set()

    for comp_type, patterns in COMPONENT_PATTERNS.items():
        for pattern in patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if comp_type == "service":
                    name = match.group(1) if match.groups() else "Service"
                elif comp_type in [
                    "database",
                    "api",
                    "queue",
                    "cache",
                    "storage",
                    "auth",
                    "gateway",
                ]:
                    name = match.group(1) if match.groups() else comp_type.title()
                else:
                    name = (
                        match.group(1)
                        if match.groups()
                        else f"{comp_type.title()}_Component"
                    )

                if name and name not in detected:
                    detected.add(name)
                    components.append(
                        Component(
                            name=name,
                            type=comp_type,
                            styling=COMPONENT_STYLES.get(comp_type, {}),
                        )
                    )

    code_structure = parse_code_structure(code)
    for item in code_structure:
        if item not in detected and any(
            kw in item.lower()
            for kw in ["service", "handler", "controller", "provider"]
        ):
            detected.add(item)
            components.append(
                Component(
                    name=item,
                    type="service",
                    styling=COMPONENT_STYLES.get("service", {}),
                )
            )

    return components


def detect_relationships(code: str, components: List[Component]) -> List[Relationship]:
    """Detect relationships between components"""
    relationships = []
    component_names = {c.name for c in components}

    for rel_type, patterns in RELATIONSHIP_PATTERNS.items():
        for pattern in patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                if match.groups():
                    source = match.group(1) if len(match.groups()) >= 1 else None
                    target = match.group(2) if len(match.groups()) >= 2 else None

                    if source and (target or rel_type in ["sends", "receives"]):
                        if source in component_names:
                            relationships.append(
                                Relationship(
                                    source=source,
                                    target=target or f"{rel_type}_target",
                                    type=rel_type,
                                    protocol="http"
                                    if rel_type in ["calls", "api"]
                                    else None,
                                )
                            )

    if "requests" in code or "httpx" in code:
        for comp in components:
            if comp.type == "service":
                relationships.append(
                    Relationship(
                        source=comp.name,
                        target="External API",
                        type="calls",
                        protocol="HTTP",
                    )
                )

    return relationships[:20]


def generate_mermaid_diagram(
    components: List[Component], relationships: List[Relationship]
) -> str:
    """Generate Mermaid diagram code"""
    lines = ["graph TD"]

    for comp in components:
        style = comp.styling
        if style:
            lines.append(f'    {comp.name}["{comp.name}"]')
            lines.append(
                f'    style {comp.name} fill:#{style.get("fill", "eee")},stroke:#{style.get("stroke", "333")},color:#{style.get("color", "000")}'
            )

    for rel in relationships:
        arrow = "-->" if rel.type in ["calls", "sends"] else "---"
        label = f"|{rel.label}|" if rel.label else ""
        lines.append(f"    {rel.source} {arrow} {label} {rel.target}")

    return "\n".join(lines)


def generate_plantuml_diagram(
    components: List[Component], relationships: List[Relationship]
) -> str:
    """Generate PlantUML diagram code"""
    lines = ["@startuml"]
    lines.append("")

    for comp in components:
        comp_type = comp.type.lower()
        if comp_type == "database":
            lines.append(f'entity "{comp.name}" as {comp.name.replace(" ", "_")} {{')
            lines.append("    ...")
            lines.append("}}")
        elif comp_type in ["service", "api"]:
            lines.append(f'package "{comp.name}" {{')
            lines.append(f"    class {comp.name} {{")
            lines.append("        +execute()")
            lines.append("    }")
            lines.append("}")
        else:
            lines.append(f'component "{comp.name}" as {comp.name.replace(" ", "_")}')

    lines.append("")

    for rel in relationships:
        source = rel.source.replace(" ", "_")
        target = rel.target.replace(" ", "_")
        arrow = "-->" if rel.type in ["calls", "sends"] else "--"
        if rel.label:
            lines.append(f"{source} {arrow} {target} : {rel.label}")
        else:
            lines.append(f"{source} {arrow} {target}")

    lines.append("")
    lines.append("@enduml")

    return "\n".join(lines)


def diagram_generator(code: str, options: dict = None) -> dict:
    """
    Generate architecture diagram from code.

    Args:
        code: Architecture code to analyze
        options: Output options (format: mermaid or plantuml)

    Returns:
        dict with status, components, relationships, and diagram
    """
    if options is None:
        options = {}

    if not code or not code.strip():
        return {
            "status": "error",
            "error": "No code provided",
            "components": [],
            "relationships": [],
            "diagram": "",
        }

    output_format = options.get("format", "mermaid").lower()
    include_styling = options.get("styling", True)

    components = detect_components(code)
    relationships = detect_relationships(code, components)

    if output_format == "plantuml":
        diagram = generate_plantuml_diagram(components, relationships)
    else:
        diagram = generate_mermaid_diagram(components, relationships)

    if not include_styling:
        for comp in components:
            comp.styling = {}

    components_data = [
        {
            "name": c.name,
            "type": c.type,
            "description": c.description,
            "protocols": c.protocols,
            "styling": c.styling if include_styling else {},
        }
        for c in components
    ]

    relationships_data = [
        {
            "source": r.source,
            "target": r.target,
            "type": r.type,
            "label": r.label,
            "protocol": r.protocol,
        }
        for r in relationships
    ]

    return {
        "status": "success",
        "components": components_data,
        "relationships": relationships_data,
        "diagram": diagram,
        "format": output_format,
        "component_count": len(components),
        "relationship_count": len(relationships),
    }


def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "generate")
    code = payload.get("code", "")
    options = payload.get("options", {})

    if action == "generate":
        result = diagram_generator(code, options)
    elif action == "detect_components":
        components = detect_components(code)
        result = {
            "status": "success",
            "components": [{"name": c.name, "type": c.type} for c in components],
        }
    elif action == "detect_relationships":
        components = detect_components(code)
        relationships = detect_relationships(code, components)
        result = {
            "status": "success",
            "relationships": [
                {"source": r.source, "target": r.target, "type": r.type}
                for r in relationships
            ],
        }
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return {"result": result}


def register_skill():
    """Return skill metadata"""
    return {
        "name": "diagram-generator",
        "description": "Generate architecture diagrams from code - detects components, relationships and outputs Mermaid/PlantUML",
        "version": "1.0.0",
        "domain": "DOCUMENTATION",
        "capabilities": [
            "detect_services",
            "detect_databases",
            "detect_apis",
            "detect_queues",
            "detect_caches",
            "detect_storage",
            "detect_auth",
            "detect_gateways",
            "identify_relationships",
            "generate_mermaid",
            "generate_plantuml",
            "apply_styling",
        ],
    }
