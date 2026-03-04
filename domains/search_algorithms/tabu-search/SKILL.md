---
Domain: search_algorithms
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: tabu-search
---



## Description

Automatically designs and implements optimal tabu search algorithms for solving complex optimization problems, including combinatorial optimization, scheduling, routing, and discrete optimization. This skill provides comprehensive frameworks for tabu list management, aspiration criteria, neighborhood exploration, and long-term memory strategies.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Tabu List Management**: Implement dynamic tabu lists with adaptive tenure, frequency-based memory, and recency-based memory
- **Aspiration Criteria**: Design aspiration criteria for overriding tabu restrictions when promising solutions are found
- **Neighborhood Exploration**: Create problem-specific neighborhood structures with intelligent exploration strategies
- **Long-term Memory**: Implement strategic oscillation, diversification, and intensification mechanisms
- **Solution Space Analysis**: Analyze solution space characteristics for optimal tabu search configuration
- **Parallel Tabu Search**: Design parallel implementations for improved performance and solution quality
- **Hybrid Approaches**: Combine with other metaheuristics (simulated annealing, genetic algorithms) for enhanced performance

## Usage Examples

### Basic Tabu Search Framework

```python
"""
Basic Tabu Search Framework
"""

import random
import math
from typing import List, Tuple, Dict, Callable, Any, Set
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Solution:
    """Solution representation"""
    state: List[int]
    cost: float = 0.0
    is_tabu: bool = False
    
    def __hash__(self):
        return hash(tuple(self.state))
    
    def __eq__(self, other):
        return self.state == other.state

@dataclass
class Move:
    """Move representation"""
    from_state: List[int]
    to_state: List[int]
    move_type: str
    move_cost: float
    tabu_tenure: int = 0
    
    def __hash__(self):
        return hash((tuple(self.from_state), tuple(self.to_state), self.move_type))

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
        tour = solution.state
        
        for i in range(len(tour)):
            from_city = tour[i]
            to_city = tour[(i + 1) % len(tour)]
            total_distance += self.distance_matrix[from_city][to_city]
        
        return total_distance
    
    def is_minimization(self) -> bool:
        return True  # Minimize distance

class TabuList:
    """Tabu list for managing forbidden moves"""
    
    def __init__(self, tabu_tenure: int = 10):
        self.tabu_tenure = tabu_tenure
        self.tabu_moves: Dict[Move, int] = {}
        self.iteration_count = 0
    
    def add_move(self, move: Move):
        """Add move to tabu list"""
        self.tabu_moves[move] = self.iteration_count + self.tabu_tenure
    
    def is_tabu(self, move: Move) -> bool:
        """Check if move is tabu"""
        if move not in self.tabu_moves:
            return False
        
        return self.iteration_count < self.tabu_moves[move]
    
    def update(self):
        """Update tabu list"""
        self.iteration_count += 1
        
        # Remove expired moves
        expired_moves = [move for move, expiry in self.tabu_moves.items() 
                        if expiry <= self.iteration_count]
        for move in expired_moves:
            del self.tabu_moves[move]

class TabuSearch:
    """Basic Tabu Search implementation"""
    
    def __init__(self, 
                 initial_solution: Solution,
                 cost_function: CostFunction,
                 tabu_tenure: int = 10,
                 max_iterations: int = 1000,
                 neighborhood_size: int = 50):
        """
        Initialize Tabu Search
        
        Args:
            initial_solution: Starting solution
            cost_function: Cost function to optimize
            tabu_tenure: Number of iterations a move stays tabu
            max_iterations: Maximum number of iterations
            neighborhood_size: Number of neighbors to explore
        """
        self.initial_solution = initial_solution
        self.cost_function = cost_function
        self.tabu_tenure = tabu_tenure
        self.max_iterations = max_iterations
        self.neighborhood_size = neighborhood_size
        
        # Current state
        self.current_solution = initial_solution
        self.best_solution = initial_solution
        self.tabu_list = TabuList(tabu_tenure)
        
        # Statistics
        self.cost_history: List[float] = []
        self.tabu_moves_history: List[int] = []
        
        # Initialize costs
        self.current_solution.cost = self.cost_function.evaluate(self.current_solution)
        self.best_solution.cost = self.current_solution.cost
    
    def generate_neighbor(self, solution: Solution) -> Solution:
        """Generate a neighboring solution using 2-opt move"""
        neighbor_state = solution.state.copy()
        
        # 2-opt move: reverse segment
        i, j = sorted(random.sample(range(len(solution.state)), 2))
        neighbor_state[i:j+1] = reversed(neighbor_state[i:j+1])
        
        neighbor = Solution(state=neighbor_state)
        neighbor.cost = self.cost_function.evaluate(neighbor)
        
        return neighbor
    
    def generate_move(self, from_solution: Solution, to_solution: Solution) -> Move:
        """Generate move representation"""
        return Move(
            from_state=from_solution.state.copy(),
            to_state=to_solution.state.copy(),
            move_type="2-opt",
            move_cost=to_solution.cost - from_solution.cost
        )
    
    def aspiration_criteria(self, move: Move, new_solution: Solution) -> bool:
        """Check if move satisfies aspiration criteria"""
        # Aspiration: if new solution is better than best known
        if self.cost_function.is_minimization():
            return new_solution.cost < self.best_solution.cost
        else:
            return new_solution.cost > self.best_solution.cost
    
    def select_best_move(self, neighbors: List[Solution]) -> Tuple[Solution, Move]:
        """Select best non-tabu move"""
        best_neighbor = None
        best_move = None
        best_cost = float('inf') if self.cost_function.is_minimization() else float('-inf')
        
        for neighbor in neighbors:
            move = self.generate_move(self.current_solution, neighbor)
            
            # Check if move is tabu
            if self.tabu_list.is_tabu(move) and not self.aspiration_criteria(move, neighbor):
                continue
            
            # Update best move
            if self.cost_function.is_minimization():
                if neighbor.cost < best_cost:
                    best_cost = neighbor.cost
                    best_neighbor = neighbor
                    best_move = move
            else:
                if neighbor.cost > best_cost:
                    best_cost = neighbor.cost
                    best_neighbor = neighbor
                    best_move = move
        
        return best_neighbor, best_move
    
    def solve(self) -> Solution:
        """Run tabu search optimization"""
        for iteration in range(self.max_iterations):
            # Generate neighborhood
            neighbors = []
            for _ in range(self.neighborhood_size):
                neighbor = self.generate_neighbor(self.current_solution)
                neighbors.append(neighbor)
            
            # Select best move
            best_neighbor, best_move = self.select_best_move(neighbors)
            
            # If no valid move found, generate random move
            if best_neighbor is None:
                best_neighbor = self.generate_neighbor(self.current_solution)
                best_move = self.generate_move(self.current_solution, best_neighbor)
            
            # Update tabu list
            self.tabu_list.add_move(best_move)
            
            # Update current solution
            self.current_solution = best_neighbor
            
            # Update best solution
            if ((self.cost_function.is_minimization() and best_neighbor.cost < self.best_solution.cost) or
                (not self.cost_function.is_minimization() and best_neighbor.cost > self.best_solution.cost)):
                self.best_solution = best_neighbor
            
            # Update tabu list
            self.tabu_list.update()
            
            # Track statistics
            self.cost_history.append(self.current_solution.cost)
            self.tabu_moves_history.append(len(self.tabu_list.tabu_moves))
            
            # Print progress
            if iteration % 100 == 0:
                print(f"Iteration {iteration}: Best cost = {self.best_solution.cost:.6f}, "
                      f"Tabu moves = {len(self.tabu_list.tabu_moves)}")
        
        return self.best_solution

# Example usage
def example_basic_tabu():
    """Example: Basic Tabu Search for TSP"""
    
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
    
    # Create initial solution (random tour)
    initial_tour = list(range(num_cities))
    random.shuffle(initial_tour)
    initial_solution = Solution(state=initial_tour)
    
    # Create cost function
    cost_func = TravelingSalesmanCost(distance_matrix)
    
    # Create tabu search
    tabu = TabuSearch(
        initial_solution=initial_solution,
        cost_function=cost_func,
        tabu_tenure=15,
        max_iterations=2000,
        neighborhood_size=100
    )
    
    # Solve
    best_solution = tabu.solve()
    
    print(f"\nBest TSP tour found:")
    print(f"  Cost: {best_solution.cost:.2f}")
    print(f"  Tour: {best_solution.state}")
    
    return best_solution, tabu

if __name__ == "__main__":
    example_basic_tabu()
```

### Advanced Tabu Search with Adaptive Memory

```python
"""
Advanced Tabu Search with Adaptive Memory
"""

import random
import math
from typing import List, Tuple, Dict, Callable, Any, Set
from dataclasses import dataclass
from collections import defaultdict, deque

@dataclass
class AdaptiveTabuConfig:
    """Configuration for adaptive tabu search"""
    tabu_tenure: int = 10
    max_iterations: int = 5000
    neighborhood_size: int = 100
    diversification_factor: float = 0.1
    intensification_factor: float = 0.1
    frequency_memory_size: int = 100

class FrequencyMemory:
    """Frequency-based memory for diversification"""
    
    def __init__(self, memory_size: int = 100):
        self.memory_size = memory_size
        self.frequency_count: Dict[tuple, int] = defaultdict(int)
        self.recent_solutions: deque = deque(maxlen=memory_size)
    
    def add_solution(self, solution: Solution):
        """Add solution to frequency memory"""
        solution_key = tuple(solution.state)
        self.frequency_count[solution_key] += 1
        self.recent_solutions.append(solution_key)
    
    def get_diversification_penalty(self, solution: Solution) -> float:
        """Calculate diversification penalty based on frequency"""
        solution_key = tuple(solution.state)
        frequency = self.frequency_count[solution_key]
        
        # Penalty increases with frequency
        return frequency * 0.1

class RecencyMemory:
    """Recency-based memory for intensification"""
    
    def __init__(self, memory_size: int = 50):
        self.memory_size = memory_size
        self.recent_moves: deque = deque(maxlen=memory_size)
        self.move_weights: Dict[tuple, float] = defaultdict(float)
    
    def add_move(self, move: Move):
        """Add move to recency memory"""
        move_key = (tuple(move.from_state), tuple(move.to_state), move.move_type)
        self.recent_moves.append(move_key)
        
        # Increase weight for recent moves
        self.move_weights[move_key] += 1.0
    
    def get_intensification_bonus(self, move: Move) -> float:
        """Calculate intensification bonus for promising moves"""
        move_key = (tuple(move.from_state), tuple(move.to_state), move.move_type)
        
        # Bonus based on move weight
        return self.move_weights.get(move_key, 0.0) * 0.05

class StrategicOscillation:
    """Strategic oscillation for escaping local optima"""
    
    def __init__(self, oscillation_period: int = 100):
        self.oscillation_period = oscillation_period
        self.current_phase = "exploration"  # exploration or exploitation
        self.phase_counter = 0
    
    def should_oscillate(self, iteration: int) -> bool:
        """Check if oscillation should occur"""
        return iteration % self.oscillation_period == 0
    
    def get_oscillation_factor(self, iteration: int) -> float:
        """Get oscillation factor for exploration/exploitation balance"""
        if self.should_oscillate(iteration):
            self.phase_counter += 1
            self.current_phase = "exploitation" if self.current_phase == "exploration" else "exploration"
        
        # Return factor based on phase
        if self.current_phase == "exploration":
            return 1.5  # Encourage exploration
        else:
            return 0.5   # Encourage exploitation

class AdaptiveTabuSearch:
    """Advanced tabu search with adaptive memory"""
    
    def __init__(self, config: AdaptiveTabuConfig):
        self.config = config
        
        # Memory structures
        self.frequency_memory = FrequencyMemory(config.frequency_memory_size)
        self.recency_memory = RecencyMemory(config.frequency_memory_size // 2)
        self.strategic_oscillation = StrategicOscillation(100)
        
        # State
        self.tabu_list = TabuList(config.tabu_tenure)
        self.best_solution = None
        self.current_solution = None
        
        # Statistics
        self.cost_history = []
        self.diversity_history = []
        self.intensification_history = []
    
    def generate_adaptive_neighbor(self, solution: Solution, iteration: int) -> Solution:
        """Generate neighbor with adaptive diversification/intensification"""
        neighbor_state = solution.state.copy()
        
        # Apply strategic oscillation
        oscillation_factor = self.strategic_oscillation.get_oscillation_factor(iteration)
        
        # Choose move type based on oscillation
        if oscillation_factor > 1.0:  # Exploration phase
            # Use more disruptive moves
            neighbor_state = self.apply_multi_opt_move(neighbor_state, num_moves=3)
        else:  # Exploitation phase
            # Use conservative moves
            neighbor_state = self.apply_2_opt_move(neighbor_state)
        
        neighbor = Solution(state=neighbor_state)
        neighbor.cost = self.cost_function.evaluate(neighbor)
        
        # Apply diversification penalty
        diversification_penalty = self.frequency_memory.get_diversification_penalty(neighbor)
        neighbor.cost += diversification_penalty
        
        return neighbor
    
    def apply_2_opt_move(self, state: List[int]) -> List[int]:
        """Apply 2-opt move"""
        new_state = state.copy()
        i, j = sorted(random.sample(range(len(state)), 2))
        new_state[i:j+1] = reversed(new_state[i:j+1])
        return new_state
    
    def apply_multi_opt_move(self, state: List[int], num_moves: int) -> List[int]:
        """Apply multiple 2-opt moves"""
        new_state = state.copy()
        for _ in range(num_moves):
            new_state = self.apply_2_opt_move(new_state)
        return new_state
    
    def adaptive_aspiration_criteria(self, move: Move, new_solution: Solution, iteration: int) -> bool:
        """Adaptive aspiration criteria"""
        # Standard aspiration: better than best
        if self.cost_function.is_minimization():
            if new_solution.cost < self.best_solution.cost:
                return True
        else:
            if new_solution.cost > self.best_solution.cost:
                return True
        
        # Adaptive aspiration: based on oscillation phase
        oscillation_factor = self.strategic_oscillation.get_oscillation_factor(iteration)
        
        if oscillation_factor > 1.0:  # Exploration phase
            # Allow moves that are significantly better than current
            improvement_threshold = 0.05  # 5% improvement
            if self.cost_function.is_minimization():
                return new_solution.cost < self.current_solution.cost * (1 - improvement_threshold)
            else:
                return new_solution.cost > self.current_solution.cost * (1 + improvement_threshold)
        
        return False
    
    def select_adaptive_move(self, neighbors: List[Solution], iteration: int) -> Tuple[Solution, Move]:
        """Select best move with adaptive criteria"""
        best_neighbor = None
        best_move = None
        best_score = float('inf') if self.cost_function.is_minimization() else float('-inf')
        
        for neighbor in neighbors:
            move = self.generate_move(self.current_solution, neighbor)
            
            # Check tabu status with adaptive aspiration
            if self.tabu_list.is_tabu(move) and not self.adaptive_aspiration_criteria(move, neighbor, iteration):
                continue
            
            # Calculate adaptive score
            score = self.calculate_adaptive_score(neighbor, move, iteration)
            
            # Update best move
            if self.cost_function.is_minimization():
                if score < best_score:
                    best_score = score
                    best_neighbor = neighbor
                    best_move = move
            else:
                if score > best_score:
                    best_score = score
                    best_neighbor = neighbor
                    best_move = move
        
        return best_neighbor, best_move
    
    def calculate_adaptive_score(self, solution: Solution, move: Move, iteration: int) -> float:
        """Calculate adaptive score considering memory and oscillation"""
        base_score = solution.cost
        
        # Add diversification penalty
        diversification_penalty = self.frequency_memory.get_diversification_penalty(solution)
        
        # Add intensification bonus
        intensification_bonus = self.recency_memory.get_intensification_bonus(move)
        
        # Apply oscillation factor
        oscillation_factor = self.strategic_oscillation.get_oscillation_factor(iteration)
        
        # Calculate final score
        adaptive_score = base_score + (diversification_penalty * oscillation_factor) - intensification_bonus
        
        return adaptive_score
    
    def solve_adaptive(self, initial_solution: Solution, cost_function: CostFunction) -> Solution:
        """Run adaptive tabu search"""
        self.current_solution = initial_solution
        self.best_solution = initial_solution
        self.cost_function = cost_function
        
        # Initialize costs
        self.current_solution.cost = self.cost_function.evaluate(self.current_solution)
        self.best_solution.cost = self.current_solution.cost
        
        for iteration in range(self.config.max_iterations):
            # Generate adaptive neighborhood
            neighbors = []
            for _ in range(self.config.neighborhood_size):
                neighbor = self.generate_adaptive_neighbor(self.current_solution, iteration)
                neighbors.append(neighbor)
            
            # Select best move
            best_neighbor, best_move = self.select_adaptive_move(neighbors, iteration)
            
            # Update memory structures
            self.frequency_memory.add_solution(best_neighbor)
            self.recency_memory.add_move(best_move)
            
            # Update tabu list
            self.tabu_list.add_move(best_move)
            
            # Update current solution
            self.current_solution = best_neighbor
            
            # Update best solution
            if ((self.cost_function.is_minimization() and best_neighbor.cost < self.best_solution.cost) or
                (not self.cost_function.is_minimization() and best_neighbor.cost > self.best_solution.cost)):
                self.best_solution = best_neighbor
            
            # Update tabu list
            self.tabu_list.update()
            
            # Track statistics
            self.cost_history.append(self.current_solution.cost)
            self.diversity_history.append(self.frequency_memory.get_diversification_penalty(self.current_solution))
            self.intensification_history.append(self.recency_memory.get_intensification_bonus(best_move))
            
            # Print progress
            if iteration % 500 == 0:
                print(f"Iteration {iteration}: Best = {self.best_solution.cost:.6f}, "
                      f"Tabu moves = {len(self.tabu_list.tabu_moves)}")
        
        return self.best_solution

# Example usage with advanced tabu search
def example_advanced_tabu():
    """Example: Advanced Adaptive Tabu Search"""
    
    # Create TSP instance
    num_cities = 30
    distance_matrix = [[random.uniform(1, 100) for _ in range(num_cities)] for _ in range(num_cities)]
    for i in range(num_cities):
        distance_matrix[i][i] = 0.0
    
    # Create initial solution
    initial_tour = list(range(num_cities))
    random.shuffle(initial_tour)
    initial_solution = Solution(state=initial_tour)
    
    # Create cost function
    cost_func = TravelingSalesmanCost(distance_matrix)
    
    # Create adaptive tabu config
    config = AdaptiveTabuConfig(
        tabu_tenure=20,
        max_iterations=3000,
        neighborhood_size=150,
        diversification_factor=0.1,
        intensification_factor=0.1
    )
    
    # Create advanced tabu search
    advanced_tabu = AdaptiveTabuSearch(config)
    
    # Solve
    best_solution = advanced_tabu.solve_adaptive(initial_solution, cost_func)
    
    print(f"\nAdvanced Tabu Search Best Solution:")
    print(f"  Cost: {best_solution.cost:.2f}")
    print(f"  Tour length: {len(best_solution.state)} cities")
    
    return best_solution, advanced_tabu

if __name__ == "__main__":
    example_advanced_tabu()
```

### Parallel Tabu Search

```python
"""
Parallel Tabu Search Implementation
"""

import random
import math
from typing import List, Tuple, Dict, Callable, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp

@dataclass
class ParallelTabuConfig:
    """Configuration for parallel tabu search"""
    num_threads: int = 4
    tabu_tenure: int = 10
    max_iterations: int = 2000
    neighborhood_size: int = 50
    migration_rate: float = 0.1
    migration_interval: int = 100

class ThreadedTabuSearch:
    """Threaded tabu search for parallel execution"""
    
    def __init__(self, config: ParallelTabuConfig, cost_function: CostFunction):
        self.config = config
        self.cost_function = cost_function
        
        # Thread-specific state
        self.local_best = None
        self.current_solution = None
        self.tabu_list = None
        
        # Statistics
        self.thread_id = None
    
    def initialize_thread(self, initial_solution: Solution, thread_id: int):
        """Initialize thread with solution"""
        self.thread_id = thread_id
        self.current_solution = Solution(state=initial_solution.state.copy())
        self.local_best = Solution(state=initial_solution.state.copy())
        self.tabu_list = TabuList(self.config.tabu_tenure)
        
        # Initialize costs
        self.current_solution.cost = self.cost_function.evaluate(self.current_solution)
        self.local_best.cost = self.current_solution.cost
    
    def thread_search(self, iterations: int) -> Solution:
        """Run tabu search in thread"""
        for iteration in range(iterations):
            # Generate neighborhood
            neighbors = []
            for _ in range(self.config.neighborhood_size):
                neighbor = self.generate_neighbor(self.current_solution)
                neighbors.append(neighbor)
            
            # Select best move
            best_neighbor, best_move = self.select_best_move(neighbors)
            
            # Update tabu list
            self.tabu_list.add_move(best_move)
            
            # Update current solution
            self.current_solution = best_neighbor
            
            # Update local best
            if ((self.cost_function.is_minimization() and best_neighbor.cost < self.local_best.cost) or
                (not self.cost_function.is_minimization() and best_neighbor.cost > self.local_best.cost)):
                self.local_best = best_neighbor
            
            # Update tabu list
            self.tabu_list.update()
        
        return self.local_best
    
    def generate_neighbor(self, solution: Solution) -> Solution:
        """Generate neighbor (2-opt move)"""
        neighbor_state = solution.state.copy()
        i, j = sorted(random.sample(range(len(solution.state)), 2))
        neighbor_state[i:j+1] = reversed(neighbor_state[i:j+1])
        
        neighbor = Solution(state=neighbor_state)
        neighbor.cost = self.cost_function.evaluate(neighbor)
        
        return neighbor
    
    def select_best_move(self, neighbors: List[Solution]) -> Tuple[Solution, Move]:
        """Select best non-tabu move"""
        best_neighbor = None
        best_move = None
        best_cost = float('inf') if self.cost_function.is_minimization() else float('-inf')
        
        for neighbor in neighbors:
            move = Move(
                from_state=self.current_solution.state.copy(),
                to_state=neighbor.state.copy(),
                move_type="2-opt",
                move_cost=neighbor.cost - self.current_solution.cost
            )
            
            # Check tabu status
            if self.tabu_list.is_tabu(move):
                continue
            
            # Update best move
            if self.cost_function.is_minimization():
                if neighbor.cost < best_cost:
                    best_cost = neighbor.cost
                    best_neighbor = neighbor
                    best_move = move
            else:
                if neighbor.cost > best_cost:
                    best_cost = neighbor.cost
                    best_neighbor = neighbor
                    best_move = move
        
        return best_neighbor, best_move

class ParallelTabuSearch:
    """Parallel tabu search with migration"""
    
    def __init__(self, config: ParallelTabuConfig):
        self.config = config
        self.threads = []
        self.global_best = None
        
        # Migration tracking
        self.migration_counter = 0
    
    def initialize_threads(self, initial_solution: Solution, cost_function: CostFunction):
        """Initialize all threads"""
        self.threads = []
        
        for i in range(self.config.num_threads):
            # Create perturbed initial solution for each thread
            perturbed_solution = self.perturb_solution(initial_solution, i)
            
            thread_search = ThreadedTabuSearch(self.config, cost_function)
            thread_search.initialize_thread(perturbed_solution, i)
            self.threads.append(thread_search)
    
    def perturb_solution(self, solution: Solution, thread_id: int) -> Solution:
        """Create perturbed solution for thread diversity"""
        perturbed_state = solution.state.copy()
        
        # Apply random perturbations based on thread ID
        num_perturbations = 2 + (thread_id % 4)
        
        for _ in range(num_perturbations):
            i, j = sorted(random.sample(range(len(perturbed_state)), 2))
            perturbed_state[i:j+1] = reversed(perturbed_state[i:j+1])
        
        return Solution(state=perturbed_state)
    
    def migrate_solutions(self):
        """Perform migration between threads"""
        # Select best solutions from each thread
        thread_solutions = [thread.local_best for thread in self.threads]
        
        # Sort by quality
        if self.config.cost_function.is_minimization():
            sorted_solutions = sorted(thread_solutions, key=lambda x: x.cost)
        else:
            sorted_solutions = sorted(thread_solutions, key=lambda x: x.cost, reverse=True)
        
        # Migrate best solutions to other threads
        num_migrants = max(1, int(self.config.num_threads * self.config.migration_rate))
        
        for i in range(num_migrants):
            migrant = sorted_solutions[i]
            
            # Distribute to other threads
            for j, thread in enumerate(self.threads):
                if j != i % self.config.num_threads:
                    # Replace thread's current solution with migrant
                    thread.current_solution = Solution(state=migrant.state.copy())
                    thread.current_solution.cost = self.config.cost_function.evaluate(thread.current_solution)
    
    def solve_parallel(self, initial_solution: Solution, cost_function: CostFunction) -> Solution:
        """Run parallel tabu search"""
        self.initialize_threads(initial_solution, cost_function)
        self.config.cost_function = cost_function  # Store for migration
        
        iterations_per_thread = self.config.max_iterations // self.config.num_threads
        
        for iteration in range(self.config.max_iterations):
            # Run threads in parallel
            with ThreadPoolExecutor(max_workers=self.config.num_threads) as executor:
                futures = [executor.submit(thread.thread_search, iterations_per_thread) 
                          for thread in self.threads]
                
                results = [future.result() for future in futures]
            
            # Update global best
            for result in results:
                if self.global_best is None or (
                    cost_function.is_minimization() and result.cost < self.global_best.cost) or (
                    not cost_function.is_minimization() and result.cost > self.global_best.cost):
                    self.global_best = result
            
            # Migration
            if iteration % self.config.migration_interval == 0 and iteration > 0:
                self.migrate_solutions()
                self.migration_counter += 1
            
            # Print progress
            if iteration % 200 == 0:
                print(f"Iteration {iteration}: Global best = {self.global_best.cost:.6f}, "
                      f"Migrations = {self.migration_counter}")
        
        return self.global_best

# Example usage with parallel tabu search
def example_parallel_tabu():
    """Example: Parallel Tabu Search"""
    
    # Create TSP instance
    num_cities = 40
    distance_matrix = [[random.uniform(1, 100) for _ in range(num_cities)] for _ in range(num_cities)]
    for i in range(num_cities):
        distance_matrix[i][i] = 0.0
    
    # Create initial solution
    initial_tour = list(range(num_cities))
    random.shuffle(initial_tour)
    initial_solution = Solution(state=initial_tour)
    
    # Create cost function
    cost_func = TravelingSalesmanCost(distance_matrix)
    
    # Create parallel tabu config
    config = ParallelTabuConfig(
        num_threads=4,
        tabu_tenure=15,
        max_iterations=2000,
        neighborhood_size=80,
        migration_rate=0.2,
        migration_interval=50
    )
    
    # Create parallel tabu search
    parallel_tabu = ParallelTabuSearch(config)
    
    # Solve
    best_solution = parallel_tabu.solve_parallel(initial_solution, cost_func)
    
    print(f"\nParallel Tabu Search Best Solution:")
    print(f"  Cost: {best_solution.cost:.2f}")
    print(f"  Migrations: {parallel_tabu.migration_counter}")
    
    return best_solution, parallel_tabu

if __name__ == "__main__":
    example_parallel_tabu()
```

## Input Format

### Tabu Search Configuration

```yaml
tabu_search_config:
  problem_definition:
    solution_type: "permutation|binary|continuous"
    solution_length: number       # Length of solution vector
    optimization_type: "minimize|maximize"
    
  algorithm_parameters:
    tabu_tenure: number           # Number of iterations moves stay tabu
    max_iterations: number        # Maximum number of iterations
    neighborhood_size: number     # Number of neighbors to explore per iteration
    aspiration_criteria: "best_solution|improvement_threshold|adaptive"
    
  memory_management:
    frequency_memory: boolean     # Use frequency-based memory
    recency_memory: boolean       # Use recency-based memory
    strategic_oscillation: boolean # Use strategic oscillation
    memory_size: number           # Size of memory structures
    
  diversification_strategies:
    diversification_factor: number # Factor for diversification penalty
    perturbation_strength: number # Strength of solution perturbations
    restart_threshold: number     # Threshold for restart strategies
    
  parallel_parameters:
    num_threads: number           # Number of parallel threads
    migration_rate: number        # Rate of solution migration
    migration_interval: number    # Iterations between migrations
    
  termination_criteria:
    max_iterations: number        # Maximum iterations
    time_limit: number            # Maximum execution time in seconds
    stagnation_limit: number      # Iterations without improvement
    solution_quality: number      # Target solution quality
```

### Advanced Memory Configuration

```yaml
memory_configuration:
  frequency_memory:
    enabled: boolean              # Enable frequency memory
    memory_size: number           # Size of frequency memory
    penalty_factor: number        # Factor for frequency penalty
    decay_rate: number            # Rate of frequency decay
    
  recency_memory:
    enabled: boolean              # Enable recency memory
    memory_size: number           # Size of recency memory
    bonus_factor: number          # Factor for recency bonus
    decay_rate: number            # Rate of recency decay
    
  strategic_oscillation:
    enabled: boolean              # Enable strategic oscillation
    oscillation_period: number    # Period of oscillation
    exploration_factor: number    # Factor for exploration phase
    exploitation_factor: number   # Factor for exploitation phase
    
  adaptive_parameters:
    adaptive_tenure: boolean      # Adapt tabu tenure dynamically
    adaptive_aspiration: boolean  # Adapt aspiration criteria
    adaptive_diversification: boolean # Adapt diversification strategies
```

## Output Format

### Optimization Results

```yaml
optimization_results:
  best_solution:
    state: array                 # Best solution found
    cost: number                 # Final cost value
    iteration_found: number      # Iteration when best was found
    thread_id: number            # Thread that found best solution (parallel)
    
  convergence_analysis:
    convergence_iteration: number # Iteration when converged
    convergence_stability: number # Stability of convergence
    stagnation_detected: boolean # Whether stagnation occurred
    restart_count: number        # Number of restarts performed
    migration_count: number      # Number of migrations (parallel)
    
  memory_analysis:
    frequency_diversity: number   # Diversity from frequency memory
    recency_effectiveness: number # Effectiveness of recency memory
    oscillation_balance: number   # Balance between exploration/exploitation
    
  algorithm_statistics:
    total_iterations: number     # Total iterations performed
    tabu_moves_generated: number # Total tabu moves generated
    aspiration_activations: number # Number of aspiration criteria activations
    diversification_triggers: number # Number of diversification triggers
    
  performance_metrics:
    execution_time: number       # Total execution time
    iterations_per_second: number # Iterations per second
    memory_usage: string         # Peak memory usage
    parallel_efficiency: number  # Efficiency of parallel processing
```

### Tabu Search History

```yaml
tabu_search_history:
  iteration_data: array          # Data for each iteration
  - iteration: number
    current_cost: number
    best_cost: number
    tabu_list_size: number
    aspiration_used: boolean
    diversification_applied: boolean
    
  memory_data: array             # Memory structure data
  - iteration: number
    frequency_diversity: number
    recency_bonus: number
    oscillation_phase: string
    
  migration_data: array          # Migration data (parallel)
  - iteration: number
    migrants_sent: number
    migrants_received: number
    best_migrant_cost: number
```

## Configuration Options

### Neighborhood Structures

```yaml
neighborhood_structures:
  2_opt_moves:
    description: "Reverse segment of solution"
    best_for: ["tsp", "routing", "scheduling"]
    complexity: "O(n)"
    parameters: ["segment_length"]
    
  swap_moves:
    description: "Swap two elements in solution"
    best_for: ["assignment", "permutation_problems"]
    complexity: "O(1)"
    parameters: ["swap_distance"]
    
  insertion_moves:
    description: "Move element to different position"
    best_for: ["scheduling", "routing"]
    complexity: "O(n)"
    parameters: ["insertion_range"]
    
  bit_flip_moves:
    description: "Flip bits in binary solution"
    best_for: ["binary_optimization", "subset_selection"]
    complexity: "O(1)"
    parameters: ["flip_count"]
```

### Aspiration Criteria

```yaml
aspiration_criteria:
  best_solution:
    description: "Accept if better than global best"
    best_for: ["all_problems", "standard_approach"]
    complexity: "O(1)"
    parameters: []
    
  improvement_threshold:
    description: "Accept if significant improvement"
    best_for: ["stagnation_avoidance", "local_optima_escape"]
    complexity: "O(1)"
    parameters: ["threshold_percentage"]
    
  frequency_based:
    description: "Accept if move is infrequent"
    best_for: ["diversification", "exploration"]
    complexity: "O(1)"
    parameters: ["frequency_threshold"]
    
  adaptive:
    description: "Adapt criteria based on search progress"
    best_for: ["dynamic_problems", "adaptive_optimization"]
    complexity: "O(1)"
    parameters: ["adaptation_rate"]
```

## Error Handling

### Search Failures

```yaml
search_failures:
  premature_convergence:
    detection_strategy: "diversity_monitoring"
    recovery_strategy: "intensified_diversification"
    max_retries: 3
    fallback_action: "restart_with_perturbation"
  
  stagnation:
    detection_strategy: "improvement_monitoring"
    recovery_strategy: "strategic_oscillation"
    max_retries: 2
    fallback_action: "alternative_algorithm"
  
  memory_overflow:
    detection_strategy: "memory_usage_monitoring"
    recovery_strategy: "memory_cleanup"
    max_retries: 1
    fallback_action: "simplified_memory"
  
  parallel_sync_failure:
    detection_strategy: "heartbeat_monitoring"
    recovery_strategy: "thread_reinitialization"
    max_retries: 2
    fallback_action: "sequential_mode"
```

### Configuration Errors

```yaml
configuration_errors:
  invalid_tabu_tenure:
    detection_strategy: "parameter_validation"
    recovery_strategy: "parameter_adjustment"
    max_retries: 1
    fallback_action: "default_parameters"
  
  insufficient_memory:
    detection_strategy: "resource_monitoring"
    recovery_strategy: "memory_optimization"
    max_retries: 1
    fallback_action: "reduced_memory_mode"
  
  neighborhood_too_small:
    detection_strategy: "neighborhood_analysis"
    recovery_strategy: "neighborhood_expansion"
    max_retries: 1
    fallback_action: "adaptive_neighborhood"
```

## Performance Optimization

### Algorithm Optimization

```python
# Optimization: Fast tabu list implementation
class FastTabuList:
    """Optimized tabu list with hash-based lookup"""
    
    def __init__(self, tabu_tenure: int = 10):
        self.tabu_tenure = tabu_tenure
        self.tabu_set: Set[tuple] = set()
        self.expiry_queue: List[Tuple[tuple, int]] = []
        self.current_time = 0
    
    def add_move(self, move: Move):
        """Add move to tabu list with O(1) lookup"""
        move_key = self._get_move_key(move)
        self.tabu_set.add(move_key)
        self.expiry_queue.append((move_key, self.current_time + self.tabu_tenure))
    
    def is_tabu(self, move: Move) -> bool:
        """Check if move is tabu with O(1) lookup"""
        move_key = self._get_move_key(move)
        return move_key in self.tabu_set
    
    def update(self):
        """Update tabu list with O(1) amortized complexity"""
        self.current_time += 1
        
        # Remove expired moves
        while self.expiry_queue and self.expiry_queue[0][1] <= self.current_time:
            expired_key, _ = self.expiry_queue.pop(0)
            self.tabu_set.discard(expired_key)
    
    def _get_move_key(self, move: Move) -> tuple:
        """Get hashable key for move"""
        return (tuple(move.from_state), tuple(move.to_state), move.move_type)
```

### Memory Optimization

```yaml
memory_optimization:
  tabu_list_compression:
    technique: "move_hashing"
    memory_reduction: "60-80%"
    implementation: "hash_based_storage"
    
  solution_caching:
    technique: "cost_caching"
    memory_reduction: "30-50%"
    implementation: "hash_based_caching"
    
  parallel_memory_sharing:
    technique: "shared_memory_objects"
    memory_reduction: "40-60%"
    implementation: "memory_mapped_files"
    
  streaming_processing:
    technique: "chunked_neighborhoods"
    memory_reduction: "unlimited_problem_size"
    implementation: "iterator_based_generation"
```

## Integration Examples

### With Scheduling Problems

```python
# Integration with job shop scheduling
class JobShopTabuSearch:
    """Tabu search for job shop scheduling"""
    
    def __init__(self, jobs: List[List[int]], machines: List[int]):
        self.jobs = jobs  # jobs[i][j] = processing time of job i on machine j
        self.machines = machines
        self.num_jobs = len(jobs)
        self.num_machines = len(machines)
    
    def evaluate_schedule(self, schedule: Solution) -> float:
        """Evaluate makespan of schedule"""
        # Calculate completion times
        completion_times = [[0] * self.num_machines for _ in range(self.num_jobs)]
        
        for job_idx in schedule.state:
            for machine_idx in range(self.num_machines):
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
    
    def generate_neighbor_schedule(self, schedule: Solution) -> Solution:
        """Generate neighbor by swapping adjacent jobs"""
        neighbor_state = schedule.state.copy()
        
        # Find adjacent jobs that can be swapped
        swap_positions = []
        for i in range(len(neighbor_state) - 1):
            job1, job2 = neighbor_state[i], neighbor_state[i+1]
            
            # Check if swap is valid (no machine conflicts)
            if self._is_valid_swap(job1, job2):
                swap_positions.append(i)
        
        if swap_positions:
            pos = random.choice(swap_positions)
            neighbor_state[pos], neighbor_state[pos+1] = neighbor_state[pos+1], neighbor_state[pos]
        
        neighbor = Solution(state=neighbor_state)
        neighbor.cost = self.evaluate_schedule(neighbor)
        
        return neighbor
```

### With Vehicle Routing

```python
# Integration with vehicle routing problem
class VRPTabuSearch:
    """Tabu search for vehicle routing problem"""
    
    def __init__(self, customers: List[Tuple[float, float]], 
                 demands: List[int], capacity: int, depot: Tuple[float, float]):
        self.customers = customers
        self.demands = demands
        self.capacity = capacity
        self.depot = depot
        self.num_customers = len(customers)
    
    def calculate_route_cost(self, route: List[int]) -> float:
        """Calculate total distance for route"""
        total_distance = 0.0
        
        # Add depot to beginning and end
        route_with_depot = [0] + route + [0]
        
        for i in range(len(route_with_depot) - 1):
            from_pos = self.depot if route_with_depot[i] == 0 else self.customers[route_with_depot[i]-1]
            to_pos = self.depot if route_with_depot[i+1] == 0 else self.customers[route_with_depot[i+1]-1]
            
            distance = math.sqrt((to_pos[0] - from_pos[0])**2 + (to_pos[1] - from_pos[1])**2)
            total_distance += distance
        
        return total_distance
    
    def generate_vrp_neighbor(self, solution: Solution) -> Solution:
        """Generate neighbor by moving customer between routes"""
        # This is a simplified version - full VRP requires route structure
        neighbor_state = solution.state.copy()
        
        # Randomly move customer to different position
        if len(neighbor_state) > 1:
            from_pos = random.randint(0, len(neighbor_state) - 1)
            to_pos = random.randint(0, len(neighbor_state) - 1)
            
            customer = neighbor_state.pop(from_pos)
            neighbor_state.insert(to_pos, customer)
        
        neighbor = Solution(state=neighbor_state)
        neighbor.cost = self.evaluate_vrp_solution(neighbor)
        
        return neighbor
```

## Best Practices

1. **Tabu Tenure Selection**:
   - Start with problem size-based tenure (n/3 to n/2 for n elements)
   - Use adaptive tenure for dynamic problems
   - Monitor tabu list effectiveness and adjust accordingly

2. **Neighborhood Design**:
   - Design problem-specific neighborhood structures
   - Balance neighborhood size with exploration quality
   - Use multiple neighborhood types for better coverage

3. **Memory Management**:
   - Implement both frequency and recency memory
   - Use strategic oscillation for exploration/exploitation balance
   - Monitor memory effectiveness and adjust parameters

4. **Parallel Implementation**:
   - Use migration for information exchange between threads
   - Balance migration frequency with computational overhead
   - Implement load balancing for optimal performance

## Troubleshooting

### Common Issues

1. **Poor Solution Quality**: Increase neighborhood size, adjust tabu tenure, improve aspiration criteria
2. **Slow Convergence**: Use intensification strategies, adjust diversification parameters, implement restart strategies
3. **Memory Issues**: Implement memory cleanup, use compressed representations, limit memory size
4. **Parallel Performance**: Optimize migration strategies, balance thread workload, reduce synchronization overhead

### Debug Mode

```python
# Debug mode: Enhanced tabu search debugging
class DebugTabuSearch:
    """Tabu search with enhanced debugging capabilities"""
    
    def __init__(self, config):
        self.config = config
        self.debug_log = []
        self.tabu_analysis = {}
        self.memory_analysis = {}
    
    def log_iteration(self, iteration_data):
        """Log detailed iteration information"""
        self.debug_log.append({
            'iteration': iteration_data['iteration'],
            'current_cost': iteration_data['current_cost'],
            'best_cost': iteration_data['best_cost'],
            'tabu_list_size': iteration_data['tabu_list_size'],
            'moves_considered': iteration_data['moves_considered'],
            'moves_accepted': iteration_data['moves_accepted'],
            'aspiration_used': iteration_data['aspiration_used']
        })
    
    def analyze_tabu_effectiveness(self):
        """Analyze tabu list effectiveness"""
        tabu_blocks = 0
        aspiration_activations = 0
        
        for entry in self.debug_log:
            if entry['aspiration_used']:
                aspiration_activations += 1
            # Count potential improvements blocked by tabu
            if entry['moves_considered'] > entry['moves_accepted']:
                tabu_blocks += entry['moves_considered'] - entry['moves_accepted']
        
        self.tabu_analysis = {
            'total_blocks': tabu_blocks,
            'aspiration_activations': aspiration_activations,
            'tabu_effectiveness': tabu_blocks / max(1, len(self.debug_log)),
            'aspiration_rate': aspiration_activations / max(1, len(self.debug_log))
        }
        
        return self.tabu_analysis
    
    def generate_debug_report(self):
        """Generate comprehensive debug report"""
        return {
            'execution_summary': self.get_execution_summary(),
            'tabu_analysis': self.analyze_tabu_effectiveness(),
            'memory_analysis': self.analyze_memory_effectiveness(),
            'neighborhood_analysis': self.get_neighborhood_analysis(),
            'recommendations': self.get_recommendations()
        }
```

## Monitoring and Metrics

### Tabu Search Performance Metrics

```yaml
tabu_search_metrics:
  convergence_metrics:
    convergence_speed: number     # Iterations to convergence
    convergence_stability: number # Stability of convergence
    solution_quality: number      # Quality of final solution
    
  exploration_metrics:
    search_space_coverage: number # Coverage of search space
    diversity_maintenance: number # Maintenance of solution diversity
    local_optima_escape: number   # Ability to escape local optima
    
  memory_metrics:
    tabu_effectiveness: number    # Effectiveness of tabu restrictions
    memory_utilization: number    # Utilization of memory structures
    aspiration_frequency: number  # Frequency of aspiration criteria usage
    
  efficiency_metrics:
    iterations_per_second: number # Iterations per second
    memory_efficiency: number     # Memory usage efficiency
    parallel_efficiency: number   # Efficiency of parallel processing
```

## Dependencies

- **Mathematical Libraries**: NumPy, SciPy for mathematical operations
- **Optimization Libraries**: DEAP, PyGAD for advanced optimization features
- **Parallel Processing**: multiprocessing, concurrent.futures for parallel execution
- **Visualization**: Matplotlib, Plotly for result visualization
- **Graph Libraries**: NetworkX for graph-based problems

## Version History

- **1.0.0**: Initial release with comprehensive tabu search frameworks
- **1.1.0**: Added adaptive memory management and strategic oscillation
- **1.2.0**: Enhanced parallel tabu search and hybrid approaches
- **1.3.0**: Improved debugging tools and performance monitoring
- **1.4.0**: Advanced integration with scheduling and routing problems

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.