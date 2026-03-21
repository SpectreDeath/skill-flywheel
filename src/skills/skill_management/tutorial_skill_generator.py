"""
Tutorial Skill Generator

Generates skill modules from SKILL.md files for tutorial-type skills.
These are skills derived from Jupyter Notebook tutorials.

This generator:
1. Reads SKILL.md to extract metadata (domain, workflow, constraints)
2. Generates a skill with workflow documentation
3. Creates placeholder implementations based on workflow steps
"""

import datetime as dt
import json
import logging
import os
import sqlite3
import uuid
from typing import Any, Dict, List

import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(CURRENT_DIR, "..", "..", ".."))
SKILLS_ROOT = os.path.join(PROJECT_ROOT, "src", "skills")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

REGISTRY_DB_PATH = os.path.join(DATA_DIR, "skill_registry.db")
BACKLOG_PATH = os.path.join(DATA_DIR, "skills_backlog.json")
DOMAINS_ROOT = os.path.join(PROJECT_ROOT, "domains")


def parse_skill_md(file_path: str) -> Dict[str, Any]:
    """
    Parse a SKILL.md file to extract metadata.

    Returns:
        dict with keys: name, domain, version, complexity, type, category,
                       description, workflow, examples, notes, constraints
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse YAML frontmatter
    metadata = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            metadata = yaml.safe_load(frontmatter) or {}
            content = parts[2].strip()

    # Extract markdown sections
    lines = content.split("\n")
    current_section = None
    section_content = []

    for line in lines:
        if line.startswith("## "):
            if current_section:
                metadata[current_section] = "\n".join(section_content).strip()
            current_section = line[3:].lower().replace(" ", "_")
            section_content = []
        elif current_section:
            section_content.append(line)

    if current_section:
        metadata[current_section] = "\n".join(section_content).strip()

    return metadata


def generate_tutorial_skill_code(
    skill_name: str,
    domain: str,
    metadata: Dict[str, Any],
    skill_id: str = None,
) -> str:
    """
    Generate skill module code from parsed SKILL.md metadata.
    Uses .format() as required.
    """
    skill_id = skill_id or str(uuid.uuid4())

    description = (
        (metadata.get("description") or "Tutorial skill")[:200]
        .replace('"', '\\"')
        .replace("'", "\\'")
    )
    version = metadata.get("version") or "1.0.0"
    complexity = metadata.get("Complexity", "Unknown")
    skill_type = metadata.get("Type", "Tutorial")
    category = (metadata.get("Category") or "").replace('"', '\\"').replace("'", "\\'")

    workflow_text = metadata.get("workflow", "No workflow defined")
    examples_text = metadata.get("examples", "No examples available")
    notes_text = (
        (metadata.get("Implementation Notes") or "No notes available")[:300]
        .replace('"', '\\"')
        .replace("'", "\\'")
    )
    constraints_text = (
        (metadata.get("Constraints") or "No constraints specified")[:300]
        .replace('"', '\\"')
        .replace("'", "\\'")
    )

    workflow_lines = [l.strip() for l in workflow_text.split("\n") if l.strip()]
    workflow_json = json.dumps(workflow_lines)

    code = '''"""
Tutorial Skill: {skill_name}

Domain: {domain}
Version: {version}
Complexity: {complexity}
Type: {skill_type}
Category: {category}

{description}

## Workflow
{workflow_text}

## Constraints
{constraints_text}

Generated: {timestamp}
"""
import logging
import time
import datetime
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SKILL_ID = "{skill_id}"
SKILL_NAME = "{skill_name}"
DOMAIN = "{domain}"
VERSION = "{version}"
COMPLEXITY = "{complexity}"

WORKFLOW_STEPS = {workflow_json}

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for skill invocation.
    
    Expected payload:
        - action: str (optional): The action to perform
                     - "describe": Describe this skill
                     - "workflow": Get workflow steps
                     - "validate": Validate constraints
                     - "execute": Execute the tutorial (placeholder)
        - data: dict (optional): Additional data for the action
    
    Returns:
        dict with 'result' and 'metadata' keys
    """
    start_time = time.time()
    timestamp = datetime.datetime.now().isoformat()
    
    action = payload.get("action", "describe")
    data = payload.get("data", {{}})
    
    if action == "describe":
        result = {{
            "skill_name": SKILL_NAME,
            "domain": DOMAIN,
            "version": VERSION,
            "complexity": COMPLEXITY,
            "description": "{description}",
            "category": "{category}",
            "workflow_steps": WORKFLOW_STEPS,
        }}
    elif action == "workflow":
        result = {{
            "steps": WORKFLOW_STEPS,
            "total_steps": len(WORKFLOW_STEPS),
        }}
    elif action == "validate":
        result = {{
            "valid": True,
            "constraints": "{constraints_text}",
            "notes": "{notes_text}",
        }}
    elif action == "execute":
        result = {{
            "status": "not_implemented",
            "message": "Tutorial execution not yet implemented",
            "note": "This is a placeholder skill generated from a tutorial specification. "
                    "Full implementation requires the source Jupyter Notebook.",
            "workflow": WORKFLOW_STEPS,
        }}
    else:
        result = {{
            "error": "Unknown action: " + action,
            "available_actions": ["describe", "workflow", "validate", "execute"],
        }}
    
    elapsed = time.time() - start_time
    
    return {{
        "result": result,
        "metadata": {{
            "timestamp": timestamp,
            "skill_id": SKILL_ID,
            "skill_name": SKILL_NAME,
            "domain": DOMAIN,
            "version": VERSION,
            "action": action,
            "elapsed_seconds": elapsed,
        }}
    }}


def register_skill():
    """Return skill metadata for registration"""
    return {{
        "name": SKILL_NAME,
        "description": "{description}",
        "domain": DOMAIN,
        "version": VERSION,
    }}
'''.format(
        skill_name=skill_name,
        skill_id=skill_id,
        domain=domain,
        version=version,
        complexity=complexity,
        skill_type=skill_type,
        category=category,
        description=description[:200],
        workflow_text=workflow_text[:500],
        workflow_json=workflow_json,
        constraints_text=constraints_text[:300],
        notes_text=notes_text[:300],
        timestamp=dt.datetime.now().isoformat(),
    )

    return code


def save_skill_module(
    domain: str, skill_name: str, code: str, overwrite: bool = False
) -> str:
    """Save the generated skill module to disk."""
    domain_path = os.path.join(SKILLS_ROOT, domain.lower())
    os.makedirs(domain_path, exist_ok=True)

    # Convert skill name to valid filename
    filename = skill_name.replace("-", "_").replace(" ", "_")[:50]
    file_path = os.path.join(domain_path, "{}.py".format(filename))

    if os.path.exists(file_path) and not overwrite:
        raise FileExistsError("Skill file already exists: {}".format(file_path))

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    logger.info("Saved skill module to: {}".format(file_path))
    return file_path


def verify_module_import(file_path: str) -> bool:
    """Verify that the generated module can be imported cleanly."""
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location("generated_skill", file_path)
    if spec is None or spec.loader is None:
        raise Exception("Failed to create module spec")

    module = importlib.util.module_from_spec(spec)

    sys_modules_backup = sys.modules.copy()
    try:
        spec.loader.exec_module(module)

        if not hasattr(module, "invoke"):
            raise Exception("Module missing invoke function")

        if not callable(module.invoke):
            raise Exception("invoke is not callable")

        logger.info("Module imported successfully from: {}".format(file_path))
        return True
    finally:
        sys.modules.clear()
        sys.modules.update(sys_modules_backup)


def register_skill_in_db(
    domain: str,
    skill_name: str,
    module_path: str,
    skill_id: str,
    version: str = "1.0.0",
    description: str = None,
) -> str:
    """Register the skill in the skill registry database."""
    if description is None:
        description = "Tutorial skill: {}".format(skill_name)

    conn = sqlite3.connect(REGISTRY_DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO skills (skill_id, name, domain, module_path, entry_function, version, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                skill_id,
                skill_name,
                domain,
                module_path,
                "invoke",
                version,
                description,
            ),
        )
        conn.commit()
        logger.info("Registered skill with ID: {}".format(skill_id))
    except sqlite3.IntegrityError:
        logger.warning("Skill already exists, updating...")
        cursor.execute(
            """
            UPDATE skills 
            SET name = ?, domain = ?, module_path = ?, entry_function = ?, version = ?, description = ?
            WHERE skill_id = ?
        """,
            (
                skill_name,
                domain,
                module_path,
                "invoke",
                version,
                description,
                skill_id,
            ),
        )
        conn.commit()
    finally:
        conn.close()

    return skill_id


def update_backlog_status(skill_id: str) -> bool:
    """Update a single backlog entry to IMPLEMENTED."""
    if not os.path.exists(BACKLOG_PATH):
        return False

    with open(BACKLOG_PATH, "r", encoding="utf-8") as f:
        backlog = json.load(f)

    today = dt.datetime.now().strftime("%Y-%m-%d")
    updated = False

    for entry in backlog:
        if entry.get("skill_id") == skill_id:
            entry["status"] = "IMPLEMENTED"
            entry["implemented_at"] = today
            updated = True
            break

    if updated:
        with open(BACKLOG_PATH, "w", encoding="utf-8") as f:
            json.dump(backlog, f, indent=2)
        logger.info("Updated backlog for skill: {}".format(skill_id))

    return updated


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a new tutorial skill module from SKILL.md.

    Expected payload keys:
        - skill_name: str - Name of the skill (must match backlog entry)
        - domain: str - Target skill domain
        - skill_id: str (optional) - Override generated skill_id
        - overwrite: bool (optional) - Whether to overwrite existing file

    Returns:
        dict with 'result' and 'metadata' keys
    """
    timestamp = dt.datetime.now().isoformat()

    skill_name = payload.get("skill_name")
    domain = payload.get("domain")
    skill_id_override = payload.get("skill_id")
    overwrite = payload.get("overwrite", False)

    if not skill_name:
        return {
            "result": {"error": "Missing required parameter: skill_name"},
            "metadata": {"timestamp": timestamp, "error": "skill_name is required"},
        }

    if not domain:
        return {
            "result": {"error": "Missing required parameter: domain"},
            "metadata": {"timestamp": timestamp, "error": "domain is required"},
        }

    logger.info("Generating tutorial skill: {}, domain: {}".format(skill_name, domain))

    # Find SKILL.md - try multiple path variations
    path_variations = [
        os.path.join(
            DOMAINS_ROOT, domain.upper(), "SKILL.{}".format(skill_name), "SKILL.md"
        ),
        os.path.join(
            DOMAINS_ROOT, domain.lower(), "SKILL.{}".format(skill_name), "SKILL.md"
        ),
        os.path.join(DOMAINS_ROOT, domain, "SKILL.{}".format(skill_name), "SKILL.md"),
        # Also try without SKILL. prefix (for legacy entries)
        os.path.join(DOMAINS_ROOT, domain.upper(), skill_name, "SKILL.md"),
        os.path.join(DOMAINS_ROOT, domain.lower(), skill_name, "SKILL.md"),
        os.path.join(DOMAINS_ROOT, domain, skill_name, "SKILL.md"),
    ]

    skill_md_path = None
    for path in path_variations:
        if os.path.exists(path):
            skill_md_path = path
            break

    # Also try case-insensitive search if not found
    if not skill_md_path:
        for d in [domain.upper(), domain.lower(), domain]:
            domain_path = os.path.join(DOMAINS_ROOT, d)
            if os.path.exists(domain_path):
                for item in os.listdir(domain_path):
                    if (
                        item.lower() == "SKILL.{}".format(skill_name).lower()
                        or item.lower() == skill_name.lower()
                    ):
                        skill_md_path = os.path.join(domain_path, item, "SKILL.md")
                        if os.path.exists(skill_md_path):
                            break
                if skill_md_path:
                    break

    if not skill_md_path or not os.path.exists(skill_md_path):
        return {
            "result": {
                "error": "SKILL.md not found for: {} in {}".format(skill_name, domain)
            },
            "metadata": {"timestamp": timestamp, "error": "SKILL.md file not found"},
        }

    # Parse metadata
    try:
        metadata = parse_skill_md(skill_md_path)
    except Exception as e:
        return {
            "result": {"error": "Failed to parse SKILL.md: {}".format(str(e))},
            "metadata": {"timestamp": timestamp, "error": str(e)},
        }

    skill_id = skill_id_override or str(uuid.uuid4())
    version = metadata.get("version", "1.0.0")

    # Generate code
    try:
        code = generate_tutorial_skill_code(skill_name, domain, metadata, skill_id)
        generated_path = save_skill_module(domain, skill_name, code, overwrite)
    except FileExistsError:
        return {
            "result": {
                "message": "Skill file already exists, skipping generation",
                "generated_path": os.path.join(
                    SKILLS_ROOT,
                    domain.lower(),
                    "{}.py".format(skill_name.replace("-", "_")[:50]),
                ),
            },
            "metadata": {"timestamp": timestamp, "skipped": True},
        }

    # Verify import
    try:
        verify_module_import(generated_path)
    except Exception as e:
        if os.path.exists(generated_path):
            os.remove(generated_path)
        return {
            "result": {"error": "Generated module failed to import: {}".format(str(e))},
            "metadata": {"timestamp": timestamp, "error": "Import verification failed"},
        }

    # Register
    try:
        register_skill_in_db(
            domain=domain,
            skill_name=skill_name,
            module_path=generated_path,
            skill_id=skill_id,
            version=version,
            description=metadata.get("description"),
        )
    except Exception as e:
        if os.path.exists(generated_path):
            os.remove(generated_path)
        return {
            "result": {"error": "Registration failed: {}".format(str(e))},
            "metadata": {"timestamp": timestamp, "error": "Registration failed"},
        }

    # Update backlog
    update_backlog_status(skill_id)

    return {
        "result": {
            "generated_path": generated_path,
            "registered_id": skill_id,
            "skill_name": skill_name,
        },
        "metadata": {
            "timestamp": timestamp,
            "version": version,
            "complexity": metadata.get("Complexity", "Unknown"),
        },
    }


def register_skill():
    """Return skill metadata for registration"""
    return {
        "name": "tutorial-skill-generator",
        "description": "Generate skill modules from SKILL.md tutorial files",
        "version": "1.0.0",
        "domain": "skill_management",
    }
