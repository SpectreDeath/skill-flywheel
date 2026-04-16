import sqlite3
import json
from pathlib import Path


def check_metadata():
    db_path = Path("data/skill_registry.db")
    if not db_path.exists():
        print("Database not found.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Find skills with missing tags or long descriptions
    cursor.execute("""
        SELECT name, domain, tags, description, category
        FROM skills 
        WHERE (tags = '[]' OR tags IS NULL) 
           OR (description IS NULL OR length(description) < 20)
        LIMIT 50
    """)

    rows = cursor.fetchall()
    needs_enrichment = [dict(r) for r in rows]

    print(f"Found {len(needs_enrichment)} skills needing enrichment.")
    for skill in needs_enrichment[:10]:
        desc_len = len(skill["description"]) if skill["description"] else 0
        print(
            f" - {skill['name']} ({skill['domain']}): Tags={skill['tags']}, Desc Len={desc_len}"
        )

    return needs_enrichment


if __name__ == "__main__":
    check_metadata()
