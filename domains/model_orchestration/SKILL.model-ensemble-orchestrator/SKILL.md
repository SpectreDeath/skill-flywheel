---
Domain: model_orchestration
Version: 4.2.0
Type: Strategy
Category: Model Orchestration
Complexity: Advanced
Estimated Execution Time: 1500ms
name: SKILL.model-ensemble-orchestrator
---

# Model Ensemble Orchestrator

## Description

Manages multi-model consensus and voting workflows by soliciting outputs from an ensemble of models and synthesizing results.

## Purpose

Ensures high output quality and hallucination detection for mission-critical tasks through collective model intelligence.

## Capabilities

- Ensemble selection based on task diversity
- Parallel request dispatching
- Response normalization and consistency analysis
- Majority (2/3) and weighted voting algorithms

## Usage Examples

- "Acknowledge a critical security vulnerability" -> Verify with 3 models.
- "Fact-check a historical claim" -> Consensus via diversity routing.

## Input Format

JSON request containing the prompt and ensemble size (3, 5, or 7).

## Output Format

Final consensus result, vote counts, and confidence scores.

## Configuration Options

- `ensemble_size`: Default 3
- `consensus_threshold`: Default 0.66

## Constraints

- **ALWAYS** use at least 3 models for ensemble voting.
- **MUST** log the identity of the dissenting model.
- **NEVER** use identical model checkpoints in the same ensemble.

## Examples

### Example 1: Security Scan

**Input**: "Is this snippet vulnerable?"
**Output**: Confirmed (3/3 Unanimous)

## Error Handling

- Case: Consensus Failure -> Action: Route to tie-breaker or human.
- Case: Member Dropout -> Action: Recalculate based on available quorum.

## Performance Optimization

- Utilize `asyncio.gather` for parallel dispatch.
- Implement strict per-member timeouts.

## Integration Examples

- Plugs into `AgentOrchestrator` for high-criticality missions.
- Accessible via `/model-ensemble`.

## Best Practices

- Use an odd number of models to avoid ties.
- Mix model families (Llama + GPT + Claude) to reduce bias.

## Troubleshooting

- Symptom: Constant tie-votes -> Check: Consensus threshold too high.
- Symptom: High cost -> Check: Ensemble size optimization.

## Monitoring and Metrics

- Track `ensemble_disagreement_rate`.
- Monitor `total_ensemble_duration`.

## Dependencies

- `async_executor`
- `semantic_comparator`

## Version History

- 1.0.0: Initial release
- 4.2.0: Synchronized with Skill Flywheel industrial standard

## License

MIT License
