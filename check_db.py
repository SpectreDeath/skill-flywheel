import sqlite3
import os

db_path = r'D:\GitHub\projects\Skill Flywheel\data\skill_registry.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Get tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    print("Tables:", tables)
    
    # Check skills table structure
    if tables:
        c.execute("PRAGMA table_info(skills)")
        columns = c.fetchall()
        print("\nSkills table columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Get some skills
        c.execute("SELECT name FROM skills LIMIT 10")
        skills = c.fetchall()
        print("\nFirst 10 skills:")
        for skill in skills:
            print(f"  {skill[0]}")
    
    conn.close()
else:
    print("Database file not found at:", db_path)