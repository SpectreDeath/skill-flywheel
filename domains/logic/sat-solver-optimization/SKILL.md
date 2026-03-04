---
Domain: logic
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: sat-solver-optimization
---



## Description

Automatically designs and implements optimal SAT (Boolean Satisfiability) solver configurations and optimization strategies for solving complex logical constraint problems. This skill provides comprehensive frameworks for problem encoding, solver selection, heuristic optimization, clause learning, conflict analysis, and performance tuning for various SAT problem domains including formal verification, planning, scheduling, and constraint satisfaction.

## Purpose

To provide a structured framework for solving NP-complete problems via Boolean Satisfiability, ensuring efficient encoding and solver configuration for industrial-grade constraint solving.

## Examples

### Example 1: Logical Equivalency Checking

**Goal**: Verify if two circuits are functionally identical.
**Workflow**: Encode the XOR of the two outputs and check for UNSAT.

## Implementation Notes

- **DIMACS Standard**: Always prefer DIMACS CNF format for solver inputs to ensure cross-platform compatibility.
- **Variable Ordering**: Prioritize variables that appear most frequently in short clauses to trigger unit propagation earlier.

## Capabilities

- **Problem Encoding Optimization**: Design efficient CNF (Conjunctive Normal Form) encodings for various problem types with minimal clause explosion
- **Solver Selection and Configuration**: Automatically select and configure optimal SAT solvers based on problem characteristics and constraints
- **Heuristic Optimization**: Implement advanced variable and value selection heuristics including VSIDS, MOMS, and activity-based strategies
- **Clause Learning and Management**: Optimize clause learning strategies, redundancy elimination, and clause database management
- **Conflict Analysis and Resolution**: Implement sophisticated conflict analysis, backjumping, and learning techniques
- **Parallel and Incremental Solving**: Design parallel SAT solving strategies and incremental solving for dynamic problem modifications
- **Performance Profiling and Tuning**: Analyze solver performance and automatically tune parameters for optimal performance

## Usage Examples

### SAT Problem Encoding

```python
# CNF Encoding for Graph Coloring Problem
def encode_graph_coloring(graph, num_colors):
    """
    Encode graph coloring problem as SAT instance
    """
    clauses = []
    variables = {}
    var_counter = 1
    
    # Create variables: color(node, color)
    for node in graph.nodes:
        for color in range(num_colors):
            variables[(node, color)] = var_counter
            var_counter += 1
    
    # Constraint 1: Each node must have at least one color
    for node in graph.nodes:
        clause = [variables[(node, color)] for color in range(num_colors)]
        clauses.append(clause)
    
    # Constraint 2: Each node can have at most one color (pairwise exclusion)
    for node in graph.nodes:
        for i in range(num_colors):
            for j in range(i + 1, num_colors):
                clause = [-variables[(node, i)], -variables[(node, j)]]
                clauses.append(clause)
    
    # Constraint 3: Adjacent nodes must have different colors
    for edge in graph.edges:
        node1, node2 = edge
        for color in range(num_colors):
            clause = [-variables[(node1, color)], -variables[(node2, color)]]
            clauses.append(clause)
    
    return clauses, variables

# Example usage
graph = {
    'nodes': ['A', 'B', 'C', 'D'],
    'edges': [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), ('A', 'C')]
}
clauses, variables = encode_graph_coloring(graph, 3)
```

### SAT Solver Configuration

```yaml
sat_solver_configuration:
  problem_type: "graph_coloring"
  problem_size: "medium"
  constraints: "complex"
  
  solver_selection:
    primary_solver: "MiniSat"
    backup_solvers: ["Glucose", "Lingeling"]
    selection_criteria:
      - criterion: "problem_structure"
        weight: 0.4
        threshold: 0.8
      - criterion: "constraint_density"
        weight: 0.3
        threshold: 0.6
      - criterion: "variable_count"
        weight: 0.3
        threshold: 1000
  
  optimization_parameters:
    branching_heuristic: "VSIDS"
    clause_learning: "enabled"
    conflict_analysis: "enabled"
    restart_strategy: "geometric"
    restart_base: 100
    restart_factor: 1.5
    
    preprocessing:
      variable_elimination: "aggressive"
      subsumption_elimination: "enabled"
      pure_literal_elimination: "enabled"
      unit_propagation: "enabled"
    
    clause_management:
      clause_deletion: "activity_based"
      clause_database_limit: 1000000
      learned_clause_minimization: "enabled"
      phase_saving: "enabled"
  
  performance_tuning:
    memory_limit: "2GB"
    time_limit: "300s"
    parallel_solving: "enabled"
    thread_count: 4
    incremental_solving: "enabled"
```

### Advanced Heuristics Implementation

```python
class SATHeuristics:
    """Advanced heuristics for SAT solving"""
    
    def __init__(self, clauses):
        self.clauses = clauses
        self.variable_activity = {}
        self.decay_factor = 0.95
        self.vsids_scores = {}
        
    def initialize_vsids_scores(self):
        """Initialize VSIDS (Variable State Independent Decaying Sum) scores"""
        for clause in self.clauses:
            for literal in clause:
                var = abs(literal)
                if var not in self.vsids_scores:
                    self.vsids_scores[var] = 1.0
                else:
                    self.vsids_scores[var] += 1.0
    
    def update_vsids_scores(self, conflict_clause):
        """Update VSIDS scores based on conflict analysis"""
        for literal in conflict_clause:
            var = abs(literal)
            self.vsids_scores[var] += 1.0
        
        # Apply decay
        for var in self.vsids_scores:
            self.vsids_scores[var] *= self.decay_factor
    
    def select_branching_variable(self):
        """Select variable for branching using VSIDS heuristic"""
        unassigned_vars = [var for var in self.vsids_scores.keys() 
                          if var not in self.assignment]
        
        if not unassigned_vars:
            return None
            
        # Select variable with highest VSIDS score
        best_var = max(unassigned_vars, 
                      key=lambda var: self.vsids_scores[var])
        return best_var
    
    def mom_heuristic(self, clauses):
        """MOMS (Maximum Occurrences in clauses of Minimum Size) heuristic"""
        min_clause_size = min(len(clause) for clause in clauses if clause)
        
        # Find clauses of minimum size
        min_clauses = [clause for clause in clauses 
                      if len(clause) == min_clause_size]
        
        # Count literal occurrences
        literal_counts = {}
        for clause in min_clauses:
            for literal in clause:
                literal_counts[literal] = literal_counts.get(literal, 0) + 1
        
        # Select literal with maximum count
        if literal_counts:
            best_literal = max(literal_counts.keys(), 
                             key=lambda lit: literal_counts[lit])
            return abs(best_literal), best_literal > 0
        
        return None, None
```

## Input Format

### SAT Problem Specification

```yaml
sat_problem_specification:
  problem_id: string              # Unique problem identifier
  problem_type: string            # Type of problem (scheduling, planning, etc.)
  encoding_format: "CNF|DIMACS"   # Input format
  
  problem_structure:
    variables_count: number       # Number of Boolean variables
    clauses_count: number         # Number of clauses
    constraint_density: number    # Clauses per variable ratio
    clause_length_distribution: object  # Distribution of clause lengths
    
  constraints:
    hard_constraints: array       # Must-satisfy constraints
    soft_constraints: array       # Preferable but not required
    cardinality_constraints: array # At-most/at-least constraints
    
  optimization_objectives:
    primary_objective: string     # Primary optimization goal
    secondary_objectives: array   # Secondary optimization goals
    objective_weights: object     # Weights for multi-objective optimization
    
  performance_requirements:
    time_limit: number            # Maximum solving time in seconds
    memory_limit: string          # Maximum memory usage
    solution_quality: string      # Required solution quality
    parallel_execution: boolean   # Whether parallel solving is allowed
```

### Solver Configuration Request

```yaml
solver_configuration_request:
  problem_characteristics:
    variables: number
    clauses: number
    average_clause_length: number
    constraint_types: array
    problem_domain: string
    
  performance_goals:
    solving_time: string
    memory_efficiency: string
    solution_optimality: string
    robustness: string
    
  resource_constraints:
    cpu_cores: number
    memory_gb: number
    storage_gb: number
    network_bandwidth: string
    
  solver_preferences:
    solver_type: "complete|incomplete|stochastic"
    heuristics: array
    optimization_techniques: array
    parallel_strategies: array
```

## Output Format

### Optimized SAT Solver Configuration

```yaml
optimized_solver_configuration:
  solver_id: string
  configuration_timestamp: timestamp
  problem_characteristics: object
  
  selected_solver: string
  configuration_parameters:
    branching_strategy: string
    conflict_analysis: boolean
    clause_learning: boolean
    restart_policy: string
    preprocessing_level: string
    optimization_level: string
    
  performance_optimizations:
    memory_management: object
    cache_optimization: object
    parallel_execution: object
    incremental_solving: object
    
  expected_performance:
    estimated_solving_time: string
    memory_usage_estimate: string
    success_probability: number
    scalability_characteristics: object
    
  tuning_recommendations:
    parameter_adjustments: array
    heuristic_improvements: array
    constraint_handling: array
    performance_monitoring: array
```

### SAT Solution Report

```yaml
sat_solution_report:
  problem_id: string
  solver_used: string
  solving_time: number
  memory_used: string
  
  solution_status: "SATISFIABLE|UNSATISFIABLE|TIMEOUT"
  
  if solution_status == "SATISFIABLE":
    satisfying_assignment: object
    objective_value: number
    constraint_satisfaction: object
    
  if solution_status == "UNSATISFIABLE":
    unsatisfiability_proof: object
    minimal_unsatisfiable_core: array
    conflict_analysis: object
    
  performance_metrics:
    conflicts: number
    decisions: number
    propagations: number
    learned_clauses: number
    restarts: number
    
  optimization_results:
    best_solution_found: object
    solution_improvements: array
    convergence_analysis: object
```

## Configuration Options

### SAT Solver Types

```yaml
solver_types:
  complete_solvers:
    description: "Guaranteed to find solution or prove unsatisfiability"
    best_for: ["formal_verification", "mathematical_proofs", "critical_systems"]
    examples: ["MiniSat", "Glucose", "Lingeling"]
    complexity: "exponential_worst_case"
  
  incomplete_solvers:
    description: "Heuristic-based solvers for finding solutions quickly"
    best_for: ["large_problems", "practical_applications", "time_constrained"]
    examples: ["WalkSAT", "GSAT", "ProbSAT"]
    complexity: "polynomial_average_case"
  
  stochastic_solvers:
    description: "Randomized algorithms with probabilistic guarantees"
    best_for: ["combinatorial_optimization", "approximation_algorithms"]
    examples: ["Simulated_Annealing", "Genetic_Algorithms"]
    complexity: "probabilistic_polynomial"
```

### Heuristic Strategies

```yaml
heuristic_strategies:
  vsids:
    description: "Variable State Independent Decaying Sum"
    best_for: ["structured_problems", "industrial_applications"]
    complexity: "O(log n)"
    memory_usage: "medium"
  
  mom:
    description: "Maximum Occurrences in clauses of Minimum Size"
    best_for: ["random_sat_problems", "theoretical_analysis"]
    complexity: "O(n)"
    memory_usage: "low"
  
  jw:
    description: "Jeroslow-Wang heuristic"
    best_for: ["weighted_sat_problems", "optimization_tasks"]
    complexity: "O(n log n)"
    memory_usage: "medium"
  
  activity_based:
    description: "Activity-based variable selection"
    best_for: ["dynamic_problems", "incremental_solving"]
    complexity: "O(log n)"
    memory_usage: "high"
```

## Error Handling

### SAT Solving Failures

```yaml
solving_failures:
  timeout_exceeded:
    retry_strategy: "parameter_adjustment"
    max_retries: 3
    fallback_action: "incomplete_solver"
  
  memory_exhaustion:
    retry_strategy: "memory_optimization"
    max_retries: 2
    fallback_action: "problem_decomposition"
  
  unsatisfiable_core:
    retry_strategy: "constraint_relaxation"
    max_retries: 1
    fallback_action: "partial_satisfiability"
  
  numerical_instability:
    retry_strategy: "precision_adjustment"
    max_retries: 2
    fallback_action: "alternative_encoding"
```

### Configuration Errors

```yaml
configuration_errors:
  invalid_parameters:
    detection_strategy: "parameter_validation"
    recovery_strategy: "default_configuration"
    escalation: "manual_configuration"
  
  incompatible_heuristics:
    detection_strategy: "compatibility_checking"
    recovery_strategy: "heuristic_replacement"
    escalation: "simplified_configuration"
  
  resource_constraints_violation:
    detection_strategy: "resource_monitoring"
    recovery_strategy: "resource_optimization"
    escalation: "problem_simplification"
```

## Performance Optimization

### Memory Optimization

```python
class MemoryOptimizer:
    """Memory optimization for SAT solvers"""
    
    def __init__(self, solver):
        self.solver = solver
        self.memory_usage = 0
        self.clause_database = []
        
    def optimize_clause_storage(self):
        """Optimize clause database storage"""
        # Implement clause compression
        compressed_clauses = []
        for clause in self.clause_database:
            compressed = self.compress_clause(clause)
            compressed_clauses.append(compressed)
        
        self.clause_database = compressed_clauses
    
    def implement_garbage_collection(self):
        """Implement garbage collection for learned clauses"""
        # Remove redundant clauses
        non_redundant_clauses = []
        for clause in self.clause_database:
            if not self.is_redundant(clause):
                non_redundant_clauses.append(clause)
        
        self.clause_database = non_redundant_clauses
    
    def optimize_variable_tracking(self):
        """Optimize variable activity and assignment tracking"""
        # Use bit vectors for assignment tracking
        self.assignment_vector = [None] * self.solver.num_variables
        
        # Use heap for activity tracking
        import heapq
        self.activity_heap = []
        for var in range(self.solver.num_variables):
            heapq.heappush(self.activity_heap, (0, var))
```

### Parallel Solving Optimization

```python
class ParallelSolverOptimizer:
    """Optimization for parallel SAT solving"""
    
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.solvers = []
        self.load_balancer = LoadBalancer()
        
    def implement_work_stealing(self):
        """Implement work stealing for load balancing"""
        # Each solver maintains a queue of work units
        for solver in self.solvers:
            solver.work_queue = deque()
        
        # Implement stealing mechanism
        def steal_work(victim_solver):
            if victim_solver.work_queue:
                return victim_solver.work_queue.popleft()
            return None
    
    def optimize_communication(self):
        """Optimize communication between parallel solvers"""
        # Use shared clause database
        self.shared_clause_db = SharedClauseDatabase()
        
        # Implement efficient clause exchange
        def exchange_clauses(solver_id, clauses):
            self.shared_clause_db.add_clauses(solver_id, clauses)
            
        # Implement clause filtering
        def filter_clauses(clauses):
            return [clause for clause in clauses 
                   if self.is_useful_clause(clause)]
```

## Integration Examples

### With Formal Verification

```python
# Integration with formal verification tools
class FormalVerificationSAT:
    """SAT-based formal verification"""
    
    def __init__(self, model_checker):
        self.model_checker = model_checker
        
    def encode_verification_problem(self, specification, model):
        """Encode formal verification as SAT problem"""
        # Convert temporal logic to SAT
        clauses = self.convert_ltl_to_sat(specification)
        
        # Add model constraints
        model_clauses = self.encode_model(model)
        clauses.extend(model_clauses)
        
        return clauses
    
    def verify_property(self, property_spec):
        """Verify property using SAT solving"""
        clauses = self.encode_verification_problem(property_spec)
        
        # Solve SAT problem
        solver = SATSolver()
        result = solver.solve(clauses)
        
        if result == "UNSATISFIABLE":
            return "PROPERTY_VERIFIED"
        else:
            return "COUNTEREXAMPLE_FOUND", result
```

### With Planning Systems

```python
# Integration with automated planning
class SATPlanning:
    """SAT-based automated planning"""
    
    def __init__(self, domain, problem):
        self.domain = domain
        self.problem = problem
        
    def encode_planning_problem(self):
        """Encode planning problem as SAT"""
        clauses = []
        
        # Encode initial state
        initial_clauses = self.encode_initial_state()
        clauses.extend(initial_clauses)
        
        # Encode goal state
        goal_clauses = self.encode_goal_state()
        clauses.extend(goal_clauses)
        
        # Encode actions and transitions
        action_clauses = self.encode_actions()
        clauses.extend(action_clauses)
        
        return clauses
    
    def find_plan(self, horizon):
        """Find plan using SAT solving"""
        for t in range(horizon):
            clauses = self.encode_planning_problem()
            clauses.extend(self.encode_time_steps(t))
            
            solver = SATSolver()
            result = solver.solve(clauses)
            
            if result == "SATISFIABLE":
                return self.extract_plan(result)
        
        return "NO_PLAN_FOUND"
```

## Best Practices

1. **Problem Encoding**:
   - Use efficient encodings to minimize clause explosion
   - Apply domain-specific optimizations
   - Use symmetry breaking constraints when applicable
   - Implement incremental encoding for dynamic problems

2. **Solver Configuration**:
   - Analyze problem characteristics before selecting solver
   - Tune parameters based on problem structure
   - Use appropriate heuristics for different problem types
   - Implement fallback strategies for robustness

3. **Performance Optimization**:
   - Monitor memory usage and implement garbage collection
   - Use parallel solving for large problems
   - Implement incremental solving for dynamic modifications
   - Profile solver performance and identify bottlenecks

4. **Solution Quality**:
   - Verify solution correctness through independent checking
   - Implement solution validation mechanisms
   - Use multiple solvers for critical applications
   - Document solution assumptions and limitations

## Troubleshooting

### Common Issues

1. **Performance Problems**: Analyze problem encoding and solver configuration
2. **Memory Issues**: Implement memory optimization and garbage collection
3. **Solution Quality**: Verify encoding correctness and solver settings
4. **Scalability Issues**: Use problem decomposition and parallel solving
5. **Configuration Failures**: Implement parameter validation and fallback strategies

### Debug Mode

```python
class SATDebugger:
    """Debugging utilities for SAT solvers"""
    
    def __init__(self, solver):
        self.solver = solver
        self.debug_mode = True
        
    def enable_detailed_logging(self):
        """Enable detailed logging for debugging"""
        self.solver.log_level = "DEBUG"
        self.solver.enable_conflict_logging()
        self.solver.enable_clause_logging()
        
    def analyze_conflicts(self):
        """Analyze conflicts for debugging"""
        conflicts = self.solver.get_conflicts()
        for conflict in conflicts:
            print(f"Conflict: {conflict}")
            self.analyze_conflict_reason(conflict)
    
    def profile_performance(self):
        """Profile solver performance"""
        import cProfile
        profiler = cProfile.Profile()
        profiler.enable()
        
        # Run solver
        self.solver.solve()
        
        profiler.disable()
        profiler.print_stats(sort='cumulative')
```

## Monitoring and Metrics

### Performance Metrics

```yaml
performance_metrics:
  solving_metrics:
    solving_time: number
    memory_usage: string
    cpu_utilization: number
    disk_io: string
    
  algorithmic_metrics:
    conflicts: number
    decisions: number
    propagations: number
    learned_clauses: number
    restarts: number
    
  quality_metrics:
    solution_optimality: number
    constraint_satisfaction_rate: number
    verification_success_rate: number
    scalability_score: number
    
  resource_metrics:
    peak_memory: string
    average_cpu: number
    io_operations: number
    network_usage: string
```

## Dependencies

- **SAT Solvers**: MiniSat, Glucose, Lingeling, or other compatible SAT solvers
- **Constraint Libraries**: Libraries for constraint handling and optimization
- **Parallel Computing**: MPI, OpenMP, or other parallel computing frameworks
- **Performance Tools**: Profiling and monitoring tools for performance analysis
- **Integration Frameworks**: APIs for connecting with verification and planning systems

## Version History

- **1.0.0**: Initial release with comprehensive SAT solver optimization frameworks
- **1.1.0**: Added advanced heuristics and parallel solving strategies
- **1.2.0**: Enhanced conflict analysis and clause learning optimization
- **1.3.0**: Improved performance profiling and automatic tuning
- **1.4.0**: Advanced integration patterns with formal verification and planning

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.

## Constraints

- MUST verify the correctness of the CNF encoding before starting long-running solves.
- ALWAYS set a time-limit for solver execution to prevent hung processes in the context window.
- STOP if the number of variables exceeds a predefined complexity threshold for the current agent tier.
