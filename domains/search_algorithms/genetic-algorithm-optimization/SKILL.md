---
Domain: search_algorithms
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: genetic-algorithm-optimization
---



## Description

Automatically designs and implements optimal genetic algorithms for solving complex optimization problems, including parameter tuning, feature selection, scheduling, and combinatorial optimization. This skill provides comprehensive frameworks for population management, selection strategies, crossover operations, mutation techniques, and convergence analysis.


## Purpose

*[Content for Purpose section to be added based on the specific skill requirements]*

## Examples

*[Content for Examples section to be added based on the specific skill requirements]*

## Implementation Notes

*[Content for Implementation Notes section to be added based on the specific skill requirements]*
## Capabilities

- **Population Management**: Implement efficient population structures with elitism, diversity maintenance, and adaptive sizing
- **Selection Strategies**: Design tournament selection, roulette wheel selection, rank-based selection, and adaptive selection methods
- **Crossover Operations**: Implement single-point, multi-point, uniform, and problem-specific crossover techniques
- **Mutation Techniques**: Create adaptive mutation rates, problem-specific mutation operators, and diversity preservation
- **Fitness Functions**: Design multi-objective fitness functions, constraint handling, and fitness scaling techniques
- **Convergence Analysis**: Monitor convergence, detect premature convergence, and implement restart strategies
- **Parallel Processing**: Optimize genetic algorithms for parallel execution and distributed computing environments

## Usage Examples

### Basic Genetic Algorithm Framework

```python
"""
Basic Genetic Algorithm Framework
"""

import random
import numpy as np
from typing import List, Tuple, Dict, Callable, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Individual:
    """Individual in the population"""
    chromosome: List[float]
    fitness: float = 0.0
    generation: int = 0
    
    def __lt__(self, other):
        return self.fitness < other.fitness
    
    def __hash__(self):
        return hash(tuple(self.chromosome))
    
    def __eq__(self, other):
        return self.chromosome == other.chromosome

class FitnessFunction(ABC):
    """Abstract base class for fitness functions"""
    
    @abstractmethod
    def evaluate(self, individual: Individual) -> float:
        """Evaluate fitness of an individual"""
        pass
    
    @abstractmethod
    def is_maximization(self) -> bool:
        """Return True if higher fitness is better"""
        pass

class RastriginFitness(FitnessFunction):
    """Rastrigin function for optimization testing"""
    
    def __init__(self, A: float = 10.0):
        self.A = A
    
    def evaluate(self, individual: Individual) -> float:
        """Evaluate Rastrigin function"""
        n = len(individual.chromosome)
        sum_term = sum(x**2 - self.A * np.cos(2 * np.pi * x) for x in individual.chromosome)
        return self.A * n + sum_term
    
    def is_maximization(self) -> bool:
        return False  # Minimization problem

class GeneticAlgorithm:
    """Basic Genetic Algorithm implementation"""
    
    def __init__(self, 
                 population_size: int,
                 chromosome_length: int,
                 fitness_function: FitnessFunction,
                 crossover_rate: float = 0.8,
                 mutation_rate: float = 0.01,
                 elitism_rate: float = 0.1,
                 bounds: Tuple[float, float] = (-5.12, 5.12)):
        """
        Initialize Genetic Algorithm
        
        Args:
            population_size: Number of individuals in population
            chromosome_length: Length of each chromosome
            fitness_function: Fitness function to optimize
            crossover_rate: Probability of crossover
            mutation_rate: Probability of mutation
            elitism_rate: Proportion of elite individuals to preserve
            bounds: Bounds for chromosome values
        """
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.fitness_function = fitness_function
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_rate = elitism_rate
        self.bounds = bounds
        
        # Population tracking
        self.population: List[Individual] = []
        self.generation = 0
        self.best_individual: Individual = None
        
        # Statistics
        self.fitness_history: List[float] = []
        self.diversity_history: List[float] = []
    
    def initialize_population(self):
        """Initialize population with random individuals"""
        self.population = []
        for _ in range(self.population_size):
            chromosome = [random.uniform(self.bounds[0], self.bounds[1]) 
                         for _ in range(self.chromosome_length)]
            individual = Individual(chromosome=chromosome, generation=0)
            self.population.append(individual)
        
        self.evaluate_population()
        self.update_best_individual()
    
    def evaluate_population(self):
        """Evaluate fitness of all individuals"""
        for individual in self.population:
            individual.fitness = self.fitness_function.evaluate(individual)
    
    def update_best_individual(self):
        """Update the best individual found so far"""
        if self.fitness_function.is_maximization():
            current_best = max(self.population, key=lambda x: x.fitness)
        else:
            current_best = min(self.population, key=lambda x: x.fitness)
        
        if (self.best_individual is None or 
            (self.fitness_function.is_maximization() and current_best.fitness > self.best_individual.fitness) or
            (not self.fitness_function.is_maximization() and current_best.fitness < self.best_individual.fitness)):
            self.best_individual = current_best
    
    def selection_tournament(self, k: int = 3) -> Individual:
        """Tournament selection"""
        tournament = random.sample(self.population, k)
        if self.fitness_function.is_maximization():
            return max(tournament, key=lambda x: x.fitness)
        else:
            return min(tournament, key=lambda x: x.fitness)
    
    def selection_roulette(self) -> Individual:
        """Roulette wheel selection"""
        # Handle minimization by inverting fitness
        if self.fitness_function.is_maximization():
            fitnesses = [ind.fitness for ind in self.population]
        else:
            # For minimization, use inverse fitness
            min_fitness = min(ind.fitness for ind in self.population)
            fitnesses = [1.0 / (ind.fitness - min_fitness + 1e-10) for ind in self.population]
        
        total_fitness = sum(fitnesses)
        if total_fitness == 0:
            return random.choice(self.population)
        
        pick = random.uniform(0, total_fitness)
        current = 0
        for individual, fitness in zip(self.population, fitnesses):
            current += fitness
            if current >= pick:
                return individual
        return self.population[-1]
    
    def crossover_single_point(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Single-point crossover"""
        if random.random() > self.crossover_rate:
            return parent1, parent2
        
        crossover_point = random.randint(1, self.chromosome_length - 1)
        
        child1_chromosome = (parent1.chromosome[:crossover_point] + 
                           parent2.chromosome[crossover_point:])
        child2_chromosome = (parent2.chromosome[:crossover_point] + 
                           parent1.chromosome[crossover_point:])
        
        child1 = Individual(chromosome=child1_chromosome, generation=self.generation + 1)
        child2 = Individual(chromosome=child2_chromosome, generation=self.generation + 1)
        
        return child1, child2
    
    def crossover_uniform(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Uniform crossover"""
        if random.random() > self.crossover_rate:
            return parent1, parent2
        
        child1_chromosome = []
        child2_chromosome = []
        
        for i in range(self.chromosome_length):
            if random.random() < 0.5:
                child1_chromosome.append(parent1.chromosome[i])
                child2_chromosome.append(parent2.chromosome[i])
            else:
                child1_chromosome.append(parent2.chromosome[i])
                child2_chromosome.append(parent1.chromosome[i])
        
        child1 = Individual(chromosome=child1_chromosome, generation=self.generation + 1)
        child2 = Individual(chromosome=child2_chromosome, generation=self.generation + 1)
        
        return child1, child2
    
    def mutate(self, individual: Individual) -> Individual:
        """Mutate an individual"""
        mutated_chromosome = individual.chromosome.copy()
        
        for i in range(self.chromosome_length):
            if random.random() < self.mutation_rate:
                # Gaussian mutation
                mutation_value = random.gauss(0, 0.1)
                mutated_chromosome[i] += mutation_value
                
                # Ensure bounds
                mutated_chromosome[i] = max(self.bounds[0], 
                                          min(self.bounds[1], mutated_chromosome[i]))
        
        return Individual(chromosome=mutated_chromosome, generation=individual.generation)
    
    def get_elite(self) -> List[Individual]:
        """Get elite individuals"""
        elite_size = int(self.population_size * self.elitism_rate)
        if self.fitness_function.is_maximization():
            elite = sorted(self.population, key=lambda x: x.fitness, reverse=True)[:elite_size]
        else:
            elite = sorted(self.population, key=lambda x: x.fitness)[:elite_size]
        return elite
    
    def calculate_diversity(self) -> float:
        """Calculate population diversity"""
        if len(self.population) < 2:
            return 0.0
        
        # Calculate average pairwise distance
        total_distance = 0.0
        count = 0
        
        for i in range(len(self.population)):
            for j in range(i + 1, len(self.population)):
                distance = np.linalg.norm(np.array(self.population[i].chromosome) - 
                                        np.array(self.population[j].chromosome))
                total_distance += distance
                count += 1
        
        return total_distance / count if count > 0 else 0.0
    
    def evolve(self, max_generations: int = 100) -> Individual:
        """Evolve the population"""
        self.initialize_population()
        
        for generation in range(max_generations):
            self.generation = generation
            
            # Get elite individuals
            elite = self.get_elite()
            
            # Create new population
            new_population = elite.copy()
            
            # Generate offspring
            while len(new_population) < self.population_size:
                # Selection
                parent1 = self.selection_tournament()
                parent2 = self.selection_tournament()
                
                # Crossover
                child1, child2 = self.crossover_single_point(parent1, parent2)
                
                # Mutation
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                
                # Add to new population
                new_population.extend([child1, child2])
            
            # Replace population
            self.population = new_population[:self.population_size]
            
            # Evaluate new population
            self.evaluate_population()
            self.update_best_individual()
            
            # Track statistics
            avg_fitness = np.mean([ind.fitness for ind in self.population])
            diversity = self.calculate_diversity()
            
            self.fitness_history.append(avg_fitness)
            self.diversity_history.append(diversity)
            
            # Print progress
            if generation % 10 == 0:
                print(f"Generation {generation}: Best fitness = {self.best_individual.fitness:.6f}, "
                      f"Avg fitness = {avg_fitness:.6f}, Diversity = {diversity:.6f}")
        
        return self.best_individual

# Example usage
def example_basic_ga():
    """Example: Basic Genetic Algorithm optimization"""
    
    # Create fitness function
    fitness_func = RastriginFitness()
    
    # Create GA
    ga = GeneticAlgorithm(
        population_size=50,
        chromosome_length=10,
        fitness_function=fitness_func,
        crossover_rate=0.8,
        mutation_rate=0.01,
        elitism_rate=0.1
    )
    
    # Evolve
    best_solution = ga.evolve(max_generations=200)
    
    print(f"\nBest solution found:")
    print(f"  Fitness: {best_solution.fitness:.6f}")
    print(f"  Chromosome: {best_solution.chromosome}")
    
    return best_solution, ga

if __name__ == "__main__":
    example_basic_ga()
```

### Advanced Genetic Algorithm with Adaptive Parameters

```python
"""
Advanced Genetic Algorithm with Adaptive Parameters
"""

import random
import numpy as np
from typing import List, Tuple, Dict, Callable, Any
from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class AdaptiveGAConfig:
    """Configuration for adaptive genetic algorithm"""
    initial_population_size: int = 100
    min_population_size: int = 20
    max_population_size: int = 500
    initial_crossover_rate: float = 0.9
    min_crossover_rate: float = 0.6
    initial_mutation_rate: float = 0.01
    max_mutation_rate: float = 0.1
    diversity_threshold: float = 0.1
    convergence_window: int = 20

class MultiObjectiveFitness:
    """Multi-objective fitness function"""
    
    def __init__(self, objectives: List[Callable], weights: List[float] = None):
        self.objectives = objectives
        self.weights = weights or [1.0] * len(objectives)
    
    def evaluate(self, individual: Individual) -> float:
        """Evaluate multi-objective fitness using weighted sum"""
        values = [obj.evaluate(individual) for obj in self.objectives]
        return sum(w * v for w, v in zip(self.weights, values))
    
    def is_maximization(self) -> bool:
        return False

class AdaptiveGeneticAlgorithm:
    """Advanced GA with adaptive parameters"""
    
    def __init__(self, config: AdaptiveGAConfig):
        self.config = config
        self.generation = 0
        self.convergence_counter = 0
        self.previous_best_fitness = float('inf')
        
        # Adaptive parameters
        self.current_population_size = config.initial_population_size
        self.current_crossover_rate = config.initial_crossover_rate
        self.current_mutation_rate = config.initial_mutation_rate
    
    def adapt_parameters(self, diversity: float, fitness_change: float):
        """Adapt GA parameters based on diversity and convergence"""
        
        # Adapt population size
        if diversity < self.config.diversity_threshold:
            # Low diversity - increase population size
            self.current_population_size = min(
                self.config.max_population_size,
                self.current_population_size + 10
            )
            # Increase mutation rate to restore diversity
            self.current_mutation_rate = min(
                self.config.max_mutation_rate,
                self.current_mutation_rate * 1.2
            )
        else:
            # High diversity - can reduce population size for efficiency
            self.current_population_size = max(
                self.config.min_population_size,
                self.current_population_size - 5
            )
            # Reduce mutation rate
            self.current_mutation_rate = max(
                0.001,
                self.current_mutation_rate * 0.95
            )
        
        # Adapt crossover rate based on fitness improvement
        if fitness_change < 1e-6:  # No improvement
            self.convergence_counter += 1
            if self.convergence_counter > self.config.convergence_window:
                # Likely converged - reduce crossover, increase mutation
                self.current_crossover_rate = max(
                    self.config.min_crossover_rate,
                    self.current_crossover_rate * 0.9
                )
                self.current_mutation_rate = min(
                    self.config.max_mutation_rate,
                    self.current_mutation_rate * 1.5
                )
        else:
            self.convergence_counter = 0
            # Good improvement - maintain or slightly increase crossover
            self.current_crossover_rate = min(
                0.95,
                self.current_crossover_rate * 1.05
            )
    
    def selection_rank(self) -> Individual:
        """Rank-based selection"""
        # Sort by fitness
        sorted_pop = sorted(self.population, key=lambda x: x.fitness)
        
        # Assign ranks (1 to N)
        ranks = list(range(1, len(sorted_pop) + 1))
        total_rank = sum(ranks)
        
        # Calculate selection probabilities
        probabilities = [rank / total_rank for rank in ranks]
        
        # Select based on probabilities
        pick = random.uniform(0, 1)
        current = 0
        for individual, prob in zip(sorted_pop, probabilities):
            current += prob
            if current >= pick:
                return individual
        return sorted_pop[-1]
    
    def crossover_adaptive(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Adaptive crossover based on fitness"""
        if random.random() > self.current_crossover_rate:
            return parent1, parent2
        
        # Fitness-based crossover probability
        # Better parents have higher chance of successful crossover
        fitness_sum = parent1.fitness + parent2.fitness
        if fitness_sum == 0:
            crossover_prob = 0.5
        else:
            # Normalize fitness (lower is better for minimization)
            norm_fitness1 = parent1.fitness / fitness_sum
            norm_fitness2 = parent2.fitness / fitness_sum
            crossover_prob = 1.0 - (norm_fitness1 + norm_fitness2) / 2
        
        if random.random() > crossover_prob:
            return parent1, parent2
        
        # Perform uniform crossover
        child1_chromosome = []
        child2_chromosome = []
        
        for i in range(len(parent1.chromosome)):
            if random.random() < 0.5:
                child1_chromosome.append(parent1.chromosome[i])
                child2_chromosome.append(parent2.chromosome[i])
            else:
                child1_chromosome.append(parent2.chromosome[i])
                child2_chromosome.append(parent1.chromosome[i])
        
        child1 = Individual(chromosome=child1_chromosome, generation=self.generation + 1)
        child2 = Individual(chromosome=child2_chromosome, generation=self.generation + 1)
        
        return child1, child2
    
    def mutate_adaptive(self, individual: Individual) -> Individual:
        """Adaptive mutation based on fitness and diversity"""
        mutated_chromosome = individual.chromosome.copy()
        
        # Adaptive mutation rate
        base_rate = self.current_mutation_rate
        
        # Increase mutation for poor individuals
        if individual.fitness > np.mean([ind.fitness for ind in self.population]):
            mutation_rate = base_rate * 2.0
        else:
            mutation_rate = base_rate * 0.5
        
        for i in range(len(mutated_chromosome)):
            if random.random() < mutation_rate:
                # Adaptive mutation strength
                if individual.fitness > np.percentile([ind.fitness for ind in self.population], 75):
                    # Poor individual - large mutations
                    mutation_strength = 0.5
                else:
                    # Good individual - small mutations
                    mutation_strength = 0.1
                
                mutation_value = random.gauss(0, mutation_strength)
                mutated_chromosome[i] += mutation_value
                
                # Ensure bounds
                mutated_chromosome[i] = max(-5.12, min(5.12, mutated_chromosome[i]))
        
        return Individual(chromosome=mutated_chromosome, generation=individual.generation)
    
    def niching_selection(self, niche_radius: float = 0.5) -> List[Individual]:
        """Niching selection to maintain diversity"""
        niches = []
        
        for individual in self.population:
            # Find closest niche
            closest_niche = None
            min_distance = float('inf')
            
            for niche in niches:
                distance = np.linalg.norm(np.array(individual.chromosome) - 
                                        np.array(niche['center']))
                if distance < min_distance:
                    min_distance = distance
                    closest_niche = niche
            
            # Add to existing niche or create new one
            if closest_niche and min_distance < niche_radius:
                closest_niche['members'].append(individual)
                # Update niche center
                closest_niche['center'] = np.mean([
                    np.array(ind.chromosome) for ind in closest_niche['members']
                ], axis=0).tolist()
            else:
                niches.append({
                    'center': individual.chromosome,
                    'members': [individual]
                })
        
        # Select from each niche
        selected = []
        for niche in niches:
            if niche['members']:
                # Select best from each niche
                best_in_niche = min(niche['members'], key=lambda x: x.fitness)
                selected.append(best_in_niche)
        
        return selected

# Example usage with adaptive GA
def example_adaptive_ga():
    """Example: Adaptive Genetic Algorithm"""
    
    # Create fitness function
    fitness_func = RastriginFitness()
    
    # Create adaptive GA
    config = AdaptiveGAConfig(
        initial_population_size=100,
        initial_crossover_rate=0.8,
        initial_mutation_rate=0.02
    )
    
    # Initialize population
    population = []
    for _ in range(config.initial_population_size):
        chromosome = [random.uniform(-5.12, 5.12) for _ in range(10)]
        individual = Individual(chromosome=chromosome, generation=0)
        population.append(individual)
    
    # Evaluate initial population
    for individual in population:
        individual.fitness = fitness_func.evaluate(individual)
    
    # Evolution loop
    best_fitness_history = []
    diversity_history = []
    
    for generation in range(100):
        # Calculate statistics
        best_individual = min(population, key=lambda x: x.fitness)
        avg_fitness = np.mean([ind.fitness for ind in population])
        diversity = calculate_diversity(population)
        
        # Track history
        best_fitness_history.append(best_individual.fitness)
        diversity_history.append(diversity)
        
        # Adapt parameters
        fitness_change = abs(best_individual.fitness - config.previous_best_fitness)
        adapt_parameters(config, diversity, fitness_change)
        config.previous_best_fitness = best_individual.fitness
        
        # Selection with niching
        selected = niching_selection(population, niche_radius=1.0)
        
        # Create new population
        new_population = selected.copy()
        
        # Generate offspring
        while len(new_population) < config.current_population_size:
            parent1 = selection_rank(population)
            parent2 = selection_rank(population)
            
            child1, child2 = crossover_adaptive(parent1, parent2, config.current_crossover_rate)
            
            child1 = mutate_adaptive(child1, config.current_mutation_rate)
            child2 = mutate_adaptive(child2, config.current_mutation_rate)
            
            new_population.extend([child1, child2])
        
        population = new_population[:config.current_population_size]
        
        # Evaluate new population
        for individual in population:
            individual.fitness = fitness_func.evaluate(individual)
        
        # Print progress
        if generation % 10 == 0:
            print(f"Generation {generation}: Best = {best_individual.fitness:.6f}, "
                  f"Pop size = {config.current_population_size}, "
                  f"Crossover = {config.current_crossover_rate:.3f}, "
                  f"Mutation = {config.current_mutation_rate:.4f}")
    
    return best_individual, best_fitness_history, diversity_history

if __name__ == "__main__":
    example_adaptive_ga()
```

### Parallel Genetic Algorithm

```python
"""
Parallel Genetic Algorithm Implementation
"""

import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import random
import numpy as np
from typing import List, Tuple, Dict, Callable, Any
from dataclasses import dataclass

class ParallelGeneticAlgorithm:
    """Parallel GA implementation"""
    
    def __init__(self, 
                 population_size: int,
                 chromosome_length: int,
                 fitness_function: Callable,
                 num_islands: int = 4,
                 migration_rate: float = 0.1,
                 migration_interval: int = 10):
        """
        Initialize parallel GA
        
        Args:
            population_size: Total population size
            chromosome_length: Length of chromosomes
            fitness_function: Fitness function to evaluate
            num_islands: Number of parallel islands
            migration_rate: Rate of migration between islands
            migration_interval: Generations between migrations
        """
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.fitness_function = fitness_function
        self.num_islands = num_islands
        self.migration_rate = migration_rate
        self.migration_interval = migration_interval
        
        # Island populations
        self.islands = []
        self.island_sizes = []
        
        # Statistics
        self.global_best = None
        self.convergence_history = []
    
    def initialize_islands(self):
        """Initialize island populations"""
        base_size = self.population_size // self.num_islands
        remainder = self.population_size % self.num_islands
        
        self.islands = []
        self.island_sizes = []
        
        for i in range(self.num_islands):
            size = base_size + (1 if i < remainder else 0)
            self.island_sizes.append(size)
            
            # Create island population
            population = []
            for _ in range(size):
                chromosome = [random.uniform(-5.12, 5.12) for _ in range(self.chromosome_length)]
                individual = Individual(chromosome=chromosome, generation=0)
                population.append(individual)
            
            self.islands.append(population)
    
    def evaluate_island(self, island_idx: int) -> List[Individual]:
        """Evaluate fitness for an island"""
        island = self.islands[island_idx]
        
        # Parallel evaluation
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.fitness_function.evaluate, individual) 
                      for individual in island]
            
            for individual, future in zip(island, futures):
                individual.fitness = future.result()
        
        return island
    
    def evolve_island(self, island_idx: int) -> List[Individual]:
        """Evolve a single island"""
        island = self.islands[island_idx]
        
        # Selection
        selected = self.selection_tournament(island, k=3)
        
        # Create new generation
        new_island = [selected[0]]  # Elitism
        
        while len(new_island) < len(island):
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            
            # Crossover
            if random.random() < 0.8:
                child1, child2 = self.crossover_single_point(parent1, parent2)
            else:
                child1, child2 = parent1, parent2
            
            # Mutation
            child1 = self.mutate(child1, 0.01)
            child2 = self.mutate(child2, 0.01)
            
            new_island.extend([child1, child2])
        
        return new_island[:len(island)]
    
    def migrate(self):
        """Perform migration between islands"""
        # Select individuals to migrate
        migrants = []
        for i, island in enumerate(self.islands):
            # Select top individuals for migration
            sorted_island = sorted(island, key=lambda x: x.fitness)
            num_migrants = max(1, int(len(island) * self.migration_rate))
            migrants.extend(sorted_island[:num_migrants])
        
        # Distribute migrants randomly
        for migrant in migrants:
            target_island = random.randint(0, self.num_islands - 1)
            self.islands[target_island].append(migrant)
    
    def get_global_best(self) -> Individual:
        """Get the best individual across all islands"""
        all_individuals = []
        for island in self.islands:
            all_individuals.extend(island)
        
        return min(all_individuals, key=lambda x: x.fitness)
    
    def evolve_parallel(self, max_generations: int = 100) -> Individual:
        """Evolve using parallel islands"""
        self.initialize_islands()
        
        # Initial evaluation
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.evaluate_island, i) for i in range(self.num_islands)]
            self.islands = [future.result() for future in futures]
        
        for generation in range(max_generations):
            # Evolve each island in parallel
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.evolve_island, i) for i in range(self.num_islands)]
                self.islands = [future.result() for future in futures]
            
            # Re-evaluate populations
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.evaluate_island, i) for i in range(self.num_islands)]
                self.islands = [future.result() for future in futures]
            
            # Migration
            if generation % self.migration_interval == 0 and generation > 0:
                self.migrate()
            
            # Track global best
            global_best = self.get_global_best()
            self.convergence_history.append(global_best.fitness)
            
            if generation % 10 == 0:
                print(f"Generation {generation}: Global best = {global_best.fitness:.6f}")
        
        return self.get_global_best()

# Example usage with parallel GA
def example_parallel_ga():
    """Example: Parallel Genetic Algorithm"""
    
    def rastrigin_parallel(x):
        """Rastrigin function for parallel evaluation"""
        n = len(x)
        A = 10.0
        sum_term = sum(xi**2 - A * np.cos(2 * np.pi * xi) for xi in x)
        return A * n + sum_term
    
    # Create parallel GA
    pga = ParallelGeneticAlgorithm(
        population_size=200,
        chromosome_length=10,
        fitness_function=rastrigin_parallel,
        num_islands=4,
        migration_rate=0.1,
        migration_interval=5
    )
    
    # Evolve
    best_solution = pga.evolve_parallel(max_generations=50)
    
    print(f"\nParallel GA Best Solution:")
    print(f"  Fitness: {best_solution.fitness:.6f}")
    print(f"  Chromosome: {best_solution.chromosome[:5]}...")  # Show first 5 values
    
    return best_solution, pga.convergence_history

if __name__ == "__main__":
    example_parallel_ga()
```

## Input Format

### Genetic Algorithm Configuration

```yaml
genetic_algorithm_config:
  problem_definition:
    chromosome_length: number     # Length of chromosomes
    variable_bounds: array        # Bounds for each variable [min, max]
    optimization_type: "minimize|maximize"
    
  population_parameters:
    population_size: number       # Initial population size
    elitism_rate: number          # Proportion of elite individuals
    diversity_threshold: number   # Threshold for diversity maintenance
    
  genetic_operators:
    selection_method: "tournament|roulette|rank"
    tournament_size: number       # Size for tournament selection
    crossover_method: "single_point|uniform|multi_point"
    crossover_rate: number        # Probability of crossover
    mutation_method: "gaussian|uniform|adaptive"
    mutation_rate: number         # Probability of mutation
    mutation_strength: number     # Strength of mutations
    
  adaptive_parameters:
    enable_adaptation: boolean    # Enable parameter adaptation
    adaptation_strategy: "diversity_based|fitness_based|hybrid"
    population_adaptation: boolean # Adapt population size
    rate_adaptation: boolean      # Adapt crossover/mutation rates
    
  parallel_parameters:
    enable_parallel: boolean      # Enable parallel processing
    num_islands: number           # Number of parallel islands
    migration_rate: number        # Rate of migration between islands
    migration_interval: number    # Generations between migrations
    
  termination_criteria:
    max_generations: number       # Maximum number of generations
    fitness_threshold: number     # Target fitness value
    convergence_generations: number # Generations without improvement
    time_limit: number            # Maximum execution time in seconds
```

### Multi-Objective Configuration

```yaml
multi_objective_config:
  objectives:
    - objective_name: string      # Name of objective
      weight: number             # Weight in fitness calculation
      bounds: array              # [min, max] for objective
      is_constraint: boolean     # Whether this is a constraint
    
  fitness_aggregation:
    method: "weighted_sum|pareto|lexicographic"
    pareto_config:
      archive_size: number       # Size of Pareto archive
      diversity_mechanism: string # Diversity preservation method
      
  constraint_handling:
    penalty_method: "static|dynamic|adaptive"
    constraint_weights: array    # Weights for constraint violations
    feasibility_preference: boolean # Prefer feasible solutions
```

## Output Format

### Optimization Results

```yaml
optimization_results:
  best_solution:
    chromosome: array            # Best chromosome found
    fitness: number              # Fitness value
    generation_found: number     # Generation when found
    evaluation_count: number     # Number of fitness evaluations
    
  convergence_analysis:
    convergence_generation: number # Generation when converged
    convergence_rate: number     # Rate of convergence
    stagnation_detected: boolean # Whether stagnation occurred
    restart_count: number        # Number of restarts performed
    
  population_statistics:
    final_population_size: number
    average_fitness: number      # Average fitness of final population
    fitness_variance: number     # Variance in fitness
    diversity_measure: number    # Population diversity metric
    
  performance_metrics:
    total_execution_time: number # Total execution time
    evaluations_per_second: number # Fitness evaluations per second
    memory_usage: string         # Peak memory usage
    parallel_efficiency: number  # Efficiency of parallel processing
```

### Evolution History

```yaml
evolution_history:
  generation_data: array         # Data for each generation
  - generation: number
    best_fitness: number
    average_fitness: number
    worst_fitness: number
    population_diversity: number
    parameter_values: object     # Adaptive parameter values
    
  convergence_plot_data:
    x_axis: array                # Generation numbers
    y_axis: array                # Fitness values
    diversity_data: array        # Diversity over time
    
  parameter_evolution:
    crossover_rate: array        # Crossover rate over time
    mutation_rate: array         # Mutation rate over time
    population_size: array       # Population size over time
```

## Configuration Options

### Selection Strategies

```yaml
selection_strategies:
  tournament_selection:
    description: "Select best from random subset"
    best_for: ["general_purpose", "diversity_maintenance"]
    complexity: "O(k)"
    parameters: ["tournament_size"]
    
  roulette_wheel_selection:
    description: "Probabilistic selection based on fitness"
    best_for: ["fitness_proportional_selection"]
    complexity: "O(n)"
    parameters: ["fitness_scaling"]
    
  rank_based_selection:
    description: "Selection based on fitness rank"
    best_for: ["early_convergence_prevention"]
    complexity: "O(n log n)"
    parameters: ["selection_pressure"]
    
  niching_selection:
    description: "Maintain diversity through niching"
    best_for: ["multi_modal_optimization"]
    complexity: "O(n²)"
    parameters: ["niche_radius", "niche_count"]
```

### Crossover Methods

```yaml
crossover_methods:
  single_point_crossover:
    description: "Single crossover point"
    best_for: ["general_purpose", "simple_problems"]
    complexity: "O(n)"
    parameters: ["crossover_rate"]
    
  uniform_crossover:
    description: "Random gene selection from parents"
    best_for: ["diversity_generation", "complex_problems"]
    complexity: "O(n)"
    parameters: ["gene_probability"]
    
  multi_point_crossover:
    description: "Multiple crossover points"
    best_for: ["preserving_gene_blocks"]
    complexity: "O(n)"
    parameters: ["num_points", "crossover_rate"]
    
  arithmetic_crossover:
    description: "Linear combination of parents"
    best_for: ["continuous_optimization"]
    complexity: "O(n)"
    parameters: ["alpha", "beta"]
```

## Error Handling

### Optimization Failures

```yaml
optimization_failures:
  premature_convergence:
    detection_strategy: "diversity_monitoring"
    recovery_strategy: "increase_mutation"
    max_retries: 3
    fallback_action: "restart_with_new_population"
  
  no_improvement:
    detection_strategy: "fitness_plateau_detection"
    recovery_strategy: "parameter_adaptation"
    max_retries: 2
    fallback_action: "alternative_algorithm"
  
  constraint_violation:
    detection_strategy: "constraint_checking"
    recovery_strategy: "repair_mechanisms"
    max_retries: 1
    fallback_action: "penalty_method"
  
  numerical_instability:
    detection_strategy: "value_range_checking"
    recovery_strategy: "parameter_bounds_enforcement"
    max_retries: 2
    fallback_action: "simplified_model"
```

### Parallel Processing Failures

```yaml
parallel_failures:
  island_divergence:
    detection_strategy: "island_comparison"
    recovery_strategy: "increased_migration"
    max_retries: 2
    fallback_action: "sequential_processing"
  
  load_imbalance:
    detection_strategy: "execution_time_monitoring"
    recovery_strategy: "dynamic_load_balancing"
    max_retries: 1
    fallback_action: "fixed_partitioning"
  
  communication_failure:
    detection_strategy: "heartbeat_monitoring"
    recovery_strategy: "reconnection_attempts"
    max_retries: 3
    fallback_action: "island_isolation"
```

## Performance Optimization

### Algorithm Optimization

```python
# Optimization: Elitism with Dynamic Population Size
class DynamicElitismGA:
    """GA with dynamic elitism and population size"""
    
    def __init__(self, base_config):
        self.base_config = base_config
        self.elite_pool = []
        self.adaptive_params = {
            'population_size': base_config.population_size,
            'elitism_rate': base_config.elitism_rate,
            'diversity_target': 0.5
        }
    
    def adapt_elitism(self, current_diversity):
        """Adapt elitism based on diversity"""
        if current_diversity < self.adaptive_params['diversity_target']:
            # Low diversity - reduce elitism to allow more exploration
            self.adaptive_params['elitism_rate'] = max(0.05, 
                self.adaptive_params['elitism_rate'] * 0.8)
        else:
            # High diversity - increase elitism to preserve good solutions
            self.adaptive_params['elitism_rate'] = min(0.3, 
                self.adaptive_params['elitism_rate'] * 1.1)
    
    def maintain_elite_pool(self, new_elites):
        """Maintain a pool of elite individuals"""
        self.elite_pool.extend(new_elites)
        
        # Keep only top N elites
        self.elite_pool = sorted(self.elite_pool, key=lambda x: x.fitness)[:100]
        
        # Occasionally inject elite pool into population
        if random.random() < 0.1:
            return random.sample(self.elite_pool, min(5, len(self.elite_pool)))
        return []
```

### Memory Optimization

```yaml
memory_optimization:
  individual_caching:
    technique: "fitness_caching"
    memory_reduction: "30-50%"
    implementation: "hash_based_caching"
    
  population_streaming:
    technique: "chunked_processing"
    memory_reduction: "unlimited_population_size"
    implementation: "disk_based_storage"
    
  parallel_memory_sharing:
    technique: "shared_memory_objects"
    memory_reduction: "60-80%"
    implementation: "memory_mapped_files"
    
  incremental_evaluation:
    technique: "partial_evaluation"
    memory_reduction: "40-60%"
    implementation: "lazy_computation"
```

## Integration Examples

### With Machine Learning

```python
# Integration with hyperparameter optimization
class MLHyperparameterGA:
    """GA for machine learning hyperparameter optimization"""
    
    def __init__(self, model_class, parameter_space, validation_data):
        self.model_class = model_class
        self.parameter_space = parameter_space
        self.validation_data = validation_data
    
    def encode_parameters(self, params):
        """Encode hyperparameters as chromosome"""
        chromosome = []
        for param_name, param_config in self.parameter_space.items():
            if param_config['type'] == 'continuous':
                chromosome.append(params[param_name])
            elif param_config['type'] == 'discrete':
                chromosome.append(param_config['values'].index(params[param_name]))
        return chromosome
    
    def decode_chromosome(self, chromosome):
        """Decode chromosome to hyperparameters"""
        params = {}
        idx = 0
        for param_name, param_config in self.parameter_space.items():
            if param_config['type'] == 'continuous':
                params[param_name] = chromosome[idx]
                idx += 1
            elif param_config['type'] == 'discrete':
                value_idx = int(chromosome[idx])
                params[param_name] = param_config['values'][value_idx]
                idx += 1
        return params
    
    def evaluate_fitness(self, individual):
        """Evaluate model with given hyperparameters"""
        params = self.decode_chromosome(individual.chromosome)
        model = self.model_class(**params)
        
        # Train and evaluate
        model.fit(self.validation_data['X_train'], self.validation_data['y_train'])
        score = model.score(self.validation_data['X_val'], self.validation_data['y_val'])
        
        return -score  # Minimize negative score
```

### With Feature Selection

```python
# Integration with feature selection
class FeatureSelectionGA:
    """GA for feature selection in machine learning"""
    
    def __init__(self, dataset, model, target_metric='accuracy'):
        self.dataset = dataset
        self.model = model
        self.target_metric = target_metric
        self.num_features = dataset.shape[1] - 1  # Exclude target
    
    def evaluate_fitness(self, individual):
        """Evaluate feature subset"""
        # Decode chromosome to feature mask
        feature_mask = [gene > 0.5 for gene in individual.chromosome]
        
        # Select features
        X_selected = self.dataset.iloc[:, feature_mask]
        y = self.dataset.iloc[:, -1]  # Target
        
        # Train model and evaluate
        X_train, X_test, y_train, y_test = train_test_split(
            X_selected, y, test_size=0.3, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        
        # Calculate fitness (number of features vs performance)
        num_features = sum(feature_mask)
        performance = accuracy_score(y_test, predictions)
        
        # Fitness: balance performance and feature count
        fitness = performance - 0.01 * num_features
        
        return -fitness  # Minimize negative fitness
```

## Best Practices

1. **Parameter Tuning**:
   - Start with standard parameters and adapt based on problem characteristics
   - Use adaptive parameters for dynamic optimization landscapes
   - Balance exploration and exploitation through parameter adjustment

2. **Population Management**:
   - Maintain diversity through appropriate selection and mutation strategies
   - Use elitism to preserve good solutions
   - Implement niching for multi-modal problems

3. **Convergence Monitoring**:
   - Track multiple convergence indicators (fitness, diversity, parameter stability)
   - Implement restart strategies for premature convergence
   - Use adaptive termination criteria

4. **Parallel Processing**:
   - Use island models for parallelization
   - Balance migration rates for information exchange
   - Monitor load balancing in distributed implementations

## Troubleshooting

### Common Issues

1. **Premature Convergence**: Increase mutation rate, use niching, implement restart strategies
2. **Slow Convergence**: Adjust selection pressure, improve crossover operators, use adaptive parameters
3. **Poor Solution Quality**: Check fitness function design, increase population size, improve diversity
4. **High Computational Cost**: Use parallel processing, implement early termination, optimize fitness evaluation

### Debug Mode

```python
# Debug mode: Enhanced GA debugging
class DebugGA:
    """GA with enhanced debugging capabilities"""
    
    def __init__(self, config):
        self.config = config
        self.debug_log = []
        self.genealogy_tree = {}
        self.convergence_analysis = {}
    
    def log_generation(self, generation_data):
        """Log detailed generation information"""
        self.debug_log.append({
            'generation': generation_data['generation'],
            'best_fitness': generation_data['best_fitness'],
            'population_diversity': generation_data['diversity'],
            'parameter_values': generation_data['parameters'],
            'convergence_indicators': generation_data['convergence']
        })
    
    def analyze_convergence(self):
        """Analyze convergence patterns"""
        fitness_trend = [entry['best_fitness'] for entry in self.debug_log]
        
        # Detect plateaus
        plateaus = []
        for i in range(len(fitness_trend) - 10):
            window = fitness_trend[i:i+10]
            if max(window) - min(window) < 1e-6:
                plateaus.append(i)
        
        self.convergence_analysis['plateaus'] = plateaus
        self.convergence_analysis['convergence_rate'] = self.calculate_convergence_rate()
        
        return self.convergence_analysis
    
    def generate_debug_report(self):
        """Generate comprehensive debug report"""
        return {
            'execution_summary': self.get_execution_summary(),
            'convergence_analysis': self.analyze_convergence(),
            'parameter_evolution': self.get_parameter_evolution(),
            'population_dynamics': self.get_population_dynamics(),
            'recommendations': self.get_recommendations()
        }
```

## Monitoring and Metrics

### GA Performance Metrics

```yaml
ga_performance_metrics:
  convergence_metrics:
    convergence_speed: number     # Generations to convergence
    convergence_stability: number # Stability of convergence
    solution_quality: number      # Quality of final solution
    
  diversity_metrics:
    genotypic_diversity: number   # Genetic diversity in population
    phenotypic_diversity: number  # Phenotypic diversity
    niche_diversity: number       # Diversity across niches
    
  efficiency_metrics:
    evaluations_per_generation: number
    parallel_efficiency: number   # Efficiency of parallel processing
    memory_efficiency: number     # Memory usage efficiency
    
  robustness_metrics:
    restart_effectiveness: number # Effectiveness of restart strategies
    parameter_sensitivity: number # Sensitivity to parameter changes
    problem_adaptability: number  # Adaptability to different problems
```

## Dependencies

- **Mathematical Libraries**: NumPy, SciPy for mathematical operations
- **Parallel Processing**: multiprocessing, concurrent.futures for parallel execution
- **Optimization Libraries**: DEAP, PyGAD for advanced GA features
- **Machine Learning**: scikit-learn, TensorFlow for ML integration
- **Visualization**: Matplotlib, Plotly for result visualization

## Version History

- **1.0.0**: Initial release with comprehensive genetic algorithm frameworks
- **1.1.0**: Added adaptive parameters and parallel processing capabilities
- **1.2.0**: Enhanced multi-objective optimization and constraint handling
- **1.3.0**: Improved debugging tools and performance monitoring
- **1.4.0**: Advanced integration with machine learning and feature selection

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

Content for ## Constraints involving Genetic Algorithm Optimization.