---
Domain: formal_methods
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: model-checking-frameworks
---



## Description

Automatically designs and implements optimal model checking frameworks for automated verification of finite-state systems, temporal logic model checking, and system property verification. This skill provides comprehensive frameworks for state space exploration, property specification, counterexample generation, and integration with formal verification workflows.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **State Space Exploration**: Design and implement efficient state space exploration algorithms for model checking
- **Temporal Logic Verification**: Create frameworks for verifying temporal logic properties (LTL, CTL, CTL*)
- **Counterexample Generation**: Implement counterexample generation and analysis for failed properties
- **Symbolic Model Checking**: Develop symbolic model checking using BDDs and SAT/SMT solvers
- **Bounded Model Checking**: Create bounded model checking frameworks for bug detection
- **Abstraction and Refinement**: Implement abstraction techniques and counterexample-guided abstraction refinement (CEGAR)
- **Performance Optimization**: Optimize model checking performance through state compression and parallelization

## Usage Examples

### Model Checking Framework for Concurrent Systems

```python
"""
Model Checking Framework for Concurrent Systems
"""

from typing import List, Set, Dict, Tuple, Optional, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod
import networkx as nx
from z3 import *

@dataclass
class State:
    """System state representation"""
    variables: Dict[str, int]
    process_states: Dict[str, str]
    
    def __hash__(self):
        return hash((tuple(self.variables.items()), 
                    tuple(self.process_states.items())))
    
    def __eq__(self, other):
        return (self.variables == other.variables and 
                self.process_states == other.process_states)

@dataclass
class Transition:
    """State transition representation"""
    source: State
    target: State
    action: str

class TemporalLogicFormula(ABC):
    """Abstract base class for temporal logic formulas"""
    
    @abstractmethod
    def evaluate(self, state: State, model: 'ModelChecker') -> bool:
        pass
    
    @abstractmethod
    def to_string(self) -> str:
        pass

class AtomicProposition(TemporalLogicFormula):
    """Atomic proposition in temporal logic"""
    
    def __init__(self, prop: str):
        self.prop = prop
    
    def evaluate(self, state: State, model: 'ModelChecker') -> bool:
        return model.evaluate_proposition(self.prop, state)
    
    def to_string(self) -> str:
        return self.prop

class AndFormula(TemporalLogicFormula):
    """Logical AND in temporal logic"""
    
    def __init__(self, left: TemporalLogicFormula, right: TemporalLogicFormula):
        self.left = left
        self.right = right
    
    def evaluate(self, state: State, model: 'ModelChecker') -> bool:
        return (self.left.evaluate(state, model) and 
                self.right.evaluate(state, model))
    
    def to_string(self) -> str:
        return f"({self.left.to_string()} && {self.right.to_string()})"

class OrFormula(TemporalLogicFormula):
    """Logical OR in temporal logic"""
    
    def __init__(self, left: TemporalLogicFormula, right: TemporalLogicFormula):
        self.left = left
        self.right = right
    
    def evaluate(self, state: State, model: 'ModelChecker') -> bool:
        return (self.left.evaluate(state, model) or 
                self.right.evaluate(state, model))
    
    def to_string(self) -> str:
        return f"({self.left.to_string()} || {self.right.to_string()})"

class NotFormula(TemporalLogicFormula):
    """Logical NOT in temporal logic"""
    
    def __init__(self, formula: TemporalLogicFormula):
        self.formula = formula
    
    def evaluate(self, state: State, model: 'ModelChecker') -> bool:
        return not self.formula.evaluate(state, model)
    
    def to_string(self) -> str:
        return f"!({self.formula.to_string()})"

class AlwaysFormula(TemporalLogicFormula):
    """Always (Globally) operator in temporal logic"""
    
    def __init__(self, formula: TemporalLogicFormula):
        self.formula = formula
    
    def evaluate(self, state: State, model: 'ModelChecker') -> bool:
        return model.check_always(state, self.formula)
    
    def to_string(self) -> str:
        return f"G({self.formula.to_string()})"

class EventuallyFormula(TemporalLogicFormula):
    """Eventually (Finally) operator in temporal logic"""
    
    def __init__(self, formula: TemporalLogicFormula):
        self.formula = formula
    
    def evaluate(self, state: State, model: 'ModelChecker') -> bool:
        return model.check_eventually(state, self.formula)
    
    def to_string(self) -> str:
        return f"F({self.formula.to_string()})"

class UntilFormula(TemporalLogicFormula):
    """Until operator in temporal logic"""
    
    def __init__(self, left: TemporalLogicFormula, right: TemporalLogicFormula):
        self.left = left
        self.right = right
    
    def evaluate(self, state: State, model: 'ModelChecker') -> bool:
        return model.check_until(state, self.left, self.right)
    
    def to_string(self) -> str:
        return f"({self.left.to_string()} U {self.right.to_string()})"

class ModelChecker:
    """Main model checking framework"""
    
    def __init__(self):
        self.states: Set[State] = set()
        self.transitions: List[Transition] = []
        self.initial_states: Set[State] = set()
        self.graph = nx.DiGraph()
        
    def add_state(self, state: State):
        """Add a state to the model"""
        self.states.add(state)
        self.graph.add_node(state)
        
    def add_transition(self, source: State, target: State, action: str):
        """Add a transition between states"""
        if source not in self.states or target not in self.states:
            raise ValueError("States must be added before transitions")
        
        transition = Transition(source, target, action)
        self.transitions.append(transition)
        self.graph.add_edge(source, target, action=action)
        
    def set_initial_states(self, states: Set[State]):
        """Set initial states"""
        self.initial_states = states
        
    def evaluate_proposition(self, prop: str, state: State) -> bool:
        """Evaluate atomic proposition in a state"""
        # Parse proposition and evaluate against state
        if prop.startswith("var_"):
            var_name = prop[4:]
            if var_name in state.variables:
                return state.variables[var_name] > 0
        elif prop.startswith("proc_"):
            proc_name = prop[5:]
            if proc_name in state.process_states:
                return state.process_states[proc_name] == "running"
        return False
        
    def check_safety_property(self, formula: TemporalLogicFormula) -> Tuple[bool, Optional[List[State]]]:
        """Check safety property (always formula)"""
        for state in self.states:
            if not formula.evaluate(state, self):
                # Find counterexample path
                counterexample = self.find_counterexample_path(state, formula)
                return False, counterexample
        return True, None
        
    def check_liveness_property(self, formula: TemporalLogicFormula) -> Tuple[bool, Optional[List[State]]]:
        """Check liveness property (eventually formula)"""
        for state in self.initial_states:
            if not formula.evaluate(state, self):
                # Find counterexample path
                counterexample = self.find_counterexample_path(state, formula)
                return False, counterexample
        return True, None
        
    def check_always(self, state: State, formula: TemporalLogicFormula) -> bool:
        """Check always (Globally) property"""
        visited = set()
        
        def dfs(current_state: State) -> bool:
            if current_state in visited:
                return True
            visited.add(current_state)
            
            if not formula.evaluate(current_state, self):
                return False
                
            for neighbor in self.graph.successors(current_state):
                if not dfs(neighbor):
                    return False
            return True
            
        return dfs(state)
        
    def check_eventually(self, state: State, formula: TemporalLogicFormula) -> bool:
        """Check eventually (Finally) property"""
        visited = set()
        
        def dfs(current_state: State) -> bool:
            if current_state in visited:
                return False
            visited.add(current_state)
            
            if formula.evaluate(current_state, self):
                return True
                
            for neighbor in self.graph.successors(current_state):
                if dfs(neighbor):
                    return True
            return False
            
        return dfs(state)
        
    def check_until(self, state: State, left: TemporalLogicFormula, right: TemporalLogicFormula) -> bool:
        """Check until property"""
        visited = set()
        
        def dfs(current_state: State) -> bool:
            if current_state in visited:
                return False
            visited.add(current_state)
            
            if right.evaluate(current_state, self):
                return True
                
            if not left.evaluate(current_state, self):
                return False
                
            for neighbor in self.graph.successors(current_state):
                if dfs(neighbor):
                    return True
            return False
            
        return dfs(state)
        
    def find_counterexample_path(self, start_state: State, 
                               formula: TemporalLogicFormula) -> List[State]:
        """Find counterexample path for failed property"""
        path = [start_state]
        
        def dfs(current_state: State) -> bool:
            if not formula.evaluate(current_state, self):
                return True
                
            for neighbor in self.graph.successors(current_state):
                path.append(neighbor)
                if dfs(neighbor):
                    return True
                path.pop()
            return False
            
        dfs(start_state)
        return path
        
    def symbolic_model_checking(self, formula: TemporalLogicFormula) -> bool:
        """Symbolic model checking using Z3"""
        solver = Solver()
        
        # Create symbolic variables for states
        state_vars = {}
        for state in self.states:
            state_vars[state] = Bool(f"state_{hash(state)}")
            
        # Add initial state constraints
        for state in self.initial_states:
            solver.add(state_vars[state])
            
        # Add transition constraints
        for transition in self.transitions:
            solver.add(Implies(state_vars[transition.source], 
                             state_vars[transition.target]))
                             
        # Check property
        return solver.check() == sat

# Example usage
def example_concurrent_system():
    """Example: Dining Philosophers Problem"""
    model = ModelChecker()
    
    # Create states for 2 philosophers
    states = []
    for p1_state in ["thinking", "eating", "hungry"]:
        for p1_fork in [0, 1]:
            for p2_state in ["thinking", "eating", "hungry"]:
                for p2_fork in [0, 1]:
                    state = State(
                        variables={"fork1": p1_fork, "fork2": p2_fork},
                        process_states={"phil1": p1_state, "phil2": p2_state}
                    )
                    states.append(state)
                    model.add_state(state)
    
    # Set initial states (both thinking, no forks)
    initial = State(variables={"fork1": 0, "fork2": 0}, 
                   process_states={"phil1": "thinking", "phil2": "thinking"})
    model.set_initial_states({initial})
    
    # Add transitions (simplified)
    # Philosopher 1 picks up fork 1
    for state in states:
        if (state.process_states["phil1"] == "hungry" and 
            state.variables["fork1"] == 0 and
            state.variables["fork2"] == 0):
            
            new_state = State(
                variables={"fork1": 1, "fork2": 0},
                process_states={"phil1": "eating", "phil2": state.process_states["phil2"]}
            )
            if new_state in model.states:
                model.add_transition(state, new_state, "phil1_picks_fork1")
    
    # Define properties
    mutual_exclusion = NotFormula(
        AndFormula(
            AtomicProposition("proc_phil1"),
            AtomicProposition("proc_phil2")
        )
    )
    
    # Check property
    result, counterexample = model.check_safety_property(mutual_exclusion)
    print(f"Mutual exclusion property: {'Holds' if result else 'Violated'}")
    
    if counterexample:
        print("Counterexample path:")
        for i, state in enumerate(counterexample):
            print(f"  Step {i}: {state.process_states}")
    
    return model

if __name__ == "__main__":
    example_concurrent_system()
```

### Bounded Model Checking with SAT Solvers

```python
"""
Bounded Model Checking Framework using SAT Solvers
"""

from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
from z3 import *

@dataclass
class BMCState:
    """State representation for bounded model checking"""
    variables: Dict[str, int]
    step: int
    
    def __hash__(self):
        return hash((tuple(self.variables.items()), self.step))
    
    def __eq__(self, other):
        return (self.variables == other.variables and 
                self.step == other.step)

class BoundedModelChecker:
    """Bounded Model Checking framework"""
    
    def __init__(self, bound: int):
        self.bound = bound
        self.solver = Solver()
        self.state_vars: Dict[int, Dict[str, Int]] = {}
        self.transition_constraints: List[BoolRef] = []
        
    def add_state_variables(self, step: int, variables: List[str]):
        """Add state variables for a specific step"""
        self.state_vars[step] = {var: Int(f"{var}_{step}") for var in variables}
        
    def add_initial_constraints(self, initial_values: Dict[str, int]):
        """Add initial state constraints"""
        for var, value in initial_values.items():
            self.solver.add(self.state_vars[0][var] == value)
            
    def add_transition_relation(self, step: int, 
                              transition_func: callable):
        """Add transition relation constraints"""
        current_vars = self.state_vars[step]
        next_vars = self.state_vars[step + 1]
        
        constraints = transition_func(current_vars, next_vars)
        self.transition_constraints.extend(constraints)
        self.solver.add(constraints)
        
    def add_property_constraint(self, step: int, 
                              property_func: callable):
        """Add property violation constraint"""
        vars_at_step = self.state_vars[step]
        violation = property_func(vars_at_step)
        self.solver.add(violation)
        
    def check_property(self, property_func: callable) -> Tuple[bool, Optional[List[Dict[str, int]]]]:
        """Check if property can be violated within bound"""
        
        # Add property violation constraints for all steps
        for step in range(self.bound + 1):
            self.add_property_constraint(step, property_func)
            
        # Check satisfiability
        result = self.solver.check()
        
        if result == sat:
            # Property can be violated
            model = self.solver.model()
            counterexample = self.extract_counterexample(model)
            return False, counterexample
        else:
            # Property holds within bound
            return True, None
            
    def extract_counterexample(self, model: ModelRef) -> List[Dict[str, int]]:
        """Extract counterexample from SAT model"""
        counterexample = []
        
        for step in range(self.bound + 1):
            step_values = {}
            for var, z3_var in self.state_vars[step].items():
                value = model.evaluate(z3_var, model_completion=True)
                step_values[var] = value.as_long()
            counterexample.append(step_values)
            
        return counterexample
        
    def add_invariant(self, invariant_func: callable):
        """Add invariant constraint"""
        for step in range(self.bound + 1):
            vars_at_step = self.state_vars[step]
            invariant = invariant_func(vars_at_step)
            self.solver.add(invariant)

# Example: Bounded Model Checking for Mutual Exclusion
def example_bmc_mutual_exclusion():
    """Example: Bounded Model Checking for Mutual Exclusion"""
    
    bmc = BoundedModelChecker(bound=10)
    
    # Add state variables for each step
    for step in range(11):
        bmc.add_state_variables(step, ["pc1", "pc2", "turn"])
        
    # Initial state: both processes at non-critical section, turn = 1
    bmc.add_initial_constraints({"pc1": 0, "pc2": 0, "turn": 1})
    
    # Transition relation for Peterson's algorithm
    def peterson_transition(current_vars, next_vars):
        constraints = []
        
        # Process 1 transitions
        constraints.append(Or(
            # Stay in non-critical section
            And(current_vars["pc1"] == 0, next_vars["pc1"] == 0),
            # Enter critical section (if turn allows)
            And(current_vars["pc1"] == 0, current_vars["turn"] == 1, 
                next_vars["pc1"] == 1, next_vars["turn"] == 2),
            # Exit critical section
            And(current_vars["pc1"] == 1, next_vars["pc1"] == 0, 
                next_vars["turn"] == 2)
        ))
        
        # Process 2 transitions
        constraints.append(Or(
            # Stay in non-critical section
            And(current_vars["pc2"] == 0, next_vars["pc2"] == 0),
            # Enter critical section (if turn allows)
            And(current_vars["pc2"] == 0, current_vars["turn"] == 2, 
                next_vars["pc2"] == 1, next_vars["turn"] == 1),
            # Exit critical section
            And(current_vars["pc2"] == 1, next_vars["pc2"] == 0, 
                next_vars["turn"] == 1)
        ))
        
        return constraints
        
    # Add transition relations
    for step in range(10):
        bmc.add_transition_relation(step, peterson_transition)
        
    # Property: Never both in critical section
    def mutual_exclusion_property(vars_at_step):
        return Not(And(vars_at_step["pc1"] == 1, vars_at_step["pc2"] == 1))
        
    # Check property
    result, counterexample = bmc.check_property(mutual_exclusion_property)
    
    print(f"Mutual exclusion property: {'Holds' if result else 'Violated'}")
    
    if counterexample:
        print("Counterexample:")
        for i, state in enumerate(counterexample):
            print(f"  Step {i}: pc1={state['pc1']}, pc2={state['pc2']}, turn={state['turn']}")
    
    return bmc

if __name__ == "__main__":
    example_bmc_mutual_exclusion()
```

### Counterexample-Guided Abstraction Refinement (CEGAR)

```python
"""
Counterexample-Guided Abstraction Refinement (CEGAR) Framework
"""

from typing import List, Dict, Set, Tuple, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
import networkx as nx

@dataclass
class AbstractState:
    """Abstract state representation"""
    abstract_id: int
    concrete_states: Set['ConcreteState']
    
class ConcreteState:
    """Concrete state representation"""
    def __init__(self, variables: Dict[str, int]):
        self.variables = variables
        
    def __hash__(self):
        return hash(tuple(self.variables.items()))
        
    def __eq__(self, other):
        return self.variables == other.variables

class AbstractionFunction(ABC):
    """Abstract base class for abstraction functions"""
    
    @abstractmethod
    def abstract(self, concrete_state: ConcreteState) -> AbstractState:
        pass
        
    @abstractmethod
    def refine(self, abstract_state: AbstractState, 
               counterexample: List[ConcreteState]) -> List[AbstractState]:
        pass

class PredicateAbstraction(AbstractionFunction):
    """Predicate-based abstraction"""
    
    def __init__(self, predicates: List[Callable[[ConcreteState], bool]]):
        self.predicates = predicates
        self.predicate_cache: Dict[ConcreteState, Tuple[bool, ...]] = {}
        
    def abstract(self, concrete_state: ConcreteState) -> AbstractState:
        """Abstract concrete state to abstract state"""
        if concrete_state in self.predicate_cache:
            predicate_values = self.predicate_cache[concrete_state]
        else:
            predicate_values = tuple(pred(concrete_state) for pred in self.predicates)
            self.predicate_cache[concrete_state] = predicate_values
            
        # Create abstract state based on predicate values
        abstract_id = hash(predicate_values)
        return AbstractState(abstract_id, {concrete_state})
        
    def refine(self, abstract_state: AbstractState, 
               counterexample: List[ConcreteState]) -> List[AbstractState]:
        """Refine abstraction based on counterexample"""
        new_abstract_states = []
        
        # Group concrete states by new predicate evaluations
        groups = {}
        for concrete_state in abstract_state.concrete_states:
            # Evaluate all predicates on this state
            predicate_values = tuple(pred(concrete_state) for pred in self.predicates)
            if predicate_values not in groups:
                groups[predicate_values] = set()
            groups[predicate_values].add(concrete_state)
            
        # Create new abstract states for each group
        for i, (predicate_values, concrete_states) in enumerate(groups.items()):
            new_abstract_id = hash((abstract_state.abstract_id, i))
            new_abstract_state = AbstractState(new_abstract_id, concrete_states)
            new_abstract_states.append(new_abstract_state)
            
        return new_abstract_states

class CEGARFramework:
    """Counterexample-Guided Abstraction Refinement framework"""
    
    def __init__(self, abstraction: AbstractionFunction):
        self.abstraction = abstraction
        self.concrete_model = None
        self.abstract_model = None
        self.refinement_count = 0
        
    def set_concrete_model(self, concrete_model):
        """Set the concrete model to verify"""
        self.concrete_model = concrete_model
        
    def build_abstract_model(self):
        """Build abstract model from concrete model"""
        if not self.concrete_model:
            raise ValueError("Concrete model not set")
            
        # Abstract all concrete states
        abstract_states = {}
        for concrete_state in self.concrete_model.states:
            abstract_state = self.abstraction.abstract(concrete_state)
            if abstract_state.abstract_id not in abstract_states:
                abstract_states[abstract_state.abstract_id] = abstract_state
            else:
                abstract_states[abstract_state.abstract_id].concrete_states.update(
                    abstract_state.concrete_states)
                    
        # Build abstract transitions
        abstract_transitions = []
        for transition in self.concrete_model.transitions:
            source_abstract = self.abstraction.abstract(transition.source)
            target_abstract = self.abstraction.abstract(transition.target)
            
            if source_abstract.abstract_id != target_abstract.abstract_id:
                abstract_transitions.append((source_abstract.abstract_id, 
                                           target_abstract.abstract_id, 
                                           transition.action))
                                           
        self.abstract_model = {
            'states': abstract_states,
            'transitions': abstract_transitions,
            'initial_states': {self.abstraction.abstract(s).abstract_id 
                             for s in self.concrete_model.initial_states}
        }
        
    def verify_abstract_property(self, property_formula):
        """Verify property on abstract model"""
        # Simple model checking on abstract model
        # This would typically use a model checker
        
        # For demonstration, we'll do a basic reachability check
        reachable = set(self.abstract_model['initial_states'])
        worklist = list(reachable)
        
        while worklist:
            current = worklist.pop()
            for source, target, action in self.abstract_model['transitions']:
                if source == current and target not in reachable:
                    reachable.add(target)
                    worklist.append(target)
                    
        # Check if any reachable state violates the property
        for state_id in reachable:
            abstract_state = self.abstract_model['states'][state_id]
            # Check if any concrete state in this abstract state violates property
            for concrete_state in abstract_state.concrete_states:
                if not property_formula.evaluate(concrete_state, self.concrete_model):
                    return False, self.find_concrete_counterexample(concrete_state)
                    
        return True, None
        
    def find_concrete_counterexample(self, violating_state) -> List[ConcreteState]:
        """Find concrete counterexample path"""
        # This would typically use a concrete model checker
        # For demonstration, return a simple path
        return [violating_state]
        
    def refine_abstraction(self, counterexample: List[ConcreteState]):
        """Refine abstraction based on counterexample"""
        self.refinement_count += 1
        
        # Find abstract state containing counterexample
        for abstract_id, abstract_state in self.abstract_model['states'].items():
            if any(concrete in abstract_state.concrete_states 
                   for concrete in counterexample):
                
                # Refine this abstract state
                new_abstract_states = self.abstraction.refine(abstract_state, counterexample)
                
                # Update abstract model
                del self.abstract_model['states'][abstract_id]
                for new_abstract in new_abstract_states:
                    self.abstract_model['states'][new_abstract.abstract_id] = new_abstract
                    
                break
                
    def verify_property(self, property_formula, max_refinements: int = 10):
        """Main CEGAR verification loop"""
        
        while self.refinement_count < max_refinements:
            # Build abstract model
            self.build_abstract_model()
            
            # Verify on abstract model
            result, counterexample = self.verify_abstract_property(property_formula)
            
            if result:
                # Property holds on abstract model
                # Check if abstraction is precise enough
                if self.is_abstraction_precise():
                    return True, None
                else:
                    # Need more refinement
                    continue
            else:
                # Property violated on abstract model
                # Check if counterexample is spurious
                if self.is_spurious_counterexample(counterexample):
                    # Refine abstraction
                    self.refine_abstraction(counterexample)
                else:
                    # Real counterexample found
                    return False, counterexample
                    
        # Max refinements reached
        return None, "Max refinements reached"
        
    def is_abstraction_precise(self) -> bool:
        """Check if abstraction is precise enough"""
        # This would check if abstract model is bisimilar to concrete model
        return False
        
    def is_spurious_counterexample(self, counterexample: List[ConcreteState]) -> bool:
        """Check if counterexample is spurious"""
        # This would check if counterexample exists in concrete model
        return True

# Example usage
def example_cegar():
    """Example: CEGAR for mutual exclusion"""
    
    # Define predicates for abstraction
    def has_fork1(state: ConcreteState):
        return state.variables.get("fork1", 0) > 0
        
    def has_fork2(state: ConcreteState):
        return state.variables.get("fork2", 0) > 0
        
    def is_eating(state: ConcreteState):
        return state.variables.get("eating", False)
        
    predicates = [has_fork1, has_fork2, is_eating]
    abstraction = PredicateAbstraction(predicates)
    
    # Create CEGAR framework
    cegar = CEGARFramework(abstraction)
    
    # Set concrete model (would be created from system)
    # cegar.set_concrete_model(concrete_model)
    
    # Define property to verify
    # property_formula = ...
    
    # Verify property
    # result, counterexample = cegar.verify_property(property_formula)
    
    print("CEGAR framework initialized with predicates:")
    for i, pred in enumerate(predicates):
        print(f"  {i+1}. {pred.__name__}")
        
    return cegar

if __name__ == "__main__":
    example_cegar()
```

## Input Format

### Model Checking Specification

```yaml
model_checking_specification:
  system_name: string             # Name of the system to verify
  model_type: "explicit|symbolic|bounded"
  
  states:
    - state_id: string
      variables: object           # State variables and values
      properties: array           # Properties holding in this state
      
    - state_id: string
      variables: object
      properties: array
  
  transitions:
    - source_state: string
      target_state: string
      action: string              # Action causing transition
      guard: string               # Guard condition (optional)
      
    - source_state: string
      target_state: string
      action: string
      guard: string
  
  initial_states: array           # List of initial state IDs
  properties:
    - property_name: string
      property_type: "safety|liveness"
      temporal_logic: "LTL|CTL|CTL*"
      formula: string             # Temporal logic formula
      
    - property_name: string
      property_type: "safety|liveness"
      temporal_logic: "LTL|CTL|CTL*"
      formula: string
  
  verification_config:
    model_checker: "nuXmv|SPIN|PRISM|custom"
    abstraction_enabled: boolean
    counterexample_generation: boolean
    parallel_verification: boolean
```

### Temporal Logic Formula Specification

```yaml
temporal_logic_formula:
  formula_type: "atomic|and|or|not|always|eventually|until"
  
  if formula_type == "atomic":
    proposition: string           # Atomic proposition
    
  if formula_type in ["and", "or", "until"]:
    left_operand: temporal_logic_formula
    right_operand: temporal_logic_formula
    
  if formula_type == "not":
    operand: temporal_logic_formula
    
  if formula_type in ["always", "eventually"]:
    operand: temporal_logic_formula
```

## Output Format

### Model Checking Results

```yaml
model_checking_results:
  system_name: string
  verification_timestamp: timestamp
  
  verification_results:
    - property_name: string
      result: "verified|violated|unknown"
      verification_time: number
      states_explored: number
      memory_usage: string
      
      if result == "violated":
        counterexample:
          type: "finite|infinite"
          path: array               # Counterexample execution path
          violating_state: string
          explanation: string
      
      if result == "unknown":
        reason: string              # Reason for unknown result
        suggestions: array          # Suggestions for resolution
  
  performance_metrics:
    total_verification_time: number
    average_property_time: number
    peak_memory_usage: string
    state_space_size: number
    transition_count: number
  
  abstraction_metrics:
    abstraction_level: number       # Level of abstraction used
    refinement_iterations: number   # Number of CEGAR iterations
    abstract_states_count: number
    concrete_states_count: number
```

### Counterexample Analysis

```yaml
counterexample_analysis:
  counterexample_id: string
  property_violated: string
  counterexample_type: "finite|infinite"
  
  if counterexample_type == "finite":
    execution_path:
      - state: string
        variables: object
        action: string              # Action taken
        time: number                # Time step
        
      - state: string
        variables: object
        action: string
        time: number
  
  if counterexample_type == "infinite":
    finite_prefix:
      - state: string
        variables: object
        action: string
        time: number
        
    loop:
      - state: string
        variables: object
        action: string
        time: number
  
  analysis:
    root_cause: string              # Root cause of violation
    affected_components: array      # Components involved
    suggested_fixes: array          # Suggested fixes
    impact_assessment: string       # Impact of the violation
```

## Configuration Options

### Model Checking Algorithms

```yaml
model_checking_algorithms:
  explicit_state:
    description: "Explicit state space exploration"
    best_for: ["small_systems", "detailed_analysis"]
    memory_usage: "high"
    time_complexity: "exponential"
    
  symbolic_model_checking:
    description: "Symbolic model checking with BDDs"
    best_for: ["medium_systems", "combinatorial_explosion_avoidance"]
    memory_usage: "depends_on_bdd_size"
    time_complexity: "variable"
    
  bounded_model_checking:
    description: "Bounded model checking with SAT/SMT"
    best_for: ["bug_detection", "large_systems"]
    memory_usage: "moderate"
    time_complexity: "polynomial_in_bound"
    
  probabilistic_model_checking:
    description: "Probabilistic model checking"
    best_for: ["stochastic_systems", "performance_analysis"]
    memory_usage: "high"
    time_complexity: "exponential"
```

### Abstraction Techniques

```yaml
abstraction_techniques:
  predicate_abstraction:
    description: "Abstraction based on predicates"
    best_for: ["software_verification", "infinite_state_systems"]
    precision: "high"
    complexity: "medium"
    
  data_abstraction:
    description: "Abstraction of data values"
    best_for: ["data_intensive_systems", "numeric_properties"]
    precision: "medium"
    complexity: "low"
    
  control_flow_abstraction:
    description: "Abstraction of control flow"
    best_for: ["concurrent_systems", "protocol_verification"]
    precision: "medium"
    complexity: "low"
    
  counterexample_guided_refinement:
    description: "CEGAR - counterexample-guided abstraction refinement"
    best_for: ["complex_systems", "precise_verification"]
    precision: "very_high"
    complexity: "high"
```

## Error Handling

### Model Checking Failures

```yaml
model_checking_failures:
  state_space_explosion:
    retry_strategy: "abstraction_refinement"
    max_retries: 3
    fallback_action: "bounded_model_checking"
  
  timeout_exceeded:
    retry_strategy: "incremental_verification"
    max_retries: 2
    fallback_action: "statistical_model_checking"
  
  memory_exhaustion:
    retry_strategy: "disk_based_algorithms"
    max_retries: 2
    fallback_action: "distributed_model_checking"
  
  counterexample_too_large:
    retry_strategy: "counterexample_simplification"
    max_retries: 1
    fallback_action: "manual_analysis"
```

### Abstraction Errors

```yaml
abstraction_errors:
  abstraction_too_coarse:
    detection_strategy: "counterexample_analysis"
    recovery_strategy: "refinement"
    escalation: "manual_abstraction_design"
  
  abstraction_too_precise:
    detection_strategy: "performance_monitoring"
    recovery_strategy: "coarsening"
    escalation: "abstraction_redesign"
  
  abstraction_inconsistency:
    detection_strategy: "consistency_checking"
    recovery_strategy: "abstraction_reconstruction"
    escalation: "expert_intervention"
```

## Performance Optimization

### State Space Optimization

```python
# Optimization: State compression
class StateCompressor:
    """Compress state representations for memory efficiency"""
    
    def __init__(self):
        self.state_cache = {}
        self.reverse_cache = {}
        
    def compress_state(self, state):
        """Compress state to smaller representation"""
        if state in self.state_cache:
            return self.state_cache[state]
            
        compressed = self._compute_compressed_representation(state)
        self.state_cache[state] = compressed
        self.reverse_cache[compressed] = state
        return compressed
        
    def decompress_state(self, compressed_state):
        """Decompress state from compressed representation"""
        return self.reverse_cache.get(compressed_state, None)

# Optimization: Incremental state exploration
class IncrementalExplorer:
    """Incrementally explore state space"""
    
    def __init__(self, model_checker):
        self.model_checker = model_checker
        self.explored_states = set()
        self.frontier = []
        
    def explore_incrementally(self, max_states: int):
        """Explore state space incrementally"""
        states_explored = 0
        
        while self.frontier and states_explored < max_states:
            current_state = self.frontier.pop(0)
            
            if current_state in self.explored_states:
                continue
                
            self.explored_states.add(current_state)
            states_explored += 1
            
            # Explore successors
            for successor in self.model_checker.get_successors(current_state):
                if successor not in self.explored_states:
                    self.frontier.append(successor)
                    
        return states_explored

# Optimization: Parallel state exploration
from concurrent.futures import ThreadPoolExecutor

class ParallelExplorer:
    """Parallel state space exploration"""
    
    def __init__(self, num_workers: int):
        self.num_workers = num_workers
        
    def explore_parallel(self, initial_states, transition_function):
        """Explore state space in parallel"""
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = []
            
            for state in initial_states:
                future = executor.submit(self._explore_from_state, 
                                       state, transition_function)
                futures.append(future)
                
            results = [future.result() for future in futures]
            return self._merge_results(results)
            
    def _explore_from_state(self, state, transition_function):
        """Explore from a single state"""
        explored = {state}
        frontier = [state]
        
        while frontier:
            current = frontier.pop(0)
            for successor in transition_function(current):
                if successor not in explored:
                    explored.add(successor)
                    frontier.append(successor)
                    
        return explored
```

### Verification Optimization

```yaml
verification_optimizations:
  symmetry_reduction:
    technique: "automorphism_detection"
    reduction_factor: "exponential_in_best_case"
    applicability: "symmetric_systems"
    
  partial_order_reduction:
    technique: "ample_sets"
    reduction_factor: "depends_on_independence"
    applicability: "concurrent_systems"
    
  on_the_fly_verification:
    technique: "lazy_state_generation"
    memory_reduction: "significant"
    time_reduction: "moderate"
    
  incremental_verification:
    technique: "assume_guarantee"
    decomposition_strategy: "component_based"
    verification_efficiency: "improved"
```

## Integration Examples

### With Formal Verification Tools

```python
# Integration with NuSMV
class NuSMVIntegration:
    """Integration with NuSMV model checker"""
    
    def __init__(self, nusmv_path: str):
        self.nusmv_path = nusmv_path
        
    def generate_nusmv_model(self, model_checker):
        """Generate NuSMV model from our model"""
        smv_content = self._convert_to_smv(model_checker)
        
        with open("model.smv", "w") as f:
            f.write(smv_content)
            
        return "model.smv"
        
    def run_nusmv_verification(self, smv_file: str, properties: list):
        """Run NuSMV verification"""
        cmd = [self.nusmv_path, "-ctl", smv_file]
        
        for prop in properties:
            cmd.extend(["-p", prop])
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        return self._parse_nusmv_output(result.stdout)
        
    def _convert_to_smv(self, model_checker):
        """Convert our model to SMV format"""
        # Implementation details for SMV conversion
        pass

# Integration with SPIN
class SPINIntegration:
    """Integration with SPIN model checker"""
    
    def __init__(self, spin_path: str):
        self.spin_path = spin_path
        
    def generate_promela_model(self, model_checker):
        """Generate Promela model from our model"""
        promela_content = self._convert_to_promela(model_checker)
        
        with open("model.pml", "w") as f:
            f.write(promela_content)
            
        return "model.pml"
        
    def run_spin_verification(self, promela_file: str):
        """Run SPIN verification"""
        # Generate verifier
        subprocess.run([self.spin_path, "-a", promela_file])
        
        # Compile verifier
        subprocess.run(["gcc", "-o", "pan", "pan.c"])
        
        # Run verification
        result = subprocess.run(["./pan"], capture_output=True, text=True)
        return self._parse_spin_output(result.stdout)
```

## Best Practices

1. **Model Design**:
   - Create accurate and complete system models
   - Use appropriate abstraction levels
   - Validate models against system requirements
   - Document model assumptions and limitations

2. **Property Specification**:
   - Write clear and precise temporal logic properties
   - Use both safety and liveness properties
   - Validate properties with examples
   - Document property intent and scope

3. **Verification Strategy**:
   - Choose appropriate model checking algorithm
   - Use abstraction for large state spaces
   - Apply symmetry reduction when applicable
   - Monitor performance and adjust strategy

4. **Counterexample Analysis**:
   - Analyze counterexamples thoroughly
   - Identify root causes of violations
   - Use counterexamples for debugging
   - Document lessons learned

## Troubleshooting

### Common Issues

1. **State Space Explosion**: Apply abstraction, symmetry reduction, or bounded model checking
2. **Long Verification Times**: Use incremental verification or distributed checking
3. **Memory Issues**: Implement disk-based algorithms or distributed verification
4. **Complex Counterexamples**: Apply counterexample simplification techniques
5. **Abstraction Failures**: Review abstraction design and apply refinement

### Debug Mode

```python
# Debug mode: Enhanced debugging
class DebugModelChecker(ModelChecker):
    """Model checker with enhanced debugging capabilities"""
    
    def __init__(self):
        super().__init__()
        self.debug_log = []
        
    def log_state_explored(self, state, depth):
        """Log state exploration for debugging"""
        self.debug_log.append({
            'type': 'state_explored',
            'state': state,
            'depth': depth,
            'timestamp': time.time()
        })
        
    def log_transition_taken(self, source, target, action):
        """Log transition for debugging"""
        self.debug_log.append({
            'type': 'transition',
            'source': source,
            'target': target,
            'action': action,
            'timestamp': time.time()
        })
        
    def log_property_violation(self, state, property_name):
        """Log property violation for debugging"""
        self.debug_log.append({
            'type': 'property_violation',
            'state': state,
            'property': property_name,
            'timestamp': time.time()
        })
        
    def generate_debug_report(self):
        """Generate debug report"""
        report = {
            'total_states_explored': len([e for e in self.debug_log if e['type'] == 'state_explored']),
            'total_transitions': len([e for e in self.debug_log if e['type'] == 'transition']),
            'property_violations': [e for e in self.debug_log if e['type'] == 'property_violation'],
            'exploration_depth': max([e.get('depth', 0) for e in self.debug_log], default=0)
        }
        return report
```

## Monitoring and Metrics

### Verification Metrics

```yaml
verification_metrics:
  correctness_metrics:
    properties_verified: number
    verification_coverage: number
    false_positives: number
    false_negatives: number
    
  performance_metrics:
    average_verification_time: number
    maximum_verification_time: number
    memory_usage_peak: string
    state_space_explored: number
    
  abstraction_metrics:
    abstraction_precision: number
    refinement_iterations: number
    abstract_state_ratio: number
    concrete_state_ratio: number
    
  quality_metrics:
    model_accuracy: number
    property_completeness: number
    counterexample_quality: number
    verification_reliability: number
```

## Dependencies

- **Model Checkers**: NuSMV, SPIN, PRISM, UPPAAL, or custom implementations
- **SAT/SMT Solvers**: Z3, CVC4, Yices for symbolic and bounded model checking
- **Graph Libraries**: NetworkX, Graphviz for state space visualization
- **Optimization Tools**: BDD libraries, abstraction refinement frameworks
- **Integration Frameworks**: APIs for connecting with other verification tools

## Version History

- **1.0.0**: Initial release with comprehensive model checking frameworks
- **1.1.0**: Added advanced abstraction techniques and CEGAR
- **1.2.0**: Enhanced integration with formal verification tools and SAT solvers
- **1.3.0**: Improved performance optimization and parallel verification
- **1.4.0**: Advanced counterexample analysis and debugging capabilities

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.