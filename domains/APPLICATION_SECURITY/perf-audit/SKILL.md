---
Domain: APPLICATION_SECURITY
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: perf-audit
---



## Purpose

Identify and analyze performance bottlenecks, inefficiencies, and optimization opportunities in a codebase. Used to improve application responsiveness, reduce resource consumption, and enhance user experience.


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

- Before major releases to ensure optimal performance
- When users report slow application response times
- During capacity planning for scaling initiatives
- When investigating high resource usage (CPU, memory, network)
- Before implementing performance-critical features
- During regular codebase health assessments

## When NOT to Use

- When immediate performance fixes are needed (use targeted optimization instead)
- When the application is already meeting performance requirements
- When time is severely constrained and only specific performance issues matter
- When you need real-time performance monitoring (use APM tools instead)

## Inputs

- **Required**: Repository path and target performance metrics
- **Optional**: Performance baselines or benchmarks to compare against
- **Optional**: Specific areas of concern (database queries, API calls, rendering, etc.)
- **Optional**: Load testing scenarios or expected traffic patterns
- **Assumptions**: Access to profiling tools, test environment for benchmarking

## Outputs

- **Primary**: Performance audit report (JSON format with bottlenecks and recommendations)
- **Secondary**: Performance baseline measurements and trend analysis
- **Format**: Markdown report with prioritized issues, optimization strategies, and implementation guidance

## Capabilities

1. **Performance Baseline Establishment**
   - Measure current application performance metrics (response times, throughput, resource usage)
   - Establish baseline benchmarks for key user journeys
   - Document current infrastructure and deployment configuration
   - Identify performance-critical code paths and components

2. **Code-Level Performance Analysis**
   - Analyze algorithmic complexity of critical functions
   - Identify inefficient loops, nested iterations, and redundant calculations
   - Check for memory leaks, excessive allocations, and garbage collection issues
   - Review data structures and their performance characteristics

3. **Database and Storage Performance Review**
   - Analyze query performance and identify slow queries
   - Check for N+1 query problems and missing indexes
   - Review database connection pooling and transaction management
   - Assess caching strategies and cache hit rates

4. **Network and API Performance Assessment**
   - Identify API call bottlenecks and excessive round trips
   - Check for inefficient data transfer (over-fetching, under-fetching)
   - Review request/response sizes and compression strategies
   - Analyze third-party service dependencies and their impact

5. **Frontend Performance Analysis** (if applicable)
   - Review bundle sizes and code splitting strategies
   - Check for render-blocking resources and inefficient rendering patterns
   - Analyze image optimization and asset loading
   - Review client-side caching and storage usage

6. **Infrastructure and Configuration Review**
   - Assess server configuration and resource allocation
   - Check for configuration issues affecting performance
   - Review load balancing and scaling strategies
   - Analyze monitoring and alerting setup

7. **Optimization Strategy Development**
   - Prioritize performance issues by impact and effort required
   - Design specific optimization approaches for each bottleneck
   - Estimate potential performance improvements
   - Create implementation roadmap with validation criteria

8. **Report Generation and Recommendations**
   - Document all performance findings with specific metrics
   - Provide actionable optimization recommendations
   - Include implementation guidance and best practices
   - Create performance monitoring and regression prevention strategies

## Constraints

- MUST establish baselines before making optimizations
- SHOULD focus on high-impact, low-effort improvements first
- MUST consider trade-offs between performance, maintainability, and functionality
- SHOULD validate optimizations with realistic test scenarios
- MUST document performance assumptions and dependencies
- SHOULD plan for ongoing performance monitoring and regression testing

## Examples

### Example 1: Web Application Performance Review

**Input**: Repository path with target metrics = "page load time < 3s", areas of concern = "API calls, rendering"
**Output**: Comprehensive web performance audit report
**Focus**: Frontend optimization, API efficiency, database query performance
**Notes**: Emphasize user-facing performance metrics and Core Web Vitals

### Example 2: API Performance Optimization

**Input**: Repository with target metrics = "API response time < 200ms", areas of concern = "database queries, serialization"
**Output**: API-specific performance analysis and recommendations
**Focus**: Query optimization, caching strategies, response serialization
**Notes**: Focus on backend performance and scalability

### Example 3: Mobile App Performance Audit

**Input**: Repository with target metrics = "app startup < 2s", areas of concern = "initialization, rendering"
**Output**: Mobile-specific performance assessment
**Focus**: App startup time, memory usage, battery impact, network efficiency
**Notes**: Consider mobile-specific constraints and user experience patterns

## Assets

- performance_profiler.py: Tool for measuring and analyzing performance metrics
- code_analyzer.py: Script for identifying performance anti-patterns in code
- query_analyzer.py: Tool for database query performance analysis
- bundle_analyzer.py: Script for frontend bundle size and composition analysis
- benchmark_runner.py: Tool for establishing performance baselines
- optimization_patterns.py: Library of proven performance optimization techniques
- monitoring_setup.py: Script for performance monitoring and alerting configuration


## Description

The Perf Audit skill provides an automated workflow to address identify and analyze performance bottlenecks, inefficiencies, and optimization opportunities in a codebase. used to improve application responsiveness, reduce resource consumption, and enhance user experience.. It is designed to be highly modular and integrates seamlessly into larger agentic pipelines.

## Usage Examples

### Basic Usage
'Use perf-audit to analyze my current project context.'

### Advanced Usage
'Run perf-audit with focus on high-priority optimization targets.'

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