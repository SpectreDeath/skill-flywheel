---
Domain: agent_evolution
Version: 1.0.0
Type: Process
Category: Context Management
Complexity: Medium
Estimated Execution Time: 30s - 2m
name: dynamic-context-adaptation
---

# SKILL: dynamic-context-adaptation


## Implementation Notes
To be provided dynamically during execution.

## Description

Dynamically resizes, filters, and prioritizes the agent's context window based on task relevance, preventing "distraction" from stale information and optimizing token usage.

## Purpose

Ensures the agent stays focused on the most critical information while maintaining awareness of the broader task goals.

## Capabilities

1. **Context Slicing**: Automatically archives completed task sub-steps.
2. **Relevance Ranking**: Prioritizes current workspace files over reference docs.
3. **Adaptive Summarization**: Condenses large files into key semantic points if they exceed context limits.

## Usage Examples

### Basic Usage

"Optimize context for the current debugging task."

## Input Format

```json
{
  "focus_files": ["string"],
  "relevance_threshold": "float"
}
```

## Output Format

```markdown
### Context Optimization Report
- **Archived Tokens**: [count]
- **Current Focus**: [list]
```

## Configuration Options

- `max_context_window`: Hard limit for token count.

## Constraints

- DO NOT discard "Constitutional" rules or the current `task.md`.

## Examples

### Example 1: Context Pruning

**Input**: Context filled with 10k tokens of previous research.
**Output**: Summarized research + full focus on local source code.

## Error Handling

- **Critical Information Loss Detection**: Warns if a high-relevance item is being archived.

## Performance Optimization

- **Semantic Caching**: Stores summaries of large files to avoid re-summarizing.

## Integration Examples

Injects into the start of any complex Multi-Step task.

## Best Practices

- Clear context before switching to a fundamentally different TaskName.

## Troubleshooting

- **Loss of history**: Check the `archive_location` for retrieved summaries.

## Monitoring and Metrics

- **Token Compression Ratio**: Percentage of context reduced via summarization/pruning.

## Dependencies

- `token_counter.py`

## Version History

- 1.0.0: Initial release.

## License

MIT License
