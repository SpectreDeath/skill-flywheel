import sys
sys.path.insert(0, 'src')

from flywheel.core.skills import EnhancedSkillManager
import asyncio

async def main():
    manager = EnhancedSkillManager(skills_dir='src/flywheel/skills')
    await manager.discover_skills()
    
    print("Discovered skills:")
    for name in sorted(manager.skills.keys()):
        print("  - " + name)
    
    if 'candidate_identifier' in manager.skills:
        print("\nFound candidate_identifier!")
    if 'meta.candidate_identifier' in manager.skills:
        print("\nFound meta.candidate_identifier!")

asyncio.run(main())
