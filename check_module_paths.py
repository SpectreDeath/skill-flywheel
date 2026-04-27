import sqlite3
import os

db_path = r'D:\GitHub\projects\Skill Flywheel\data\skill_registry.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Check module_path for high reasoning skills
    c.execute("""
        SELECT name, module_path 
        FROM skills 
        WHERE name IN ('sat-solver-optimization', 'belief-revision', 'bayesian-networks')
    """)
    skills = c.fetchall()
    print("Module paths for high reasoning skills:")
    for skill in skills:
        print(f"  {skill[0]}: {skill[1]}")
        
    conn.close()
else:
    print("Database file not found at:", db_path)