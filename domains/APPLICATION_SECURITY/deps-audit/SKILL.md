---
Domain: APPLICATION_SECURITY
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: deps-audit
---



## Purpose

Analyze and assess the health, security, and maintenance status of project dependencies. Used to identify outdated packages, security vulnerabilities, license compliance issues, and potential upgrade opportunities.


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

- Before major releases to ensure dependency health
- During security audits to identify vulnerable packages
- When onboarding to understand project dependencies
- During refactoring to evaluate dependency impact
- For compliance and licensing reviews
- When planning dependency upgrade strategies

## When NOT to Use

- When you need to install or update specific dependencies (use package manager instead)
- When time is severely constrained and only critical vulnerabilities matter
- When the project has no external dependencies
- When you need real-time dependency resolution (use build tools instead)

## Inputs

- **Required**: Repository path with package management files
- **Optional**: Package managers to focus on (npm, pip, cargo, maven, etc.)
- **Optional**: Security severity threshold (low, medium, high, critical)
- **Optional**: License compliance requirements
- **Optional**: Upgrade strategy preferences (conservative, aggressive, LTS)
- **Assumptions**: Package management files exist, network access for vulnerability databases

## Outputs

- **Primary**: Dependency audit report (JSON format with detailed findings)
- **Secondary**: Risk assessment and upgrade recommendations
- **Format**: Markdown report with categorized issues, upgrade paths, and action items

## Capabilities

1. **Dependency Inventory**
   - Scan package.json, requirements.txt, Cargo.toml, pom.xml, etc.
   - Identify direct and transitive dependencies
   - Map dependency relationships and version constraints
   - Document development vs production dependencies

2. **Security Vulnerability Analysis**
   - Check dependencies against known vulnerability databases (CVE, NVD)
   - Identify packages with active security issues
   - Assess severity and potential impact of vulnerabilities
   - Cross-reference with project usage patterns

3. **Version Health Assessment**
   - Compare current versions with latest available
   - Identify outdated packages and their update history
   - Check for packages with no recent updates (abandoned)
   - Assess version constraint flexibility

4. **License Compliance Review**
   - Analyze licenses of all dependencies
   - Identify potential license conflicts or incompatibilities
   - Flag licenses requiring special attention (GPL, AGPL, etc.)
   - Assess compliance with organizational policies

5. **Maintenance and Quality Evaluation**
   - Check dependency maintenance status (active, abandoned, deprecated)
   - Assess dependency popularity and community support
   - Identify dependencies with known issues or poor quality
   - Evaluate dependency size and bundle impact

6. **Upgrade Path Analysis**
   - Identify safe upgrade paths for outdated packages
   - Assess breaking changes and migration complexity
   - Prioritize upgrades by risk and benefit
   - Generate upgrade recommendations with timelines

7. **Report Generation and Recommendations**
   - Categorize findings by severity and priority
   - Provide specific remediation steps for each issue
   - Create upgrade roadmap with risk assessments
   - Generate compliance reports for stakeholders

## Constraints

- DO NOT automatically update or modify package files
- MUST respect existing version constraints and compatibility requirements
- SHOULD prioritize security vulnerabilities over feature updates
- MUST consider breaking changes and migration effort
- DO NOT assume all packages should be updated to latest versions
- SHOULD balance security, stability, and feature requirements

## Examples

### Example 1: Pre-Release Security Audit

**Input**: Repository path with security threshold = "medium", package managers = "all"
**Output**: Security-focused dependency audit report
**Focus**: Vulnerabilities, outdated packages, license compliance
**Notes**: Prioritize critical and high-severity security issues

### Example 2: Dependency Modernization

**Input**: Repository with upgrade strategy = "conservative", focus areas = "major version updates"
**Output**: Modernization roadmap with upgrade paths
**Focus**: Safe upgrade opportunities, breaking change analysis, migration planning
**Notes**: Emphasize stability and minimal risk

### Example 3: License Compliance Review

**Input**: Repository with license compliance = "strict", package managers = "npm, pip"
**Output**: License compliance report with risk assessment
**Focus**: License conflicts, GPL contamination, compliance violations
**Notes**: Flag any licenses incompatible with project requirements

## Assets

- dependency_scanner.py: Tool for analyzing package management files
- vulnerability_checker.py: Script for checking known security issues
- license_analyzer.py: Tool for license compliance analysis
- upgrade_planner.py: Script for generating upgrade recommendations
- package_health.py: Tool for assessing package maintenance status
- audit_report_template.md: Standard audit report format
- security_databases.json: Local cache of known vulnerabilities (optional)


## Description

The Deps Audit skill provides an automated workflow to address analyze and assess the health, security, and maintenance status of project dependencies. used to identify outdated packages, security vulnerabilities, license compliance issues, and potential upgrade opportunities.. It is designed to be highly modular and integrates seamlessly into larger agentic pipelines.

## Usage Examples

### Basic Usage
'Use deps-audit to analyze my current project context.'

### Advanced Usage
'Run deps-audit with focus on high-priority optimization targets.'

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