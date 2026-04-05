---
Domain: agent_evolution
Version: 1.0.0
Type: Meta-Process
Category: Capability Expansion
Complexity: High
Estimated Execution Time: 2m - 10m
name: autonomous-tool-learning
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


# SKILL: autonomous-tool-learning


## Implementation Notes
To be provided dynamically during execution.

## Description

Enables an agent to discover, analyze, and learn to use new tools or APIs by reading their documentation/MCP servers and generating their own internal "How-to" guides.

## Purpose

Allows the agent to expand its capabilities without manual skill drafting from a human.

## Capabilities

1. **API/MCP Surface Mapping**: Scans available tool definitions.
2. **Usage Pattern Discovery**: Reads examples and generates trial queries.
3. **Safety Shadowing**: Runs new tools in restricted/dry-run modes first.

## Usage Examples

"Learn how to use the new `database_migration` MCP tool."

## Input Format

```json
{
  "tool_name": "string",
  "documentation_uri": "string"
}
```

## Output Format

```markdown
### Tool Learning Summary
- **Primary Workflows**: [list]
- **Safety Constraints**: [list]
- **Example Usage**: [code]
```

## Configuration Options

- `validation_level`: (Dry-run|Limited-Execution|Full)

## Constraints

- NEVER run destructive commands during the learning phase.

## Examples

### Example 1: Learning a new CLI

**Input**: `git` documentation.
**Output**: Specialized `SKILL.git_wizard.md`.

## Error Handling

- **Ambiguous Docs**: Requests specific examples from the user if documentation is unclear.

## Performance Optimization

- **Lazy Schema Fetching**: Only reads tool schemas when invoked.

## Integration Examples

Feeds into `skill-drafting` to create permanent library additions.

## Best Practices

- Always start with `read-only` tools before moving to `write` tools.

## Troubleshooting

- **Incorrect Usage**: Check the generated `Usage Examples` section.

## Monitoring and Metrics

- **Learning Accuracy**: Percentage of first-run success after learning.

## Dependencies

- `schema_parser.py`

## Version History

- 1.0.0: Initial release.

## License

MIT License
