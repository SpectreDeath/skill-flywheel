---
Domain: APPLICATION_SECURITY
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: skill-critiquing
---

## Description

The Skill Critiquing meta-skill provides a systematic framework for evaluating the logic, structure, and quality of AgentSkills. It is used to identify gaps, hallucinations, and inconsistencies during the development and audit phases.

## Purpose

Analyze AgentSkills against defined quality criteria to ensure they are logically sound, structurally compliant, and practically executable.

## Capabilities

1. **Logical Consistency Check**: Validate that inputs flow logically to outputs.
2. **Structural Validation**: Ensure all 18 mandatory sections are present and relevant.
3. **Hallucination Detection**: Identify irrelevant or out-of-context technical details.
4. **Actionable Feedback**: Provide specific recommendations for improvement.

## Usage Examples

### Basic Usage

"Critique the logic of the new security-scan skill."

### Advanced Usage

"Run a full audit on the APPLICATION_SECURITY domain and generate a health report."

## Input Format

### Skill Critique Request

```yaml
skill_critique_request:
  skill_path: string              # Path to the SKILL.md file to be critiqued
  focus_areas: array              # Specific areas to focus on (e.g., "workflow", "constraints", "testing")
  target_environment: string      # (Optional) Description of where the skill will be executed
  historical_performance: object  # (Optional) Success/failure history of the skill
  specific_questions: array       # (Optional) Specific questions for the critic
```

## Output Format

### Skill Critique Report

```yaml
skill_critique_report:
  skill_id: string                # Identification of the skill reviewed
  score:
    clarity: number               # 1-10 score for clarity
    testability: number           # 1-10 score for testability
    robustness: number            # 1-10 score for robustness
    overall: number               # Aggregate quality score
  
  issues:
    - category: string            # Issue category (e.g., "Ambiguity", "Safety", "Scope")
      description: string         # Detailed description of the problem
      severity: "low|medium|high" # Impact on execution
      line_reference: string      # (Optional) Line or section reference
  
  recommendations:
    - priority: "low|medium|high"
      action: string              # Concrete step to improve the skill
      expected_impact: string     # Benefit of the change
  
  refined_skill_preview: string   # (Optional) Markdown snippet showing the improved version
```

## Implementation Notes

The skill-critiquing engine uses semantic analysis to compare the purpose and capabilities against the defined workflow. It identifies logical leaps where a capability is claimed but not supported by the action steps.

## When to Use

- You've drafted a new skill and want feedback before using it
- A skill is producing inconsistent or unexpected results
- You want to improve an existing skill's structure or clarity
- You're auditing your skill library for quality

## When NOT to Use

- The skill is already proven and working reliably
- You're in a time-critical situation and need to use the skill as-is
- The skill is clearly well-structured and doesn't need refinement
- You're just starting to learn skill development (use drafting skill first)

## Capabilities

1. **Logical Consistency Check**: Validate that inputs flow logically to outputs.
2. **Structural Validation**: Ensure all 18 mandatory sections are present and relevant.
3. **Hallucination Detection**: Identify irrelevant or out-of-context technical details.
4. **Actionable Feedback**: Provide specific recommendations for improvement.

## Usage Examples

### Basic Usage

"Critique the logic of the new security-scan skill."

### Advanced Usage

"Run a full audit on the APPLICATION_SECURITY domain and generate a health report."

## Configuration Options

- `severity_threshold`: Minimum level of issue to report (low, medium, high).
- `focus_areas`: Specific skill components to prioritize (e.g., "schemas", "workflow").

## Performance Optimization

- **Cached Evaluation**: Store results of common pattern checks to speed up batch audits.
- **Parallel Processing**: Audit multiple skills simultaneously in large libraries.

## Constraints

- ALWAYS provide constructive, actionable feedback
- NEVER rewrite the entire skill unless absolutely necessary
- MUST focus on improving clarity and reliability
- SHOULD suggest splitting skills that are too broad
- MUST respect the original intent and purpose

## Examples

### Example 1: Vague Workflow Critique

**Input Skill**: "Analyze code quality" with steps like "Look at the code and see if it's good"

**Critique Output**: "Issue: Step is too vague. Suggestion: Replace with specific checks (linting, complexity, test coverage)."

### Example 2: Missing Constraints

**Input Skill**: "Deploy to production" without safety checks

**Critique Output**:

- **Issue**: No safety constraints or rollback procedures
- **Suggestion**: Add pre-deployment checks, rollback plan, and approval requirements
- **Improvement**: Include "NEVER deploy on Fridays" and "ALWAYS have monitoring ready"

**Usage**: `agent run SKILL.skill_critiquing.md --skill-file "SKILL.deploy.md" --constraints "safety_requirements"`

### Example 3: Overly Broad Scope

**Input Skill**: "Handle all customer support requests"

**Critique Output**:

- **Issue**: Too broad, covers many different types of requests
- **Suggestion**: Split into specific skills: "Handle billing inquiries", "Debug technical issues", "Process feature requests"
- **Improvement**: Each skill can be more focused and effective

**Usage**: `agent run SKILL.skill_critiquing.md --skill-file "SKILL.support.md" --scope "too_broad"`

### Example 4: Missing Testability

**Input Skill**: "Optimize application performance" with no measurable outcomes

**Critique Output**:

- **Issue**: No way to measure if optimization succeeded
- **Suggestion**: Add specific metrics (response time, memory usage, CPU utilization)
- **Improvement**: Include baseline measurements and target improvements

**Usage**: `agent run SKILL.skill_critiquing.md --skill-file "SKILL.performance.md" --testability "metrics_required"`

## Integration Examples

- **Flywheel Loop**: Integrated into Phase 2 of the flywheel for automated quality gating.
- **CI/CD**: Can be run as a pre-commit hook to validate skill structural integrity.

## Best Practices

- **Objective Criteria**: Always use the `audit_criteria.md` to ensure consistency.
- **Specific Feedback**: Avoid generic critiques; point to specific lines or sections.

## Troubleshooting

- **Schema Mismatches**: Ensure the target skill's YAML matches the expected sub-schema.
- **Deep Nesting**: Flatten complex logic if the critique report becomes too dense.

## Monitoring and Metrics

- **Critique Success Rate**: Tracked via user acceptance of generated suggestions.

## Dependencies

- **Standard Tools**: Requires base AgentSkills execution environment.
- **Audit Logic**: Depends on `audit_criteria.md` for grounding.

## Edge Cases and Troubleshooting

### Edge Case 1: Contradictory Constraints

**Problem**: Skill has conflicting requirements (e.g., "fast execution" vs "thorough analysis")
**Solution**: Prioritize constraints and suggest trade-offs or alternative approaches

### Edge Case 2: Missing Error Handling

**Problem**: Skill doesn't specify what happens when steps fail
**Solution**: Add explicit error handling and recovery procedures for each step

### Edge Case 3: Unclear Dependencies

**Problem**: Skill assumes tools or APIs without documenting them
**Solution**: Create explicit dependency list and version requirements

### Edge Case 4: Inconsistent Naming

**Problem**: Skill uses inconsistent terminology or naming conventions
**Solution**: Standardize terminology and create glossary if needed

## Quality Checklist

Use this checklist when critiquing skills:

- [ ] **Scope**: Is the skill focused and well-defined?
- [ ] **Clarity**: Are all steps unambiguous and clear?
- [ ] **Testability**: Can success be measured and validated?
- [ ] **Constraints**: Are safety and failure modes documented?
- [ ] **Composability**: Does it work well with other skills?
- [ ] **Examples**: Are there realistic usage examples?
- [ ] **Dependencies**: Are all required tools and APIs documented?
- [ ] **Edge Cases**: Are failure scenarios handled?

## Before/After Examples

### Before (Poor Quality)

```markdown
## Capabilities
1. Look at the code
2. Make it better
3. Test it
```

### After (Improved)

```markdown
## Capabilities
1. **Static Analysis**: Run ESLint and TypeScript compiler
   - Check for syntax errors and type violations
   - Validate against coding standards
2. **Performance Review**: Analyze algorithmic complexity
   - Identify O(n²) operations in critical paths
   - Check for memory leaks and excessive allocations
3. **Testing**: Execute test suite and validate coverage
   - Run unit tests with coverage report
   - Verify integration tests pass
   - Check for new test coverage requirements
```

## Assets

- critique_checklist.md: Standard checklist for skill review
- common_issues.md: List of frequent problems and solutions
- before_after_examples.md: Examples of skills before and after critique

## Error Handling

- **Invalid Input**: The skill will report specific missing parameters and request clarification.
- **Timeout**: Large-scale operations will be chunked to avoid process hangs.
- **Tool Failure**: Fallback mechanisms will attempt alternative logic paths.

## Version History

- **1.0.0**: Initial automated generation via Skill Flywheel Phase 7.

## License

MIT License - Part of the Open AgentSkills Library.
