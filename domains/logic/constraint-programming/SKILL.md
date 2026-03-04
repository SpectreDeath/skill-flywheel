---
Domain: logic
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: constraint-programming
---



## Description

Automatically designs and implements optimal constraint programming systems for solving complex combinatorial optimization problems. This skill provides comprehensive frameworks for constraint modeling, domain propagation, search strategies, constraint satisfaction, optimization techniques, and hybrid solving approaches for applications including scheduling, resource allocation, configuration, and planning problems.


## Purpose

*[Content for Purpose section to be added based on the specific skill requirements]*

## Examples

*[Content for Examples section to be added based on the specific skill requirements]*

## Implementation Notes

*[Content for Implementation Notes section to be added based on the specific skill requirements]*
## Capabilities

- **Constraint Modeling**: Design efficient constraint models using various constraint types (arithmetic, logical, global constraints)
- **Domain Propagation**: Implement sophisticated domain reduction and constraint propagation algorithms
- **Search Strategy Design**: Create advanced search strategies including variable/value ordering, restart strategies, and hybrid approaches
- **Global Constraint Implementation**: Design and implement specialized global constraints for specific problem domains
- **Optimization Techniques**: Apply constraint-based optimization methods including branch-and-bound, constraint-based local search
- **Hybrid Solving**: Integrate constraint programming with other solving paradigms (SAT, MIP, CP-SAT)
- **Performance Optimization**: Optimize constraint solving performance through modeling improvements and algorithmic enhancements

## Usage Examples

### Constraint Programming Model

```python
# Scheduling Problem: Job Shop Scheduling
from constraint import Problem, AllDifferentConstraint

def solve_job_shop_scheduling(jobs, machines, processing_times):
    """
    Solve job shop scheduling using constraint programming
    """
    problem = Problem()
    
    # Variables: start times for each operation
    variables = {}
    for job in jobs:
        for operation in jobs[job]:
            var_name = f"start_{job}_{operation}"
            variables[var_name] = (0, max_time_horizon)
            problem.addVariable(var_name, range(max_time_horizon))
    
    # Constraints: Precedence constraints within jobs
    for job in jobs:
        operations = jobs[job]
        for i in range(len(operations) - 1):
            op1 = operations[i]
            op2 = operations[i + 1]
            start1 = f"start_{job}_{op1}"
            start2 = f"start_{job}_{op2}"
            duration1 = processing_times[job][op1]
            
            # op2 must start after op1 finishes
            problem.addConstraint(
                lambda s1, s2, d=duration1: s2 >= s1 + d,
                (start1, start2)
            )
    
    # Constraints: Resource constraints (machine capacity)
    for machine in machines:
        # Get all operations using this machine
        machine_operations = []
        for job in jobs:
            for operation in jobs[job]:
                if machines[machine][operation]:
                    machine_operations.append((job, operation))
        
        # No overlap constraint for operations on same machine
        for i in range(len(machine_operations)):
            for j in range(i + 1, len(machine_operations)):
                job1, op1 = machine_operations[i]
                job2, op2 = machine_operations[j]
                
                start1 = f"start_{job1}_{op1}"
                start2 = f"start_{job2}_{op2}"
                duration1 = processing_times[job1][op1]
                duration2 = processing_times[job2][op2]
                
                # Operations cannot overlap on same machine
                problem.addConstraint(
                    lambda s1, s2, d1=duration1, d2=duration2: 
                        s1 + d1 <= s2 or s2 + d2 <= s1,
                    (start1, start2)
                )
    
    # Objective: Minimize makespan
    makespan_var = "makespan"
    problem.addVariable(makespan_var, range(max_time_horizon))
    
    # Makespan constraint
    for job in jobs:
        last_operation = jobs[job][-1]
        start_var = f"start_{job}_{last_operation}"
        duration = processing_times[job][last_operation]
        
        problem.addConstraint(
            lambda s, m, d=duration: m >= s + d,
            (start_var, makespan_var)
        )
    
    # Solve with optimization
    solutions = problem.getSolutions()
    best_solution = min(solutions, key=lambda sol: sol[makespan_var])
    
    return best_solution

# Example usage
jobs = {
    'job1': ['op1', 'op2', 'op3'],
    'job2': ['op1', 'op2']
}
machines = {
    'machine1': {'op1': True, 'op2': False, 'op3': True},
    'machine2': {'op1': False, 'op2': True, 'op3': False}
}
processing_times = {
    'job1': {'op1': 3, 'op2': 2, 'op3': 4},
    'job2': {'op1': 2, 'op2': 3}
}
solution = solve_job_shop_scheduling(jobs, machines, processing_times)
```

### Global Constraint Implementation

```python
class GlobalConstraints:
    """Implementation of global constraints"""
    
    @staticmethod
    def all_different(variables):
        """AllDifferent constraint: all variables must have different values"""
        def constraint_func(*values):
            return len(set(values)) == len(values)
        return constraint_func
    
    @staticmethod
    def cumulative(starts, durations, resources, capacity):
        """Cumulative constraint for resource scheduling"""
        def constraint_func(*args):
            # Extract values
            starts_vals = args[:len(starts)]
            durations_vals = args[len(starts):len(starts)+len(durations)]
            resources_vals = args[len(starts)+len(durations):]
            
            # Check resource usage at each time point
            max_time = max(s + d for s, d in zip(starts_vals, durations_vals))
            
            for t in range(max_time):
                usage = 0
                for i in range(len(starts_vals)):
                    if starts_vals[i] <= t < starts_vals[i] + durations_vals[i]:
                        usage += resources_vals[i]
                    if usage > capacity:
                        return False
            return True
        return constraint_func
    
    @staticmethod
    def element(index, values, result):
        """Element constraint: result = values[index]"""
        def constraint_func(idx, res):
            if 0 <= idx < len(values):
                return res == values[idx]
            return False
        return constraint_func
    
    @staticmethod
    def circuit(path):
        """Circuit constraint for Hamiltonian path problems"""
        def constraint_func(*values):
            # Check if values form a single circuit
            n = len(values)
            visited = [False] * n
            
            current = 0
            for _ in range(n):
                if visited[current]:
                    return False
                visited[current] = True
                current = values[current]
            
            return current == 0 and all(visited)
        return constraint_func
```

### Advanced Search Strategies

```python
class SearchStrategies:
    """Advanced search strategies for constraint programming"""
    
    @staticmethod
    def first_fail(variables, domains):
        """First-fail principle: choose variable with smallest domain"""
        min_domain_size = float('inf')
        selected_var = None
        
        for var in variables:
            domain_size = len(domains[var])
            if 1 < domain_size < min_domain_size:
                min_domain_size = domain_size
                selected_var = var
        
        return selected_var
    
    @staticmethod
    def most_constrained(variables, domains, constraints):
        """Most constrained variable: choose variable involved in most constraints"""
        constraint_counts = {}
        
        for var in variables:
            count = sum(1 for constraint in constraints 
                       if var in constraint.variables)
            constraint_counts[var] = count
        
        # Choose variable with most constraints and smallest domain
        best_var = None
        best_score = -1
        
        for var in variables:
            if len(domains[var]) > 1:
                score = constraint_counts[var] / len(domains[var])
                if score > best_score:
                    best_score = score
                    best_var = var
        
        return best_var
    
    @staticmethod
    def min_regret(variables, domains):
        """Min-regret: choose variable where wrong choice has highest cost"""
        best_var = None
        max_regret = -1
        
        for var in variables:
            if len(domains[var]) > 1:
                sorted_values = sorted(domains[var])
                regret = sorted_values[1] - sorted_values[0]  # Difference between best two
                
                if regret > max_regret:
                    max_regret = regret
                    best_var = var
        
        return best_var
    
    @staticmethod
    def value_ordering_middle_first(domain):
        """Value ordering: try middle values first"""
        if not domain:
            return []
        
        middle = len(domain) // 2
        ordered = [domain[middle]]
        
        # Alternate left and right from middle
        left = middle - 1
        right = middle + 1
        
        while left >= 0 or right < len(domain):
            if right < len(domain):
                ordered.append(domain[right])
                right += 1
            if left >= 0:
                ordered.append(domain[left])
                left -= 1
        
        return ordered
```

## Input Format

### Constraint Programming Model Specification

```yaml
constraint_model_specification:
  problem_id: string              # Unique problem identifier
  problem_type: string            # Type of constraint problem
  optimization_goal: string       # minimize|maximize|satisfy
  
  variables:
    - variable_name: string
      domain: array               # Possible values
      type: "integer|boolean|real"
      bounds: object              # Lower and upper bounds
    
    - variable_name: string
      domain: array
      type: "integer|boolean|real"
      bounds: object
  
  constraints:
    - constraint_type: "arithmetic|logical|global"
      variables: array
      expression: string
      parameters: object
    
    - constraint_type: "arithmetic|logical|global"
      variables: array
      expression: string
      parameters: object
  
  objective:
    type: "minimize|maximize"
    expression: string
    coefficients: object
  
  search_strategy:
    variable_ordering: string     # "first_fail|most_constrained|min_regret"
    value_ordering: string        # "ascending|descending|middle_first"
    restart_strategy: string      # "none|geometric|luby"
    restart_base: number
    restart_factor: number
```

### Constraint Solver Configuration

```yaml
constraint_solver_config:
  solver_type: "CP-SAT|traditional_CP|hybrid"
  solver_parameters:
    time_limit: number            # Maximum solving time
    memory_limit: string          # Maximum memory usage
    optimality_tolerance: number  # Tolerance for optimization
    solution_limit: number        # Maximum number of solutions
    
  propagation_level: string       # "basic|advanced|full"
  search_parallelism: number      # Number of parallel search threads
  solution_pool_size: number      # Size of solution pool
  
  preprocessing:
    constraint_simplification: boolean
    variable_elimination: boolean
    domain_reduction: boolean
    symmetry_breaking: boolean
  
  postprocessing:
    solution_validation: boolean
    solution_optimization: boolean
    solution_diversity: boolean
```

## Output Format

### Constraint Solution Report

```yaml
constraint_solution_report:
  problem_id: string
  solver_used: string
  solving_time: number
  memory_used: string
  
  solution_status: "OPTIMAL|FEASIBLE|INFEASIBLE|TIMEOUT"
  
  if solution_status in ["OPTIMAL", "FEASIBLE"]:
    solution:
      variables: object           # Variable assignments
      objective_value: number     # Objective function value
      solution_quality: string    # Quality assessment
    
    constraint_satisfaction:
      satisfied_constraints: number
      total_constraints: number
      satisfaction_rate: number
    
    search_statistics:
      nodes_explored: number
      branches_pruned: number
      propagations: number
      restarts: number
  
  if solution_status == "INFEASIBLE":
    infeasibility_analysis:
      conflicting_constraints: array
      minimal_unsatisfiable_core: array
      relaxation_suggestions: array
  
  performance_metrics:
    constraint_propagation_efficiency: number
    search_tree_balance: number
    memory_efficiency: number
    parallel_efficiency: number
```

### Constraint Model Analysis

```yaml
constraint_model_analysis:
  model_complexity:
    variables_count: number
    constraints_count: number
    average_arity: number
    constraint_types_distribution: object
  
  propagation_analysis:
    domain_reduction_effectiveness: number
    constraint_tightness: number
    propagation_frequency: number
    redundant_constraints: array
  
  search_analysis:
    search_space_size: number
    pruning_effectiveness: number
    solution_density: number
    search_strategy_effectiveness: number
  
  optimization_analysis:
    objective_function_properties: object
    constraint_optimality_conditions: array
    solution_quality_distribution: object
    convergence_characteristics: object
```

## Configuration Options

### Constraint Programming Paradigms

```yaml
cp_paradigms:
  traditional_cp:
    description: "Classical constraint programming with backtracking search"
    best_for: ["combinatorial_problems", "scheduling", "configuration"]
    complexity: "exponential_worst_case"
    memory_usage: "medium"
    examples: ["Gecode", "Choco", "ECLiPSe"]
  
  cp_sat:
    description: "Constraint programming with SAT-based solving"
    best_for: ["large_problems", "industrial_applications", "optimization"]
    complexity: "polynomial_average_case"
    memory_usage: "high"
    examples: ["Google_OR-Tools", "CPLEX_CP_Optimizer"]
  
  hybrid_cp:
    description: "Hybrid approaches combining CP with other paradigms"
    best_for: ["complex_problems", "multi-objective_optimization"]
    complexity: "variable"
    memory_usage: "high"
    examples: ["CP-MIP", "CP-SAT", "CP-Local_Search"]
```

### Global Constraints

```yaml
global_constraints:
  all_different:
    description: "All variables must have different values"
    complexity: "O(n log n)"
    applications: ["scheduling", "assignment", "puzzles"]
  
  cumulative:
    description: "Resource constraint for scheduling problems"
    complexity: "O(n^2)"
    applications: ["resource_allocation", "project_scheduling"]
  
  element:
    description: "Array indexing constraint"
    complexity: "O(1)"
    applications: ["routing", "assignment", "configuration"]
  
  circuit:
    description: "Hamiltonian path constraint"
    complexity: "O(n^2)"
    applications: ["routing", "sequencing", "tour_planning"]
  
  regular:
    description: "Finite automaton constraint"
    complexity: "O(n * states)"
    applications: ["pattern_constraints", "sequence_constraints"]
```

## Error Handling

### Constraint Solving Failures

```yaml
solving_failures:
  infeasible_problem:
    retry_strategy: "relaxation_analysis"
    max_retries: 1
    fallback_action: "partial_satisfaction"
  
  timeout_exceeded:
    retry_strategy: "parameter_adjustment"
    max_retries: 3
    fallback_action: "heuristic_solution"
  
  memory_exhaustion:
    retry_strategy: "problem_decomposition"
    max_retries: 2
    fallback_action: "incremental_solving"
  
  numerical_instability:
    retry_strategy: "precision_adjustment"
    max_retries: 2
    fallback_action: "alternative_modeling"
```

### Modeling Errors

```yaml
modeling_errors:
  inconsistent_constraints:
    detection_strategy: "constraint_analysis"
    recovery_strategy: "conflict_resolution"
    escalation: "model_reconstruction"
  
  unbounded_variables:
    detection_strategy: "domain_analysis"
    recovery_strategy: "bound_estimation"
    escalation: "constraint_addition"
  
  poor_propagation:
    detection_strategy: "propagation_monitoring"
    recovery_strategy: "constraint_reformulation"
    escalation: "global_constraint_usage"
```

## Performance Optimization

### Constraint Propagation Optimization

```python
class PropagationOptimizer:
    """Optimization for constraint propagation"""
    
    def __init__(self, constraint_network):
        self.constraint_network = constraint_network
        self.propagation_queue = []
        self.domain_changes = {}
        
    def implement_arc_consistency(self):
        """Implement AC-3 or AC-2001 algorithm"""
        # Initialize queue with all constraints
        for constraint in self.constraint_network.constraints:
            for var in constraint.variables:
                self.propagation_queue.append((constraint, var))
        
        # Process queue until empty
        while self.propagation_queue:
            constraint, variable = self.propagation_queue.pop(0)
            
            if self.revise_domain(constraint, variable):
                # Add affected constraints to queue
                for neighbor_constraint in self.get_affected_constraints(variable):
                    for neighbor_var in neighbor_constraint.variables:
                        if neighbor_var != variable:
                            self.propagation_queue.append((neighbor_constraint, neighbor_var))
    
    def implement_bound_consistency(self):
        """Optimize for integer domains using bound consistency"""
        for constraint in self.constraint_network.constraints:
            if constraint.type == "arithmetic":
                self.optimize_bounds_propagation(constraint)
    
    def implement_path_consistency(self):
        """Implement path consistency for binary constraints"""
        variables = list(self.constraint_network.variables.keys())
        
        for k in variables:
            for i in variables:
                for j in variables:
                    if i != j and i != k and j != k:
                        self.enforce_path_consistency(i, j, k)
```

### Search Optimization

```python
class SearchOptimizer:
    """Optimization for constraint search"""
    
    def __init__(self, solver):
        self.solver = solver
        self.restart_strategy = None
        self.diversification_strategy = None
        
    def implement_restart_strategies(self):
        """Implement various restart strategies"""
        if self.restart_strategy == "geometric":
            return self.geometric_restart()
        elif self.restart_strategy == "luby":
            return self.luby_restart()
        elif self.restart_strategy == "linear":
            return self.linear_restart()
    
    def implement_diversification(self):
        """Implement search diversification strategies"""
        # Randomization
        self.randomize_variable_ordering()
        self.randomize_value_ordering()
        
        # Different search strategies
        self.implement_simulated_annealing()
        self.implement_tabu_search()
        self.implement_genetic_algorithms()
    
    def implement_parallel_search(self):
        """Implement parallel constraint search"""
        # Portfolio approach: run multiple strategies in parallel
        strategies = [
            "first_fail_descending",
            "most_constrained_ascending", 
            "min_regret_middle_first"
        ]
        
        # Run strategies in parallel
        results = self.run_parallel_strategies(strategies)
        
        # Combine results
        return self.combine_parallel_results(results)
```

## Integration Examples

### With Scheduling Systems

```python
# Integration with scheduling systems
class CPScheduling:
    """Constraint programming for scheduling"""
    
    def __init__(self, resources, tasks):
        self.resources = resources
        self.tasks = tasks
        
    def model_scheduling_problem(self):
        """Model scheduling as constraint problem"""
        # Variables: start times, resource assignments
        variables = self.create_scheduling_variables()
        
        # Constraints: resource capacity, precedence, time windows
        constraints = self.create_scheduling_constraints()
        
        # Objective: minimize makespan or maximize resource utilization
        objective = self.create_scheduling_objective()
        
        return variables, constraints, objective
    
    def solve_scheduling_problem(self):
        """Solve scheduling problem using CP"""
        variables, constraints, objective = self.model_scheduling_problem()
        
        # Create and solve CP model
        solver = CPSolver()
        solver.add_variables(variables)
        solver.add_constraints(constraints)
        solver.set_objective(objective)
        
        return solver.solve()
```

### With Optimization Systems

```python
# Integration with optimization systems
class CPOptimization:
    """Constraint programming for optimization"""
    
    def __init__(self, optimization_problem):
        self.problem = optimization_problem
        
    def hybrid_cp_optimization(self):
        """Hybrid CP and mathematical optimization"""
        # Use CP for feasibility
        cp_model = self.create_cp_model()
        feasible_solution = cp_model.solve()
        
        # Use mathematical optimization for quality
        if feasible_solution:
            mip_model = self.create_mip_model(feasible_solution)
            optimized_solution = mip_model.solve()
            
            return optimized_solution
        
        return None
    
    def constraint_based_local_search(self):
        """Constraint-based local search"""
        # Start with initial solution
        current_solution = self.generate_initial_solution()
        
        # Iteratively improve solution
        while self.can_improve(current_solution):
            neighbors = self.generate_neighbors(current_solution)
            best_neighbor = self.select_best_neighbor(neighbors)
            
            if self.is_better(best_neighbor, current_solution):
                current_solution = best_neighbor
        
        return current_solution
```

## Best Practices

1. **Modeling**:
   - Use appropriate variable types and domains
   - Apply symmetry breaking constraints
   - Use global constraints when available
   - Implement redundant constraints for better propagation

2. **Search Strategy**:
   - Choose appropriate variable and value ordering
   - Implement restart strategies for difficult problems
   - Use parallel search for large problems
   - Apply diversification strategies to escape local optima

3. **Performance Optimization**:
   - Monitor constraint propagation effectiveness
   - Use appropriate propagation levels
   - Implement efficient data structures
   - Profile and optimize hotspots

4. **Solution Quality**:
   - Validate solutions independently
   - Implement solution quality metrics
   - Use multiple solving strategies
   - Document solution assumptions and limitations

## Troubleshooting

### Common Issues

1. **Poor Performance**: Analyze constraint propagation and search strategy
2. **Infeasible Solutions**: Check constraint consistency and domain bounds
3. **Suboptimal Solutions**: Improve search strategy and add redundant constraints
4. **Memory Issues**: Implement problem decomposition and incremental solving
5. **Modeling Errors**: Validate constraint definitions and variable domains

### Debug Mode

```python
class CPDebugger:
    """Debugging utilities for constraint programming"""
    
    def __init__(self, solver):
        self.solver = solver
        self.debug_mode = True
        
    def enable_constraint_tracing(self):
        """Enable detailed constraint propagation tracing"""
        self.solver.enable_propagation_logging()
        self.solver.enable_domain_logging()
        self.solver.enable_search_logging()
        
    def analyze_constraint_network(self):
        """Analyze constraint network structure"""
        # Check constraint graph connectivity
        connectivity = self.check_connectivity()
        
        # Analyze constraint tightness
        tightness = self.analyze_tightness()
        
        # Identify bottlenecks
        bottlenecks = self.identify_bottlenecks()
        
        return {
            'connectivity': connectivity,
            'tightness': tightness,
            'bottlenecks': bottlenecks
        }
    
    def profile_search_performance(self):
        """Profile search performance"""
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
  modeling_metrics:
    variables_count: number
    constraints_count: number
    average_arity: number
    constraint_tightness: number
    
  propagation_metrics:
    domain_reduction_rate: number
    propagation_efficiency: number
    constraint_checking_frequency: number
    redundant_constraint_detection: number
    
  search_metrics:
    nodes_explored: number
    solution_quality: number
    search_tree_balance: number
    pruning_effectiveness: number
    
  resource_metrics:
    memory_usage_peak: string
    cpu_utilization: number
    solving_time: number
    parallel_efficiency: number
```

## Dependencies

- **Constraint Solvers**: Gecode, Choco, OR-Tools, or other CP solvers
- **Mathematical Libraries**: Libraries for arithmetic and logical constraints
- **Optimization Libraries**: Integration with MIP and other optimization solvers
- **Parallel Computing**: Frameworks for parallel constraint solving
- **Visualization Tools**: Tools for constraint network visualization and analysis

## Version History

- **1.0.0**: Initial release with comprehensive constraint programming frameworks
- **1.1.0**: Added advanced global constraints and propagation techniques
- **1.2.0**: Enhanced search strategies and hybrid solving approaches
- **1.3.0**: Improved performance optimization and parallel solving
- **1.4.0**: Advanced integration patterns with scheduling and optimization systems

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

Content for ## Constraints involving Constraint Programming.