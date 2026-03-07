---
Domain: orchestration
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: dynamic-skill-selection-routing
---



## Description

Implements intelligent dynamic skill selection and routing to optimize task execution based on real-time conditions, skill performance metrics, and contextual requirements. This skill uses machine learning algorithms and decision trees to route tasks to the most appropriate skills while adapting to changing conditions and performance patterns.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Intelligent Skill Matching**: Match tasks to optimal skills based on capabilities, performance, and context
- **Real-time Performance Monitoring**: Continuously track skill performance and adjust routing decisions
- **Adaptive Learning**: Learn from execution outcomes to improve future routing decisions
- **Load Balancing**: Distribute tasks across skills based on current load and capacity
- **Context-Aware Routing**: Consider task context, urgency, and resource requirements
- **Fallback Mechanisms**: Automatically route to alternative skills when primary choices fail
- **Performance Optimization**: Continuously optimize routing for throughput, latency, and success rates

## Usage Examples

### Basic Dynamic Routing

```yaml
routing_config:
  task_type: "data_processing"
  routing_strategy: "performance_based"
  fallback_skills: ["data_processor_backup", "data_processor_legacy"]
  
  skill_profiles:
    - skill_name: "data_processor_v2"
      capability_score: 95
      performance_score: 92
      availability: "high"
      cost_factor: 1.2
    
    - skill_name: "data_processor_v1"
      capability_score: 85
      performance_score: 88
      availability: "medium"
      cost_factor: 1.0
```

### Advanced Context-Aware Routing

```yaml
context_aware_routing:
  task_context:
    data_size: "large"
    complexity: "high"
    urgency: "medium"
    resource_requirements: "cpu_intensive"
  
  routing_decision:
    selected_skill: "high_performance_processor"
    confidence_score: 0.94
    reasoning: "Best match for large data size and high complexity"
    alternatives: ["standard_processor", "parallel_processor"]
  
  performance_tracking:
    execution_time: 1500
    success_rate: 0.98
    resource_usage: "optimal"
```

### Machine Learning-Based Routing

```yaml
ml_routing:
  model_type: "reinforcement_learning"
  training_data:
    historical_performance: "last_30_days"
    skill_metrics: "real_time"
    task_outcomes: "tracked"
  
  decision_factors:
    - factor: "skill_capability"
      weight: 0.3
    - factor: "current_load"
      weight: 0.25
    - factor: "task_complexity"
      weight: 0.2
    - factor: "resource_availability"
      weight: 0.15
    - factor: "historical_success_rate"
      weight: 0.1
  
  optimization_targets:
    - "minimize_execution_time"
    - "maximize_success_rate"
    - "balance_resource_usage"
```

## Input Format

### Task Routing Request

```yaml
routing_request:
  task_id: string                 # Unique task identifier
  task_type: string               # Type of task to route
  task_context: object            # Contextual information about the task
  priority: number                # Task priority (1-10)
  deadline: timestamp             # Task deadline (optional)
  resource_requirements: object   # Required resources
  constraints: object             # Routing constraints
  
  task_metadata:
    estimated_complexity: "low|medium|high|critical"
    data_size: number             # Estimated data size in bytes
    execution_time_limit: number  # Maximum allowed execution time
    quality_requirements: object  # Quality or accuracy requirements
```

### Skill Profile Schema

```yaml
skill_profile:
  skill_name: string
  version: string
  capabilities: array             # List of supported capabilities
  performance_metrics:
    average_execution_time: number
    success_rate: number
    throughput: number
    resource_efficiency: number
  
  availability:
    current_status: "active|degraded|maintenance"
    load_percentage: number
    capacity_remaining: number
    estimated_recovery_time: number
  
  cost_metrics:
    execution_cost: number
    resource_cost: number
    priority_cost: number
  
  compatibility:
    platform_requirements: array
    dependency_requirements: array
    constraint_compliance: array
```

## Output Format

### Routing Decision

```yaml
routing_decision:
  task_id: string
  selected_skill: string
  confidence_score: number        # 0.0 to 1.0
  decision_timestamp: timestamp
  reasoning: string               # Explanation for the decision
  
  alternatives:
    - skill_name: string
      confidence_score: number
      reasoning: string
  
  performance_prediction:
    estimated_execution_time: number
    predicted_success_rate: number
    resource_usage_prediction: object
    risk_assessment: string
  
  routing_metadata:
    decision_algorithm: string
    factors_considered: array
    weights_applied: object
    fallback_strategy: string
```

### Performance Report

```yaml
performance_report:
  task_id: string
  actual_execution_time: number
  actual_success_rate: number
  resource_usage_actual: object
  quality_metrics: object
  
  decision_accuracy:
    prediction_accuracy: number
    confidence_calibration: number
    learning_improvement: number
  
  optimization_suggestions:
    - suggestion: string
      impact: "high|medium|low"
      priority: number
  
  feedback_for_model:
    outcome: "success|failure"
    deviation_from_prediction: object
    contributing_factors: array
```

## Configuration Options

### Routing Algorithms

```yaml
routing_algorithms:
  performance_based:
    description: "Route based on historical performance metrics"
    best_for: "stable_workloads"
    complexity: "medium"
    accuracy: "high"
  
  load_balanced:
    description: "Distribute load evenly across available skills"
    best_for: "high_volume_workloads"
    complexity: "low"
    accuracy: "medium"
  
  context_aware:
    description: "Consider task context and skill capabilities"
    best_for: "complex_heterogeneous_workloads"
    complexity: "high"
    accuracy: "very_high"
  
  machine_learning:
    description: "Use ML models for intelligent routing decisions"
    best_for: "dynamic_adaptive_workloads"
    complexity: "very_high"
    accuracy: "adaptive"
```

### Decision Factors

```yaml
decision_factors:
  skill_capability:
    description: "How well the skill matches task requirements"
    weight_range: [0.1, 0.4]
    measurement: "capability_matching_algorithm"
  
  current_load:
    description: "Current workload of the skill"
    weight_range: [0.1, 0.3]
    measurement: "real_time_load_monitoring"
  
  task_complexity:
    description: "Complexity of the task being routed"
    weight_range: [0.1, 0.3]
    measurement: "complexity_analysis"
  
  resource_availability:
    description: "Available resources for skill execution"
    weight_range: [0.05, 0.25]
    measurement: "resource_monitoring"
  
  historical_performance:
    description: "Past performance of skill on similar tasks"
    weight_range: [0.1, 0.3]
    measurement: "performance_history_analysis"
```

## Error Handling

### Routing Failures

```yaml
routing_failures:
  no_available_skills:
    cause: "All skills are unavailable or overloaded"
    recovery_strategy: "queue_for_later|escalate_to_human"
    retry_policy: "exponential_backoff"
  
  skill_mismatch:
    cause: "No skill matches task requirements"
    recovery_strategy: "broaden_criteria|use_alternative_approach"
    retry_policy: "immediate_with_adjustments"
  
  routing_algorithm_failure:
    cause: "Routing algorithm encountered an error"
    recovery_strategy: "fallback_to_simple_routing"
    retry_policy: "immediate"
  
  performance_prediction_failure:
    cause: "Unable to predict skill performance"
    recovery_strategy: "use_historical_average|conservative_estimation"
    retry_policy: "immediate"
```

### Fallback Strategies

```yaml
fallback_strategies:
  simple_round_robin:
    description: "Distribute tasks evenly without intelligence"
    use_case: "algorithm_failure|no_data_available"
    performance: "basic"
  
  priority_based:
    description: "Route based on skill priority levels"
    use_case: "emergency_routing|simple_workloads"
    performance: "medium"
  
  capability_matching:
    description: "Match tasks to skills based on capability tags"
    use_case: "no_performance_data|new_skills"
    performance: "good"
  
  human_intervention:
    description: "Escalate to human operator for manual routing"
    use_case: "critical_tasks|complex_decisions"
    performance: "expert"
```

## Performance Optimization

### Adaptive Learning

```yaml
adaptive_learning:
  learning_rate: 0.1
  memory_window: 1000             # Number of past decisions to remember
  update_frequency: 300000        # Update model every 5 minutes
  
  learning_metrics:
    - metric: "routing_accuracy"
      target: 0.95
      weight: 0.4
    - metric: "execution_time_improvement"
      target: 0.15
      weight: 0.3
    - metric: "success_rate_improvement"
      target: 0.05
      weight: 0.2
    - metric: "resource_optimization"
      target: 0.20
      weight: 0.1
  
  model_types:
    - type: "decision_tree"
      use_case: "interpretable_routing"
    - type: "neural_network"
      use_case: "complex_pattern_recognition"
    - type: "ensemble"
      use_case: "highest_accuracy"
```

### Real-time Optimization

```yaml
real_time_optimization:
  monitoring_interval: 1000       # Monitor every second
  adjustment_threshold: 0.05      # 5% deviation triggers adjustment
  optimization_targets:
    - target: "minimize_average_execution_time"
      constraint: "maintain_success_rate_above_95%"
    
    - target: "maximize_skill_utilization"
      constraint: "prevent_overloading_any_single_skill"
    
    - target: "balance_workload_distribution"
      constraint: "ensure_fair_resource_allocation"
  
  auto_scaling:
    scale_up_threshold: 0.8       # 80% utilization
    scale_down_threshold: 0.3     # 30% utilization
    cooldown_period: 300000       # 5 minutes
```

## Integration Examples

### With Task Management Systems

```yaml
task_management_integration:
  task_submission:
    api_endpoint: "http://task-manager:8080/tasks"
    authentication: "bearer_token"
    format: "json"
  
  status_updates:
    webhook_url: "http://task-manager:8080/webhooks/routing"
    events: ["routing_complete", "skill_selected", "execution_started"]
  
  feedback_loop:
    performance_data: "real_time"
    learning_updates: "batched"
    model_retraining: "scheduled"
```

### With Monitoring and Analytics

```yaml
monitoring_integration:
  metrics_collection:
    prometheus: true
    grafana_dashboard: "skill_routing_metrics"
    custom_metrics: ["routing_accuracy", "decision_latency", "skill_utilization"]
  
  alerting:
    routing_failures: "immediate"
    performance_degradation: "threshold_based"
    skill_unavailability: "real_time"
  
  analytics:
    decision_patterns: "tracked"
    performance_trends: "analyzed"
    optimization_opportunities: "identified"
```

## Best Practices

1. **Skill Profiling**:
   - Maintain accurate and up-to-date skill profiles
   - Track performance metrics in real-time
   - Regularly validate skill capabilities
   - Implement skill health monitoring

2. **Routing Strategy**:
   - Choose appropriate routing algorithms for your workload
   - Implement multiple fallback strategies
   - Monitor routing decision accuracy
   - Continuously optimize routing parameters

3. **Performance Monitoring**:
   - Track key routing metrics and KPIs
   - Set up appropriate alerting thresholds
   - Analyze routing patterns for optimization opportunities
   - Regularly review and update routing strategies

4. **Machine Learning**:
   - Use high-quality training data
   - Implement proper model validation
   - Monitor for model drift and retrain as needed
   - Maintain interoperability for critical routing decisions

## Troubleshooting

### Common Routing Issues

1. **Poor Routing Decisions**: Review skill profiles and decision factors
2. **High Routing Latency**: Optimize routing algorithms and caching
3. **Skill Overloading**: Implement better load balancing and capacity planning
4. **Inaccurate Predictions**: Improve training data and model parameters
5. **Fallback Failures**: Review and test fallback strategies

### Debug Mode

```yaml
debug_config:
  enabled: true
  log_level: "debug"
  decision_tracing: true
  performance_monitoring: true
  model_explanation: true
  routing_simulation: true
```

## Monitoring and Metrics

### Key Routing Metrics

```yaml
routing_metrics:
  decision_metrics:
    routing_accuracy: number      # Percentage of correct routing decisions
    decision_latency: number      # Time taken to make routing decisions
    confidence_calibration: number # How well confidence scores match actual success
  
  performance_metrics:
    task_completion_rate: number  # Percentage of successfully completed tasks
    average_execution_time: number # Average time to complete routed tasks
    skill_utilization_rate: number # How effectively skills are being used
  
  optimization_metrics:
    resource_efficiency: number   # How well resources are being utilized
    load_balance_score: number    # How evenly load is distributed
    cost_optimization: number     # Cost savings from intelligent routing
  
  learning_metrics:
    model_improvement_rate: number # Rate at which routing model improves
    prediction_accuracy_trend: number # Trend in prediction accuracy over time
    adaptation_speed: number      # How quickly the system adapts to changes
```

## Dependencies

- **Machine Learning Frameworks**: TensorFlow, PyTorch, or scikit-learn for intelligent routing
- **Monitoring Systems**: Prometheus, Grafana, or custom metrics collection
- **Task Management**: Integration with task queues and workflow systems
- **Performance Tracking**: Real-time metrics collection and analysis
- **Decision Trees**: Algorithms for capability matching and routing logic

## Version History

- **1.0.0**: Initial release with basic dynamic routing and performance-based selection
- **1.1.0**: Added machine learning-based routing and adaptive learning
- **1.2.0**: Enhanced context-aware routing and real-time optimization
- **1.3.0**: Performance monitoring and advanced fallback strategies
- **1.4.0**: Integration with external systems and comprehensive analytics

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.



## Constraints

To be provided dynamically during execution.