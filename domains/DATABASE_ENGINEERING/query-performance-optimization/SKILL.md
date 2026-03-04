---
Domain: DATABASE_ENGINEERING
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: query-performance-optimization
---


## Implementation Notes
Content for ## Implementation Notes section to be added based on the specific skill requirements.

## Description

Analyze and optimize slow SQL queries for better performance.

## Purpose

To identify and remediate inefficient SQL queries and schema designs that lead to slow application response times, high CPU/I/O usage, and database deadlocks.

## Capabilities

1. **Explain Plan Analysis**: Interpret output from `EXPLAIN ANALYZE` to identify seq scans and nested loops.
2. **Index Strategy**: Propose missing indexes (B-Tree, GIN, BRIN) based on query predicates.
3. **Wait Event Monitoring**: Correlate slow queries with system-level wait events (e.g., IO:DataFileRead).
4. **N+1 Query Detection**: Flag application-level loops that lead to redundant database roundtrips.

## Usage Examples

### Basic Usage

'Use query-performance-optimization to analyze my current project context.'

### Advanced Usage

'Run query-performance-optimization with focus on high-priority optimization targets.'

## Input Format

- **Query**: Natural language request or specific target identifier.
- **Context**: (Optional) Relevant file paths or metadata.
- **Options**: Custom parameters for execution depth.

## Output Format

- **Report**: A structured summary of findings and actions.
- **Artifacts**: (Optional) Generated files or updated configurations.
- **Status**: Success/Failure metrics with detailed logs.

## Configuration Options

- `execution_depth`: Control the thoroughness of the analysis (default: standard).
- `report_format`: Choose between markdown, json, or console output.
- `verbose`: Enable detailed logging for debugging purposes.

## Constraints

- NEVER apply schema changes (DDL) without a verified backup.
- DO NOT perform load testing on production instances during peak hours.
- MUST anonymize PII/sensitive data in query result samples.

## Examples

### Example 1: Optimizing an Unindexed Join

**Input**: Query joining `orders` and `users` without an index on `user_id`.
**Insight**: High cost due to sequential scan on `orders`.
**Action**: Propose `CREATE INDEX idx_orders_user_id ON orders(user_id);`.

## Error Handling

- **Invalid Input**: The skill will report specific missing parameters and request clarification.
- **Timeout**: Large-scale operations will be chunked to avoid process hangs.
- **Tool Failure**: Fallback mechanisms will attempt alternative logic paths.

## Performance Optimization

- **Caching**: Results are cached when applicable to reduce redundant computations.
- **Lazy Loading**: Supporting assets are only loaded when strictly necessary.
- **Parallelization**: Multi-target scans are executed in parallel where supported.

## Integration Examples

### Pipeline Integration

This skill is a core component of `FLOW.full_cycle.yaml` and works well with `skill-drafting` for automated refinement.

## Best Practices

- **Specific Context**: Provide as much specific context as possible for more accurate results.
- **Regular Audits**: Use this skill as part of a recurring CI/CD quality gate.
- **Review Outputs**: Always manually verify critical recommendations before implementation.

## Troubleshooting

- **Empty Results**: Verify that the input identifiers are correct and accessible.
- **Slow Execution**: Reduce the `execution_depth` or narrowed the focus area.
- **Permission Errors**: Ensure the agent has read/write access to the target directories.

## Monitoring and Metrics

- **Execution Time**: Tracked per run to identify bottlenecks.
- **Success Rate**: Monitored across automated cycles to ensure reliability.
- **Token Usage**: Optimized to minimize context window consumption.

## Dependencies

- **Standard Tools**: Requires base AgentSkills execution environment.
- **Python 3.10+**: For supporting scripts and automation logic.

## Version History

- **1.0.0**: Initial automated generation via Skill Flywheel Phase 7.

## License

MIT License - Part of the Open AgentSkills Library.
