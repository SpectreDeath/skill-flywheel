---
Domain: meta_agent_enhancement
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Quality
Estimated Execution Time: 1s
name: cognitive-bias-guardrail
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


# SKILL: Cognitive Bias Guardrail


## Implementation Notes
To be provided dynamically during execution.

## Description

The Cognitive Bias Guardrail skill provides a structured method for detecting and mitigating common cognitive biases in LLM outputs. It focuses on identifying "lazy" implementation patterns, recency bias in library selection, and compliance mimicry, ensuring that the agent's reasoning remains thorough and objective.

## Purpose

Detects and corrects common LLM biases such as 'Laziness' (skipping boilerplate), 'Recency Bias' (overusing the most recent library version regardless of fit), and 'Compliance Mimicry'.

## Capabilities

1. Pattern-match for "I have skipped the rest of the code" lazy blocks.
2. Contextual check for implementation completeness.
3. Bias scoring (1-10) for suggested approaches.

## Workflow

1. Scan draft output for bias markers.
2. Flag "lazy" segments for immediate regeneration.
3. Re-evaluate alternative solutions to ensure non-biased selection.

## Usage Examples

- Reviewing a large code refactor to ensure no "TBD" or placeholder comments were accidentally left.
- Checking if a suggested library is truly the best fit or just the most "hyped" one.
- Validating that the agent isn't just saying "Yes" to satisfy a user's leading question.

## Input Format

- **Content to Review**: Text, code, or architectural designs.
- **Bias Profile**: (Optional) Specific biases to focus on (e.g., "anti-boilerplate").

## Output Format

- **Bias Assessment**: A report detailing detected biases and their location.
- **Corrected Content**: A revised version of the input with biases mitigated.

## Configuration Options

- `rigor_level`: Sensitivity of the detection (Low, Medium, High).
- `bias_whitelist`: Specific patterns to ignore.

## Constraints

- MUST NOT suppress creative solutions that happen to look like bias without verification.
- MUST provide clear reasoning for every "bias" flag raised.

## Examples

### Example 1: Detecting Boilerplate Skipping

**Input**: "I have implemented the main logic, you can fill in the imports."
**Output**: Flagged as "Laziness Bias". Recommendation: Generate complete, copy-pasteable code.

## Error Handling

- If the context window is too small for full re-evaluation, it prioritizes the most high-impact bias checks.

## Performance Optimization

- Uses regex-based pre-screening to quickly identify obvious bias markers before deeper semantic analysis.

## Integration Examples

- Can be used as a pre-commit hook or as a final validation step in an automated agentic loop.

## Best Practices

- Use in conjunction with "Agentic Workflow Optimization" for maximum efficiency and quality.
- Regularly update the bias markers as LLM behavior evolves.

## Troubleshooting

- If legitimate shortcuts are being flagged, adjust the `rigor_level` to Medium or Low.

## Monitoring and Metrics

- Tracks "Boilerplate Completion Rate" and "Bias Mitigation Score".

## Dependencies

- No external tool dependencies; uses internal semantic processing.

## Version History

- 1.0.0: Initial release.

## License

MIT
