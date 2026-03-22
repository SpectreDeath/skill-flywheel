import sqlite3
from pathlib import Path

def check_schema():
    db_path = Path("data/skill_registry.db")
    if not db_path.exists():
        print("Database not found.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(skills)")
    rows = cursor.fetchall()
    
    print("Schema for 'skills' table:")
    for row in rows:
        print(f" - {row['name']} ({row['type']})")

if __name__ == "__main__":
    check_schema()
