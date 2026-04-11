---
Domain: APPLICATION_SECURITY
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: skill-drafting
---

## Description

The Skill Drafting meta-skill provides an automated workflow to transform high-level intent into structured, testable `SKILL.md` files. It ensures that new skills follow the project's 18-section template and maintain logical consistency.

## Purpose

Automate the scaffolding of new AgentSkills by extracting core elements from natural language descriptions and organizing them into standard formats.

## Input Format

### Skill Drafting Request

```yaml
skill_draft_request:
  intent: string                  # Natural language description of the new skill
  domain: string                  # Target domain (e.g., "DEVOPS", "SECURITY")
  constraints: array              # (Optional) Known limitations or rules
  environment: object             # (Optional) Tooling and directory context
  desired_examples: array         # (Optional) Logic for specific usage examples
```

## Output Format

### Skill Draft Report

```yaml
skill_draft_report:
  skill_name: string              # Generated name for the skill
  structured_content: string      # Full Markdown content of the new SKILL.md
  questions:
    - section: string             # Section needing clarification
      question: string            # Clarifying question for the user
  
  compliance_check:
    sections_present: boolean     # All 18 sections generated
    logic_score: number           # Initial estimate of workflow soundness
```

## Implementation Notes

Skill Drafting leverages structural templates and domain-specific knowledge bases to ensure that the generated workflows are both theoretically sound and practically executable by agents.

## When to Use

- You have a rough idea for a new skill but need to formalize it
- You want to ensure your skill follows established patterns
- You're building multiple skills and want consistency
- You need to capture tribal knowledge as reusable workflows

## When NOT to Use

- The task is too trivial for a full skill specification
- The workflow is highly variable and can't be standardized
- You already have a well-defined skill template to follow

## Capabilities

1. **Extract Core Elements**: Identify purpose, use cases, inputs, and outputs.
2. **Identify Missing Information**: Spot unclear boundaries or ambiguous success criteria.
3. **Structure the Skill**: Organize information into standard sections.
4. **Validate Against Best Practices**: Ensure testability and composability.
5. **Generate Output**: Create the complete drafted `SKILL.md`.

## Usage Examples

### Basic Usage

"Draft a skill for analyzing Python complex numbers."

### Advanced Usage

"Generate a suite of 5 skills for advanced Kubernetes troubleshooting with specific security constraints."

## Configuration Options

- `template_version`: Version of the SKILL.md template to use.
- `domain_defaults`: Pre-configured settings for specific domains (e.g., "DEVOPS").

## Performance Optimization

- **Template Fragment Caching**: Reuse common section fragments across multiple drafts.
- **Parallel Generation**: Process multiple drafting requests in parallel threads.

## Constraints

- NEVER assume tools or capabilities that aren't explicitly mentioned
- ALWAYS include "when NOT to use" guidance
- MUST keep steps finite and bounded
- SHOULD suggest splitting overly broad skills into smaller units

## Examples

### Example 1: Code Review Skill

**Input**: "I want a skill that can review pull requests for common issues."
**Output**: Complete `SKILL.code_review.md` with structured workflow and security focus.

## Error Handling

- **Invalid Input**: The skill will report specific missing parameters and request clarification.
- **Timeout**: Large-scale operations will be chunked to avoid process hangs.
- **Tool Failure**: Fallback mechanisms will attempt alternative logic paths.

## Integration Examples

### Pipeline Integration

This skill works well with `skill-critiquing` for automated refinement post-drafting.

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
