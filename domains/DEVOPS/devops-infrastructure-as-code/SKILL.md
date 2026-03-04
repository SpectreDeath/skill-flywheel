---
Domain: DEVOPS
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: devops-infrastructure-as-code
---



## Purpose
Comprehensive infrastructure as code (IaC) development and management using Terraform, CloudFormation, Pulumi, and other IaC tools for automated, version-controlled infrastructure provisioning.


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

- Automating infrastructure provisioning and management
- Implementing consistent and repeatable infrastructure deployments
- Managing multi-cloud or hybrid cloud environments
- Enforcing infrastructure governance and compliance
- Implementing disaster recovery and backup strategies
- Managing infrastructure dependencies and relationships

## When NOT to Use

- Simple infrastructure requirements that don't benefit from automation
- Environments with frequent manual changes that bypass IaC
- Teams without IaC expertise and training
- Legacy systems that cannot be easily managed through code
- Projects with minimal infrastructure requirements

## Inputs

- **Required**: IaC tool selection (Terraform, CloudFormation, Pulumi, etc.)
- **Required**: Cloud provider or platform (AWS, Azure, GCP, on-premise)
- **Optional**: Infrastructure architecture and design
- **Optional**: Security and compliance requirements
- **Optional**: Cost optimization and resource management needs
- **Optional**: Monitoring and observability requirements

## Outputs

- **Primary**: Complete IaC templates and modules for infrastructure provisioning
- **Secondary**: Infrastructure governance and compliance frameworks
- **Tertiary**: Cost optimization and resource management strategies
- **Format**: IaC-specific documentation with code examples and best practices

## Capabilities

### 1. IaC Tool Selection and Setup
- **Evaluate IaC platforms** (Terraform, CloudFormation, Pulumi, Ansible)
- **Assess organizational requirements** and constraints
- **Design module structure** and organization
- **Set up version control** and collaboration workflows
- **Configure state management** and backend storage

### 2. Infrastructure Design and Architecture
- **Design infrastructure topology** and network architecture
- **Plan resource organization** and naming conventions
- **Define environment strategies** (dev, staging, production)
- **Establish dependency management** and resource relationships
- **Create reusable modules** and components

### 3. Security and Compliance Implementation
- **Implement security best practices** in IaC templates
- **Set up access controls** and IAM policies
- **Configure compliance frameworks** and auditing
- **Implement secrets management** and sensitive data handling
- **Design security scanning** and validation processes

### 4. Cost Optimization and Resource Management
- **Implement cost tracking** and monitoring
- **Design resource optimization** strategies
- **Set up tagging** and cost allocation
- **Configure auto-scaling** and resource limits
- **Implement resource lifecycle** management

### 5. Testing and Validation
- **Create automated testing** for IaC templates
- **Implement validation** and linting processes
- **Set up integration testing** for infrastructure changes
- **Design rollback** and recovery procedures
- **Configure drift detection** and remediation

### 6. Deployment and Operations
- **Set up CI/CD pipelines** for IaC deployment
- **Implement change management** and approval workflows
- **Configure monitoring** and alerting for infrastructure
- **Design incident response** procedures
- **Establish operational runbooks** and documentation

## Constraints

- **NEVER** hardcode sensitive information in IaC templates
- **ALWAYS** implement proper state management and locking
- **MUST** follow security best practices for all resources
- **SHOULD** implement comprehensive testing and validation
- **MUST** maintain infrastructure documentation and runbooks

## Examples

### Example 1: Multi-Cloud IaC Implementation

**Input**: Enterprise application requiring deployment across AWS and Azure
**Output**:
- Terraform modules for AWS and Azure resources
- Centralized state management with remote backends
- Cross-cloud networking and connectivity
- Unified security policies and compliance frameworks
- Cost optimization and monitoring across clouds

### Example 2: Kubernetes Infrastructure as Code

**Input**: Kubernetes cluster with supporting infrastructure
**Output**:
- IaC templates for cluster provisioning
- Network and storage configuration as code
- Security policies and RBAC configuration
- Monitoring and logging infrastructure
- Auto-scaling and resource management

### Example 3: Serverless Application IaC

**Input**: Serverless application with AWS Lambda and supporting services
**Output**:
- CloudFormation or SAM templates for serverless resources
- CI/CD pipeline for serverless deployments
- Environment-specific configurations
- Cost monitoring and optimization
- Security scanning and compliance validation

## Edge Cases and Troubleshooting

### Edge Case 1: State Drift
**Problem**: Infrastructure state diverges from IaC definitions
**Solution**: Implement drift detection, automated remediation, and proper state management

### Edge Case 2: Resource Dependencies
**Problem**: Complex resource dependencies causing deployment failures
**Solution**: Design proper dependency management, use modules, and implement validation

### Edge Case 3: Cost Overruns
**Problem**: IaC deployments causing unexpected costs
**Solution**: Implement cost monitoring, resource limits, and approval workflows

### Edge Case 4: Security Vulnerabilities
**Problem**: IaC templates with security misconfigurations
**Solution**: Implement security scanning, compliance validation, and secure coding practices

## Quality Metrics

### Infrastructure Quality Metrics
- **Provisioning Time**: Fast and efficient infrastructure deployment
- **Consistency**: Identical environments across stages
- **Reliability**: High success rate for infrastructure changes
- **Maintainability**: Well-organized and documented IaC code
- **Reusability**: Modular and reusable infrastructure components

### Security and Compliance Metrics
- **Security Score**: Adherence to security best practices
- **Compliance Score**: Meeting regulatory and organizational requirements
- **Vulnerability Detection**: Comprehensive security scanning
- **Access Control**: Proper authentication and authorization
- **Audit Trail**: Complete logging and change tracking

### Cost and Performance Metrics
- **Cost Optimization**: Efficient resource utilization and cost management
- **Resource Utilization**: Optimal use of compute, storage, and network resources
- **Performance**: Fast infrastructure provisioning and updates
- **Scalability**: Support for auto-scaling and resource growth
- **Reliability**: High availability and fault tolerance

## Integration with Other Skills

### With DevOps CI/CD
Integrate IaC with automated deployment pipelines and continuous delivery workflows.

### With Security Scan
Apply comprehensive security scanning to IaC templates and infrastructure configurations.

### With Performance Audit
Optimize infrastructure performance and resource utilization through IaC.

## Usage Patterns

### IaC Implementation Strategy
```
1. Select appropriate IaC tool and platform
2. Design infrastructure architecture and module structure
3. Implement security and compliance frameworks
4. Set up testing and validation processes
5. Configure CI/CD pipelines for deployment
6. Establish monitoring and operational procedures
```

### Multi-Cloud IaC Management
```
1. Design cloud-agnostic infrastructure patterns
2. Create provider-specific modules and configurations
3. Implement centralized state management
4. Set up cross-cloud networking and security
5. Configure unified monitoring and cost management
6. Establish governance and compliance frameworks
```

## Success Stories

### Enterprise IaC Transformation
A large enterprise reduced infrastructure provisioning time from weeks to hours through comprehensive IaC implementation, achieving 90% cost savings and improved compliance.

### Startup Infrastructure Scaling
A fast-growing startup successfully scaled their infrastructure to support 10x growth using IaC, maintaining consistency and reliability across all environments.

### Multi-Cloud Cost Optimization
An organization implemented IaC across multiple clouds, achieving 40% cost reduction through automated resource management and optimization.

## When Infrastructure as Code Works Best

- **Complex infrastructure requirements** with multiple components
- **Multi-environment deployments** requiring consistency
- **Regulated industries** needing compliance and audit trails
- **Rapid scaling requirements** needing automation
- **DevOps teams** implementing continuous delivery

## When to Avoid Infrastructure as Code

- **Simple infrastructure** that doesn't benefit from automation
- **Frequent manual changes** that bypass IaC processes
- **Teams without IaC expertise** and training
- **Legacy systems** that cannot be easily managed through code
- **Projects with minimal infrastructure** requirements

## Future Infrastructure as Code Trends

### GitOps Integration
Widespread adoption of GitOps for declarative infrastructure management and deployment.

### AI-Powered IaC
Integration of AI for intelligent infrastructure optimization and anomaly detection.

### Policy as Code
Advanced policy-as-code frameworks for automated compliance and governance.

### Edge Infrastructure IaC
Specialized IaC for edge computing and distributed infrastructure management.

## Infrastructure as Code Mindset

Remember: IaC requires treating infrastructure like software, with version control, testing, and continuous improvement. Focus on automation, consistency, and maintainability while ensuring security and compliance.

This skill provides comprehensive infrastructure as code guidance for professional infrastructure automation and management.


## Description

The Devops Infrastructure As Code skill provides an automated workflow to address comprehensive infrastructure as code (iac) development and management using terraform, cloudformation, pulumi, and other iac tools for automated, version-controlled infrastructure provisioning.. It is designed to be highly modular and integrates seamlessly into larger agentic pipelines.

## Usage Examples

### Basic Usage
'Use devops-infrastructure-as-code to analyze my current project context.'

### Advanced Usage
'Run devops-infrastructure-as-code with focus on high-priority optimization targets.'

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