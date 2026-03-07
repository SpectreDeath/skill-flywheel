---
Domain: orchestration
Version: 1.0.0
Complexity: High
Type: Process
Category: Management
Estimated Execution Time: 300ms - 4 minutes
name: SKILL.skill_team_assembler
---


## Implementation Notes
To be provided dynamically during execution.

## Description

Implements intelligent skill team assembly for complex operations requiring multi-domain collaboration. This skill analyzes mission requirements, identifies optimal skill combinations, assembles specialized teams (such as forensics+osint+strategy for cyber ops), manages team dynamics, and ensures seamless coordination across the 234-skill empire. Uses constraint satisfaction algorithms and team optimization models to build the most effective skill teams for any objective.

## Purpose

To command skill team assembly by:
- Analyzing mission requirements and identifying required skill sets
- Assembling optimal teams from forensics, osint, strategy, and other domains
- Managing team composition and skill compatibility
- Optimizing team performance through strategic pairing
- Ensuring seamless coordination and communication between team members
- Adapting team composition based on mission evolution
- Maintaining team effectiveness and preventing skill conflicts

## Capabilities

- **Mission Analysis**: Analyze complex objectives to identify required skills
- **Team Composition Optimization**: Build optimal skill teams using constraint satisfaction
- **Cross-Domain Collaboration**: Assemble teams spanning multiple domains
- **Skill Compatibility Assessment**: Ensure skills work well together
- **Team Performance Monitoring**: Track and optimize team effectiveness
- **Dynamic Team Adaptation**: Modify teams based on evolving requirements
- **Conflict Resolution**: Prevent and resolve skill conflicts within teams
- **Communication Coordination**: Ensure seamless information flow between team members

## Usage Examples

### Basic Team Assembly

```yaml
team_assembly_request:
  mission_id: "cyber_ops_investigation_001"
  mission_type: "complex_cyber_operations"
  required_domains: ["FORENSICS", "OSINT_COLLECTOR", "STRATEGY_ANALYSIS"]
  
  team_requirements: {
    "minimum_skills": 5,
    "maximum_skills": 10,
    "required_specializations": ["data_analysis", "intelligence_gathering", "strategic_planning"],
    "compatibility_constraints": ["no_conflicting_skills", "complementary_expertise"]
  }
  
  assembled_team: {
    "team_id": "team_cyber_ops_alpha",
    "skills": [
      "forensic_data_collection",
      "osint_intelligence_gathering",
      "strategic_analysis",
      "threat_assessment",
      "response_coordination"
    ],
    "team_lead": "strategic_analysis",
    "communication_protocol": "real_time_sync"
  }
```

### Advanced Team Optimization

```yaml
team_optimization:
  optimization_strategy: "constraint_satisfaction"
  team_objective: "maximize_effectiveness"
  constraints: {
    "domain_diversity": "minimum_3_domains",
    "skill_compatibility": "no_conflicts",
    "resource_limits": "within_capacity",
    "time_constraints": "meet_deadlines"
  }
  
  optimization_results: {
    "team_composition_score": 0.94,
    "domain_coverage": 100.0,
    "skill_synergy": 0.88,
    "resource_efficiency": 0.82
  }
```

### Dynamic Team Adaptation

```yaml
dynamic_adaptation:
  team_id: "adaptive_investigation_team"
  base_composition: ["forensic_analysis", "osint_collection", "strategic_planning"]
  
  adaptation_rules: {
    "if_complexity_increases": {
      "action": "add_specialized_skills",
      "skills": ["advanced_threat_analysis", "cryptographic_analysis"],
      "trigger_condition": "complexity_score > 8.0"
    },
    "if_timeline_shortens": {
      "action": "optimize_for_speed",
      "skills": ["rapid_analysis", "automated_correlation"],
      "trigger_condition": "time_remaining < 50%_of_estimated"
    }
  }
```

## Input Format

### Team Assembly Request

```yaml
team_assembly_request:
  mission_id: string
  mission_description: string
  required_domains: array
  team_size_constraints: object
  skill_requirements: array
  compatibility_constraints: array
  
  mission_parameters: {
    "complexity_level": number,
    "time_sensitivity": string,
    "resource_availability": object,
    "risk_tolerance": string
  }
```

### Team Configuration

```yaml
team_configuration:
  team_id: string
  team_name: string
  team_lead: string
  team_members: array
  communication_strategy: string
  coordination_protocol: string
  
  team_rules: {
    "decision_making": "consensus|majority|lead_authority",
    "conflict_resolution": "mediation|escalation|rotation",
    "information_sharing": "open|restricted|need_to_know"
  }
```

## Output Format

### Team Assembly Report

```yaml
team_assembly_report:
  team_id: string
  assembly_timestamp: timestamp
  mission_id: string
  team_composition: array
  team_effectiveness_score: number
  
  skill_analysis: [
    {
      "skill_name": string,
      "role": string,
      "contribution_score": number,
      "compatibility_score": number,
      "criticality": string
    }
  ]
  
  team_dynamics: {
    "communication_efficiency": number,
    "conflict_potential": number,
    "collaboration_strength": number,
    "adaptability_score": number
  }
```

### Team Performance Report

```yaml
team_performance_report:
  team_id: string
  performance_period: object
  mission_progress: object
  team_effectiveness_metrics: object
  
  performance_indicators: {
    "task_completion_rate": number,
    "collaboration_efficiency": number,
    "conflict_resolution_time": number,
    "adaptation_speed": number
  }
  
  improvement_recommendations: [
    {
      "area": string,
      "recommendation": string,
      "priority": string,
      "expected_impact": string
    }
  ]
```

## Configuration Options

### Team Assembly Strategies

```yaml
team_assembly_strategies:
  constraint_satisfaction:
    description: "Optimize teams using constraint satisfaction algorithms"
    use_case: "complex_requirements"
    complexity: "high"
    accuracy: "very_high"
  
  genetic_algorithm:
    description: "Evolutionary approach to team optimization"
    use_case: "large_skill_pools"
    complexity: "medium"
    accuracy: "high"
  
  heuristic_matching:
    description: "Rule-based skill matching"
    use_case: "standard_teams"
    complexity: "low"
    accuracy: "medium"
  
  machine_learning:
    description: "ML-based team prediction and optimization"
    use_case: "adaptive_teams"
    complexity: "very_high"
    accuracy: "adaptive"
```

### Team Management Approaches

```yaml
team_management_approaches:
  centralized_coordination:
    description: "Single point of coordination and control"
    use_case: "critical_missions"
    communication: "hub_and_spoke"
    decision_making: "top_down"
  
  distributed_collaboration:
    description: "Peer-to-peer coordination and collaboration"
    use_case: "innovative_projects"
    communication: "mesh_network"
    decision_making: "consensus_based"
  
  hybrid_management:
    description: "Combination of centralized and distributed approaches"
    use_case: "complex_operations"
    communication: "mixed_topology"
    decision_making: "adaptive"
```

## Constraints

- **Skill Availability**: Cannot assign skills that are currently unavailable or overloaded
- **Domain Balance**: Must maintain appropriate domain representation in teams
- **Compatibility Requirements**: Skills must be compatible and non-conflicting
- **Resource Limits**: Team composition must respect resource constraints
- **Mission Alignment**: Team must align with mission objectives and requirements
- **Communication Protocols**: Must establish effective communication channels
- **Performance Standards**: Teams must meet minimum effectiveness thresholds

## Examples

### Cyber Operations Team

```yaml
cyber_ops_team: {
  "team_id": "cyber_ops_alpha",
  "mission": "complex_cyber_investigation",
  "skills": [
    "forensic_data_collection",
    "osint_intelligence_gathering",
    "strategic_analysis",
    "threat_assessment",
    "response_coordination"
  ],
  "team_structure": {
    "lead": "strategic_analysis",
    "specialists": ["forensic_data_collection", "osint_intelligence_gathering"],
    "support": ["threat_assessment", "response_coordination"]
  }
}
```

### Emergency Response Team

```yaml
emergency_response_team: {
  "team_id": "emergency_response_delta",
  "mission": "rapid_incident_response",
  "skills": [
    "rapid_assessment",
    "crisis_management",
    "communication_coordination",
    "resource_mobilization"
  ],
  "activation_protocol": "immediate",
  "response_time_target": "15_minutes"
}
```

## Error Handling

### Team Assembly Failures

```yaml
team_assembly_failures:
  insufficient_skills:
    cause: "Not enough qualified skills available"
    recovery: "expand_search_criteria_or_queue_for_availability"
    retry_policy: "adaptive_with_expanded_criteria"
  
  skill_conflicts:
    cause: "Identified skill incompatibilities"
    recovery: "resolve_conflicts_or_substitute_skills"
    retry_policy: "immediate_with_conflict_resolution"
  
  resource_overload:
    cause: "Team would exceed resource capacity"
    recovery: "optimize_team_size_or_stagger_activation"
    retry_policy: "immediate_with_resource_optimization"
  
  domain_imbalance:
    cause: "Team lacks required domain diversity"
    recovery: "recruit_missing_domain_skills"
    retry_policy: "immediate_with_domain_expansion"
```

### Team Performance Issues

```yaml
team_performance_issues:
  communication_breakdown:
    cause: "Poor information flow between team members"
    recovery: "implement_better_communication_protocols"
    retry_policy: "immediate_with_protocol_updates"
  
  skill_conflict:
    cause: "Team members have conflicting approaches"
    recovery: "mediate_conflict_or_reassign_roles"
    retry_policy: "immediate_with_conflict_resolution"
  
  performance_degradation:
    cause: "Team effectiveness declining over time"
    recovery: "team_restructuring_or_skill_refreshment"
    retry_policy: "gradual_with_performance_monitoring"
```

## Performance Optimization

### Team Optimization

```yaml
team_optimization:
  optimization_frequency: "real_time"
  performance_metrics: [
    "task_completion_rate",
    "collaboration_efficiency",
    "resource_utilization",
    "conflict_resolution_time"
  ]
  
  optimization_algorithms: {
    "team_composition": "constraint_satisfaction",
    "skill_pairing": "compatibility_analysis",
    "resource_allocation": "adaptive_distribution"
  }
```

### Dynamic Adaptation

```yaml
dynamic_adaptation:
  adaptation_triggers: [
    "mission_complexity_change",
    "resource_availability_change",
    "timeline_modification",
    "performance_degradation"
  ]
  
  adaptation_strategies: {
    "skill_replacement": "automatic_with_compatibility_check",
    "team_restructuring": "gradual_with_minimal_disruption",
    "protocol_updates": "immediate_with_team_notification"
  }
```

## Integration Examples

### With Multi-Skill Chaining Engine

```yaml
integration_chaining_engine: {
  "team_to_chain_mapping": "automatic",
  "execution_coordination": "synchronized",
  "performance_monitoring": "integrated",
  "error_handling": "coordinated"
}
```

### With Domain Portfolio Manager

```yaml
integration_portfolio_manager: {
  "domain_balance_monitoring": "continuous",
  "skill_availability_tracking": "real_time",
  "resource_allocation": "portfolio_aware",
  "compliance_monitoring": "integrated"
}
```

## Best Practices

1. **Skill Assessment**: Thoroughly assess skill capabilities and compatibility
2. **Team Diversity**: Ensure appropriate domain and skill diversity
3. **Communication Protocols**: Establish clear communication channels and protocols
4. **Performance Monitoring**: Continuously monitor team performance and effectiveness
5. **Conflict Resolution**: Implement proactive conflict resolution mechanisms
6. **Adaptability**: Design teams to be adaptable to changing requirements
7. **Documentation**: Maintain clear documentation of team structures and protocols

## Troubleshooting

### Common Team Assembly Issues

1. **Skill Shortages**: Implement skill development and cross-training programs
2. **Communication Breakdowns**: Establish redundant communication channels
3. **Performance Variance**: Implement performance standardization and training
4. **Resource Conflicts**: Use resource allocation optimization algorithms
5. **Domain Silos**: Promote cross-domain collaboration and understanding

### Debug Mode Configuration

```yaml
debug_config: {
  "enabled": true,
  "log_level": "detailed",
  "team_tracing": true,
  "performance_debugging": true,
  "compatibility_analysis": true
}
```

## Monitoring and Metrics

### Team Performance Metrics

```yaml
team_performance_metrics: {
  "team_effectiveness_score": "percentage",
  "collaboration_efficiency": "score",
  "task_completion_rate": "percentage",
  "conflict_resolution_time": "minutes"
}
```

### Team Health Indicators

```yaml
team_health_indicators: {
  "skill_compatibility": "score",
  "communication_quality": "score",
  "resource_balance": "percentage",
  "adaptability_index": "score"
}
```

## Dependencies

- **Skill Registry**: For skill metadata and availability information
- **Domain Portfolio Manager**: For domain balance and resource allocation
- **Multi-Skill Chaining Engine**: For team execution coordination
- **Empire Health Monitor**: For system health and performance data
- **Communication Hub**: For team coordination and information flow

## Version History

- **1.0.0**: Initial release with basic team assembly and compatibility checking
- **1.1.0**: Added constraint satisfaction algorithms and performance optimization
- **1.2.0**: Enhanced dynamic adaptation and conflict resolution
- **1.3.0**: Real-time team monitoring and adaptive management
- **1.4.0**: Advanced team analytics and comprehensive metrics

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.