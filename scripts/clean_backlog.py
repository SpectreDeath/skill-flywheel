#!/usr/bin/env python3
"""Remove low/no-value skills from backlog and mark completed ones."""
import json

BACKLOG_PATH = 'data/skills_backlog.json'

with open(BACKLOG_PATH) as f:
    data = json.load(f)

print(f"Original backlog: {len(data)} entries")

# Skills to remove
remove_names = {
    # Archived placeholders (LOW VALUE)
    'ch-003', 'ch-006', 'ch-009',
    'database-security-ninja', 'database-whisperer-ai', 'query-time-machine',
    # Malware/C2 techniques (NO VALUE)
    'beacon-data-pipeline', 'beacon-management-gateway', 'beacon-ip-resolution',
    'covert-network-triggers', 'layered-crypto-channel', 'binary-configuration-patcher',
    'one-way-transfer', 'xor-string-obfuscation', 'self-deleting-daemon',
    'cross-platform-persistence', 'vpn-covert-redirect', 'cutthroat-ilm-plugin',
    # Missing source (performance_benchmarks domain deleted)
    'performance-benchmarks-database-performance-audit',
    'performance-benchmarks-memory-leak-detection',
    'performance-benchmarks-network-latency-analysis',
    'performance-benchmarks-query-optimization',
    'performance-benchmarks-response-time-monitoring',
    'performance-benchmarks-system-resource-monitoring',
}

# Mark these as IMPLEMENTED
implement_names = {
    'multi-platform-cross-compilation',
    'operational-deliverables',
}

filtered = []
removed_count = 0
implemented_count = 0

for item in data:
    name = item.get('name', '')
    if name in remove_names:
        removed_count += 1
        continue
    if name in implement_names:
        item['status'] = 'IMPLEMENTED'
        implemented_count += 1
    filtered.append(item)

with open(BACKLOG_PATH, 'w') as f:
    json.dump(filtered, f, indent=2)

print(f"Removed: {removed_count}")
print(f"Marked IMPLEMENTED: {implemented_count}")
print(f"New backlog: {len(filtered)} entries")