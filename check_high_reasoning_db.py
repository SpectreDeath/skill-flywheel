import sqlite3
import os

db_path = r'D:\GitHub\projects\Skill Flywheel\data\skill_registry.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Check for high reasoning skills
    c.execute("SELECT name FROM skills WHERE name LIKE '%sat_solver%' OR name LIKE '%belief_revision%' OR name LIKE '%bayesian_networks%'")
    skills = c.fetchall()
    print("High reasoning skills in DB:")
    for skill in skills:
        print(f"  {skill[0]}")
    
    # Check for any skills with 'high_reasoning' in path
    c.execute("SELECT name FROM skills WHERE module_path LIKE '%high_reasoning%'")
    skills = c.fetchall()
    print("\nSkills with high_reasoning in module path:")
    for skill in skills:
        print(f"  {skill[0]}")
        
    conn.close()
else:
    print("Database file not found at:", db_path)