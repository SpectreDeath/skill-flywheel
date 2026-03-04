---
Domain: DEVOPS
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: devops-cicd-automation
---



## Purpose
Comprehensive CI/CD pipeline development and automation workflows for modern DevOps practices, including containerization, infrastructure as code, and deployment strategies.


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

- Building automated CI/CD pipelines for software projects
- Implementing containerization with Docker and Kubernetes
- Creating infrastructure as code (IaC) solutions
- Setting up automated testing and deployment workflows
- Managing multi-environment deployments
- Implementing GitOps and continuous delivery practices

## When NOT to Use

- Simple projects without deployment requirements
- Manual deployment processes that don't require automation
- Legacy systems that cannot be containerized
- Projects with strict compliance requirements that prohibit automation
- When team lacks DevOps expertise and training

## Inputs

- **Required**: Target platform (AWS, Azure, GCP, on-premise)
- **Required**: Application type (web, mobile, microservices, etc.)
- **Optional**: Container orchestration platform (Kubernetes, Docker Swarm)
- **Optional**: Infrastructure as code tool (Terraform, CloudFormation, Pulumi)
- **Optional**: CI/CD platform (Jenkins, GitLab CI, GitHub Actions, Azure DevOps)
- **Optional**: Security and compliance requirements

## Outputs

- **Primary**: Complete CI/CD pipeline architecture and implementation
- **Secondary**: Containerization and orchestration strategies
- **Tertiary**: Infrastructure as code templates and automation
- **Format**: DevOps-specific documentation with pipeline configurations and best practices

## Capabilities

### 1. Pipeline Architecture Design
- **Analyze application requirements** and deployment patterns
- **Design pipeline stages** (build, test, deploy, monitor)
- **Select appropriate tools** and technologies
- **Plan multi-environment** deployment strategies
- **Establish rollback** and recovery procedures

### 2. Containerization Strategy
- **Create Docker configurations** for all application components
- **Design multi-stage builds** for optimization
- **Implement container security** best practices
- **Set up container registries** and image management
- **Plan resource allocation** and scaling strategies

### 3. Infrastructure as Code
- **Design IaC templates** for consistent environments
- **Implement version control** for infrastructure changes
- **Create environment-specific** configurations
- **Set up automated provisioning** and teardown
- **Establish infrastructure monitoring** and alerting

### 4. Automated Testing Integration
- **Integrate unit and integration** testing in pipeline
- **Implement security scanning** and vulnerability assessment
- **Add performance testing** and load testing
- **Create automated code quality** checks
- **Set up test environment** provisioning and cleanup

### 5. Deployment Strategies
- **Design blue-green** or canary deployment patterns
- **Implement zero-downtime** deployment strategies
- **Create automated rollback** mechanisms
- **Set up feature flag** management
- **Plan database migration** strategies

### 6. Monitoring and Observability
- **Implement comprehensive** logging and monitoring
- **Set up alerting** and notification systems
- **Create dashboards** for pipeline and application metrics
- **Establish SLA/SLO** monitoring and reporting
- **Design incident response** procedures

## Constraints

- **NEVER** deploy未经测试的 code to production
- **ALWAYS** maintain pipeline security and access controls
- **MUST** implement proper rollback and recovery procedures
- **SHOULD** follow infrastructure as code best practices
- **MUST** ensure compliance with security and regulatory requirements

## Examples

### Example 1: Microservices CI/CD Pipeline

**Input**: Containerized microservices application on Kubernetes
**Output**:
- Multi-stage Docker builds for each service
- Kubernetes manifests and Helm charts
- GitLab CI pipeline with automated testing
- Blue-green deployment strategy
- Centralized logging and monitoring setup

### Example 2: Serverless Application Pipeline

**Input**: AWS Lambda-based serverless application
**Output**:
- SAM/CloudFormation templates for infrastructure
- GitHub Actions workflow for deployment
- Automated testing with local Lambda simulation
- Canary deployment with traffic shifting
- CloudWatch monitoring and alerting

### Example 3: Enterprise Multi-Environment Setup

**Input**: Large enterprise application with dev/staging/prod environments
**Output**:
- Terraform modules for environment provisioning
- Jenkins pipeline with approval gates
- Automated security scanning and compliance checks
- Database migration automation
- Comprehensive monitoring and incident management

## Edge Cases and Troubleshooting

### Edge Case 1: Pipeline Failures
**Problem**: Pipeline fails during deployment or testing
**Solution**: Implement comprehensive error handling, rollback mechanisms, and detailed logging

### Edge Case 2: Security Vulnerabilities
**Problem**: Security scanning detects vulnerabilities in containers or code
**Solution**: Implement automated security scanning, vulnerability management, and secure coding practices

### Edge Case 3: Resource Constraints
**Problem**: Pipeline runs out of resources during build or deployment
**Solution**: Optimize resource allocation, implement parallel processing, and use efficient build strategies

### Edge Case 4: Compliance Requirements
**Problem**: Pipeline doesn't meet regulatory or compliance requirements
**Solution**: Implement compliance automation, audit trails, and governance controls

## Quality Metrics

### Pipeline Performance Metrics
- **Build Time**: Optimized for fast feedback cycles
- **Deployment Frequency**: Support for multiple daily deployments
- **Lead Time**: Minimized time from commit to production
- **Recovery Time**: Fast rollback and recovery capabilities
- **Success Rate**: High percentage of successful deployments

### Infrastructure Metrics
- **Environment Consistency**: Identical environments across stages
- **Provisioning Time**: Fast infrastructure deployment
- **Resource Utilization**: Efficient use of compute and storage
- **Scalability**: Support for auto-scaling and load balancing
- **Reliability**: High availability and fault tolerance

### Security Metrics
- **Vulnerability Detection**: Comprehensive security scanning
- **Compliance Score**: Adherence to security standards
- **Access Control**: Proper authentication and authorization
- **Audit Trail**: Complete logging and monitoring
- **Incident Response**: Fast detection and resolution

## Integration with Other Skills

### With Security Scan
Apply comprehensive security scanning to all pipeline components and infrastructure code.

### With Performance Audit
Optimize pipeline performance and resource utilization for faster deployments.

### With Test Survey
Implement comprehensive testing strategies throughout the CI/CD pipeline.

## Usage Patterns

### CI/CD Pipeline Development
```
1. Analyze application architecture and deployment requirements
2. Design pipeline stages and tool selection
3. Implement containerization and IaC
4. Set up automated testing and quality gates
5. Configure deployment strategies and monitoring
6. Establish governance and compliance controls
```

### Infrastructure as Code Implementation
```
1. Design IaC architecture and module structure
2. Create reusable infrastructure templates
3. Implement version control and change management
4. Set up automated provisioning and testing
5. Establish monitoring and governance
6. Plan for scaling and optimization
```

## Success Stories

### Enterprise Transformation
A Fortune 500 company reduced deployment time from 2 weeks to 15 minutes through comprehensive CI/CD automation and containerization.

### Startup Scaling
A fast-growing startup successfully scaled from 10 to 1000+ deployments per day using automated CI/CD pipelines and Kubernetes orchestration.

### Legacy Modernization
An enterprise modernized legacy applications through containerization and CI/CD, achieving 90% reduction in deployment failures.

## When DevOps CI/CD Works Best

- **Microservices architectures** requiring automated deployment
- **Cloud-native applications** with containerization needs
- **High-frequency deployments** requiring automation
- **Multi-environment setups** needing consistency
- **Regulated industries** requiring compliance automation

## When to Avoid DevOps CI/CD

- **Simple applications** with infrequent deployments
- **Legacy systems** that cannot be easily automated
- **Teams without DevOps expertise** and training
- **Projects with strict manual approval** requirements
- **Environments with limited automation** capabilities

## Future DevOps Trends

### GitOps Evolution
Widespread adoption of GitOps for declarative infrastructure and application management.

### AI-Powered Automation
Integration of AI for intelligent pipeline optimization and anomaly detection.

### Edge Computing CI/CD
Specialized pipelines for edge computing and IoT deployments.

### Security-First DevOps
Shift-left security practices integrated throughout the pipeline.

## DevOps CI/CD Mindset

Remember: DevOps CI/CD requires balancing speed, security, and reliability while fostering collaboration between development and operations teams. Focus on automation, monitoring, and continuous improvement while maintaining security and compliance standards.

This skill provides comprehensive DevOps CI/CD pipeline automation guidance for professional software delivery.


## Description

The Devops Cicd Automation skill provides an automated workflow to address comprehensive ci/cd pipeline development and automation workflows for modern devops practices, including containerization, infrastructure as code, and deployment strategies.. It is designed to be highly modular and integrates seamlessly into larger agentic pipelines.

## Usage Examples

### Basic Usage
'Use devops-cicd-automation to analyze my current project context.'

### Advanced Usage
'Run devops-cicd-automation with focus on high-priority optimization targets.'

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