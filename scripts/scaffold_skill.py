import os
import sys
import json
from pathlib import Path

def scaffold_skill(skill_name: str, domain: str = "General"):
    """
    Generate a boilerplate Python module for a skill based on its name.
    """
    skill_dir = Path("src/flywheel/skills") / domain.upper()
    skill_dir.mkdir(exist_ok=True, parents=True)
    
    safe_name = skill_name.lower().replace("-", "_")
    output_path = skill_dir / f"{safe_name}.py"
    
    if output_path.exists():
        print(f"Skill '{safe_name}' already exists at {output_path}")
        return
        
    content = f'''"""
Skill: {skill_name}
Domain: {domain}
"""

import logging

logger = logging.getLogger(__name__)

def {safe_name}(*args, **kwargs):
    """
    Main implementation for skill: {skill_name}
    """
    logger.info(f"Executing skill '{skill_name}' with args: {{args}}, kwargs: {{kwargs}}")
    
    # TODO: Implement core logic here
    result = {{
        "status": "success",
        "message": "Skill '{skill_name}' executed successfully from scaffold.",
        "input_args": args,
        "input_kwargs": kwargs
    }}
    
    return result
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Scaffolded skill '{skill_name}' in domain '{domain}' at {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/scaffold_skill.py <skill_name> [domain]")
        sys.exit(1)
        
    name = sys.argv[1]
    dom = sys.argv[2] if len(sys.argv) > 2 else "General"
    scaffold_skill(name, dom)
