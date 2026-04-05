---
Domain: SPECIFICATION_ENGINEERING
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: specification-api-design
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
Comprehensive API specification design that creates living API contracts evolving with usage patterns, automatically generating OpenAPI specs from actual API traffic and usage analytics with real-time validation and version management.


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

- Designing RESTful APIs with comprehensive contract documentation
- Creating GraphQL schemas with detailed type definitions and resolvers
- Establishing API versioning and backward compatibility strategies
- Generating OpenAPI/Swagger specifications from existing APIs
- Designing API contracts that evolve with actual usage patterns
- When API documentation needs to stay synchronized with implementation

## When NOT to Use

- Simple internal APIs with minimal external consumers
- Prototypes or experimental APIs with rapidly changing contracts
- When existing API documentation is sufficient and stable
- Projects with very tight timelines requiring rapid API development
- APIs with minimal integration requirements

## Inputs

- **Required**: API endpoints and functionality requirements
- **Required**: Data models and business logic specifications
- **Optional**: Usage analytics and traffic patterns
- **Optional**: Consumer requirements and integration needs
- **Optional**: Security and authentication requirements
- **Optional**: Performance and scalability constraints

## Outputs

- **Primary**: Comprehensive API specification (OpenAPI/Swagger)
- **Secondary**: API contract documentation with examples
- **Tertiary**: Version management and migration strategies
- **Format**: Structured API specifications with interactive documentation and validation

## Capabilities

### 1. API Contract Analysis and Design
- **Analyze business requirements** and map to API endpoints
- **Design resource models** and URI structures
- **Define HTTP methods** and status codes
- **Establish data contracts** and schema definitions
- **Plan API versioning** and evolution strategies

### 2. Specification Generation and Documentation
- **Generate OpenAPI/Swagger specifications** with comprehensive details
- **Create interactive API documentation** with examples
- **Document authentication** and authorization mechanisms
- **Specify error handling** and response formats
- **Include rate limiting** and usage guidelines

### 3. Usage Pattern Analysis and Optimization
- **Analyze actual API usage** patterns and traffic
- **Identify performance bottlenecks** and optimization opportunities
- **Optimize API design** based on real-world usage
- **Validate specification accuracy** against implementation
- **Update specifications** based on usage insights

### 4. Version Management and Compatibility
- **Establish versioning strategy** (URL, header, parameter-based)
- **Design backward compatibility** and migration paths
- **Create deprecation policies** and communication plans
- **Manage API lifecycle** from design to retirement
- **Ensure smooth transitions** between API versions

### 5. Validation and Testing Integration
- **Validate API specifications** against implementation
- **Create automated tests** based on API contracts
- **Implement contract testing** for consumer-provider alignment
- **Set up continuous validation** in CI/CD pipelines
- **Monitor API compliance** and specification drift

### 6. Developer Experience and Integration
- **Create developer-friendly** API documentation
- **Provide SDK generation** and client libraries
- **Establish support channels** and community resources
- **Monitor developer feedback** and improve API design
- **Create best practices** and integration guidelines

## Constraints

- **NEVER** create API specifications that don't match actual implementation
- **ALWAYS** maintain backward compatibility when possible
- **MUST** ensure API specifications are testable and verifiable
- **SHOULD** follow RESTful principles and industry standards
- **MUST** maintain security and performance requirements

## Examples

### Example 1: E-commerce API Platform

**Input**: E-commerce business requirements, product catalog, order management, payment integration
**Output**:
- Comprehensive RESTful API specification for e-commerce platform
- OpenAPI documentation with interactive examples
- Version management strategy for API evolution
- Authentication and authorization specifications
- Performance and scalability guidelines

### Example 2: Financial Services API

**Input**: Banking services, transaction processing, compliance requirements, security standards
**Output**:
- Secure API specification with OAuth2 authentication
- Compliance documentation for financial regulations
- Rate limiting and security specifications
- Error handling and audit trail requirements
- Integration guidelines for third-party services

### Example 3: IoT Device Management API

**Input**: Device management, telemetry data, real-time communication, scalability requirements
**Output**:
- API specification for IoT device management
- WebSocket and REST API integration patterns
- Real-time data streaming specifications
- Device authentication and security protocols
- Scalability and performance optimization guidelines

## Edge Cases and Troubleshooting

### Edge Case 1: Legacy API Modernization
**Problem**: Modernizing legacy APIs with outdated specifications
**Solution**: Use API analysis tools to reverse-engineer existing APIs and generate modern specifications

### Edge Case 2: Microservices API Consistency
**Problem**: Maintaining consistent API design across multiple microservices
**Solution**: Establish API design standards and automated validation across all services

### Edge Case 3: High-Volume API Performance
**Problem**: Designing APIs for high-volume, low-latency requirements
**Solution**: Implement performance optimization strategies and comprehensive testing

### Edge Case 4: Third-Party API Integration
**Problem**: Integrating with external APIs with inconsistent specifications
**Solution**: Create adapter patterns and standardized integration approaches

## Quality Metrics

### API Specification Quality
- **Completeness**: All endpoints, parameters, and responses documented
- **Accuracy**: Specifications match actual API implementation
- **Clarity**: API contracts are clear and unambiguous
- **Consistency**: Uniform patterns and naming conventions
- **Testability**: Specifications can be validated and tested

### Developer Experience Quality
- **Documentation Quality**: Clear, comprehensive, and interactive documentation
- **Example Coverage**: Complete examples for all API operations
- **SDK Availability**: Client libraries and code generation support
- **Support Resources**: Community support and troubleshooting guides
- **Integration Ease**: Simple integration with existing systems

### API Performance Quality
- **Response Time**: API meets performance requirements and SLAs
- **Scalability**: API handles expected load and growth
- **Reliability**: High availability and fault tolerance
- **Security**: Proper authentication, authorization, and data protection
- **Monitoring**: Comprehensive observability and alerting

## Integration with Other Skills

### With Technical Specification Authoring
Ensure API specifications integrate seamlessly with overall technical architecture documentation.

### With Test Plan Specification
Create comprehensive test plans based on API specifications and contract testing requirements.

### With Architecture Decision Records
Document API design decisions and evolution in ADR format for architectural history.

## Usage Patterns

### API Design and Specification Workflow
```
1. Analyze business requirements and define API scope
2. Design API contracts and data models
3. Generate comprehensive API specifications
4. Validate specifications against implementation
5. Create interactive documentation and examples
6. Establish version management and testing processes
```

### API Evolution and Maintenance
```
1. Monitor API usage patterns and performance
2. Identify optimization opportunities and improvements
3. Update specifications based on real-world usage
4. Manage version transitions and backward compatibility
5. Maintain documentation and developer resources
```

## Success Stories

### API Developer Adoption
A SaaS company increased API developer adoption by 70% through comprehensive API specifications and interactive documentation that made integration simple and straightforward.

### Microservices Consistency
An enterprise improved microservices API consistency by 80% by implementing standardized API specification practices across all development teams.

### Third-Party Integration Success
A financial services platform reduced integration time for third-party developers by 60% through well-designed API specifications and comprehensive documentation.

## When API Specification Design Works Best

- **Public APIs** with external consumers and integration needs
- **Microservices architectures** requiring consistent API patterns
- **Enterprise applications** with multiple system integrations
- **Regulated industries** needing comprehensive API documentation
- **High-traffic systems** requiring performance optimization

## When to Avoid Complex API Specifications

- **Internal APIs** with minimal external consumers
- **Prototypes** or experimental APIs with rapidly changing contracts
- **Simple integrations** with straightforward requirements
- **Projects with tight timelines** requiring rapid development
- **When existing specifications** are sufficient and stable

## Future API Specification Trends

### AI-Powered API Design
Using AI to analyze usage patterns and automatically optimize API design for better performance and developer experience.

### Real-time Specification Updates
Integrating with API gateways and monitoring tools to automatically update specifications based on actual usage.

### Contract-First Development
Emphasizing API contract definition before implementation to ensure consistency and consumer needs.

### API Governance Automation
Automated tools for API specification validation, compliance checking, and governance enforcement.

## API Specification Design Mindset

Remember: Effective API specification design requires balancing developer experience, performance requirements, and maintainability while ensuring specifications remain accurate and useful throughout the API lifecycle. Focus on creating living contracts that evolve with usage patterns and provide clear guidance for both API providers and consumers while maintaining backward compatibility and performance standards.

This skill provides comprehensive API specification design guidance for professional software development.


## Description

The Specification Api Design skill provides an automated workflow to address comprehensive api specification design that creates living api contracts evolving with usage patterns, automatically generating openapi specs from actual api traffic and usage analytics with real-time validation and version management.. It is designed to be highly modular and integrates seamlessly into larger agentic pipelines.

## Usage Examples

### Basic Usage
'Use specification-api-design to analyze my current project context.'

### Advanced Usage
'Run specification-api-design with focus on high-priority optimization targets.'

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