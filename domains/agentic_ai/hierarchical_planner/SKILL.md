---
Domain: agentic_ai
Version: 1.0.0
Complexity: Very High
Type: Planning
Category: Hierarchical Planning
Estimated Execution Time: 2-8 minutes
name: hierarchical_planner
---

## Implementation Notes
To be provided dynamically during execution.

## Description

Implements comprehensive hierarchical planning systems for creating multi-level planning architectures that enable agents to break down complex tasks into manageable subtasks with proper coordination and execution strategies. This skill creates sophisticated planning hierarchies with goal decomposition, task allocation, and progress monitoring.

## Purpose

To command hierarchical planning by:
- Creating multi-level planning architectures from complex task requirements
- Implementing goal decomposition and task breakdown mechanisms
- Designing task allocation and coordination strategies across planning levels
- Establishing progress monitoring and adaptation mechanisms
- Optimizing planning efficiency and resource utilization
- Ensuring seamless integration with multi-agent coordination systems

## Capabilities

- **Goal Decomposition**: Break down complex goals into hierarchical task structures
- **Task Allocation**: Distribute tasks across different planning levels and agents
- **Coordination Strategy Design**: Create coordination mechanisms for hierarchical planning
- **Progress Monitoring**: Implement comprehensive progress tracking and adaptation
- **Resource Optimization**: Optimize resource allocation across planning hierarchies
- **Adaptation Mechanisms**: Create dynamic adaptation strategies for changing conditions
- **Conflict Resolution**: Handle conflicts and dependencies in hierarchical planning
- **Performance Optimization**: Optimize planning efficiency and execution speed

## Usage Examples

### Basic Hierarchical Planning

```yaml
hierarchical_planning_request:
  complex_goal: "Develop_comprehensive_AI_research_platform"
  planning_levels: 3
  
  goal_decomposition: {
    "level_1_goals": ["platform_architecture", "core_functionality", "user_interface"],
    "level_2_tasks": {
      "platform_architecture": ["system_design", "technology_selection", "infrastructure_setup"],
      "core_functionality": ["data_processing", "ai_model_integration", "api_development"],
      "user_interface": ["ui_design", "user_experience", "accessibility_features"]
    },
    "level_3_subtasks": {
      "system_design": ["architecture_planning", "component_design", "integration_strategy"],
      "technology_selection": ["framework_evaluation", "tool_selection", "compatibility_analysis"]
    }
  }
  
  task_allocation: {
    "level_1_agents": ["architecture_agent", "development_agent", "design_agent"],
    "level_2_agents": ["specialized_development_agents"],
    "level_3_agents": ["implementation_agents"]
  }
```

### Advanced Multi-Agent Hierarchical Coordination

```yaml
multi_agent_hierarchical_coordination:
  coordination_type: "hierarchical_with_peer_communication"
  planning_strategy: "distributed_hierarchical_planning"
  
  coordination_mechanisms: {
    "goal_alignment": "top_down_goal_propagation",
    "task_coordination": "cross_level_task_synchronization",
    "progress_monitoring": "hierarchical_progress_tracking",
    "conflict_resolution": "escalation_based_resolution"
  }
  
  communication_patterns: {
    "vertical_communication": "goal_progress_updates",
    "horizontal_communication": "peer_coordination_messages",
    "cross_level_communication": "dependency_coordination"
  }
  
  adaptation_strategies: {
    "dynamic_replanning": "enabled",
    "resource_reallocation": "adaptive",
    "priority_adjustment": "intelligent"
  }
```

### Enterprise Hierarchical Planning System

```yaml
enterprise_hierarchical_planning:
  planning_scale: "enterprise_level"
  complexity_level: "very_high"
  coordination_requirements: "comprehensive"
  
  planning_hierarchy: {
    "strategic_level": {
      "time_horizon": "1-3_years",
      "decision_makers": ["executive_team"],
      "planning_focus": ["vision_goals", "resource_allocation", "strategic_direction"]
    },
    "tactical_level": {
      "time_horizon": "3-12_months",
      "decision_makers": ["department_leaders"],
      "planning_focus": ["departmental_goals", "resource_distribution", "implementation_strategy"]
    },
    "operational_level": {
      "time_horizon": "1-4_weeks",
      "decision_makers": ["team_leads", "individual_agents"],
      "planning_focus": ["task_execution", "daily_operations", "performance_monitoring"]
    }
  }
  
  integration_requirements: {
    "cross_level_integration": "seamless",
    "real_time_coordination": "enabled",
    "performance_tracking": "comprehensive",
    "adaptation_capabilities": "advanced"
  }
```

## Input Format

### Hierarchical Planning Request

```yaml
hierarchical_planning_request:
  planning_specification: object
  coordination_requirements: object
  performance_requirements: object
  
  planning_specification: {
    "complex_goal": string,
    "planning_levels": number,
    "goal_decomposition": object,
    "task_allocation": object
  }
  
  coordination_requirements: {
    "coordination_type": string,
    "communication_patterns": object,
    "conflict_resolution": object
  }
  
  performance_requirements: {
    "planning_efficiency": object,
    "resource_optimization": object,
    "adaptation_capabilities": object
  }
```

### Goal Decomposition Specification

```yaml
goal_decomposition_specification:
  complex_goal: {
    "goal_description": string,
    "goal_priority": string,
    "goal_deadline": string,
    "goal_dependencies": array
  }
  
  decomposition_strategy: {
    "decomposition_method": string,
    "level_count": number,
    "granularity_level": string,
    "dependency_mapping": object
  }
  
  task_structure: {
    "level_1_goals": array,
    "level_2_tasks": object,
    "level_3_subtasks": object,
    "task_dependencies": array
  }
```

## Output Format

### Hierarchical Planning Architecture

```yaml
hierarchical_planning_architecture:
  planning_metadata: {
    "architecture_name": string,
    "architecture_version": string,
    "complex_goal": string,
    "planning_levels": number,
    "creation_date": string
  }
  
  planning_hierarchy: {
    "level_1_strategic": object,
    "level_2_tactical": object,
    "level_3_operational": object
  }
  
  coordination_framework: {
    "coordination_mechanisms": object,
    "communication_protocols": object,
    "conflict_resolution": object
  }
  
  performance_framework: {
    "efficiency_metrics": object,
    "optimization_strategies": object,
    "adaptation_mechanisms": object
  }
```

### Task Allocation Plan

```yaml
task_allocation_plan:
  allocation_metadata: {
    "allocation_strategy": string,
    "agent_distribution": object,
    "resource_allocation": object
  }
  
  level_1_allocation: {
    "agents_assigned": array,
    "responsibilities": array,
    "coordination_requirements": object
  }
  
  level_2_allocation: {
    "agents_assigned": array,
    "responsibilities": array,
    "coordination_requirements": object
  }
  
  level_3_allocation: {
    "agents_assigned": array,
    "responsibilities": array,
    "coordination_requirements": object
  }
```

## Configuration Options

### Planning Levels

```yaml
planning_levels:
  strategic_level:
    description: "High-level planning for long-term goals and vision"
    time_horizon: "1-3_years",
    decision_makers: ["executive_agents"],
    complexity: "very_high",
    coordination: "top_down"
  
  tactical_level:
    description: "Mid-level planning for departmental and team goals"
    time_horizon: "3-12_months",
    decision_makers: ["managerial_agents"],
    complexity: "high",
    coordination: "cross_functional"
  
  operational_level:
    description: "Low-level planning for daily tasks and execution"
    time_horizon: "1-4_weeks",
    decision_makers: ["implementation_agents"],
    complexity: "medium",
    coordination: "peer_to_peer"
  
  execution_level:
    description: "Task-level planning for specific actions and operations"
    time_horizon: "hours_to_days",
    decision_makers: ["specialized_agents"],
    complexity: "low",
    coordination: "task_specific"
```

### Decomposition Strategies

```yaml
decomposition_strategies:
  functional_decomposition:
    description: "Decompose goals based on functional requirements"
    use_case: "complex_system_development",
    granularity: "medium",
    dependencies: "moderate"
  
  temporal_decomposition:
    description: "Decompose goals based on time-based milestones"
    use_case: "project_management",
    granularity: "fine",
    dependencies: "sequential"
  
  spatial_decomposition:
    description: "Decompose goals based on geographical or spatial factors"
    use_case: "distributed_systems",
    granularity: "coarse",
    dependencies: "independent"
  
  hybrid_decomposition:
    description: "Combine multiple decomposition approaches"
    use_case: "complex_enterprise_systems",
    granularity: "adaptive",
    dependencies: "complex"
```

## Constraints

- **Planning Consistency**: All planning levels must maintain consistency with overall goals
- **Coordination Requirements**: Comprehensive coordination mechanisms mandatory
- **Resource Allocation**: Optimize resource distribution across all planning levels
- **Adaptation Capabilities**: Dynamic adaptation mechanisms required for changing conditions
- **Performance Standards**: Must meet specified planning efficiency and execution speed
- **Conflict Resolution**: Robust conflict resolution mechanisms mandatory

## Examples

### Research Platform Hierarchical Planning

```yaml
research_platform_hierarchical_planning: {
  "planning_metadata": {
    "architecture_name": "ai_research_platform_planning",
    "architecture_version": "1.0.0",
    "complex_goal": "Develop_comprehensive_AI_research_platform",
    "planning_levels": 3,
    "creation_date": "2024-01-01"
  },
  
  "planning_hierarchy": {
    "level_1_strategic": {
      "goals": ["platform_vision", "technology_strategy", "resource_allocation"],
      "time_horizon": "6_months",
      "agents": ["architecture_agent", "strategy_agent"],
      "coordination": "top_down_goal_propagation"
    },
    "level_2_tactical": {
      "goals": ["core_components", "integration_strategy", "user_experience"],
      "time_horizon": "3_months",
      "agents": ["development_agents", "design_agents"],
      "coordination": "cross_level_task_synchronization"
    },
    "level_3_operational": {
      "goals": ["implementation_tasks", "testing_phases", "deployment_strategy"],
      "time_horizon": "1_month",
      "agents": ["implementation_agents", "testing_agents"],
      "coordination": "peer_coordination_and_progress_tracking"
    }
  },
  
  "coordination_framework": {
    "coordination_mechanisms": {
      "goal_alignment": "hierarchical_goal_propagation_with_feedback",
      "task_coordination": "dependency_based_task_synchronization",
      "progress_monitoring": "real_time_progress_tracking_across_levels",
      "conflict_resolution": "escalation_based_conflict_resolution"
    },
    "communication_protocols": {
      "vertical_communication": "goal_progress_updates_with_feedback_loops",
      "horizontal_communication": "peer_coordination_with_status_sharing",
      "cross_level_communication": "dependency_coordination_with_priority_management"
    },
    "conflict_resolution": {
      "resolution_strategy": "escalation_based_resolution",
      "escalation_levels": ["peer_negotiation", "managerial_intervention", "executive_decision"],
      "resolution_timeframes": ["immediate", "within_24_hours", "within_1_week"]
    }
  },
  
  "performance_framework": {
    "efficiency_metrics": {
      "planning_speed": "under_10_minutes_for_complex_goals",
      "coordination_efficiency": "minimize_communication_overhead",
      "resource_utilization": "optimize_across_all_levels"
    },
    "optimization_strategies": {
      "parallel_planning": "enabled_where_possible",
      "resource_optimization": "adaptive_allocation_across_levels",
      "communication_optimization": "minimize_cross_level_communication"
    },
    "adaptation_mechanisms": {
      "dynamic_replanning": "enabled_for_all_levels",
      "resource_reallocation": "adaptive_based_on_progress",
      "priority_adjustment": "intelligent_priority_management"
    }
  }
}
```

### Multi-Agent Coordination Strategy

```yaml
multi_agent_coordination_strategy: {
  "coordination_type": "hierarchical_with_peer_communication",
  "planning_strategy": "distributed_hierarchical_planning",
  
  "coordination_mechanisms": {
    "goal_alignment": {
      "alignment_method": "top_down_goal_propagation_with_bottom_up_feedback",
      "alignment_frequency": "continuous",
      "alignment_validation": "automatic_validation_with_conflict_detection"
    },
    "task_coordination": {
      "coordination_method": "dependency_based_task_synchronization",
      "coordination_frequency": "real_time",
      "coordination_validation": "automatic_dependency_validation"
    },
    "progress_monitoring": {
      "monitoring_method": "hierarchical_progress_tracking",
      "monitoring_frequency": "real_time",
      "monitoring_validation": "automatic_progress_validation"
    },
    "conflict_resolution": {
      "resolution_method": "escalation_based_resolution",
      "resolution_frequency": "as_needed",
      "resolution_validation": "automatic_resolution_validation"
    }
  },
  
  "communication_patterns": {
    "vertical_communication": {
      "communication_type": "goal_progress_updates",
      "communication_frequency": "periodic_with_event_triggered",
      "communication_format": "structured_update_format"
    },
    "horizontal_communication": {
      "communication_type": "peer_coordination_messages",
      "communication_frequency": "as_needed",
      "communication_format": "coordination_message_format"
    },
    "cross_level_communication": {
      "communication_type": "dependency_coordination",
      "communication_frequency": "event_triggered",
      "communication_format": "dependency_message_format"
    }
  },
  
  "adaptation_strategies": {
    "dynamic_replanning": {
      "replanning_trigger": "goal_progress_deviation",
      "replanning_scope": "adaptive_scope_based_on_impact",
      "replanning_frequency": "as_needed"
    },
    "resource_reallocation": {
      "reallocation_trigger": "resource_utilization_imbalance",
      "reallocation_scope": "cross_level_resource_optimization",
      "reallocation_frequency": "adaptive"
    },
    "priority_adjustment": {
      "adjustment_trigger": "changing_priority_requirements",
      "adjustment_scope": "hierarchical_priority_realignment",
      "adjustment_frequency": "continuous"
    }
  }
}
```

## Error Handling

### Planning Construction Failures

```yaml
planning_construction_failures:
  goal_decomposition_failure:
    cause: "Complex goal cannot be properly decomposed"
    recovery: "goal_analysis_with_decomposition_redesign"
    retry_policy: "none"
  
  coordination_failure:
    cause: "Coordination mechanisms fail to integrate properly"
    recovery: "coordination_redesign_with_integration_analysis"
    retry_policy: "immediate_with_coordination_analysis"
  
  resource_allocation_failure:
    cause: "Resource allocation violates constraints or requirements"
    recovery: "resource_analysis_with_allocation_redesign"
    retry_policy: "immediate_with_resource_analysis"
```

### Runtime Planning Issues

```yaml
runtime_planning_issues:
  goal_conflict:
    cause: "Conflicting goals detected across planning levels"
    recovery: "goal_conflict_resolution_with_priority_reassessment"
    retry_policy: "automatic_with_conflict_resolution"
  
  coordination_breakdown:
    cause: "Coordination mechanisms fail during execution"
    recovery: "coordination_recovery_with_mechanism_restart"
    retry_policy: "automatic_with_coordination_recovery"
  
  adaptation_failure:
    cause: "Adaptation mechanisms fail to respond to changes"
    recovery: "adaptation_strategy_redesign_with_manual_intervention"
    retry_policy: "none"
```

## Performance Optimization

### Planning Performance

```yaml
planning_performance:
  execution_optimization: {
    "parallel_planning": "enabled_where_possible",
    "resource_optimization": "enabled",
    "coordination_optimization": "enabled"
  }
  
  scalability_optimization: {
    "horizontal_scaling": "agent_cloning_with_load_balancing",
    "vertical_scaling": "resource_allocation_optimization",
    "performance_scaling": "adaptive_algorithm_optimization"
  }
  
  fault_tolerance: {
    "error_recovery": "automatic_with_state_preservation",
    "graceful_degradation": "enabled",
    "backup_planning": "provisioned_for_critical_operations"
  }
```

### Resource Management

```yaml
resource_management:
  memory_optimization: {
    "memory_pooling": "enabled",
    "garbage_collection": "optimized",
    "memory_monitoring": "continuous"
  }
  
  cpu_optimization: {
    "task_scheduling": "intelligent",
    "parallel_processing": "enabled",
    "resource_allocation": "dynamic"
  }
  
  coordination_optimization: {
    "communication_optimization": "enabled",
    "coordination_efficiency": "optimized",
    "conflict_prevention": "enabled"
  }
```

## Integration Examples

### With Multi-Agent Workflow Generator

```yaml
integration_workflow_generator: {
  "hierarchical_planning": "required_input",
  "workflow_integration": "seamless",
  "performance_alignment": "ensured"
}
```

### With Agent Architecture Designer

```yaml
integration_architecture_designer: {
  "planning_requirements": "required_input",
  "architecture_integration": "seamless",
  "coordination_alignment": "ensured"
}
```

## Best Practices

1. **Goal Consistency**: Maintain consistency across all planning levels
2. **Coordination First**: Always implement comprehensive coordination mechanisms
3. **Adaptation Readiness**: Design for dynamic adaptation to changing conditions
4. **Resource Optimization**: Optimize resource allocation across all levels
5. **Performance Monitoring**: Include comprehensive performance tracking
6. **Conflict Prevention**: Implement proactive conflict prevention mechanisms
7. **Documentation Quality**: Maintain comprehensive planning documentation

## Troubleshooting

### Common Planning Issues

1. **Goal Conflicts**: Implement better goal alignment and conflict resolution
2. **Coordination Breakdowns**: Enhance coordination mechanisms and communication
3. **Resource Conflicts**: Improve resource management and allocation strategies
4. **Adaptation Failures**: Enhance adaptation mechanisms and response strategies
5. **Performance Bottlenecks**: Optimize planning algorithms and resource allocation

### Debug Mode Configuration

```yaml
debug_config: {
  "enabled": true,
  "log_level": "verbose",
  "planning_tracing": true,
  "coordination_monitoring": true,
  "performance_tracking": true
}
```

## Monitoring and Metrics

### Planning Metrics

```yaml
planning_metrics: {
  "planning_efficiency": "planning_speed_and_accuracy",
  "coordination_effectiveness": "coordination_success_rate",
  "resource_utilization": "resource_optimization_percentage",
  "adaptation_responsiveness": "adaptation_response_time"
}
```

### System Health Metrics

```yaml
system_health_metrics: {
  "planning_availability": "percentage",
  "coordination_reliability": "uptime_percentage",
  "resource_efficiency": "cpu_memory_usage_optimization",
  "conflict_resolution_rate": "conflicts_resolved_percentage"
}
```

## Dependencies

- **Multi-Agent Workflow Generator**: For hierarchical planning integration
- **Agent Architecture Designer**: For planning architecture integration
- **Coordination Framework**: For comprehensive coordination mechanisms
- **Resource Management**: For resource allocation optimization
- **Performance Monitoring**: For planning performance tracking

## Version History

- **1.0.0**: Initial release with comprehensive hierarchical planning
- **1.1.0**: Added advanced multi-agent coordination strategies
- **1.2.0**: Enhanced adaptation mechanisms and conflict resolution
- **1.3.0**: Improved performance optimization and monitoring

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.