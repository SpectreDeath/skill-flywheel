---
name: spec-regression-monitoring
description: "Use when: tracking specification drift over time, monitoring spec changes for regressions, validating backward compatibility during spec evolution, or detecting breaking changes in APIs. Triggers: 'spec regression', 'breaking changes', 'backward compatibility', 'spec drift', 'spec version', 'version comparison', 'spec monitoring'. NOT for: stable rarely-changing specs, single-team projects without consumers, or early-stage prototyping."
---

# Spec Regression Monitoring

Monitor specification evolution and detect regression issues to ensure changes maintain backward compatibility. This skill provides proactive breaking change detection and impact analysis.

## When to Use This Skill

Use this skill when:
- Tracking specification drift over time
- Monitoring spec changes for regressions
- Validating backward compatibility during spec evolution
- Detecting breaking changes in APIs
- Managing API versioning with multiple consumers

Do NOT use this skill when:
- Stable, rarely-changing specifications
- Single-team projects without external consumers
- Early-stage prototyping

## Input Format

```yaml
monitoring_request:
  spec_versions: array           # Historical spec versions to compare
  current_spec: string           # Current specification path
  baseline: string               # Baseline version for comparison
  watchlist: array              # Specific requirements to monitor
```

## Output Format

```yaml
monitoring_result:
  drift_detected: boolean        # Whether drift was detected
  changes: array                 # List of changes since baseline
  breaking_changes: array       # Breaking changes identified
  impact_analysis: object        # Impact assessment
  alerts: array                  # Generated alerts
```

## Capabilities

### 1. Version Comparison (10 min)

- Compare specification versions
- Identify additions, modifications, deletions
- Calculate change magnitude

### 2. Breaking Change Detection (15 min)

- Detect breaking changes in APIs
- Identify backward incompatibilities
- Flag deprecated features

### 3. Drift Monitoring (10 min)

- Track specification drift in real-time
- Monitor for unintended changes
- Alert on significant deviations

### 4. Impact Analysis (15 min)

- Assess impact of spec changes
- Identify affected implementations
- Estimate migration effort

### 5. Regression Reporting (10 min)

- Generate regression reports
- Track regression trends over time
- Maintain change history

## Usage Examples

### Basic Usage

"Check my API spec for breaking changes since last version."

### Advanced Usage

"Monitor specification drift and alert on regressions in production systems."

## When to Use

- API versioning and evolution
- Maintaining backward compatibility
- Compliance and audit requirements
- Multiple teams consuming shared specs

## When NOT to Use

- Stable, rarely-changing specifications
- Single-team projects without external consumers
- Early-stage prototyping

## Configuration Options

- `sensitivity`: Detection sensitivity (low, medium, high)
- `alert_threshold`: Alert on change percentage
- `auto_monitor`: Enable real-time monitoring
- `breaking_changes`: Define what constitutes breaking

## Constraints

- MUST detect all breaking changes
- SHOULD provide migration guidance
- MUST maintain change history
- SHOULD minimize false positives

## Integration Examples

- API gateways: Block breaking changes
- CI/CD: Fail builds on breaking changes
- API registries: Update version documentation

## Dependencies

- Python 3.10+
- Diff libraries for version comparison
- Optional: API specification parsers
