import json
import sys
from pathlib import Path

REGISTRY_FILE = Path(r"D:\Skill Flywheel\skill_registry.json")


def search_registry(query, max_results=10):
    query = query.lower()
    results = []

    if not REGISTRY_FILE.exists():
        return [{"error": "Registry file not found. Run reindex_skills.py first."}]

    try:
        with open(REGISTRY_FILE, encoding="utf-8") as f:
            registry = json.load(f)

        for skill in registry:
            score = 0
            name = skill.get("name", "").lower()
            purpose = skill.get("purpose", "").lower()
            description = skill.get("description", "").lower()

            if query in name:
                score += 10
            if query in purpose:
                score += 5
            if query in description:
                score += 3

            # Substring matches for words in query
            for word in query.split():
                if word in name or word in purpose or word in description:
                    score += 2

            if score > 0:
                results.append(
                    {
                        "name": skill.get("name"),
                        "domain": skill.get("domain"),
                        "purpose": (purpose[:100] + "...") if purpose else "",
                        "path": skill.get("path"),
                        "score": score,
                    }
                )
    except Exception as e:
        return [{"error": f"Error reading registry: {str(e)}"}]

    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No query provided"}))
        sys.exit(1)

    query = sys.argv[1]
    matches = search_registry(query)
    print(json.dumps(matches, indent=2))
