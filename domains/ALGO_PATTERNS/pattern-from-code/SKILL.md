---
Domain: ALGO_PATTERNS
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: pattern-from-code
---



## Description

Automatically identifies and extracts design patterns, algorithmic patterns, and architectural patterns from existing codebases. This skill analyzes source code structure, relationships, and behavior to recognize established patterns, generate documentation, and provide insights for refactoring and optimization opportunities.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Code Pattern Recognition**: Identify design patterns, algorithmic patterns, and architectural patterns in source code
- **Structure Analysis**: Analyze class hierarchies, method relationships, and data flow patterns
- **Behavioral Pattern Detection**: Recognize behavioral patterns through method calls, event handling, and state transitions
- **Pattern Documentation Generation**: Automatically generate comprehensive pattern documentation
- **Refactoring Recommendations**: Suggest pattern-based refactoring opportunities
- **Pattern Violation Detection**: Identify deviations from established pattern implementations
- **Code Quality Assessment**: Evaluate code quality based on pattern usage and adherence

## Usage Examples

### Design Pattern Recognition

```yaml
design_pattern_recognition:
  code_analysis:
    file_path: "src/services/OrderService.java"
    analysis_scope: "class_hierarchy"
    detected_patterns: array
    
  singleton_pattern_detection:
    pattern_name: "Singleton"
    confidence_score: 0.95
    evidence:
      - "Private static instance variable"
      - "Private constructor"
      - "Public static getInstance() method"
      - "Thread-safe implementation with double-checked locking"
    
    implementation_quality:
      correct_implementation: true
      thread_safety: "verified"
      lazy_initialization: "implemented"
      serialization_safe: "not_implemented"
    
    recommendations:
      - "Consider enum-based singleton for better serialization safety"
      - "Add null checks in getInstance() method"
      - "Document singleton behavior and lifecycle"
  
  observer_pattern_detection:
    pattern_name: "Observer"
    confidence_score: 0.88
    evidence:
      - "Subject interface with attach/detach methods"
      - "Observer interface with update method"
      - "Concrete subject maintaining observer list"
      - "Notification mechanism implementation"
    
    implementation_quality:
      loose_coupling: "verified"
      dynamic_subscriptions: "implemented"
      notification_order: "not_guaranteed"
      memory_management: "needs_improvement"
    
    recommendations:
      - "Use weak references to prevent memory leaks"
      - "Implement notification filtering"
      - "Add thread-safe notification mechanism"
```

### Algorithmic Pattern Recognition

```yaml
algorithmic_pattern_recognition:
  algorithm_analysis:
    file_path: "src/algorithms/GraphAlgorithms.java"
    algorithm_type: "graph_traversal"
    detected_patterns: array
  
  divide_and_conquer_detection:
    pattern_name: "Divide and Conquer"
    confidence_score: 0.92
    evidence:
      - "Recursive function calls"
      - "Problem decomposition into subproblems"
      - "Base case handling"
      - "Solution combination logic"
    
    algorithm_details:
      problem_type: "matrix_multiplication"
      subproblem_count: 8
      subproblem_size: "n/2"
      combination_complexity: "O(n²)"
    
    optimization_opportunities:
      - "Strassen's algorithm for better complexity"
      - "Memoization for overlapping subproblems"
      - "Parallel execution for independent subproblems"
  
  dynamic_programming_detection:
    pattern_name: "Dynamic Programming"
    confidence_score: 0.85
    evidence:
      - "Overlapping subproblems identified"
      - "Optimal substructure property"
      - "Memoization table usage"
      - "Bottom-up approach implementation"
    
    implementation_quality:
      state_definition: "clear"
      transition_function: "correct"
      base_cases: "complete"
      space_optimization: "not_implemented"
    
    recommendations:
      - "Implement space-optimized version"
      - "Add early termination conditions"
      - "Consider top-down approach with memoization"
```

### Architectural Pattern Recognition

```yaml
architectural_pattern_recognition:
  architecture_analysis:
    project_structure: "multi_module"
    detected_patterns: array
    layer_dependencies: object
  
  mvc_pattern_detection:
    pattern_name: "Model-View-Controller"
    confidence_score: 0.90
    evidence:
      - "Separate model classes in domain layer"
      - "View components in presentation layer"
      - "Controller classes in web layer"
      - "Clear separation of concerns"
    
    implementation_quality:
      model_layer: "well_defined"
      view_layer: "decoupled"
      controller_layer: "thin_controllers"
      layer_communication: "proper"
    
    recommendations:
      - "Consider adding service layer for business logic"
      - "Implement proper validation in controllers"
      - "Use dependency injection for better testability"
  
  layered_architecture_detection:
    pattern_name: "Layered Architecture"
    confidence_score: 0.88
    evidence:
      - "Clear layer boundaries"
      - "Dependency direction enforcement"
      - "Interface-based communication"
      - "Separation of concerns"
    
    layer_analysis:
      presentation_layer: "web_controllers"
      business_layer: "services"
      data_layer: "repositories"
      infrastructure_layer: "external_services"
    
    violations_detected:
      - "Direct database access from controllers"
      - "Business logic in presentation layer"
      - "Circular dependencies between layers"
    
    refactoring_suggestions:
      - "Move business logic to service layer"
      - "Use DTOs for layer communication"
      - "Implement proper exception handling"
```

## Input Format

### Pattern Recognition Request

```yaml
pattern_recognition_request:
  codebase_path: string           # Path to analyze
  analysis_scope: "file|directory|project"
  pattern_categories: array       # Types of patterns to detect
  analysis_depth: "shallow|medium|deep"
  
  codebase_characteristics:
    language: string              # Programming language
    framework: string             # Framework used
    project_type: "web|mobile|desktop|api"
    codebase_size: "small|medium|large"
  
  analysis_requirements:
    include_documentation: boolean
    include_recommendations: boolean
    include_violations: boolean
    include_metrics: boolean
```

### Code Analysis Schema

```yaml
code_analysis_schema:
  static_analysis:
    class_hierarchy: object       # Class inheritance relationships
    method_signatures: array      # Method definitions and signatures
    field_declarations: array     # Field definitions
    interface_implementations: array # Interface usage
  
  dynamic_analysis:
    method_calls: array           # Method call relationships
    object_creation: array        # Object instantiation patterns
    event_handling: array         # Event-driven patterns
    state_transitions: array      # State change patterns
  
  structural_analysis:
    package_structure: object     # Package/module organization
    dependency_graph: object      # Dependency relationships
    coupling_metrics: object      # Coupling measurements
    cohesion_metrics: object      # Cohesion measurements
```

## Output Format

### Pattern Recognition Report

```yaml
pattern_recognition_report:
  codebase_path: string
  analysis_timestamp: timestamp
  analysis_scope: string
  total_patterns_detected: number
  
  detected_patterns:
    - pattern_name: string
      pattern_type: "design|algorithmic|architectural"
      confidence_score: number    # 0.0 to 1.0
      evidence: array             # Code evidence supporting detection
      implementation_quality: object
      recommendations: array      # Improvement suggestions
      
      pattern_details:
        intent: string            # Pattern purpose
        context: string           # When pattern is applicable
        structure: object         # Pattern structure description
        participants: array       # Key components
        collaborations: array     # Component interactions
      
      code_locations:
        - file_path: string
        - line_numbers: array
        - method_names: array
        - class_names: array
  
  pattern_violations:
    - violation_type: string
      pattern_name: string
      severity: "low|medium|high|critical"
      description: string
      location: object
      suggested_fix: string
  
  refactoring_opportunities:
    - opportunity_type: string
      current_implementation: string
      recommended_pattern: string
      complexity_impact: string
      benefit_score: number
      implementation_effort: string
```

### Pattern Documentation

```yaml
pattern_documentation:
  pattern_name: string
  pattern_type: string
  version: string
  
  overview:
    description: string
    when_to_use: string
    when_not_to_use: string
    benefits: array
    tradeoffs: array
  
  implementation_guide:
    step_by_step: array
    code_examples: array
    best_practices: array
    common_mistakes: array
  
  variations:
    - variation_name: string
    - variation_description: string
    - when_to_use: string
    - implementation_differences: array
  
  related_patterns:
    - pattern_name: string
    - relationship: string
    - combination_benefits: array
  
  testing_strategy:
    unit_tests: array
    integration_tests: array
    pattern_validation_tests: array
    performance_tests: array
```

## Configuration Options

### Pattern Detection Categories

```yaml
pattern_detection_categories:
  design_patterns:
    creational: ["singleton", "factory", "builder", "prototype", "abstract_factory"]
    structural: ["adapter", "bridge", "composite", "decorator", "facade", "flyweight", "proxy"]
    behavioral: ["observer", "strategy", "command", "state", "visitor", "mediator", "iterator"]
  
  algorithmic_patterns:
    divide_and_conquer: "enabled"
    dynamic_programming: "enabled"
    greedy_algorithms: "enabled"
    backtracking: "enabled"
    branch_and_bound: "enabled"
    randomized_algorithms: "enabled"
  
  architectural_patterns:
    mvc: "enabled"
    mvp: "enabled"
    mvvm: "enabled"
    layered: "enabled"
    microservices: "enabled"
    event_driven: "enabled"
    service_oriented: "enabled"
```

### Analysis Parameters

```yaml
analysis_parameters:
  confidence_thresholds:
    high: 0.8
    medium: 0.6
    low: 0.4
  
  analysis_depth:
    shallow: { max_files: 10, max_lines: 1000 }
    medium: { max_files: 100, max_lines: 10000 }
    deep: { max_files: 1000, max_lines: 100000 }
  
  pattern_specific_weights:
    singleton: { thread_safety: 0.4, lazy_initialization: 0.3, serialization: 0.3 }
    observer: { loose_coupling: 0.4, dynamic_subscriptions: 0.3, memory_management: 0.3 }
    factory: { abstraction: 0.5, extensibility: 0.3, complexity: 0.2 }
```

## Error Handling

### Analysis Failures

```yaml
analysis_failures:
  insufficient_code_coverage:
    retry_strategy: "expand_analysis_scope"
    max_retries: 2
    fallback_action: "partial_analysis"
  
  unsupported_language:
    retry_strategy: "language_detection"
    max_retries: 1
    fallback_action: "generic_pattern_analysis"
  
  memory_exhaustion:
    retry_strategy: "streaming_analysis"
    max_retries: 2
    fallback_action: "file_by_file_analysis"
  
  pattern_confidence_low:
    retry_strategy: "enhanced_analysis"
    max_retries: 3
    fallback_action: "manual_review_required"
```

### Pattern Detection Errors

```yaml
detection_errors:
  false_positives:
    detection_strategy: "confidence_thresholding"
    recovery_strategy: "manual_verification"
    escalation: "expert_review"
  
  false_negatives:
    detection_strategy: "comprehensive_scanning"
    recovery_strategy: "alternative_detection_methods"
    escalation: "pattern_database_enhancement"
  
  incomplete_patterns:
    detection_strategy: "pattern_completion_analysis"
    recovery_strategy: "partial_pattern_recognition"
    escalation: "custom_pattern_definition"
```

## Performance Optimization

### Analysis Optimization

```yaml
analysis_optimization:
  parallel_analysis: true
  caching_strategy: true
  incremental_analysis: true
  memory_optimization: true
  
  optimization_techniques:
    - technique: "code_indexing"
      applicable_to: ["static_analysis", "pattern_detection"]
      performance_gain: "significant"
      memory_overhead: "moderate"
    
    - technique: "streaming_analysis"
      applicable_to: ["large_codebases", "memory_constrained_environments"]
      performance_gain: "moderate"
      memory_overhead: "minimal"
    
    - technique: "pattern_caching"
      applicable_to: ["repeated_analysis", "similar_codebases"]
      performance_gain: "high"
      memory_overhead: "low"
```

### Pattern Recognition Optimization

```yaml
recognition_optimization:
  algorithmic_optimizations: true
  data_structure_optimizations: true
  pattern_matching_optimizations: true
  result_caching: true
  
  optimization_strategies:
    - strategy: "pattern_similarity_matching"
      benefits: ["reduced_computation", "improved_accuracy"]
      tradeoffs: ["memory_usage", "initialization_overhead"]
    
    - strategy: "incremental_pattern_detection"
      benefits: ["faster_analysis", "real_time_updates"]
      tradeoffs: ["complexity", "state_management"]
    
    - strategy: "parallel_pattern_recognition"
      benefits: ["linear_speedup", "better_resource_utilization"]
      tradeoffs: ["synchronization_overhead", "memory_sharing"]
```

## Integration Examples

### With Development Tools

```yaml
development_tool_integration:
  integrated_development_environments:
    visual_studio_code: "enabled"
    intellij_idea: "enabled"
    eclipse: "enabled"
    visual_studio: "enabled"
  
  static_analysis_tools:
    sonarqube: "enabled"
    checkstyle: "enabled"
    pmd: "enabled"
    eslint: "enabled"
  
  code_review_tools:
    github: "enabled"
    gitlab: "enabled"
    bitbucket: "enabled"
    azure_devops: "enabled"
```

### With Architecture Tools

```yaml
architecture_tool_integration:
  uml_generation:
    class_diagrams: "enabled"
    sequence_diagrams: "enabled"
    component_diagrams: "enabled"
    deployment_diagrams: "enabled"
  
  architecture_analysis:
    dependency_analysis: "enabled"
    coupling_cohesion_analysis: "enabled"
    pattern_compliance_analysis: "enabled"
    refactoring_recommendations: "enabled"
  
  documentation_generation:
    pattern_documentation: "enabled"
    architecture_documentation: "enabled"
    code_documentation: "enabled"
    api_documentation: "enabled"
```

## Best Practices

1. **Pattern Recognition**:
   - Use multiple detection techniques for higher accuracy
   - Consider context and domain-specific patterns
   - Validate detected patterns with manual review
   - Maintain pattern databases with known implementations

2. **Code Analysis**:
   - Analyze both static structure and dynamic behavior
   - Consider architectural context and constraints
   - Use appropriate analysis depth based on codebase size
   - Document assumptions and limitations

3. **Documentation Generation**:
   - Generate comprehensive pattern documentation
   - Include code examples and best practices
   - Document variations and related patterns
   - Provide testing strategies and validation approaches

4. **Refactoring Guidance**:
   - Prioritize refactoring based on impact and effort
   - Consider team expertise and project constraints
   - Plan refactoring in incremental steps
   - Validate refactoring with comprehensive testing

## Troubleshooting

### Common Issues

1. **False Pattern Detection**: Review confidence thresholds, validate with manual analysis, improve pattern matching algorithms
2. **Missing Patterns**: Expand analysis scope, use alternative detection methods, enhance pattern databases
3. **Performance Issues**: Optimize analysis algorithms, use incremental analysis, implement caching strategies
4. **Integration Problems**: Check tool compatibility, validate configuration, ensure proper permissions
5. **Documentation Quality**: Review documentation templates, include practical examples, validate completeness

### Debug Mode

```yaml
debug_config:
  enabled: true
  log_level: "debug"
  pattern_detection_debugging: true
  code_analysis_debugging: true
  documentation_generation_debugging: true
  performance_monitoring_debugging: true
```

## Monitoring and Metrics

### Key Performance Indicators

```yaml
kpi_metrics:
  detection_accuracy:
    true_positive_rate: number
    false_positive_rate: number
    precision_score: number
    recall_score: number
  
  analysis_performance:
    analysis_time: number
    memory_usage: number
    scalability_metrics: object
    throughput_metrics: object
  
  documentation_quality:
    completeness_score: number
    accuracy_score: number
    usability_score: number
    maintenance_score: number
```

## Dependencies

- **Static Analysis Tools**: For code structure and pattern analysis
- **Pattern Databases**: Comprehensive collections of known patterns
- **Code Parsing Libraries**: For language-specific code analysis
- **Visualization Tools**: For generating diagrams and visualizations
- **Documentation Generation Tools**: For creating comprehensive pattern documentation

## Version History

- **1.0.0**: Initial release with basic pattern recognition and documentation generation
- **1.1.0**: Added advanced pattern detection algorithms and refactoring recommendations
- **1.2.0**: Enhanced integration with development tools and architecture analysis
- **1.3.0**: Improved performance optimization and incremental analysis capabilities
- **1.4.0**: Advanced machine learning-based pattern recognition and intelligent recommendations

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.