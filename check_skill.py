import sqlite3
conn = sqlite3.connect('data/skill_registry.db')
cursor = conn.cursor()
cursor.execute("SELECT name, domain, description FROM skills WHERE name = 'bayesian-networks'")
row = cursor.fetchone()
if row:
    print('Name:', row[0])
    print('Domain:', row[1]) 
    print('Description:', row[2][:200] if row[2] else 'None')
else:
    print('Skill not found in database')
conn.close()