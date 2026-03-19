import json
import os
import re
from pathlib import Path

import yaml

WORKSPACE_ROOT = Path(__file__).parent.parent.parent
SKILLS_DIR = WORKSPACE_ROOT / "domains"
REGISTRY_FILE = WORKSPACE_ROOT / "skill_registry.json"

def get_skill_metadata(file_path):
    """Extract metadata from a SKILL.md file."""
    try:
        with open(file_path, encoding='utf-8') as f:
            content = f.read()
            
        if not content.startswith('---'):
            return None
            
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None
            
        fm = yaml.safe_load(parts[1]) or {}
        
        # Extract purpose
        purpose = ""
        purpose_match = re.search(r'## Purpose\s*\n\s*(.+)', parts[2])
        if purpose_match:
            purpose = purpose_match.group(1).strip()
            
        # Extract description
        description = ""
        desc_match = re.search(r'## Description\s*\n\s*(.+)', parts[2])
        if desc_match:
            description = desc_match.group(1).strip()

        return {
            "name": fm.get('name', file_path.parent.name),
            "domain": fm.get('Domain', 'General'),
            "version": fm.get('Version', '0.1.0'),
            "purpose": purpose,
            "description": description,
            "path": str(file_path.relative_to(SKILLS_DIR.parent)),
            "last_modified": os.path.getmtime(file_path)
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
            
    with open(REGISTRY_FILE, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)
        
    print(f"Successfully indexed {len(registry)} skills to {REGISTRY_FILE}")

if __name__ == "__main__":
    reindex()
