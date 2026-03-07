---
Domain: orchestration
Version: 1.0.0
Complexity: High
Type: Process
Category: Monitoring
Estimated Execution Time: 50ms - 2 minutes
name: SKILL.context_rot_detector
---


## Implementation Notes
To be provided dynamically during execution.

## Description

Implements real-time context rot detection to identify and analyze degradation in LLM conversation quality. This skill monitors key metrics including token pressure, U-shape bias, recency bias, semantic drift, confidence fabrication, and needle miss rates. Uses advanced pattern recognition and statistical analysis to detect early signs of context rot before they impact conversation effectiveness. Integrates with Empire Health Monitor for comprehensive conversation health scoring.

## Purpose

To detect and analyze context rot in real-time by:
- Monitoring conversation token pressure and window utilization
- Identifying U-shape bias patterns (ignoring middle context)
- Detecting recency bias (over-weighting recent tokens)
- Analyzing semantic drift in definitions and concepts
- Identifying confidence fabrication (plausible wrong answers)
- Measuring needle miss rates for key fact recall
- Providing actionable recommendations for context optimization
- Maintaining conversation quality across long multi-turn interactions

## Capabilities

- **Token Pressure Analysis**: Monitor context window utilization and pressure points
- **Bias Detection**: Identify U-shape and recency bias patterns in responses
- **Semantic Drift Monitoring**: Track definition and concept consistency over time
- **Confidence Validation**: Detect overconfident but incorrect responses
- **Needle-in-Haystack Testing**: Measure key fact recall accuracy
- **Rot Scoring**: Generate comprehensive context rot scores (0.0-1.0)
- **Symptom Identification**: Pinpoint specific context rot symptoms
- **Recommendation Engine**: Provide actionable optimization recommendations

## Usage Examples

### Basic Context Rot Detection

```yaml
context_rot_detection:
  conversation_history: [
    {"role": "user", "content": "Initial query about project requirements"},
    {"role": "assistant", "content": "Detailed response with technical specifications"},
    {"role": "user", "content": "Follow-up question about implementation details"},
    {"role": "assistant", "content": "Response that may show signs of context rot"}
  ]
  current_token_count: 12500
  max_context_window: 16000
  
  detection_results: {
    "rot_score": 0.35,
    "symptoms": ["recency_bias", "semantic_drift"],
    "recommendation": "prune",
    "confidence": 0.82
  }
```

### Advanced Context Analysis

```yaml
advanced_context_analysis:
  conversation_metrics: {
    "token_utilization": 0.78,
    "message_count": 25,
    "conversation_duration": "45_minutes",
    "topic_complexity": "high"
  }
  
  bias_analysis: {
    "u_shape_bias": {
      "detected": true,
      "severity": 0.65,
      "impact": "medium"
    },
    "recency_bias": {
      "detected": true,
      "severity": 0.82,
      "impact": "high"
    }
  }
  
  semantic_consistency: {
    "term_drift_detected": true,
    "drift_terms": ["API", "integration", "deployment"],
    "consistency_score": 0.72
  }
```

### Needle-in-Haystack Testing

```yaml
needle_testing: {
  "test_type": "key_fact_recall",
  "needles_inserted": 5,
  "needles_retrieved": 3,
  "recall_accuracy": 0.60,
  "missed_needles": ["initial_requirement_3", "constraint_7"],
  "test_confidence": 0.95
}
```

## Input Format

### Context Rot Detection Request

```yaml
context_rot_request:
  conversation_history: array        # Array of message objects
  current_token_count: number        # Current context window usage
  max_context_window: number         # Maximum context window size
  detection_sensitivity: string      # "low|medium|high|critical"
  
  analysis_parameters: {
    "include_bias_detection": boolean,
    "include_semantic_analysis": boolean,
    "include_needle_testing": boolean,
    "include_confidence_validation": boolean
  }
  
  conversation_metadata: {
    "conversation_id": string,
    "start_time": timestamp,
    "topic_domains": array,
    "complexity_level": string
  }
```

### Real-time Monitoring Configuration

```yaml
monitoring_config:
  monitoring_frequency: string       # "real_time|per_message|periodic"
  alert_thresholds: object
  sensitivity_levels: object
  
  detection_rules: {
    "token_pressure_threshold": 0.80,
    "bias_detection_enabled": true,
    "semantic_drift_threshold": 0.25,
    "confidence_fabrication_threshold": 0.70
  }
```

## Output Format

### Context Rot Detection Report

```yaml
context_rot_report:
  detection_timestamp: timestamp
  conversation_id: string
  rot_score: number                  # 0.0 (healthy) to 1.0 (severe rot)
  rot_level: string                  # "healthy|warning|critical|severe"
  confidence: number                 # Detection confidence (0.0-1.0)
  
  detected_symptoms: [
    {
      "symptom_type": string,
      "severity": number,
      "evidence": array,
      "impact_level": string
    }
  ]
  
  conversation_metrics: {
    "token_pressure": number,
    "message_count": number,
    "semantic_consistency": number,
    "recall_accuracy": number
  }
  
  recommendations: [
    {
      "action": string,              # "prune|reset|summarize"
      "priority": string,            # "low|medium|high|critical"
      "description": string,
      "expected_impact": string
    }
  ]
```

### Real-time Monitoring Alert

```yaml
monitoring_alert:
  alert_id: string
  alert_type: string                 # "token_pressure|bias_detected|semantic_drift"
  severity: string                   # "warning|critical|emergency"
  timestamp: timestamp
  
  alert_details: {
    "metric_value": number,
    "threshold_exceeded": number,
    "trend_direction": string,
    "affected_components": array
  }
  
  immediate_actions: [
    {
      "action_type": string,
      "description": string,
      "execution_required": boolean
    }
  ]
```

## Configuration Options

### Detection Strategies

```yaml
detection_strategies:
  real_time_monitoring:
    description: "Continuous monitoring with immediate alerts"
    use_case: "long_conversations"
    frequency: "per_message"
    latency: "under_100ms"
  
  batch_analysis:
    description: "Periodic comprehensive analysis"
    use_case: "conversation_review"
    frequency: "every_10_messages"
    latency: "under_500ms"
  
  predictive_detection:
    description: "Predict context rot before it occurs"
    use_case: "proactive_optimization"
    frequency: "adaptive"
    latency: "under_200ms"
```

### Sensitivity Levels

```yaml
sensitivity_levels:
  low: {
    "description": "Conservative detection, fewer false positives",
    "token_pressure_threshold": 0.90,
    "bias_detection_sensitivity": 0.80,
    "semantic_drift_threshold": 0.35
  }
  
  medium: {
    "description": "Balanced detection and accuracy",
    "token_pressure_threshold": 0.80,
    "bias_detection_sensitivity": 0.60,
    "semantic_drift_threshold": 0.25
  }
  
  high: {
    "description": "Aggressive detection, catches early signs",
    "token_pressure_threshold": 0.70,
    "bias_detection_sensitivity": 0.40,
    "semantic_drift_threshold": 0.15
  }
  
  critical: {
    "description": "Maximum sensitivity for critical conversations",
    "token_pressure_threshold": 0.60,
    "bias_detection_sensitivity": 0.20,
    "semantic_drift_threshold": 0.10
  }
```

## Constraints

- **Performance Requirements**: Must complete detection within 2 seconds for real-time use
- **Accuracy Standards**: Must maintain >85% accuracy in rot detection
- **Resource Efficiency**: Must not significantly impact conversation performance
- **False Positive Limits**: Must keep false positive rate below 10%
- **Integration Compatibility**: Must integrate seamlessly with existing MCP skills
- **Privacy Compliance**: Must not expose sensitive conversation content
- **Scalability**: Must handle conversations with 1000+ messages

## Examples

### Agency Compliance Conversation

```yaml
Agency_conversation_monitoring: {
  "conversation_type": "Agency_compliance_review",
  "message_count": 150,
  "token_utilization": 0.85,
  "rot_score": 0.45,
  "detected_issues": ["recency_bias", "semantic_drift"],
  "recommendation": "summarize_and_prune",
  "immediate_action_required": false
}
```

### Technical Architecture Discussion

```yaml
architecture_discussion: {
  "conversation_type": "technical_architecture",
  "complexity_level": "very_high",
  "rot_score": 0.25,
  "symptoms": ["minor_recency_bias"],
  "recommendation": "monitor_closely",
  "next_check_in": "10_messages"
}
```

## Error Handling

### Detection Failures

```yaml
detection_failures:
  analysis_timeout:
    cause: "Context analysis exceeded time limit"
    recovery: "reduce_analysis_depth_or_use_sampling"
    retry_policy: "immediate_with_reduced_scope"
  
  insufficient_context:
    cause: "Not enough conversation history for analysis"
    recovery: "collect_more_context_or_use_alternative_metrics"
    retry_policy: "queue_for_later_analysis"
  
  metric_calculation_error:
    cause: "Error calculating specific metrics"
    recovery: "use_estimated_values_or_skip_problematic_metrics"
    retry_policy: "immediate_with_fallback_metrics"
  
  integration_failure:
    cause: "Failure to integrate with other MCP skills"
    recovery: "use_standalone_mode_or_manual_integration"
    retry_policy: "immediate_with_fallback_mode"
```

### False Positive Handling

```yaml
false_positive_handling:
  high_confidence_false_positive:
    cause: "System incorrectly detected context rot"
    recovery: "manual_review_and_threshold_adjustment"
    retry_policy: "manual_intervention_required"
  
  recurring_false_positives:
    cause: "System consistently generating false positives"
    recovery: "retrain_detection_algorithms_or_adjust_sensitivity"
    retry_policy: "scheduled_with_algorithm_update"
```

## Performance Optimization

### Real-time Processing

```yaml
real_time_optimization:
  processing_frequency: "per_message"
  batch_size: 1
  parallel_processing: false
  caching_strategy: "conversation_level"
  
  performance_targets: {
    "detection_latency": "under_200ms",
    "analysis_accuracy": "above_85%",
    "resource_usage": "minimal_impact"
  }
```

### Scalability Considerations

```yaml
scalability_config:
  conversation_size: "1000+ messages"
  concurrent_analyses: 10
  data_retention: "conversation_duration"
  memory_optimization: "enabled"
  
  scaling_triggers: {
    "message_count_500": "enable_sampling",
    "message_count_1000": "enable_streaming_analysis",
    "rot_score_0.8": "increase_monitoring_frequency"
  }
```

## Integration Examples

### With Empire Health Monitor

```yaml
integration_health_monitor: {
  "health_data_sharing": "real_time_metrics",
  "alert_forwarding": true,
  "coordinated_optimization": true,
  "conversation_health_scoring": "integrated"
}
```

### With MCP Load Balancer

```yaml
integration_mcp_balancer: {
  "context_load_distribution": "aware",
  "skill_routing": "context_health_aware",
  "performance_optimization": "context_optimized",
  "resource_allocation": "conversation_health_based"
}
```

## Best Practices

1. **Early Detection**: Monitor for context rot from the beginning of conversations
2. **Gradual Escalation**: Increase monitoring frequency as rot score increases
3. **Actionable Recommendations**: Always provide specific, actionable recommendations
4. **Integration Testing**: Test integration with all existing MCP skills
5. **Performance Monitoring**: Continuously monitor detection performance and accuracy
6. **Threshold Tuning**: Adjust sensitivity thresholds based on conversation type
7. **Documentation**: Maintain clear documentation of detection algorithms and thresholds

## Troubleshooting

### Common Detection Issues

1. **High False Positive Rate**: Adjust sensitivity thresholds and review detection algorithms
2. **Slow Detection**: Implement sampling strategies for long conversations
3. **Inconsistent Results**: Standardize detection parameters and algorithms
4. **Integration Failures**: Check MCP skill communication protocols
5. **Resource Consumption**: Optimize analysis algorithms and caching strategies

### Debug Mode Configuration

```yaml
debug_config: {
  "enabled": true,
  "log_level": "detailed",
  "context_tracing": true,
  "detection_debugging": true,
  "performance_debugging": true
}
```

## Monitoring and Metrics

### Detection Performance Metrics

```yaml
detection_metrics: {
  "detection_accuracy": "percentage",
  "false_positive_rate": "percentage",
  "detection_latency": "milliseconds",
  "resource_utilization": "percentage"
}
```

### Context Health Indicators

```yaml
context_health_indicators: {
  "average_rot_score": "score",
  "detection_frequency": "count_per_hour",
  "recommendation_effectiveness": "percentage",
  "conversation_recovery_rate": "percentage"
}
```

## Dependencies

- **Empire Health Monitor**: For conversation health scoring and alert integration
- **MCP Load Balancer**: For context-aware skill routing and resource optimization
- **Multi-Skill Chaining Engine**: For complex context analysis workflows
- **Skill Registry**: For skill metadata and availability information
- **Conversation Storage**: For accessing conversation history and context

## Version History

- **1.0.0**: Initial release with basic context rot detection and bias analysis
- **1.1.0**: Added semantic drift detection and needle-in-haystack testing
- **1.2.0**: Enhanced real-time monitoring and predictive detection capabilities
- **1.3.0**: Advanced integration with Empire Health Monitor and MCP Load Balancer
- **1.4.0**: Machine learning-based detection optimization and comprehensive metrics

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.