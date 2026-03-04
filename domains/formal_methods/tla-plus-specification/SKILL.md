---
Domain: formal_methods
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: tla-plus-specification
---



## Description

Automatically designs and implements optimal TLA+ (Temporal Logic of Actions) specifications for formal system modeling, concurrent system verification, and distributed algorithm specification. This skill provides comprehensive frameworks for state machine modeling, temporal property specification, safety and liveness property verification, and model checking with TLC (Temporal Logic of Actions Checker).


## Purpose

*[Content for Purpose section to be added based on the specific skill requirements]*

## Examples

*[Content for Examples section to be added based on the specific skill requirements]*

## Implementation Notes

*[Content for Implementation Notes section to be added based on the specific skill requirements]*
## Capabilities

- **State Machine Modeling**: Design precise state machine models using TLA+ for system behavior specification
- **Temporal Property Specification**: Create formal specifications of safety and liveness properties using temporal logic
- **Concurrent System Verification**: Model and verify concurrent and distributed systems with precise temporal reasoning
- **Model Checking Integration**: Integrate with TLC model checker for automated verification and counterexample generation
- **Refinement and Abstraction**: Implement stepwise refinement and abstraction techniques for complex system modeling
- **Invariant Discovery**: Automatically discover and verify system invariants and safety properties
- **Performance Optimization**: Optimize TLA+ specifications for efficient model checking and verification

## Usage Examples

### TLA+ Specification for Distributed Consensus

```tla
------------------------------ MODULE Consensus ------------------------------

EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS Nodes, QuorumSize, MaxValue

VARIABLES value, decided, votes, round

Node == Nodes
Value == 1..MaxValue

TypeOK == 
    /\ value \in [Node -> Value \cup {None}]
    /\ decided \in [Node -> BOOLEAN]
    /\ votes \in [Node -> SUBSET Value]
    /\ round \in [Node -> Nat]

Init ==
    /\ value = [n \in Node |-> None]
    /\ decided = [n \in Node |-> FALSE]
    /\ votes = [n \in Node |-> {}]
    /\ round = [n \in Node |-> 0]

Propose(n, v) ==
    /\ ~decided[n]
    /\ value[n] = None
    /\ votes[n] = {}
    /\ round[n] = round[n] + 1
    /\ value' = [value EXCEPT ![n] = v]
    /\ UNCHANGED <<decided, votes>>

Vote(n, proposer, v) ==
    /\ ~decided[n]
    /\ value[proposer] = v
    /\ v \notin votes[n]
    /\ votes' = [votes EXCEPT ![n] = votes[n] \cup {v}]
    /\ UNCHANGED <<value, decided, round>>

Decide(n, v) ==
    /\ ~decided[n]
    /\ Cardinality({m \in Node : v \in votes[m]}) >= QuorumSize
    /\ decided' = [decided EXCEPT ![n] = TRUE]
    /\ UNCHANGED <<value, votes, round>>

SafetyProperty ==
    \A n1, n2 \in Node, v1, v2 \in Value :
        (decided[n1] /\ decided[n2] /\ value[n1] = v1 /\ value[n2] = v2)
        => (v1 = v2)

LivenessProperty ==
    \A n \in Node : 
        (value[n] # None) ~> (decided[n] = TRUE)

ConsensusSpec ==
    Init /\ [][Next]_<<value, decided, votes, round>>

Next ==
    \E n \in Node :
        \E v \in Value :
            \/ Propose(n, v)
            \/ Vote(n, n, v)
            \/ Decide(n, v)

=============================================================================
```

### TLA+ Specification for Bank Account System

```tla
------------------------------ MODULE BankAccount ------------------------------

EXTENDS Naturals, Integers

CONSTANTS Accounts, MaxAmount

VARIABLES balance, transactions

Account == Accounts
Amount == 0..MaxAmount

TypeOK ==
    /\ balance \in [Account -> Amount]
    /\ transactions \in Seq([type : {"deposit", "withdraw"}, 
                             account : Account, 
                             amount : Amount])

Init ==
    /\ balance = [a \in Account |-> 0]
    /\ transactions = <<>>

Deposit(a, amt) ==
    /\ amt > 0
    /\ balance[a] + amt <= MaxAmount
    /\ balance' = [balance EXCEPT ![a] = balance[a] + amt]
    /\ transactions' = Append(transactions, 
                              [type |-> "deposit", account |-> a, amount |-> amt])

Withdraw(a, amt) ==
    /\ amt > 0
    /\ balance[a] >= amt
    /\ balance' = [balance EXCEPT ![a] = balance[a] - amt]
    /\ transactions' = Append(transactions, 
                              [type |-> "withdraw", account |-> a, amount |-> amt])

Transfer(from, to, amt) ==
    /\ amt > 0
    /\ from # to
    /\ balance[from] >= amt
    /\ balance[to] + amt <= MaxAmount
    /\ balance' = [balance EXCEPT 
                    ![from] = balance[from] - amt,
                    ![to] = balance[to] + amt]
    /\ transactions' = Append(transactions, 
                              [type |-> "transfer", 
                               account |-> from, 
                               amount |-> amt])

AtomicTransfer(from, to, amt) ==
    /\ amt > 0
    /\ from # to
    /\ balance[from] >= amt
    /\ balance[to] + amt <= MaxAmount
    /\ LET newBalance == [balance EXCEPT 
                           ![from] = balance[from] - amt,
                           ![to] = balance[to] + amt]
       IN /\ balance' = newBalance
          /\ transactions' = Append(transactions, 
                                    [type |-> "transfer", 
                                     account |-> from, 
                                     amount |-> amt])

ConsistencyInvariant ==
    \A a \in Account : balance[a] >= 0

TotalConservation ==
    LET totalBalance == SumRange(balance)
    IN totalBalance = totalBalance

BankSpec ==
    Init /\ [][Next]_<<balance, transactions>>

Next ==
    \E a \in Account, amt \in Amount :
        \/ Deposit(a, amt)
        \/ Withdraw(a, amt)
        \/ \E b \in Account \ {a} :
            Transfer(a, b, amt)

=============================================================================
```

### TLA+ Specification for Producer-Consumer System

```tla
------------------------------ MODULE ProducerConsumer ------------------------------

EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS BufferSize, MaxItems, Producers, Consumers

VARIABLES buffer, in, out, count, producerState, consumerState

BufferIndex == 0..(BufferSize - 1)
Item == 1..MaxItems
Producer == Producers
Consumer == Consumers

TypeOK ==
    /\ buffer \in [BufferIndex -> Item \cup {None}]
    /\ in \in BufferIndex
    /\ out \in BufferIndex
    /\ count \in 0..BufferSize
    /\ producerState \in [Producer -> {"idle", "producing"}]
    /\ consumerState \in [Consumer -> {"idle", "consuming"}]

None == -1

Init ==
    /\ buffer = [i \in BufferIndex |-> None]
    /\ in = 0
    /\ out = 0
    /\ count = 0
    /\ producerState = [p \in Producer |-> "idle"]
    /\ consumerState = [c \in Consumer |-> "idle"]

Produce(p, item) ==
    /\ producerState[p] = "idle"
    /\ count < BufferSize
    /\ buffer' = [buffer EXCEPT ![in] = item]
    /\ in' = (in + 1) % BufferSize
    /\ count' = count + 1
    /\ producerState' = [producerState EXCEPT ![p] = "producing"]
    /\ UNCHANGED <<out, consumerState>>

Consume(c) ==
    /\ consumerState[c] = "idle"
    /\ count > 0
    /\ buffer[out] # None
    /\ buffer' = [buffer EXCEPT ![out] = None]
    /\ out' = (out + 1) % BufferSize
    /\ count' = count - 1
    /\ consumerState' = [consumerState EXCEPT ![c] = "consuming"]
    /\ UNCHANGED <<in, producerState>>

ProducerDone(p) ==
    /\ producerState[p] = "producing"
    /\ producerState' = [producerState EXCEPT ![p] = "idle"]
    /\ UNCHANGED <<buffer, in, out, count, consumerState>>

ConsumerDone(c) ==
    /\ consumerState[c] = "consuming"
    /\ consumerState' = [consumerState EXCEPT ![c] = "idle"]
    /\ UNCHANGED <<buffer, in, out, count, producerState>>

SafetyProperty ==
    /\ \A p \in Producer : producerState[p] \in {"idle", "producing"}
    /\ \A c \in Consumer : consumerState[c] \in {"idle", "consuming"}
    /\ count \in 0..BufferSize
    /\ in \in BufferIndex
    /\ out \in BufferIndex

BoundedBufferInvariant ==
    count = (in - out + BufferSize) % BufferSize

ProducerConsumerSpec ==
    Init /\ [][Next]_<<buffer, in, out, count, producerState, consumerState>>

Next ==
    \/ \E p \in Producer, item \in Item : Produce(p, item)
    \/ \E c \in Consumer : Consume(c)
    \/ \E p \in Producer : ProducerDone(p)
    \/ \E c \in Consumer : ConsumerDone(c)

=============================================================================
```

## Input Format

### TLA+ Specification Request

```yaml
tla_plus_specification_request:
  system_name: string             # Name of the system to specify
  specification_type: string      # Type of specification (concurrent, distributed, etc.)
  
  constants:
    - constant_name: string
      type: string                # Type of constant (natural, set, etc.)
      value: any                  # Value or range of values
      
    - constant_name: string
      type: string
      value: any
  
  variables:
    - variable_name: string
      type: string                # Type of variable
      domain: string              # Domain specification
      initial_value: any          # Initial value expression
      
    - variable_name: string
      type: string
      domain: string
      initial_value: any
  
  actions:
    - action_name: string
      parameters: array           # Action parameters
      precondition: string        # Precondition expression
      effect: string              # Effect expression
      
    - action_name: string
      parameters: array
      precondition: string
      effect: string
  
  properties:
    - property_name: string
      property_type: "safety|liveness"
      expression: string          # TLA+ property expression
      
    - property_name: string
      property_type: "safety|liveness"
      expression: string
  
  verification_requirements:
    model_checker: "TLC|Apalache"
    state_space_limit: number     # Maximum states to explore
    time_limit: number            # Time limit in seconds
    counterexample_generation: boolean
```

### TLA+ Model Configuration

```yaml
tla_model_configuration:
  model_name: string
  specification_file: string      # Path to .tla file
  configuration_file: string      # Path to .cfg file
  
  constants:
    constant_assignments: object  # Constant value assignments
    model_values: object          # Model value definitions
  
  properties:
    invariants: array             # List of invariant properties
    liveness_properties: array    # List of liveness properties
  
  model_checking:
    symmetry_reduction: boolean   # Enable symmetry reduction
    partial_order_reduction: boolean # Enable partial order reduction
    state_compression: boolean    # Enable state compression
    distributed_checking: boolean # Enable distributed checking
  
  performance:
    memory_limit: string          # Memory limit for model checking
    disk_usage: boolean           # Allow disk-based state storage
    parallel_workers: number      # Number of parallel workers
```

## Output Format

### TLA+ Specification Output

```yaml
tla_plus_specification_output:
  specification_id: string
  generation_timestamp: timestamp
  
  generated_files:
    - file_name: string
      file_type: "specification|configuration"
      content: string             # Generated TLA+ content
      size: number                # File size in bytes
      
    - file_name: string
      file_type: "specification|configuration"
      content: string
      size: number
  
  specification_summary:
    constants_count: number
    variables_count: number
    actions_count: number
    properties_count: number
    state_variables: array
    action_names: array
  
  verification_results:
    model_checking_status: "verified|counterexample_found|timeout|error"
    states_explored: number
    states_remaining: number
    verification_time: number
    memory_usage: string
    
    if model_checking_status == "counterexample_found":
      counterexample:
        type: "finite|infinite"
        path: array               # Counterexample execution path
        violating_property: string
        explanation: string
    
    if model_checking_status == "verified":
      verification_details:
        invariants_verified: array
        liveness_properties_verified: array
        proof_obligations_satisfied: array
```

### TLA+ Analysis Report

```yaml
tla_plus_analysis_report:
  specification_complexity:
    action_complexity: string     # Simple, medium, complex
    state_space_size: string      # Estimated state space size
    temporal_logic_complexity: string
    refinement_depth: number      # Depth of refinement hierarchy
  
  verification_complexity:
    model_checking_complexity: string
    proof_complexity: string
    counterexample_complexity: string
    optimization_effectiveness: number
  
  specification_quality:
    completeness_score: number    # 0.0 to 1.0
    consistency_score: number     # 0.0 to 1.0
    clarity_score: number         # 0.0 to 1.0
    maintainability_score: number # 0.0 to 1.0
  
  recommendations:
    - recommendation_type: "optimization|clarification|extension"
      description: string
      priority: "high|medium|low"
      impact: "performance|correctness|maintainability"
```

## Configuration Options

### TLA+ Specification Patterns

```yaml
specification_patterns:
  state_machine:
    description: "State machine pattern for reactive systems"
    best_for: ["protocol_specification", "control_systems", "reactive_systems"]
    complexity: "medium"
    model_checking: "efficient"
    
  distributed_algorithm:
    description: "Pattern for distributed algorithms and protocols"
    best_for: ["consensus_algorithms", "distributed_systems", "network_protocols"]
    complexity: "high"
    model_checking: "challenging"
    
  data_structure:
    description: "Pattern for abstract data structure specification"
    best_for: ["algorithms", "data_structures", "mathematical_objects"]
    complexity: "variable"
    model_checking: "depends_on_structure"
    
  refinement_hierarchy:
    description: "Stepwise refinement from abstract to concrete"
    best_for: ["system_development", "verification", "abstraction"]
    complexity: "high"
    model_checking: "layered_verification"
```

### Model Checking Strategies

```yaml
model_checking_strategies:
  exhaustive:
    description: "Exhaustive state space exploration"
    best_for: ["small_systems", "critical_properties", "debugging"]
    memory_usage: "high"
    time_complexity: "exponential"
    
  bounded:
    description: "Bounded model checking with depth limits"
    best_for: ["large_systems", "bug_detection", "counterexample_generation"]
    memory_usage: "moderate"
    time_complexity: "polynomial_in_bound"
    
  symbolic:
    description: "Symbolic model checking with BDDs"
    best_for: ["medium_systems", "combinatorial_explosion_avoidance"]
    memory_usage: "depends_on_BDD_size"
    time_complexity: "variable"
    
  distributed:
    description: "Distributed model checking across multiple machines"
    best_for: ["very_large_systems", "high_performance_environments"]
    memory_usage: "distributed"
    time_complexity: "reduced_by_parallelization"
```

## Error Handling

### Specification Errors

```yaml
specification_errors:
  syntax_error:
    detection_strategy: "parser_validation"
    recovery_strategy: "syntax_correction"
    escalation: "manual_review"
  
  type_error:
    detection_strategy: "type_checking"
    recovery_strategy: "type_inference"
    escalation: "type_annotation_required"
  
  semantic_error:
    detection_strategy: "semantic_analysis"
    recovery_strategy: "specification_rewriting"
    escalation: "expert_intervention"
  
  inconsistency_error:
    detection_strategy: "consistency_checking"
    recovery_strategy: "conflict_resolution"
    escalation: "specification_revision"
```

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

## Performance Optimization

### Specification Optimization

```tla
(* Optimization: State space reduction *)
StateSpaceReduction ==
    (* Use symmetry reduction for symmetric systems *)
    SymmetricStates ==
        \A s1, s2 \in State :
            (IsSymmetric(s1, s2)) => (Equivalent(s1, s2))
    
    (* Use partial order reduction for independent actions *)
    IndependentActions ==
        \A a1, a2 \in Actions :
            (Independent(a1, a2)) => (Commutative(a1, a2))

(* Optimization: Action ordering *)
ActionOrdering ==
    (* Prioritize actions that reduce state space *)
    PriorityActions ==
        {a \in Actions : ReducesStateSpace(a)}
    
    (* Defer expensive actions when possible *)
    DeferredActions ==
        {a \in Actions : ExpensiveAction(a)}

(* Optimization: Invariant strengthening *)
InvariantStrengthening ==
    (* Add auxiliary variables for better invariants *)
    AuxiliaryVariables ==
        [aux1 : Type1, aux2 : Type2, ...]
    
    (* Strengthen invariants with auxiliary information *)
    StrongerInvariants ==
        OriginalInvariants /\ AuxiliaryInvariants
```

### Model Checking Optimization

```yaml
model_checking_optimizations:
  state_compression:
    technique: "hash_compaction"
    compression_ratio: "variable"
    memory_reduction: "significant"
    
  symmetry_reduction:
    technique: "automorphism_detection"
    symmetry_groups: "detected_automatically"
    state_reduction: "exponential_in_best_case"
    
  partial_order_reduction:
    technique: "ample_sets"
    reduction_factor: "depends_on_independence"
    applicability: "concurrent_systems"
    
  incremental_verification:
    technique: "assume_guarantee"
    decomposition_strategy: "component_based"
    verification_efficiency: "improved"
```

## Integration Examples

### With Formal Verification Tools

```python
# Integration with TLC model checker
class TLCSpecification:
    """TLA+ specification integration with TLC"""
    
    def __init__(self, specification_file):
        self.spec_file = specification_file
        self.tlc_path = "/path/to/tlc"
        
    def run_model_checking(self, config):
        """Run TLC model checking with specified configuration"""
        # Generate TLC command
        tlc_command = self.generate_tlc_command(config)
        
        # Execute TLC
        result = self.execute_tlc(tlc_command)
        
        # Parse results
        parsed_results = self.parse_tlc_results(result)
        
        return parsed_results
    
    def generate_counterexample(self, property):
        """Generate counterexample for failed property"""
        # Configure TLC for counterexample generation
        config = {
            'check_safety': True,
            'check_liveness': False,
            'generate_counterexample': True,
            'property': property
        }
        
        return self.run_model_checking(config)
    
    def optimize_specification(self):
        """Apply optimization techniques to TLA+ specification"""
        # Apply symmetry reduction
        self.apply_symmetry_reduction()
        
        # Apply partial order reduction
        self.apply_partial_order_reduction()
        
        # Optimize state representation
        self.optimize_state_representation()
```

### With Proof Assistants

```python
# Integration with proof assistants
class TLAProofIntegration:
    """TLA+ integration with proof assistants"""
    
    def __init__(self, proof_assistant):
        self.proof_assistant = proof_assistant
        
    def convert_to_proof_obligations(self, specification):
        """Convert TLA+ specification to proof obligations"""
        # Extract invariants
        invariants = self.extract_invariants(specification)
        
        # Generate proof obligations
        obligations = self.generate_proof_obligations(invariants)
        
        return obligations
    
    def discharge_proof_obligations(self, obligations):
        """Discharge proof obligations using proof assistant"""
        results = []
        
        for obligation in obligations:
            result = self.proof_assistant.prove(obligation)
            results.append(result)
        
        return results
    
    def combine_model_checking_and_proving(self, specification):
        """Combine model checking and theorem proving"""
        # Use model checking for finite cases
        finite_result = self.run_finite_model_checking(specification)
        
        # Use theorem proving for general cases
        general_result = self.run_theorem_proving(specification)
        
        return {
            'finite_verification': finite_result,
            'general_verification': general_result
        }
```

## Best Practices

1. **Specification Design**:
   - Use clear, descriptive names for constants, variables, and actions
   - Document assumptions and design decisions
   - Use stepwise refinement for complex systems
   - Apply abstraction to manage complexity

2. **Model Checking**:
   - Start with small models and gradually increase size
   - Use symmetry reduction for symmetric systems
   - Apply partial order reduction for concurrent systems
   - Monitor memory usage and state space growth

3. **Property Specification**:
   - Write both safety and liveness properties
   - Use temporal logic operators appropriately
   - Verify properties incrementally
   - Generate meaningful counterexamples

4. **Optimization**:
   - Apply abstraction techniques early
   - Use appropriate data structures
   - Optimize state representation
   - Implement efficient action guards

## Troubleshooting

### Common Issues

1. **State Space Explosion**: Apply abstraction, symmetry reduction, or bounded model checking
2. **Long Verification Times**: Use incremental verification or distributed checking
3. **Memory Issues**: Implement disk-based algorithms or distributed verification
4. **Complex Counterexamples**: Apply counterexample simplification techniques
5. **Specification Errors**: Use formal specification tools and validation

### Debug Mode

```tla
(* Debug mode: Enhanced traceability *)
DebugMode ==
    (* Add trace variables *)
    TraceVariables ==
        [trace_actions : Seq(Action),
         trace_states : Seq(State),
         trace_time : Nat]
    
    (* Add assertion checking *)
    Assertions ==
        \A s \in State :
            (Invariant(s)) => (AssertionsHold(s))
    
    (* Add detailed logging *)
    DetailedLogging ==
        \A a \in Actions :
            LoggingEnabled(a) => (LogAction(a))
```

## Monitoring and Metrics

### Verification Metrics

```yaml
verification_metrics:
  model_checking_metrics:
    states_explored: number
    states_remaining: number
    transitions_explored: number
    verification_time: number
    
  specification_metrics:
    lines_of_specification: number
    complexity_score: number
    abstraction_level: number
    refinement_depth: number
    
  performance_metrics:
    memory_usage_peak: string
    cpu_utilization: number
    parallel_efficiency: number
    disk_usage: string
    
  quality_metrics:
    coverage_ratio: number
    property_verification_rate: number
    counterexample_quality: number
    specification_maintainability: number
```

## Dependencies

- **TLA+ Tools**: TLC model checker, Apalache model checker, TLA+ Toolbox
- **Proof Assistants**: Isabelle/HOL, Coq, or other theorem provers for integration
- **Formal Methods Libraries**: Libraries for temporal logic and formal verification
- **Performance Tools**: Profiling and monitoring tools for model checking performance
- **Integration Frameworks**: APIs for connecting TLA+ with other formal methods tools

## Version History

- **1.0.0**: Initial release with comprehensive TLA+ specification frameworks
- **1.1.0**: Added advanced model checking optimization techniques
- **1.2.0**: Enhanced integration with proof assistants and formal verification tools
- **1.3.0**: Improved performance optimization and distributed model checking
- **1.4.0**: Advanced abstraction techniques and stepwise refinement support

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.

## Constraints

Content for ## Constraints involving Tla Plus Specification.