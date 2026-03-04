---
Domain: agent_evolution
Version: 1.0.0
Type: Meta-Process
Category: Logic
Complexity: Very High
Estimated Execution Time: 5m - 20m
name: recursive-reasoning-refinement
---

# SKILL: recursive-reasoning-refinement


## Implementation Notes
Content for ## Implementation Notes section to be added based on the specific skill requirements.

## Description

A deep-thought skill that forces the agent to take its own initial plan, attempt to find 3 ways it will fail, and then recursively refine the plan until it achieves a "Confidence Score" > 90%.

## Purpose

Ensures extreme reliability for critical or high-risk tasks by applying adversarial thinking to the agent's own logic.

## Capabilities

1. **Adversarial Critique**: Identifies hidden assumptions and failure points.
2. **Recursive Loop**: Re-plans based on critiques until criteria are met.
3. **Confidence Modeling**: Assigns a numeric probability of success.

## Usage Examples

"Apply recursive refinement to the database migration plan."

## Input Format

```json
{
  "initial_plan": "string",
  "success_criteria": ["string"]
}
```

## Output Format

```markdown
### Refined Plan
1. **Version 1 Critique**: [text]
2. **Refined Steps**: [list]
3. **Confidence Score**: [0-100]
```

## Configuration Options

- `max_recursions`: depth of the adversarial loop.

## Constraints

- STOP recursion if no improvement is found after 2 cycles.

## Examples

### Example 1: Critical Refactor

**Input**: Plan to change core auth logic.
**Output**: Refined plan with 5 additional safety checks.

## Error Handling

- **Analysis Paralysis**: Breaks the loop if confidence does not increase.

## Performance Optimization

- **Heuristic Pruning**: Skips refinement for low-risk sub-tasks.

## Integration Examples

Invoked during the PLANNING phase of any "High" complexity task.

## Best Practices

- Use a diverse set of "failure modes" during the critique phase.

## Troubleshooting

- **Infinite Loop**: Check the `recursion_depth` output.

## Monitoring and Metrics

- **Confidence Gain Index**: Increase in confidence per recursion.

## Dependencies

- `adversarial_logic_engine.py`

## Version History

- 1.0.0: Initial release.

## License

MIT License
