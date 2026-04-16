#!/usr/bin/env python3
"""Enrich skills in the registry."""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path("data/skill_registry.db")


def get_skills_needing_enrichment(limit=10):
    """Get skills that need enrichment (missing tags or short descriptions)."""
    if not DB_PATH.exists():
        print("Database not found.")
        return []

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT skill_id, name, domain, description, tags
        FROM skills 
        WHERE (tags = '[]' OR tags IS NULL OR tags = '')
           OR (description IS NULL OR length(description) < 20)
        LIMIT ?
    """,
        (limit,),
    )

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def update_skill(name, enriched_data):
    """Update a skill with enriched data."""
    if not DB_PATH.exists():
        print("Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tags = json.dumps(enriched_data.get("tags", []))
    description = enriched_data.get("description", "")
    category = enriched_data.get("category", "")
    complexity = enriched_data.get("complexity", "")

    cursor.execute(
        """
        UPDATE skills 
        SET tags = ?, description = ?, category = ?, complexity = ?
        WHERE name = ?
    """,
        (tags, description, category, complexity, name),
    )

    conn.commit()
    conn.close()
    print(f"Updated {name}")


if __name__ == "__main__":
    skills = get_skills_needing_enrichment()
    print(f"Found {len(skills)} skills needing enrichment:")
    for s in skills:
        desc_len = len(s["description"]) if s["description"] else 0
        print(f"  - {s['name']} ({s['domain']}): desc_len={desc_len}, tags={s['tags']}")

    if skills:
        print("\nTo enrich: call update_skill(name, enriched_data)")
