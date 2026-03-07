---
Domain: orchestration
Version: 1.0.0
Complexity: Very High
Type: Process
Category: Analysis
Estimated Execution Time: 200ms - 5 minutes
name: SKILL.context_health_analyzer
---


## Implementation Notes
To be provided dynamically during execution.

## Description

Implements comprehensive context health analysis to perform deep diagnostics on conversation quality and degradation patterns. This skill uses advanced analytics including embedding drift analysis, needle-in-haystack testing, confidence validation, and trend analysis to provide detailed insights into conversation health. Integrates with Multi-Skill Chaining Engine for complex analysis workflows and provides actionable insights for conversation optimization across the 234-skill empire.

## Purpose

To perform deep context health analysis by:
- Analyzing embedding drift and semantic consistency over time
- Conducting comprehensive needle-in-haystack testing for key fact retention
- Validating response confidence and accuracy patterns
- Identifying degradation trends and patterns in long conversations
- Generating detailed health reports with actionable insights
- Providing optimization recommendations for conversation recovery
- Maintaining conversation quality metrics for continuous improvement

## Capabilities

- **Embedding Drift Analysis**: Analyze semantic similarity changes in key concepts over time
- **Needle-in-Haystack Testing**: Comprehensive testing of key fact recall accuracy
- **Confidence Validation**: Validate response confidence against actual accuracy
- **Trend Analysis**: Identify degradation patterns and trends in conversation quality
- **Health Scoring**: Generate detailed health scores with component breakdowns
- **Recovery Planning**: Create actionable plans for conversation recovery
- **Pattern Recognition**: Identify recurring issues and improvement opportunities
- **Quality Metrics**: Track and analyze conversation quality indicators

## Usage Examples

### Comprehensive Context Health Analysis

```yaml
context_health_analysis:
  conversation_id: "Agency_compliance_review_001"
  analysis_type: "comprehensive_health_check"
  time_range: "last_2_hours"
  
  embedding_drift_analysis: {
    "concept_stability": 0.72,
    "drift_patterns": ["gradual_drift", "sudden_shifts"],
    "affected_concepts": ["regulatory_requirements", "compliance_standards"],
    "drift_severity": "moderate"
  }
  
  needle_testing_results: {
    "total_needles": 15,
    "needles_retrieved": 9,
    "recall_accuracy": 0.60,
    "missed_needles": ["requirement_3", "constraint_7", "guideline_12"],
    "test_confidence": 0.95
  }
  
  confidence_validation: {
    "overconfidence_detected": true,
    "confidence_accuracy_gap": 0.35,
    "fabrication_incidents": 3,
    "validation_score": 0.65
  }
  
  health_score_breakdown: {
    "overall_health": 0.68,
    "semantic_consistency": 0.72,
    "fact_recall": 0.60,
    "response_accuracy": 0.65,
    "trend_direction": "declining"
  }
```

### Trend Analysis and Pattern Recognition

```yaml
trend_analysis: {
  "analysis_period": "24_hours",
  "conversation_phases": [
    {
      "phase": "initial_setup",
      "duration": "30_minutes",
      "health_score": 0.92,
      "stability": "high"
    },
    {
      "phase": "complex_discussion",
      "duration": "90_minutes",
      "health_score": 0.75,
      "stability": "medium"
    },
    {
      "phase": "context_rot_detected",
      "duration": "60_minutes",
      "health_score": 0.45,
      "stability": "low"
    }
  ],
  "degradation_patterns": ["increasing_recency_bias", "semantic_drift_acceleration"],
  "recovery_opportunities": ["immediate_pruning", "gradual_reset"]
}
```

### Recovery Planning

```yaml
recovery_planning: {
  "current_state": "moderate_context_rot",
  "recovery_strategy": "phased_recovery",
  "recovery_phases": [
    {
      "phase": "immediate_stabilization",
      "actions": ["context_pruning", "key_fact_reinforcement"],
      "timeline": "15_minutes",
      "expected_improvement": 0.25
    },
    {
      "phase": "gradual_rebuilding",
      "actions": ["structured_reintroduction", "confidence_monitoring"],
      "timeline": "2_hours",
      "expected_improvement": 0.35
    },
    {
      "phase": "stabilization",
      "actions": ["continuous_monitoring", "preventive_measures"],
      "timeline": "ongoing",
      "expected_improvement": 0.15
    }
  ]
}
```

## Input Format

### Health Analysis Request

```yaml
health_analysis_request:
  conversation_id: string
  analysis_scope: string             # "comprehensive|focused|trend_analysis"
  time_range: object
  analysis_depth: string             # "light|medium|deep|comprehensive"
  
  analysis_components: {
    "embedding_drift": boolean,
    "needle_testing": boolean,
    "confidence_validation": boolean,
    "trend_analysis": boolean,
    "pattern_recognition": boolean
  }
  
  conversation_context: {
    "topic_domains": array,
    "complexity_level": string,
    "criticality_level": string,
    "expected_duration": string
  }
```

### Deep Analysis Configuration

```yaml
deep_analysis_config:
  analysis_type: string              # "embedding_drift|needle_testing|confidence_validation"
  parameters: object
  validation_criteria: object
  
  analysis_strategy: {
    "sampling_method": string,
    "confidence_threshold": number,
    "error_tolerance": number
  }
```

## Output Format

### Comprehensive Health Report

```yaml
comprehensive_health_report:
  report_id: string
  analysis_timestamp: timestamp
  conversation_id: string
  analysis_scope: string
  
  overall_health_score: number       # 0.0 to 1.0
  health_trend: string               # "improving|stable|declining"
  stability_assessment: string       # "high|medium|low"
  
  component_analysis: {
    "semantic_consistency": {
      "score": number,
      "trend": string,
      "issues": array,
      "recommendations": array
    },
    "fact_recall_accuracy": {
      "score": number,
      "trend": string,
      "missed_facts": array,
      "reinforcement_needed": boolean
    },
    "response_confidence": {
      "score": number,
      "overconfidence_level": number,
      "fabrication_incidents": number,
      "validation_required": boolean
    },
    "context_utilization": {
      "score": number,
      "token_pressure": number,
      "efficiency_rating": string,
      "optimization_opportunities": array
    }
  }
  
  actionable_insights: [
    {
      "insight_type": string,
      "description": string,
      "priority": string,
      "recommended_action": string,
      "expected_impact": string
    }
  ]
```

### Trend Analysis Report

```yaml
trend_analysis_report:
  analysis_period: object
  trend_direction: string            # "positive|neutral|negative"
  trend_velocity: string             # "slow|moderate|rapid"
  
  phase_analysis: [
    {
      "phase_name": string,
      "start_time": timestamp,
      "end_time": timestamp,
      "health_score": number,
      "key_events": array,
      "stability_level": string
    }
  ]
  
  degradation_patterns: [
    {
      "pattern_type": string,
      "onset_time": timestamp,
      "severity_progression": array,
      "triggering_events": array,
      "mitigation_effectiveness": string
    }
  ]
  
  recovery_opportunities: [
    {
      "opportunity_type": string,
      "timing": string,
      "required_actions": array,
      "success_probability": number,
      "implementation_complexity": string
    }
  ]
```

## Configuration Options

### Analysis Strategies

```yaml
analysis_strategies:
  comprehensive_analysis:
    description: "Full analysis across all components"
    use_case: "critical_conversations"
    complexity: "very_high"
    accuracy: "maximum"
  
  focused_analysis:
    description: "Targeted analysis of specific issues"
    use_case: "problematic_conversations"
    complexity: "medium"
    accuracy: "high"
  
  trend_analysis:
    description: "Historical trend and pattern analysis"
    use_case: "long_term_monitoring"
    complexity: "high"
    accuracy: "adaptive"
  
  real_time_analysis:
    description: "Continuous monitoring and analysis"
    use_case: "live_conversations"
    complexity: "medium"
    accuracy: "balanced"
```

### Analysis Depth Levels

```yaml
analysis_depth_levels:
  light: {
    "description": "Basic health check with key metrics",
    "components": ["overall_health", "major_issues"],
    "processing_time": "under_30_seconds",
    "resource_usage": "minimal"
  }
  
  medium: {
    "description": "Moderate analysis with trend identification",
    "components": ["comprehensive_metrics", "trend_analysis"],
    "processing_time": "1-2_minutes",
    "resource_usage": "moderate"
  }
  
  deep: {
    "description": "Detailed analysis with pattern recognition",
    "components": ["all_components", "pattern_analysis", "recovery_planning"],
    "processing_time": "3-5_minutes",
    "resource_usage": "high"
  }
  
  comprehensive: {
    "description": "Full analysis with machine learning insights",
    "components": ["all_analysis_types", "predictive_modeling"],
    "processing_time": "5-10_minutes",
    "resource_usage": "very_high"
  }
```

## Constraints

- **Analysis Accuracy**: Must maintain >90% accuracy in health scoring
- **Processing Time**: Must complete within specified time limits for each depth level
- **Resource Efficiency**: Must optimize resource usage for long conversations
- **Data Privacy**: Must not expose sensitive conversation content in analysis results
- **Integration Requirements**: Must integrate seamlessly with existing MCP skills
- **Scalability**: Must handle conversations with extensive history and complexity
- **Validation Standards**: Must validate all analysis results with appropriate confidence levels

## Examples

### Agency Compliance Conversation Analysis

```yaml
Agency_conversation_analysis: {
  "conversation_type": "Agency_compliance_review",
  "analysis_scope": "comprehensive",
  "overall_health_score": 0.62,
  "key_issues": ["semantic_drift_in_regulatory_terms", "fact_recall_degradation"],
  "recovery_strategy": "immediate_pruning_with_gradual_rebuilding",
  "success_probability": 0.78
}
```

### Technical Architecture Discussion Analysis

```yaml
architecture_analysis: {
  "conversation_type": "technical_architecture_design",
  "complexity_level": "very_high",
  "health_score": 0.75,
  "stability": "medium",
  "degradation_patterns": ["increasing_complexity_confusion"],
  "optimization_recommendations": ["structured_summarization", "key_concept_reinforcement"]
}
```

## Error Handling

### Analysis Failures

```yaml
analysis_failures:
  embedding_analysis_failure:
    cause: "Embedding calculation or comparison failed"
    recovery: "use_alternative_similarity_metrics_or_reduce_analysis_scope"
    retry_policy: "immediate_with_fallback_method"
  
  needle_testing_failure:
    cause: "Needle-in-haystack testing could not be completed"
    recovery: "reduce_needle_count_or_use_sampling_technique"
    retry_policy: "immediate_with_reduced_scope"
  
  confidence_validation_failure:
    cause: "Confidence validation algorithms failed"
    recovery: "use_historical_accuracy_data_or_manual_validation"
    retry_policy: "immediate_with_estimated_values"
  
  trend_analysis_failure:
    cause: "Trend analysis could not identify clear patterns"
    recovery: "extend_analysis_period_or_use_alternative_metrics"
    retry_policy: "immediate_with_extended_data"
```

### Data Quality Issues

```yaml
data_quality_issues:
  insufficient_data:
    cause: "Not enough conversation data for comprehensive analysis"
    recovery: "extend_analysis_period_or_use_lighter_analysis_depth"
    retry_policy: "immediate_with_adjusted_scope"
  
  inconsistent_data:
    cause: "Conversation data contains inconsistencies or errors"
    recovery: "data_cleaning_or_manual_review_required"
    retry_policy: "manual_intervention_required"
  
  corrupted_data:
    cause: "Conversation data is corrupted or incomplete"
    recovery: "use_backup_data_or_restart_conversation"
    retry_policy: "immediate_with_data_recovery"
```

## Performance Optimization

### Analysis Optimization

```yaml
analysis_optimization:
  optimization_frequency: "per_analysis"
  optimization_targets: [
    "analysis_accuracy",
    "processing_time",
    "resource_utilization",
    "result_reliability"
  ]
  
  optimization_algorithms: {
    "embedding_analysis": "optimized_similarity_algorithms",
    "needle_testing": "intelligent_sampling_techniques",
    "trend_analysis": "machine_learning_based_detection",
    "pattern_recognition": "neural_network_classification"
  }
```

### Resource Management

```yaml
resource_management:
  resource_monitoring: {
    "analysis_overhead": "tracked",
    "memory_consumption": "optimized",
    "processing_time": "monitored"
  }
  
  optimization_strategies: {
    "data_compression": "enabled_for_large_conversations",
    "caching_strategy": "intelligent_caching",
    "parallel_processing": "selective_parallelization"
  }
```

## Integration Examples

### With Multi-Skill Chaining Engine

```yaml
integration_chaining_engine: {
  "complex_analysis_workflows": "enabled",
  "skill_coordination": "automatic",
  "result_aggregation": "comprehensive",
  "performance_optimization": "coordinated"
}
```

### With Context Rot Detector

```yaml
integration_rot_detector: {
  "early_warning_integration": "real_time",
  "detection_result_validation": "automatic",
  "comprehensive_analysis_triggers": "coordinated",
  "health_scoring": "integrated"
}
```

## Best Practices

1. **Comprehensive Analysis**: Use comprehensive analysis for critical conversations
2. **Trend Monitoring**: Regularly monitor trends to catch degradation early
3. **Pattern Recognition**: Use pattern recognition to identify recurring issues
4. **Recovery Planning**: Always create actionable recovery plans for degraded conversations
5. **Integration Testing**: Test integration with all related MCP skills
6. **Performance Monitoring**: Continuously monitor analysis performance and accuracy
7. **Documentation**: Maintain clear documentation of analysis methodologies and results

## Troubleshooting

### Common Analysis Issues

1. **Inconsistent Results**: Standardize analysis parameters and validate data quality
2. **Slow Analysis**: Implement sampling strategies for long conversations
3. **High Resource Usage**: Optimize analysis algorithms and implement caching
4. **Integration Failures**: Check MCP skill communication protocols and data formats
5. **Poor Accuracy**: Review and refine analysis algorithms and validation criteria

### Debug Mode Configuration

```yaml
debug_config: {
  "enabled": true,
  "log_level": "detailed",
  "analysis_tracing": true,
  "performance_debugging": true,
  "data_validation_debugging": true
}
```

## Monitoring and Metrics

### Analysis Performance Metrics

```yaml
analysis_metrics: {
  "analysis_accuracy": "percentage",
  "processing_time": "milliseconds",
  "resource_utilization": "percentage",
  "result_reliability": "score"
}
```

### Health Analysis Indicators

```yaml
health_analysis_indicators: {
  "average_health_score": "score",
  "analysis_frequency": "count_per_hour",
  "recovery_success_rate": "percentage",
  "trend_prediction_accuracy": "percentage"
}
```

## Dependencies

- **Context Rot Detector**: For early warning integration and detection result validation
- **Multi-Skill Chaining Engine**: For complex analysis workflows and skill coordination
- **Empire Health Monitor**: For comprehensive health scoring and trend analysis
- **Skill Registry**: For skill metadata and availability information
- **Data Storage**: For accessing conversation history and analysis data

## Version History

- **1.0.0**: Initial release with basic health analysis and trend identification
- **1.1.0**: Added embedding drift analysis and needle-in-haystack testing
- **1.2.0**: Enhanced pattern recognition and recovery planning capabilities
- **1.3.0**: Real-time analysis and machine learning integration
- **1.4.0**: Advanced predictive modeling and comprehensive metrics

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.