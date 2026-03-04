---
Domain: APPLICATION_SECURITY
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: refactor-plan
---



## Purpose

Develop a comprehensive, safe refactoring strategy for improving code quality, maintainability, and performance. Used when preparing to make significant code changes while minimizing risk and ensuring system stability.


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