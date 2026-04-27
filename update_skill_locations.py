import sqlite3
import os

db_path = r'D:\GitHub\projects\Skill Flywheel\data\skill_registry.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Update the module_path for the three skills
    updates = [
        ('sat-solver-optimization', 'flywheel.skills.high_reasoning.sat_solver_optimization'),
        ('belief-revision', 'flywheel.skills.high_reasoning.belief_revision'),
        ('bayesian-networks', 'flywheel.skills.high_reasoning.bayesian_networks')
    ]
    
    for skill_name, new_module_path in updates:
        c.execute("""
            UPDATE skills 
            SET module_path = ? 
            WHERE name = ?
        """, (new_module_path, skill_name))
        print(f"Updated {skill_name}: module_path -> {new_module_path}")
        
        # Also, let's check and update entry_function if needed
        c.execute("SELECT entry_function FROM skills WHERE name = ?", (skill_name,))
        entry_function = c.fetchone()[0]
        print(f"  Current entry_function: {entry_function}")
        # If entry_function is empty or doesn't match the skill name, we might want to set it
        # But let's leave it as is for now, assuming it's correct.
    
    conn.commit()
    
    # Verify the updates
    print("\nVerification:")
    for skill_name, _ in updates:
        c.execute("SELECT name, module_path FROM skills WHERE name = ?", (skill_name,))
        row = c.fetchone()
        print(f"  {row[0]}: {row[1]}")
    
    conn.close()
else:
    print("Database file not found at:", db_path)