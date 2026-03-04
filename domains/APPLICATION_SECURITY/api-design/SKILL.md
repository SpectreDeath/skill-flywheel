---
Domain: APPLICATION_SECURITY
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: api-design
---



## Purpose

Evaluate and improve the design, usability, and maintainability of APIs (REST, GraphQL, gRPC, etc.). Used to ensure APIs follow best practices, provide good developer experience, and maintain long-term compatibility.


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

- Before releasing new APIs to production
- When reviewing existing APIs for improvements or standardization
- During API versioning and migration planning
- When onboarding new developers to understand API patterns
- Before implementing breaking changes to existing APIs
- During API documentation and specification reviews

## When NOT to Use

- When you need to implement specific API endpoints (use implementation skills instead)
- When time is severely constrained and only basic functionality matters
- When the API is already following established, proven patterns
- When you need real-time API testing or monitoring (use testing tools instead)

## Inputs

- **Required**: API specifications, documentation, or codebase with API endpoints
- **Optional**: API type (REST, GraphQL, gRPC, WebSocket, etc.)
- **Optional**: Target audience (internal developers, external partners, public)
- **Optional**: Performance and scalability requirements
- **Assumptions**: Access to API documentation, examples, and usage patterns

## Outputs

- **Primary**: API design assessment report (JSON format with issues and recommendations)
- **Secondary**: API improvement roadmap with prioritized changes
- **Format**: Markdown report with design patterns, best practice violations, and enhancement suggestions

## Capabilities

1. **API Specification Analysis**
   - Review API documentation completeness and clarity
   - Analyze endpoint naming conventions and URL structure
   - Check for consistent data formats and response patterns
   - Assess error handling and status code usage

2. **Design Pattern Evaluation**
   - Evaluate adherence to REST principles (if applicable)
   - Check for proper resource modeling and relationships
   - Assess query parameter design and filtering capabilities
   - Review pagination, sorting, and data retrieval patterns

3. **Developer Experience Assessment**
   - Analyze API discoverability and self-documentation
   - Check for comprehensive examples and use cases
   - Evaluate authentication and authorization patterns
   - Assess SDK and client library availability

4. **Performance and Scalability Review**
   - Identify potential performance bottlenecks in API design
   - Check for efficient data transfer and payload optimization
   - Assess caching strategies and rate limiting
   - Review versioning and backward compatibility approaches

5. **Security and Compliance Analysis**
   - Evaluate authentication and authorization mechanisms
   - Check for proper input validation and sanitization
   - Assess data privacy and compliance requirements
   - Review API security best practices implementation

6. **Maintainability and Evolution Planning**
   - Analyze API versioning strategy and migration paths
   - Check for deprecation policies and communication
   - Assess testing and monitoring coverage
   - Review documentation maintenance processes

7. **API Improvement Strategy Development**
   - Prioritize design improvements by impact and effort
   - Design migration strategies for breaking changes
   - Create standardization guidelines for future APIs
   - Plan for API governance and review processes

8. **Report Generation and Recommendations**
   - Document design issues with specific examples and impact
   - Provide actionable improvement recommendations
   - Include implementation guidance and best practices
   - Create API design guidelines and standards

## Constraints

- MUST maintain backward compatibility unless explicitly planning breaking changes
- SHOULD follow established API design principles and industry standards
- MUST consider developer experience and ease of use
- SHOULD plan for API evolution and versioning
- MUST document all design decisions and rationale
- SHOULD establish API governance and review processes

## Examples

### Example 1: REST API Design Review

**Input**: REST API specifications with target audience = "external developers", performance requirements = "high throughput"
**Output**: REST API design assessment with optimization recommendations
**Focus**: Resource modeling, HTTP methods, status codes, response formats
**Notes**: Emphasize RESTful principles and developer experience

### Example 2: GraphQL Schema Review

**Input**: GraphQL schema with target audience = "internal teams", performance requirements = "low latency"
**Output**: GraphQL schema optimization report
**Focus**: Query complexity, resolver patterns, data fetching efficiency
**Notes**: Focus on query performance and schema design best practices

### Example 3: API Standardization Assessment

**Input**: Multiple APIs with goal = "standardization", target audience = "all developers"
**Output**: API standardization roadmap and guidelines
**Focus**: Consistency across APIs, common patterns, governance
**Notes**: Establish organization-wide API design standards

## Assets

- api_analyzer.py: Tool for analyzing API specifications and patterns
- design_checker.py: Script for evaluating API design against best practices
- performance_assessor.py: Tool for identifying API performance issues
- security_reviewer.py: Script for API security assessment
- documentation_reviewer.py: Tool for evaluating API documentation quality
- standardization_guide.py: Template for API design standards and guidelines
- migration_planner.py: Tool for planning API versioning and migration strategies


## Description

The Api Design skill provides an automated workflow to address evaluate and improve the design, usability, and maintainability of apis (rest, graphql, grpc, etc.). used to ensure apis follow best practices, provide good developer experience, and maintain long-term compatibility.. It is designed to be highly modular and integrates seamlessly into larger agentic pipelines.

## Usage Examples

### Basic Usage
'Use api-design to analyze my current project context.'

### Advanced Usage
'Run api-design with focus on high-priority optimization targets.'

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