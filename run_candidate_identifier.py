import sys
sys.path.insert(0, 'src')

# Directly import the candidate identifier skill
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
print('Using: architecture-candidate-identifier skill')
print('=' * 70)
print(f'\nTotal skills in registry: {len(all_skills)}')

# Load Prolog and Hy surface code
import os
base_path = os.path.join(os.path.dirname(__file__), 'src', 'flywheel', 'skills', 'meta')
pl_path = os.path.join(base_path, 'candidate_identifier.pl')
hy_path = os.path.join(base_path, 'candidate_identifier.hy')

with open(pl_path, 'r') as f:
    prolog_code = f.read()
with open(hy_path, 'r') as f:
    hy_code = f.read()

print(f'\nProlog rules loaded: {len(prolog_code.split(chr(10)))} lines')
print(f'Hy scoring function loaded: {len(hy_code.split(chr(10)))} lines')

# Mock surfaces (since we can't actually run Prolog and Hy here easily)
# The actual assessment would use the surfaces to score each skill
print('\n' + '=' * 70)
print('ASSESSMENT METHODOLOGY')
print('=' * 70)
print("""
The architecture-candidate-identifier assesses skills using:

1. PROLOG SURFACE (Hard Rules):
   - Checks if skill domain is in Tier-1 domains:
     * epistemology, logic, logic_programming, game_theory,
     * formal_methods, reasoning
   - If yes -> 'Highly Recommended'
   - Otherwise -> 'Consider for Enhancement'

2. HY SURFACE (Soft Heuristics):
   - Analyzes skill description for keywords:
     logic, heuristic, rules, reliability, trust, verification,
     optimization, orchestration, reasoning, epistemic,
     validation, consensus, formal, mathematical, truth,
     inference, engine
   - Each match adds 0.15 to suitability score (0.1 base)
   - Score capped at 1.0

3. PYTHON SURFACE (Orchestration):
   - Combines Prolog and Hy results
   - Sorts by suitability score and priority
   - Returns top candidates
""")

# Run the actual candidate_identifier
result = candidate_identifier({'limit': 20}, {})

print('=' * 70)
print('TOP CANDIDATES FOR COLLECTIVE-MIND ARCHITECTURE')
print('=' * 70)
print(f'\nShowing top {len(result["top_candidates"])} of {result["total_analyzed"]} analyzed skills\n')

for i, c in enumerate(result['top_candidates'], 1):
    name = c['name']
    domain = c['domain']
    priority = c['priority']
    score = c['suitability_score']
    desc = c['description'][:100] if c['description'] else '(no description)'
    
    bar = '#' * int(score * 20)
    
    print(f'{i:>2}. {name}')
    print(f'    Domain: {domain}')
    print(f'    Priority: {priority}')
    print(f'    Suitability: {score:.2f} {bar}')
    print(f'    Description: {desc}')
    print()

print('=' * 70)
print('ASSESSMENT COMPLETE')
print('=' * 70)
