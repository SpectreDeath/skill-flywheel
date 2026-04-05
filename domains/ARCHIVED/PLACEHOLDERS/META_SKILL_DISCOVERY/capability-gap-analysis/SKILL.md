---
Domain: META_SKILL_DISCOVERY
Version: 1.0.0
Type: Meta-Process
Category: Strategic Planning
Complexity: High
Estimated Execution Time: 2m - 5m
name: capability-gap-analysis
---
origin: manual
triggers:
  - agent
  - ai
  - development
quality:
  applied_count: 0
  success_count: 0
  completion_rate: 0.0
  token_savings_avg: 0.0
created_at: "2026-03-24T10:00:00Z"
updated_at: "2026-03-24T10:00:00Z"


# SKILL: capability-gap-analysis


## Implementation Notes
To be provided dynamically during execution.

## Description

Systematically identifies missing capabilities in the skill library by analyzing task failure logs and industry-standard competency frameworks.

## Purpose

Provides the "Input" for the Ralph Wiggum chaos flywheel by identifying what *should* exist but doesn't.

## Capabilities

1. **Failure Log Mining**: Extracts keywords from tasks where the agent lacked a specialized skill.
2. **Competency Benchmarking**: Compares the library against predefined goal domains (e.g., DevOps, Security).
3. **Priority Ranking**: Identifies which missing skills would have the highest impact.

## Usage Examples

"Perform a gap analysis on the `agent_evolution` domain."

## Input Format

```json
{
  "target_domain": "string",
  "data_source": "string (logs|framework)"
}
```

## Output Format

```markdown
### Capability Gap Report
- **Missing Skills**: [list]
- **Target Contexts**: [list]
- **Impact Score**: [0-10]
```

## Configuration Options

- `benchmark_framework`: URI to a standard competency matrix.

## Constraints

- FOCUS on capabilities that cannot be currently solved by composing existing skills.

## Examples

### Example 1: Identifying ML gaps

**Input**: Search logs for "LLM Quantization".
**Output**: Identified gap for `SKILL.quantization_advisor.md`.

## Error Handling

- **Insufficient Data**: Reports if too few logs are available for meaningful analysis.

## Performance Optimization

- **Keyword Clustering**: Uses frequency analysis to group fragmented requests into single capability targets.

## Integration Examples

Feeds directly into `flywheel_loop.py` Phase 1 (Chaos Generation).

## Best Practices

- Update the competency benchmark regularly as new technologies emerge.

## Troubleshooting

- **Overlapping results**: Ensure existing skills are properly indexed before running the analysis.

## Monitoring and Metrics

- **Library Coverage Index**: Percentage of targeted domain competencies currently implemented.

## Dependencies

- `log_miner.py` (internal utility)

## Version History

- 1.0.0: Initial release.

## License

MIT License
