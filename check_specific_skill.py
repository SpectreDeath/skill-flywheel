import sqlite3
import os

db_path = r'D:\GitHub\projects\Skill Flywheel\data\skill_registry.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Check the exact entry for sat-solver-optimization
    c.execute("""
        SELECT name, module_path, entry_function, version, description, dependencies
        FROM skills 
        WHERE name = 'sat-solver-optimization'
    """)
    row = c.fetchone()
    if row:
        print("sat-solver-optimization:")
        print(f"  name: {row[0]}")
        print(f"  module_path: {row[1]}")
        print(f"  entry_function: {row[2]}")
        print(f"  version: {row[3]}")
        print(f"  description: {row[4][:50]}..." if row[4] else "  description: None")
        print(f"  dependencies: {row[5]}")
    else:
        print("sat-solver-optimization not found in DB")
    
    conn.close()
else:
    print("Database file not found at:", db_path)