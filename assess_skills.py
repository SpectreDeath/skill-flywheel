import asyncio
import sys
sys.path.insert(0, 'src')
from flywheel.core.skills import EnhancedSkillManager

async def main():
    manager = EnhancedSkillManager(skills_dir='src/flywheel/skills')
    await manager.discover_skills()
    meta_module = await manager.load_skill_dynamically('meta.candidate_identifier')
    result = meta_module.candidate_identifier({'limit': 20}, {})
    print('Assessment Results:')
    print('Total analyzed:', result['total_analyzed'])
    print('Top candidates:')
    for i, c in enumerate(result['top_candidates'], 1):
        n = c['name']
        d = c['domain']
        p = c['priority']
        s = c['suitability_score']
        print('  ' + str(i) + '. ' + n + ' (' + d + ') - Priority: ' + p + ', Score: ' + str(s))

asyncio.run(main())