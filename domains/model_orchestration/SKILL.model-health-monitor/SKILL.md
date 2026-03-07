---
Domain: model_orchestration
Version: 4.2.0
Type: Strategy
Category: Model Orchestration
Complexity: Advanced
Estimated Execution Time: 50ms
name: SKILL.model-health-monitor
---

# Model Health Monitor

## Description

A diagnostics engine that performs automated health checks on model endpoints by evaluating GPU memory, inference errors, and token throughput stability.

## Purpose

Ensures only healthy models are included in active missions, automatically flagging and decommissioning degraded endpoints.

## Capabilities

- VRAM utilization tracking
- Inference error-code auditing (429, 500, 503)
- Throughput performance degradation detection
- Self-healing trigger generation (Context reset, Service restart)

## Usage Examples

- "Check health of Llama-70B on Port 8012" -> Status: Healthy (VRAM 18GB/24GB)
- "Audit error rates for GPT-4o" -> Status: Degraded (Rate 5.4%)

## Input Format

Model ID or endpoint URL to audit.

## Output Format

Health status (Healthy, Degraded, Critical), VRAM stats, and error log summary.

## Configuration Options

- `error_threshold_percentage`: Default 1.0%
- `vram_warning_level`: Default 85%

## Constraints

- **ALWAYS** perform a health check before including a model in a high-priority mission.
- **MUST** flag models as "Critical" if error rate exceeds 5.0%.
- **MUST** release VRAM in 30s if model is idle and flagged.

## Examples

### Example 1: GPU Under Stress

**Input**: Llama-3 (Port 8000)
**Output**: Status: Degraded (VRAM 23.5GB/24GB)

## Error Handling

- Case: NVML Failure -> Action: Use basic inference timing for health estimation.
- Case: No Probe Output -> Action: Flag as "Unknown/Stalled".

## Performance Optimization

- Use passive monitoring of active requests to reduce probe overhead.
- Aggregate metrics in a shared `performance_monitor` singleton.

## Integration Examples

- Integrated with `discovery_service.py` to update service status.
- Integrated with `McpHealthCheck` in Docker.

## Best Practices

- Monitor token throughput (Tokens/Sec) for "Silent Degradation".
- Use binary state checks (UP/DOWN) for fast routing decisions.

## Troubleshooting

- Symptom: Constant False Positives -> Check: Thresholds too sensitive.
- Symptom: Stale Health Data -> Check: Metric TTL in memory.

## Monitoring and Metrics

- Track `model_uptime_percentage`.
- Monitor `average_recovery_time_ms`.

## Dependencies

- `performance_monitor`
- `nvidia-ml-py`

## Version History

- 1.0.0: Initial release
- 4.2.0: Synchronized with Skill Flywheel industrial standard

## License

MIT License
