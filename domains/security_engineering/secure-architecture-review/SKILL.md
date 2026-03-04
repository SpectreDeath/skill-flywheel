---
Domain: security_engineering
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: secure-architecture-review
---



## Description

Completely automates secure architecture reviews and threat modeling across applications, infrastructure, and cloud environments. This skill analyzes system designs, identifies security vulnerabilities, performs threat modeling, and provides comprehensive security recommendations while integrating with development workflows and compliance frameworks.


## Purpose

*[Content for Purpose section to be added based on the specific skill requirements]*

## Examples

*[Content for Examples section to be added based on the specific skill requirements]*

## Implementation Notes

*[Content for Implementation Notes section to be added based on the specific skill requirements]*
## Capabilities

- **Architecture Analysis**: Analyze system architecture diagrams, code structure, and deployment configurations
- **Threat Modeling**: Implement STRIDE, DREAD, and PASTA methodologies with automated threat identification
- **Security Pattern Validation**: Validate against security design patterns and anti-patterns
- **Attack Surface Analysis**: Identify and analyze potential attack vectors and entry points
- **Data Flow Security**: Analyze data flows for security vulnerabilities and compliance violations
- **Cloud Security Assessment**: Review cloud architecture for security best practices and misconfigurations
- **Compliance Mapping**: Map architecture to security standards (NIST, ISO 27001, SOC 2, PCI DSS)

## Usage Examples

### Application Architecture Security Review

```yaml
architecture_review:
  application_type: "microservices"
  technology_stack: ["kubernetes", "docker", "istio", "aws"]
  review_scope: "comprehensive"
  
  architecture_components:
    - component: "api_gateway"
      technology: "istio_ingress"
      security_controls:
        - "tls_termination"
        - "rate_limiting"
        - "authentication"
        - "authorization"
      vulnerabilities:
        - "ddos_vulnerability"
        - "certificate_management"
    
    - component: "authentication_service"
      technology: "oauth2_oidc"
      security_controls:
        - "multi_factor_auth"
        - "session_management"
        - "password_policy"
        - "account_lockout"
      vulnerabilities:
        - "brute_force_attacks"
        - "session_fixation"
        - "token_theft"
    
    - component: "database_layer"
      technology: "aws_rds_postgresql"
      security_controls:
        - "encryption_at_rest"
        - "encryption_in_transit"
        - "access_controls"
        - "audit_logging"
      vulnerabilities:
        - "sql_injection"
        - "privilege_escalation"
        - "data_exfiltration"
  
  threat_modeling:
    stride_analysis:
      spoofing:
        - threat: "identity_spoofing"
          likelihood: "medium"
          impact: "high"
          mitigation: "implement_strong_authentication"
      
      tampering:
        - threat: "data_tampering"
          likelihood: "low"
          impact: "critical"
          mitigation: "implement_integrity_checks"
      
      repudiation:
        - threat: "non_repudiation"
          likelihood: "medium"
          impact: "medium"
          mitigation: "implement_audit_trails"
      
      information_disclosure:
        - threat: "data_leakage"
          likelihood: "high"
          impact: "critical"
          mitigation: "implement_data_encryption"
      
      denial_of_service:
        - threat: "service_disruption"
          likelihood: "medium"
          impact: "high"
          mitigation: "implement_rate_limiting"
      
      elevation_of_privilege:
        - threat: "privilege_escalation"
          likelihood: "low"
          impact: "critical"
          mitigation: "implement_least_privilege"
    
    dread_scoring:
      - threat: "sql_injection"
        damage: 9
        reproducibility: 8
        exploitability: 7
        affected_users: 10
        discoverability: 6
        dread_score: 8.0
    
    pasta_analysis:
      - stage: "business_impact_analysis"
        focus: "identify_business_assets"
        output: "asset_criticality_matrix"
      
      - stage: "technical_scope_definition"
        focus: "define_technical_boundaries"
        output: "technical_scope_document"
      
      - stage: "decomposition"
        focus: "analyze_system_components"
        output: "component_analysis_report"
      
      - stage: "threat_analysis"
        focus: "identify_potential_threats"
        output: "threat_catalog"
      
      - stage: "vulnerability_identification"
        focus: "find_system_vulnerabilities"
        output: "vulnerability_assessment"
```

### Cloud Infrastructure Security Assessment

```yaml
cloud_security_assessment:
  cloud_provider: "aws"
  deployment_model: "multi_region"
  services_analyzed: ["ec2", "s3", "rds", "lambda", "iam", "vpc"]
  
  security_assessment:
    identity_and_access_management:
      - control: "least_privilege_access"
        status: "compliant"
        findings: []
        recommendations: []
      
      - control: "multi_factor_authentication"
        status: "partial"
        findings: ["root_account_mfa_missing"]
        recommendations: ["enable_mfa_for_root_account"]
    
    network_security:
      - control: "network_segmentation"
        status: "compliant"
        findings: []
        recommendations: []
      
      - control: "security_groups"
        status: "non_compliant"
        findings: ["overly_permissive_rules"]
        recommendations: ["implement_least_privilege_security_groups"]
    
    data_protection:
      - control: "encryption_at_rest"
        status: "compliant"
        findings: []
        recommendations: []
      
      - control: "encryption_in_transit"
        status: "partial"
        findings: ["unencrypted_data_transfers"]
        recommendations: ["enforce_tls_for_all_communications"]
    
    logging_and_monitoring:
      - control: "cloudtrail_enabled"
        status: "compliant"
        findings: []
        recommendations: []
      
      - control: "security_hub_enabled"
        status: "non_compliant"
        findings: ["security_hub_not_enabled"]
        recommendations: ["enable_security_hub_for_centralized_monitoring"]
  
  compliance_mapping:
    nist_framework:
      identify: "85%"
      protect: "78%"
      detect: "92%"
      respond: "75%"
      recover: "88%"
    
    iso_27001:
      a5_information_security_policies: "compliant"
      a6_organization_of_information_security: "compliant"
      a7_human_resource_security: "partial"
      a8_asset_management: "compliant"
      a9_access_control: "partial"
      a10_cryptography: "compliant"
      a11_physical_and_environmental_security: "compliant"
      a12_operations_security: "partial"
      a13_communications_security: "compliant"
      a14_system_acquisition_development_and_maintenance: "partial"
      a15_supplier_relationships: "compliant"
      a16_information_security_incident_management: "compliant"
      a17_information_security_aspects_of_business_continuity_management: "compliant"
      a18_compliance: "compliant"
```

### Secure Development Lifecycle Integration

```yaml
secure_devsecops_integration:
  design_phase:
    - activity: "security_requirements_definition"
      tools: ["threat_modeling", "security_patterns"]
      deliverables: ["security_requirements_document"]
      review_checklist: ["authentication", "authorization", "data_protection"]
    
    - activity: "architecture_security_review"
      tools: ["architecture_analysis", "threat_modeling"]
      deliverables: ["security_architecture_review_report"]
      review_checklist: ["security_controls", "attack_surface", "data_flow"]
  
  development_phase:
    - activity: "secure_coding_standards"
      tools: ["static_analysis", "code_reviews"]
      deliverables: ["secure_code_review_report"]
      review_checklist: ["input_validation", "output_encoding", "error_handling"]
    
    - activity: "dependency_security"
      tools: ["software_composition_analysis", "vulnerability_scanning"]
      deliverables: ["dependency_security_report"]
      review_checklist: ["known_vulnerabilities", "license_compliance", "supply_chain_risks"]
  
  testing_phase:
    - activity: "dynamic_security_testing"
      tools: ["dast", "penetration_testing"]
      deliverables: ["dynamic_security_test_report"]
      review_checklist: ["runtime_vulnerabilities", "configuration_issues", "authentication_bypass"]
    
    - activity: "security_integration_testing"
      tools: ["security_test_automation", "api_security_testing"]
      deliverables: ["security_integration_test_report"]
      review_checklist: ["api_security", "data_validation", "access_controls"]
  
  deployment_phase:
    - activity: "infrastructure_security_validation"
      tools: ["infrastructure_as_code_scanning", "container_security"]
      deliverables: ["infrastructure_security_report"]
      review_checklist: ["configuration_hardening", "container_security", "network_security"]
    
    - activity: "runtime_application_protection"
      tools: ["waf_configuration", "runtime_application_self_protection"]
      deliverables: ["runtime_protection_report"]
      review_checklist: ["waf_rules", "runtime_monitoring", "incident_response"]
```

## Input Format

### Architecture Review Configuration

```yaml
architecture_review_config:
  review_id: string               # Unique review identifier
  review_type: "application|infrastructure|cloud|hybrid"
  scope_definition: object        # Review scope and boundaries
  analysis_parameters: object     # Analysis configuration
  compliance_requirements: object # Compliance framework requirements
  
  scope_definition:
    systems_under_review: array   # Systems to analyze
    boundaries: object            # System boundaries
    assumptions: array            # Review assumptions
    limitations: array            # Review limitations
  
  analysis_parameters:
    threat_modeling_method: "stride|dread|pasta|octave"
    risk_assessment_method: "qualitative|quantitative|hybrid"
    security_frameworks: array    # Security frameworks to apply
    analysis_depth: "light|medium|deep|comprehensive"
  
  compliance_requirements:
    frameworks: array             # Compliance frameworks
    regulatory_requirements: array # Regulatory requirements
    industry_standards: array     # Industry standards
    organizational_policies: array # Organizational policies
```

### Architecture Documentation Schema

```yaml
architecture_documentation:
  system_overview:
    system_name: string
    system_description: string
    business_objectives: array
    technical_objectives: array
  
  architecture_diagrams:
    - diagram_type: "component_diagram"
      description: string
      file_path: string
      complexity_level: "low|medium|high"
    
    - diagram_type: "data_flow_diagram"
      description: string
      file_path: string
      complexity_level: "low|medium|high"
    
    - diagram_type: "deployment_diagram"
      description: string
      file_path: string
      complexity_level: "low|medium|high"
  
  component_details:
    - component_name: string
      component_type: "service|database|api|frontend|backend"
      technology_stack: array
      security_controls: array
      data_classification: string
      trust_zone: string
  
  data_flow_details:
    - flow_id: string
      source_component: string
      destination_component: string
      data_type: string
      data_classification: string
      security_requirements: array
      transmission_method: string
```

## Output Format

### Security Architecture Review Report

```yaml
security_architecture_review_report:
  review_metadata:
    review_id: string
    review_date: timestamp
    review_duration: number
    systems_reviewed: array
    reviewers: array
  
  executive_summary:
    overall_security_posture: "excellent|good|fair|poor"
    critical_findings: number
    high_risk_findings: number
    medium_risk_findings: number
    low_risk_findings: number
    risk_score: number            # 0-100 scale
    compliance_score: number      # 0-100 scale
  
  detailed_findings:
    - finding_id: string
      finding_title: string
      finding_description: string
      severity: "critical|high|medium|low"
      risk_score: number
      affected_components: array
      root_cause: string
      business_impact: string
      technical_impact: string
      likelihood: "low|medium|high"
      confidentiality_impact: "low|medium|high"
      integrity_impact: "low|medium|high"
      availability_impact: "low|medium|high"
      remediation_recommendations: array
      implementation_complexity: "low|medium|high"
      estimated_effort: string
      priority: "P1|P2|P3|P4"
  
  threat_modeling_results:
    identified_threats: array
    attack_vectors: array
    vulnerability_assessment: object
    risk_assessment: object
  
  security_control_assessment:
    preventive_controls: object
    detective_controls: object
    corrective_controls: object
    compensating_controls: object
  
  compliance_assessment:
    framework_compliance: object
    regulatory_compliance: object
    industry_standard_compliance: object
    policy_compliance: object
```

### Threat Model Report

```yaml
threat_model_report:
  threat_model_metadata:
    modeling_method: string
    modeling_date: timestamp
    systems_modeled: array
    threat_intelligence_sources: array
  
  identified_threats:
    - threat_id: string
      threat_name: string
      threat_description: string
      threat_actor: string
      motivation: string
      capability: string
      opportunity: string
      likelihood: "low|medium|high"
      impact: "low|medium|high|critical"
      risk_level: "low|medium|high|critical"
      mitigation_strategies: array
      detection_methods: array
      response_procedures: array
  
  attack_trees:
    - attack_tree_id: string
      target: string
      root_cause: string
      attack_paths: array
      required_skills: array
      required_resources: array
      estimated_time: string
  
  security_requirements:
    - requirement_id: string
      requirement_type: "confidentiality|integrity|availability|authentication|authorization|non_repudiation"
      requirement_description: string
      implementation_guidance: string
      verification_method: string
      priority: "high|medium|low"
```

## Configuration Options

### Review Methodologies

```yaml
review_methodologies:
  threat_modeling:
    stride: "enabled"
    dread: "enabled"
    pasta: "enabled"
    octave: "enabled"
    trike: "enabled"
  
  risk_assessment:
    qualitative: "enabled"
    quantitative: "enabled"
    hybrid: "enabled"
    fair: "enabled"
  
  security_frameworks:
    nist_csf: "enabled"
    iso_27001: "enabled"
    soc_2: "enabled"
    pci_dss: "enabled"
    hipaa: "enabled"
    gdpr: "enabled"
```

### Analysis Depth Levels

```yaml
analysis_depth_levels:
  light:
    scope: "high_level_review"
    tools: ["basic_scanning", "document_review"]
    time_allocation: "2-4_hours"
    deliverables: ["summary_report"]
  
  medium:
    scope: "detailed_review"
    tools: ["comprehensive_scanning", "architecture_analysis", "threat_modeling"]
    time_allocation: "4-8_hours"
    deliverables: ["detailed_report", "threat_model"]
  
  deep:
    scope: "in_depth_review"
    tools: ["full_analysis", "penetration_testing", "code_review"]
    time_allocation: "8-16_hours"
    deliverables: ["comprehensive_report", "threat_model", "test_results"]
  
  comprehensive:
    scope: "enterprise_wide_review"
    tools: ["all_available_tools", "manual_testing", "expert_review"]
    time_allocation: "16-24_hours"
    deliverables: ["enterprise_report", "threat_model", "test_results", "roadmap"]
```

## Error Handling

### Review Failures

```yaml
review_failures:
  documentation_unavailable:
    retry_strategy: "alternative_sources"
    max_retries: 3
    fallback_action: "interview_based_analysis"
  
  tool_integration_failure:
    retry_strategy: "alternative_tools"
    max_retries: 2
    fallback_action: "manual_analysis"
  
  scope_discrepancies:
    retry_strategy: "scope_validation"
    max_retries: 1
    escalation: "architecture_review_board"
  
  resource_constraints:
    retry_strategy: "scope_reduction"
    max_retries: 1
    escalation: "management_approval"
```

### Analysis Errors

```yaml
analysis_errors:
  incomplete_data:
    retry_strategy: "data_collection"
    max_retries: 2
    fallback_action: "partial_analysis"
  
  conflicting_information:
    retry_strategy: "validation_process"
    max_retries: 1
    escalation: "subject_matter_expert"
  
  tool_incompatibility:
    retry_strategy: "tool_configuration"
    max_retries: 1
    fallback_action: "manual_analysis"
```

## Performance Optimization

### Review Optimization

```yaml
review_optimization:
  parallel_analysis: true
  caching_strategy: "architecture_patterns"
  incremental_reviews: true
  template_reuse: true
  
  resource_optimization:
    cpu_allocation: "dynamic"
    memory_management: "optimized"
    storage_optimization: "enabled"
    network_optimization: "enabled"
```

### Analysis Performance

```yaml
analysis_performance:
  batch_processing: true
  parallel_processing: true
  result_caching: true
  incremental_analysis: true
  
  performance_monitoring:
    real_time_metrics: true
    bottleneck_detection: true
    optimization_recommendations: true
    resource_utilization_tracking: true
```

## Integration Examples

### With Development Workflows

```yaml
development_workflow_integration:
  design_phase:
    - integration_point: "architecture_design"
      tools: ["architecture_analysis", "threat_modeling"]
      artifacts: ["security_architecture_review"]
      gates: ["security_design_approval"]
  
  development_phase:
    - integration_point: "code_development"
      tools: ["secure_coding_guidelines", "code_reviews"]
      artifacts: ["secure_code_review"]
      gates: ["security_code_approval"]
  
  testing_phase:
    - integration_point: "security_testing"
      tools: ["sast", "dast", "penetration_testing"]
      artifacts: ["security_test_results"]
      gates: ["security_test_approval"]
  
  deployment_phase:
    - integration_point: "production_deployment"
      tools: ["infrastructure_scanning", "runtime_protection"]
      artifacts: ["deployment_security_report"]
      gates: ["security_deployment_approval"]
```

### With Security Tools

```yaml
security_tool_integration:
  static_analysis_tools:
    - tool: "sonarqube"
      integration_type: "api_based"
      scan_frequency: "continuous"
      report_format: "json"
      quality_gates: "enabled"
    
    - tool: "checkmarx"
      integration_type: "api_based"
      scan_frequency: "on_commit"
      report_format: "xml"
      quality_gates: "enabled"
  
  dynamic_analysis_tools:
    - tool: "owasp_zap"
      integration_type: "api_based"
      scan_frequency: "on_deploy"
      report_format: "html"
      quality_gates: "enabled"
    
    - tool: "burp_suite"
      integration_type: "api_based"
      scan_frequency: "scheduled"
      report_format: "json"
      quality_gates: "enabled"
  
  infrastructure_tools:
    - tool: "terraform"
      integration_type: "plugin_based"
      scan_frequency: "on_plan"
      report_format: "json"
      quality_gates: "enabled"
    
    - tool: "kubernetes"
      integration_type: "api_based"
      scan_frequency: "continuous"
      report_format: "yaml"
      quality_gates: "enabled"
```

## Best Practices

1. **Architecture Review Process**:
   - Establish clear review criteria and checklists
   - Use standardized threat modeling methodologies
   - Document all assumptions and limitations
   - Maintain consistency across reviews

2. **Threat Modeling**:
   - Involve cross-functional teams in threat modeling
   - Use multiple threat modeling methodologies
   - Regularly update threat models as systems evolve
   - Validate threat models with real-world scenarios

3. **Security Integration**:
   - Integrate security reviews into development lifecycle
   - Establish security gates at key milestones
   - Provide clear security requirements and guidance
   - Maintain security documentation and artifacts

4. **Continuous Improvement**:
   - Regularly review and update security standards
   - Learn from security incidents and near misses
   - Stay current with security best practices
   - Measure and improve review effectiveness

## Troubleshooting

### Common Issues

1. **Incomplete Documentation**: Use alternative sources, conduct interviews, implement documentation standards
2. **Tool Integration Problems**: Check API connectivity, validate configuration, review authentication
3. **Scope Discrepancies**: Clarify scope with stakeholders, establish clear boundaries, document assumptions
4. **Resource Constraints**: Prioritize critical systems, implement phased approach, leverage automation
5. **Stakeholder Buy-in**: Demonstrate business value, provide clear guidance, offer training and support

### Debug Mode

```yaml
debug_config:
  enabled: true
  log_level: "debug"
  architecture_analysis_debugging: true
  threat_modeling_debugging: true
  compliance_mapping_debugging: true
  performance_monitoring: true
```

## Monitoring and Metrics

### Key Performance Indicators

```yaml
kpi_metrics:
  review_effectiveness:
    critical_findings_detected: number
    false_positive_rate: number
    review_completion_rate: number
    stakeholder_satisfaction: number
  
  security_improvement:
    risk_reduction_achieved: number
    compliance_improvement: number
    security_incident_reduction: number
    remediation_completion_rate: number
  
  business_value:
    cost_avoidance: number
    time_to_market_improvement: number
    regulatory_compliance_score: number
    customer_trust_improvement: number
```

## Dependencies

- **Architecture Analysis Tools**: UML tools, architecture modeling software, diagram analysis tools
- **Threat Modeling Tools**: Threat modeling frameworks, attack tree analysis tools, risk assessment tools
- **Security Analysis Tools**: SAST, DAST, IaC scanning, container security tools
- **Compliance Frameworks**: NIST, ISO 27001, SOC 2, PCI DSS, HIPAA, GDPR frameworks
- **Integration APIs**: Development tools, security tools, compliance management systems

## Version History

- **1.0.0**: Initial release with comprehensive architecture review and threat modeling
- **1.1.0**: Added advanced threat modeling methodologies and cloud security assessment
- **1.2.0**: Enhanced DevSecOps integration and automated security analysis
- **1.3.0**: Improved compliance mapping and continuous monitoring capabilities
- **1.4.0**: Advanced AI-driven architecture analysis and predictive security assessment

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

Content for ## Constraints involving Secure Architecture Review.