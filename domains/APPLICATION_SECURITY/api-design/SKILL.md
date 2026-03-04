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

### Deployment Configuration Request

```yaml
deployment_configuration_request:
  application_id: string          # Unique application identifier
  application_name: string        # Application name
  target_stores: array            # Target app stores (App Store, Google Play, etc.)
  
  platform_configurations:
    ios:
      bundle_identifier: string   # iOS bundle identifier
      team_id: string             # Apple Developer Team ID
      provisioning_profile: string # Provisioning profile name
      certificate_id: string      # Certificate identifier
    
    android:
      package_name: string        # Android package name
      keystore_file: string       # Keystore file path
      keystore_password: string   # Keystore password
      key_alias: string           # Key alias
      key_password: string        # Key password
  
  compliance_requirements:
    privacy_policy_url: string    # Privacy policy URL
    terms_of_service_url: string  # Terms of service URL
    data_usage_disclosure: object # Data usage disclosure information
    age_rating: string            # App age rating
    content_descriptors: array    # Content descriptors
  
  deployment_strategy:
    rollout_strategy: "immediate|staged|phased"
    rollout_percentage: number    # Initial rollout percentage
    monitoring_enabled: boolean   # Whether monitoring is enabled
    rollback_enabled: boolean     # Whether automatic rollback is enabled
```

### App Store Metadata Schema

```yaml
app_store_metadata:
  app_information:
    app_name: string              # App name
    subtitle: string              # App subtitle (iOS only)
    app_description: string       # App description
    keywords: array               # App keywords
    support_url: string           # Support URL
    marketing_url: string         # Marketing URL
  
  visual_assets:
    app_icon: string              # App icon file path
    screenshots: array            # Screenshots for different devices
    app_preview: string           # App preview video (iOS only)
    feature_graphic: string       # Feature graphic (Android only)
  
  technical_information:
    bundle_size: string           # App bundle size
    supported_devices: array      # Supported device types
    required_permissions: array   # Required app permissions
    background_modes: array       # Background modes (iOS only)
  
  compliance_information:
    privacy_policy: string        # Privacy policy content
    terms_of_service: string      # Terms of service content
    data_collection_purposes: array # Data collection purposes
    third_party_integrations: array # Third-party integrations
```

## Output Format

### Deployment Report

```yaml
deployment_report:
  application_id: string
  deployment_timestamp: timestamp
  target_stores: array
  overall_status: "success|failed|partial"
  
  store_specific_reports:
    - store_name: "Apple App Store"
      status: "submitted|approved|rejected|in_review"
      submission_id: string
      review_status: string
      estimated_review_time: string
      compliance_status: "compliant|non_compliant"
      compliance_issues: array
      next_steps: array
    
    - store_name: "Google Play Store"
      status: "published|pending|rejected"
      track: "internal|alpha|beta|production"
      rollout_percentage: number
      compliance_status: "compliant|non_compliant"
      compliance_issues: array
      next_steps: array
  
  build_information:
    build_number: string
    build_time: string
    build_artifacts: array
    code_signing_status: "valid|invalid"
    bundle_size: string
  
  compliance_summary:
    total_checks: number
    passed_checks: number
    failed_checks: number
    compliance_percentage: number
    critical_issues: array
    warnings: array
  
  deployment_metrics:
    deployment_time: string
    success_rate: number
    rollback_count: number
    user_impact: string
```

### Compliance Validation Report

```yaml
compliance_validation_report:
  validation_timestamp: timestamp
  validation_scope: "full|partial|targeted"
  
  app_store_guidelines:
    apple_app_store:
      total_guidelines: 100
      validated_guidelines: 95
      compliant_guidelines: 92
      non_compliant_guidelines: 3
      critical_violations: array
      warnings: array
    
    google_play_store:
      total_policies: 50
      validated_policies: 50
      compliant_policies: 50
      non_compliant_policies: 0
      critical_violations: array
      warnings: array
  
  technical_requirements:
    ios_requirements:
      app_size: "compliant|non_compliant"
      launch_screen: "compliant|non_compliant"
      app_icons: "compliant|non_compliant"
      bitcode: "compliant|non_compliant"
    
    android_requirements:
      app_bundle: "compliant|non_compliant"
      target_sdk: "compliant|non_compliant"
      permissions: "compliant|non_compliant"
      app_size: "compliant|non_compliant"
  
  security_compliance:
    data_encryption: "compliant|non_compliant"
    secure_communication: "compliant|non_compliant"
    authentication_requirements: "compliant|non_compliant"
    privacy_compliance: "compliant|non_compliant"
  
  recommendations:
    - priority: "high"
      category: "compliance"
      recommendation: string
      impact: string
      effort: string
    
    - priority: "medium"
      category: "performance"
      recommendation: string
      impact: string
      effort: string
```

## Implementation Notes

*[Content for Implementation Notes section to be added based on the specific skill requirements]*
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