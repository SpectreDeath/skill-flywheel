---
name: spec-evolution-engine
description: "Use when: planning specification version upgrades, managing backward compatibility during spec changes, guiding specification evolution strategy, or designing migration paths for breaking changes. Triggers: 'spec evolution', 'version upgrade', 'migration', 'backward compatibility', 'deprecation', 'semver', 'breaking changes'. NOT for: internal APIs without consumers, rapid prototyping, or specs without dependencies."
---

# Spec Evolution Engine

Manage specification versioning and evolution while maintaining backward compatibility through predictive analysis and strategic planning. This skill guides spec evolution with migration support.

## When to Use This Skill

Use this skill when:
- Planning specification version upgrades
- Managing backward compatibility during spec changes
- Guiding specification evolution strategy
- Designing migration paths for breaking changes
- Strategic API versioning decisions

Do NOT use this skill when:
- Internal APIs without external consumers
- Rapid prototyping phases
- Simple specifications without dependencies

## Input Format

```yaml
evolution_request:
  current_spec: string           # Current specification
  proposed_changes: array        # Proposed changes to evaluate
  compatibility_mode: string     # Compatibility level (strict, lenient)
  timeline: object              # Evolution timeline requirements
```

## Output Format

```yaml
evolution_result:
  strategy: object               # Recommended evolution strategy
  breaking_changes: array       # Identified breaking changes
  migration_path: object        # Recommended migration path
  compatibility_score: number   # Backward compatibility score
  rollout_plan: object          # Phased rollout plan
```

## Capabilities

### 1. Compatibility Analysis (15 min)

- Analyze proposed changes for compatibility
- Identify breaking changes
- Calculate compatibility impact

### 2. Migration Planning (15 min)

- Design migration paths
- Identify deprecated features
- Create backward compatibility layers

### 3. Version Strategy (10 min)

- Recommend version numbering (semver)
- Define deprecation timeline
- Plan feature flags

### 4. Impact Modeling (15 min)

- Model impact on consumers
- Estimate migration effort
- Identify risk factors

### 5. Rollout Planning (10 min)

- Create phased rollout plan
- Define rollback procedures
- Set success criteria

## Usage Examples

### Basic Usage

"Plan evolution of my API specification with backward compatibility."

### Advanced Usage

"Generate full migration strategy for breaking changes with phased rollout."

## When to Use

- Planning API specification changes
- Managing shared specifications with multiple consumers
- Ensuring backward compatibility
- Strategic versioning decisions

## When NOT to Use

- Internal APIs without consumers
- Rapid prototyping phases
- Simple specifications without dependencies

## Configuration Options

- `compatibility_mode`: Strict or lenient
- `deprecation_period`: Time before removing features
- `feature_flags`: Enable feature flagging
- `auto_migration`: Auto-generate migration code

## Constraints

- MUST maintain backward compatibility when possible
- SHOULD provide clear deprecation timelines
- MUST identify all breaking changes
- SHOULD minimize consumer impact

## Integration Examples

- API registries: Publish versioned specs
- Documentation: Generate changelogs
- CI/CD: Validate compatibility in pipeline

## Dependencies

- Python 3.10+
- Specification parsers
- Optional: Migration code generators
