---
Domain: search_algorithms
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: ant-colony-optimization
---



## Description

Automatically designs and implements optimal ant colony optimization algorithms for solving complex optimization problems, including combinatorial optimization, routing problems, scheduling, and discrete optimization. This skill provides comprehensive frameworks for pheromone management, colony behavior simulation, heuristic information, and convergence analysis.


## Purpose

*[Content for Purpose section to be added based on the specific skill requirements]*

## Examples

*[Content for Examples section to be added based on the specific skill requirements]*

## Implementation Notes

*[Content for Implementation Notes section to be added based on the specific skill requirements]*
## Capabilities

- **Pheromone Management**: Implement pheromone trail initialization, updating, evaporation, and reinforcement strategies
- **Colony Simulation**: Design ant colony behavior with exploration/exploitation balance, population dynamics, and communication
- **Heuristic Information**: Create problem-specific heuristic functions and combine with pheromone information
- **Path Construction**: Implement probabilistic path construction with state transition rules and local search integration
- **Convergence Analysis**: Monitor convergence, detect stagnation, and implement restart strategies
- **Multi-objective Optimization**: Extend ACO for multi-objective problems with Pareto optimization
- **Parallel Implementation**: Design parallel ACO algorithms for improved performance and solution quality

## Usage Examples

### Basic Ant Colony Optimization Framework

```python
"""
Basic Ant Colony Optimization Framework
"""

import random
import math
from typing import List, Tuple, Dict, Callable, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Solution:
    """Solution representation"""
    path: List[int]
    cost: float = 0.0
    
    def __hash__(self):
        return hash(tuple(self.path))
    
    def __eq__(self, other):
        return self.path == other.path

@dataclass
class PheromoneMatrix:
    """Pheromone matrix for ACO"""
    matrix: List[List[float]]
    evaporation_rate: float = 0.1
    min_pheromone: float = 0.1
    max_pheromone: float = 10.0
    
    def evaporate(self):
        """Apply pheromone evaporation"""
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] *= (1 - self.evaporation_rate)
                # Ensure bounds
                self.matrix[i][j] = max(self.min_pheromone, min(self.max_pheromone, self.matrix[i][j]))
    
    def deposit(self, i: int, j: int, amount: float):
        """Deposit pheromone on edge (i,j)"""
        self.matrix[i][j] += amount
        # Ensure bounds
        self.matrix[i][j] = max(self.min_pheromone, min(self.max_pheromone, self.matrix[i][j]))

class CostFunction(ABC):
    """Abstract base class for cost functions"""
    
    @abstractmethod
    def evaluate(self, solution: Solution) -> float:
        """Evaluate cost of a solution"""
        pass
    
    @abstractmethod
    def is_minimization(self) -> bool:
        """Return True if this is a minimization problem"""
        pass

class TravelingSalesmanCost(CostFunction):
    """Traveling Salesman Problem cost function"""
    
    def __init__(self, distance_matrix: List[List[float]]):
        self.distance_matrix = distance_matrix
    
    def evaluate(self, solution: Solution) -> float:
        """Calculate total tour distance"""
        total_distance = 0.0
        path = solution.path
        
        for i in range(len(path)):
            from_city = path[i]
            to_city = path[(i + 1) % len(path)]
            total_distance += self.distance_matrix[from_city][to_city]
        
        return total_distance
    
    def is_minimization(self) -> bool:
        return True  # Minimize distance

class AntColonyOptimization:
    """Basic Ant Colony Optimization implementation"""
    
    def __init__(self, 
                 num_ants: int,
                 distance_matrix: List[List[float]],
                 cost_function: CostFunction,
                 alpha: float = 1.0,           # Pheromone importance
                 beta: float = 2.0,            # Heuristic importance
                 evaporation_rate: float = 0.1,
                 q: float = 100.0,             # Pheromone deposit constant
                 max_iterations: int = 100):
        """
        Initialize Ant Colony Optimization
        
        Args:
            num_ants: Number of ants in colony
            distance_matrix: Distance matrix for TSP
            cost_function: Cost function to optimize
            alpha: Pheromone importance factor
            beta: Heuristic importance factor
            evaporation_rate: Rate of pheromone evaporation
            q: Pheromone deposit constant
            max_iterations: Maximum number of iterations
        """
        self.num_ants = num_ants
        self.distance_matrix = distance_matrix
        self.cost_function = cost_function
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.q = q
        self.max_iterations = max_iterations
        self.num_cities = len(distance_matrix)
        
        # Initialize pheromone matrix
        initial_pheromone = 1.0 / (self.num_cities * self.average_distance())
        self.pheromone_matrix = PheromoneMatrix(
            matrix=[[initial_pheromone for _ in range(self.num_cities)] for _ in range(self.num_cities)],
            evaporation_rate=evaporation_rate
        )
        
        # Heuristic information (visibility)
        self.heuristic_matrix = self.calculate_heuristic_matrix()
        
        # Current state
        self.best_solution = None
        self.best_cost = float('inf')
        
        # Statistics
        self.cost_history: List[float] = []
        self.pheromone_history: List[float] = []
    
    def average_distance(self) -> float:
        """Calculate average distance between cities"""
        total_distance = 0.0
        count = 0
        for i in range(self.num_cities):
            for j in range(i + 1, self.num_cities):
                total_distance += self.distance_matrix[i][j]
                count += 1
        return total_distance / count if count > 0 else 1.0
    
    def calculate_heuristic_matrix(self) -> List[List[float]]:
        """Calculate heuristic information (inverse of distances)"""
        heuristic = []
        for i in range(self.num_cities):
            row = []
            for j in range(self.num_cities):
                if i == j:
                    row.append(0.0)
                else:
                    row.append(1.0 / max(self.distance_matrix[i][j], 1e-10))
            heuristic.append(row)
        return heuristic
    
    def select_next_city(self, current_city: int, visited: set) -> int:
        """Select next city using probability rule"""
        unvisited = [city for city in range(self.num_cities) if city not in visited]
        
        if not unvisited:
            return list(visited)[0]  # Return to start
        
        # Calculate probabilities
        probabilities = []
        total_prob = 0.0
        
        for city in unvisited:
            pheromone = self.pheromone_matrix.matrix[current_city][city] ** self.alpha
            heuristic = self.heuristic_matrix[current_city][city] ** self.beta
            probability = pheromone * heuristic
            probabilities.append(probability)
            total_prob += probability
        
        # Select city based on probabilities
        if total_prob == 0:
            return random.choice(unvisited)
        
        # Normalize probabilities
        probabilities = [p / total_prob for p in probabilities]
        
        # Select based on cumulative probabilities
        rand = random.random()
        cumulative_prob = 0.0
        
        for i, prob in enumerate(probabilities):
            cumulative_prob += prob
            if rand <= cumulative_prob:
                return unvisited[i]
        
        return unvisited[-1]
    
    def construct_solution(self) -> Solution:
        """Construct solution for one ant"""
        # Start from random city
        start_city = random.randint(0, self.num_cities - 1)
        current_city = start_city
        path = [start_city]
        visited = {start_city}
        
        # Build path
        while len(path) < self.num_cities:
            next_city = self.select_next_city(current_city, visited)
            path.append(next_city)
            visited.add(next_city)
            current_city = next_city
        
        # Return to start
        path.append(start_city)
        
        solution = Solution(path=path)
        solution.cost = self.cost_function.evaluate(solution)
        
        return solution
    
    def update_pheromones(self, solutions: List[Solution]):
        """Update pheromone matrix based on solutions"""
        # Evaporate pheromones
        self.pheromone_matrix.evaporate()
        
        # Deposit pheromones
        for solution in solutions:
            # Calculate deposit amount
            deposit_amount = self.q / solution.cost
            
            # Deposit on each edge in path
            for i in range(len(solution.path) - 1):
                from_city = solution.path[i]
                to_city = solution.path[i + 1]
                self.pheromone_matrix.deposit(from_city, to_city, deposit_amount)
    
    def solve(self) -> Solution:
        """Run ant colony optimization"""
        for iteration in range(self.max_iterations):
            # Construct solutions for all ants
            solutions = []
            for _ in range(self.num_ants):
                solution = self.construct_solution()
                solutions.append(solution)
            
            # Update best solution
            current_best = min(solutions, key=lambda x: x.cost)
            if current_best.cost < self.best_cost:
                self.best_solution = current_best
                self.best_cost = current_best.cost
            
            # Update pheromones
            self.update_pheromones(solutions)
            
            # Track statistics
            avg_cost = sum(sol.cost for sol in solutions) / len(solutions)
            self.cost_history.append(avg_cost)
            self.pheromone_history.append(self.average_pheromone())
            
            # Print progress
            if iteration % 10 == 0:
                print(f"Iteration {iteration}: Best cost = {self.best_cost:.2f}, "
                      f"Avg cost = {avg_cost:.2f}")
        
        return self.best_solution
    
    def average_pheromone(self) -> float:
        """Calculate average pheromone level"""
        total_pheromone = 0.0
        count = 0
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if i != j:
                    total_pheromone += self.pheromone_matrix.matrix[i][j]
                    count += 1
        return total_pheromone / count if count > 0 else 0.0

# Example usage
def example_basic_aco():
    """Example: Basic Ant Colony Optimization for TSP"""
    
    # Create distance matrix for TSP
    num_cities = 20
    distance_matrix = []
    for i in range(num_cities):
        row = []
        for j in range(num_cities):
            if i == j:
                row.append(0.0)
            else:
                row.append(random.uniform(1.0, 100.0))
        distance_matrix.append(row)
    
    # Create cost function
    cost_func = TravelingSalesmanCost(distance_matrix)
    
    # Create ACO
    aco = AntColonyOptimization(
        num_ants=50,
        distance_matrix=distance_matrix,
        cost_function=cost_func,
        alpha=1.0,
        beta=2.0,
        evaporation_rate=0.1,
        q=100.0,
        max_iterations=200
    )
    
    # Solve
    best_solution = aco.solve()
    
    print(f"\nBest TSP tour found:")
    print(f"  Cost: {best_solution.cost:.2f}")
    print(f"  Path: {best_solution.path[:10]}...")  # Show first 10 cities
    
    return best_solution, aco

if __name__ == "__main__":
    example_basic_aco()
```

### Advanced ACO with Elitism and Local Search

```python
"""
Advanced ACO with Elitism and Local Search
"""

import random
import math
from typing import List, Tuple, Dict, Callable, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class AdvancedACOConfig:
    """Configuration for advanced ACO"""
    num_ants: int = 100
    alpha: float = 1.0
    beta: float = 2.0
    evaporation_rate: float = 0.1
    q: float = 100.0
    elitism_weight: float = 0.5
    local_search_rate: float = 0.3
    max_iterations: int = 500
    stagnation_limit: int = 50

class ElitistAntColonyOptimization:
    """ACO with elitism and local search"""
    
    def __init__(self, config: AdvancedACOConfig, distance_matrix: List[List[float]], cost_function: CostFunction):
        self.config = config
        self.distance_matrix = distance_matrix
        self.cost_function = cost_function
        self.num_cities = len(distance_matrix)
        
        # Initialize pheromone matrix
        initial_pheromone = 1.0 / (self.num_cities * self.average_distance())
        self.pheromone_matrix = PheromoneMatrix(
            matrix=[[initial_pheromone for _ in range(self.num_cities)] for _ in range(self.num_cities)],
            evaporation_rate=config.evaporation_rate
        )
        
        # Heuristic information
        self.heuristic_matrix = self.calculate_heuristic_matrix()
        
        # State
        self.global_best = None
        self.global_best_cost = float('inf')
        self.stagnation_counter = 0
        
        # Statistics
        self.cost_history = []
        self.diversity_history = []
    
    def average_distance(self) -> float:
        """Calculate average distance between cities"""
        total_distance = 0.0
        count = 0
        for i in range(self.num_cities):
            for j in range(i + 1, self.num_cities):
                total_distance += self.distance_matrix[i][j]
                count += 1
        return total_distance / count if count > 0 else 1.0
    
    def calculate_heuristic_matrix(self) -> List[List[float]]:
        """Calculate heuristic information"""
        heuristic = []
        for i in range(self.num_cities):
            row = []
            for j in range(self.num_cities):
                if i == j:
                    row.append(0.0)
                else:
                    row.append(1.0 / max(self.distance_matrix[i][j], 1e-10))
            heuristic.append(row)
        return heuristic
    
    def select_next_city_adaptive(self, current_city: int, visited: set, iteration: int) -> int:
        """Adaptive city selection with dynamic alpha/beta"""
        unvisited = [city for city in range(self.num_cities) if city not in visited]
        
        if not unvisited:
            return list(visited)[0]
        
        # Adaptive alpha and beta based on iteration
        adaptive_alpha = self.config.alpha * (1 + iteration / self.config.max_iterations)
        adaptive_beta = self.config.beta * (1 - iteration / self.config.max_iterations)
        
        # Calculate probabilities
        probabilities = []
        total_prob = 0.0
        
        for city in unvisited:
            pheromone = self.pheromone_matrix.matrix[current_city][city] ** adaptive_alpha
            heuristic = self.heuristic_matrix[current_city][city] ** adaptive_beta
            probability = pheromone * heuristic
            probabilities.append(probability)
            total_prob += probability
        
        # Select city
        if total_prob == 0:
            return random.choice(unvisited)
        
        probabilities = [p / total_prob for p in probabilities]
        
        rand = random.random()
        cumulative_prob = 0.0
        
        for i, prob in enumerate(probabilities):
            cumulative_prob += prob
            if rand <= cumulative_prob:
                return unvisited[i]
        
        return unvisited[-1]
    
    def apply_local_search(self, solution: Solution) -> Solution:
        """Apply 2-opt local search"""
        improved = True
        current_solution = solution
        
        while improved:
            improved = False
            best_neighbor = current_solution
            
            # Try all 2-opt moves
            for i in range(len(current_solution.path) - 2):
                for j in range(i + 2, len(current_solution.path) - 1):
                    # Create neighbor by reversing segment
                    neighbor_path = current_solution.path.copy()
                    neighbor_path[i:j+1] = reversed(neighbor_path[i:j+1])
                    
                    neighbor = Solution(path=neighbor_path)
                    neighbor.cost = self.cost_function.evaluate(neighbor)
                    
                    # Check if better
                    if neighbor.cost < best_neighbor.cost:
                        best_neighbor = neighbor
                        improved = True
            
            current_solution = best_neighbor
        
        return current_solution
    
    def construct_solution_with_local_search(self, iteration: int) -> Solution:
        """Construct solution with optional local search"""
        # Construct initial solution
        start_city = random.randint(0, self.num_cities - 1)
        current_city = start_city
        path = [start_city]
        visited = {start_city}
        
        while len(path) < self.num_cities:
            next_city = self.select_next_city_adaptive(current_city, visited, iteration)
            path.append(next_city)
            visited.add(next_city)
            current_city = next_city
        
        path.append(start_city)
        solution = Solution(path=path)
        solution.cost = self.cost_function.evaluate(solution)
        
        # Apply local search probabilistically
        if random.random() < self.config.local_search_rate:
            solution = self.apply_local_search(solution)
        
        return solution
    
    def update_pheromones_elitist(self, solutions: List[Solution]):
        """Update pheromones with elitism"""
        # Evaporate pheromones
        self.pheromone_matrix.evaporate()
        
        # Deposit pheromones from all solutions
        for solution in solutions:
            deposit_amount = self.config.q / solution.cost
            for i in range(len(solution.path) - 1):
                from_city = solution.path[i]
                to_city = solution.path[i + 1]
                self.pheromone_matrix.deposit(from_city, to_city, deposit_amount)
        
        # Extra deposit from global best solution (elitism)
        if self.global_best is not None:
            elitist_deposit = self.config.elitism_weight * self.config.q / self.global_best.cost
            for i in range(len(self.global_best.path) - 1):
                from_city = self.global_best.path[i]
                to_city = self.global_best.path[i + 1]
                self.pheromone_matrix.deposit(from_city, to_city, elitist_deposit)
    
    def calculate_diversity(self, solutions: List[Solution]) -> float:
        """Calculate population diversity"""
        if len(solutions) < 2:
            return 0.0
        
        # Calculate average pairwise distance
        total_distance = 0.0
        count = 0
        
        for i in range(len(solutions)):
            for j in range(i + 1, len(solutions)):
                # Calculate Hamming distance between paths
                distance = sum(1 for a, b in zip(solutions[i].path, solutions[j].path) if a != b)
                total_distance += distance
                count += 1
        
        return total_distance / count if count > 0 else 0.0
    
    def solve_advanced(self) -> Solution:
        """Run advanced ACO with elitism and local search"""
        for iteration in range(self.config.max_iterations):
            # Construct solutions
            solutions = []
            for _ in range(self.config.num_ants):
                solution = self.construct_solution_with_local_search(iteration)
                solutions.append(solution)
            
            # Update global best
            current_best = min(solutions, key=lambda x: x.cost)
            if current_best.cost < self.global_best_cost:
                self.global_best = current_best
                self.global_best_cost = current_best.cost
                self.stagnation_counter = 0
            else:
                self.stagnation_counter += 1
            
            # Update pheromones
            self.update_pheromones_elitist(solutions)
            
            # Track statistics
            avg_cost = sum(sol.cost for sol in solutions) / len(solutions)
            diversity = self.calculate_diversity(solutions)
            
            self.cost_history.append(avg_cost)
            self.diversity_history.append(diversity)
            
            # Print progress
            if iteration % 20 == 0:
                print(f"Iteration {iteration}: Best = {self.global_best_cost:.2f}, "
                      f"Avg = {avg_cost:.2f}, Diversity = {diversity:.2f}")
            
            # Check for stagnation
            if self.stagnation_counter > self.config.stagnation_limit:
                # Restart with perturbed pheromones
                self.restart_pheromones()
                self.stagnation_counter = 0
        
        return self.global_best
    
    def restart_pheromones(self):
        """Restart pheromone matrix to escape stagnation"""
        initial_pheromone = 1.0 / (self.num_cities * self.average_distance())
        
        # Add noise to prevent premature convergence
        noise_factor = 0.1
        
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                noise = random.uniform(-noise_factor, noise_factor)
                self.pheromone_matrix.matrix[i][j] = max(
                    0.1, initial_pheromone * (1 + noise)
                )

# Example usage with advanced ACO
def example_advanced_aco():
    """Example: Advanced ACO with Elitism and Local Search"""
    
    # Create TSP instance
    num_cities = 30
    distance_matrix = [[random.uniform(1, 100) for _ in range(num_cities)] for _ in range(num_cities)]
    for i in range(num_cities):
        distance_matrix[i][i] = 0.0
    
    # Create cost function
    cost_func = TravelingSalesmanCost(distance_matrix)
    
    # Create advanced ACO config
    config = AdvancedACOConfig(
        num_ants=80,
        alpha=1.0,
        beta=2.5,
        evaporation_rate=0.1,
        q=100.0,
        elitism_weight=0.8,
        local_search_rate=0.4,
        max_iterations=300,
        stagnation_limit=30
    )
    
    # Create advanced ACO
    advanced_aco = ElitistAntColonyOptimization(config, distance_matrix, cost_func)
    
    # Solve
    best_solution = advanced_aco.solve_advanced()
    
    print(f"\nAdvanced ACO Best Solution:")
    print(f"  Cost: {best_solution.cost:.2f}")
    print(f"  Cities: {len(best_solution.path)-1}")
    
    return best_solution, advanced_aco

if __name__ == "__main__":
    example_advanced_aco()
```

### Multi-Objective Ant Colony Optimization

```python
"""
Multi-Objective Ant Colony Optimization
"""

import random
import math
from typing import List, Tuple, Dict, Callable, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class MultiObjectiveSolution:
    """Multi-objective solution representation"""
    path: List[int]
    objectives: List[float]
    is_pareto_optimal: bool = False
    
    def __hash__(self):
        return hash(tuple(self.path))
    
    def __eq__(self, other):
        return self.path == other.path

class MultiObjectiveACO:
    """Multi-Objective Ant Colony Optimization"""
    
    def __init__(self, 
                 num_ants: int,
                 distance_matrix: List[List[float]],
                 time_matrix: List[List[float]],  # Time/cost matrix
                 alpha: float = 1.0,
                 beta: float = 2.0,
                 evaporation_rate: float = 0.1,
                 q: float = 100.0,
                 max_iterations: int = 200):
        """
        Initialize Multi-Objective ACO
        
        Args:
            num_ants: Number of ants
            distance_matrix: Distance matrix
            time_matrix: Time/cost matrix
            alpha, beta: ACO parameters
            evaporation_rate: Pheromone evaporation rate
            q: Pheromone deposit constant
            max_iterations: Maximum iterations
        """
        self.num_ants = num_ants
        self.distance_matrix = distance_matrix
        self.time_matrix = time_matrix
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.q = q
        self.max_iterations = max_iterations
        self.num_cities = len(distance_matrix)
        
        # Initialize pheromone matrices for each objective
        initial_pheromone = 1.0 / (self.num_cities * self.average_distance())
        self.pheromone_distance = PheromoneMatrix(
            matrix=[[initial_pheromone for _ in range(self.num_cities)] for _ in range(self.num_cities)],
            evaporation_rate=evaporation_rate
        )
        self.pheromone_time = PheromoneMatrix(
            matrix=[[initial_pheromone for _ in range(self.num_cities)] for _ in range(self.num_cities)],
            evaporation_rate=evaporation_rate
        )
        
        # Heuristic matrices
        self.heuristic_distance = self.calculate_heuristic_matrix(distance_matrix)
        self.heuristic_time = self.calculate_heuristic_matrix(time_matrix)
        
        # Pareto archive
        self.pareto_archive: List[MultiObjectiveSolution] = []
        
        # Statistics
        self.pareto_history = []
    
    def calculate_heuristic_matrix(self, matrix: List[List[float]]) -> List[List[float]]:
        """Calculate heuristic information for given matrix"""
        heuristic = []
        for i in range(self.num_cities):
            row = []
            for j in range(self.num_cities):
                if i == j:
                    row.append(0.0)
                else:
                    row.append(1.0 / max(matrix[i][j], 1e-10))
            heuristic.append(row)
        return heuristic
    
    def select_next_city_multi_objective(self, current_city: int, visited: set, weights: List[float]) -> int:
        """Select next city considering multiple objectives"""
        unvisited = [city for city in range(self.num_cities) if city not in visited]
        
        if not unvisited:
            return list(visited)[0]
        
        # Calculate combined probabilities for multiple objectives
        probabilities = []
        total_prob = 0.0
        
        for city in unvisited:
            # Calculate probability for each objective
            prob_distance = (self.pheromone_distance.matrix[current_city][city] ** self.alpha) * \
                           (self.heuristic_distance[current_city][city] ** self.beta)
            
            prob_time = (self.pheromone_time.matrix[current_city][city] ** self.alpha) * \
                       (self.heuristic_time[current_city][city] ** self.beta)
            
            # Combine probabilities using weights
            combined_prob = weights[0] * prob_distance + weights[1] * prob_time
            
            probabilities.append(combined_prob)
            total_prob += combined_prob
        
        # Select city
        if total_prob == 0:
            return random.choice(unvisited)
        
        probabilities = [p / total_prob for p in probabilities]
        
        rand = random.random()
        cumulative_prob = 0.0
        
        for i, prob in enumerate(probabilities):
            cumulative_prob += prob
            if rand <= cumulative_prob:
                return unvisited[i]
        
        return unvisited[-1]
    
    def evaluate_multi_objective(self, path: List[int]) -> List[float]:
        """Evaluate multiple objectives for a path"""
        total_distance = 0.0
        total_time = 0.0
        
        for i in range(len(path) - 1):
            from_city = path[i]
            to_city = path[i + 1]
            total_distance += self.distance_matrix[from_city][to_city]
            total_time += self.time_matrix[from_city][to_city]
        
        return [total_distance, total_time]
    
    def is_dominated(self, solution1: MultiObjectiveSolution, solution2: MultiObjectiveSolution) -> bool:
        """Check if solution1 is dominated by solution2"""
        # Minimization problem
        better_in_any = False
        worse_in_any = False
        
        for i in range(len(solution1.objectives)):
            if solution1.objectives[i] > solution2.objectives[i]:
                worse_in_any = True
            elif solution1.objectives[i] < solution2.objectives[i]:
                better_in_any = True
        
        return worse_in_any and not better_in_any
    
    def update_pareto_archive(self, solutions: List[MultiObjectiveSolution]):
        """Update Pareto archive with non-dominated solutions"""
        # Add new solutions to archive
        self.pareto_archive.extend(solutions)
        
        # Remove dominated solutions
        non_dominated = []
        for i, sol1 in enumerate(self.pareto_archive):
            is_dominated_by_any = False
            for j, sol2 in enumerate(self.pareto_archive):
                if i != j and self.is_dominated(sol1, sol2):
                    is_dominated_by_any = True
                    break
            
            if not is_dominated_by_any:
                non_dominated.append(sol1)
        
        self.pareto_archive = non_dominated
    
    def update_pheromones_multi_objective(self, solutions: List[MultiObjectiveSolution]):
        """Update pheromone matrices for multiple objectives"""
        # Evaporate pheromones
        self.pheromone_distance.evaporate()
        self.pheromone_time.evaporate()
        
        # Deposit pheromones from Pareto solutions
        for solution in self.pareto_archive:
            distance_deposit = self.q / solution.objectives[0]
            time_deposit = self.q / solution.objectives[1]
            
            for i in range(len(solution.path) - 1):
                from_city = solution.path[i]
                to_city = solution.path[i + 1]
                
                self.pheromone_distance.deposit(from_city, to_city, distance_deposit)
                self.pheromone_time.deposit(from_city, to_city, time_deposit)
    
    def solve_multi_objective(self) -> List[MultiObjectiveSolution]:
        """Run multi-objective ACO"""
        for iteration in range(self.max_iterations):
            # Construct solutions with different weight combinations
            solutions = []
            
            # Use different weight combinations to explore Pareto front
            weight_combinations = [
                [1.0, 0.0],  # Distance only
                [0.0, 1.0],  # Time only
                [0.7, 0.3],  # Distance weighted
                [0.3, 0.7],  # Time weighted
                [0.5, 0.5]   # Balanced
            ]
            
            for weights in weight_combinations:
                for _ in range(self.num_ants // len(weight_combinations)):
                    # Construct solution
                    start_city = random.randint(0, self.num_cities - 1)
                    current_city = start_city
                    path = [start_city]
                    visited = {start_city}
                    
                    while len(path) < self.num_cities:
                        next_city = self.select_next_city_multi_objective(current_city, visited, weights)
                        path.append(next_city)
                        visited.add(next_city)
                        current_city = next_city
                    
                    path.append(start_city)
                    
                    # Evaluate objectives
                    objectives = self.evaluate_multi_objective(path)
                    solution = MultiObjectiveSolution(path=path, objectives=objectives)
                    solutions.append(solution)
            
            # Update Pareto archive
            self.update_pareto_archive(solutions)
            
            # Update pheromones
            self.update_pheromones_multi_objective(solutions)
            
            # Track statistics
            self.pareto_history.append(len(self.pareto_archive))
            
            # Print progress
            if iteration % 20 == 0:
                print(f"Iteration {iteration}: Pareto archive size = {len(self.pareto_archive)}")
        
        return self.pareto_archive

# Example usage with multi-objective ACO
def example_multi_objective_aco():
    """Example: Multi-Objective ACO for TSP with distance and time"""
    
    # Create distance and time matrices
    num_cities = 20
    distance_matrix = [[random.uniform(1, 100) for _ in range(num_cities)] for _ in range(num_cities)]
    time_matrix = [[random.uniform(1, 50) for _ in range(num_cities)] for _ in range(num_cities)]
    
    for i in range(num_cities):
        distance_matrix[i][i] = 0.0
        time_matrix[i][i] = 0.0
    
    # Create multi-objective ACO
    mo_aco = MultiObjectiveACO(
        num_ants=100,
        distance_matrix=distance_matrix,
        time_matrix=time_matrix,
        alpha=1.0,
        beta=2.0,
        evaporation_rate=0.1,
        q=100.0,
        max_iterations=200
    )
    
    # Solve
    pareto_solutions = mo_aco.solve_multi_objective()
    
    print(f"\nMulti-Objective ACO Results:")
    print(f"  Pareto archive size: {len(pareto_solutions)}")
    print(f"  Best distance: {min(sol.objectives[0] for sol in pareto_solutions):.2f}")
    print(f"  Best time: {min(sol.objectives[1] for sol in pareto_solutions):.2f}")
    
    return pareto_solutions, mo_aco

if __name__ == "__main__":
    example_multi_objective_aco()
```

## Input Format

### Ant Colony Optimization Configuration

```yaml
ant_colony_config:
  problem_definition:
    num_ants: number              # Number of ants in colony
    solution_type: "path|assignment|scheduling"
    optimization_type: "minimize|maximize"
    
  algorithm_parameters:
    alpha: number                 # Pheromone importance factor
    beta: number                  # Heuristic importance factor
    evaporation_rate: number      # Rate of pheromone evaporation
    q: number                     # Pheromone deposit constant
    max_iterations: number        # Maximum number of iterations
    
  pheromone_management:
    initial_pheromone: number     # Initial pheromone level
    min_pheromone: number         # Minimum pheromone level
    max_pheromone: number         # Maximum pheromone level
    evaporation_strategy: "constant|adaptive|dynamic"
    
  colony_behavior:
    exploration_rate: number      # Rate of exploration vs exploitation
    local_search_rate: number     # Rate of local search application
    elitism_weight: number        # Weight for elite solution reinforcement
    population_diversity: number  # Desired population diversity
    
  advanced_features:
    multi_objective: boolean      # Enable multi-objective optimization
    adaptive_parameters: boolean  # Enable adaptive parameter tuning
    parallel_execution: boolean   # Enable parallel ant execution
    restart_strategy: boolean     # Enable restart strategies
    
  termination_criteria:
    max_iterations: number        # Maximum iterations
    time_limit: number            # Maximum execution time in seconds
    stagnation_limit: number      # Iterations without improvement
    pareto_convergence: number    # Pareto front convergence threshold
```

### Multi-Objective Configuration

```yaml
multi_objective_config:
  objectives:
    - objective_name: string      # Name of objective
      weight: number             # Weight in aggregation
      is_constraint: boolean     # Whether this is a constraint
      optimization_direction: "minimize|maximize"
      
  pareto_management:
    archive_size: number          # Maximum size of Pareto archive
    diversity_mechanism: string   # Diversity preservation method
    convergence_metric: string    # Metric for convergence measurement
    
  weight_strategies:
    uniform_weights: boolean      # Use uniform weight distribution
    adaptive_weights: boolean     # Adapt weights dynamically
    random_weights: boolean       # Use random weight combinations
    
  constraint_handling:
    penalty_method: "static|dynamic|adaptive"
    constraint_weights: array     # Weights for constraint violations
    feasibility_preference: boolean # Prefer feasible solutions
```

## Output Format

### Optimization Results

```yaml
optimization_results:
  best_solution:
    path: array                  # Best path found
    cost: number                 # Final cost value
    objectives: array            # Multi-objective values
    iteration_found: number      # Iteration when best was found
    
  pareto_archive:
    solutions_count: number      # Number of Pareto-optimal solutions
    diversity_metric: number     # Diversity of Pareto front
    convergence_metric: number   # Convergence of Pareto front
    spread_metric: number        # Spread of Pareto front
    
  convergence_analysis:
    convergence_iteration: number # Iteration when converged
    stagnation_detected: boolean # Whether stagnation occurred
    restart_count: number        # Number of restarts performed
    elitism_effectiveness: number # Effectiveness of elitism
    
  algorithm_statistics:
    total_iterations: number     # Total iterations performed
    pheromone_updates: number    # Number of pheromone updates
    local_search_applications: number # Number of local search applications
    population_diversity: number # Average population diversity
    
  performance_metrics:
    execution_time: number       # Total execution time
    ants_per_second: number      # Ants processed per second
    memory_usage: string         # Peak memory usage
    parallel_efficiency: number  # Efficiency of parallel processing
```

### ACO History

```yaml
aco_history:
  iteration_data: array          # Data for each iteration
  - iteration: number
    best_cost: number
    avg_cost: number
    pareto_size: number
    pheromone_level: number
    diversity: number
    
  pheromone_data: array          # Pheromone matrix evolution
  - iteration: number
    pheromone_distribution: array
    evaporation_rate: number
    deposit_amount: number
    
  population_data: array         # Population statistics
  - iteration: number
    exploration_rate: number
    exploitation_rate: number
    local_search_rate: number
```

## Configuration Options

### Pheromone Strategies

```yaml
pheromone_strategies:
  constant_evaporation:
    description: "Fixed evaporation rate throughout execution"
    best_for: ["standard_problems", "simple_optimization"]
    complexity: "O(1)"
    parameters: ["evaporation_rate"]
    
  adaptive_evaporation:
    description: "Adaptive evaporation based on convergence"
    best_for: ["complex_problems", "dynamic_environments"]
    complexity: "O(1)"
    parameters: ["adaptation_rate", "convergence_threshold"]
    
  dynamic_evaporation:
    description: "Dynamic evaporation based on population diversity"
    best_for: ["multi_modal_problems", "diversity_maintenance"]
    complexity: "O(n)"
    parameters: ["diversity_threshold", "evaporation_bounds"]
    
  elitist_deposition:
    description: "Extra deposition from elite solutions"
    best_for: ["convergence_acceleration", "quality_improvement"]
    complexity: "O(n)"
    parameters: ["elitism_weight", "elite_count"]
```

### Colony Behavior

```yaml
colony_behaviors:
  exploration_exploitation:
    description: "Balance between exploration and exploitation"
    best_for: ["all_problems", "standard_approach"]
    complexity: "O(1)"
    parameters: ["exploration_rate", "exploitation_rate"]
    
  adaptive_behavior:
    description: "Adapt behavior based on search progress"
    best_for: ["dynamic_problems", "adaptive_optimization"]
    complexity: "O(1)"
    parameters: ["adaptation_strategy", "progress_threshold"]
    
  cooperative_behavior:
    description: "Ants cooperate through shared information"
    best_for: ["complex_problems", "information_sharing"]
    complexity: "O(n)"
    parameters: ["cooperation_rate", "information_sharing"]
    
  competitive_behavior:
    description: "Ants compete for best solutions"
    best_for: ["diversity_maintenance", "exploration"]
    complexity: "O(n)"
    parameters: ["competition_rate", "selection_pressure"]
```

## Error Handling

### Optimization Failures

```yaml
optimization_failures:
  premature_convergence:
    detection_strategy: "diversity_monitoring"
    recovery_strategy: "increased_exploration"
    max_retries: 3
    fallback_action: "restart_with_perturbation"
  
  stagnation:
    detection_strategy: "improvement_monitoring"
    recovery_strategy: "pheromone_restart"
    max_retries: 2
    fallback_action: "alternative_algorithm"
  
  numerical_instability:
    detection_strategy: "value_range_checking"
    recovery_strategy: "parameter_bounds_enforcement"
    max_retries: 2
    fallback_action: "simplified_model"
  
  pareto_degeneration:
    detection_strategy: "pareto_archive_monitoring"
    recovery_strategy: "diversity_enhancement"
    max_retries: 1
    fallback_action: "single_objective_mode"
```

### Parallel Processing Failures

```yaml
parallel_failures:
  load_imbalance:
    detection_strategy: "execution_time_monitoring"
    recovery_strategy: "dynamic_load_balancing"
    max_retries: 1
    fallback_action: "fixed_partitioning"
  
  communication_failure:
    detection_strategy: "heartbeat_monitoring"
    recovery_strategy: "reconnection_attempts"
    max_retries: 3
    fallback_action: "sequential_processing"
  
  synchronization_issues:
    detection_strategy: "state_consistency_checking"
    recovery_strategy: "state_reconciliation"
    max_retries: 2
    fallback_action: "lock_free_processing"
```

## Performance Optimization

### Algorithm Optimization

```python
# Optimization: Fast pheromone matrix operations
class FastPheromoneMatrix:
    """Optimized pheromone matrix with NumPy operations"""
    
    def __init__(self, size: int, initial_value: float = 1.0):
        self.matrix = np.full((size, size), initial_value, dtype=np.float64)
        self.evaporation_rate = 0.1
        self.min_pheromone = 0.1
        self.max_pheromone = 10.0
    
    def evaporate(self):
        """Fast evaporation using NumPy"""
        self.matrix *= (1 - self.evaporation_rate)
        np.clip(self.matrix, self.min_pheromone, self.max_pheromone, out=self.matrix)
    
    def deposit_vectorized(self, paths: List[List[int]], costs: List[float]):
        """Vectorized pheromone deposition"""
        for path, cost in zip(paths, costs):
            deposit_amount = 100.0 / cost
            
            # Create edge pairs
            edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            
            # Vectorized deposition
            for from_city, to_city in edges:
                self.matrix[from_city, to_city] += deposit_amount
        
        # Ensure bounds
        np.clip(self.matrix, self.min_pheromone, self.max_pheromone, out=self.matrix)
```

### Memory Optimization

```yaml
memory_optimization:
  pheromone_compression:
    technique: "matrix_compression"
    memory_reduction: "50-70%"
    implementation: "sparse_matrix_storage"
    
  solution_caching:
    technique: "cost_caching"
    memory_reduction: "30-50%"
    implementation: "hash_based_caching"
    
  parallel_memory_sharing:
    technique: "shared_memory_objects"
    memory_reduction: "40-60%"
    implementation: "memory_mapped_files"
    
  streaming_processing:
    technique: "chunked_ant_execution"
    memory_reduction: "unlimited_colony_size"
    implementation: "iterator_based_execution"
```

## Integration Examples

### With Vehicle Routing

```python
# Integration with vehicle routing problem
class VRPACO:
    """Ant Colony Optimization for Vehicle Routing Problem"""
    
    def __init__(self, customers: List[Tuple[float, float]], 
                 demands: List[int], capacity: int, depot: Tuple[float, float]):
        self.customers = customers
        self.demands = demands
        self.capacity = capacity
        self.depot = depot
        self.num_customers = len(customers)
        
        # Create distance matrix
        self.distance_matrix = self.create_distance_matrix()
    
    def create_distance_matrix(self) -> List[List[float]]:
        """Create distance matrix including depot"""
        # Add depot at index 0
        all_points = [self.depot] + self.customers
        matrix = []
        
        for i in range(len(all_points)):
            row = []
            for j in range(len(all_points)):
                if i == j:
                    row.append(0.0)
                else:
                    dist = math.sqrt(
                        (all_points[i][0] - all_points[j][0])**2 + 
                        (all_points[i][1] - all_points[j][1])**2
                    )
                    row.append(dist)
            matrix.append(row)
        
        return matrix
    
    def evaluate_vrp_solution(self, routes: List[List[int]]) -> float:
        """Evaluate VRP solution cost"""
        total_cost = 0.0
        
        for route in routes:
            # Add depot to beginning and end
            route_with_depot = [0] + route + [0]
            
            # Calculate route cost
            for i in range(len(route_with_depot) - 1):
                from_point = route_with_depot[i]
                to_point = route_with_depot[i + 1]
                total_cost += self.distance_matrix[from_point][to_point]
        
        return total_cost
    
    def construct_vrp_solution(self) -> List[List[int]]:
        """Construct VRP solution using ACO"""
        # This is a simplified version - full VRP requires route construction logic
        # In practice, this would involve:
        # 1. Ant constructs routes considering capacity constraints
        # 2. Uses savings algorithm or similar for route building
        # 3. Applies local search for route optimization
        
        # For demonstration, return a simple solution
        unvisited = list(range(1, self.num_customers + 1))
        routes = []
        
        while unvisited:
            route = []
            current_load = 0
            
            while unvisited and current_load + self.demands[unvisited[0]-1] <= self.capacity:
                customer = unvisited.pop(0)
                route.append(customer)
                current_load += self.demands[customer-1]
            
            routes.append(route)
        
        return routes
```

### With Job Shop Scheduling

```python
# Integration with job shop scheduling
class JobShopACO:
    """Ant Colony Optimization for Job Shop Scheduling"""
    
    def __init__(self, jobs: List[List[int]], machines: List[int]):
        self.jobs = jobs  # jobs[i][j] = processing time of job i on machine j
        self.machines = machines
        self.num_jobs = len(jobs)
        self.num_machines = len(machines)
    
    def evaluate_schedule(self, schedule: List[Tuple[int, int]]) -> float:
        """Evaluate makespan of schedule"""
        # Calculate completion times
        completion_times = [[0] * self.num_machines for _ in range(self.num_jobs)]
        
        for job_idx, machine_idx in schedule:
            if machine_idx == 0:
                completion_times[job_idx][machine_idx] = (
                    completion_times[job_idx][machine_idx-1] + 
                    self.jobs[job_idx][machine_idx]
                )
            else:
                prev_job_completion = completion_times[job_idx][machine_idx-1] if machine_idx > 0 else 0
                prev_machine_completion = completion_times[job_idx-1][machine_idx] if job_idx > 0 else 0
                completion_times[job_idx][machine_idx] = max(
                    prev_job_completion, prev_machine_completion
                ) + self.jobs[job_idx][machine_idx]
        
        # Makespan is maximum completion time
        return max(max(row) for row in completion_times)
    
    def construct_schedule_solution(self) -> List[Tuple[int, int]]:
        """Construct job shop schedule using ACO"""
        # This is a simplified version - full job shop requires operation ordering
        # In practice, this would involve:
        # 1. Ant constructs operation sequences
        # 2. Uses precedence constraints
        # 3. Applies machine assignment rules
        
        # For demonstration, return a simple schedule
        schedule = []
        for job_idx in range(self.num_jobs):
            for machine_idx in range(self.num_machines):
                schedule.append((job_idx, machine_idx))
        
        return schedule
```

## Best Practices

1. **Parameter Tuning**:
   - Start with standard parameters (α=1, β=2, ρ=0.1)
   - Use adaptive parameters for dynamic problems
   - Monitor convergence and adjust accordingly

2. **Pheromone Management**:
   - Implement proper evaporation to prevent premature convergence
   - Use elitism to accelerate convergence
   - Maintain pheromone bounds to prevent numerical issues

3. **Colony Behavior**:
   - Balance exploration and exploitation
   - Use local search for solution refinement
   - Implement restart strategies for stagnation

4. **Multi-objective Optimization**:
   - Use diverse weight combinations to explore Pareto front
   - Maintain Pareto archive for solution diversity
   - Apply diversity preservation mechanisms

## Troubleshooting

### Common Issues

1. **Poor Solution Quality**: Increase colony size, adjust α/β parameters, improve heuristic information
2. **Slow Convergence**: Use elitism, increase pheromone deposit, apply local search
3. **Premature Convergence**: Increase evaporation rate, add noise to pheromones, use restart strategies
4. **High Computational Cost**: Optimize pheromone operations, use parallel processing, implement early termination

### Debug Mode

```python
# Debug mode: Enhanced ACO debugging
class DebugAntColonyOptimization:
    """ACO with enhanced debugging capabilities"""
    
    def __init__(self, config):
        self.config = config
        self.debug_log = []
        self.pheromone_analysis = {}
        self.convergence_analysis = {}
    
    def log_iteration(self, iteration_data):
        """Log detailed iteration information"""
        self.debug_log.append({
            'iteration': iteration_data['iteration'],
            'best_cost': iteration_data['best_cost'],
            'avg_cost': iteration_data['avg_cost'],
            'pheromone_diversity': iteration_data['pheromone_diversity'],
            'population_diversity': iteration_data['population_diversity'],
            'elitism_effectiveness': iteration_data['elitism_effectiveness']
        })
    
    def analyze_pheromone_distribution(self):
        """Analyze pheromone distribution patterns"""
        pheromone_values = []
        for entry in self.debug_log:
            pheromone_values.append(entry['pheromone_diversity'])
        
        self.pheromone_analysis = {
            'avg_diversity': sum(pheromone_values) / len(pheromone_values),
            'diversity_trend': 'increasing' if pheromone_values[-1] > pheromone_values[0] else 'decreasing',
            'convergence_indicators': self.detect_convergence_indicators()
        }
        
        return self.pheromone_analysis
    
    def generate_debug_report(self):
        """Generate comprehensive debug report"""
        return {
            'execution_summary': self.get_execution_summary(),
            'pheromone_analysis': self.analyze_pheromone_distribution(),
            'convergence_analysis': self.analyze_convergence(),
            'parameter_effectiveness': self.get_parameter_effectiveness(),
            'recommendations': self.get_recommendations()
        }
```

## Monitoring and Metrics

### ACO Performance Metrics

```yaml
aco_performance_metrics:
  convergence_metrics:
    convergence_speed: number     # Iterations to convergence
    convergence_stability: number # Stability of convergence
    solution_quality: number      # Quality of final solution
    
  exploration_metrics:
    search_space_coverage: number # Coverage of search space
    diversity_maintenance: number # Maintenance of solution diversity
    pheromone_distribution: number # Distribution of pheromone trails
    
  efficiency_metrics:
    ants_per_second: number       # Ants processed per second
    memory_efficiency: number     # Memory usage efficiency
    parallel_efficiency: number   # Efficiency of parallel processing
    
  robustness_metrics:
    parameter_sensitivity: number # Sensitivity to parameter changes
    problem_adaptability: number  # Adaptability to different problems
    convergence_reliability: number # Reliability of convergence
```

## Dependencies

- **Mathematical Libraries**: NumPy, SciPy for mathematical operations
- **Optimization Libraries**: DEAP, PyGAD for advanced optimization features
- **Parallel Processing**: multiprocessing, concurrent.futures for parallel execution
- **Visualization**: Matplotlib, Plotly for result visualization
- **Graph Libraries**: NetworkX for graph-based problems

## Version History

- **1.0.0**: Initial release with comprehensive ACO frameworks
- **1.1.0**: Added elitism and local search capabilities
- **1.2.0**: Enhanced multi-objective optimization and Pareto front management
- **1.3.0**: Improved debugging tools and performance monitoring
- **1.4.0**: Advanced integration with VRP and scheduling problems

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

Content for ## Constraints involving Ant Colony Optimization.