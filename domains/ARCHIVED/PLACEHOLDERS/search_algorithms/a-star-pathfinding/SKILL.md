---
Domain: search_algorithms
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: a-star-pathfinding
---



## Description

Automatically designs and implements optimal A* (A-star) pathfinding algorithms for finding shortest paths in weighted graphs and grids. This skill provides comprehensive frameworks for heuristic design, graph representation, path optimization, and integration with real-time applications including games, robotics, and navigation systems.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Heuristic Design**: Create optimal heuristics (Manhattan, Euclidean, Diagonal) for different pathfinding scenarios
- **Graph Representation**: Implement efficient graph structures (grid-based, node-based, hierarchical) for pathfinding
- **Path Optimization**: Optimize paths for distance, time, cost, or custom criteria using weighted graphs
- **Real-time Performance**: Implement efficient data structures (priority queues, binary heaps) for real-time applications
- **Obstacle Avoidance**: Handle dynamic obstacles, moving targets, and complex terrain
- **Multi-target Pathfinding**: Find optimal paths to multiple targets with priority handling
- **Memory Management**: Optimize memory usage for large-scale pathfinding applications

## Usage Examples

### Basic A* Pathfinding Implementation

```python
"""
A* Pathfinding Algorithm Implementation
"""

import heapq
from typing import List, Tuple, Dict, Set, Optional, Callable
from dataclasses import dataclass

@dataclass
class Node:
    """Node representation for A* algorithm"""
    x: int
    y: int
    g_cost: float = 0      # Cost from start to current node
    h_cost: float = 0      # Heuristic cost from current node to goal
    f_cost: float = 0      # Total cost (g + h)
    parent: Optional['Node'] = None
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class AStarPathfinder:
    """A* pathfinding implementation"""
    
    def __init__(self, grid: List[List[int]], 
                 heuristic_func: Callable[[Node, Node], float] = None):
        """
        Initialize A* pathfinder
        
        Args:
            grid: 2D grid where 0 = walkable, 1 = obstacle
            heuristic_func: Custom heuristic function
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        
        # Default heuristic: Manhattan distance
        if heuristic_func is None:
            self.heuristic = self.manhattan_distance
        else:
            self.heuristic = heuristic_func
    
    def manhattan_distance(self, node: Node, goal: Node) -> float:
        """Manhattan distance heuristic"""
        return abs(node.x - goal.x) + abs(node.y - goal.y)
    
    def euclidean_distance(self, node: Node, goal: Node) -> float:
        """Euclidean distance heuristic"""
        return ((node.x - goal.x) ** 2 + (node.y - goal.y) ** 2) ** 0.5
    
    def diagonal_distance(self, node: Node, goal: Node) -> float:
        """Diagonal distance heuristic (Chebyshev distance)"""
        dx = abs(node.x - goal.x)
        dy = abs(node.y - goal.y)
        return max(dx, dy)
    
    def get_neighbors(self, node: Node) -> List[Node]:
        """Get valid neighboring nodes"""
        neighbors = []
        directions = [
            (0, 1),   # Right
            (1, 0),   # Down
            (0, -1),  # Left
            (-1, 0),  # Up
            (1, 1),   # Down-Right (diagonal)
            (1, -1),  # Down-Left (diagonal)
            (-1, 1),  # Up-Right (diagonal)
            (-1, -1)  # Up-Left (diagonal)
        ]
        
        for dx, dy in directions:
            new_x, new_y = node.x + dx, node.y + dy
            
            # Check bounds
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
                # Check if walkable
                if self.grid[new_x][new_y] == 0:
                    # Calculate movement cost
                    cost = 1.0 if dx == 0 or dy == 0 else 1.414  # Diagonal cost ≈ √2
                    neighbors.append(Node(new_x, new_y, g_cost=cost))
        
        return neighbors
    
    def find_path(self, start: Tuple[int, int], 
                  goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Find shortest path from start to goal
        
        Args:
            start: Starting position (x, y)
            goal: Goal position (x, y)
            
        Returns:
            List of coordinates representing the path
        """
        start_node = Node(start[0], start[1])
        goal_node = Node(goal[0], goal[1])
        
        # Open set (priority queue)
        open_set = []
        heapq.heappush(open_set, start_node)
        
        # Closed set (visited nodes)
        closed_set: Set[Node] = set()
        
        # For path reconstruction
        came_from: Dict[Node, Node] = {}
        
        # Cost from start to each node
        g_costs: Dict[Node, float] = {start_node: 0}
        
        while open_set:
            # Get node with lowest f_cost
            current = heapq.heappop(open_set)
            
            # Check if goal reached
            if current == goal_node:
                return self.reconstruct_path(came_from, current)
            
            closed_set.add(current)
            
            # Check all neighbors
            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue
                
                # Calculate tentative g_cost
                tentative_g = g_costs[current] + neighbor.g_cost
                
                if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                    # This path is better
                    came_from[neighbor] = current
                    g_costs[neighbor] = tentative_g
                    neighbor.g_cost = tentative_g
                    neighbor.h_cost = self.heuristic(neighbor, goal_node)
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    
                    if neighbor not in open_set:
                        heapq.heappush(open_set, neighbor)
        
        # No path found
        return []
    
    def reconstruct_path(self, came_from: Dict[Node, Node], 
                        current: Node) -> List[Tuple[int, int]]:
        """Reconstruct path from goal to start"""
        path = []
        while current is not None:
            path.append((current.x, current.y))
            current = came_from.get(current)
        
        path.reverse()
        return path

# Example usage
def example_basic_pathfinding():
    """Example: Basic A* pathfinding on a grid"""
    
    # Create a grid (0 = walkable, 1 = obstacle)
    grid = [
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    
    # Create pathfinder
    pathfinder = AStarPathfinder(grid)
    
    # Find path from (0, 0) to (4, 4)
    start = (0, 0)
    goal = (4, 4)
    
    path = pathfinder.find_path(start, goal)
    
    print(f"Path from {start} to {goal}:")
    for i, (x, y) in enumerate(path):
        print(f"  Step {i}: ({x}, {y})")
    
    return path

if __name__ == "__main__":
    example_basic_pathfinding()
```

### Advanced A* with Custom Heuristics

```python
"""
Advanced A* with Custom Heuristics and Optimization
"""

import heapq
from typing import List, Tuple, Dict, Set, Optional, Callable
from dataclasses import dataclass
import math

@dataclass
class WeightedNode:
    """Enhanced node with additional pathfinding information"""
    x: int
    y: int
    g_cost: float = 0
    h_cost: float = 0
    f_cost: float = 0
    parent: Optional['WeightedNode'] = None
    terrain_cost: float = 1.0  # Movement cost for this terrain
    is_diagonal: bool = False  # Whether this move was diagonal
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost

class AdvancedAStar:
    """Advanced A* implementation with custom heuristics and optimization"""
    
    def __init__(self, grid: List[List[float]], 
                 heuristic_weights: Dict[str, float] = None):
        """
        Initialize advanced A* pathfinder
        
        Args:
            grid: 2D grid with movement costs (higher = more expensive)
            heuristic_weights: Weights for different heuristic components
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        
        # Heuristic weights
        self.weights = heuristic_weights or {
            'distance': 1.0,
            'terrain': 0.5,
            'danger': 0.3
        }
    
    def custom_heuristic(self, node: WeightedNode, goal: WeightedNode) -> float:
        """Custom heuristic combining multiple factors"""
        # Base distance heuristic
        distance = self.euclidean_distance(node, goal)
        
        # Terrain cost heuristic (penalize expensive terrain)
        terrain_penalty = self.grid[node.x][node.y] * self.weights['terrain']
        
        # Danger heuristic (avoid high-cost areas)
        danger_penalty = sum(self.grid[i][j] for i in range(max(0, node.x-1), min(self.rows, node.x+2))
                           for j in range(max(0, node.y-1), min(self.cols, node.y+2))) * self.weights['danger']
        
        return (distance * self.weights['distance'] + 
                terrain_penalty + 
                danger_penalty)
    
    def euclidean_distance(self, node: WeightedNode, goal: WeightedNode) -> float:
        """Euclidean distance with terrain consideration"""
        dx = node.x - goal.x
        dy = node.y - goal.y
        return math.sqrt(dx*dx + dy*dy)
    
    def get_neighbors(self, node: WeightedNode) -> List[WeightedNode]:
        """Get neighbors with terrain cost consideration"""
        neighbors = []
        directions = [
            (0, 1, False),   # Right
            (1, 0, False),   # Down
            (0, -1, False),  # Left
            (-1, 0, False),  # Up
            (1, 1, True),    # Down-Right
            (1, -1, True),   # Down-Left
            (-1, 1, True),   # Up-Right
            (-1, -1, True)   # Up-Left
        ]
        
        for dx, dy, is_diagonal in directions:
            new_x, new_y = node.x + dx, node.y + dy
            
            # Check bounds
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
                # Get terrain cost
                terrain_cost = self.grid[new_x][new_y]
                
                # Calculate movement cost
                base_cost = 1.0 if not is_diagonal else 1.414
                total_cost = base_cost * terrain_cost
                
                neighbor = WeightedNode(
                    x=new_x, 
                    y=new_y, 
                    g_cost=total_cost,
                    terrain_cost=terrain_cost,
                    is_diagonal=is_diagonal
                )
                neighbors.append(neighbor)
        
        return neighbors
    
    def find_optimal_path(self, start: Tuple[int, int], 
                         goal: Tuple[int, int]) -> Dict:
        """
        Find optimal path with detailed information
        
        Returns:
            Dictionary with path, cost, and performance metrics
        """
        start_node = WeightedNode(start[0], start[1])
        goal_node = WeightedNode(goal[0], goal[1])
        
        # Priority queue
        open_set = []
        heapq.heappush(open_set, start_node)
        
        # Tracking
        closed_set: Set[WeightedNode] = set()
        came_from: Dict[WeightedNode, WeightedNode] = {}
        g_costs: Dict[WeightedNode, float] = {start_node: 0}
        
        nodes_explored = 0
        
        while open_set:
            current = heapq.heappop(open_set)
            nodes_explored += 1
            
            if current == goal_node:
                path = self.reconstruct_path(came_from, current)
                return {
                    'path': path,
                    'total_cost': g_costs[current],
                    'path_length': len(path),
                    'nodes_explored': nodes_explored,
                    'success': True
                }
            
            closed_set.add(current)
            
            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue
                
                tentative_g = g_costs[current] + neighbor.g_cost
                
                if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                    came_from[neighbor] = current
                    g_costs[neighbor] = tentative_g
                    neighbor.g_cost = tentative_g
                    neighbor.h_cost = self.custom_heuristic(neighbor, goal_node)
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    
                    if neighbor not in open_set:
                        heapq.heappush(open_set, neighbor)
        
        return {
            'path': [],
            'total_cost': float('inf'),
            'path_length': 0,
            'nodes_explored': nodes_explored,
            'success': False
        }
    
    def reconstruct_path(self, came_from: Dict[WeightedNode, WeightedNode], 
                        current: WeightedNode) -> List[Tuple[int, int]]:
        """Reconstruct path with coordinate tuples"""
        path = []
        while current is not None:
            path.append((current.x, current.y))
            current = came_from.get(current)
        
        path.reverse()
        return path

# Example usage with terrain costs
def example_advanced_pathfinding():
    """Example: Advanced A* with terrain costs and custom heuristics"""
    
    # Create grid with terrain costs (higher = more expensive/dangerous)
    grid = [
        [1.0, 1.0, 1.0, 5.0, 1.0],  # 5.0 = very expensive (mountain)
        [1.0, 3.0, 1.0, 5.0, 1.0],  # 3.0 = expensive (forest)
        [1.0, 3.0, 1.0, 1.0, 1.0],
        [1.0, 1.0, 5.0, 5.0, 1.0],  # 5.0 = obstacle (water)
        [1.0, 1.0, 1.0, 1.0, 1.0]
    ]
    
    # Custom heuristic weights
    weights = {
        'distance': 1.0,    # Standard distance priority
        'terrain': 0.8,     # High terrain cost penalty
        'danger': 0.5       # Moderate danger avoidance
    }
    
    # Create advanced pathfinder
    pathfinder = AdvancedAStar(grid, weights)
    
    # Find path
    start = (0, 0)
    goal = (4, 4)
    
    result = pathfinder.find_optimal_path(start, goal)
    
    print(f"Advanced A* Pathfinding Results:")
    print(f"  Start: {start}, Goal: {goal}")
    print(f"  Path found: {result['success']}")
    print(f"  Total cost: {result['total_cost']:.2f}")
    print(f"  Path length: {result['path_length']} steps")
    print(f"  Nodes explored: {result['nodes_explored']}")
    
    if result['success']:
        print("  Path coordinates:")
        for i, (x, y) in enumerate(result['path']):
            cost = grid[x][y]
            print(f"    Step {i}: ({x}, {y}) [cost: {cost}]")
    
    return result

if __name__ == "__main__":
    example_advanced_pathfinding()
```

### Real-time A* for Games

```python
"""
Real-time A* Pathfinding for Games
"""

import heapq
import time
from typing import List, Tuple, Dict, Set, Optional, Callable
from dataclasses import dataclass
from collections import deque

@dataclass
class GameNode:
    """Node for game pathfinding with additional game-specific data"""
    x: int
    y: int
    g_cost: float = 0
    h_cost: float = 0
    f_cost: float = 0
    parent: Optional['GameNode'] = None
    unit_type: str = "ground"  # ground, air, water
    movement_points: int = 1
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost

class RealTimeAStar:
    """Real-time A* optimized for game applications"""
    
    def __init__(self, game_map: List[List[Dict]], 
                 time_limit: float = 0.016):  # 16ms for 60 FPS
        """
        Initialize real-time A* pathfinder
        
        Args:
            game_map: 2D grid with tile properties
            time_limit: Maximum time per frame (seconds)
        """
        self.game_map = game_map
        self.rows = len(game_map)
        self.cols = len(game_map[0]) if game_map else 0
        self.time_limit = time_limit
        
        # Optimization: Precompute common heuristics
        self.heuristic_cache: Dict[Tuple[int, int, int, int], float] = {}
    
    def get_movement_cost(self, from_node: GameNode, to_node: GameNode) -> float:
        """Calculate movement cost based on unit type and terrain"""
        tile = self.game_map[to_node.x][to_node.y]
        
        # Base movement cost
        base_cost = tile.get('movement_cost', 1.0)
        
        # Unit type restrictions
        unit_type = from_node.unit_type
        if unit_type == "air" and tile.get('air_impassable', False):
            return float('inf')
        elif unit_type == "ground" and tile.get('ground_impassable', False):
            return float('inf')
        elif unit_type == "water" and tile.get('water_impassable', False):
            return float('inf')
        
        # Diagonal movement penalty
        if abs(from_node.x - to_node.x) == 1 and abs(from_node.y - to_node.y) == 1:
            base_cost *= 1.414
        
        return base_cost
    
    def get_heuristic(self, node: GameNode, goal: GameNode) -> float:
        """Optimized heuristic with caching"""
        cache_key = (node.x, node.y, goal.x, goal.y)
        
        if cache_key in self.heuristic_cache:
            return self.heuristic_cache[cache_key]
        
        # Euclidean distance with terrain consideration
        dx = abs(node.x - goal.x)
        dy = abs(node.y - goal.y)
        heuristic = math.sqrt(dx*dx + dy*dy)
        
        # Cache result
        self.heuristic_cache[cache_key] = heuristic
        return heuristic
    
    def find_path_incremental(self, start: Tuple[int, int], 
                             goal: Tuple[int, int], 
                             unit_type: str = "ground") -> List[Tuple[int, int]]:
        """
        Find path incrementally to avoid frame drops
        
        Returns partial path if time limit exceeded
        """
        start_node = GameNode(start[0], start[1], unit_type=unit_type)
        goal_node = GameNode(goal[0], goal[1], unit_type=unit_type)
        
        # Priority queue
        open_set = []
        heapq.heappush(open_set, start_node)
        
        # Tracking
        closed_set: Set[GameNode] = set()
        came_from: Dict[GameNode, GameNode] = {}
        g_costs: Dict[GameNode, float] = {start_node: 0}
        
        start_time = time.time()
        
        while open_set:
            # Check time limit
            if time.time() - start_time > self.time_limit:
                # Time's up, return partial path
                return self.get_partial_path(came_from, start_node, goal_node)
            
            current = heapq.heappop(open_set)
            
            if current == goal_node:
                return self.reconstruct_path(came_from, current)
            
            closed_set.add(current)
            
            # Process neighbors
            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue
                
                movement_cost = self.get_movement_cost(current, neighbor)
                if movement_cost == float('inf'):
                    continue
                
                tentative_g = g_costs[current] + movement_cost
                
                if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                    came_from[neighbor] = current
                    g_costs[neighbor] = tentative_g
                    neighbor.g_cost = tentative_g
                    neighbor.h_cost = self.get_heuristic(neighbor, goal_node)
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    
                    if neighbor not in open_set:
                        heapq.heappush(open_set, neighbor)
        
        # No path found
        return []
    
    def get_neighbors(self, node: GameNode) -> List[GameNode]:
        """Get valid neighbors for game units"""
        neighbors = []
        directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # Cardinal
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal
        ]
        
        for dx, dy in directions:
            new_x, new_y = node.x + dx, node.y + dy
            
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
                neighbor = GameNode(new_x, new_y, unit_type=node.unit_type)
                neighbors.append(neighbor)
        
        return neighbors
    
    def get_partial_path(self, came_from: Dict[GameNode, GameNode], 
                        start: GameNode, goal: GameNode) -> List[Tuple[int, int]]:
        """Get partial path towards goal when time runs out"""
        # Find the node closest to goal that we've explored
        best_node = start
        best_distance = float('inf')
        
        for node in came_from:
            distance = self.get_heuristic(node, goal)
            if distance < best_distance:
                best_distance = distance
                best_node = node
        
        # Return path to best node found
        return self.reconstruct_path(came_from, best_node)
    
    def reconstruct_path(self, came_from: Dict[GameNode, GameNode], 
                        current: GameNode) -> List[Tuple[int, int]]:
        """Reconstruct path as coordinate tuples"""
        path = []
        while current is not None:
            path.append((current.x, current.y))
            current = came_from.get(current)
        
        path.reverse()
        return path

# Example usage for game pathfinding
def example_game_pathfinding():
    """Example: Real-time A* for game units"""
    
    # Create game map with terrain properties
    game_map = [
        [{'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 2.0, 'ground_impassable': False, 'air_impassable': False},  # Forest
         {'movement_cost': 5.0, 'ground_impassable': True, 'air_impassable': False},   # Mountain (ground impassable)
         {'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False}],
        
        [{'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 3.0, 'ground_impassable': False, 'air_impassable': False},  # Rough terrain
         {'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 5.0, 'ground_impassable': True, 'air_impassable': False},
         {'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False}],
        
        [{'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 3.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False}],
        
        [{'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 5.0, 'ground_impassable': True, 'air_impassable': False},
         {'movement_cost': 5.0, 'ground_impassable': True, 'air_impassable': False},
         {'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False}],
        
        [{'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False},
         {'movement_cost': 1.0, 'ground_impassable': False, 'air_impassable': False}]
    ]
    
    # Create real-time pathfinder
    pathfinder = RealTimeAStar(game_map, time_limit=0.005)  # 5ms time limit
    
    # Test different unit types
    start = (0, 0)
    goal = (4, 4)
    
    print("Real-time A* Pathfinding for Games:")
    
    # Ground unit (cannot cross mountains)
    ground_path = pathfinder.find_path_incremental(start, goal, "ground")
    print(f"  Ground unit path: {len(ground_path)} steps")
    print(f"    Path: {ground_path[:5]}{'...' if len(ground_path) > 5 else ''}")
    
    # Air unit (can fly over anything)
    air_path = pathfinder.find_path_incremental(start, goal, "air")
    print(f"  Air unit path: {len(air_path)} steps")
    print(f"    Path: {air_path[:5]}{'...' if len(air_path) > 5 else ''}")
    
    return {
        'ground_path': ground_path,
        'air_path': air_path
    }

if __name__ == "__main__":
    example_game_pathfinding()
```

## Input Format

### A* Pathfinding Request

```yaml
a_star_pathfinding_request:
  grid_type: "2d_array|graph|hexagonal"
  grid_data: array              # Grid representation or graph data
  
  if grid_type == "2d_array":
    obstacles: array            # Obstacle coordinates
    walkable_values: array      # Values representing walkable terrain
    movement_costs: object      # Movement cost mappings
    
  if grid_type == "graph":
    nodes: array                # Node definitions
    edges: array                # Edge connections with weights
    adjacency_list: object      # Adjacency list representation
  
  start_position: array         # Starting coordinates [x, y] or node ID
  goal_position: array          # Goal coordinates [x, y] or node ID
  
  heuristic_config:
    heuristic_type: "manhattan|euclidean|diagonal|custom"
    heuristic_weights: object   # Weights for custom heuristics
    diagonal_movement: boolean  # Allow diagonal movement
    
  optimization_config:
    time_limit: number          # Maximum execution time in seconds
    memory_limit: string        # Memory usage limit
    early_termination: boolean  # Stop when path found vs optimal
    incremental_search: boolean # Incremental pathfinding for real-time
```

### Pathfinding Configuration

```yaml
pathfinding_config:
  algorithm_type: "a_star|weighted_a_star|jump_point_search"
  performance_requirements:
    max_execution_time: number  # Maximum allowed execution time
    max_memory_usage: string    # Maximum allowed memory usage
    frame_rate_target: number   # Target FPS for real-time applications
    
  path_quality_requirements:
    optimality_guarantee: boolean # Guarantee optimal path
    smoothness_preference: boolean # Prefer smoother paths
    distance_vs_time: string    # "distance" or "time" optimization
    
  environment_constraints:
    dynamic_obstacles: boolean  # Handle moving obstacles
    multiple_agents: boolean    # Handle multiple pathfinding agents
    collision_avoidance: boolean # Avoid agent collisions
```

## Output Format

### Pathfinding Results

```yaml
pathfinding_results:
  path_found: boolean
  path_coordinates: array       # List of coordinates [(x,y), ...]
  path_length: number           # Number of steps in path
  total_cost: number            # Total path cost
  
  if path_found == true:
    execution_metrics:
      execution_time: number    # Time taken to find path
      nodes_explored: number    # Number of nodes explored
      memory_used: string       # Memory usage during execution
      algorithm_efficiency: number # Efficiency metric (nodes/cost ratio)
      
    path_details:
      step_by_step: array       # Detailed step information
      terrain_analysis: object  # Analysis of terrain costs
      alternative_paths: array  # Alternative path options
      
  if path_found == false:
    failure_analysis:
      reason: string            # Reason path not found
      closest_approach: array   # Coordinates of closest approach
      suggested_modifications: array # Suggestions to find path
```

### Performance Analysis

```yaml
performance_analysis:
  algorithm_performance:
    time_complexity: string     # O(n log n), O(n²), etc.
    space_complexity: string    # O(n), O(n²), etc.
    actual_execution_time: number # Measured execution time
    theoretical_bounds: object  # Theoretical performance bounds
    
  memory_usage:
    peak_memory: string         # Peak memory usage
    average_memory: string      # Average memory usage
    memory_efficiency: number   # Memory usage efficiency score
    
  optimization_effectiveness:
    heuristic_effectiveness: number # How well heuristic guided search
    pruning_effectiveness: number   # How well search was pruned
    cache_hit_rate: number      # Cache effectiveness for heuristics
```

## Configuration Options

### Heuristic Selection

```yaml
heuristic_selection:
  manhattan_distance:
    description: "Grid-based distance (|dx| + |dy|)"
    best_for: ["grid_maps", "cardinal_movement", "maze_like_environments"]
    complexity: "O(1)"
    accuracy: "good"
    
  euclidean_distance:
    description: "Straight-line distance (√((dx² + dy²)))"
    best_for: ["open_environments", "diagonal_movement", "continuous_spaces"]
    complexity: "O(1)"
    accuracy: "excellent"
    
  diagonal_distance:
    description: "Chebyshev distance (max(|dx|, |dy|))"
    best_for: ["chess_like_movement", "8_direction_movement"]
    complexity: "O(1)"
    accuracy: "good"
    
  custom_heuristic:
    description: "User-defined heuristic function"
    best_for: ["domain_specific", "multi_criteria_optimization"]
    complexity: "variable"
    accuracy: "domain_dependent"
```

### Optimization Strategies

```yaml
optimization_strategies:
  priority_queues:
    description: "Efficient open set management"
    implementation: "binary_heap|fibonacci_heap|bucket_queue"
    time_complexity: "O(log n)"
    space_complexity: "O(n)"
    
  bidirectional_search:
    description: "Search from both start and goal"
    best_for: ["large_maps", "single_source_single_target"]
    time_improvement: "50% reduction typical"
    memory_overhead: "2x memory usage"
    
  jump_point_search:
    description: "Skip over symmetries in grid maps"
    best_for: ["uniform_cost_grids", "video_game_maps"]
    time_improvement: "10-20x speedup typical"
    implementation_complexity: "high"
    
  hierarchical_pathfinding:
    description: "Multi-level abstraction for large maps"
    best_for: ["very_large_maps", "multi_scale_navigation"]
    time_improvement: "logarithmic scaling"
    path_quality: "approximate_optimal"
```

## Error Handling

### Pathfinding Failures

```yaml
pathfinding_failures:
  no_path_found:
    detection_strategy: "exhaustive_search"
    recovery_strategy: "relax_constraints"
    escalation: "manual_intervention"
  
  timeout_exceeded:
    retry_strategy: "increase_time_limit"
    max_retries: 2
    fallback_action: "return_partial_path"
  
  memory_exhaustion:
    retry_strategy: "reduce_search_depth"
    max_retries: 1
    fallback_action: "simplified_algorithm"
  
  invalid_input:
    detection_strategy: "input_validation"
    recovery_strategy: "input_correction"
    escalation: "user_notification"
```

### Performance Issues

```yaml
performance_issues:
  slow_execution:
    detection_strategy: "profiling"
    recovery_strategy: "algorithm_optimization"
    escalation: "hardware_upgrade"
  
  high_memory_usage:
    detection_strategy: "memory_monitoring"
    recovery_strategy: "memory_optimization"
    escalation: "distributed_computing"
  
  poor_path_quality:
    detection_strategy: "path_analysis"
    recovery_strategy: "heuristic_tuning"
    escalation: "algorithm_replacement"
```

## Performance Optimization

### Algorithm Optimization

```python
# Optimization: Bidirectional A*
class BidirectionalAStar:
    """Bidirectional A* for improved performance"""
    
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
    
    def find_path_bidirectional(self, start, goal):
        """Find path using bidirectional search"""
        # Forward search from start
        forward_open = []
        forward_closed = set()
        forward_came_from = {}
        forward_g_costs = {start: 0}
        
        # Backward search from goal
        backward_open = []
        backward_closed = set()
        backward_came_from = {}
        backward_g_costs = {goal: 0}
        
        heapq.heappush(forward_open, (0, start))
        heapq.heappush(backward_open, (0, goal))
        
        meeting_point = None
        
        while forward_open and backward_open:
            # Expand forward search
            if forward_open[0][0] <= backward_open[0][0]:
                current = heapq.heappop(forward_open)[1]
                if current in forward_closed:
                    continue
                forward_closed.add(current)
                
                # Check if met backward search
                if current in backward_closed:
                    meeting_point = current
                    break
                
                # Expand neighbors
                for neighbor in self.get_neighbors(current):
                    if neighbor in forward_closed:
                        continue
                    
                    tentative_g = forward_g_costs[current] + 1
                    
                    if neighbor not in forward_g_costs or tentative_g < forward_g_costs[neighbor]:
                        forward_came_from[neighbor] = current
                        forward_g_costs[neighbor] = tentative_g
                        f_cost = tentative_g + self.heuristic(neighbor, goal)
                        heapq.heappush(forward_open, (f_cost, neighbor))
            else:
                # Expand backward search
                current = heapq.heappop(backward_open)[1]
                if current in backward_closed:
                    continue
                backward_closed.add(current)
                
                # Check if met forward search
                if current in forward_closed:
                    meeting_point = current
                    break
                
                # Expand neighbors
                for neighbor in self.get_neighbors(current):
                    if neighbor in backward_closed:
                        continue
                    
                    tentative_g = backward_g_costs[current] + 1
                    
                    if neighbor not in backward_g_costs or tentative_g < backward_g_costs[neighbor]:
                        backward_came_from[neighbor] = current
                        backward_g_costs[neighbor] = tentative_g
                        f_cost = tentative_g + self.heuristic(neighbor, start)
                        heapq.heappush(backward_open, (f_cost, neighbor))
        
        if meeting_point:
            # Reconstruct path
            forward_path = self.reconstruct_path(forward_came_from, meeting_point)
            backward_path = self.reconstruct_path(backward_came_from, meeting_point)
            backward_path.reverse()
            
            return forward_path + backward_path[1:]  # Remove duplicate meeting point
        
        return []  # No path found
```

### Memory Optimization

```yaml
memory_optimization:
  node_pooling:
    technique: "object_reuse"
    memory_reduction: "30-50%"
    implementation: "preallocated_node_pool"
    
  lazy_evaluation:
    technique: "on_demand_computation"
    memory_reduction: "40-60%"
    implementation: "lazy_heuristic_calculation"
    
  compression:
    technique: "coordinate_compression"
    memory_reduction: "20-40%"
    implementation: "grid_abstraction"
    
  streaming:
    technique: "chunked_processing"
    memory_reduction: "unlimited_map_size"
    implementation: "tile_based_loading"
```

## Integration Examples

### With Game Engines

```python
# Integration with Unity-like game engine
class UnityAStarIntegration:
    """Integration with Unity game engine"""
    
    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.pathfinder = AStarPathfinder()
    
    def find_path_3d(self, start_pos, goal_pos, obstacles):
        """Find 3D path for game units"""
        # Convert world coordinates to grid coordinates
        start_grid = self.world_to_grid(start_pos)
        goal_grid = self.world_to_grid(goal_pos)
        
        # Create grid from obstacles
        grid = self.create_grid_from_obstacles(obstacles)
        
        # Find path
        path_grid = self.pathfinder.find_path(start_grid, goal_grid)
        
        # Convert back to world coordinates
        path_world = [self.grid_to_world(pos) for pos in path_grid]
        
        return path_world
    
    def world_to_grid(self, world_pos):
        """Convert world coordinates to grid coordinates"""
        x = int(world_pos.x / self.cell_size)
        y = int(world_pos.z / self.cell_size)  # Unity uses Y-up
        return (x, y)
    
    def grid_to_world(self, grid_pos):
        """Convert grid coordinates to world coordinates"""
        x = grid_pos[0] * self.cell_size + self.cell_size / 2
        z = grid_pos[1] * self.cell_size + self.cell_size / 2
        return Vector3(x, 0, z)  # Unity uses Y-up
```

### With Robotics Systems

```python
# Integration with ROS (Robot Operating System)
class ROSAStarIntegration:
    """Integration with ROS for robot navigation"""
    
    def __init__(self):
        self.map_subscriber = rospy.Subscriber('/map', OccupancyGrid, self.map_callback)
        self.path_publisher = rospy.Publisher('/path', Path, queue_size=10)
        self.pathfinder = AStarPathfinder()
        self.map_data = None
    
    def map_callback(self, msg):
        """Handle incoming map data"""
        self.map_data = {
            'width': msg.info.width,
            'height': msg.info.height,
            'resolution': msg.info.resolution,
            'data': msg.data
        }
    
    def find_robot_path(self, start_pose, goal_pose):
        """Find path for robot navigation"""
        if not self.map_data:
            return None
        
        # Convert poses to grid coordinates
        start_grid = self.pose_to_grid(start_pose)
        goal_grid = self.pose_to_grid(goal_pose)
        
        # Create binary grid (0 = free, 1 = occupied)
        grid = self.create_binary_grid()
        
        # Find path
        path_grid = self.pathfinder.find_path(start_grid, goal_grid)
        
        # Convert to ROS Path message
        path_msg = self.grid_path_to_ros_path(path_grid)
        
        return path_msg
```

## Best Practices

1. **Heuristic Selection**:
   - Choose appropriate heuristic for your environment
   - Ensure heuristic is admissible (never overestimates)
   - Consider using weighted heuristics for speed vs accuracy trade-offs

2. **Data Structures**:
   - Use efficient priority queues (binary heap, Fibonacci heap)
   - Implement proper node comparison and hashing
   - Consider memory pooling for large-scale applications

3. **Performance Optimization**:
   - Use bidirectional search for single-source single-target problems
   - Implement jump point search for grid-based environments
   - Consider hierarchical pathfinding for very large maps

4. **Real-time Applications**:
   - Implement time-bounded search with partial results
   - Use incremental pathfinding for dynamic environments
   - Cache results for frequently queried paths

## Troubleshooting

### Common Issues

1. **Slow Performance**: Use better heuristics, optimize data structures, implement pruning
2. **High Memory Usage**: Use iterative deepening, implement memory bounds, use streaming
3. **Poor Path Quality**: Tune heuristic weights, use more accurate cost functions
4. **No Path Found**: Check connectivity, relax constraints, use alternative algorithms

### Debug Mode

```python
# Debug mode: Enhanced pathfinding debugging
class DebugAStar:
    """A* with enhanced debugging capabilities"""
    
    def __init__(self, grid):
        self.grid = grid
        self.debug_log = []
        self.visualization_data = []
    
    def find_path_with_debug(self, start, goal):
        """Find path with detailed debugging information"""
        # Log search process
        self.debug_log.append(f"Starting search from {start} to {goal}")
        
        # Track search frontier
        frontier_log = []
        
        # Main search loop with logging
        while open_set:
            current = heapq.heappop(open_set)
            
            # Log current state
            frontier_log.append({
                'current': (current.x, current.y),
                'f_cost': current.f_cost,
                'g_cost': current.g_cost,
                'h_cost': current.h_cost,
                'open_set_size': len(open_set)
            })
            
            # Continue search...
        
        # Store visualization data
        self.visualization_data = frontier_log
        
        return path
    
    def generate_debug_report(self):
        """Generate comprehensive debug report"""
        return {
            'search_statistics': self.get_search_stats(),
            'frontier_evolution': self.visualization_data,
            'heuristic_analysis': self.analyze_heuristic(),
            'performance_metrics': self.get_performance_metrics()
        }
```

## Monitoring and Metrics

### Pathfinding Metrics

```yaml
pathfinding_metrics:
  correctness_metrics:
    path_optimality: number     # How close to optimal path
    path_completeness: number   # Whether path reaches goal
    constraint_satisfaction: number # Whether path meets all constraints
    
  performance_metrics:
    average_execution_time: number
    95th_percentile_time: number
    memory_usage_peak: string
    nodes_per_second: number
    
  quality_metrics:
    path_smoothness: number     # How smooth the path is
    obstacle_clearance: number  # Distance from obstacles
    computational_efficiency: number # Efficiency of computation
    
  reliability_metrics:
    success_rate: number        # Percentage of successful pathfinds
    failure_modes: array        # Types of failures encountered
    recovery_effectiveness: number # How well recovery strategies work
```

## Dependencies

- **Data Structures**: Priority queues, hash maps, graph libraries
- **Mathematical Libraries**: Distance calculations, geometric operations
- **Optimization Libraries**: Memory management, performance profiling
- **Integration Frameworks**: Game engines, robotics frameworks, navigation systems
- **Visualization Tools**: Path visualization, debugging tools

## Version History

- **1.0.0**: Initial release with comprehensive A* pathfinding frameworks
- **1.1.0**: Added advanced heuristics and optimization techniques
- **1.2.0**: Enhanced real-time performance and game engine integration
- **1.3.0**: Improved memory management and large-scale pathfinding
- **1.4.0**: Advanced debugging tools and performance monitoring

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.