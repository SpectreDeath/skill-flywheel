import sqlite3

conn = sqlite3.connect('data/skill_registry.db')
c = conn.cursor()
c.execute('SELECT name, domain FROM skills WHERE domain LIKE "%HIGH%" LIMIT 20')
skills = c.fetchall()
print('High reasoning skills in DB:')
for skill in skills:
    print(f'  {skill[0]} - {skill[1]}')
conn.close()