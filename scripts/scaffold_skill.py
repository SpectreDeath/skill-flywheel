#!/usr/bin/env python3
"""
Skill Scaffold Generator

Generates properly structured Python skill modules from:
1. Command line args: `python scaffold_skill.py <skill_name> <domain>`
2. SKILL.md spec: `python scaffold_skill.py --from-spec <path/to/SKILL.md>`
3. Batch from domains/: `python scaffold_skill.py --batch <domain>`

Generated skills include:
- async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]
- from datetime import datetime
- Proper metadata in return format
- Error handling with try/except
- register_skill() metadata function
"""

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

SKILLS_DIR = Path("src/flywheel/skills")
DOMAINS_DIR = Path("domains")


def safe_name(name: str) -> str:
    """Convert skill name to valid Python identifier."""
    return name.lower().replace("-", "_").replace(" ", "_")


def generate_skill_code(
    skill_name: str,
    domain: str,
    description: str = "",
    actions: Optional[Dict[str, str]] = None,
) -> str:
    """Generate complete skill module code with proper structure."""
    safe = safe_name(skill_name)
    display_name = skill_name.lower()

    if actions is None:
        actions = {"process": "Process the payload"}

    action_names = ", ".join(f'"{a}"' for a in actions.keys())
    default_action = next(iter(actions.keys()))

    # Build action if/elif blocks with proper indentation (inside try)
    lines = []
    lines.append('#!/usr/bin/env python3')
    lines.append('"""')
    lines.append(f'{skill_name}')
    lines.append('')
    lines.append(f'{description or "Skill for " + domain + " domain."}')
    lines.append('"""')
    lines.append('')
    lines.append('import logging')
    lines.append('from datetime import datetime')
    lines.append('from typing import Any, Dict')
    lines.append('')
    lines.append('logger = logging.getLogger(__name__)')
    lines.append('')
    lines.append('')
    lines.append(f'def {safe}(payload: Dict[str, Any]) -> Dict[str, Any]:')
    lines.append(f'    """')
    lines.append(f'    Core implementation for {display_name}.')
    lines.append(f'')
    lines.append(f'    Args:')
    lines.append(f'        payload: Input parameters for the skill')
    lines.append(f'')
    lines.append(f'    Returns:')
    lines.append(f'        Result dictionary with status and data')
    lines.append(f'    """')
    lines.append(f'    # TODO: Implement core logic')
    lines.append(f'    return {{')
    lines.append(f'        "action": "{display_name}",')
    lines.append(f'        "status": "success",')
    lines.append(f'        "message": "{display_name} executed",')
    lines.append(f'    }}')
    lines.append('')
    lines.append('')
    lines.append('async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:')
    lines.append('    """MCP skill invocation."""')
    lines.append(f'    action = payload.get("action", "{default_action}")')
    lines.append('    try:')
    lines.append('        if False:')
    lines.append('            pass  # Placeholder')

    # Build if/elif blocks inside try
    for i, (action, desc) in enumerate(actions.items()):
        if i == 0:
            lines.append(f'        elif action == "{action}":')
        else:
            lines.append(f'        elif action == "{action}":')
        lines.append(f'            # TODO: {desc}')
        lines.append('            result = {')
        lines.append(f'                "action": "{action}",')
        lines.append('                "status": "success",')
        lines.append(f'                "message": "{action} completed",')
        lines.append('            }')

    lines.append('        else:')
    lines.append('            result = {')
    lines.append('                "error": f"Unknown action: {action}",')
    lines.append('            }')
    lines.append('')
    lines.append('        return {')
    lines.append('            "result": result,')
    lines.append('            "metadata": {')
    lines.append('                "action": action,')
    lines.append('                "timestamp": datetime.now().isoformat(),')
    lines.append('            },')
    lines.append('        }')
    lines.append('    except Exception as e:')
    lines.append(f'        logger.error(f"Error in {display_name}: {{e}}")')
    lines.append('        return {')
    lines.append('            "result": {"error": str(e)},')
    lines.append('            "metadata": {')
    lines.append('                "action": action,')
    lines.append('                "timestamp": datetime.now().isoformat(),')
    lines.append('            },')
    lines.append('        }')
    lines.append('')
    lines.append('')
    lines.append('def register_skill() -> Dict[str, str]:')
    lines.append('    """Return skill metadata."""')
    lines.append('    return {')
    lines.append(f'        "name": "{display_name}",')
    lines.append(f'        "description": "{description or skill_name}",')
    lines.append(f'        "version": "1.0.0",')
    lines.append(f'        "domain": "{domain.upper()}",')
    lines.append('    }')
    lines.append('')
    lines.append('')
    lines.append('def register_skill() -> Dict[str, str]:')
    lines.append('    """Return skill metadata."""')
    lines.append('    return {')
    lines.append(f'        "name": "{display_name}",')
    lines.append(f'        "description": "{description or skill_name}",')
    lines.append(f'        "version": "1.0.0",')
    lines.append(f'        "domain": "{domain.upper()}",')
    lines.append('    }')
    lines.append('')

    return '\n'.join(lines)


def parse_skill_md(spec_path: Path) -> Dict[str, Any]:
    """Parse a SKILL.md file to extract spec information."""
    content = spec_path.read_text(encoding="utf-8")

    # Extract name from frontmatter
    name_match = re.search(r"name:\s*(.+)", content)
    desc_match = re.search(r"description:\s*(.+)", content)
    domain_match = re.search(r"[Dd]omain:\s*(.+)", content)

    skill_name = name_match.group(1).strip() if name_match else spec_path.parent.name
    description = desc_match.group(1).strip() if desc_match else ""
    domain = domain_match.group(1).strip() if domain_match else "General"

    return {
        "name": skill_name,
        "domain": domain,
        "description": description,
    }


def scaffold_skill(
    skill_name: str,
    domain: str = "General",
    description: str = "",
    actions: Optional[Dict[str, str]] = None,
    spec_path: Optional[Path] = None,
) -> Path:
    """Generate a skill module."""
    domain_upper = domain.upper()
    skill_dir = SKILLS_DIR / domain_upper
    skill_dir.mkdir(exist_ok=True, parents=True)

    # Ensure __init__.py exists
    init_file = skill_dir / "__init__.py"
    if not init_file.exists():
        init_file.touch()

    safe = safe_name(skill_name)
    output_path = skill_dir / f"{safe}.py"

    if output_path.exists():
        logger.info(f"Skill '{safe}' already exists at {output_path}")
        return output_path

    code = generate_skill_code(skill_name, domain, description, actions)
    output_path.write_text(code, encoding="utf-8")

    if spec_path:
        logger.info(f"Generated skill '{skill_name}' from spec {spec_path}")
    else:
        logger.info(f"Generated skill '{skill_name}' in domain '{domain}'")

    return output_path


def scaffold_from_spec(spec_path: Path) -> Path:
    """Generate skill from SKILL.md spec."""
    spec = parse_skill_md(spec_path)
    return scaffold_skill(
        skill_name=spec["name"],
        domain=spec["domain"],
        description=spec["description"],
        spec_path=spec_path,
    )


def main():
    parser = argparse.ArgumentParser(description="Scaffold MCP skills")
    parser.add_argument("skill_name", nargs="?", help="Skill name")
    parser.add_argument("domain", nargs="?", default="General", help="Domain")
    parser.add_argument("--from-spec", type=Path, help="Generate from SKILL.md spec")
    parser.add_argument("--description", default="", help="Skill description")
    parser.add_argument("--actions", type=str, nargs="*", help="Actions: name:description")

    args = parser.parse_args()

    if args.from_spec:
        path = scaffold_from_spec(args.from_spec)
        print(f"Generated: {path}")
        return

    if not args.skill_name:
        parser.print_help()
        sys.exit(1)

    actions = None
    if args.actions:
        actions = {}
        for act in args.actions:
            if ":" in act:
                name, desc = act.split(":", 1)
                actions[name] = desc
            else:
                actions[act] = f"Execute {act}"

    path = scaffold_skill(
        skill_name=args.skill_name,
        domain=args.domain,
        description=args.description,
        actions=actions,
    )
    print(f"Generated: {path}")


if __name__ == "__main__":
    main()