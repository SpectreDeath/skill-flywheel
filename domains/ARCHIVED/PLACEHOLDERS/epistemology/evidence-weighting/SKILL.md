---
Domain: epistemology
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: evidence-weighting
---
origin: manual
triggers:
  - agent
  - ai
  - development
quality:
  applied_count: 0
  success_count: 0
  completion_rate: 0.0
  token_savings_avg: 0.0
created_at: "2026-03-24T10:00:00Z"
updated_at: "2026-03-24T10:00:00Z"




## Description

Automatically designs and implements optimal evidence weighting systems for AI agents to evaluate, prioritize, and integrate multiple sources of information with varying reliability, confidence levels, and contextual relevance. This skill provides comprehensive frameworks for Bayesian updating, uncertainty quantification, source credibility assessment, and conflict resolution in multi-agent and multi-source environments.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Evidence Quality Assessment**: Analyze and score evidence based on source reliability, methodological soundness, and contextual appropriateness
- **Confidence Calibration**: Implement dynamic confidence adjustment mechanisms based on evidence strength and consistency
- **Source Credibility Modeling**: Design sophisticated source reliability tracking systems with temporal decay and bias detection
- **Conflict Resolution**: Implement principled approaches for resolving contradictory evidence using probabilistic reasoning
- **Uncertainty Quantification**: Generate comprehensive uncertainty estimates that account for multiple sources of error and ambiguity
- **Temporal Evidence Integration**: Handle time-varying evidence with appropriate weighting and forgetting mechanisms
- **Multi-Agent Evidence Aggregation**: Coordinate evidence evaluation across distributed AI agents with different perspectives and capabilities

## Usage Examples

### Evidence Quality Assessment Framework

```yaml
evidence_quality_framework:
  evidence_id: "EVID-2025-001"
  source_type: "sensor_data|expert_opinion|literature|simulation"
  quality_metrics:
    reliability_score: 0.85
    methodological_rigor: 0.92
    contextual_appropriateness: 0.78
    temporal_relevance: 0.95
    bias_indicators: ["confirmation_bias", "selection_bias"]
  
  confidence_adjustment:
    base_confidence: 0.85
    adjustment_factors:
      - factor: "source_reliability"
        weight: 0.3
        adjustment: 0.9
      - factor: "methodological_quality"
        weight: 0.4
        adjustment: 0.95
      - factor: "contextual_fit"
        weight: 0.2
        adjustment: 0.8
      - factor: "temporal_decay"
        weight: 0.1
        adjustment: 1.0
    
    final_confidence: 0.87
    
  uncertainty_quantification:
    aleatory_uncertainty: 0.12
    epistemic_uncertainty: 0.08
    total_uncertainty: 0.20
    confidence_interval: [0.67, 1.07]
```

### Bayesian Evidence Integration

```yaml
bayesian_integration:
  prior_belief:
    probability: 0.6
    confidence: 0.8
    evidence_base: "established_theory"
  
  new_evidence:
    - evidence_id: "EVID-2025-002"
      likelihood_ratio: 3.2
      evidence_strength: 0.85
      source_credibility: 0.9
    
    - evidence_id: "EVID-2025-003"
      likelihood_ratio: 0.4
      evidence_strength: 0.7
      source_credibility: 0.75
  
  posterior_calculation:
    weighted_likelihood: 2.1
    posterior_probability: 0.85
    updated_confidence: 0.88
    uncertainty_reduction: 0.15
  
  conflict_resolution:
    contradictory_evidence: ["EVID-2025-003"]
    resolution_strategy: "weighted_majority"
    resolution_confidence: 0.92
```

### Multi-Agent Evidence Aggregation

```yaml
multi_agent_aggregation:
  agents_involved:
    - agent_id: "AGENT-001"
      expertise: "domain_expert"
      confidence: 0.9
      evidence_weight: 0.4
    
    - agent_id: "AGENT-002"
      expertise: "data_analyst"
      confidence: 0.85
      evidence_weight: 0.35
    
    - agent_id: "AGENT-003"
      expertise: "external_source"
      confidence: 0.7
      evidence_weight: 0.25
  
  aggregation_method: "bayesian_weighted_average"
  consensus_threshold: 0.8
  disagreement_handling:
    - strategy: "evidence_reexamination"
      trigger: "disagreement > 0.3"
    - strategy: "meta_reasoning"
      trigger: "persistent_disagreement"
  
  final_assessment:
    aggregated_confidence: 0.82
    consensus_level: 0.88
    remaining_uncertainty: 0.18
```

## Input Format

### Evidence Evaluation Request

```yaml
evidence_evaluation_request:
  evidence_id: string              # Unique evidence identifier
  evidence_type: string            # Type of evidence (sensor, expert, literature, etc.)
  source_description: object       # Source characteristics and reliability
  content_summary: string          # Brief description of evidence content
  confidence_level: number         # Initial confidence assessment (0.0 to 1.0)
  
  context_requirements:
    domain: string                 # Relevant domain or field
    temporal_scope: object         # Time relevance requirements
    spatial_scope: object          # Geographic or spatial relevance
    uncertainty_tolerance: number  # Acceptable uncertainty level
  
  evaluation_criteria:
    quality_metrics: array         # Specific quality dimensions to assess
    bias_indicators: array         # Potential bias types to detect
    methodological_standards: array # Evaluation standards to apply
    integration_requirements: object # How evidence should integrate with existing knowledge
```

### Source Credibility Profile

```yaml
source_credibility_profile:
  source_id: string
  source_type: "sensor|expert|literature|simulation|crowd"
  
  historical_performance:
    accuracy_history: array        # Past accuracy measurements
    reliability_trend: object      # Temporal reliability patterns
    bias_history: array            # Documented bias patterns
  
  current_assessment:
    expertise_level: string        # Domain expertise rating
    methodological_rigor: number   # Quality of methods used
    transparency_score: number     # Transparency of process
    independence_score: number     # Independence from conflicts of interest
  
  temporal_factors:
    last_updated: timestamp
    decay_rate: number             # Rate of credibility decay over time
    recency_weight: number         # Weight given to recent performance
```

## Output Format

### Evidence Evaluation Report

```yaml
evidence_evaluation_report:
  evidence_id: string
  evaluation_timestamp: timestamp
  evaluator_agent: string
  
  quality_assessment:
    overall_quality_score: number
    quality_dimensions:
      - dimension: "reliability"
        score: number
        justification: string
      - dimension: "validity"
        score: number
        justification: string
      - dimension: "relevance"
        score: number
        justification: string
    
    identified_biases: array
    methodological_weaknesses: array
    contextual_limitations: array
  
  confidence_adjustment:
    initial_confidence: number
    adjustment_factors: array
    final_confidence: number
    confidence_justification: string
  
  uncertainty_analysis:
    uncertainty_components:
      - component: "measurement_error"
        magnitude: number
      - component: "model_uncertainty"
        magnitude: number
      - component: "aleatory_uncertainty"
        magnitude: number
    
    total_uncertainty: number
    confidence_intervals: object
    sensitivity_analysis: object
  
  integration_recommendations:
    integration_strategy: string
    weight_in_aggregation: number
    required_corroborating_evidence: array
    monitoring_requirements: array
```

### Evidence Integration Blueprint

```yaml
evidence_integration_blueprint:
  integration_strategy: string
  mathematical_framework: string    # Bayesian, Dempster-Shafer, etc.
  computational_approach: string    # Analytical, simulation-based, etc.
  
  implementation_phases:
    - phase: "initial_integration"
      duration: string
      tasks: array
      validation_criteria: array
    
    - phase: "confidence_calibration"
      duration: string
      tasks: array
      validation_criteria: array
    
    - phase: "ongoing_monitoring"
      duration: string
      tasks: array
      validation_criteria: array
  
  code_samples:
    - sample_name: string
      description: string
      implementation: string
      complexity: string
      dependencies: array
```

## Configuration Options

### Evidence Weighting Strategies

```yaml
weighting_strategies:
  bayesian_weighting:
    description: "Probabilistic evidence combination using Bayesian updating"
    best_for: ["quantitative_evidence", "probabilistic_reasoning", "uncertainty_quantification"]
    complexity: "medium"
    mathematical_framework: "Bayesian probability"
  
  dempster_shafer:
    description: "Evidence theory for handling uncertainty and ignorance"
    best_for: ["qualitative_evidence", "conflict_resolution", "partial_knowledge"]
    complexity: "high"
    mathematical_framework: "Dempster-Shafer theory"
  
  weighted_majority:
    description: "Simple weighted voting based on source credibility"
    best_for: ["multi_agent_systems", "quick_decisions", "consensus_building"]
    complexity: "low"
    mathematical_framework: "Weighted voting"
  
  fuzzy_logic:
    description: "Fuzzy set theory for handling vague and imprecise evidence"
    best_for: ["linguistic_evidence", "subjective_assessments", "gradual_transitions"]
    complexity: "medium"
    mathematical_framework: "Fuzzy logic"
```

### Source Credibility Models

```yaml
credibility_models:
  historical_performance:
    description: "Credibility based on past accuracy and reliability"
    metrics: ["accuracy_history", "consistency", "timeliness"]
    update_frequency: "continuous"
  
  peer_review:
    description: "Credibility based on peer evaluation and validation"
    metrics: ["peer_ratings", "citation_count", "reproducibility"]
    update_frequency: "periodic"
  
  real_time_validation:
    description: "Credibility based on immediate validation attempts"
    metrics: ["validation_success", "cross_verification", "consistency_checks"]
    update_frequency: "real_time"
  
  hybrid_model:
    description: "Combination of multiple credibility assessment approaches"
    metrics: ["composite_score", "weighted_average", "adaptive_weights"]
    update_frequency: "adaptive"
```

## Error Handling

### Evidence Evaluation Failures

```yaml
evaluation_failures:
  insufficient_information:
    retry_strategy: "information_gathering"
    max_retries: 3
    fallback_action: "conservative_assessment"
  
  contradictory_evidence:
    retry_strategy: "conflict_resolution"
    max_retries: 2
    fallback_action: "suspension_of_judgment"
  
  source_unreliable:
    retry_strategy: "alternative_sources"
    max_retries: 1
    fallback_action: "evidence_exclusion"
  
  computational_overflow:
    retry_strategy: "numerical_stabilization"
    max_retries: 2
    fallback_action: "approximation_methods"
```

### Integration Errors

```yaml
integration_errors:
  evidence_conflict:
    detection_strategy: "consistency_checking"
    recovery_strategy: "conflict_resolution"
    escalation: "human_intervention"
  
  confidence_drift:
    detection_strategy: "monitoring_and_alerting"
    recovery_strategy: "confidence_calibration"
    escalation: "system_reset"
  
  computational_complexity:
    detection_strategy: "performance_monitoring"
    recovery_strategy: "algorithm_optimization"
    escalation: "simplified_approach"
```

## Performance Optimization

### Evidence Processing Optimization

```yaml
processing_optimization:
  evidence_caching: true
  incremental_updates: true
  parallel_processing: true
  memory_optimization: true
  
  optimization_techniques:
    - technique: "evidence_summarization"
      applicable_evidence_types: ["large_datasets", "streaming_data"]
      performance_gain: "significant"
      accuracy_tradeoff: "minimal"
    
    - technique: "selective_processing"
      applicable_evidence_types: ["low_priority", "redundant"]
      performance_gain: "moderate"
      accuracy_tradeoff: "controlled"
    
    - technique: "approximate_computation"
      applicable_evidence_types: ["real_time_systems"]
      performance_gain: "high"
      accuracy_tradeoff: "acceptable"
```

### Multi-Agent Coordination Optimization

```yaml
coordination_optimization:
  communication_optimization:
    - optimization: "batch_communication"
      technique: "Aggregate evidence updates"
      impact: "Reduced communication overhead"
    
    - optimization: "selective_sharing"
      technique: "Share only significant evidence changes"
      impact: "Improved bandwidth efficiency"
    
    - optimization: "compression_strategies"
      technique: "Compress evidence representations"
      impact: "Reduced data transfer requirements"
  
  computational_optimization:
    - optimization: "distributed_computation"
      technique: "Parallel evidence processing"
      impact: "Improved processing speed"
    
    - optimization: "load_balancing"
      technique: "Dynamic workload distribution"
      impact: "Optimized resource utilization"
    
    - optimization: "caching_strategies"
      technique: "Cache intermediate results"
      impact: "Reduced redundant computation"
```

## Integration Examples

### With AI Agent Frameworks

```yaml
agent_framework_integration:
  openai_frameworks:
    integration_points: ["tool_calls", "function_calls", "memory_systems"]
    evidence_storage: "Vector databases with metadata"
    confidence_tracking: "Integrated with response generation"
  
  anthropic_frameworks:
    integration_points: ["Claude messages", "tool_use", "memory"]
    evidence_storage: "Claude memory with evidence tagging"
    confidence_tracking: "Built into response confidence"
  
  custom_agent_frameworks:
    integration_points: ["belief_systems", "reasoning_modules", "memory_management"]
    evidence_storage: "Custom knowledge graphs"
    confidence_tracking: "Agent-specific confidence models"
```

### With Decision Systems

```yaml
decision_system_integration:
  automated_decision_making:
    evidence_incorporation: "Real-time evidence weighting in decisions"
    confidence_thresholds: "Minimum confidence for action"
    uncertainty_handling: "Uncertainty-aware decision strategies"
  
  human_in_the_loop:
    evidence_presentation: "Clear evidence visualization"
    confidence_communication: "Effective confidence explanation"
    override_capabilities: "Human override with evidence context"
  
  multi_criteria_decision:
    evidence_weighting: "Evidence-based criterion weighting"
    uncertainty_propagation: "Uncertainty through decision hierarchy"
    sensitivity_analysis: "Evidence impact on decisions"
```

## Best Practices

1. **Evidence Quality Assessment**:
   - Always assess source credibility before evidence evaluation
   - Consider temporal and contextual factors in evidence assessment
   - Document assumptions and limitations in evidence evaluation
   - Regularly update evidence assessments as new information becomes available

2. **Confidence Management**:
   - Maintain separate confidence scores for different evidence aspects
   - Implement confidence calibration based on historical performance
   - Use confidence intervals rather than point estimates when possible
   - Communicate confidence levels clearly to decision-makers

3. **Uncertainty Quantification**:
   - Distinguish between different types of uncertainty (aleatory vs epistemic)
   - Propagate uncertainty through evidence integration processes
   - Use appropriate uncertainty representation methods for different contexts
   - Regularly validate uncertainty estimates against outcomes

4. **Multi-Agent Coordination**:
   - Establish clear communication protocols for evidence sharing
   - Implement conflict resolution mechanisms for contradictory evidence
   - Maintain agent-specific credibility assessments
   - Design for scalability as the number of agents increases

## Troubleshooting

### Common Issues

1. **Overconfidence**: Review evidence quality assessment and implement confidence calibration
2. **Evidence Conflicts**: Implement systematic conflict resolution strategies
3. **Computational Complexity**: Use approximation methods and optimization techniques
4. **Source Bias**: Implement bias detection and mitigation strategies
5. **Integration Failures**: Review evidence compatibility and integration frameworks

### Debug Mode

```yaml
debug_config:
  enabled: true
  log_level: "debug"
  evidence_debugging: true
  confidence_debugging: true
  integration_debugging: true
  multi_agent_debugging: true
```

## Monitoring and Metrics

### Key Performance Indicators

```yaml
kpi_metrics:
  evidence_quality:
    average_quality_score: number
    quality_trend: object
    bias_detection_rate: number
    methodological_completeness: number
  
  confidence_accuracy:
    confidence_calibration_score: number
    prediction_accuracy: number
    uncertainty_coverage: number
    confidence_stability: number
  
  integration_effectiveness:
    evidence_utilization_rate: number
    conflict_resolution_success: number
    integration_speed: number
    multi_agent_consensus: number
```

## Dependencies

- **Evidence Management Systems**: Tools for storing and retrieving evidence with metadata
- **Probabilistic Reasoning Libraries**: Libraries for Bayesian inference and uncertainty quantification
- **Multi-Agent Frameworks**: Platforms for coordinating multiple AI agents
- **Monitoring and Logging**: Systems for tracking evidence evaluation performance
- **Visualization Tools**: Tools for presenting evidence and confidence information

## Version History

- **1.0.0**: Initial release with comprehensive evidence weighting frameworks and multi-agent integration
- **1.1.0**: Added advanced uncertainty quantification and temporal evidence handling
- **1.2.0**: Enhanced multi-agent coordination and conflict resolution capabilities
- **1.3.0**: Improved performance optimization and real-time evidence processing
- **1.4.0**: Advanced bias detection and mitigation strategies with machine learning integration

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.