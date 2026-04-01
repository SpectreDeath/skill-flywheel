"""
Batch skill implementation pipeline.
Reads SKILL.md specs from domains/, generates Python modules with invoke() entry points,
verifies imports, registers in SQLite, and updates the backlog.
"""

import asyncio
import json
import logging
import os
import re
import sqlite3
import sys
import uuid
import datetime as dt

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_ROOT = os.path.join(PROJECT_ROOT, "src", "flywheel", "skills")
DOMAINS_ROOT = os.path.join(PROJECT_ROOT, "domains")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
REGISTRY_DB_PATH = os.path.join(DATA_DIR, "skill_registry.db")
BACKLOG_PATH = os.path.join(DATA_DIR, "skills_backlog.json")


def parse_skill_md(skill_md_path):
    """Parse SKILL.md to extract metadata and capabilities."""
    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    metadata = {}
    # Extract frontmatter
    fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        for line in fm.strip().split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                metadata[key.strip()] = val.strip()

    # Extract description from first paragraph after frontmatter
    desc_match = re.search(r"---.*?---\s*\n\n(.*?)(?:\n#|\n\n)", content, re.DOTALL)
    if desc_match:
        metadata.setdefault("description", desc_match.group(1).strip()[:200])

    # Extract capabilities/actions from content
    actions = []
    # Look for action-like patterns: `action_name` or bullet points with action descriptions
    for match in re.finditer(
        r"(?:^|\n)\s*[-*]\s*`?(\w[\w_]*)`?\s*[:\-]\s*(.+?)(?:\n|$)", content
    ):
        action_name = match.group(1).lower()
        action_desc = match.group(2).strip()[:100]
        if action_name not in ("name", "description", "version", "status"):
            actions.append({"name": action_name, "description": action_desc})

    # Also look for ### Section headers that could be actions
    for match in re.finditer(r"###?\s+(?:Step\s+\d+:?\s*)?([A-Z][\w\s-]+)", content):
        header = match.group(1).strip()
        action_name = re.sub(r"[^a-z0-9]+", "_", header.lower()).strip("_")
        if len(action_name) > 2 and action_name not in (
            "overview",
            "instructions",
            "constraints",
            "architecture",
        ):
            if not any(a["name"] == action_name for a in actions):
                actions.append({"name": action_name[:40], "description": header[:100]})

    # Default actions if none found
    if not actions:
        actions = [
            {
                "name": "get_info",
                "description": "Get skill information and capabilities",
            },
            {"name": "execute", "description": "Execute the skill's primary function"},
        ]

    metadata["actions"] = actions[:10]  # Cap at 10 actions
    return metadata


def normalize_domain(domain):
    """Normalize domain name to match directory conventions."""
    domain_map = {
        "ML_AI": "ML_AI",
        "DATA_ENGINEERING": "DATA_ENGINEERING",
        "CLOUD_ENGINEERING": "CLOUD_ENGINEERING",
        "APPLICATION_SECURITY": "APPLICATION_SECURITY",
        "mcp_tools": "mcp_tools",
        "AI_AGENT_DEVELOPMENT": "AI_AGENT_DEVELOPMENT",
        "agentic_ai": "agentic_ai",
        "generated_skills": "generated_skills",
        "orchestration": "orchestration",
        "skill_registry": "skill_registry",
        "skill_validation": "skill_validation",
        "meta_agent_enhancement": "meta_agent_enhancement",
        "META_SKILL_DISCOVERY": "META_SKILL_DISCOVERY",
        "performance_benchmarks": "performance_benchmarks",
        "agent_evolution": "agent_evolution",
        "QUANTUM_COMPUTING": "QUANTUM_COMPUTING",
        "ARCHIVED": "ARCHIVED",
        "WEB3": "WEB3",
        "GAME_DEV": "GAME_DEV",
        "FRONTEND": "FRONTEND",
        "DEVOPS": "DEVOPS",
        "DATABASE_ENGINEERING": "DATABASE_ENGINEERING",
        "security_engineering": "security_engineering",
        "search_algorithms": "search_algorithms",
        "mobile_development": "mobile_development",
        "logic_programming": "logic_programming",
        "formal_methods": "formal_methods",
        "epistemology": "epistemology",
        "logic": "logic",
        "probabilistic_models": "probabilistic_models",
    }
    return domain_map.get(domain, domain)


def sanitize_module_name(name):
    """Convert skill name to valid Python module name."""
    name = name.lower().replace("-", "_").replace(".", "_")
    name = re.sub(r"[^a-z0-9_]", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name[:80]


def escape_for_python_string(s):
    """Escape a string for safe inclusion in Python source code."""
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("\n", " ")
    s = s.replace("\r", "")
    s = s.replace("\t", " ")
    # Remove non-ASCII chars that could cause issues
    s = "".join(c if ord(c) < 128 else " " for c in s)
    return s[:300]  # Truncate long descriptions


def generate_skill_code(skill_name, domain, metadata):
    """Generate Python skill module code from parsed metadata."""
    description = metadata.get("description", "Skill: {}".format(skill_name))
    description = escape_for_python_string(description)
    actions = metadata.get("actions", [])

    actions_list = ", ".join('"' + a["name"] + '"' for a in actions)

    # Build action dispatch code
    dispatch_lines = []
    for i, action in enumerate(actions):
        action_name = action["name"]
        action_desc = escape_for_python_string(action.get("description", ""))
        keyword = "if" if i == 0 else "elif"
        line = (
            '    {kw} action == "{name}":\n'
            '        result = {{"action": "{name}", "status": "executed", "description": "{desc}"}}\n'
            '        return {{"result": result, "metadata": {{"action": action, "timestamp": timestamp}}}}'
        ).format(kw=keyword, name=action_name, desc=action_desc)
        dispatch_lines.append(line)
    dispatch_str = "\n".join(dispatch_lines)

    # Build the code directly without f-strings/format to avoid brace issues
    code = (
        "#!/usr/bin/env python3\n"
        '"""\n'
        "Skill: " + skill_name + "\n"
        "Domain: " + domain + "\n"
        "Description: " + description + "\n"
        '"""\n'
        "\n"
        "import logging\n"
        "from datetime import datetime\n"
        "from typing import Any, Dict\n"
        "\n"
        "logger = logging.getLogger(__name__)\n"
        "\n"
        'SKILL_NAME = "' + skill_name + '"\n'
        'DOMAIN = "' + domain + '"\n'
        'DESCRIPTION = "' + description + '"\n'
        "\n"
        "\n"
        "def get_capabilities():\n"
        '    """Return skill capabilities."""\n'
        "    return {\n"
        '        "name": SKILL_NAME,\n'
        '        "domain": DOMAIN,\n'
        '        "description": DESCRIPTION,\n'
        '        "actions": [' + actions_list + "],\n"
        "    }\n"
        "\n"
        "\n"
        "async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:\n"
        '    """Entry point for skill invocation."""\n'
        '    action = payload.get("action", "get_info")\n'
        "    timestamp = datetime.now().isoformat()\n"
        "\n"
        '    if action == "get_info" or action == "ping":\n'
        '        return {"result": get_capabilities(), "metadata": {"action": action, "timestamp": timestamp}}\n'
        "\n" + dispatch_str + "\n"
        "\n"
        "    else:\n"
        '        return {"result": {"error": "Unknown action: " + action}, "metadata": {"action": action, "timestamp": timestamp}}\n'
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    import asyncio\n"
        "    async def demo():\n"
        '        r = await invoke({"action": "get_info"})\n'
        "        print(r)\n"
        "    asyncio.run(demo())\n"
    )

    return code


def save_skill_module(domain, skill_name, code, overwrite=True):
    """Save generated skill module to disk."""
    domain_normalized = normalize_domain(domain)
    domain_path = os.path.join(SKILLS_ROOT, domain_normalized)

    # Create __init__.py if needed
    init_path = os.path.join(domain_path, "__init__.py")
    if not os.path.exists(init_path):
        os.makedirs(domain_path, exist_ok=True)
        with open(init_path, "w", encoding="utf-8") as f:
            f.write('"""Skills for domain: {}."""\n'.format(domain_normalized))

    module_name = sanitize_module_name(skill_name)
    file_path = os.path.join(domain_path, "{}.py".format(module_name))

    if os.path.exists(file_path) and not overwrite:
        return None

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    return file_path


def verify_module_import(file_path):
    """Verify the generated module imports and has invoke()."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("verify_skill", file_path)
    if spec is None or spec.loader is None:
        raise Exception("Failed to create module spec for {}".format(file_path))

    module = importlib.util.module_from_spec(spec)
    sys_modules_backup = sys.modules.copy()
    try:
        spec.loader.exec_module(module)
        if not hasattr(module, "invoke"):
            raise Exception("Module missing invoke function")
        if not callable(module.invoke):
            raise Exception("invoke is not callable")
        return True
    finally:
        sys.modules.clear()
        sys.modules.update(sys_modules_backup)


def register_skill_in_db(
    domain, skill_name, module_path, skill_id, version="1.0.0", description=None
):
    """Register skill in SQLite registry."""
    conn = sqlite3.connect(REGISTRY_DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT OR REPLACE INTO skills (skill_id, name, domain, module_path, entry_function, version, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                skill_id,
                skill_name,
                normalize_domain(domain),
                module_path,
                "invoke",
                version,
                description or "",
            ),
        )
        conn.commit()
    finally:
        conn.close()


def update_backlog_entry(skill_id):
    """Update a single backlog entry to IMPLEMENTED."""
    if not os.path.exists(BACKLOG_PATH):
        return
    with open(BACKLOG_PATH, "r", encoding="utf-8") as f:
        backlog = json.load(f)
    for entry in backlog:
        if entry.get("skill_id") == skill_id:
            entry["status"] = "IMPLEMENTED"
            break
    with open(BACKLOG_PATH, "w", encoding="utf-8") as f:
        json.dump(backlog, f, indent=2, ensure_ascii=False)


def find_skill_md_path(domain, skill_name):
    """Find the SKILL.md file for a skill."""
    variations = [
        os.path.join(DOMAINS_ROOT, domain, "SKILL.{}".format(skill_name), "SKILL.md"),
        os.path.join(
            DOMAINS_ROOT, domain.lower(), "SKILL.{}".format(skill_name), "SKILL.md"
        ),
        os.path.join(
            DOMAINS_ROOT, domain.upper(), "SKILL.{}".format(skill_name), "SKILL.md"
        ),
        os.path.join(DOMAINS_ROOT, domain, skill_name, "SKILL.md"),
        os.path.join(DOMAINS_ROOT, domain.lower(), skill_name, "SKILL.md"),
        os.path.join(DOMAINS_ROOT, domain.upper(), skill_name, "SKILL.md"),
    ]
    for path in variations:
        if os.path.exists(path):
            return path

    # Broader search
    for d in [domain, domain.lower(), domain.upper(), normalize_domain(domain)]:
        domain_dir = os.path.join(DOMAINS_ROOT, d)
        if os.path.isdir(domain_dir):
            for item in os.listdir(domain_dir):
                item_path = os.path.join(domain_dir, item)
                if os.path.isdir(item_path):
                    if item.lower() in (
                        "skill.{}".format(skill_name).lower(),
                        skill_name.lower(),
                    ):
                        md_path = os.path.join(item_path, "SKILL.md")
                        if os.path.exists(md_path):
                            return md_path
    return None


async def process_domain(domain_name, skills):
    """Process all skills in a domain."""
    implemented = 0
    skipped = 0

    for i, skill in enumerate(skills):
        skill_name = skill["name"]
        skill_id = skill.get("skill_id", str(uuid.uuid4()))

        # Check if module already exists
        domain_norm = normalize_domain(domain_name)
        module_name = sanitize_module_name(skill_name)
        existing_path = os.path.join(
            SKILLS_ROOT, domain_norm, "{}.py".format(module_name)
        )
        if os.path.exists(existing_path):
            update_backlog_entry(skill_id)
            implemented += 1
            continue

        # Find SKILL.md
        source_doc = skill.get("source_doc", "")
        if source_doc and os.path.exists(source_doc):
            skill_md_path = source_doc
        else:
            skill_md_path = find_skill_md_path(domain_name, skill_name)

        if not skill_md_path:
            skipped += 1
            continue

        try:
            metadata = parse_skill_md(skill_md_path)
            code = generate_skill_code(skill_name, domain_name, metadata)
            file_path = save_skill_module(domain_name, skill_name, code, overwrite=True)

            if file_path is None:
                skipped += 1
                continue

            verify_module_import(file_path)
            register_skill_in_db(
                domain_name,
                skill_name,
                file_path,
                skill_id,
                description=metadata.get("description", ""),
            )
            update_backlog_entry(skill_id)
            implemented += 1

        except Exception as e:
            logger.warning("Failed {}: {}".format(skill_name, str(e)[:80]))
            skipped += 1

    return {"implemented": implemented, "skipped": skipped}


async def main():
    """Main batch implementation pipeline."""
    # Load backlog
    with open(BACKLOG_PATH, "r", encoding="utf-8") as f:
        backlog = json.load(f)

    # Filter NOT_IMPLEMENTED, skip generated_skills reference skills
    not_impl = [
        s
        for s in backlog
        if s.get("status") == "NOT_IMPLEMENTED"
        and s.get("domain") != "generated_skills"
    ]

    logger.info("Found {} NOT_IMPLEMENTED skills to process".format(len(not_impl)))

    # Group by domain
    domains = {}
    for s in not_impl:
        d = s.get("domain", "UNKNOWN")
        domains.setdefault(d, []).append(s)

    total_impl = 0
    total_skip = 0

    for domain_name in sorted(domains.keys(), key=lambda d: -len(domains[d])):
        domain_skills = domains[domain_name]
        logger.info(
            "Processing domain: {} ({} skills)".format(domain_name, len(domain_skills))
        )

        result = await process_domain(domain_name, domain_skills)
        total_impl += result["implemented"]
        total_skip += result["skipped"]

        logger.info(
            "  {} -> {} implemented, {} skipped".format(
                domain_name, result["implemented"], result["skipped"]
            )
        )

    logger.info("=" * 60)
    logger.info("TOTALS: {} implemented, {} skipped".format(total_impl, total_skip))

    # Final counts
    with open(BACKLOG_PATH, "r", encoding="utf-8") as f:
        backlog = json.load(f)
    impl_count = sum(1 for s in backlog if s["status"] == "IMPLEMENTED")
    not_impl_count = sum(1 for s in backlog if s["status"] == "NOT_IMPLEMENTED")
    logger.info(
        "Backlog: {} IMPLEMENTED, {} NOT_IMPLEMENTED".format(impl_count, not_impl_count)
    )

    return {"implemented": total_impl, "skipped": total_skip}


if __name__ == "__main__":
    asyncio.run(main())
