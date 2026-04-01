#!/usr/bin/env python3
"""Analyze skills backlog."""
import json

with open('data/skills_backlog.json') as f:
    data = json.load(f)

statuses = {}
domains = {}
for item in data:
    s = item.get('status', 'unknown')
    statuses[s] = statuses.get(s, 0) + 1
    d = item.get('domain', 'unknown')
    domains[d] = domains.get(d, 0) + 1

print(f"Total entries: {len(data)}")
print(f"\nStatus counts: {json.dumps(statuses, indent=2)}")
print(f"\nDomain counts: {json.dumps(domains, indent=2)}")

non_impl = [item for item in data if item.get('status') != 'IMPLEMENTED']
print(f"\nNon-IMPLEMENTED: {len(non_impl)}")
for item in non_impl[:20]:
    print(f"  - {item.get('name')}: {item.get('status')} [{item.get('domain')}]")