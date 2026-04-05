---
Domain: APPLICATION_SECURITY
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: refactor-plan
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




## Purpose

Develop a comprehensive, safe refactoring strategy for improving code quality, maintainability, and performance. Used when preparing to make significant code changes while minimizing risk and ensuring system stability.


## Input Format

```yaml
request:
  action: string
  parameters: object
```

## Output Format

```yaml
response:
  status: string
  result: object
  errors: array
```

## Implementation Notes

To be provided dynamically during execution.
## When to Use

- Before undertaking major code restructuring or architectural changes
- When code quality issues are impacting development velocity
- When preparing to add significant new features to legacy code
- During technical debt reduction initiatives
- When performance optimization requires code changes
- Before migrating to new frameworks or technologies

## When NOT to Use

- For minor code improvements or simple bug fixes
- When immediate fixes are needed and there's no time for planning
- When the codebase is already well-structured and maintainable
- When refactoring would disrupt critical business operations
- When the team lacks the expertise to execute the planned changes

## Inputs

- **Required**: Repository path and specific code areas to refactor
- **Optional**: Refactoring goals (performance, readability, maintainability, testability)
- **Optional**: Constraints (time limits, compatibility requirements, team expertise)
- **Optional**: Risk tolerance level (conservative, moderate, aggressive)
- **Assumptions**: Existing tests are in place, team has refactoring experience

## Outputs

- **Primary**: Refactoring plan document (JSON format with phases and steps)
- **Secondary**: Risk assessment and mitigation strategy
- **Format**: Markdown plan with timeline, dependencies, and validation criteria

## Capabilities

1. **Current State Analysis**
   - Analyze code complexity metrics (cyclomatic complexity, nesting depth)
   - Identify code smells and anti-patterns
   - Map dependencies and coupling between components
   - Assess test coverage for targeted refactoring areas

2. **Refactoring Goals Definition**
   - Define specific, measurable improvement targets
   - Prioritize refactoring objectives by business value and risk
   - Establish success criteria and validation methods
   - Identify non-functional requirements (performance, security, etc.)

3. **Risk Assessment and Mitigation**
   - Identify potential breaking changes and their impact
   - Assess dependencies and integration points
   - Evaluate rollback strategies and safety nets
   - Plan for regression testing and validation

4. **Refactoring Strategy Development**
   - Design step-by-step refactoring approach
   - Identify safe refactoring patterns to apply
   - Plan incremental changes to minimize disruption
   - Define rollback points and validation checkpoints

5. **Implementation Planning**
   - Break down refactoring into manageable phases
   - Sequence changes to maintain system functionality
   - Identify required tooling and automation needs
   - Plan team coordination and communication

6. **Validation and Testing Strategy**
   - Define comprehensive testing approach for each phase
   - Plan performance benchmarks and regression tests
   - Establish monitoring and alerting for production changes
   - Create rollback procedures and emergency response plans

7. **Timeline and Resource Planning**
   - Estimate effort and duration for each refactoring phase
   - Identify required team skills and training needs
   - Plan for parallel development and feature freeze periods
   - Create communication and status reporting structure

## Constraints

- MUST maintain backward compatibility unless explicitly breaking
- SHOULD prioritize safety over speed of implementation
- MUST have comprehensive test coverage before starting
- SHOULD implement changes incrementally with validation points
- MUST document all changes and rationale
- SHOULD consider impact on dependent systems and teams

## Examples

### Example 1: Legacy System Modernization

**Input**: Repository path with refactoring goals = "performance + maintainability", risk tolerance = "conservative"
**Output**: Multi-phase modernization plan with safety checkpoints
**Focus**: Incremental improvements, comprehensive testing, rollback strategies
**Notes**: Emphasize maintaining system availability during refactoring

### Example 2: Code Quality Improvement

**Input**: Repository with specific modules = "authentication, data access", goals = "readability + testability"
**Output**: Targeted refactoring plan for specified modules
**Focus**: Extracting business logic, improving separation of concerns, adding tests
**Notes**: Focus on high-impact areas with clear quality issues

### Example 3: Performance Optimization Refactoring

**Input**: Repository with performance bottlenecks identified, goals = "performance", constraints = "no breaking changes"
**Output**: Performance-focused refactoring strategy
**Focus**: Algorithm optimization, caching strategies, database query improvements
**Notes**: Maintain functionality while improving efficiency

## Assets

- complexity_analyzer.py: Tool for measuring code complexity metrics
- code_smell_detector.py: Script for identifying code smells and anti-patterns
- dependency_mapper.py: Tool for analyzing code dependencies and coupling
- refactoring_patterns.py: Library of safe refactoring patterns and techniques
- risk_assessment.py: Script for evaluating refactoring risks and impacts
- implementation_planner.py: Tool for creating phased implementation plans
- validation_framework.py: Template for comprehensive testing strategies


## Description

The Refactor Plan skill provides an automated workflow to address develop a comprehensive, safe refactoring strategy for improving code quality, maintainability, and performance. used when preparing to make significant code changes while minimizing risk and ensuring system stability.. It is designed to be highly modular and integrates seamlessly into larger agentic pipelines.

## Usage Examples

### Basic Usage
'Use refactor-plan to analyze my current project context.'

### Advanced Usage
'Run refactor-plan with focus on high-priority optimization targets.'

## Configuration Options

- `execution_depth`: Control the thoroughness of the analysis (default: standard).
- `report_format`: Choose between markdown, json, or console output.
- `verbose`: Enable detailed logging for debugging purposes.

## Error Handling

- **Invalid Input**: The skill will report specific missing parameters and request clarification.
- **Timeout**: Large-scale operations will be chunked to avoid process hangs.
- **Tool Failure**: Fallback mechanisms will attempt alternative logic paths.

## Performance Optimization

- **Caching**: Results are cached when applicable to reduce redundant computations.
- **Lazy Loading**: Supporting assets are only loaded when strictly necessary.
- **Parallelization**: Multi-target scans are executed in parallel where supported.

## Integration Examples

### Pipeline Integration
This skill is a core component of `FLOW.full_cycle.yaml` and works well with `skill-drafting` for automated refinement.

## Best Practices

- **Specific Context**: Provide as much specific context as possible for more accurate results.
- **Regular Audits**: Use this skill as part of a recurring CI/CD quality gate.
- **Review Outputs**: Always manually verify critical recommendations before implementation.

## Troubleshooting

- **Empty Results**: Verify that the input identifiers are correct and accessible.
- **Slow Execution**: Reduce the `execution_depth` or narrowed the focus area.
- **Permission Errors**: Ensure the agent has read/write access to the target directories.

## Monitoring and Metrics

- **Execution Time**: Tracked per run to identify bottlenecks.
- **Success Rate**: Monitored across automated cycles to ensure reliability.
- **Token Usage**: Optimized to minimize context window consumption.

## Dependencies

- **Standard Tools**: Requires base AgentSkills execution environment.
- **Python 3.10+**: For supporting scripts and automation logic.

## Version History

- **1.0.0**: Initial automated generation via Skill Flywheel Phase 7.

## License

MIT License - Part of the Open AgentSkills Library.