---
Domain: APPLICATION_SECURITY
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: test-survey
---



## Purpose

Comprehensively assess test coverage, quality, and effectiveness in a codebase. Used to identify testing gaps, improve test quality, and ensure adequate coverage before major releases or refactoring efforts.


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

- Before major releases to validate test coverage
- During codebase onboarding to understand testing strategy
- When refactoring to ensure test safety nets are adequate
- During quality improvement initiatives
- When evaluating testing practices for new team members

## When NOT to Use

- When you only need to run existing tests (use test runner instead)
- When time is severely constrained and only specific test files need checking
- When the codebase has no tests at all (start with test strategy skill)
- When you need to write new tests (use test writing skill instead)

## Inputs

- **Required**: Repository path to analyze
- **Optional**: Test frameworks to focus on (Jest, pytest, JUnit, etc.)
- **Optional**: Coverage threshold requirements (percentage targets)
- **Optional**: Code areas to prioritize (new features, critical paths, etc.)
- **Assumptions**: Test files follow standard naming conventions, test runner available

## Outputs

- **Primary**: Test coverage and quality analysis report (JSON format)
- **Secondary**: Test effectiveness assessment with recommendations
- **Format**: Markdown report with coverage metrics, quality scores, and improvement suggestions

## Capabilities

1. **Test Infrastructure Discovery**
   - Identify test frameworks and runners in use (Jest, pytest, Mocha, etc.)
   - Locate test directories and file naming patterns
   - Analyze test configuration files and settings
   - Document test data and fixture management

2. **Coverage Analysis**
   - Run coverage tools to measure line, branch, and function coverage
   - Identify untested code paths and critical areas
   - Map coverage by module, feature, and complexity
   - Compare coverage against defined thresholds

3. **Test Quality Assessment**
   - Evaluate test naming conventions and clarity
   - Check for proper setup/teardown patterns
   - Assess test independence and isolation
   - Review assertion quality and specificity

4. **Test Effectiveness Review**
   - Analyze test categories (unit, integration, e2e) and balance
   - Check for meaningful test scenarios and edge cases
   - Evaluate test data quality and realism
   - Assess performance and reliability of test suite

5. **Test Maintenance Analysis**
   - Identify flaky or unreliable tests
   - Check for test duplication and redundancy
   - Review test execution time and performance
   - Assess test documentation and maintainability

6. **Report Generation and Recommendations**
   - Generate coverage heatmaps and trend analysis
   - Provide specific recommendations for improvement
   - Create prioritized action plan for test enhancement
   - Suggest testing strategy improvements

## Constraints

- DO NOT modify existing test files during analysis
- MUST respect test isolation and not interfere with test execution
- SHOULD focus on actionable, measurable improvements
- MUST consider project-specific testing requirements and constraints
- DO NOT assume all code needs 100% coverage (context matters)
- SHOULD balance coverage with test quality and maintainability

## Examples

### Example 1: Pre-Release Test Assessment

**Input**: Repository path with coverage threshold = "80%", focus areas = "new features"
**Output**: Pre-release test readiness report
**Focus**: Coverage gaps in recent changes, test quality for critical paths
**Notes**: Emphasize areas that need attention before release

### Example 2: Testing Strategy Evaluation

**Input**: Repository with test frameworks = "all", coverage threshold = "70%"
**Output**: Comprehensive testing strategy assessment
**Focus**: Overall test quality, framework effectiveness, improvement opportunities
**Notes**: Provide strategic recommendations for testing approach

### Example 3: Critical Path Testing Review

**Input**: Repository with focus areas = "critical business logic, security features"
**Output**: Critical path test coverage report
**Focus**: Test adequacy for high-risk areas, edge case coverage
**Notes**: Prioritize testing of mission-critical functionality

## Assets

- coverage_analyzer.py: Tool for measuring and analyzing test coverage
- test_quality_checker.py: Script for assessing test code quality
- framework_detector.py: Script to identify testing frameworks in use
- test_metrics.py: Tool for collecting test suite performance metrics
- report_template.md: Standard test assessment report format
- best_practices.json: Testing best practices and guidelines


## Description

The Test Survey skill provides an automated workflow to address comprehensively assess test coverage, quality, and effectiveness in a codebase. used to identify testing gaps, improve test quality, and ensure adequate coverage before major releases or refactoring efforts.. It is designed to be highly modular and integrates seamlessly into larger agentic pipelines.

## Usage Examples

### Basic Usage
'Use test-survey to analyze my current project context.'

### Advanced Usage
'Run test-survey with focus on high-priority optimization targets.'

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