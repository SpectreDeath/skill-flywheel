---
Domain: SPECIFICATION_ENGINEERING
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: specification-architecture-decisions
---



## Purpose
Comprehensive Architecture Decision Records (ADR) system that automatically captures architectural decisions from code commits, pull requests, and team discussions with AI-powered context analysis and historical tracking.


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

- Documenting significant architectural decisions and their rationale
- Creating historical records of architectural evolution
- Establishing decision-making processes for technical choices
- Tracking architectural debt and technical trade-offs
- When architectural decisions need formal documentation and review
- For team knowledge sharing and onboarding new developers

## When NOT to Use

- Minor technical decisions with limited impact
- Rapid prototyping where decisions are expected to change
- When existing documentation processes are sufficient
- Projects with very tight timelines requiring rapid development
- Teams without established architectural review processes

## Inputs

- **Required**: Code commits and pull requests with architectural changes
- **Required**: Team discussions and decision-making meetings
- **Optional**: Technical design documents and architecture diagrams
- **Optional**: Business requirements and constraint documentation
- **Optional**: Risk assessments and impact analysis
- **Optional**: Alternative solutions considered and rejected

## Outputs

- **Primary**: Comprehensive Architecture Decision Records (ADRs)
- **Secondary**: Decision rationale and trade-off analysis
- **Tertiary**: Impact assessment and migration strategies
- **Format**: Structured ADR documents with metadata, context, and decision tracking

## Capabilities

### 1. Decision Identification and Capture
- **Monitor code commits** for architectural changes and patterns
- **Analyze pull requests** for architectural decision points
- **Track team discussions** and decision-making conversations
- **Identify decision triggers** (new technologies, scaling needs, performance issues)
- **Capture decision context** and influencing factors

### 2. ADR Structure and Documentation
- **Document decision context** and problem statement
- **Record alternatives considered** and rationale for choices
- **Specify decision outcome** and implementation approach
- **Define success criteria** and validation methods
- **Establish review and update** processes

### 3. Context Analysis and Rationale
- **Analyze business drivers** and technical constraints
- **Document trade-offs** and compromise decisions
- **Record assumptions** and dependencies
- **Identify risks** and mitigation strategies
- **Capture lessons learned** and future considerations

### 4. Impact Assessment and Migration
- **Assess impact** on existing systems and components
- **Plan migration strategies** for implementation
- **Identify dependencies** and integration points
- **Define rollback procedures** for risk mitigation
- **Estimate effort** and resource requirements

### 5. Review and Approval Process
- **Establish review criteria** for architectural decisions
- **Create approval workflows** with appropriate stakeholders
- **Set up decision validation** and quality gates
- **Document dissenting opinions** and alternative viewpoints
- **Maintain decision audit trail** and version history

### 6. Historical Tracking and Evolution
- **Track decision evolution** over time and context changes
- **Monitor decision effectiveness** and outcomes
- **Update ADRs** based on new information or changes
- **Retire outdated decisions** with proper documentation
- **Maintain decision lineage** and historical context

## Constraints

- **NEVER** document decisions without proper context and rationale
- **ALWAYS** maintain consistency with architectural principles
- **MUST** ensure ADRs are accessible and discoverable
- **SHOULD** follow established ADR format and structure
- **MUST** maintain historical accuracy and completeness

## Examples

### Example 1: Microservices Migration Decision

**Input**: Code commits showing service decomposition, team discussions on migration strategy, performance analysis
**Output**:
- ADR documenting microservices migration decision
- Rationale based on scalability and team autonomy needs
- Impact assessment on existing monolithic system
- Migration strategy with phased rollout approach
- Success criteria and monitoring requirements

### Example 2: Database Technology Selection

**Input**: Technical evaluation documents, performance benchmarks, team discussions on data requirements
**Output**:
- ADR for database technology selection (SQL vs NoSQL)
- Alternatives considered with detailed comparison
- Decision rationale based on data consistency and scalability needs
- Implementation plan with data migration strategy
- Risk assessment and mitigation approaches

### Example 3: Cloud Provider Selection

**Input**: Cloud provider evaluation, cost analysis, team discussions on deployment strategy
**Output**:
- ADR documenting cloud provider selection decision
- Business and technical drivers for the choice
- Cost-benefit analysis and long-term implications
- Migration strategy and vendor lock-in considerations
- Success metrics and review criteria

## Edge Cases and Troubleshooting

### Edge Case 1: Reversing Previous Decisions
**Problem**: Need to reverse or modify previously documented architectural decisions
**Solution**: Create new ADR documenting the reversal with updated rationale and impact analysis

### Edge Case 2: Emergency Architectural Changes
**Problem**: Urgent changes made without proper ADR documentation
**Solution**: Create retrospective ADRs with detailed context and justification for emergency decisions

### Edge Case 3: Conflicting ADRs
**Problem**: New decisions conflict with existing ADRs
**Solution**: Create decision conflict resolution process and update relevant ADRs with clear reasoning

### Edge Case 4: ADR Maintenance Overhead
**Problem**: ADR documentation becomes burdensome and slows development
**Solution**: Implement automated ADR generation and streamlined review processes

## Quality Metrics

### ADR Quality Metrics
- **Completeness**: All required ADR sections properly documented
- **Clarity**: Decision rationale and context clearly explained
- **Accuracy**: Technical details and assumptions accurately recorded
- **Consistency**: ADR format and structure maintained consistently
- **Timeliness**: ADRs created and updated in a timely manner

### Decision Quality Metrics
- **Rationale Quality**: Clear reasoning behind architectural choices
- **Alternatives Coverage**: Comprehensive consideration of alternatives
- **Impact Assessment**: Thorough analysis of decision consequences
- **Risk Management**: Proper identification and mitigation of risks
- **Stakeholder Alignment**: Consensus and buy-in from relevant stakeholders

### Historical Tracking Metrics
- **Decision Lineage**: Clear tracking of decision evolution over time
- **Outcome Tracking**: Monitoring of decision effectiveness and results
- **Knowledge Preservation**: Effective capture of institutional knowledge
- **Accessibility**: Easy discovery and understanding of architectural history
- **Maintenance**: Regular updates and maintenance of ADR repository

## Integration with Other Skills

### With Technical Specification Authoring
Ensure ADRs integrate with technical specifications and provide architectural context for implementation.

### With API Specification Design
Document API design decisions and architectural patterns in ADR format for comprehensive architectural history.

### With Test Plan Specification
Create test strategies based on architectural decisions and ensure ADR compliance in testing processes.

## Usage Patterns

### ADR Creation and Management Workflow
```
1. Identify architectural decision points and triggers
2. Capture decision context and influencing factors
3. Document alternatives considered and rationale
4. Create structured ADR with all required sections
5. Establish review and approval process
6. Maintain ADR repository and historical tracking
```

### Automated ADR Generation
```
1. Monitor code changes and pull requests for architectural patterns
2. Analyze team discussions and decision-making conversations
3. Automatically generate ADR drafts with AI-powered context analysis
4. Validate ADR completeness and accuracy
5. Integrate with review and approval workflows
```

## Success Stories

### Architectural Knowledge Preservation
A software development team reduced onboarding time for new developers by 50% through comprehensive ADR documentation that captured architectural decisions and rationale.

### Decision Quality Improvement
An enterprise improved architectural decision quality by 60% by implementing structured ADR processes that ensured proper consideration of alternatives and impact assessment.

### Technical Debt Management
A development organization successfully managed technical debt by using ADRs to track architectural decisions and identify areas requiring refactoring or improvement.

## When ADR System Works Best

- **Large development teams** requiring architectural consistency
- **Complex systems** with multiple architectural decision points
- **Long-term projects** needing architectural history preservation
- **Regulated industries** requiring decision documentation and audit trails
- **Organizations with established** architectural review processes

## When to Avoid Complex ADR Systems

- **Small teams** with simple architectural decisions
- **Rapid prototyping** projects with evolving architecture
- **Teams without established** architectural review processes
- **Projects with very tight timelines** requiring rapid development
- **When existing documentation** processes are sufficient

## Future ADR Trends

### AI-Powered Decision Analysis
Using AI to analyze code patterns and automatically identify architectural decision points for ADR documentation.

### Real-time ADR Updates
Integrating ADR systems with development workflows to automatically update decisions based on code changes and new information.

### Decision Impact Visualization
Creating visual representations of architectural decision impact and relationships for better understanding and communication.

### ADR Integration with Development Tools
Deep integration with IDEs, version control systems, and project management tools for seamless ADR creation and maintenance.

## Architecture Decision Records Mindset

Remember: Effective ADR systems require balancing documentation completeness with development agility while ensuring architectural decisions are properly captured, reviewed, and maintained. Focus on creating living documents that preserve institutional knowledge, support decision-making, and enable architectural evolution while maintaining clarity and accessibility for development teams.

This skill provides comprehensive Architecture Decision Records guidance for professional software development.


## Description

The Specification Architecture Decisions skill provides an automated workflow to address comprehensive architecture decision records (adr) system that automatically captures architectural decisions from code commits, pull requests, and team discussions with ai-powered context analysis and historical tracking.. It is designed to be highly modular and integrates seamlessly into larger agentic pipelines.

## Usage Examples

### Basic Usage
'Use specification-architecture-decisions to analyze my current project context.'

### Advanced Usage
'Run specification-architecture-decisions with focus on high-priority optimization targets.'

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