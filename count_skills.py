#!/usr/bin/env python3
"""
Count and analyze SKILL.md files across all domains
"""

import os
from pathlib import Path

def count_skill_files():
    skills_path = Path("skills")
    skill_files = []
    
    for domain_path in skills_path.iterdir():
        if domain_path.is_dir() and domain_path.name not in ['archive', 'mcp_tools', 'docs']:
            for skill_file in domain_path.glob("**/SKILL.*.md"):
                skill_files.append(skill_file)
            for skill_file in domain_path.glob("**/SKILL.md"):
                if skill_file not in skill_files:
                    skill_files.append(skill_file)
    
    print(f"Total SKILL files found: {len(skill_files)}")
    print("\nFiles by domain:")
    
    domain_counts = {}
    for skill_file in skill_files:
        domain = skill_file.parent.name
        if domain not in domain_counts:
            domain_counts[domain] = []
        domain_counts[domain].append(skill_file.name)
    
    for domain, files in sorted(domain_counts.items()):
        print(f"{domain}: {len(files)} files")
        for file in sorted(files):
            print(f"  - {file}")
    
    return skill_files

if __name__ == "__main__":
    count_skill_files()