import sys
sys.path.insert(0, 'src')

from flywheel.skills.meta.candidate_identifier import candidate_identifier
import sqlite3

# Get skills from DB
conn = sqlite3.connect('data/skill_registry.db')
cursor = conn.cursor()
cursor.execute("SELECT name, domain, description FROM skills")
all_skills = cursor.fetchall()
conn.close()

print('=' * 70)
print('COLLECTIVE-MIND ARCHITECTURE ASSESSMENT')
print('=' * 70)
print(f'\nTotal skills in registry: {len(all_skills)}')

# Keywords that boost Hy surface score
keywords = ['logic', 'heuristic', 'rules', 'reliability', 'trust', 'verification',
            'optimization', 'orchestration', 'reasoning', 'epistemic',
            'validation', 'consensus', 'formal', 'mathematical', 'truth',
            'inference', 'engine']

# Find skills with keyword-rich descriptions
print('\nSkills with HIGH potential (description contains 3+ keywords):')
print('-' * 70)
high_potential = []
for name, domain, desc in all_skills:
    if desc:
        desc_lower = desc.lower()
        matches = sum(1 for kw in keywords if kw in desc_lower)
        if matches >= 3:
            high_potential.append((name, domain, desc, matches))

high_potential.sort(key=lambda x: x[3], reverse=True)
for name, domain, desc, matches in high_potential[:20]:
    print(f'  {name:40s} ({domain:25s}) [{matches} keywords]')

print(f'\nFound {len(high_potential)} skills with 3+ keywords')

# Tier-1 domains (Prolog hard rules)
tier1 = {'epistemology', 'logic', 'logic_programming', 'game_theory', 
         'formal_methods', 'reasoning'}

print('\nSkills in TIER-1 domains (Prolog hard rules):')
print('-' * 70)
tier1_skills = [(n, d, desc) for n, d, desc in all_skills if d.lower() in tier1]
for name, domain, desc in sorted(tier1_skills)[:20]:
    print(f'  {name:40s} ({domain})')
print(f'\nFound {len(tier1_skills)} Tier-1 domain skills')

# Run the actual candidate_identifier
print('\n' + '=' * 70)
print('RUNNING CANDIDATE_IDENTIFIER SKILL')
print('=' * 70)
result = candidate_identifier({'limit': 20}, {})

print('\nTop candidates from candidate_identifier:')
print('=' * 70)
for i, c in enumerate(result['top_candidates'], 1):
    name = c['name']
    domain = c['domain']
    priority = c['priority']
    score = c['suitability_score']
    desc = c['description'][:80] if c['description'] else '(no description)'
    bar = '#' * max(1, int(score * 20))
    print(f'{i:>2}. {name}')
    print(f'    Domain: {domain}')
    print(f'    Priority: {priority}')
    print(f'    Suitability: {score:.2f} {bar}')
    print(f'    Description: {desc}')
    print()
