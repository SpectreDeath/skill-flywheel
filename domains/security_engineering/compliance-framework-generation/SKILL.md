---
Domain: security_engineering
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: compliance-framework-generation
---



## Description

Automatically generates comprehensive compliance frameworks and security standards tailored to specific industries, regulatory requirements, and organizational needs. This skill analyzes existing security controls, maps them to relevant compliance standards, identifies gaps, and creates customized frameworks with detailed control requirements, assessment procedures, and continuous monitoring mechanisms.


## Purpose

*[Content for Purpose section to be added based on the specific skill requirements]*

## Examples

*[Content for Examples section to be added based on the specific skill requirements]*

## Implementation Notes

*[Content for Implementation Notes section to be added based on the specific skill requirements]*
## Capabilities

- **Regulatory Analysis**: Analyze applicable regulations (GDPR, HIPAA, SOX, PCI-DSS, NIST, ISO 27001, etc.)
- **Framework Mapping**: Map existing controls to multiple compliance frameworks simultaneously
- **Gap Analysis**: Identify compliance gaps and provide remediation roadmaps
- **Custom Framework Creation**: Generate organization-specific security frameworks
- **Control Assessment**: Define assessment procedures and evidence requirements
- **Continuous Monitoring**: Implement ongoing compliance monitoring and reporting
- **Audit Preparation**: Generate audit-ready documentation and evidence collection procedures

## Usage Examples

### Industry-Specific Compliance Framework

```yaml
compliance_framework:
  industry: "healthcare"
  organization_type: "hospital_network"
  regulatory_requirements:
    - "HIPAA_HITECH"
    - "NIST_Cybersecurity_Framework"
    - "SOC_2_Type_II"
    - "State_privacy_laws"
  
  framework_components:
    governance_structure:
      board_overview: "cybersecurity_committee"
      executive_sponsorship: "CISO_direct_report"
      risk_management: "enterprise_wide"
    
    security_controls:
      access_control:
        - control_id: "AC-1"
          control_name: "Access Control Policy"
          implementation: "role_based_access_control"
          monitoring: "continuous"
          assessment_frequency: "quarterly"
      
      data_protection:
        - control_id: "DP-1"
          control_name: "Data Classification"
          implementation: "automated_classification_tool"
          monitoring: "real_time"
          assessment_frequency: "monthly"
    
    incident_response:
      - procedure: "breach_notification"
        timeline: "72_hours"
        stakeholders: ["HIPAA_breach_notification", "state_laws"]
        documentation: "automated_template"
  
  compliance_monitoring:
    automated_assessments: true
    continuous_monitoring: true
    reporting_frequency: "monthly"
    executive_reporting: true
```

### Multi-Framework Mapping

```yaml
multi_framework_mapping:
  organization_profile:
    size: "enterprise"
    industry: "financial_services"
    geographic_presence: ["US", "EU", "Asia"]
  
  applicable_frameworks:
    - framework: "PCI_DSS_v4.0"
      scope: "payment_processing"
      controls_required: 378
      implementation_priority: "high"
    
    - framework: "SOX_404"
      scope: "financial_reporting"
      controls_required: 45
      implementation_priority: "critical"
    
    - framework: "NIST_SP_800-53"
      scope: "federal_contractor"
      controls_required: 1093
      implementation_priority: "medium"
    
    - framework: "ISO_27001"
      scope: "information_security"
      controls_required: 114
      implementation_priority: "medium"
  
  control_mapping:
    unified_controls:
      - control_id: "UNIFIED-AC-001"
        pci_dss_reference: "Req_8.1"
        sox_reference: "ITGC-AC-01"
        nist_reference: "AC-2"
        iso_reference: "A.9.1.1"
        description: "User Access Management"
        implementation: "identity_governance_platform"
        assessment_method: "automated_testing"
    
    gap_analysis:
      - framework: "PCI_DSS"
        gaps_identified: 15
        high_priority: 8
        medium_priority: 5
        low_priority: 2
        estimated_remediation_time: "6_months"
```

### Custom Security Framework Generation

```yaml
custom_framework_generation:
  organization_requirements:
    business_objectives: ["customer_trust", "regulatory_compliance", "competitive_advantage"]
    risk_tolerance: "low"
    technology_stack: ["cloud_native", "microservices", "containerized"]
    compliance_requirements: ["industry_specific", "international", "customer_contractual"]
  
  framework_structure:
    governance_layer:
      policy_framework:
        - policy_name: "Information_Security_Policy"
          policy_type: "governing"
          approval_authority: "board_of_directors"
          review_frequency: "annually"
        
        - policy_name: "Data_Protection_Policy"
          policy_type: "technical"
          approval_authority: "CISO"
          review_frequency: "semi_annually"
    
    control_layer:
      preventive_controls:
        - control_category: "access_management"
          controls: ["mfa", "rbac", "least_privilege"]
          implementation: "automated"
          monitoring: "continuous"
        
        - control_category: "data_protection"
          controls: ["encryption", "data_loss_prevention", "classification"]
          implementation: "layered"
          monitoring: "real_time"
    
    assessment_layer:
      control_assessment:
        - assessment_type: "automated_scanning"
          frequency: "continuous"
          tools: ["vulnerability_scanners", "configuration_assessment"]
        
        - assessment_type: "manual_testing"
          frequency: "quarterly"
          scope: ["critical_systems", "new_deployments"]
          methodology: "industry_standards"
    
    improvement_layer:
      continuous_improvement:
        - process: "lessons_learned"
          trigger: "security_incidents"
          timeline: "30_days"
          output: "process_improvements"
        
        - process: "framework_review"
          trigger: "regulatory_changes"
          timeline: "immediate"
          output: "framework_updates"
```

## Input Format

### Compliance Requirements Schema

```yaml
compliance_requirements:
  organization_profile:
    industry_sector: string
    organization_size: string
    geographic_presence: array
    regulatory_jurisdictions: array
    business_critical_systems: array
  
  applicable_regulations:
    - regulation_name: string
      jurisdiction: string
      scope: string
      enforcement_authority: string
      penalties: object
  
  existing_frameworks:
    - framework_name: string
      implementation_status: "not_implemented|partial|full"
      last_assessment_date: timestamp
      assessment_results: object
  
  business_requirements:
    risk_tolerance: "low|medium|high"
    compliance_priorities: array
    resource_constraints: object
    technology_constraints: object
```

### Framework Generation Parameters

```yaml
framework_generation_params:
  generation_type: "gap_analysis|framework_mapping|custom_framework"
  target_frameworks: array
  customization_level: "minimal|medium|high"
  automation_level: "manual|semi_automated|fully_automated"
  
  output_requirements:
    documentation_format: ["pdf", "html", "json", "excel"]
    audience: ["technical", "management", "executive", "audit"]
    integration_requirements: object
```

## Output Format

### Compliance Framework Document

```yaml
compliance_framework_document:
  framework_metadata:
    framework_name: string
    version: string
    creation_date: timestamp
    last_updated: timestamp
    applicable_industries: array
    regulatory_references: array
  
  framework_structure:
    governance_framework:
      - governance_component:
          component_name: string
          description: string
          responsible_party: string
          reporting_structure: object
    
    control_framework:
      - security_control:
          control_id: string
          control_name: string
          control_description: string
          control_type: "preventive|detective|corrective"
          implementation_guidance: string
          assessment_procedures: array
          evidence_requirements: array
          monitoring_frequency: string
          risk_impact: "high|medium|low"
    
    assessment_framework:
      - assessment_method:
          method_name: string
          scope: string
          frequency: string
          responsible_party: string
          tools_required: array
          success_criteria: object
  
  implementation_guide:
    phase_1: "assessment_and_planning"
    phase_2: "control_implementation"
    phase_3: "testing_and_validation"
    phase_4: "monitoring_and_improvement"
    
    implementation_roadmap:
      - milestone: string
        timeline: string
        resources_required: object
        success_metrics: array
```

### Gap Analysis Report

```yaml
gap_analysis_report:
  analysis_metadata:
    analysis_date: timestamp
    frameworks_analyzed: array
    scope: string
    methodology: string
  
  gap_summary:
    total_gaps: number
    critical_gaps: number
    high_priority_gaps: number
    medium_priority_gaps: number
    low_priority_gaps: number
  
  detailed_gaps:
    - gap_id: string
      framework_reference: string
      control_description: string
      current_state: string
      desired_state: string
      gap_severity: "critical|high|medium|low"
      remediation_effort: "low|medium|high|very_high"
      estimated_cost: number
      recommended_timeline: string
      responsible_party: string
  
  remediation_plan:
    - remediation_item:
        item_id: string
        description: string
        priority: "P1|P2|P3|P4"
        estimated_duration: string
        resource_requirements: object
        dependencies: array
        success_criteria: object
```

## Configuration Options

### Framework Types

```yaml
framework_types:
  industry_specific:
    healthcare: "HIPAA_HITECH|HITRUST|NIST_800-53"
    financial: "PCI_DSS|SOX|GLBA|FFIEC"
    government: "FISMA|NIST_SP_800-53|CMMC"
    cloud: "SOC_2|ISO_27001|CSA_STAR"
  
  regulatory_frameworks:
    privacy: "GDPR|CCPA|PIPEDA|LGPD"
    security: "NIST|ISO_27001|CIS_Critical_Security_Controls"
    industry: "PCI_DSS|HIPAA|SOX|NERC_CIP"
  
  custom_frameworks:
    organization_specific: "tailored_to_business_needs"
    technology_specific: "cloud_native|devsecops|iot"
    risk_based: "risk_tolerance_driven"
```

### Assessment Methods

```yaml
assessment_methods:
  automated_assessment:
    vulnerability_scanning: true
    configuration_assessment: true
    compliance_monitoring: true
    continuous_assessment: true
  
  manual_assessment:
    policy_review: true
    procedure_testing: true
    interview_based: true
    documentation_review: true
  
  hybrid_assessment:
    automated_discovery: true
    manual_validation: true
    risk_based_sampling: true
    continuous_monitoring: true
```

## Error Handling

### Framework Generation Errors

```yaml
framework_generation_errors:
  regulatory_analysis_failure:
    retry_strategy: "alternative_sources"
    max_retries: 3
    fallback_action: "manual_analysis"
  
  control_mapping_conflicts:
    resolution_strategy: "highest_standard"
    conflict_detection: "automated"
    manual_review_required: true
  
  resource_constraints:
    retry_strategy: "scope_reduction"
    max_retries: 2
    escalation: "management_approval"
  
  data_quality_issues:
    retry_strategy: "data_validation"
    max_retries: 1
    fallback_action: "partial_generation"
```

### Compliance Assessment Errors

```yaml
compliance_assessment_errors:
  evidence_unavailable:
    retry_strategy: "alternative_evidence"
    max_retries: 2
    escalation: "control_owner"
  
  assessment_tool_failure:
    retry_strategy: "alternative_tool"
    max_retries: 1
    fallback_action: "manual_assessment"
  
  scope_discrepancies:
    retry_strategy: "scope_validation"
    max_retries: 1
    escalation: "compliance_manager"
```

## Performance Optimization

### Framework Generation Optimization

```yaml
generation_optimization:
  parallel_processing: true
  caching_strategy: "framework_templates"
  incremental_updates: true
  template_reuse: true
  
  resource_optimization:
    cpu_allocation: "dynamic"
    memory_management: "optimized"
    storage_optimization: "enabled"
    network_optimization: "enabled"
```

### Assessment Performance

```yaml
assessment_performance:
  batch_processing: true
  parallel_assessments: true
  incremental_assessments: true
  result_caching: true
  
  performance_monitoring:
    real_time_metrics: true
    bottleneck_detection: true
    optimization_recommendations: true
    resource_utilization_tracking: true
```

## Integration Examples

### With GRC Platforms

```yaml
grc_integration:
  service_now_governance:
    instance_url: "https://company.service-now.com"
    username: "grc_integration"
    password: "encrypted_password"
    tables: ["rm_compliance_control", "rm_compliance_policy"]
  
  rsa_archer:
    api_endpoint: "https://archer.company.com/api"
    api_key: "encrypted_api_key"
    modules: ["compliance", "risk", "policy"]
  
  metricstream:
    integration_type: "api_based"
    endpoints: ["compliance_frameworks", "control_assessments"]
    authentication: "oauth2"
```

### With Security Tools

```yaml
security_tool_integration:
  vulnerability_scanners:
    nessus:
      api_endpoint: "https://nessus.company.com:8834"
      scan_policies: "compliance_based"
      reporting: "framework_mapped"
    
    qualys:
      api_endpoint: "https://qualysapi.qualys.com"
      scan_templates: "compliance_specific"
      compliance_reports: "automated"
  
  configuration_assessment:
    ansible:
      playbooks: "compliance_playbooks"
      inventory: "compliance_inventory"
      reporting: "compliance_status"
    
    chef:
      cookbooks: "compliance_cookbooks"
      compliance_profiles: "inspec_based"
      reporting: "compliance_dashboard"
```

## Best Practices

1. **Framework Development**:
   - Align frameworks with business objectives and risk tolerance
   - Use industry best practices as baseline
   - Ensure frameworks are scalable and maintainable
   - Regularly review and update frameworks

2. **Compliance Assessment**:
   - Use risk-based assessment approaches
   - Implement continuous monitoring where possible
   - Maintain comprehensive documentation
   - Regularly validate assessment results

3. **Gap Analysis**:
   - Prioritize gaps based on risk and impact
   - Develop realistic remediation timelines
   - Consider resource constraints in planning
   - Track progress and measure effectiveness

4. **Continuous Improvement**:
   - Monitor regulatory changes
   - Update frameworks based on lessons learned
   - Implement feedback mechanisms
   - Regularly assess framework effectiveness

## Troubleshooting

### Common Issues

1. **Framework Complexity**: Simplify frameworks, focus on critical controls, use automation
2. **Resource Constraints**: Prioritize high-impact controls, implement phased approach, leverage automation
3. **Stakeholder Buy-in**: Demonstrate business value, provide clear guidance, offer training
4. **Regulatory Changes**: Implement monitoring mechanisms, establish update processes, maintain flexibility
5. **Assessment Accuracy**: Use multiple assessment methods, implement validation procedures, maintain documentation

### Debug Mode

```yaml
debug_config:
  enabled: true
  log_level: "debug"
  framework_generation_tracing: true
  assessment_debugging: true
  compliance_mapping_debugging: true
  performance_monitoring: true
```

## Monitoring and Metrics

### Key Performance Indicators

```yaml
kpi_metrics:
  framework_effectiveness:
    compliance_score: number
    control_implementation_rate: number
    assessment_completion_rate: number
    remediation_completion_rate: number
  
  business_value:
    risk_reduction_achieved: number
    compliance_cost_reduction: number
    audit_efficiency_improvement: number
    stakeholder_satisfaction: number
  
  operational_metrics:
    framework_update_frequency: number
    assessment_accuracy: number
    resource_utilization: number
    automation_effectiveness: number
```

## Dependencies

- **Regulatory Databases**: Up-to-date regulatory requirements and interpretations
- **Framework Templates**: Industry-standard framework templates and best practices
- **Assessment Tools**: Vulnerability scanners, configuration assessment tools, GRC platforms
- **Reporting Systems**: Compliance dashboards, executive reporting, audit documentation
- **Integration APIs**: GRC platforms, security tools, enterprise systems

## Version History

- **1.0.0**: Initial release with basic compliance framework generation and gap analysis
- **1.1.0**: Added multi-framework mapping and automated assessment capabilities
- **1.2.0**: Enhanced regulatory analysis and continuous monitoring features
- **1.3.0**: Improved integration with GRC platforms and security tools
- **1.4.0**: Advanced AI-driven framework optimization and predictive compliance

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

Content for ## Constraints involving Compliance Framework Generation.