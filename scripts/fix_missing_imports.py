#!/usr/bin/env python3
"""Fix missing datetime imports and other common issues."""
import re
from pathlib import Path

SKILLS_DIR = Path("src/flywheel/skills")

def fix_file(filepath: Path) -> bool:
    content = filepath.read_text()
    if "from datetime import datetime" in content:
        return False
    
    # Add after first import statement
    lines = content.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            lines.insert(i + 1, "from datetime import datetime")
            break
    
    filepath.write_text("\n".join(lines))
    return True

# Fix cognitive skills
for f in (SKILLS_DIR / "cognitive_skills").glob("*.py"):
    if f.name == "__init__.py":
        continue
    if fix_file(f):
        print(f"Fixed: {f.name}")

# Fix other files with missing datetime
files_to_fix = [
    "src/flywheel/skills/distributed_systems/federated_learning_differential_privacy.py",
    "src/flywheel/skills/model_orchestration/hardware_model_selector.py",
    "src/flywheel/skills/model_orchestration/model_health_monitor.py",
    "src/flywheel/skills/SECURITY/secure_patterns.py",
    "src/flywheel/skills/TESTING_QUALITY/fuzzing_configurator.py",
    "src/flywheel/skills/CODEBASE_INTELLIGENCE/dependency_analyzer.py",
    "src/flywheel/skills/game_development/game_development.py",
]

for path in files_to_fix:
    p = Path(path)
    if p.exists():
        if fix_file(p):
            print(f"Fixed: {path}")

print("Done!")