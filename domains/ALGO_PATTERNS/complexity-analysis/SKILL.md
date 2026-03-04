---
Domain: ALGO_PATTERNS
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: complexity-analysis
---



## Description

Automatically analyzes algorithmic complexity including time complexity, space complexity, and asymptotic behavior. This skill provides comprehensive complexity analysis using mathematical techniques, empirical measurement, and performance prediction to evaluate algorithm efficiency and scalability across different input sizes and conditions.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Theoretical Complexity Analysis**: Analyze Big O, Big Theta, and Big Omega notation for time and space complexity
- **Recurrence Relation Solving**: Solve recurrence relations using master theorem, substitution method, and recursion trees
- **Empirical Performance Measurement**: Measure actual runtime and memory usage across different input sizes
- **Asymptotic Analysis**: Determine growth rates and compare algorithmic efficiency
- **Complexity Visualization**: Generate complexity graphs and performance curves
- **Scalability Prediction**: Predict performance for large input sizes based on complexity analysis
- **Optimization Opportunity Identification**: Identify potential areas for algorithmic improvement

## Usage Examples

### Theoretical Time Complexity Analysis

```yaml
theoretical_analysis:
  algorithm: "Merge Sort"
  analysis_type: "time_complexity"
  
  recurrence_relation: "T(n) = 2T(n/2) + O(n)"
  solving_method: "master_theorem"
  
  master_theorem_application:
    a: 2                      # Number of subproblems
    b: 2                      # Factor by which problem size is reduced
    f_n: "n"                  # Non-recursive work
    log_b_a: 1                # log₂(2) = 1
    case: "Case 2"            # f(n) = Θ(n^log_b_a)
  
  complexity_result:
    time_complexity: "O(n log n)"
    space_complexity: "O(n)"
    best_case: "O(n log n)"
    average_case: "O(n log n)"
    worst_case: "O(n log n)"
  
  mathematical_proof:
    base_case: "T(1) = O(1)"
    inductive_step: "Assume T(k) = O(k log k) for k < n"
    conclusion: "T(n) = O(n log n) by induction"
```

### Empirical Performance Analysis

```yaml
empirical_analysis:
  algorithm: "Quick Sort"
  test_configurations:
    - input_size: 1000
      iterations: 100
      average_time: 0.0025
      memory_usage: 8192
      variance: 0.0001
    
    - input_size: 10000
      iterations: 50
      average_time: 0.032
      memory_usage: 81920
      variance: 0.0015
    
    - input_size: 100000
      iterations: 10
      average_time: 0.45
      memory_usage: 819200
      variance: 0.025
  
  complexity_estimation:
    time_complexity: "O(n log n)"
    space_complexity: "O(log n)"
    confidence_interval: "95%"
    r_squared: 0.987
  
  performance_characteristics:
    cache_friendliness: "high"
    branch_prediction: "good"
    memory_locality: "excellent"
    parallelization_potential: "medium"
```

### Recurrence Relation Analysis

```yaml
recurrence_analysis:
  problem: "Binary Search"
  recurrence_relation: "T(n) = T(n/2) + O(1)"
  
  solving_methods:
    - method: "substitution"
      steps:
        - "T(n) = T(n/2) + c"
        - "T(n) = T(n/4) + 2c"
        - "T(n) = T(n/8) + 3c"
        - "..."
        - "T(n) = T(1) + k*c where n/2^k = 1"
        - "k = log₂(n)"
        - "T(n) = T(1) + c*log₂(n) = O(log n)"
    
    - method: "recursion_tree"
      tree_depth: "log₂(n)"
      nodes_per_level: [1, 1, 1, ..., 1]
      work_per_level: [1, 1, 1, ..., 1]
      total_work: "log₂(n) * 1 = O(log n)"
    
    - method: "master_theorem"
      a: 1
      b: 2
      f_n: "1"
      log_b_a: 0
      case: "Case 2"
      result: "O(log n)"
  
  verification:
    mathematical_induction: "verified"
    empirical_testing: "confirmed"
    edge_case_analysis: "passes"
```

## Input Format

### Complexity Analysis Request

```yaml
complexity_analysis_request:
  algorithm_id: string            # Unique algorithm identifier
  algorithm_description: string   # Natural language description
  implementation_details: object  # Code or pseudocode
  analysis_requirements: object   # What to analyze
  
  algorithm_characteristics:
    algorithm_type: "recursive|iterative|divide_and_conquer|dynamic_programming|greedy"
    input_type: "array|tree|graph|string|numeric"
    input_size_range: object      # Min/max input sizes for analysis
    constraints: object           # Problem constraints
  
  analysis_scope:
    time_complexity: true
    space_complexity: true
    best_case_analysis: true
    average_case_analysis: true
    worst_case_analysis: true
    amortized_analysis: false
    empirical_analysis: true
```

### Algorithm Implementation Schema

```yaml
algorithm_implementation:
  pseudocode: string              # Algorithm pseudocode
  code_language: string           # Programming language
  actual_code: string             # Actual implementation
  key_operations: array           # Critical operations to analyze
  
  operation_analysis:
    - operation: "comparison"
      frequency: "n log n"
      cost: "O(1)"
      total_cost: "O(n log n)"
    
    - operation: "assignment"
      frequency: "n"
      cost: "O(1)"
      total_cost: "O(n)"
    
    - operation: "function_call"
      frequency: "log n"
      cost: "O(1)"
      total_cost: "O(log n)"
  
  data_structures:
    - structure: "array"
      access_pattern: "sequential"
      memory_overhead: "O(1)"
    
    - structure: "tree"
      access_pattern: "random"
      memory_overhead: "O(n)"
```

## Output Format

### Complexity Analysis Report

```yaml
complexity_analysis_report:
  algorithm_id: string
  analysis_timestamp: timestamp
  analysis_methods: array         # Methods used for analysis
  
  theoretical_analysis:
    time_complexity:
      big_o: string               # O(n log n)
      big_theta: string           # Θ(n log n)
      big_omega: string           # Ω(n log n)
      mathematical_proof: string  # Proof details
    
    space_complexity:
      auxiliary_space: string     # O(log n)
      total_space: string         # O(n)
      space_time_tradeoffs: array # Potential trade-offs
    
    recurrence_relation:
      relation: string            # T(n) = 2T(n/2) + O(n)
      solved_form: string         # T(n) = O(n log n)
      solving_method: string      # Master theorem
      verification: string        # Proof method used
  
  empirical_analysis:
    test_results: array           # Empirical measurements
    complexity_estimation: object # Estimated complexity from data
    confidence_interval: string   # Statistical confidence
    r_squared: number             # Goodness of fit
    
    performance_metrics:
      cache_performance: string   # Cache hit/miss rates
      branch_prediction: string   # Branch prediction accuracy
      memory_access_pattern: string # Sequential/random access
      parallelization_efficiency: string # Speedup potential
  
  scalability_analysis:
    predicted_performance: object # Performance for large inputs
    bottleneck_identification: array # Performance bottlenecks
    optimization_opportunities: array # Improvement areas
    scalability_limitations: array # Limiting factors
```

### Performance Visualization Data

```yaml
performance_visualization:
  complexity_graphs:
    - graph_type: "time_vs_input_size"
      x_axis: "Input Size (n)"
      y_axis: "Execution Time (ms)"
      data_points: array
      trend_line: "y = a * n * log(n) + b"
      r_squared: 0.987
    
    - graph_type: "space_vs_input_size"
      x_axis: "Input Size (n)"
      y_axis: "Memory Usage (bytes)"
      data_points: array
      trend_line: "y = c * n + d"
      r_squared: 0.992
  
  comparison_analysis:
    - algorithm: "Algorithm A"
      time_complexity: "O(n²)"
      space_complexity: "O(1)"
      crossover_point: 1000
    
    - algorithm: "Algorithm B"
      time_complexity: "O(n log n)"
      space_complexity: "O(n)"
      crossover_point: 1000
  
  optimization_impact:
    - optimization: "Memoization"
      time_improvement: "O(n²) → O(n)"
      space_overhead: "O(n)"
      applicability: "High"
    
    - optimization: "Iterative_implementation"
      time_improvement: "O(log n) stack overhead"
      space_overhead: "None"
      applicability: "Medium"
```

## Configuration Options

### Analysis Methods

```yaml
analysis_methods:
  theoretical:
    master_theorem: "enabled"
    substitution_method: "enabled"
    recursion_tree: "enabled"
    iteration_method: "enabled"
    characteristic_equation: "enabled"
  
  empirical:
    benchmarking: "enabled"
    profiling: "enabled"
    statistical_analysis: "enabled"
    curve_fitting: "enabled"
  
  hybrid:
    theoretical_validation: "enabled"
    empirical_verification: "enabled"
    complexity_prediction: "enabled"
```

### Analysis Parameters

```yaml
analysis_parameters:
  input_size_ranges:
    small: [1, 100]
    medium: [100, 10000]
    large: [10000, 1000000]
    very_large: [1000000, 100000000]
  
  measurement_precision:
    time_precision: "microseconds"
    memory_precision: "bytes"
    statistical_confidence: "95%"
    sample_size: 100
  
  optimization_goals:
    primary: "time_efficiency"
    secondary: "space_efficiency"
    constraints: ["memory_limit", "time_limit"]
```

## Error Handling

### Analysis Failures

```yaml
analysis_failures:
  unsolvable_recurrence:
    retry_strategy: "numerical_methods"
    max_retries: 2
    fallback_action: "empirical_analysis"
  
  insufficient_data:
    retry_strategy: "additional_sampling"
    max_retries: 3
    fallback_action: "theoretical_analysis"
  
  contradictory_results:
    retry_strategy: "hybrid_approach"
    max_retries: 1
    fallback_action: "expert_review"
  
  measurement_errors:
    retry_strategy: "error_correction"
    max_retries: 2
    fallback_action: "alternative_measurement"
```

### Mathematical Errors

```yaml
mathematical_errors:
  division_by_zero:
    detection_strategy: "boundary_checking"
    recovery_strategy: "limit_analysis"
    escalation: "manual_review"
  
  infinite_recursion:
    detection_strategy: "depth_monitoring"
    recovery_strategy: "iteration_limit"
    escalation: "algorithm_redesign"
  
  numerical_instability:
    detection_strategy: "precision_monitoring"
    recovery_strategy: "arbitrary_precision"
    escalation: "alternative_approach"
```

## Performance Optimization

### Analysis Optimization

```yaml
analysis_optimization:
  algorithmic_optimizations: true
  data_structure_optimizations: true
  measurement_optimizations: true
  computational_optimizations: true
  
  optimization_techniques:
    - technique: "memoization"
      applicable_to: ["recurrence_solving", "complexity_calculation"]
      performance_gain: "significant"
      memory_overhead: "moderate"
    
    - technique: "parallel_analysis"
      applicable_to: ["empirical_measurement", "statistical_analysis"]
      performance_gain: "linear"
      memory_overhead: "minimal"
    
    - technique: "approximation_algorithms"
      applicable_to: ["complex_calculations", "large_input_analysis"]
      performance_gain: "substantial"
      accuracy_tradeoff: "acceptable"
```

### Measurement Optimization

```yaml
measurement_optimization:
  sampling_strategy: "adaptive"
  measurement_frequency: "dynamic"
  precision_control: "automatic"
  error_correction: "enabled"
  
  optimization_strategies:
    - strategy: "warmup_runs"
      purpose: "eliminate_jit_effects"
      iterations: 5
      discard_results: true
    
    - strategy: "outlier_detection"
      purpose: "improve_measurement_accuracy"
      method: "statistical_analysis"
      threshold: "2_standard_deviations"
    
    - strategy: "memory_cleanup"
      purpose: "reduce_memory_interference"
      method: "garbage_collection"
      frequency: "between_runs"
```

## Integration Examples

### With Algorithm Design Tools

```yaml
algorithm_design_integration:
  design_pattern_libraries:
    complexity_aware_patterns: "enabled"
    optimization_patterns: "enabled"
    performance_patterns: "enabled"
  
  complexity_database:
    known_algorithms: "enabled"
    complexity_patterns: "enabled"
    optimization_techniques: "enabled"
  
  performance_prediction:
    scalability_modeling: "enabled"
    bottleneck_prediction: "enabled"
    optimization_recommendation: "enabled"
```

### With Development Tools

```yaml
development_tool_integration:
  integrated_development_environments:
    visual_studio_code: "enabled"
    intellij_idea: "enabled"
    eclipse: "enabled"
  
  profiling_tools:
    built_in_profilers: "enabled"
    third_party_profilers: "enabled"
    custom_profilers: "enabled"
  
  benchmarking_frameworks:
    google_benchmark: "enabled"
    custom_benchmarks: "enabled"
    comparative_analysis: "enabled"
```

## Best Practices

1. **Theoretical Analysis**:
   - Use multiple methods to verify complexity results
   - Consider both best-case and worst-case scenarios
   - Account for all operations, not just the dominant ones
   - Validate theoretical results with empirical data

2. **Empirical Analysis**:
   - Use sufficient sample sizes for statistical significance
   - Control for external factors (system load, caching)
   - Test across a wide range of input sizes
   - Use appropriate measurement precision

3. **Complexity Communication**:
   - Clearly distinguish between theoretical and empirical results
   - Provide confidence intervals and error margins
   - Use appropriate visualization for different audiences
   - Document assumptions and limitations

4. **Optimization Guidance**:
   - Focus on algorithmic improvements before micro-optimizations
   - Consider trade-offs between time and space complexity
   - Validate optimizations don't compromise correctness
   - Measure actual performance impact

## Troubleshooting

### Common Issues

1. **Inconsistent Results**: Check measurement methodology, validate theoretical analysis, consider system interference
2. **Unexpected Complexity**: Review algorithm implementation, check for hidden operations, analyze data structures
3. **Poor Scalability**: Identify bottlenecks, consider algorithmic improvements, analyze memory usage patterns
4. **Measurement Noise**: Increase sample size, control environment, use statistical filtering techniques
5. **Theoretical-Practical Mismatch**: Consider constant factors, cache effects, system overhead

### Debug Mode

```yaml
debug_config:
  enabled: true
  log_level: "debug"
  detailed_tracing: true
  measurement_debugging: true
  complexity_calculation_debugging: true
  visualization_debugging: true
```

## Monitoring and Metrics

### Key Performance Indicators

```yaml
kpi_metrics:
  analysis_accuracy:
    theoretical_accuracy: number
    empirical_accuracy: number
    prediction_accuracy: number
    confidence_intervals: object
  
  analysis_efficiency:
    analysis_time: number
    resource_usage: object
    scalability: object
    automation_level: number
  
  analysis_completeness:
    coverage_percentage: number
    edge_case_analysis: number
    optimization_identification: number
    documentation_quality: number
```

## Dependencies

- **Mathematical Libraries**: For recurrence relation solving and complexity calculations
- **Statistical Analysis Tools**: For empirical measurement and curve fitting
- **Profiling Tools**: For runtime and memory measurement
- **Visualization Libraries**: For complexity graph generation
- **Benchmarking Frameworks**: For performance measurement and comparison

## Version History

- **1.0.0**: Initial release with basic complexity analysis and recurrence solving
- **1.1.0**: Added empirical analysis and performance measurement
- **1.2.0**: Enhanced visualization and scalability prediction
- **1.3.0**: Improved integration with development tools and profiling frameworks
- **1.4.0**: Advanced machine learning-based complexity prediction and optimization recommendation

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.