---
Domain: search_algorithms
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: simulated-annealing
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

Automatically designs and implements optimal simulated annealing algorithms for solving complex optimization problems, including combinatorial optimization, continuous optimization, and global optimization. This skill provides comprehensive frameworks for temperature scheduling, neighborhood generation, acceptance criteria, and convergence analysis.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Temperature Scheduling**: Implement exponential, linear, logarithmic, and adaptive cooling schedules
- **Neighborhood Generation**: Design problem-specific neighborhood functions for solution space exploration
- **Acceptance Criteria**: Implement Metropolis criterion with adaptive acceptance probabilities
- **Annealing Strategies**: Support for reheating, restart strategies, and parallel tempering
- **Convergence Analysis**: Monitor convergence, detect optimal stopping points, and implement adaptive termination
- **Multi-objective Optimization**: Extend simulated annealing for multi-objective problems with Pareto optimization
- **Hybrid Approaches**: Combine with other algorithms (genetic algorithms, tabu search) for enhanced performance

## Usage Examples

### Basic Simulated Annealing Framework

```python
"""
Basic Simulated Annealing Framework
"""

import random
import math
from typing import List, Tuple, Dict, Callable, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Solution:
    """Solution representation"""
    state: List[float]
    cost: float = 0.0
    temperature: float = 0.0
    
    def __hash__(self):
        return hash(tuple(self.state))
    
    def __eq__(self, other):
        return self.state == other.state

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

class RastriginCost(CostFunction):
    """Rastrigin function for optimization testing"""
    
    def __init__(self, A: float = 10.0):
        self.A = A
    
    def evaluate(self, solution: Solution) -> float:
        """Evaluate Rastrigin function"""
        n = len(solution.state)
        sum_term = sum(x**2 - self.A * math.cos(2 * math.pi * x) for x in solution.state)
        return self.A * n + sum_term
    
    def is_minimization(self) -> bool:
        return True  # Minimization problem

class SimulatedAnnealing:
    """Basic Simulated Annealing implementation"""
    
    def __init__(self, 
                 initial_solution: Solution,
                 cost_function: CostFunction,
                 initial_temperature: float = 1000.0,
                 cooling_rate: float = 0.95,
                 min_temperature: float = 1e-8,
                 max_iterations: int = 10000,
                 neighborhood_size: int = 10):
        """
        Initialize Simulated Annealing
        
        Args:
            initial_solution: Starting solution
            cost_function: Cost function to optimize
            initial_temperature: Starting temperature
            cooling_rate: Rate of temperature decrease
            min_temperature: Minimum temperature threshold
            max_iterations: Maximum number of iterations
            neighborhood_size: Number of neighbors to generate
        """
        self.initial_solution = initial_solution
        self.cost_function = cost_function
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature
        self.max_iterations = max_iterations
        self.neighborhood_size = neighborhood_size
        
        # Current state
        self.current_solution = initial_solution
        self.best_solution = initial_solution
        self.temperature = initial_temperature
        
        # Statistics
        self.cost_history: List[float] = []
        self.temperature_history: List[float] = []
        self.acceptance_history: List[float] = []
        
        # Initialize costs
        self.current_solution.cost = self.cost_function.evaluate(self.current_solution)
        self.best_solution.cost = self.current_solution.cost
    
    def generate_neighbor(self, solution: Solution) -> Solution:
        """Generate a neighboring solution"""
        neighbor_state = solution.state.copy()
        
        # Randomly perturb one or more dimensions
        for _ in range(random.randint(1, min(3, len(solution.state)))):
            index = random.randint(0, len(solution.state) - 1)
            # Gaussian perturbation
            perturbation = random.gauss(0, 0.1)
            neighbor_state[index] += perturbation
            
            # Ensure bounds (-5.12 to 5.12 for Rastrigin)
            neighbor_state[index] = max(-5.12, min(5.12, neighbor_state[index]))
        
        neighbor = Solution(state=neighbor_state, temperature=self.temperature)
        neighbor.cost = self.cost_function.evaluate(neighbor)
        
        return neighbor
    
    def acceptance_probability(self, current_cost: float, new_cost: float, temperature: float) -> float:
        """Calculate acceptance probability using Metropolis criterion"""
        if self.cost_function.is_minimization():
            if new_cost <= current_cost:
                return 1.0
            else:
                return math.exp(-(new_cost - current_cost) / temperature)
        else:
            if new_cost >= current_cost:
                return 1.0
            else:
                return math.exp((new_cost - current_cost) / temperature)
    
    def cool_temperature(self) -> float:
        """Cool the temperature"""
        return self.temperature * self.cooling_rate
    
    def should_terminate(self, iteration: int, acceptance_rate: float) -> bool:
        """Check termination criteria"""
        # Temperature too low
        if self.temperature < self.min_temperature:
            return True
        
        # Maximum iterations reached
        if iteration >= self.max_iterations:
            return True
        
        # Low acceptance rate (convergence)
        if acceptance_rate < 0.01 and iteration > 100:
            return True
        
        return False
    
    def solve(self) -> Solution:
        """Run simulated annealing optimization"""
        iteration = 0
        accepted_count = 0
        
        while not self.should_terminate(iteration, accepted_count / max(1, iteration)):
            # Generate neighborhood
            neighbors = []
            for _ in range(self.neighborhood_size):
                neighbor = self.generate_neighbor(self.current_solution)
                neighbors.append(neighbor)
            
            # Select best neighbor
            if self.cost_function.is_minimization():
                best_neighbor = min(neighbors, key=lambda x: x.cost)
            else:
                best_neighbor = max(neighbors, key=lambda x: x.cost)
            
            # Calculate acceptance probability
            acceptance_prob = self.acceptance_probability(
                self.current_solution.cost, 
                best_neighbor.cost, 
                self.temperature
            )
            
            # Accept or reject
            if random.random() < acceptance_prob:
                self.current_solution = best_neighbor
                accepted_count += 1
                
                # Update best solution
                if ((self.cost_function.is_minimization() and best_neighbor.cost < self.best_solution.cost) or
                    (not self.cost_function.is_minimization() and best_neighbor.cost > self.best_solution.cost)):
                    self.best_solution = best_neighbor
            
            # Cool temperature
            self.temperature = self.cool_temperature()
            
            # Track statistics
            self.cost_history.append(self.current_solution.cost)
            self.temperature_history.append(self.temperature)
            self.acceptance_history.append(accepted_count / max(1, iteration + 1))
            
            # Print progress
            if iteration % 1000 == 0:
                print(f"Iteration {iteration}: Best cost = {self.best_solution.cost:.6f}, "
                      f"Temp = {self.temperature:.6f}, Acceptance = {accepted_count/(iteration+1):.3f}")
            
            iteration += 1
        
        return self.best_solution

# Example usage
def example_basic_sa():
    """Example: Basic Simulated Annealing optimization"""
    
    # Create initial solution
    initial_state = [random.uniform(-5.12, 5.12) for _ in range(10)]
    initial_solution = Solution(state=initial_state)
    
    # Create cost function
    cost_func = RastriginCost()
    
    # Create SA
    sa = SimulatedAnnealing(
        initial_solution=initial_solution,
        cost_function=cost_func,
        initial_temperature=1000.0,
        cooling_rate=0.95,
        min_temperature=1e-8,
        max_iterations=20000,
        neighborhood_size=20
    )
    
    # Solve
    best_solution = sa.solve()
    
    print(f"\nBest solution found:")
    print(f"  Cost: {best_solution.cost:.6f}")
    print(f"  State: {best_solution.state[:5]}...")  # Show first 5 values
    
    return best_solution, sa

if __name__ == "__main__":
    example_basic_sa()
```

### Advanced Simulated Annealing with Adaptive Cooling

```python
"""
Advanced Simulated Annealing with Adaptive Cooling
"""

import random
import math
import numpy as np
from typing import List, Tuple, Dict, Callable, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class AdaptiveSAConfig:
    """Configuration for adaptive simulated annealing"""
    initial_temperature: float = 1000.0
    min_temperature: float = 1e-8
    max_iterations: int = 50000
    neighborhood_size: int = 50
    cooling_strategy: str = "adaptive"  # "exponential", "linear", "logarithmic", "adaptive"
    reheating_threshold: float = 0.1    # Reheat when acceptance rate drops below this
    restart_threshold: float = 0.01     # Restart when improvement stalls

class AdaptiveCoolingSchedule:
    """Adaptive cooling schedule"""
    
    def __init__(self, config: AdaptiveSAConfig):
        self.config = config
        self.history = []
        self.acceptance_rates = []
        
    def get_temperature(self, iteration: int, current_temp: float, 
                       acceptance_rate: float) -> float:
        """Get next temperature based on adaptive strategy"""
        
        if self.config.cooling_strategy == "exponential":
            return current_temp * 0.95
        
        elif self.config.cooling_strategy == "linear":
            return current_temp - 0.1
        
        elif self.config.cooling_strategy == "logarithmic":
            return current_temp / (1 + 0.01 * math.log(iteration + 1))
        
        elif self.config.cooling_strategy == "adaptive":
            # Adaptive cooling based on acceptance rate
            if acceptance_rate > 0.5:
                # High acceptance - cool slowly
                return current_temp * 0.98
            elif acceptance_rate > 0.1:
                # Medium acceptance - cool normally
                return current_temp * 0.95
            else:
                # Low acceptance - cool quickly
                return current_temp * 0.85
        
        return current_temp

class MultiObjectiveSA:
    """Multi-objective simulated annealing"""
    
    def __init__(self, objectives: List[CostFunction], weights: List[float] = None):
        self.objectives = objectives
        self.weights = weights or [1.0] * len(objectives)
        
    def evaluate(self, solution: Solution) -> float:
        """Evaluate multi-objective cost"""
        costs = [obj.evaluate(solution) for obj in self.objectives]
        return sum(w * c for w, c in zip(self.weights, costs))
    
    def is_minimization(self) -> bool:
        return all(obj.is_minimization() for obj in self.objectives)

class ParallelTemperingSA:
    """Parallel tempering (replica exchange) simulated annealing"""
    
    def __init__(self, num_replicas: int = 4, temperature_range: Tuple[float, float] = (100.0, 1000.0)):
        self.num_replicas = num_replicas
        self.temperature_range = temperature_range
        self.replicas = []
        
    def initialize_replicas(self, initial_solution: Solution, cost_function: CostFunction):
        """Initialize replicas with different temperatures"""
        temp_min, temp_max = self.temperature_range
        temperatures = np.logspace(math.log10(temp_min), math.log10(temp_max), self.num_replicas)
        
        self.replicas = []
        for temp in temperatures:
            replica_solution = Solution(
                state=initial_solution.state.copy(),
                cost=cost_function.evaluate(initial_solution),
                temperature=temp
            )
            self.replicas.append(replica_solution)
    
    def exchange_replicas(self, cost_function: CostFunction):
        """Exchange configurations between replicas"""
        for i in range(len(self.replicas) - 1):
            replica1, replica2 = self.replicas[i], self.replicas[i + 1]
            
            # Calculate exchange probability
            delta_e = (replica2.cost - replica1.cost) * (1/replica1.temperature - 1/replica2.temperature)
            exchange_prob = min(1.0, math.exp(-delta_e))
            
            if random.random() < exchange_prob:
                # Swap configurations
                replica1.state, replica2.state = replica2.state.copy(), replica1.state.copy()
                replica1.cost = cost_function.evaluate(replica1)
                replica2.cost = cost_function.evaluate(replica2)

class AdvancedSimulatedAnnealing:
    """Advanced SA with adaptive features"""
    
    def __init__(self, config: AdaptiveSAConfig):
        self.config = config
        self.cooling_schedule = AdaptiveCoolingSchedule(config)
        
        # State tracking
        self.temperature_history = []
        self.cost_history = []
        self.acceptance_history = []
        
        # Adaptive features
        self.reheating_count = 0
        self.restart_count = 0
        self.stagnation_counter = 0
        self.best_cost_history = []
    
    def generate_adaptive_neighbor(self, solution: Solution, iteration: int) -> Solution:
        """Generate neighbor with adaptive perturbation"""
        neighbor_state = solution.state.copy()
        
        # Adaptive perturbation size based on temperature
        perturbation_scale = max(0.01, solution.temperature / 1000.0)
        
        # Perturb multiple dimensions
        num_perturbations = random.randint(1, min(5, len(solution.state)))
        
        for _ in range(num_perturbations):
            index = random.randint(0, len(solution.state) - 1)
            
            # Gaussian perturbation scaled by temperature
            perturbation = random.gauss(0, perturbation_scale)
            neighbor_state[index] += perturbation
            
            # Ensure bounds
            neighbor_state[index] = max(-5.12, min(5.12, neighbor_state[index]))
        
        neighbor = Solution(state=neighbor_state, temperature=solution.temperature)
        return neighbor
    
    def adaptive_acceptance_probability(self, current_cost: float, new_cost: float, 
                                       temperature: float, iteration: int) -> float:
        """Adaptive acceptance probability with memory"""
        # Base Metropolis criterion
        if self.config.cooling_strategy == "adaptive":
            if new_cost <= current_cost:
                return 1.0
            else:
                # Adaptive acceptance based on history
                recent_improvements = self.best_cost_history[-10:] if self.best_cost_history else [current_cost]
                improvement_rate = (current_cost - min(recent_improvements)) / max(1e-10, current_cost)
                
                # Higher acceptance if improvements are rare
                adaptive_factor = 1.0 + (1.0 - improvement_rate)
                return math.exp(-(new_cost - current_cost) / (temperature * adaptive_factor))
        else:
            # Standard Metropolis
            if new_cost <= current_cost:
                return 1.0
            else:
                return math.exp(-(new_cost - current_cost) / temperature)
    
    def should_reheat(self, acceptance_rate: float, iteration: int) -> bool:
        """Check if reheating is needed"""
        if acceptance_rate < self.config.reheating_threshold and iteration > 1000:
            return True
        return False
    
    def should_restart(self, iteration: int) -> bool:
        """Check if restart is needed"""
        if len(self.best_cost_history) > 100:
            recent_costs = self.best_cost_history[-100:]
            if max(recent_costs) - min(recent_costs) < 1e-6:
                return True
        return False
    
    def solve_adaptive(self, initial_solution: Solution, cost_function: CostFunction) -> Solution:
        """Run adaptive simulated annealing"""
        current_solution = Solution(
            state=initial_solution.state.copy(),
            cost=cost_function.evaluate(initial_solution),
            temperature=self.config.initial_temperature
        )
        
        best_solution = current_solution
        temperature = self.config.initial_temperature
        
        iteration = 0
        accepted_count = 0
        
        while iteration < self.config.max_iterations and temperature > self.config.min_temperature:
            # Generate adaptive neighbor
            neighbor = self.generate_adaptive_neighbor(current_solution, iteration)
            neighbor.cost = cost_function.evaluate(neighbor)
            
            # Calculate adaptive acceptance probability
            acceptance_prob = self.adaptive_acceptance_probability(
                current_solution.cost, neighbor.cost, temperature, iteration
            )
            
            # Accept or reject
            if random.random() < acceptance_prob:
                current_solution = neighbor
                accepted_count += 1
                
                # Update best solution
                if neighbor.cost < best_solution.cost:
                    best_solution = neighbor
                    self.stagnation_counter = 0
                else:
                    self.stagnation_counter += 1
            
            # Track history
            self.best_cost_history.append(best_solution.cost)
            self.cost_history.append(current_solution.cost)
            self.temperature_history.append(temperature)
            
            # Adaptive features
            acceptance_rate = accepted_count / max(1, iteration + 1)
            
            # Reheating
            if self.should_reheat(acceptance_rate, iteration):
                temperature = min(self.config.initial_temperature, temperature * 2.0)
                self.reheating_count += 1
                print(f"Reheating at iteration {iteration}, temp = {temperature:.6f}")
            
            # Restart
            if self.should_restart(iteration):
                # Restart with best solution
                current_solution = Solution(
                    state=best_solution.state.copy(),
                    cost=best_solution.cost,
                    temperature=temperature
                )
                self.restart_count += 1
                print(f"Restarting at iteration {iteration}")
            
            # Cool temperature
            temperature = self.cooling_schedule.get_temperature(
                iteration, temperature, acceptance_rate
            )
            
            # Reset counters
            if iteration % 1000 == 0:
                accepted_count = 0
            
            # Print progress
            if iteration % 2000 == 0:
                print(f"Iteration {iteration}: Best = {best_solution.cost:.6f}, "
                      f"Temp = {temperature:.6f}, Acceptance = {acceptance_rate:.3f}")
            
            iteration += 1
        
        return best_solution

# Example usage with advanced SA
def example_advanced_sa():
    """Example: Advanced Simulated Annealing"""
    
    # Create initial solution
    initial_state = [random.uniform(-5.12, 5.12) for _ in range(10)]
    initial_solution = Solution(state=initial_state)
    
    # Create cost function
    cost_func = RastriginCost()
    
    # Create adaptive SA config
    config = AdaptiveSAConfig(
        initial_temperature=2000.0,
        cooling_strategy="adaptive",
        max_iterations=30000,
        neighborhood_size=30
    )
    
    # Create advanced SA
    advanced_sa = AdvancedSimulatedAnnealing(config)
    
    # Solve
    best_solution = advanced_sa.solve_adaptive(initial_solution, cost_func)
    
    print(f"\nAdvanced SA Best Solution:")
    print(f"  Cost: {best_solution.cost:.6f}")
    print(f"  Reheatings: {advanced_sa.reheating_count}")
    print(f"  Restarts: {advanced_sa.restart_count}")
    
    return best_solution, advanced_sa

if __name__ == "__main__":
    example_advanced_sa()
```

### Hybrid Simulated Annealing with Genetic Algorithm

```python
"""
Hybrid Simulated Annealing with Genetic Algorithm
"""

import random
import math
import numpy as np
from typing import List, Tuple, Dict, Callable, Any
from dataclasses import dataclass

@dataclass
class HybridSolution:
    """Solution for hybrid algorithm"""
    state: List[float]
    cost: float = 0.0
    temperature: float = 0.0
    generation: int = 0
    fitness: float = 0.0

class HybridAnnealingGA:
    """Hybrid SA-GA algorithm"""
    
    def __init__(self, 
                 population_size: int = 50,
                 initial_temperature: float = 1000.0,
                 cooling_rate: float = 0.95,
                 crossover_rate: float = 0.8,
                 mutation_rate: float = 0.1,
                 elite_rate: float = 0.1):
        """
        Initialize hybrid algorithm
        
        Args:
            population_size: Size of population
            initial_temperature: Starting temperature for SA
            cooling_rate: Cooling rate for SA
            crossover_rate: Crossover probability for GA
            mutation_rate: Mutation probability for GA
            elite_rate: Elite preservation rate
        """
        self.population_size = population_size
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elite_rate = elite_rate
        
        # State
        self.population: List[HybridSolution] = []
        self.temperature = initial_temperature
        self.best_solution: HybridSolution = None
        
        # Statistics
        self.cost_history = []
        self.temperature_history = []
    
    def initialize_population(self, solution_length: int, cost_function: Callable) -> List[HybridSolution]:
        """Initialize population with random solutions"""
        population = []
        for _ in range(self.population_size):
            state = [random.uniform(-5.12, 5.12) for _ in range(solution_length)]
            solution = HybridSolution(
                state=state,
                temperature=self.temperature,
                generation=0
            )
            solution.cost = cost_function(solution)
            solution.fitness = 1.0 / (1.0 + solution.cost)  # Convert cost to fitness
            population.append(solution)
        
        return population
    
    def selection_tournament(self, population: List[HybridSolution], k: int = 3) -> HybridSolution:
        """Tournament selection"""
        tournament = random.sample(population, k)
        return max(tournament, key=lambda x: x.fitness)
    
    def crossover(self, parent1: HybridSolution, parent2: HybridSolution) -> Tuple[HybridSolution, HybridSolution]:
        """Uniform crossover"""
        if random.random() > self.crossover_rate:
            return parent1, parent2
        
        child1_state = []
        child2_state = []
        
        for i in range(len(parent1.state)):
            if random.random() < 0.5:
                child1_state.append(parent1.state[i])
                child2_state.append(parent2.state[i])
            else:
                child1_state.append(parent2.state[i])
                child2_state.append(parent1.state[i])
        
        child1 = HybridSolution(
            state=child1_state,
            temperature=self.temperature,
            generation=max(parent1.generation, parent2.generation) + 1
        )
        child2 = HybridSolution(
            state=child2_state,
            temperature=self.temperature,
            generation=max(parent1.generation, parent2.generation) + 1
        )
        
        return child1, child2
    
    def mutate(self, solution: HybridSolution) -> HybridSolution:
        """Gaussian mutation"""
        if random.random() > self.mutation_rate:
            return solution
        
        mutated_state = solution.state.copy()
        
        # Mutate random positions
        for _ in range(random.randint(1, 3)):
            index = random.randint(0, len(solution.state) - 1)
            mutation = random.gauss(0, 0.1 * (self.temperature / self.initial_temperature))
            mutated_state[index] += mutation
            
            # Ensure bounds
            mutated_state[index] = max(-5.12, min(5.12, mutated_state[index]))
        
        return HybridSolution(
            state=mutated_state,
            temperature=self.temperature,
            generation=solution.generation
        )
    
    def simulated_annealing_step(self, solution: HybridSolution, cost_function: Callable) -> HybridSolution:
        """Perform SA step on a solution"""
        # Generate neighbor
        neighbor_state = solution.state.copy()
        index = random.randint(0, len(solution.state) - 1)
        perturbation = random.gauss(0, 0.1)
        neighbor_state[index] += perturbation
        neighbor_state[index] = max(-5.12, min(5.12, neighbor_state[index]))
        
        neighbor = HybridSolution(
            state=neighbor_state,
            temperature=self.temperature,
            generation=solution.generation
        )
        neighbor.cost = cost_function(neighbor)
        
        # Acceptance criterion
        delta_cost = neighbor.cost - solution.cost
        if delta_cost <= 0 or random.random() < math.exp(-delta_cost / self.temperature):
            return neighbor
        else:
            return solution
    
    def evolve_generation(self, cost_function: Callable) -> HybridSolution:
        """Evolve one generation"""
        # Get elite solutions
        elite_size = int(self.population_size * self.elite_rate)
        sorted_population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        new_population = sorted_population[:elite_size]
        
        # Generate offspring
        while len(new_population) < self.population_size:
            # Selection
            parent1 = self.selection_tournament(self.population)
            parent2 = self.selection_tournament(self.population)
            
            # Crossover
            child1, child2 = self.crossover(parent1, parent2)
            
            # Mutation
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)
            
            # Simulated annealing refinement
            child1 = self.simulated_annealing_step(child1, cost_function)
            child2 = self.simulated_annealing_step(child2, cost_function)
            
            # Evaluate
            child1.cost = cost_function(child1)
            child1.fitness = 1.0 / (1.0 + child1.cost)
            child2.cost = cost_function(child2)
            child2.fitness = 1.0 / (1.0 + child2.cost)
            
            new_population.extend([child1, child2])
        
        self.population = new_population[:self.population_size]
        
        # Update best solution
        current_best = max(self.population, key=lambda x: x.fitness)
        if self.best_solution is None or current_best.fitness > self.best_solution.fitness:
            self.best_solution = current_best
        
        return current_best
    
    def solve_hybrid(self, solution_length: int, cost_function: Callable, 
                    max_generations: int = 1000) -> HybridSolution:
        """Run hybrid SA-GA algorithm"""
        # Initialize population
        self.population = self.initialize_population(solution_length, cost_function)
        self.temperature = self.initial_temperature
        
        for generation in range(max_generations):
            # Evolve generation
            current_best = self.evolve_generation(cost_function)
            
            # Cool temperature
            self.temperature *= self.cooling_rate
            
            # Track statistics
            self.cost_history.append(current_best.cost)
            self.temperature_history.append(self.temperature)
            
            # Print progress
            if generation % 100 == 0:
                print(f"Generation {generation}: Best cost = {current_best.cost:.6f}, "
                      f"Temp = {self.temperature:.6f}")
        
        return self.best_solution

# Example usage with hybrid algorithm
def example_hybrid_sa_ga():
    """Example: Hybrid Simulated Annealing and Genetic Algorithm"""
    
    def rastrigin_hybrid(solution):
        """Rastrigin function for hybrid algorithm"""
        n = len(solution.state)
        A = 10.0
        sum_term = sum(x**2 - A * math.cos(2 * math.pi * x) for x in solution.state)
        return A * n + sum_term
    
    # Create hybrid algorithm
    hybrid = HybridAnnealingGA(
        population_size=100,
        initial_temperature=1000.0,
        cooling_rate=0.95,
        crossover_rate=0.8,
        mutation_rate=0.1,
        elite_rate=0.1
    )
    
    # Solve
    best_solution = hybrid.solve_hybrid(
        solution_length=10,
        cost_function=rastrigin_hybrid,
        max_generations=500
    )
    
    print(f"\nHybrid SA-GA Best Solution:")
    print(f"  Cost: {best_solution.cost:.6f}")
    print(f"  Generation: {best_solution.generation}")
    
    return best_solution, hybrid

if __name__ == "__main__":
    example_hybrid_sa_ga()
```

## Input Format

### Simulated Annealing Configuration

```yaml
simulated_annealing_config:
  problem_definition:
    solution_length: number       # Length of solution vector
    variable_bounds: array        # Bounds for each variable [min, max]
    optimization_type: "minimize|maximize"
    
  algorithm_parameters:
    initial_temperature: number   # Starting temperature
    min_temperature: number       # Minimum temperature threshold
    cooling_rate: number          # Rate of temperature decrease
    max_iterations: number        # Maximum number of iterations
    neighborhood_size: number     # Number of neighbors to generate per iteration
    
  cooling_schedule:
    schedule_type: "exponential|linear|logarithmic|adaptive"
    cooling_factor: number        # Factor for exponential cooling
    linear_step: number           # Step size for linear cooling
    logarithmic_base: number      # Base for logarithmic cooling
    
  acceptance_criteria:
    metropolis_criterion: boolean # Use standard Metropolis criterion
    adaptive_acceptance: boolean  # Use adaptive acceptance probabilities
    reheating_enabled: boolean    # Enable reheating strategies
    restart_enabled: boolean      # Enable restart strategies
    
  hybrid_parameters:
    enable_ga_hybrid: boolean     # Combine with genetic algorithm
    enable_tabu_hybrid: boolean   # Combine with tabu search
    hybrid_ratio: number          # Ratio of hybrid operations
    
  termination_criteria:
    max_iterations: number        # Maximum iterations
    min_temperature: number       # Minimum temperature
    stagnation_limit: number      # Iterations without improvement
    time_limit: number            # Maximum execution time in seconds
```

### Multi-Objective Configuration

```yaml
multi_objective_sa_config:
  objectives:
    - objective_name: string      # Name of objective
      weight: number             # Weight in aggregation
      is_constraint: boolean     # Whether this is a constraint
      
  aggregation_method:
    method: "weighted_sum|pareto|lexicographic"
    pareto_config:
      archive_size: number       # Size of Pareto archive
      diversity_weight: number   # Weight for diversity preservation
      
  constraint_handling:
    penalty_method: "static|dynamic|adaptive"
    constraint_weights: array    # Weights for constraint violations
    feasibility_threshold: number # Threshold for feasible solutions
```

## Output Format

### Optimization Results

```yaml
optimization_results:
  best_solution:
    state: array                 # Best solution found
    cost: number                 # Final cost value
    iteration_found: number      # Iteration when best was found
    temperature_at_best: number  # Temperature when best was found
    
  convergence_analysis:
    convergence_iteration: number # Iteration when converged
    convergence_temperature: number # Temperature at convergence
    stagnation_detected: boolean # Whether stagnation occurred
    reheating_count: number      # Number of reheating events
    restart_count: number        # Number of restarts performed
    
  algorithm_statistics:
    total_iterations: number     # Total iterations performed
    acceptance_rate: number      # Overall acceptance rate
    average_acceptance_rate: number # Average acceptance rate
    temperature_progression: array # Temperature over time
    
  performance_metrics:
    execution_time: number       # Total execution time
    iterations_per_second: number # Iterations per second
    memory_usage: string         # Peak memory usage
    convergence_speed: number    # Speed of convergence
```

### Annealing History

```yaml
annealing_history:
  iteration_data: array          # Data for each iteration
  - iteration: number
    temperature: number
    current_cost: number
    best_cost: number
    acceptance_rate: number
    neighborhood_size: number
    
  temperature_schedule:
    initial_temperature: number
    final_temperature: number
    cooling_curve: array         # Temperature progression
    cooling_rate_history: array  # Adaptive cooling rates
    
  acceptance_analysis:
    acceptance_rates: array      # Acceptance rate over time
    rejection_reasons: array     # Reasons for rejection
    improvement_statistics: array # Statistics on improvements
```

## Configuration Options

### Cooling Schedules

```yaml
cooling_schedules:
  exponential_cooling:
    description: "Temperature decreases exponentially"
    best_for: ["general_purpose", "fast_convergence"]
    complexity: "O(1)"
    parameters: ["cooling_rate", "initial_temperature"]
    
  linear_cooling:
    description: "Temperature decreases linearly"
    best_for: ["steady_convergence", "detailed_search"]
    complexity: "O(1)"
    parameters: ["cooling_step", "initial_temperature"]
    
  logarithmic_cooling:
    description: "Temperature decreases logarithmically"
    best_for: ["theoretical_optimality", "slow_convergence"]
    complexity: "O(log n)"
    parameters: ["logarithmic_base", "initial_temperature"]
    
  adaptive_cooling:
    description: "Temperature adapts based on acceptance rate"
    best_for: ["dynamic_problems", "adaptive_optimization"]
    complexity: "O(1)"
    parameters: ["acceptance_target", "adaptation_rate"]
```

### Neighborhood Generation

```yaml
neighborhood_generation:
  gaussian_perturbation:
    description: "Add Gaussian noise to current solution"
    best_for: ["continuous_optimization", "smooth_landscapes"]
    complexity: "O(n)"
    parameters: ["perturbation_scale", "dimensions_to_perturb"]
    
  uniform_perturbation:
    description: "Add uniform random noise"
    best_for: ["exploration", "rough_landscapes"]
    complexity: "O(n)"
    parameters: ["perturbation_range", "dimensions_to_perturb"]
    
  problem_specific:
    description: "Use problem-specific neighborhood operators"
    best_for: ["combinatorial_optimization", "structured_problems"]
    complexity: "variable"
    parameters: ["operator_type", "neighborhood_size"]
    
  adaptive_perturbation:
    description: "Adapt perturbation based on temperature"
    best_for: ["adaptive_optimization", "multi_scale_problems"]
    complexity: "O(n)"
    parameters: ["temperature_scale", "adaptation_factor"]
```

## Error Handling

### Optimization Failures

```yaml
optimization_failures:
  premature_convergence:
    detection_strategy: "acceptance_rate_monitoring"
    recovery_strategy: "reheating"
    max_retries: 3
    fallback_action: "restart_with_new_initial"
  
  slow_convergence:
    detection_strategy: "improvement_rate_monitoring"
    recovery_strategy: "adaptive_cooling"
    max_retries: 2
    fallback_action: "alternative_algorithm"
  
  numerical_instability:
    detection_strategy: "value_range_checking"
    recovery_strategy: "parameter_bounds_enforcement"
    max_retries: 2
    fallback_action: "simplified_model"
  
  infinite_loop:
    detection_strategy: "iteration_count_monitoring"
    recovery_strategy: "time_based_termination"
    max_retries: 1
    fallback_action: "algorithm_termination"
```

### Hybrid Algorithm Failures

```yaml
hybrid_failures:
  population_diversity_loss:
    detection_strategy: "diversity_monitoring"
    recovery_strategy: "mutation_rate_increase"
    max_retries: 2
    fallback_action: "pure_sa_mode"
  
  convergence_imbalance:
    detection_strategy: "component_performance_monitoring"
    recovery_strategy: "component_weight_adjustment"
    max_retries: 1
    fallback_action: "single_algorithm_mode"
  
  parameter_conflict:
    detection_strategy: "parameter_consistency_checking"
    recovery_strategy: "parameter_normalization"
    max_retries: 1
    fallback_action: "default_parameters"
```

## Performance Optimization

### Algorithm Optimization

```python
# Optimization: Fast neighborhood generation
class FastNeighborhoodGenerator:
    """Optimized neighborhood generation"""
    
    def __init__(self, solution_length: int, cache_size: int = 1000):
        self.solution_length = solution_length
        self.cache = {}
        self.cache_size = cache_size
    
    def generate_neighbors_cached(self, solution: Solution, num_neighbors: int) -> List[Solution]:
        """Generate neighbors with caching"""
        cache_key = tuple(solution.state)
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        neighbors = []
        for _ in range(num_neighbors):
            neighbor = self.generate_single_neighbor(solution)
            neighbors.append(neighbor)
        
        # Cache result
        if len(self.cache) >= self.cache_size:
            # Remove oldest entry
            self.cache.pop(next(iter(self.cache)))
        
        self.cache[cache_key] = neighbors
        return neighbors
    
    def generate_single_neighbor(self, solution: Solution) -> Solution:
        """Generate single neighbor efficiently"""
        # Use pre-allocated arrays for performance
        neighbor_state = solution.state.copy()
        
        # Single dimension perturbation for speed
        index = random.randrange(len(solution.state))
        neighbor_state[index] += random.gauss(0, 0.1)
        
        return Solution(state=neighbor_state, temperature=solution.temperature)
```

### Memory Optimization

```yaml
memory_optimization:
  solution_caching:
    technique: "cost_caching"
    memory_reduction: "30-50%"
    implementation: "hash_based_caching"
    
  incremental_computation:
    technique: "delta_evaluation"
    memory_reduction: "40-60%"
    implementation: "partial_recomputation"
    
  streaming_processing:
    technique: "chunked_neighborhoods"
    memory_reduction: "unlimited_problem_size"
    implementation: "iterator_based_generation"
    
  parallel_evaluation:
    technique: "distributed_evaluation"
    memory_reduction: "memory_sharing"
    implementation: "shared_memory_objects"
```

## Integration Examples

### With Machine Learning

```python
# Integration with neural network training
class NeuralNetworkSA:
    """Simulated annealing for neural network optimization"""
    
    def __init__(self, network_architecture, training_data, validation_data):
        self.network_architecture = network_architecture
        self.training_data = training_data
        self.validation_data = validation_data
        
    def encode_network_weights(self, network) -> List[float]:
        """Encode neural network weights as solution vector"""
        weights = []
        for layer in network.layers:
            weights.extend(layer.get_weights().flatten())
        return weights
    
    def decode_network_weights(self, solution_vector, network):
        """Decode solution vector back to network weights"""
        idx = 0
        for layer in network.layers:
            weights_shape = layer.get_weights().shape
            num_weights = np.prod(weights_shape)
            layer_weights = np.array(solution_vector[idx:idx+num_weights]).reshape(weights_shape)
            layer.set_weights(layer_weights)
            idx += num_weights
    
    def evaluate_network_cost(self, solution_vector):
        """Evaluate network performance as cost"""
        # Create temporary network
        temp_network = self.create_network_from_architecture()
        
        # Set weights
        self.decode_network_weights(solution_vector, temp_network)
        
        # Train briefly and evaluate
        temp_network.fit(self.training_data['X'], self.training_data['y'], epochs=1, verbose=0)
        loss = temp_network.evaluate(self.validation_data['X'], self.validation_data['y'], verbose=0)
        
        return loss
```

### With Combinatorial Optimization

```python
# Integration with traveling salesman problem
class TSPSimulatedAnnealing:
    """Simulated annealing for TSP"""
    
    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
    
    def calculate_tour_cost(self, tour):
        """Calculate total distance of tour"""
        total_distance = 0
        for i in range(len(tour)):
            from_city = tour[i]
            to_city = tour[(i + 1) % len(tour)]
            total_distance += self.distance_matrix[from_city][to_city]
        return total_distance
    
    def generate_neighbor_tour(self, current_tour):
        """Generate neighbor tour using 2-opt or 3-opt moves"""
        tour = current_tour.copy()
        
        # 2-opt move: reverse segment
        if random.random() < 0.7:
            i, j = sorted(random.sample(range(len(tour)), 2))
            tour[i:j+1] = reversed(tour[i:j+1])
        else:
            # 3-opt move: more complex rearrangement
            i, j, k = sorted(random.sample(range(len(tour)), 3))
            # Implement 3-opt logic here
            
        return tour
    
    def solve_tsp(self, initial_tour=None, max_iterations=10000):
        """Solve TSP using simulated annealing"""
        if initial_tour is None:
            initial_tour = list(range(self.num_cities))
            random.shuffle(initial_tour)
        
        current_tour = initial_tour
        current_cost = self.calculate_tour_cost(current_tour)
        best_tour = current_tour.copy()
        best_cost = current_cost
        
        temperature = 1000.0
        
        for iteration in range(max_iterations):
            # Generate neighbor
            neighbor_tour = self.generate_neighbor_tour(current_tour)
            neighbor_cost = self.calculate_tour_cost(neighbor_tour)
            
            # Acceptance criterion
            delta_cost = neighbor_cost - current_cost
            if delta_cost <= 0 or random.random() < math.exp(-delta_cost / temperature):
                current_tour = neighbor_tour
                current_cost = neighbor_cost
                
                if current_cost < best_cost:
                    best_tour = current_tour.copy()
                    best_cost = current_cost
            
            # Cool temperature
            temperature *= 0.995
            
            if iteration % 1000 == 0:
                print(f"Iteration {iteration}: Best cost = {best_cost:.2f}")
        
        return best_tour, best_cost
```

## Best Practices

1. **Temperature Scheduling**:
   - Start with high temperature for exploration
   - Use appropriate cooling rate (0.85-0.99)
   - Monitor acceptance rate and adjust accordingly
   - Consider adaptive cooling for complex landscapes

2. **Neighborhood Generation**:
   - Design problem-specific neighborhood functions
   - Balance exploration and exploitation
   - Use adaptive perturbation sizes
   - Consider multiple neighborhood types

3. **Convergence Monitoring**:
   - Track multiple convergence indicators
   - Implement reheating for premature convergence
   - Use restart strategies for complex problems
   - Monitor solution diversity

4. **Hybrid Approaches**:
   - Combine with other algorithms for enhanced performance
   - Use SA for local refinement in GA
   - Implement parallel tempering for difficult problems
   - Balance exploration and exploitation

## Troubleshooting

### Common Issues

1. **Slow Convergence**: Increase initial temperature, adjust cooling rate, improve neighborhood generation
2. **Premature Convergence**: Implement reheating, increase mutation rate, use adaptive cooling
3. **Poor Solution Quality**: Check neighborhood generation, adjust temperature schedule, use hybrid approaches
4. **High Computational Cost**: Optimize neighborhood generation, use caching, implement early termination

### Debug Mode

```python
# Debug mode: Enhanced SA debugging
class DebugSimulatedAnnealing:
    """SA with enhanced debugging capabilities"""
    
    def __init__(self, config):
        self.config = config
        self.debug_log = []
        self.acceptance_analysis = {}
        self.convergence_analysis = {}
    
    def log_iteration(self, iteration_data):
        """Log detailed iteration information"""
        self.debug_log.append({
            'iteration': iteration_data['iteration'],
            'temperature': iteration_data['temperature'],
            'current_cost': iteration_data['current_cost'],
            'best_cost': iteration_data['best_cost'],
            'acceptance_decision': iteration_data['acceptance_decision'],
            'neighborhood_stats': iteration_data['neighborhood_stats']
        })
    
    def analyze_acceptance_patterns(self):
        """Analyze acceptance patterns"""
        acceptance_rates = []
        temperature_ranges = []
        
        for i in range(0, len(self.debug_log), 100):
            window = self.debug_log[i:i+100]
            if window:
                accepted = sum(1 for entry in window if entry['acceptance_decision'] == 'accepted')
                rate = accepted / len(window)
                temp = window[0]['temperature']
                
                acceptance_rates.append(rate)
                temperature_ranges.append(temp)
        
        self.acceptance_analysis = {
            'acceptance_rates': acceptance_rates,
            'temperature_ranges': temperature_ranges,
            'optimal_acceptance_range': self.find_optimal_acceptance_range()
        }
        
        return self.acceptance_analysis
    
    def generate_debug_report(self):
        """Generate comprehensive debug report"""
        return {
            'execution_summary': self.get_execution_summary(),
            'acceptance_analysis': self.analyze_acceptance_patterns(),
            'convergence_analysis': self.analyze_convergence(),
            'parameter_effectiveness': self.get_parameter_effectiveness(),
            'recommendations': self.get_recommendations()
        }
```

## Monitoring and Metrics

### SA Performance Metrics

```yaml
sa_performance_metrics:
  convergence_metrics:
    convergence_speed: number     # Iterations to convergence
    convergence_stability: number # Stability of convergence
    solution_quality: number      # Quality of final solution
    
  exploration_metrics:
    search_space_coverage: number # Coverage of search space
    diversity_maintenance: number # Maintenance of solution diversity
    escape_capability: number     # Ability to escape local optima
    
  efficiency_metrics:
    iterations_per_second: number # Iterations per second
    memory_efficiency: number     # Memory usage efficiency
    computational_complexity: string # Algorithmic complexity
    
  robustness_metrics:
    parameter_sensitivity: number # Sensitivity to parameter changes
    problem_adaptability: number  # Adaptability to different problems
    convergence_reliability: number # Reliability of convergence
```

## Dependencies

- **Mathematical Libraries**: NumPy, SciPy for mathematical operations
- **Optimization Libraries**: DEAP, PyGAD for advanced optimization features
- **Machine Learning**: scikit-learn, TensorFlow for ML integration
- **Visualization**: Matplotlib, Plotly for result visualization
- **Parallel Processing**: multiprocessing for parallel implementations

## Version History

- **1.0.0**: Initial release with comprehensive simulated annealing frameworks
- **1.1.0**: Added adaptive cooling schedules and reheating strategies
- **1.2.0**: Enhanced multi-objective optimization and hybrid approaches
- **1.3.0**: Improved debugging tools and performance monitoring
- **1.4.0**: Advanced integration with machine learning and combinatorial optimization

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.