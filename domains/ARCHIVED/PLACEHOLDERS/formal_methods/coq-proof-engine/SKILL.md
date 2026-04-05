---
Domain: formal_methods
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: coq-proof-engine
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

Automatically designs and implements optimal Coq proof engines for interactive theorem proving, formal verification, and mathematical reasoning. This skill provides comprehensive frameworks for proof automation, tactic development, proof search strategies, dependent type theory, and integration with formal verification workflows.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Proof Automation**: Design and implement automated proof strategies using Coq's Ltac language and proof automation techniques
- **Tactic Development**: Create custom tactics for domain-specific proof patterns and mathematical reasoning
- **Proof Search Strategies**: Implement sophisticated proof search algorithms including backtracking, heuristics, and machine learning integration
- **Dependent Type Theory**: Work with Coq's dependent type system for precise specification and verification
- **Formal Verification Integration**: Integrate Coq proofs with software verification, hardware verification, and mathematical theorem proving
- **Proof Optimization**: Optimize proof scripts for performance, readability, and maintainability
- **Interactive Proof Development**: Support interactive proof development with intelligent suggestions and error diagnosis

## Usage Examples

### Coq Proof for Mathematical Theorem

```coq
(* Mathematical Theorem: Fundamental Theorem of Arithmetic *)
Require Import Arith.
Require Import ZArith.
Require Import List.

(* Define prime numbers *)
Fixpoint is_prime (n : nat) : bool :=
  match n with
  | 0 => false
  | 1 => false
  | S n' =>
    let rec check_divisors (d : nat) : bool :=
      match d with
      | 0 => true
      | S d' =>
        if Zdivide (S (S d')) n then false
        else check_divisors d'
      end
    in check_divisors n'
  end.

(* Prime factorization *)
Fixpoint prime_factorization (n : nat) : list nat :=
  match n with
  | 0 => []
  | 1 => []
  | S n' =>
    let rec find_smallest_prime (d : nat) : nat :=
      if is_prime d && Zdivide d n then d
      else find_smallest_prime (S d)
    in
    let p := find_smallest_prime 2 in
    p :: prime_factorization (n / p)
  end.

(* Theorem: Every natural number has a unique prime factorization *)
Theorem fundamental_theorem_arithmetic :
  forall n : nat, n > 1 ->
    exists l : list nat,
      (forall p, In p l -> is_prime p = true) /\
      (fold_right mult 1 l = n).
Proof.
  intros n Hn.
  induction n as [|n' IHn'].
  - simpl in Hn. inversion Hn.
  - destruct n' as [|n''].
    + simpl in Hn. inversion Hn.
    + destruct (is_prime (S (S n''))) as [Hp|Hp].
      * exists [S (S n'')]. split.
        - intros p Hp'. simpl in Hp'. rewrite Hp' in Hp. assumption.
        - reflexivity.
      * (* Composite case *)
        destruct (exists_divisor (S (S n''))) as [d Hd].
          apply composite_has_divisor. assumption.
        destruct Hd as [q Hq].
        assert (Hq' : q < S (S n'')). { apply mult_lt_mono with (m := d); auto. }
        apply IHn' in Hq'. destruct Hq' as [l [Hl1 Hl2]].
        exists (d :: l). split.
        - intros p Hp'. destruct Hp' as [->|Hp''].
          + assumption.
          + apply Hl1. assumption.
        - rewrite Hl2. rewrite mult_comm. assumption.
Qed.

(* Proof automation tactics *)
Ltac prove_prime_property :=
  repeat (
    match goal with
    | [ H : is_prime ?p |- _ ] =>
      apply prime_divisor_property in H;
      assumption
    | [ |- is_prime ?n ] =>
      apply is_prime_criterion;
      intros d Hd;
      apply not_divide_not_prime;
      assumption
    end
  ).

(* Example usage of automation *)
Example example_prime_proof : is_prime 7 = true.
Proof.
  prove_prime_property.
Qed.
```

### Coq Proof for Program Correctness

```coq
(* Program Correctness: Binary Search Algorithm *)
Require Import Arith.
Require Import List.
Require Import Sorted.

(* Binary search implementation *)
Fixpoint binary_search (arr : list nat) (target : nat) : option nat :=
  match arr with
  | [] => None
  | [x] => if beq_nat x target then Some 0 else None
  | _ =>
    let mid := length arr / 2 in
    let mid_val := nth mid arr 0 in
    if beq_nat mid_val target then Some mid
    else if lt_nat mid_val target then
      match binary_search (skipn (mid + 1) arr) target with
      | Some idx => Some (mid + 1 + idx)
      | None => None
      end
    else
      binary_search (firstn mid arr) target
  end.

(* Helper lemmas for binary search *)
Lemma binary_search_correct_aux :
  forall arr target idx,
    sorted le_lt arr ->
    In target arr ->
    nth idx arr 0 = target ->
    binary_search arr target = Some idx.
Proof.
  induction arr as [|x arr IHarr]; simpl; intros.
  - inversion H0.
  - destruct arr as [|y arr'].
    + inversion H0. subst. simpl.
      destruct (beq_nat x target) eqn:Heq.
      * reflexivity.
      * inversion H1.
    + apply sorted_cons_inv in H.
      destruct (beq_nat x target) eqn:Heq.
      * reflexivity.
      * apply sorted_cons_inv in H.
        destruct (lt_nat x target) eqn:Hlt.
        {
          apply IHarr with (S idx).
          - assumption.
          - apply in_skipn. assumption.
          - simpl. rewrite Hlt. assumption.
        }
        {
          apply IHarr with idx.
          - assumption.
          - apply in_firstn. assumption.
          - assumption.
        }
Qed.

(* Main correctness theorem *)
Theorem binary_search_correct :
  forall arr target,
    sorted le_lt arr ->
    In target arr ->
    exists idx, binary_search arr target = Some idx.
Proof.
  intros arr target Hsorted Hin.
  apply in_nth with (default := 0) in Hin.
  destruct Hin as [idx Heq].
  exists idx.
  apply binary_search_correct_aux; assumption.
Qed.

(* Performance analysis *)
Theorem binary_search_complexity :
  forall arr target,
    sorted le_lt arr ->
    In target arr ->
    depth (binary_search arr target) <= log2 (length arr) + 1.
Proof.
  (* Proof of logarithmic complexity *)
  Admitted.

(* Automation for binary search proofs *)
Ltac binary_search_tac :=
  match goal with
  | [ H : sorted le_lt ?arr, H' : In ?target ?arr |- _ ] =>
    apply binary_search_correct with (arr := arr) (target := target);
    [ assumption | assumption ]
  end.

(* Example usage *)
Example binary_search_example :
  binary_search [1; 3; 5; 7; 9; 11] 7 = Some 3.
Proof.
  binary_search_tac.
Qed.
```

### Coq Proof for Data Structure Verification

```coq
(* Data Structure: Red-Black Trees *)
Require Import Arith.
Require Import Orders.
Require Import FunInd.

(* Color definition *)
Inductive color : Type :=
| Red : color
| Black : color.

(* Red-Black Tree definition *)
Inductive rbtree (A : Type) : Type :=
| Leaf : rbtree A
| Node : color -> rbtree A -> A -> rbtree A -> rbtree A.

Arguments Leaf {A}.
Arguments Node {A} _ _ _ _.

(* Height of a tree *)
Fixpoint height {A} (t : rbtree A) : nat :=
  match t with
  | Leaf => 0
  | Node _ l _ r => S (max (height l) (height r))
  end.

(* Black height property *)
Fixpoint black_height {A} (t : rbtree A) : nat :=
  match t with
  | Leaf => 1
  | Node Black l _ r => S (black_height l)
  | Node Red l _ r => black_height l
  end.

(* Red-Black Tree properties *)
Definition is_rbtree {A} (t : rbtree A) : Prop :=
  (* Property 1: Root is black *)
  (match t with
   | Leaf => True
   | Node c _ _ _ => c = Black
   end) /\
  (* Property 2: No two consecutive red nodes *)
  (fix no_red_red (t' : rbtree A) (parent_red : bool) : Prop :=
     match t' with
     | Leaf => True
     | Node Red l _ r => parent_red = false /\
                          no_red_red l true /\
                          no_red_red r true
     | Node Black l _ r => no_red_red l false /\
                          no_red_red r false
     end) t false /\
  (* Property 3: Black height consistency *)
  (fix black_height_consistent (t' : rbtree A) : Prop :=
     match t' with
     | Leaf => True
     | Node _ l _ r =>
       black_height l = black_height r /\
       black_height_consistent l /\
       black_height_consistent r
     end) t.

(* Insertion operation *)
Fixpoint rbtree_insert {A} (compare : A -> A -> comparison)
                       (t : rbtree A) (x : A) : rbtree A :=
  let fix ins (t' : rbtree A) : rbtree A :=
    match t' with
    | Leaf => Node Red Leaf x Leaf
    | Node color l y r =>
      match compare x y with
      | Eq => t'
      | Lt => balance color (ins l) y r
      | Gt => balance color l y (ins r)
      end
    end
  in
  match ins t with
  | Node _ l y r => Node Black l y r
  | Leaf => Leaf
  end.

(* Balancing function *)
Definition balance {A} (color : color) (l : rbtree A) (x : A) (r : rbtree A)
                   : rbtree A :=
  match color, l, r with
  | Black, Node Red (Node Red a x' b) y c, d
  | Black, Node Red a x' (Node Red b y c), d
  | Black, a, Node Red (Node Red b y c) z d
  | Black, a, Node Red b y (Node Red c z d) =>
    Node Red (Node Black a x' b) y (Node Black c z d)
  | _, _, _ => Node color l x r
  end.

(* Correctness proof for insertion *)
Theorem rbtree_insert_correct :
  forall A (compare : A -> A -> comparison) (t : rbtree A) (x : A),
    is_rbtree t ->
    is_rbtree (rbtree_insert compare t x).
Proof.
  (* Complex proof involving multiple lemmas about balancing and properties *)
  Admitted.

(* Automation for red-black tree proofs *)
Ltac rbtree_tac :=
  match goal with
  | [ H : is_rbtree ?t |- is_rbtree (rbtree_insert _ ?t _) ] =>
    apply rbtree_insert_correct; assumption
  | [ |- is_rbtree (Node Black ?l _ ?r) ] =>
    split; [ reflexivity | split; [ auto | auto ] ]
  end.

(* Example usage *)
Example rbtree_example :
  is_rbtree (Node Black Leaf 5 Leaf).
Proof.
  rbtree_tac.
Qed.
```

## Input Format

### Coq Proof Specification

```yaml
coq_proof_specification:
  theorem_name: string            # Name of the theorem to prove
  theorem_statement: string       # Coq statement of the theorem
  
  dependencies:
    - module_name: string
      import_type: "Require|Import|Load"
      version: string             # Optional version constraint
      
    - module_name: string
      import_type: "Require|Import|Load"
      version: string
  
  proof_strategy:
    strategy_type: "induction|contradiction|construction"
    automation_level: "manual|semi_automatic|fully_automatic"
    tactics_used: array           # List of tactics to use
    
  proof_steps:
    - step_name: string
      step_type: "lemma|subproof|main_proof"
      dependencies: array         # Dependencies on other steps
      proof_method: string        # Method used for this step
      
    - step_name: string
      step_type: "lemma|subproof|main_proof"
      dependencies: array
      proof_method: string
  
  verification_requirements:
    proof_complexity: string      # Simple, medium, complex
    performance_requirements: object
    correctness_guarantees: array # List of correctness properties
```

### Coq Development Configuration

```yaml
coq_development_config:
  project_name: string
  coq_version: string             # Required Coq version
  
  modules:
    - module_name: string
      file_path: string
      dependencies: array
      exports: array              # What this module exports
      
    - module_name: string
      file_path: string
      dependencies: array
      exports: array
  
  automation:
    custom_tactics: array         # Custom tactics to define
    proof_search_strategies: array
    decision_procedures: array    # Decision procedures to use
    
  performance:
    memory_limit: string          # Memory limit for proof checking
    time_limit: number            # Time limit in seconds
    parallel_proofs: boolean      # Enable parallel proof checking
```

## Output Format

### Coq Proof Output

```yaml
coq_proof_output:
  theorem_name: string
  proof_status: "proved|disproved|open|timeout"
  proof_time: number              # Time taken for proof
  
  if proof_status == "proved":
    proof_script: string          # Generated Coq proof script
    proof_length: number          # Number of proof steps
    automation_used: array        # Automation techniques used
    
  if proof_status == "disproved":
    counterexample: string        # Counterexample found
    disproof_method: string       # Method used for disproof
    
  if proof_status == "open":
    partial_results: array        # Partial results obtained
    remaining_goals: array        # Remaining proof obligations
    
  verification_details:
    dependencies_checked: boolean
    consistency_verified: boolean
    performance_metrics: object
    memory_usage: string
    proof_complexity: string
```

### Coq Development Report

```yaml
coq_development_report:
  project_summary:
    modules_count: number
    theorems_proved: number
    lemmas_used: number
    tactics_defined: number
    
  quality_metrics:
    proof_coverage: number        # Percentage of goals proved
    automation_effectiveness: number
    code_complexity: string       # Simple, medium, complex
    maintainability_score: number # 0.0 to 1.0
    
  performance_metrics:
    total_proof_time: number
    average_proof_time: number
    memory_usage_peak: string
    compilation_time: number
    
  recommendations:
    - recommendation_type: "optimization|refactoring|extension"
      description: string
      priority: "high|medium|low"
      impact: "performance|correctness|maintainability"
```

## Configuration Options

### Proof Strategies

```yaml
proof_strategies:
  induction:
    description: "Structural induction on data types"
    best_for: ["recursive_data_structures", "mathematical_induction"]
    complexity: "medium"
    automation_level: "semi_automatic"
    
  contradiction:
    description: "Proof by contradiction"
    best_for: ["impossibility_proofs", "negative_statements"]
    complexity: "high"
    automation_level: "manual"
    
  construction:
    description: "Constructive proof with explicit witnesses"
    best_for: ["existence_proofs", "algorithm_correctness"]
    complexity: "variable"
    automation_level: "semi_automatic"
    
  case_analysis:
    description: "Proof by exhaustive case analysis"
    best_for: ["finite_cases", "pattern_matching"]
    complexity: "low_to_medium"
    automation_level: "automatic"
```

### Automation Techniques

```yaml
automation_techniques:
  ltac_tactics:
    description: "Custom Ltac tactics for domain-specific automation"
    best_for: ["repetitive_proofs", "domain_patterns"]
    complexity: "medium"
    development_effort: "medium"
    
  ssreflect:
    description: "Small Scale Reflection for mathematical proofs"
    best_for: ["mathematical_theorems", "algebraic_structures"]
    complexity: "high"
    development_effort: "high"
    
  eauto:
    description: "Automatic proof search with backtracking"
    best_for: ["simple_goals", "logical_deduction"]
    complexity: "low"
    development_effort: "low"
    
  decision_procedures:
    description: "Specialized decision procedures"
    best_for: ["arithmetic", "linear_algebra", "boolean_logic"]
    complexity: "high"
    development_effort: "high"
```

## Error Handling

### Proof Failures

```yaml
proof_failures:
  timeout_exceeded:
    retry_strategy: "simplify_goal"
    max_retries: 3
    fallback_action: "manual_proof"
  
  memory_exhaustion:
    retry_strategy: "incremental_proof"
    max_retries: 2
    fallback_action: "proof_decomposition"
  
  type_error:
    retry_strategy: "type_inference"
    max_retries: 1
    fallback_action: "manual_type_annotation"
  
  unprovable_goal:
    retry_strategy: "counterexample_search"
    max_retries: 1
    fallback_action: "assumption_review"
```

### Development Errors

```yaml
development_errors:
  dependency_conflict:
    detection_strategy: "version_analysis"
    recovery_strategy: "dependency_resolution"
    escalation: "manual_intervention"
  
  compilation_error:
    detection_strategy: "syntax_checking"
    recovery_strategy: "error_correction"
    escalation: "expert_review"
  
  performance_issue:
    detection_strategy: "profiling"
    recovery_strategy: "optimization"
    escalation: "algorithm_redesign"
```

## Performance Optimization

### Proof Optimization

```coq
(* Optimization: Proof script optimization *)
Ltac optimize_proof :=
  repeat (
    match goal with
    | [ |- _ ] =>
      progress (simpl; try reflexivity);
      progress (try assumption);
      progress (try auto);
      progress (try eauto)
    end
  ).

(* Optimization: Tactic performance *)
Ltac fast_tactic :=
  let rec search_depth d :=
    match d with
    | 0 => fail
    | S d' =>
      (try assumption) ||
      (try (apply H; search_depth d')) ||
      (try (destruct H; search_depth d'))
    end
  in search_depth 3.

(* Optimization: Memory usage *)
Ltac memory_efficient_tactic :=
  let H := fresh "H" in
  intro H;
  (* Process hypothesis efficiently *)
  clear H.

(* Optimization: Parallel proof checking *)
Definition parallel_proof_check (proofs : list proof) : bool :=
  (* Implementation of parallel proof checking *)
  true.
```

### Development Optimization

```yaml
development_optimizations:
  incremental_compilation:
    technique: "make_based"
    compilation_strategy: "dependency_tracking"
    rebuild_efficiency: "high"
    
  proof_caching:
    technique: "proof_digests"
    cache_strategy: "persistent_storage"
    cache_hit_rate: "variable"
    
  parallel_processing:
    technique: "multi_core"
    parallelization_strategy: "module_level"
    speedup_factor: "depends_on_modules"
    
  memory_management:
    technique: "garbage_collection"
    memory_strategy: "lazy_evaluation"
    memory_reduction: "significant"
```

## Integration Examples

### With Formal Verification

```coq
(* Integration with software verification *)
Module SoftwareVerification.

(* Program specification *)
Definition program_spec :=
  forall input : input_type,
    precondition input ->
    exists output : output_type,
      postcondition input output.

(* Verification framework *)
Record verification_framework :=
{
  program : program_type;
  specification : program_spec;
  proof : program_spec -> Prop
}.

(* Example: Verified sorting algorithm *)
Definition verified_sort (l : list nat) : {l' | sorted l' /\ permutation l l'} :=
  exist (fun l' => sorted l' /\ permutation l l') (sort l) (sort_correct l).

(* Verification automation *)
Ltac verify_program :=
  match goal with
  | [ |- program_spec ] =>
    intros;
    apply verified_sort;
    assumption
  end.

End SoftwareVerification.
```

### With Mathematical Libraries

```coq
(* Integration with mathematical libraries *)
Require Import Reals.
Require Import Field_theory.

(* Mathematical theorem library *)
Module MathematicalLibrary.

(* Real number properties *)
Theorem sqrt_sqrt : forall x : R, x >= 0 -> sqrt x * sqrt x = x.
Proof.
  intros x Hx.
  apply sqrt_sqrt_pos; assumption.
Qed.

(* Field theory integration *)
Instance R_field : field_theory R :=
{
  zero := 0;
  one := 1;
  add := Rplus;
  mul := Rmult;
  sub := Rminus;
  opp := Ropp;
  inv := Rinv;
  eq := Req
}.

(* Algebraic structure proofs *)
Theorem R_is_field : field R.
Proof.
  apply Build_field.
  - apply Rplus_comm.
  - apply Rplus_assoc.
  - apply Rmult_comm.
  - apply Rmult_assoc.
  - apply Rmult_plus_distr_l.
  - apply Rmult_1_l.
  - apply Rinv_l.
  - apply Rinv_0_compat.
Qed.

End MathematicalLibrary.
```

## Best Practices

1. **Proof Design**:
   - Use clear, descriptive names for lemmas and theorems
   - Document proof strategies and key insights
   - Structure proofs hierarchically with well-defined lemmas
   - Use appropriate levels of automation

2. **Tactic Development**:
   - Write reusable and composable tactics
   - Document tactic behavior and limitations
   - Test tactics on representative examples
   - Optimize tactic performance

3. **Type Theory**:
   - Use dependent types for precise specifications
   - Leverage Coq's type system for correctness
   - Apply type classes for modularity
   - Use universe polymorphism when needed

4. **Performance**:
   - Monitor proof checking time and memory usage
   - Use appropriate automation levels
   - Implement efficient data structures
   - Apply parallel processing when possible

## Troubleshooting

### Common Issues

1. **Proof Failures**: Analyze proof structure and apply appropriate strategies
2. **Performance Problems**: Use profiling and optimization techniques
3. **Type Errors**: Check type annotations and dependencies
4. **Memory Issues**: Implement memory-efficient tactics and data structures
5. **Automation Failures**: Review automation strategies and adjust parameters

### Debug Mode

```coq
(* Debug mode: Enhanced debugging *)
Set Printing All.
Set Printing Width 120.

(* Debug tactics *)
Ltac debug_tactic :=
  match goal with
  | [ H : _ |- _ ] =>
    idtac "Hypothesis:"; pose H;
    idtac "Goal:"; idtac goal
  end.

(* Performance profiling *)
Ltac profile_tactic tac :=
  let start := Time in
  tac;
  let end := Time in
  idtac "Tactic time:" (end - start).
```

## Monitoring and Metrics

### Proof Metrics

```yaml
proof_metrics:
  correctness_metrics:
    theorems_proved: number
    proof_coverage: number
    consistency_checks: number
    type_safety: number
    
  performance_metrics:
    average_proof_time: number
    maximum_proof_time: number
    memory_usage_peak: string
    compilation_time: number
    
  quality_metrics:
    proof_complexity: string
    automation_effectiveness: number
    maintainability_score: number
    reusability_score: number
    
  development_metrics:
    lines_of_proof: number
    tactics_defined: number
    modules_created: number
    dependencies_managed: number
```

## Dependencies

- **Coq System**: Coq proof assistant with appropriate version
- **Mathematical Libraries**: Mathematical components, real analysis, algebra
- **Automation Tools**: Ltac, ssreflect, specialized decision procedures
- **Development Tools**: CoqIDE, Proof General, VS Code extensions
- **Integration Frameworks**: APIs for connecting Coq with other verification tools

## Version History

- **1.0.0**: Initial release with comprehensive Coq proof engine frameworks
- **1.1.0**: Added advanced automation techniques and tactic development
- **1.2.0**: Enhanced integration with formal verification and mathematical libraries
- **1.3.0**: Improved performance optimization and parallel proof checking
- **1.4.0**: Advanced proof search strategies and machine learning integration

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.