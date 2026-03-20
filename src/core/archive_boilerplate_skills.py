import contextlib
import json
import shutil
from pathlib import Path


def archive_placeholders():
    workspace_root = Path(__file__).parent.parent.parent
    registry_path = workspace_root / "skill_registry.json"
    archive_dir = workspace_root / "domains" / "ARCHIVED" / "PLACEHOLDERS"
    
    if not registry_path.exists():
        print("Registry not found.")
        return

    with open(registry_path, encoding='utf-8') as f:
        registry = json.load(f)

    archive_dir.mkdir(parents=True, exist_ok=True)
    
    archived_count = 0
    placeholders = ["dynamically during execution", "*[Content for", "Auto-generated boilerplate"]
    
    new_registry = []
    
    for skill in registry:
        skill_path = workspace_root / skill['path']
        if not skill_path.exists():
            continue
            
        with open(skill_path, encoding='utf-8') as f:
            content = f.read()
            
        if any(p in content for p in placeholders):
            print(f"Archiving {skill['name']}...")
            
            # Create relative path in archive
            rel_path = skill_path.relative_to(workspace_root / "domains")
            target_path = archive_dir / rel_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file
            shutil.move(str(skill_path), str(target_path))
            
            # If directory is now empty, remove it (optional cleanup)
            with contextlib.suppress(OSError):
                skill_path.parent.rmdir()
                
            archived_count += 1
        else:
            new_registry.append(skill)

    # Update registry
    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(new_registry, f, indent=2)

    print(f"Archived {archived_count} placeholder skills. Updated registry with {len(new_registry)} skills.")

if __name__ == "__main__":
    archive_placeholders()
