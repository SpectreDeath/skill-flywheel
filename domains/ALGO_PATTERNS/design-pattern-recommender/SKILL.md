---
Domain: ALGO_PATTERNS
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: design-pattern-recommender
---



## Description

Automatically recommends appropriate design patterns based on problem characteristics, constraints, and requirements. This skill analyzes problem domains, object relationships, behavioral patterns, and architectural needs to suggest optimal design patterns from creational, structural, and behavioral categories with implementation guidance and trade-off analysis.


## Purpose

*[Content for Purpose section to be added based on the specific skill requirements]*

## Examples

*[Content for Examples section to be added based on the specific skill requirements]*

## Implementation Notes

*[Content for Implementation Notes section to be added based on the specific skill requirements]*
## Capabilities

- **Problem Domain Analysis**: Analyze problem characteristics to identify suitable design pattern categories
- **Pattern Matching**: Match problem requirements to established design patterns with confidence scoring
- **Relationship Analysis**: Analyze object interactions, dependencies, and composition patterns
- **Architectural Pattern Recognition**: Identify system-level patterns for large-scale design
- **Implementation Guidance**: Provide detailed implementation examples and best practices
- **Trade-off Analysis**: Evaluate pattern benefits, drawbacks, and complexity implications
- **Pattern Combination**: Recommend combinations of patterns for complex scenarios

## Usage Examples

### Creational Pattern Recommendation

```yaml
creational_pattern_recommendation:
  problem_context:
    problem_type: "object_creation"
    requirements:
      - "Control object instantiation"
      - "Ensure single instance"
      - "Lazy initialization"
      - "Thread safety"
    
    constraints:
      - "Memory efficiency"
      - "Performance critical"
      - "Configuration flexibility"
  
  pattern_candidates:
    - pattern: "Singleton"
      confidence_score: 0.95
      applicability: "high"
      benefits:
        - "Guaranteed single instance"
        - "Lazy initialization"
        - "Thread safety"
      drawbacks:
        - "Global state"
        - "Testing complexity"
        - "Tight coupling"
      implementation:
        - "Private constructor"
        - "Static instance variable"
        - "Thread-safe getInstance() method"
        - "Lazy initialization with double-checked locking"
    
    - pattern: "Factory Method"
      confidence_score: 0.75
      applicability: "medium"
      benefits:
        - "Subclass customization"
        - "Loose coupling"
        - "Extensibility"
      drawbacks:
        - "Additional classes"
        - "Complexity overhead"
  
  recommended_pattern: "Singleton"
  justification: "Single instance requirement with thread safety and lazy initialization"
  implementation_complexity: "low"
```

### Behavioral Pattern Analysis

```yaml
behavioral_pattern_analysis:
  problem_context:
    problem_type: "object communication"
    requirements:
      - "Loose coupling between objects"
      - "Multiple interested objects"
      - "Dynamic subscription"
      - "Event-driven architecture"
    
    object_relationships:
      - "One-to-many relationship"
      - "Subject-observer pattern"
      - "Push vs pull notification"
  
  pattern_evaluation:
    - pattern: "Observer"
      confidence_score: 0.98
      pattern_type: "behavioral"
      core_concept: "Publish-subscribe mechanism"
      key_components:
        - "Subject (Observable)"
        - "Observers (Subscribers)"
        - "Notification mechanism"
      implementation_approaches:
        - "Push model: Subject pushes data to observers"
        - "Pull model: Observers pull data from subject"
        - "Event-driven: Using event queues and handlers"
      
      benefits:
        - "Loose coupling"
        - "Dynamic relationships"
        - "Broadcast communication"
      tradeoffs:
        - "Memory overhead for observer lists"
        - "Potential for memory leaks"
        - "Notification order not guaranteed"
    
    - pattern: "Mediator"
      confidence_score: 0.65
      pattern_type: "behavioral"
      core_concept: "Centralized communication control"
      benefits:
        - "Reduced direct coupling"
        - "Centralized control"
        - "Simplified object protocols"
      tradeoffs:
        - "Mediator becomes central point"
        - "Potential performance bottleneck"
  
  recommended_pattern: "Observer"
  implementation_strategy:
    - "Interface-based design"
    - "Weak references for memory management"
    - "Thread-safe notification mechanism"
    - "Event filtering and prioritization"
```

### Structural Pattern Selection

```yaml
structural_pattern_selection:
  problem_context:
    problem_type: "object composition"
    requirements:
      - "Interface compatibility"
      - "Dynamic behavior addition"
      - "Simplified interface"
      - "Component aggregation"
    
    existing_system:
      - "Legacy interfaces"
      - "Multiple implementations"
      - "Complex hierarchies"
  
  pattern_recommendations:
    - pattern: "Adapter"
      confidence_score: 0.90
      pattern_type: "structural"
      use_case: "Interface compatibility"
      implementation:
        - "Object adapter: Composition-based"
        - "Class adapter: Inheritance-based"
        - "Two-way adapter: Bidirectional conversion"
      benefits:
        - "Reuses existing classes"
        - "No modification required"
        - "Interface standardization"
      considerations:
        - "Performance overhead"
        - "Complexity in adapter hierarchy"
    
    - pattern: "Decorator"
      confidence_score: 0.85
      pattern_type: "structural"
      use_case: "Dynamic behavior addition"
      implementation:
        - "Component interface"
        - "Concrete component"
        - "Decorator base class"
        - "Concrete decorators"
      benefits:
        - "Flexible functionality addition"
        - "No subclass explosion"
        - "Runtime behavior modification"
      considerations:
        - "Multiple wrapper layers"
        - "Potential performance impact"
    
    - pattern: "Facade"
      confidence_score: 0.80
      pattern_type: "structural"
      use_case: "Simplified interface"
      implementation:
        - "Facade class"
        - "Subsystem classes"
        - "Unified interface"
      benefits:
        - "Simplified client interface"
        - "Reduced dependencies"
        - "Layered architecture support"
      considerations:
        - "Potential single point of failure"
        - "May hide useful functionality"
  
  recommended_patterns:
    - "Primary: Adapter (for legacy integration)"
    - "Secondary: Decorator (for dynamic features)"
    - "Tertiary: Facade (for simplified access)"
```

## Input Format

### Pattern Recommendation Request

```yaml
pattern_recommendation_request:
  problem_id: string              # Unique problem identifier
  problem_description: string     # Natural language problem description
  domain_context: string          # Application domain (web, mobile, enterprise, etc.)
  
  problem_characteristics:
    problem_type: "creational|structural|behavioral|architectural"
    complexity_level: "simple|medium|complex"
    scale: "small|medium|large"
    performance_requirements: object
    maintainability_requirements: object
    extensibility_requirements: object
  
  constraints:
    technology_stack: array       # Programming languages, frameworks
    architectural_constraints: array
    performance_constraints: object
    resource_constraints: object
  
  existing_system:
    current_patterns: array       # Already used patterns
    system_complexity: string
    integration_requirements: array
    legacy_systems: array
```

### Pattern Analysis Schema

```yaml
pattern_analysis:
  domain_analysis:
    business_domain: string       # Industry/domain specific
    problem_domain: string        # Technical problem domain
    user_requirements: array      # Functional requirements
    system_requirements: array    # Non-functional requirements
  
  relationship_analysis:
    object_interactions: array    # How objects interact
    dependency_patterns: array    # Dependency relationships
    communication_patterns: array # Communication mechanisms
    data_flow_patterns: array     # Data movement patterns
  
  pattern_matching:
    candidate_patterns: array     # Potential patterns
    matching_criteria: object     # Criteria for pattern selection
    confidence_scores: object     # Confidence in pattern recommendations
    tradeoff_analysis: object     # Benefits vs drawbacks
```

## Output Format

### Pattern Recommendation Report

```yaml
pattern_recommendation_report:
  problem_id: string
  recommendation_timestamp: timestamp
  analysis_confidence: number     # Overall confidence score
  
  recommended_patterns:
    - pattern_name: string
      pattern_type: "creational|structural|behavioral|architectural"
      confidence_score: number    # 0.0 to 1.0
      applicability: "high|medium|low"
      
      pattern_details:
        intent: string            # Pattern purpose
        motivation: string        # Why this pattern
        structure: object         # Class/object diagram description
        participants: array       # Key classes and roles
        collaborations: array     # How participants interact
      
      implementation_guidance:
        key_components: array     # Essential classes/interfaces
        implementation_steps: array
        best_practices: array
        common_mistakes: array
      
      tradeoff_analysis:
        benefits: array
        drawbacks: array
        complexity_impact: string
        performance_impact: string
      
      variations:
        - variation_name: string
        - variation_description: string
        - when_to_use: string
      
      related_patterns:
        - pattern_name: string
        - relationship: string
        - combination_benefits: array
  
  pattern_combinations:
    - combination_name: string
      patterns: array
      synergy_benefits: array
      implementation_order: array
      complexity_assessment: string
  
  implementation_examples:
    - language: string
      code_example: string
      explanation: string
      variations: array
```

### Pattern Implementation Blueprint

```yaml
implementation_blueprint:
  pattern_name: string
  architecture_overview: string
  class_diagram: object           # UML class diagram description
  
  core_components:
    - component_name: string
      component_type: "class|interface|abstract_class"
      responsibilities: array
      dependencies: array
      collaborators: array
  
  implementation_phases:
    - phase: "foundation"
      tasks: array
      deliverables: array
      validation_criteria: array
    
    - phase: "integration"
      tasks: array
      deliverables: array
      validation_criteria: array
    
    - phase: "optimization"
      tasks: array
      deliverables: array
      validation_criteria: array
  
  testing_strategy:
    unit_tests: array
    integration_tests: array
    pattern_validation_tests: array
    performance_tests: array
  
  deployment_considerations:
    configuration_requirements: array
    runtime_dependencies: array
    monitoring_requirements: array
    rollback_procedures: array
```

## Configuration Options

### Pattern Categories

```yaml
pattern_categories:
  creational:
    singleton: "enabled"
    factory_method: "enabled"
    abstract_factory: "enabled"
    builder: "enabled"
    prototype: "enabled"
    object_pool: "enabled"
  
  structural:
    adapter: "enabled"
    bridge: "enabled"
    composite: "enabled"
    decorator: "enabled"
    facade: "enabled"
    flyweight: "enabled"
    proxy: "enabled"
  
  behavioral:
    chain_of_responsibility: "enabled"
    command: "enabled"
    interpreter: "enabled"
    iterator: "enabled"
    mediator: "enabled"
    memento: "enabled"
    observer: "enabled"
    state: "enabled"
    strategy: "enabled"
    template_method: "enabled"
    visitor: "enabled"
  
  architectural:
    mvc: "enabled"
    mvp: "enabled"
    mvvm: "enabled"
    layered: "enabled"
    microservices: "enabled"
    event_driven: "enabled"
```

### Analysis Parameters

```yaml
analysis_parameters:
  confidence_thresholds:
    high: 0.8
    medium: 0.6
    low: 0.4
  
  complexity_weights:
    implementation_complexity: 0.3
    maintenance_complexity: 0.4
    performance_complexity: 0.3
  
  domain_specific_weights:
    enterprise: { scalability: 0.4, maintainability: 0.4, performance: 0.2 }
    web: { scalability: 0.3, performance: 0.4, maintainability: 0.3 }
    mobile: { performance: 0.5, battery_efficiency: 0.3, maintainability: 0.2 }
    embedded: { performance: 0.6, memory_efficiency: 0.3, maintainability: 0.1 }
```

## Error Handling

### Recommendation Failures

```yaml
recommendation_failures:
  no_suitable_pattern:
    retry_strategy: "expand_search_scope"
    max_retries: 2
    fallback_action: "custom_pattern_design"
  
  ambiguous_requirements:
    retry_strategy: "requirement_clarification"
    max_retries: 3
    fallback_action: "multiple_pattern_recommendation"
  
  conflicting_constraints:
    retry_strategy: "constraint_prioritization"
    max_retries: 2
    fallback_action: "hybrid_pattern_approach"
  
  implementation_complexity_high:
    retry_strategy: "simplification"
    max_retries: 2
    fallback_action: "alternative_pattern_recommendation"
```

### Analysis Errors

```yaml
analysis_errors:
  insufficient_domain_knowledge:
    detection_strategy: "domain_coverage_analysis"
    recovery_strategy: "external_pattern_database"
    escalation: "expert_consultation"
  
  pattern_conflicts:
    detection_strategy: "pattern_compatibility_check"
    recovery_strategy: "conflict_resolution"
    escalation: "architectural_review"
  
  performance_prediction_inaccurate:
    detection_strategy: "empirical_validation"
    recovery_strategy: "performance_profiling"
    escalation: "algorithm_redesign"
```

## Performance Optimization

### Pattern Selection Optimization

```yaml
pattern_selection_optimization:
  caching_strategy: "enabled"
  pattern_database_optimization: true
  matching_algorithm_optimization: true
  recommendation_engine_optimization: true
  
  optimization_techniques:
    - technique: "pattern_similarity_matching"
      applicable_to: ["pattern_matching", "recommendation_engine"]
      performance_gain: "significant"
      memory_overhead: "minimal"
    
    - technique: "domain_specific_optimization"
      applicable_to: ["pattern_selection", "analysis_engine"]
      performance_gain: "moderate"
      memory_overhead: "low"
    
    - technique: "parallel_pattern_analysis"
      applicable_to: ["pattern_evaluation", "recommendation_generation"]
      performance_gain: "linear"
      memory_overhead: "moderate"
```

### Implementation Optimization

```yaml
implementation_optimization:
  pattern_implementation_optimization: true
  code_generation_optimization: true
  performance_monitoring: true
  memory_optimization: true
  
  optimization_strategies:
    - strategy: "lazy_initialization"
      applicable_patterns: ["singleton", "factory", "prototype"]
      benefits: ["memory_efficiency", "startup_performance"]
      tradeoffs: ["runtime_overhead", "complexity"]
    
    - strategy: "object_pooling"
      applicable_patterns: ["prototype", "factory", "singleton"]
      benefits: ["reduced_allocation", "improved_performance"]
      tradeoffs: ["memory_usage", "complexity"]
    
    - strategy: "caching_mechanisms"
      applicable_patterns: ["proxy", "decorator", "facade"]
      benefits: ["reduced_computation", "improved_response_time"]
      tradeoffs: ["memory_usage", "staleness"]
```

## Integration Examples

### With Development Frameworks

```yaml
framework_integration:
  java_spring:
    pattern_support: ["singleton", "factory", "proxy", "observer"]
    integration_level: "native"
    configuration_examples: "available"
  
  .net_framework:
    pattern_support: ["singleton", "factory", "adapter", "decorator"]
    integration_level: "native"
    configuration_examples: "available"
  
  javascript_react:
    pattern_support: ["observer", "strategy", "composite", "decorator"]
    integration_level: "framework_agnostic"
    configuration_examples: "available"
  
  python_django:
    pattern_support: ["singleton", "factory", "adapter", "observer"]
    integration_level: "framework_agnostic"
    configuration_examples: "available"
```

### With Architecture Tools

```yaml
architecture_tool_integration:
  uml_tools:
    class_diagram_generation: "enabled"
    sequence_diagram_generation: "enabled"
    component_diagram_generation: "enabled"
  
  architecture_analysis_tools:
    pattern_detection: "enabled"
    pattern_validation: "enabled"
    architecture_compliance: "enabled"
  
  code_analysis_tools:
    pattern_usage_analysis: "enabled"
    pattern_violation_detection: "enabled"
    refactoring_suggestions: "enabled"
```

## Best Practices

1. **Pattern Selection**:
   - Analyze problem requirements thoroughly before selecting patterns
   - Consider both immediate and future requirements
   - Evaluate trade-offs between complexity and benefits
   - Choose patterns that align with team expertise

2. **Implementation**:
   - Follow established pattern implementations and best practices
   - Use appropriate abstraction levels
   - Implement proper error handling and validation
   - Document pattern usage and rationale

3. **Integration**:
   - Ensure patterns work well together without conflicts
   - Maintain consistency in pattern application
   - Consider performance implications of pattern choices
   - Plan for pattern evolution and refactoring

4. **Maintenance**:
   - Monitor pattern effectiveness over time
   - Update pattern implementations as needed
   - Document pattern modifications and reasons
   - Train team members on pattern usage

## Troubleshooting

### Common Issues

1. **Pattern Overuse**: Review pattern necessity, consider simpler solutions, evaluate complexity overhead
2. **Pattern Conflicts**: Analyze pattern interactions, resolve conflicts through architectural changes
3. **Performance Issues**: Profile pattern implementations, optimize critical paths, consider alternative patterns
4. **Maintenance Complexity**: Simplify pattern implementations, improve documentation, provide training
5. **Integration Problems**: Review pattern compatibility, ensure proper interfaces, validate assumptions

### Debug Mode

```yaml
debug_config:
  enabled: true
  log_level: "debug"
  pattern_matching_debugging: true
  recommendation_engine_debugging: true
  implementation_validation_debugging: true
  performance_monitoring_debugging: true
```

## Monitoring and Metrics

### Key Performance Indicators

```yaml
kpi_metrics:
  recommendation_quality:
    accuracy_score: number
    user_satisfaction: number
    pattern_success_rate: number
    implementation_success_rate: number
  
  system_performance:
    recommendation_time: number
    analysis_time: number
    memory_usage: number
    scalability_metrics: object
  
  pattern_effectiveness:
    pattern_utilization_rate: number
    pattern_performance_impact: number
    pattern_maintainability_impact: number
    pattern_reusability_score: number
```

## Dependencies

- **Pattern Databases**: Comprehensive collections of design patterns with implementations
- **Architecture Analysis Tools**: Tools for analyzing system architecture and pattern usage
- **Code Analysis Frameworks**: Static analysis tools for pattern detection and validation
- **Performance Profiling Tools**: Tools for measuring pattern performance impact
- **Documentation Generation Tools**: Tools for generating pattern documentation and examples

## Version History

- **1.0.0**: Initial release with basic pattern recommendation and analysis
- **1.1.0**: Added advanced pattern matching and trade-off analysis
- **1.2.0**: Enhanced integration with development frameworks and tools
- **1.3.0**: Improved performance optimization and implementation guidance
- **1.4.0**: Advanced machine learning-based pattern recommendation and pattern combination analysis

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

Content for ## Constraints involving Design Pattern Recommender.