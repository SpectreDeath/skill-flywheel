import json
import sys
from pathlib import Path

# Paths relative to script location in src/core
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
REGISTRY_FILE = WORKSPACE_ROOT / "skill_registry.json"
DISCOVERY_FILE = WORKSPACE_ROOT / "src" / "discovery" / "discovery_service.py"


def get_registry_domains():
    if not REGISTRY_FILE.exists():
        print(f"Error: Registry file not found at {REGISTRY_FILE}")
        return set()
    with open(REGISTRY_FILE, encoding="utf-8") as f:
        registry = json.load(f)
    return {skill.get("domain") for skill in registry if skill.get("domain")}


def get_discovery_domains():
    if not DISCOVERY_FILE.exists():
        print(f"Error: Discovery service file not found at {DISCOVERY_FILE}")
        return set()

    with open(DISCOVERY_FILE, encoding="utf-8") as f:
        content = f.read()

    # More robust extraction of SERVICE_GROUPS content
    import re

    # Find the SERVICE_GROUPS dictionary block
    bg_match = re.search(r"SERVICE_GROUPS = \{(.*?)\}", content, re.DOTALL)
    if not bg_match:
        return set()

    # Find all strings within brackets in that block
    list_content = bg_match.group(1)
    domains = set(re.findall(r'"([^"]+)"', list_content))
    return domains


def verify():
    reg_domains = get_registry_domains()
    disc_domains = get_discovery_domains()

    missing = reg_domains - disc_domains

    if not missing:
        print("✅ SUCCESS: All registry domains are covered in Discovery Service.")
        return True
    else:
        print(
            """❌ FAILURE: The following domains are in the registry but MISSING from Discovery Service:"""
        )
        for d in sorted(missing):
            print(f"  - {d}")
        return False


if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)
