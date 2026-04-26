import sqlite3
conn = sqlite3.connect('data/skill_registry.db')
cursor = conn.cursor()
cursor.execute("SELECT name, domain FROM skills WHERE domain = 'probabilistic_models'")
rows = cursor.fetchall()
print('Skills in probabilistic_models domain:')
for row in rows:
    print(' ', row[0])
conn.close()