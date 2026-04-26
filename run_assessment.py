import sys
sys.path.insert(0, 'src')

from flywheel.core.skills import EnhancedSkillManager
import asyncio

async def main():
    manager = EnhancedSkillManager(skills_dir='src/flywheel/skills')
    await manager.discover_skills()
    
    # Load the candidate identifier
    meta_skill = await manager.load_skill_dynamically('meta.candidate_identifier')
    
    # Run the assessment
    result = meta_skill.candidate_identifier({'limit': 20}, {})
    
    print('=' * 60)
    print('COLLECTIVE-MIND ARCHITECTURE ASSESSMENT RESULTS')
    print('=' * 60)
    print(f'\nTotal skills analyzed: {result["total_analyzed"]}')
    print(f'Architecture pattern: Collective-Mind (Python + Prolog + Hy)')
    print(f'\nTop {len(result["top_candidates"])} candidates for upgrade:\n')
    
    for i, c in enumerate(result['top_candidates'], 1):
        name = c['name']
        domain = c['domain']
        priority = c['priority']
        score = c['suitability_score']
        desc = c['description'][:80]
        
        bar = '#' * int(score * 20)
        
        print(f'{i:>2}. {name}')
        print(f'    Domain: {domain}')
        print(f'    Priority: {priority}')
        print(f'    Suitability: {score:.2f} {bar}')
        print(f'    Description: {desc}...')
        print()

asyncio.run(main())
