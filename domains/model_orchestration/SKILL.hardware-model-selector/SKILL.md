---
Domain: model_orchestration
Version: 4.2.0
Type: Strategy
Category: Model Orchestration
Complexity: Advanced
Estimated Execution Time: 20ms
name: SKILL.hardware-model-selector
---

# Hardware Model Selector

## Description

This skill provides a standardized framework for hardware-aware model routing by mapping system-level hardware characteristics (e.g., VRAM, CUDA cores) to model requirements.

## Purpose

Enables agents to autonomously determine the optimal LLM configuration based on available hardware profiles and resource constraints.

## Capabilities

- Hardware discovery and VRAM telemetry
- Profile generation for heterogeneous clusters
- Quantization-aware model mapping (4-bit/AWQ vs FP16)
- Safety margin calculations for KV cache headroom

## Usage Examples

- "Select a model for a laptop with 8GB VRAM" -> Result: "Llama-3-8B-Q4"
- "Select a model for an A100 cluster for 405B execution" -> Result: "Llama-3.1-405B-FP8"

## Input Format

JSON object containing `hardware_stats` (VRAM, compute_cap) or a string describing the device.

## Output Format

Recommended model ID, quantization level, and execution strategy.

## Configuration Options

- `min_headroom_gb`: Default 2.0
- `preferred_quantization`: Default AWQ

## Constraints

- **ALWAYS** check available VRAM before model selection.
- **NEVER** exceed 90% of available GPU VRAM.
- **MUST** provide a fallback model in every selection plan.

## Examples

### Example 1: High-End Consumer

**Input**: RTX 4090 (24GB)
**Output**: Llama-3.1-70B-AWQ

## Error Handling

- Case: OOM Imminent -> Action: Downscale to 8B model.
- Case: Driver Mismatch -> Action: Force CPU fallback or basic quantization.

## Performance Optimization

- Cache hardware profiles for 300s to avoid redundant `nvidia-smi` calls.
- Use pre-calculated VRAM tables for all registered models.

## Integration Examples

- Integrated into `AgentOrchestrator` mission planning lifecycle.
- Called via MCP tool `model_select`.

## Best Practices

- Always prioritize quantization for consumer hardware.
- Maintain a 2GB VRAM "System Buffer" at all times.

## Troubleshooting

- Symptom: Model load failure -> Check: `nvidia-smi` for hidden VRAM consumers.
- Symptom: Slow TTFT -> Check: Bus bandwidth vs model size.

## Monitoring and Metrics

- Track VRAM peaks and model load success rates.
- Monitor `hardware_selection_latency` (Target < 10ms).

## Dependencies

- `performance_monitor`
- `model_registry`
- `nvml-python`

## Version History

- 1.0.0: Initial release
- 4.2.0: Synchronized with Skill Flywheel industrial standard

## License

MIT License
