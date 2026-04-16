#!/usr/bin/env python3
"""
Find orphaned SKILL.md files - specs without implementation.

Checks if each SKILL.md has a corresponding .py file in src/flywheel/skills/
"""

import sys
from pathlib import Path
from collections import defaultdict

SKILLS_DIR = Path("src/flywheel/skills")
DOMAINS_DIR = Path("domains")


def find_all_py_files() -> dict:
    """Find ALL .py files across ALL domains, indexed by normalized name."""
    all_files = {}

    for domain_dir in SKILLS_DIR.iterdir():
        if not domain_dir.is_dir():
            continue
        domain = domain_dir.name.lower()

        # Handle direct .py files in domain dir
        for f in domain_dir.glob("*.py"):
            if f.name != "__init__.py":
                normalized = f.stem.lower().replace("-", "_")
                all_files[normalized] = domain
                all_files[f.stem.lower()] = domain
                # Also add with underscore variant
                if "_" in f.stem:
                    all_files[f.stem.replace("_", "")] = domain

        # Handle .py files in subdirectories
        for subdir in domain_dir.iterdir():
            if subdir.is_dir():
                for f in subdir.glob("*.py"):
                    if f.name != "__init__.py":
                        normalized = f.stem.lower().replace("-", "_")
                        all_files[normalized] = domain
                        all_files[f.stem.lower()] = domain
                        # Extract skill name from file (e.g., skillsmp_master -> master)
                        if "_" in f.stem:
                            parts = f.stem.split("_", 1)
                            if len(parts) > 1:
                                all_files[parts[1].lower()] = domain
                        # Add variant without prefix
                        all_files[f.stem.split("_")[-1].lower()] = domain

    return all_files


def get_domain_from_path(skill_path: Path) -> str:
    """Extract domain from SKILL.md path."""
    parts = skill_path.parts
    for i, part in enumerate(parts):
        if part == "domains":
            try:
                return parts[i + 1]
            except IndexError:
                return "unknown"
    return "unknown"


def is_valid_skill_spec(skill_md_path: Path) -> bool:
    """Check if SKILL.md is actually a skill spec, not a domain README."""
    parent_name = skill_md_path.parent.name

    # Skip domain-level SKILL.md files (these are domain overviews, not skills)
    # A valid skill has SKILL. or SKILL_ prefix in directory name
    if parent_name.startswith("SKILL"):
        return True

    # Also check if it's in a domain root (not in a skill subdirectory)
    # If parent is the domain itself (like SKILLSMP_ECOSYSTEM), it's likely an overview
    try:
        content = skill_md_path.read_text(encoding="utf-8")
        # Domain overview files have multiple domain references
        lines = content.split("\n")
        domain_lines = [l for l in lines if "Domain:" in l or "domain:" in l]
        if domain_lines:
            return False  # It's a domain-level file, not a skill spec
        return "name:" in content
    except Exception:
        return False


def normalize_skill_name(dir_name: str) -> str:
    """Normalize skill directory name to match .py file."""
    name = dir_name.replace("SKILL.", "").replace("SKILL_", "")
    name = name.lower().replace("-", "_")
    return name


def get_variants(name: str) -> list[str]:
    """Generate all possible name variants for matching."""
    variants = [name]

    # Handle underscore/dash variations
    variants.append(name.replace("_", ""))
    variants.append(name.replace("-", ""))

    # Handle prefix patterns (e.g., skillsmp_skill_learner -> skill_learner, learner)
    if "_" in name:
        parts = name.split("_")
        # Remove common prefixes
        common_prefixes = ["skill", "skillsmp", "prolog", "logic", "strategic", "game"]
        for i in range(len(parts)):
            if parts[i] not in common_prefixes:
                variants.append("_".join(parts[i:]))
                variants.append(parts[i])

    return variants


def main():
    orphaned = defaultdict(list)
    mapped = []

    all_py = find_all_py_files()

    for skill_md in DOMAINS_DIR.glob("**/SKILL.md"):
        if not is_valid_skill_spec(skill_md):
            continue

        domain = get_domain_from_path(skill_md)
        skill_dir_name = skill_md.parent.name
        skill_name = normalize_skill_name(skill_dir_name)

        # Check exact match
        found = skill_name in all_py
        if found:
            mapped.append((domain, skill_md.name))
            continue

        # Check prefix match
        for py_file in all_py.keys():
            if py_file.startswith(skill_name) or skill_name.startswith(py_file):
                mapped.append((domain, skill_md.name))
                found = True
                break

        # Check variant matching (handles skillsmp_skill_learner vs skillsmp-skill-learner)
        if not found:
            variants = get_variants(skill_name)
            for variant in variants:
                if variant in all_py or any(
                    v in all_py
                    for v in [variant.replace("_", ""), variant.replace("-", "")]
                ):
                    mapped.append((domain, skill_md.name))
                    found = True
                    break

        if not found:
            orphaned[domain].append(skill_md.name)

    print("=== ORPHANED SKILL.md FILES (No Implementation) ===\n")

    total_orphan = 0
    for domain in sorted(orphaned.keys()):
        skills = orphaned[domain]
        total_orphan += len(skills)
        print(f"### {domain} ({len(skills)} skills)")
        for skill in skills[:5]:
            print(f"  - {skill}")
        if len(skills) > 5:
            print(f"  ... and {len(skills) - 5} more")
        print()

    total_mapped = len(mapped)
    total = total_orphan + total_mapped

    print("=== SUMMARY ===")
    print(f"Total skill specs: {total}")
    print(
        f"With implementation: {total_mapped} ({100 * total_mapped // total if total else 0}%)"
    )
    print(
        f"Orphaned (no code):  {total_orphan} ({100 * total_orphan // total if total else 0}%)"
    )

    if "--fix" in sys.argv:
        print("\n=== GENERATING CODE ===")
        for domain in sorted(orphaned.keys()):
            for skill_name in orphaned[domain]:
                print(f"python scripts/scaffold_skill.py '{skill_name}' {domain}")


if __name__ == "__main__":
    main()
