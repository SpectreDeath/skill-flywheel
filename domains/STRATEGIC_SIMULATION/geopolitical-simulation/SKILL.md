---
Domain: strategic_simulation
Version: 1.0.0
Complexity: Advanced
Type: Process
Category: Simulation
Estimated Execution Time: 100ms - 5 minutes
name: geopolitical-simulation
---

## Description

Geopolitical agent simulation framework based on Strategify's Clojure implementation. Provides timeline branching for counterfactual analysis, core.logic (miniKanren) for Prolog-style diplomatic rules, and real-world map-based agent positioning.

## Purpose

To build geopolitical simulations where agents represent actors (nations, factions) on geographic maps, make strategic decisions based on game theory, and explore alternative timelines through branching.

## When to Use

- Simulating international conflicts and diplomacy
- Exploring "what-if" scenarios in geopolitical events
- Modeling alliance formation and rivalries
- Testing strategic decisions under uncertainty

## When NOT to Use

- Simple two-player games (use game-theory-simulation)
- Economic simulations without geographic component
- Abstract strategy without real-world grounding

## Input Format

```yaml
geo_request:
  action: "create_state|branch_timeline|decide|analyze"
  state: object           # Current game state
  agents: array           # List of actors
  map_file: string       # GeoJSON map path
  scenario: string        # "ukraine", "middle_east", "south_china"
```

## Output Format

```yaml
geo_result:
  state: object           # Updated state
  timeline_id: string     # For branching
  decision: object        # Agent decision with reasoning
  timelines: array        # Multiple timeline branches
```

## Capabilities

### 1. Immutable Agent State (from strategify-clj)

```clojure
(defrecord Agent
    [id strategy resources history beliefs tom-level])

(defn create-agent
  [id strategy-type resources]
  (->Agent id strategy-type resources [] []))

(defn update-belief [agent belief]
  (update agent :beliefs conj belief))
```

### 2. Timeline Branching (Counterfactual)

```python
class Timeline:
    """Timeline branching for counterfactual analysis."""
    
    def branch(self, state, move):
        """Create new timeline without modifying original."""
        return apply_move(state, move)
    
    def branch_multiple(self, state, possible_moves):
        """Branch multiple possible futures."""
        return [apply_move(state, m) for m in possible_moves]
    
    def compare_outcomes(self, timelines, scorer):
        """Compare outcomes across branches."""
        return [scorer(t) for t in timelines]
```

### 3. core.logic Diplomatic Rules (miniKanren)

```python
from functools import partial

# Define relations (like Prolog's defrel)
def strategy_decides(player, strategy, action):
    """Relation: player uses strategy to determine action."""
    pass

def dominates(dominator, dominated):
    """Relation: dominator has advantage over dominated."""
    pass

def alliance(player1, player2):
    """Relation: player1 and player2 have alliance."""
    pass

# Rules using logic programming
def hawk_dominates(player, opp, resources):
    """Rule: hawk with more resources dominates."""
    return player.get("strategy") == "hawk" and resources > opp.get("resources")

def alliance_formed(p1, p2, diplomatic_history):
    """Rule: alliance forms if sufficient diplomatic contact."""
    return any(d.get("type") == "alliance" for d in diplomatic_history)
```

### 4. Geographic Map Integration

```python
import json
import folium

class GeoMap:
    """Geographic map with agent positions."""
    
    def __init__(self, geojson_path: str):
        with open(geojson_path) as f:
            self.data = json.load(f)
        self.agents = {}
    
    def place_agent(self, agent_id, region_id):
        """Place agent on map region."""
        self.agents[agent_id] = region_id
    
    def get_neighbors(self, region_id):
        """Get neighboring regions."""
        # Find region in GeoJSON and return adjacencies
        pass
    
    def render(self):
        """Render interactive Folium map."""
        m = folium.Map()
        # Add agent markers
        return m
```

### 5. Influence Maps & Spatial Reasoning

```python
def bfs_influence(start_region, influence_map, depth):
    """BFS-based spatial reasoning."""
    visited = {start_region}
    queue = [(start_region, 0)]
    
    while queue:
        region, d = queue.pop(0)
        if d >= depth:
            continue
        for neighbor in influence_map.get(region, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, d + 1))
    
    return visited

def escalation_contagion(regions, tension_levels):
    """Model how escalation spreads geographically."""
    # Adjacent high-tension regions increase local tension
    pass

def spatial_autocorrelation(regions, values):
    """Calculate Moran's I for spatial patterns."""
    pass
```

### 6. Payoff Matrix (Hawk-Dove variant)

```python
PAYOFF_MATRIX = {
    "hawk": {"hawk": -25, "dove": 50, "retreat": 0},
    "dove": {"hawk": 0, "dove": 25, "retreat": 10},
    "retreat": {"hawk": -10, "dove": 5, "retreat": 15},
}

def get_payoff(action, opponent_action):
    return PAYOFF_MATRIX.get(action, {}).get(opponent_action, 0)
```

### 7. Scenario Presets

```python
SCENARIOS = {
    "ukraine": {
        "description": "Ukraine Crisis Simulation",
        "regions": ["ukraine", "russia", "belarus", "poland"],
        "initial_tension": {"ukraine": 80, "russia": 70, "belarus": 60},
    },
    "middle_east": {
        "description": "Middle East Regional",
        "regions": ["israel", "iran", "saudi_arabia", "syria", "iraq"],
        "initial_tension": {"israel": 75, "iran": 85},
    },
    "south_china": {
        "description": "South China Sea",
        "regions": ["china", "vietnam", "philippines", "taiwan"],
        "naval_tension": True,
    },
}
```

## Implementation Notes

- Use immutable state (like Clojure's persistent data structures)
- Track history for each agent for pattern analysis
- Support multiple timeline branches with unique IDs
- Use networkx for alliance graph analysis

## Dependencies

```python
# Core
networkx  # Alliance graphs
folium    # Map visualization

# Optional
# numpy, scipy  # Spatial statistics
```

## Best Practices

1. **Immutable State**: Never modify state in-place, always return new state
2. **Timeline IDs**: Use UUIDs for unique timeline identification
3. **History Tracking**: Keep complete history for analysis
4. **Map Resolution**: Use appropriate GeoJSON detail level

## Error Handling

- Unknown region → add to unclassified
- Invalid strategy → default to "neutral"
- Timeline limit exceeded → prune oldest

## Version History

- **1.0.0**: Initial geopolitical simulation based on Strategify

## Constraints

- MUST use immutable state updates
- ALWAYS generate unique timeline IDs
- STOP if exceeds 100 simultaneous timelines