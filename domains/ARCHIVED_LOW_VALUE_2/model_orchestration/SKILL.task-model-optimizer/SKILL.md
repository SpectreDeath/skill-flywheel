---
Domain: model_orchestration
Version: 4.2.0
Type: Strategy
Category: Model Orchestration
Complexity: Advanced
Estimated Execution Time: 35ms
name: SKILL.task-model-optimizer
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


# Task Model Optimizer

## Description

This skill implements a semantic routing layer that analyzes user requests to determine the "task intensity" and "domain requirements," matching them against model capabilities.

## Purpose

Routes specific task types (e.g., Coding, Reasoning, Extraction) to the most efficient and specialized model.

## Capabilities

- Request parsing and intent extraction
- Domain classification (CODING, REASONING, NLI, EXTRACTION)
- Capability mapping to Model Registry scores
- Efficiency weighting (Balance performance vs latency)

## Usage Examples

- "Write a script in Python" -> Route to DeepSeek-V2-Coder
- "Analyze a logical paradox" -> Route to o1-mini

## Input Format

String containing the user's task or request.

## Output Format

Recommended model ID and task domain classification.

## Configuration Options

- `preferred_coding_model`: DeepSeek-V2
- `preferred_reasoning_model`: o1-mini

## Constraints

- **ALWAYS** route coding tasks to designated coding specialists.
- **MUST NOT** use frontier models for tasks categorized as "Trivial/Formatting".
- **MUST** log every routing decision with a justification.

## Examples

### Example 1: Logic Puzzle

**Input**: "Riddle: What has keys but no locks?"
**Output**: o1-mini (Reasoning)

## Error Handling

- Case: Ambiguous Task -> Action: Route to versatile generalist (Claude 3.5 Sonnet).
- Case: Service DOWN -> Action: Fallback to next-best specialist.

## Performance Optimization

- Use lightweight embeddings for classify (<50ms).
- Cache domain mapping for identical request types.

## Integration Examples

- Integrated in `AgentOrchestrator` planner.
- Used in `/model-select` endpoint.

## Best Practices

- Use DeepSeek for all heavy coding tasks.
- Match task complexity level with model parameter count.

## Troubleshooting

- Symptom: Poor coding output -> Check: Router forced a generalist model.
- Symptom: High latency -> Check: Classification model overhead.

## Monitoring and Metrics

- Track `routing_accuracy_score`.
- Monitor `task_classification_latency`.

## Dependencies

- `semantic_analyzer`
- `model_registry`

## Version History

- 1.0.0: Initial release
- 4.2.0: Synchronized with Skill Flywheel industrial standard

## License

MIT License
