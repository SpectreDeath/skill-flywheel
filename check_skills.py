#!/usr/bin/env python3
import json

with open('skill_registry.json', 'r') as f:
    registry = json.load(f)

total_skills = len(registry)
print(f'Total skills in registry: {total_skills}')
print(f'Target: 226 skills')
print(f'Difference: {226 - total_skills} skills needed')

# Check for strategy_analysis domain
strategy_skills = [skill for skill in registry if 'strategy' in skill['domain'].lower()]
print(f'\nStrategy-related domains: {len(strategy_skills)} skills')
for skill in strategy_skills:
    print(f'  - {skill["domain"]}: {skill["name"]}')

# Check for DOMAIN directory
import os
if os.path.exists('skills/DOMAIN'):
    domain_dirs = [d for d in os.listdir('skills/DOMAIN') if os.path.isdir(f'skills/DOMAIN/{d}')]
    print(f'\nDOMAIN subdirectories: {domain_dirs}')
else:
    print('\nNo DOMAIN directory found')