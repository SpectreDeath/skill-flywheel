import sqlite3

conn = sqlite3.connect('data/skill_registry.db')
cursor = conn.cursor()
cursor.execute("SELECT name, domain, description FROM skills WHERE name LIKE '%candidate%' OR name LIKE '%meta%'")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
