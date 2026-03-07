---
Domain: model_orchestration
Version: 4.2.0
Type: Strategy
Category: Model Orchestration
Complexity: Advanced
Estimated Execution Time: 25ms
name: SKILL.dynamic-model-router
---

# Dynamic Model Router

## Description

An intelligent traffic controller that monitors QoS metrics and performs "hot-swaps" between model endpoints during active missions.

## Purpose

Enables threshold-based switching to maintain session continuity when latency, error rates, or costs exceed bounds.

## Capabilities

- Real-time QoS monitoring (Latency, 5xx errors)
- Threshold evaluation and trigger events
- Instantaneous hot-swapping to warm standby models
- State preservation across model transitions

## Usage Examples

- "Primary model latency > 2s" -> Trigger swap to fallback Llama-8B.
- "Endpoint returns 503" -> Re-route task to secondary provider.

## Input Format

Inference request stream with attached QoS policies.

## Output Format

Routed request to the optimal healthy endpoint.

## Configuration Options

- `latency_threshold_ms`: Default 2000
- `success_rate_threshold`: Default 0.95

## Constraints

- **ALWAYS** maintain a warm fallback model for critical missions.
- **MUST NOT** swap to a model with lower reasoning capability for complex tasks.
- **MUST** log the reason for every hot-swap event.

## Examples

### Example 1: Provider Outage

**Input**: OpenAI 503 status
**Output**: Redirected to Claude 3.5 via AWS Bedrock

## Error Handling

- Case: Pool Exhaustion -> Action: Pause mission and alert operator.
- Case: Ping-Ponging -> Action: Implement 60s swap cooldown.

## Performance Optimization

- Routing decision mapping in <2ms.
- Use persistent connections to fallback providers.

## Integration Examples

- Integrated with `discovery_service.py` health-checks.
- Integrated with `agent_orchestration.py` mission planner.

## Best Practices

- Keep a local Llama-8B as the ultimate safe fallback.
- Set thresholds based on human-perceived responsiveness (2.5s).

## Troubleshooting

- Symptom: Infinite swapping -> Check: Thresholds too tight (noise).
- Symptom: Broken context -> Check: State-sync during mid-task swap.

## Monitoring and Metrics

- Track `total_swaps_per_hour`.
- Monitor `downtime_prevented_seconds`.

## Dependencies

- `performance_monitor`
- `discovery_service`

## Version History

- 1.0.0: Initial release
- 4.2.0: Synchronized with Skill Flywheel industrial standard

## License

MIT License
