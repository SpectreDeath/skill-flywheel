---
Domain: APPLICATION_SECURITY
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: skill-evolution
---

## Description

The Skill Evolution meta-skill analyzes execution logs and usage patterns to automatically generate specialized variants of existing skills. It enables the library to grow organically and adapt to specific domain requirements based on real-world feedback.

## Purpose

Analyze skill usage patterns and automatically generate specialized variants to enable exponential library growth and self-improvement.

## Input Format

### Skill Evolution Request

```yaml
skill_evolution_request:
  base_skill_path: string         # Path to the base SKILL.md
  usage_logs_path: string         # Path to the execution logs directory
  target_variants: number         # Number of specialized variants to generate
  optimization_goals: array       # (Optional) Specific goals (e.g., "performance", "safety")
  domain_context: string          # (Optional) Specific domain context for specialization
```

## Output Format

### Skill Evolution Report

```yaml
skill_evolution_report:
  variants_generated:
    - variant_name: string        # Name of the new specialized variant
      variant_path: string        # Path to the generated SKILL.variant.md
      improvement_summary: string # Key optimizations made vs the base skill
  
  pattern_analysis:
    common_failures: array        # Frequently encountered edge cases in logs
    usage_trends: object          # Statistical breakdown of input types
  
  recommendations:
    - target: string              # Base skill or new variant
      suggestion: string          # Architectural improvement
```

## Implementation Notes

Skill Evolution uses a tiered analysis approach: first identifying statistical regularities in usage data, then generating divergent "Ralph" concepts for specialization, and finally grounding those concepts into executable schemas.

## When to Use

- Library has been used for 10+ skill executions
- Need specialized variants for specific domains or use cases
- Want to automate skill improvement based on real-world usage

## When NOT to Use

- Library is brand new with no usage data
- Skills are highly specialized and don't benefit from variants
- Time-constrained projects needing immediate results

## Capabilities

1. **Usage Pattern Analysis**: Scan logs for frequency, success rates, and modification patterns.
2. **Ralph Wiggum Chaos Generation**: Generate divergent ideas for missing capabilities.
3. **Pattern Validation**: Cross-reference chaos with real usage data.
4. **Automated Skill Generation**: Use drafting to create complete specialized variants.
5. **Self-Replicating Integration**: Update catalogs and indexes with new variants.

## Usage Examples

### Basic Usage

"Evolve the code-review skill based on last month's PR feedback logs."

### Advanced Usage

"Scan the entire library for cross-domain optimization opportunities and generate 10 new specialized variants."

## Configuration Options

- `variant_count`: Number of specialized versions to attempt.
- `log_depth`: Number of historical execution logs to analyze (default: 10).

## Performance Optimization

- **Pattern Indexing**: Pre-calculate statistical frequent items in logs.
- **Incremental Analysis**: Only process new logs since the last evolution cycle.

## Constraints

- NEVER break existing skill functionality
- ALWAYS maintain clear naming conventions for variants (e.g., base-name-domain)
- MUST include performance benchmarks vs the base skill
- SHOULD prioritize variants with highest usage impact

## Examples

### Example 1: Security Scan Variants

**Base Skill**: `security_scan`
**Usage Analysis**: High usage in Finance domain.
**Generated Variant**: `security_scan_finance` (PCI DSS focus).

## Error Handling

- **Invalid Input**: The skill will report specific missing parameters and request clarification.
- **Timeout**: Large-scale operations will be chunked to avoid process hangs.
- **Tool Failure**: Fallback mechanisms will attempt alternative logic paths.

## Integration Examples

### Pipeline Integration

This skill works well with `skill-drafting` for implementation and `skill-critiquing` for validation.

## Best Practices

- **Specific Context**: Provide as much specific context as possible for more accurate results.
- **Review Outputs**: Always manually verify critical recommendations before implementation.

## Troubleshooting

- **Empty Results**: Verify that the input identifiers are correct and accessible.
- **Slow Execution**: Reduce the `execution_depth` or narrowed the focus area.

## Monitoring and Metrics

- **Success Rate**: Monitored across automated cycles to ensure reliability.

## Dependencies

- **Standard Tools**: Requires base AgentSkills execution environment.
- **Python 3.10+**: For supporting scripts and automation logic.

## Version History

- **1.0.0**: Initial automated generation via Skill Flywheel Phase 7.

## License

MIT License - Part of the Open AgentSkills Library.
