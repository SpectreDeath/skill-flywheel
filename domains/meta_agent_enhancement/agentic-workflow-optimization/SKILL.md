---
Domain: meta_agent_enhancement
Version: 1.0.0
Complexity: Medium
Type: Tool
Category: Efficiency
Estimated Execution Time: 500ms
name: agentic-workflow-optimization
---

# SKILL: Agentic Workflow Optimization


## Implementation Notes
To be provided dynamically during execution.

## Description

The Agentic Workflow Optimization skill is designed to enhance an agent's operational efficiency by analyzing its tool execution patterns. It identifies redundancies, optimizes sequence flows, and suggests parallel execution strategies to minimize latency and resource consumption.

## Purpose

Analyzes the agent's own tool usage history to identify redundant calls, high-latency bottlenecks, and opportunities for parallelization.

## Capabilities

1. Tool-call sequence auditing.
2. Latency and token consumption heatmapping.
3. Optimal path suggestion.

## Workflow

1. Collect telemetry from the last 10 tasks.
2. Identify patterns of "tool-pinging" or inefficient directory listing.
3. Generate an optimized "Execution Strategy" for future similar tasks.

## Usage Examples

- Optimizing a repetitive file-scanning loop.
- Identifying slow API calls in a multi-step data processing pipeline.
- Reducing token waste by streamlining redundant `list_dir` calls.

## Input Format

- **Telemetry Data**: A log of recent tool calls (name, duration, input, output).
- **Optimization Goal**: (Optional) Focus on latency, cost, or reliability.

## Output Format

- **Optimization Report**: JSON or Markdown summary of findings.
- **Execution Strategy**: Recommended tool sequence for future tasks.

## Configuration Options

- `history_depth`: Number of recent tasks to analyze (default: 10).
- `focus_area`: Priority (latency, cost, tokens).

## Constraints

- MUST NOT modify production code without user approval.
- ONLY analyzes historical data; does not perform real-time intervention.

## Examples

### Example 1: Streamlining Directory Access

**Input**: Sequence of 5 `list_dir` calls on the same path.
**Output**: Recommendation to cache directory state or use `find_by_name`.

## Error Handling

- Handles missing telemetry logs by reverting to heuristic-based optimization.
- Reports failures in parsing complex tool outputs gracefully.

## Performance Optimization

- Uses vectorized log analysis for fast processing of large telemetry volumes.

## Integration Examples

- Integrates with MCP telemetry collectors to ingest raw tool logs.

## Best Practices

- Run optimization after any major architectural change to the agent's toolset.
- Focus on the 20% of tools that cause 80% of the latency.

## Troubleshooting

- If no optimizations are suggested, ensure `history_depth` is sufficient to capture patterns.

## Monitoring and Metrics

- Tracks "Efficiency Gain" (time saved vs. original execution).

## Dependencies

- Requires access to a telemetry logging system or file.

## Version History

- 1.0.0: Initial release.

## License

MIT
