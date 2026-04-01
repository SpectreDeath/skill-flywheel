#!/usr/bin/env python3
"""Assess value of NOT_IMPLEMENTED skills."""
import json, os

with open('data/skills_backlog.json') as f:
    data = json.load(f)

non_impl = [item for item in data if item.get('status') != 'IMPLEMENTED']

archived = []
missing_source = []
malware_related = []

for item in non_impl:
    name = item.get('name', '')
    source = item.get('source_doc', '')

    if 'ARCHIVED' in source or 'PLACEHOLDER' in source:
        archived.append(name)
    elif 'performance_benchmarks' in source and 'database-performance-audit' in name:
        missing_source.append(name)
    elif 'performance_benchmarks' in source:
        missing_source.append(name)
    elif any(x in name.lower() for x in [
        'beacon', 'covert', 'crypto-channel', 'xor-string',
        'self-deleting', 'vpn-covert', 'cutthroat', 'one-way-transfer',
        'ip-resolution', 'cross-platform-persistence', 'beacon-management',
        'binary-configuration'
    ]):
        malware_related.append(name)
    else:
        print(f'UNKNOWN CATEGORY: {name}')

print('=== LOW VALUE: Archived Placeholders (16) ===')
for x in archived:
    print(f'  - {x}')

print()
print('=== MISSING SOURCE: performance_benchmarks deleted (6) ===')
for x in missing_source:
    print(f'  - {x}')

print()
print('=== NO VALUE: Malware/C2 Techniques (4) ===')
for x in malware_related:
    print(f'  - {x}')