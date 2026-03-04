---
Domain: agent_evolution
Version: 1.0.0
Type: Meta-Process
Category: Self-Optimization
Complexity: High
Estimated Execution Time: 5 - 15 minutes
name: self-improvement-loop
---

# SKILL: self-improvement-loop


## Implementation Notes
Content for ## Implementation Notes section to be added based on the specific skill requirements.

## Description

An autonomous meta-skill that enables an agent to identify logical inconsistencies, performance bottlenecks, and redundant patterns in its own execution history or codebase, and proactively propose or implement refinements.

## Purpose

Used to ensure continuous improvement of the agent's internal logic and operational efficiency. It moves from "reactive" bug fixing to "proactive" architectural evolution.

## Capabilities

1. **Log Entropy Analysis**: Scans execution logs for patterns of failure or inefficiency.
2. **Logic De-duplication**: Identifies overlapping or redundant workflow steps.
3. **Synthetic Fault Injection**: Proactively tests resilience by simulating environment failures.
4. **Performance Profiling**: Measures resource consumption per-task and identifies heavy nodes.

## Usage Examples

### Basic Usage

"Run a self-improvement audit on my last 5 task executions."

### Advanced Usage

"Initialize a recursive refinement cycle on the `ML_AI` skill domain to optimize token usage."

## Input Format

```json
{
  "target_history_depth": "integer",
  "focus_area": "string (logic|performance|reliability)",
  "automation_level": "string (audit|propose|implement)"
}
```

## Output Format

```markdown
### Self-Improvement Report
1. **Identified Bottlenecks**: [List]
2. **Proposed Refinements**: [List]
3. **Resilience Score**: [0-100]
```

## Configuration Options

- `recursion_limit`: Maximum number of refinement iterations.
- `safety_gate`: Boolean to require human approval for code writes.

## Constraints

- NEVER modify core "Constitutional" rules.
- ALWAYS backup files before applying automated refinements.
- MUST maintain backward compatibility for existing tool interfaces.

## Examples

### Example 1: Logic Consolidation

**Input**: Log history showing 3 redundant file listing calls.
**Output**: Proposed refactor to cache directory state.

## Error Handling

- **Circular Logic Detection**: Aborts if refinement creates an infinite loop.
- **Degradation Rollback**: Automatically reverts if performance metrics drop after a change.

## Performance Optimization

- **Parallel Trace Scanning**: Uses multi-threading to analyze large log files.
- **Incremental Indexing**: Only analyzes new logs since the last run.

## Integration Examples

Works in conjunction with `flywheel_loop.py` to provide the "Refine" phase of the cycle.

## Best Practices

- Run during idle periods to minimize impact on active tasks.
- Keep `safety_gate` enabled for architectural changes.

## Troubleshooting

- **No improvements found**: Increase `target_history_depth`.
- **High false-positives**: Refine the entropy threshold in configuration.

## Monitoring and Metrics

- **Improvement Delta**: Change in performance/success rate post-refinement.
- **Refinement Latency**: Time taken to identify and apply an improvement.

## Dependencies

- `log_parser.py` (internal utility)
- `resilience_tester.py` (internal utility)

## Version History

- 1.0.0: Initial release derived from Ralph Wiggum chaos loop.

## License

MIT License
