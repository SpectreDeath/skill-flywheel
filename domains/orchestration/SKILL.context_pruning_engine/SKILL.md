---
Domain: orchestration
Version: 1.0.0
Complexity: High
Type: Process
Category: Optimization
Estimated Execution Time: 100ms - 3 minutes
name: SKILL.context_pruning_engine
---


## Implementation Notes
To be provided dynamically during execution.

## Description

Implements intelligent context pruning to optimize conversation efficiency while preserving critical information. This skill analyzes conversation history to identify and remove irrelevant turns, implements essential bracketing techniques, ensures source citation integrity, and maintains conversation coherence. Uses advanced algorithms to balance context compression with information preservation, integrating with MCP Load Balancer for resource optimization across the 234-skill empire.

## Purpose

To optimize conversation context by:
- Identifying and removing irrelevant conversation turns and redundant information
- Implementing essential bracketing to preserve critical context at conversation boundaries
- Ensuring source citation integrity during context compression
- Maintaining conversation coherence and logical flow after pruning
- Optimizing resource usage through intelligent context management
- Balancing context compression with information preservation
- Enabling efficient long-term conversation management

## Capabilities

- **Irrelevant Turn Detection**: Identify and remove conversation turns that no longer contribute value
- **Essential Bracketing**: Preserve critical information at conversation start and end points
- **Source Citation Management**: Maintain citation integrity during context compression
- **Coherence Preservation**: Ensure logical flow and context continuity after pruning
- **Resource Optimization**: Reduce context overhead while maintaining conversation quality
- **Compression Analysis**: Analyze compression effectiveness and information retention
- **Recovery Mechanisms**: Provide ability to restore pruned context when needed
- **Adaptive Pruning**: Adjust pruning strategies based on conversation type and criticality

## Usage Examples

### Basic Context Pruning

```yaml
context_pruning_request:
  conversation_history: [
    {"role": "user", "content": "Initial query about project requirements", "timestamp": "2024-01-01T10:00:00Z"},
    {"role": "assistant", "content": "Detailed response with technical specifications", "timestamp": "2024-01-01T10:05:00Z"},
    {"role": "user", "content": "Irrelevant follow-up question about unrelated topic", "timestamp": "2024-01-01T10:10:00Z"},
    {"role": "assistant", "content": "Response to irrelevant question", "timestamp": "2024-01-01T10:15:00Z"},
    {"role": "user", "content": "Return to original topic with new question", "timestamp": "2024-01-01T10:20:00Z"}
  ]
  pruning_strategy: "conservative"
  preservation_requirements: ["key_decisions", "technical_specifications", "user_requirements"]
  
  pruning_results: {
    "original_length": 5,
    "pruned_length": 3,
    "compression_ratio": 0.40,
    "preserved_content": ["initial_query", "technical_specifications", "current_question"],
    "removed_content": ["irrelevant_follow_up", "response_to_irrelevant"]
  }
```

### Advanced Context Optimization

```yaml
advanced_context_optimization:
  optimization_strategy: "adaptive_pruning_with_bracketing"
  context_analysis: {
    "relevance_scores": [0.95, 0.88, 0.25, 0.30, 0.92],
    "criticality_assessment": ["high", "high", "low", "low", "high"],
    "coherence_impact": ["minimal", "minimal", "none", "none", "minimal"]
  }
  
  bracketing_strategy: {
    "essential_start": ["initial_requirements", "key_constraints"],
    "essential_end": ["current_state", "immediate_needs"],
    "preservation_priority": "high"
  }
  
  optimization_metrics: {
    "token_reduction": 0.35,
    "information_retention": 0.92,
    "coherence_score": 0.95,
    "resource_savings": "significant"
  }
```

### Source Citation Preservation

```yaml
citation_preservation: {
  "original_citations": [
    {"source": "user_requirement_1", "content": "Need real-time processing"},
    {"source": "technical_spec_3", "content": "API must support JSON"},
    {"source": "irrelevant_discussion", "content": "Off-topic conversation"}
  ],
  "preserved_citations": [
    {"source": "user_requirement_1", "content": "Need real-time processing", "status": "preserved"},
    {"source": "technical_spec_3", "content": "API must support JSON", "status": "preserved"}
  ],
  "removed_citations": [
    {"source": "irrelevant_discussion", "content": "Off-topic conversation", "status": "removed", "reason": "low_relevance"}
  ],
  "citation_integrity": "maintained"
}
```

## Input Format

### Context Pruning Request

```yaml
context_pruning_request:
  conversation_history: array        # Array of message objects with metadata
  pruning_strategy: string           # "conservative|moderate|aggressive|adaptive"
  preservation_requirements: array   # Critical content that must be preserved
  compression_target: number         # Target compression ratio (0.0 to 1.0)
  
  analysis_parameters: {
    "relevance_threshold": number,
    "criticality_weight": number,
    "coherence_weight": number,
    "citation_preservation": boolean
  }
  
  conversation_metadata: {
    "conversation_id": string,
    "total_tokens": number,
    "complexity_level": string,
    "criticality_level": string
  }
```

### Pruning Configuration

```yaml
pruning_config:
  strategy: string                   # "irrelevant_removal|bracketing_only|full_optimization"
  parameters: object
  constraints: object
  
  preservation_rules: {
    "always_preserve": array,
    "never_remove": array,
    "conditional_preservation": array
  }
```

## Output Format

### Pruning Results Report

```yaml
pruning_results_report:
  report_id: string
  pruning_timestamp: timestamp
  conversation_id: string
  pruning_strategy: string
  
  before_pruning: {
    "message_count": number,
    "token_count": number,
    "citation_count": number,
    "complexity_score": number
  }
  
  after_pruning: {
    "message_count": number,
    "token_count": number,
    "citation_count": number,
    "complexity_score": number
  }
  
  preservation_metrics: {
    "compression_ratio": number,
    "information_retention": number,
    "coherence_score": number,
    "citation_integrity": string
  }
  
  removed_content: [
    {
      "message_id": string,
      "removal_reason": string,
      "impact_assessment": string,
      "recovery_possible": boolean
    }
  ]
  
  preserved_content: [
    {
      "content_type": string,
      "preservation_reason": string,
      "criticality_level": string,
      "citation_status": string
    }
  ]
```

### Optimization Summary

```yaml
optimization_summary:
  optimization_type: string          # "token_reduction|coherence_improvement|resource_optimization"
  optimization_metrics: object
  quality_assurance: object
  
  performance_impact: {
    "processing_time": number,
    "resource_savings": string,
    "conversation_improvement": string
  }
  
  recommendations: [
    {
      "recommendation_type": string,
      "description": string,
      "priority": string,
      "expected_benefit": string
    }
  ]
```

## Configuration Options

### Pruning Strategies

```yaml
pruning_strategies:
  conservative: {
    "description": "Minimal pruning with maximum preservation",
    "use_case": "critical_conversations",
    "compression_target": 0.10,
    "preservation_priority": "maximum"
  }
  
  moderate: {
    "description": "Balanced pruning with good preservation",
    "use_case": "standard_conversations",
    "compression_target": 0.30,
    "preservation_priority": "high"
  }
  
  aggressive: {
    "description": "Maximum compression with essential preservation",
    "use_case": "long_conversations",
    "compression_target": 0.60,
    "preservation_priority": "essential_only"
  }
  
  adaptive: {
    "description": "Dynamic pruning based on conversation analysis",
    "use_case": "intelligent_optimization",
    "compression_target": "adaptive",
    "preservation_priority": "context_aware"
  }
```

### Preservation Rules

```yaml
preservation_rules:
  always_preserve: [
    "initial_requirements",
    "key_decisions",
    "technical_specifications",
    "user_constraints",
    "critical_definitions"
  ]
  
  never_remove: [
    "source_citations",
    "user_identified_critical_info",
    "recent_context",
    "active_discussion_topics"
  ]
  
  conditional_preservation: [
    {
      "condition": "complexity_high",
      "preserve": ["detailed_explanations", "step_by_step_instructions"]
    },
    {
      "condition": "criticality_critical",
      "preserve": ["all_technical_details", "all_user_requirements"]
    }
  ]
```

## Constraints

- **Information Integrity**: Must preserve all critical information and context
- **Citation Preservation**: Must maintain source citation integrity during pruning
- **Coherence Maintenance**: Must ensure logical flow after context removal
- **Recovery Capability**: Must enable restoration of pruned context when needed
- **Performance Requirements**: Must complete pruning within reasonable time limits
- **Resource Efficiency**: Must provide meaningful resource savings
- **User Control**: Must respect user-defined preservation requirements

## Examples

### FDA Compliance Conversation Pruning

```yaml
fda_conversation_pruning: {
  "conversation_type": "fda_compliance_review",
  "pruning_strategy": "conservative",
  "compression_ratio": 0.15,
  "information_retention": 0.98,
  "preserved_content": ["regulatory_requirements", "compliance_standards", "user_specifications"],
  "removed_content": ["administrative_exchanges", "clarification_requests"]
}
```

### Technical Architecture Discussion Pruning

```yaml
architecture_pruning: {
  "conversation_type": "technical_architecture_design",
  "pruning_strategy": "moderate",
  "compression_ratio": 0.35,
  "information_retention": 0.92,
  "preserved_content": ["architecture_decisions", "technical_constraints", "implementation_details"],
  "removed_content": ["exploratory_discussions", "alternative_approach_analysis"]
}
```

## Error Handling

### Pruning Failures

```yaml
pruning_failures:
  analysis_failure:
    cause: "Context analysis could not be completed"
    recovery: "use_alternative_analysis_method_or_manual_review"
    retry_policy: "immediate_with_fallback_method"
  
  preservation_violation:
    cause: "Pruning would violate preservation requirements"
    recovery: "adjust_pruning_strategy_or_preservation_rules"
    retry_policy: "immediate_with_rule_adjustment"
  
  coherence_loss:
    cause: "Pruning would break conversation coherence"
    recovery: "reduce_pruning_aggressiveness_or_add_transition_content"
    retry_policy: "immediate_with_strategy_adjustment"
  
  citation_corruption:
    cause: "Pruning would corrupt source citations"
    recovery: "preserve_citation_context_or_use_citation_reconstruction"
    retry_policy: "immediate_with_citation_protection"
```

### Recovery Scenarios

```yaml
recovery_scenarios:
  partial_recovery_needed:
    cause: "Some pruned content is required for current discussion"
    recovery: "selective_restoration_of_specific_content"
    retry_policy: "immediate_with_targeted_recovery"
  
  full_recovery_needed:
    cause: "Pruning was too aggressive and context is lost"
    recovery: "restore_full_context_from_backup_or_history"
    retry_policy: "immediate_with_full_restoration"
  
  citation_recovery_needed:
    cause: "Source citations were lost during pruning"
    recovery: "reconstruct_citations_from_context_or_external_sources"
    retry_policy: "immediate_with_citation_reconstruction"
```

## Performance Optimization

### Pruning Optimization

```yaml
pruning_optimization:
  optimization_frequency: "per_pruning_operation"
  optimization_targets: [
    "compression_efficiency",
    "information_retention",
    "processing_speed",
    "coherence_maintenance"
  ]
  
  optimization_algorithms: {
    "relevance_analysis": "machine_learning_based",
    "criticality_assessment": "rule_based_with_ml_enhancement",
    "coherence_analysis": "graph_based_algorithms",
    "citation_tracking": "reference_graph_analysis"
  }
```

### Resource Management

```yaml
resource_management:
  resource_monitoring: {
    "pruning_overhead": "tracked",
    "memory_usage": "optimized",
    "processing_time": "monitored"
  }
  
  optimization_strategies: {
    "incremental_pruning": "enabled_for_long_conversations",
    "batch_processing": "selective_for_efficiency",
    "caching_strategy": "intelligent_caching_of_analysis_results"
  }
```

## Integration Examples

### With MCP Load Balancer

```yaml
integration_mcp_balancer: {
  "context_load_optimization": "aware",
  "resource_allocation": "pruning_aware",
  "performance_monitoring": "integrated",
  "skill_routing": "context_optimized"
}
```

### With Context Health Analyzer

```yaml
integration_health_analyzer: {
  "health_assessment_integration": "real_time",
  "pruning_trigger_conditions": "coordinated",
  "optimization_validation": "automatic",
  "recovery_monitoring": "continuous"
}
```

## Best Practices

1. **Conservative Approach**: Start with conservative pruning and increase aggressiveness gradually
2. **Preservation Priority**: Always prioritize preservation of critical information and citations
3. **Coherence Check**: Verify conversation coherence after each pruning operation
4. **Recovery Planning**: Always maintain ability to restore pruned context when needed
5. **Integration Testing**: Test integration with all related MCP skills
6. **Performance Monitoring**: Continuously monitor pruning performance and effectiveness
7. **User Feedback**: Incorporate user feedback to improve pruning strategies

## Troubleshooting

### Common Pruning Issues

1. **Over-Pruning**: Adjust pruning strategy to be more conservative and increase preservation requirements
2. **Coherence Loss**: Implement transition content or reduce pruning aggressiveness
3. **Citation Loss**: Enhance citation tracking and implement citation reconstruction mechanisms
4. **Performance Issues**: Optimize analysis algorithms and implement caching strategies
5. **Integration Failures**: Check MCP skill communication protocols and data formats

### Debug Mode Configuration

```yaml
debug_config: {
  "enabled": true,
  "log_level": "detailed",
  "pruning_tracing": true,
  "analysis_debugging": true,
  "recovery_debugging": true
}
```

## Monitoring and Metrics

### Pruning Performance Metrics

```yaml
pruning_metrics: {
  "compression_ratio": "percentage",
  "information_retention": "percentage",
  "processing_time": "milliseconds",
  "coherence_score": "score"
}
```

### Optimization Indicators

```yaml
optimization_indicators: {
  "average_compression": "percentage",
  "pruning_frequency": "count_per_hour",
  "recovery_success_rate": "percentage",
  "user_satisfaction": "score"
}
```

## Dependencies

- **Context Health Analyzer**: For health assessment and pruning trigger conditions
- **MCP Load Balancer**: For context-aware resource optimization and skill routing
- **Empire Health Monitor**: For conversation health monitoring and optimization validation
- **Skill Registry**: For skill metadata and availability information
- **Data Storage**: For accessing conversation history and backup restoration

## Version History

- **1.0.0**: Initial release with basic context pruning and preservation rules
- **1.1.0**: Added essential bracketing and citation preservation capabilities
- **1.2.0**: Enhanced coherence preservation and adaptive pruning strategies
- **1.3.0**: Real-time pruning optimization and recovery mechanisms
- **1.4.0**: Advanced machine learning integration and comprehensive metrics

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.