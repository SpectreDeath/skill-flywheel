---
Domain: logic_programming
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: constraint-satisfaction-sat-solvers
---



## Description

Automatically designs, implements, and optimizes constraint satisfaction problems (CSP) and Boolean satisfiability (SAT) solvers for complex logical problems. This skill provides comprehensive support for constraint modeling, solver selection, optimization techniques, and integration with logic programming frameworks for solving NP-hard problems efficiently.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Constraint Problem Modeling**: Automatically model complex problems as constraint satisfaction problems with appropriate variable domains and constraints
- **SAT Solver Selection & Configuration**: Select and configure optimal SAT solvers (MiniSat, Z3, CVC4, etc.) based on problem characteristics
- **Constraint Propagation**: Implement advanced constraint propagation techniques for efficient search space reduction
- **Search Strategy Optimization**: Design and optimize search strategies including variable ordering, value selection, and backtracking
- **Problem Decomposition**: Decompose complex problems into smaller, solvable subproblems with coordination mechanisms
- **Parallel & Distributed Solving**: Implement parallel and distributed solving strategies for large-scale problems
- **Solution Verification**: Verify solutions and provide explanations for constraint satisfaction results

## Usage Examples

### Constraint Satisfaction Problem Modeling

```yaml
constraint_satisfaction_modeling:
  problem_domain: "University Course Scheduling"
  problem_complexity: "NP-hard"
  variables_count: 5000
  constraints_count: 15000
  
  variable_definition:
    - variable: "course_assignment"
      domain: "time_slots x classrooms"
      cardinality: 2000
      constraints: ["no_overlap", "capacity", "prerequisites"]
    
    - variable: "instructor_assignment"
      domain: "courses x time_slots"
      cardinality: 1000
      constraints: ["workload_limit", "availability", "expertise"]
    
    - variable: "student_schedule"
      domain: "courses x time_slots"
      cardinality: 2000
      constraints: ["no_conflicts", "graduation_requirements"]
  
  constraint_definition:
    - constraint: "no_overlap"
      type: "binary_constraint"
      scope: ["course_assignment", "course_assignment"]
      implementation: "AllDifferent(time_slot) for same classroom"
      propagation: "arc_consistency"
    
    - constraint: "capacity"
      type: "global_constraint"
      scope: ["course_assignment", "classroom_capacity"]
      implementation: "Cumulative constraint for room capacity"
      propagation: "bound_consistency"
    
    - constraint: "prerequisites"
      type: "precedence_constraint"
      scope: ["course_assignment", "prerequisite_courses"]
      implementation: "Time slot ordering constraints"
      propagation: "path_consistency"
  
  objective_function:
    - objective: "minimize_conflicts"
      type: "soft_constraint"
      weight: 10
      implementation: "Penalty for student schedule conflicts"
    
    - objective: "maximize_resource_utilization"
      type: "soft_constraint"
      weight: 5
      implementation: "Reward for efficient room usage"
  
  solver_configuration:
    solver_type: "CP-SAT"
    search_strategy: "first_fail"
    value_selection: "min_conflict"
    restart_strategy: "geometric"
    parallel_search: 8
```

### SAT Solver Implementation

```yaml
sat_solver_implementation:
  problem_domain: "Circuit Verification"
  sat_solver: "Z3"
  problem_size: "1000000 variables, 5000000 clauses"
  
  problem_encoding:
    - encoding: "CNF_conversion"
      technique: "Tseitin transformation"
      complexity: "Linear in circuit size"
      optimization: "Clause learning"
    
    - encoding: "Pseudo_boolean_constraints"
      technique: "Binary decision diagrams"
      complexity: "Exponential in worst case"
      optimization: "BDD minimization"
    
    - encoding: "Theory_combination"
      technique: "SMT with bitvector theory"
      complexity: "Depends on theory"
      optimization: "Theory-specific solvers"
  
  solver_configuration:
    solver_engine: "Z3"
    tactic: "smt"
    logic: "QF_BV"
    timeout: "3600 seconds"
    memory_limit: "16GB"
    
    optimization_settings:
      - setting: "sat_core_minimization"
        value: "true"
        purpose: "Minimize unsatisfiable cores"
      
      - setting: "conflict_analysis"
        value: "true"
        purpose: "Improve conflict-driven clause learning"
      
      - setting: "restart_strategy"
        value: "luby"
        purpose: "Optimize restart intervals"
  
  constraint_propagation:
    - propagation: "Unit_propagation"
      implementation: "Boolean constraint propagation"
      complexity: "O(n)"
      benefit: "Fast conflict detection"
    
    - propagation: "Watched_literals"
      implementation: "Efficient clause watching"
      complexity: "O(1) per literal"
      benefit: "Reduced propagation overhead"
    
    - propagation: "Theory_propagation"
      implementation: "Theory-specific propagation"
      complexity: "Theory-dependent"
      benefit: "Stronger propagation"
  
  performance_optimization:
    - optimization: "Clause_learning"
      technique: "Learn from conflicts"
      benefit: "Avoid repeating conflicts"
      implementation: "CDCL algorithm"
    
    - optimization: "Variable_elimination"
      technique: "Eliminate variables early"
      benefit: "Reduce problem size"
      implementation: "Bounded variable elimination"
    
    - optimization: "Symmetry_breaking"
      technique: "Break problem symmetries"
      benefit: "Reduce search space"
      implementation: "Lexicographic ordering constraints"
```

### Advanced Constraint Programming

```yaml
advanced_constraint_programming:
  problem_domain: "Cryptarithmetic Puzzles"
  constraint_framework: "MiniZinc with Gecode"
  
  model_definition:
    variables:
      - variable: "letters"
        domain: "0..9"
        cardinality: 10
        type: "integer"
      
      - variable: "carry"
        domain: "0..1"
        cardinality: 4
        type: "binary"
    
    constraints:
      - constraint: "all_different"
        scope: ["letters"]
        implementation: "Global all_different constraint"
        propagation: "domain_consistency"
      
      - constraint: "arithmetic_relation"
        scope: ["letters", "carry"]
        implementation: "Linear arithmetic constraints"
        propagation: "bound_consistency"
      
      - constraint: "leading_digit_nonzero"
        scope: ["leading_letters"]
        implementation: "Inequality constraints"
        propagation: "simple_consistency"
    
    search_strategy:
      - strategy: "variable_ordering"
        technique: "Most constrained variable"
        heuristic: "Minimum remaining values"
      
      - strategy: "value_ordering"
        technique: "Least constraining value"
        heuristic: "Maximize remaining options"
      
      - strategy: "search_restart"
        technique: "Geometric restart"
        parameters: "base=1.5, max_restarts=100"
  
  optimization_techniques:
    - technique: "Symmetry_breaking"
      implementation: "Order constraints on symmetric variables"
      benefit: "Exponential search space reduction"
    
    - technique: "Redundant_constraints"
      implementation: "Add implied constraints"
      benefit: "Improved propagation"
    
    - technique: "Global_constraint_decomposition"
      implementation: "Decompose complex constraints"
      benefit: "Better propagation algorithms"
  
  parallel_solving:
    - approach: "Portfolio_method"
      implementation: "Multiple solvers with different strategies"
      benefit: "Robustness across problem types"
    
    - approach: "Parallel_search_trees"
      implementation: "Explore different branches in parallel"
      benefit: "Speedup for tree search"
    
    - approach: "Constraint_decomposition"
      implementation: "Solve subproblems in parallel"
      benefit: "Scalability for large problems"
```

## Input Format

### Constraint Problem Definition

```yaml
constraint_problem_definition:
  problem_name: string            # Name of the constraint problem
  problem_type: "CSP|SAT|SMT|CP"  # Type of constraint problem
  problem_complexity: "P|NP|PSPACE" # Computational complexity class
  
  variables:
    - variable_name: string       # Name of the variable
      domain: object              # Domain definition (range, values, etc.)
      type: "integer|boolean|real|finite_domain" # Variable type
      cardinality: number         # Number of possible values
      constraints: array          # Constraints involving this variable
  
  constraints:
    - constraint_name: string     # Name of the constraint
      type: "unary|binary|global|soft" # Type of constraint
      scope: array                # Variables involved in constraint
      implementation: string      # How constraint is implemented
      propagation: string         # Propagation technique used
      weight: number              # Weight for soft constraints
  
  objectives:
    - objective_name: string      # Name of objective
      type: "minimize|maximize"   # Optimization direction
      expression: string          # Objective function expression
      priority: number            # Priority level for multi-objective
  
  solver_requirements:
    solver_type: string           # Type of solver needed
    performance_requirements: object # Performance constraints
    memory_requirements: object   # Memory constraints
    parallel_support: boolean     # Whether parallel solving is needed
```

### SAT Problem Encoding

```yaml
sat_problem_encoding:
  encoding_strategy: "CNF|DNF|SMT|Hybrid"
  variable_mapping: object        # Mapping from problem variables to SAT variables
  clause_generation: object       # Strategy for generating clauses
  
  encoding_techniques:
    - technique: "Tseitin_transformation"
      purpose: "Convert circuits to CNF"
      complexity: "Linear"
      benefits: "Preserves satisfiability"
    
    - technique: "Binary_encoding"
      purpose: "Encode integer variables"
      complexity: "Logarithmic"
      benefits: "Compact representation"
    
    - technique: "Unary_encoding"
      purpose: "Encode integer variables"
      complexity: "Linear"
      benefits: "Better propagation"
  
  optimization_strategies:
    - strategy: "Clause_learning"
      technique: "Learn from conflicts"
      implementation: "CDCL algorithm"
    
    - strategy: "Variable_elimination"
      technique: "Remove redundant variables"
      implementation: "Bounded elimination"
    
    - strategy: "Symmetry_breaking"
      technique: "Add symmetry-breaking constraints"
      implementation: "Lexicographic ordering"
```

## Output Format

### Constraint Solver Configuration

```yaml
constraint_solver_configuration:
  selected_solver: string
  configuration_timestamp: timestamp
  problem_characteristics: object
  solver_performance: object
  
  solver_settings:
    search_strategy: string       # Search strategy configuration
    variable_ordering: string     # Variable ordering heuristic
    value_selection: string       # Value selection heuristic
    restart_strategy: string      # Restart strategy configuration
    parallel_config: object       # Parallel solving configuration
  
  performance_metrics:
    solving_time: number          # Time to solve the problem
    memory_usage: number          # Peak memory usage
    search_nodes: number          # Number of search nodes explored
    constraint_checks: number     # Number of constraint checks performed
  
  solution_quality:
    solution_found: boolean       # Whether a solution was found
    solution_optimality: string   # Optimality status of solution
    solution_verification: object # Verification results
    explanation: string           # Explanation of solution
```

### SAT Solver Report

```yaml
sat_solver_report:
  problem_encoding: object        # Details of problem encoding
  solver_configuration: object    # SAT solver configuration
  solving_statistics: object      # Statistics from solving process
  
  encoding_details:
    variables_count: number       # Number of SAT variables
    clauses_count: number         # Number of clauses
    encoding_time: number         # Time to encode problem
    encoding_size: string         # Size of encoded problem
  
  solving_details:
    decisions: number             # Number of decisions made
    conflicts: number             # Number of conflicts encountered
    propagations: number          # Number of propagations
    restarts: number              # Number of restarts
  
  performance_analysis:
    solving_time: number          # Total solving time
    memory_peak: number           # Peak memory usage
    cpu_usage: number             # CPU usage percentage
    parallel_efficiency: number   # Efficiency of parallel solving
```

## Configuration Options

### Solver Selection Criteria

```yaml
solver_selection_criteria:
  sat_solvers:
    minisat:
      best_for: ["pure_sat_problems", "small_to_medium_problems"]
      performance: "excellent"
      memory_usage: "low"
      parallel_support: false
    
    z3:
      best_for: ["smt_problems", "theory_combinations"]
      performance: "very_good"
      memory_usage: "medium"
      parallel_support: true
    
    cvc4:
      best_for: ["smt_problems", "quantified_formulas"]
      performance: "very_good"
      memory_usage: "medium"
      parallel_support: true
  
  cp_solvers:
    gecode:
      best_for: ["finite_domain_problems", "global_constraints"]
      performance: "excellent"
      memory_usage: "low"
      parallel_support: true
    
    choco:
      best_for: ["java_integration", "constraint_programming"]
      performance: "good"
      memory_usage: "medium"
      parallel_support: true
    
    or_tools:
      best_for: ["optimization_problems", "industrial_applications"]
      performance: "very_good"
      memory_usage: "medium"
      parallel_support: true
```

### Performance Optimization Strategies

```yaml
performance_optimization_strategies:
  search_optimizations:
    - optimization: "Variable_ordering"
      techniques: ["mrv", "degree", "dom/deg"]
      impact: "High"
      complexity: "Low"
    
    - optimization: "Value_ordering"
      techniques: ["least_constraining", "max_regret"]
      impact: "Medium"
      complexity: "Low"
    
    - optimization: "Restart_strategies"
      techniques: ["geometric", "luby", "linear"]
      impact: "High"
      complexity: "Low"
  
  Propagation_optimizations:
    - optimization: "Constraint_propagation"
      techniques: ["arc_consistency", "path_consistency", "bound_consistency"]
      impact: "Very High"
      complexity: "Medium"
    
    - optimization: "Watched_literals"
      techniques: ["two_watched_literals", "lazy_propagation"]
      impact: "High"
      complexity: "Low"
    
    - optimization: "Global_constraints"
      techniques: ["decomposition", "specialized_algorithms"]
      impact: "Very High"
      complexity: "High"
```

## Error Handling

### Constraint Problem Failures

```yaml
constraint_problem_failures:
  unsatisfiable_problem:
    retry_strategy: "problem_analysis"
    max_retries: 1
    fallback_action: "relax_constraints"
  
  performance_issues:
    retry_strategy: "optimization_application"
    max_retries: 3
    fallback_action: "problem_decomposition"
  
  memory_exhaustion:
    retry_strategy: "memory_optimization"
    max_retries: 2
    fallback_action: "incremental_solving"
  
  solver_timeout:
    retry_strategy: "strategy_change"
    max_retries: 2
    fallback_action: "approximate_solving"
```

### SAT Solver Failures

```yaml
sat_solver_failures:
  encoding_failure:
    retry_strategy: "encoding_redesign"
    max_retries: 2
    fallback_action: "alternative_encoding"
  
  solver_crash:
    retry_strategy: "solver_restart"
    max_retries: 3
    fallback_action: "alternative_solver"
  
  memory_limit_exceeded:
    retry_strategy: "memory_optimization"
    max_retries: 2
    fallback_action: "incremental_solving"
  
  timeout_exceeded:
    retry_strategy: "strategy_optimization"
    max_retries: 2
    fallback_action: "partial_solving"
```

## Performance Optimization

### Advanced Search Strategies

```yaml
advanced_search_strategies:
  learning_based_search:
    - strategy: "Conflict_driven_search"
      technique: "Learn from conflicts to guide search"
      implementation: "CDCL with clause learning"
      benefit: "Avoid repeating conflicts"
    
    - strategy: "Heuristic_learning"
      technique: "Learn good heuristics from experience"
      implementation: "Reinforcement learning"
      benefit: "Adaptive search strategies"
  
  Decomposition_based_search:
    - strategy: "Problem_decomposition"
      technique: "Break problem into smaller subproblems"
      implementation: "Constraint decomposition"
      benefit: "Parallel solving opportunities"
    
    - strategy: "Hierarchical_search"
      technique: "Solve at different abstraction levels"
      implementation: "Abstract interpretation"
      benefit: "Faster convergence"
  
  Parallel_search_strategies:
    - strategy: "Portfolio_method"
      technique: "Run multiple solvers in parallel"
      implementation: "Different strategies/configurations"
      benefit: "Robustness across problem types"
    
    - strategy: "Parallel_tree_search"
      technique: "Explore search tree in parallel"
      implementation: "Work stealing"
      benefit: "Speedup for tree search"
```

### Memory Optimization

```yaml
memory_optimization:
  garbage_collection:
    - strategy: "Incremental_gc"
      technique: "Collect garbage incrementally"
      benefit: "Reduced pause times"
      implementation: "Generational garbage collection"
    
    - strategy: "Reference_counting"
      technique: "Track object references"
      benefit: "Immediate memory reclamation"
      implementation: "Automatic reference counting"
  
  Memory_pooling:
    - technique: "Object_pooling"
      implementation: "Reuse frequently allocated objects"
      benefit: "Reduced allocation overhead"
    
    - technique: "Memory_mapping"
      implementation: "Map large datasets to memory"
      benefit: "Efficient large-scale data handling"
  
  Incremental_solving:
    - technique: "Incremental_constraints"
      implementation: "Add constraints incrementally"
      benefit: "Reuse previous solving state"
    
    - technique: "Assumption_based_solving"
      implementation: "Use assumptions for incremental solving"
      benefit: "Faster solving for related problems"
```

## Integration Examples

### With Logic Programming Frameworks

```yaml
logic_programming_integration:
  prolog_integration:
    constraint_logic_programming: "CLP(FD), CLP(R)"
    integration_method: "Native Prolog constraints"
    benefits: "Declarative constraint solving"
    use_cases: ["Scheduling", "Planning", "Verification"]
  
  datalog_integration:
    constraint_datalog: "Datalog with constraints"
    integration_method: "Extended Datalog engines"
    benefits: "Recursive constraint solving"
    use_cases: ["Static analysis", "Database queries", "Network analysis"]
  
  minikanren_integration:
    constraint_minikanren: "core.logic with constraints"
    integration_method: "Relational constraint programming"
    benefits: "Relational constraint solving"
    use_cases: ["Program synthesis", "Type inference", "Verification"]
```

### With Optimization Frameworks

```yaml
optimization_framework_integration:
  mathematical_optimization:
    integration: "Mixed Integer Programming (MIP)"
    benefits: "Linear and integer constraints"
    tools: ["CPLEX", "Gurobi", "CBC"]
    use_cases: ["Resource allocation", "Scheduling", "Planning"]
  
  metaheuristics:
    integration: "Hybrid constraint-metaheuristic"
    benefits: "Scalability for large problems"
    tools: ["Genetic algorithms", "Simulated annealing", "Tabu search"]
    use_cases: ["Combinatorial optimization", "Large-scale scheduling"]
  
  machine_learning:
    integration: "Learning-based constraint solving"
    benefits: "Adaptive solving strategies"
    tools: ["Reinforcement learning", "Neural networks"]
    use_cases: ["Heuristic learning", "Problem classification"]
```

## Best Practices

1. **Problem Modeling**:
   - Choose appropriate variable domains and representations
   - Use global constraints when available
   - Add redundant constraints for better propagation
   - Break symmetries to reduce search space

2. **Solver Selection**:
   - Match solver capabilities to problem characteristics
   - Consider hybrid approaches for complex problems
   - Evaluate solver performance on representative instances
   - Plan for scalability and maintainability

3. **Search Strategy Design**:
   - Use informed variable and value ordering
   - Implement effective restart strategies
   - Consider parallel and distributed solving
   - Monitor and adapt search strategies

4. **Performance Optimization**:
   - Profile solver performance to identify bottlenecks
   - Use appropriate data structures and algorithms
   - Implement efficient constraint propagation
   - Consider incremental solving for related problems

## Troubleshooting

### Common Issues

1. **Performance Problems**: Analyze search strategy, improve constraint propagation, consider problem decomposition, use parallel solving
2. **Memory Issues**: Implement memory optimization, use incremental solving, consider problem size reduction, monitor memory usage
3. **Solution Quality**: Verify constraint correctness, check objective function, validate solution, implement solution verification
4. **Scalability Issues**: Use decomposition techniques, implement parallel solving, consider approximation algorithms, optimize data structures
5. **Integration Problems**: Verify API compatibility, check data format conversions, validate constraint handling, test integration thoroughly

### Debug Mode

```yaml
debug_config:
  enabled: true
  log_level: "debug"
  constraint_debugging: true
  solver_debugging: true
  search_debugging: true
  performance_debugging: true
```

## Monitoring and Metrics

### Key Performance Indicators

```yaml
kpi_metrics:
  solving_performance:
    solving_time: number          # Average solving time
    success_rate: number          # Percentage of problems solved
    scalability_metrics: object   # Performance scaling with problem size
    parallel_efficiency: number   # Efficiency of parallel solving
  
  solution_quality:
    solution_optimality: number   # Quality of solutions found
    constraint_satisfaction_rate: number # Percentage of constraints satisfied
    objective_value: number       # Value of objective function
    solution_diversity: number    # Diversity of solutions found
  
  system_reliability:
    solver_stability: number      # Stability of solver performance
    memory_efficiency: number     # Memory usage efficiency
    error_recovery_time: number   # Time to recover from errors
    integration_stability: number # Stability of integrations
```

## Dependencies

- **SAT Solvers**: MiniSat, Z3, CVC4, Glucose, Lingeling
- **CP Solvers**: Gecode, Choco, OR-Tools, JaCoP
- **SMT Solvers**: Z3, CVC4, Yices, MathSAT
- **Optimization Libraries**: SCIP, CBC, Gurobi, CPLEX
- **Integration Frameworks**: MiniZinc, OMT, Z3Py, PySMT

## Version History

- **1.0.0**: Initial release with basic constraint satisfaction and SAT solving
- **1.1.0**: Added advanced constraint propagation and optimization techniques
- **1.2.0**: Enhanced parallel and distributed solving capabilities
- **1.3.0**: Improved integration with logic programming frameworks
- **1.4.0**: Advanced machine learning-based search strategy optimization

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.