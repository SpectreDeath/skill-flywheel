import json
from pathlib import Path

def get_skills_needing_enrichment(limit=10):
    registry_path = Path("skill_registry.json")
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    
    needing = []
    for skill in registry:
        if not skill.get("tags") or skill["tags"] == []:
            needing.append(skill)
            if len(needing) >= limit:
                break
    return needing

def update_skill(name, enriched_data):
    registry_path = Path("skill_registry.json")
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    
    for skill in registry:
        if skill["name"] == name:
            skill.update(enriched_data)
            break
            
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    print(f"Updated {name}")

if __name__ == "__main__":
    skills = get_skills_needing_enrichment()
    for s in skills:
        print(f"ID: {s['name']} | Path: {s['path']}")
