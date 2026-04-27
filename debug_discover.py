import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flywheel.core.skills import EnhancedSkillManager
import asyncio

async def debug_discover_skills():
    print("Creating EnhancedSkillManager...")
    skill_manager = EnhancedSkillManager(skills_dir='src/flywheel/skills')
    
    print("Calling discover_skills...")
    skills = await skill_manager.discover_skills()
    
    print(f"Discovered {len(skills)} skills")
    
    # Check for our specific skills
    sat_solver_skills = [s for s in skills if 'sat_solver' in s]
    print(f"SAT solver skills: {sat_solver_skills}")
    
    high_reasoning_skills = [s for s in skills if 'high_reasoning' in s]
    print(f"High reasoning skills: {high_reasoning_skills}")
    
    # Let's also check what's in the skills dict
    print(f"\nSkills in manager: {len(skill_manager.skills)}")
    sat_solver_in_manager = [k for k in skill_manager.skills.keys() if 'sat_solver' in k]
    print(f"SAT solver skills in manager: {sat_solver_in_manager}")
    
    # Let's look at a few skills to see the pattern
    print("\nFirst 10 skills in manager:")
    for i, (name, metadata) in enumerate(list(skill_manager.skills.items())[:10]):
        print(f"  {name}: version={metadata.version}")

if __name__ == "__main__":
    asyncio.run(debug_discover_skills())