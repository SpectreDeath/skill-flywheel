import json
import os
import re
from pathlib import Path

import yaml

WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent
SKILLS_DIR = WORKSPACE_ROOT / "domains"
REGISTRY_FILE = WORKSPACE_ROOT / "skill_registry.json"


def extract_fenced_block(content, lang):
    """Extract first fenced code block of a given language tag."""
    pattern = rf"```{lang}\s*\n(.*?)```"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else None


def extract_prolog_tags(prolog_source):
    """Extract predicate names from Prolog clause heads as logic_tags."""
    if not prolog_source:
        return []
    # Match predicate heads: name( or name :- 
    heads = re.findall(r"^([a-z][a-zA-Z0-9_]*)\s*[:(]", prolog_source, re.MULTILINE)
    # Deduplicate, exclude Prolog builtins
    builtins = {"not", "is", "true", "fail", "assert", "retract"}
    return list(dict.fromkeys(h for h in heads if h not in builtins))


def extract_hy_tags(hy_source):
    """Extract function names from Hy defn forms as heuristic_tags."""
    if not hy_source:
        return []
    fns = re.findall(r"\(defn\s+([a-zA-Z][a-zA-Z0-9_\-?!]*)", hy_source)
    return list(dict.fromkeys(fns))


def get_skill_metadata(file_path):
    """Extract metadata from a SKILL.md file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("---"):
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            return None

        fm = yaml.safe_load(parts[1]) or {}
        body = parts[2]

        # Extract purpose
        purpose = ""
        purpose_match = re.search(r"## Purpose\s*\n\s*(.+)", body)
        if purpose_match:
            purpose = purpose_match.group(1).strip()

        # Extract description
        description = ""
        desc_match = re.search(r"## Description\s*\n\s*(.+)", body)
        if desc_match:
            description = desc_match.group(1).strip()

        # Extract fenced code blocks for surface detection
        prolog_source = extract_fenced_block(body, "prolog")
        hy_source = extract_fenced_block(body, "hy")
        python_source = extract_fenced_block(body, "python")

        # Build surfaces list from detected blocks
        surfaces = []
        if python_source:
            surfaces.append("python")
        if prolog_source:
            surfaces.append("prolog")
        if hy_source:
            surfaces.append("hy")
        # Fall back to frontmatter if no blocks found
        if not surfaces:
            surfaces = fm.get("surfaces", ["python"])

        # Extract tags
        logic_tags = extract_prolog_tags(prolog_source)
        heuristic_tags = extract_hy_tags(hy_source)

        return {
            "name": fm.get("name", file_path.parent.name),
            "domain": fm.get("Domain", "General"),
            "version": fm.get("Version", "0.1.0"),
            "purpose": purpose,
            "description": description,
            "path": str(file_path.relative_to(SKILLS_DIR.parent)),
            "last_modified": os.path.getmtime(file_path),
            # New fields
            "surfaces": surfaces,
            "logic_tags": logic_tags,
            "heuristic_tags": heuristic_tags,
        }
    except Exception as e:
        print(f"Error indexing {file_path}: {e}")
        return None


def reindex():
    print(f"Re-indexing skills in {SKILLS_DIR}...")
    registry = []

    # Look for both SKILL.md and SKILL_*.md files
    for skill_file in SKILLS_DIR.glob("**/SKILL.md"):
        metadata = get_skill_metadata(skill_file)
        if metadata:
            registry.append(metadata)

    for skill_file in SKILLS_DIR.glob("**/SKILL_*.md"):
        metadata = get_skill_metadata(skill_file)
        if metadata:
            registry.append(metadata)

    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    print(f"Successfully indexed {len(registry)} skills to {REGISTRY_FILE}")
    # Summary breakdown
    multi = [s for s in registry if len(s.get("surfaces", [])) > 1]
    print(f"  Multi-surface skills: {len(multi)}")
    print(f"  Single-surface skills: {len(registry) - len(multi)}")


if __name__ == "__main__":
    reindex()
