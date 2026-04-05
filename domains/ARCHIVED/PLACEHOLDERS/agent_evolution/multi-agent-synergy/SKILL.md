---
Domain: agent_evolution
Version: 1.0.0
Type: Orchestration
Category: Collaboration
Complexity: High
Estimated Execution Time: 1m - 5m
name: multi-agent-synergy
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


# SKILL: multi-agent-synergy


## Implementation Notes
To be provided dynamically during execution.

## Description

Orchestrates multiple agent instances or sub-agents by assigning specialized roles (e.g., Researcher, Coder, Reviewer) and managing the communication bridge between them.

## Purpose

Enables solving problems that are too large or complex for a single context window or perspective.

## Capabilities

1. **Role Delegation**: Assigns tasks based on sub-agent expertise.
2. **Conflict Resolution**: Mediates between divergent outputs from different agents.
3. **Synergy Scoring**: Evaluates the efficiency of the collaboration.

## Usage Examples

"Spin up a Reviewer agent to critique the current implementation."

## Input Format

```json
{
  "task_description": "string",
  "required_roles": ["string"]
}
```

## Output Format

```markdown
### Synergy Report
- **Delegated Tasks**: [list]
- **Consensus Result**: [text]
```

## Configuration Options

- `max_agents`: Maximum number of parallel sub-agents.

## Constraints

- MUST maintain a singular `task.md` as the source of truth for all agents.

## Examples

### Example 1: Pair Programming

**Input**: Code task.
**Output**: Parallel dev and test cycles.

## Error Handling

- **Agent Drift**: Identifies when a sub-agent diverges from the primary goal.

## Performance Optimization

- **Asynchronous Execution**: Runs non-dependent tasks in parallel.

## Integration Examples

Used by `flywheel_loop.py` for "Chaos" vs "Critique" separation.

## Best Practices

- Define clear interfaces between sub-agent tasks.

## Troubleshooting

- **Deadlock**: Check the `communication_log` for blocked agents.

## Monitoring and Metrics

- **Communication Overhead**: Token cost of agent-to-agent talk vs task work.

## Dependencies

- `orchestrator_node.py`

## Version History

- 1.0.0: Initial release.

## License

MIT License
