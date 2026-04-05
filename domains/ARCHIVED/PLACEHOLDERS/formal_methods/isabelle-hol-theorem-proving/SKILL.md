---
Domain: formal_methods
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: isabelle-hol-theorem-proving
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

Automatically designs and implements optimal Isabelle/HOL theorem proving frameworks for higher-order logic reasoning, formal verification, and mathematical theorem proving. This skill provides comprehensive frameworks for proof automation, Isar structured proofs, HOL-specific tactics, formal verification workflows, and integration with automated reasoning systems.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Higher-Order Logic Reasoning**: Design and implement proofs using Isabelle's higher-order logic for complex mathematical reasoning
- **Isar Structured Proofs**: Create well-structured, readable proofs using Isar language for maintainable formal developments
- **HOL-Specific Tactics**: Develop domain-specific tactics and proof methods for HOL reasoning patterns
- **Proof Automation**: Implement sophisticated automation using Isabelle's Sledgehammer, metis, and custom tactics
- **Formal Verification**: Integrate with software and hardware verification workflows using HOL's verification capabilities
- **Mathematical Library Integration**: Work with Isabelle's extensive mathematical libraries for analysis, algebra, and number theory
- **Interactive Proof Development**: Support interactive theorem proving with intelligent proof state management and goal navigation

## Usage Examples

### Isabelle/HOL Proof for Mathematical Theorem

```isabelle
theory Fundamental_Theorem_Arithmetic
imports Main "HOL-Computational_Algebra.Primes"
begin

text ‹Fundamental Theorem of Arithmetic: Every natural number has a unique prime factorization›

definition is_prime :: "nat ⇒ bool" where
  "is_prime n ⟷ n > 1 ∧ (∀m. m dvd n ⟶ m = 1 ∨ m = n)"

definition prime_factorization :: "nat ⇒ nat list" where
  "prime_factorization n = (if n = 0 then [] else
    if n = 1 then [] else
      let p = LEAST p. is_prime p ∧ p dvd n
      in p # prime_factorization (n div p))"

lemma exists_smallest_prime_divisor:
  assumes "n > 1"
  shows "∃p. is_prime p ∧ p dvd n"
proof -
  let ?P = "{p. p dvd n ∧ p > 1}"
  have "finite ?P" by (simp add: finite_divisors_nat assms)
  have "n ∈ ?P" using assms by simp
  then have "?P ≠ {}" by auto
  then obtain p where "p ∈ ?P" and "∀q∈?P. q ≥ p"
    by (rule finite_has_minimal[where m="op dvd"])
  then show ?thesis
    by (auto simp: is_prime_def intro: dvd_antisym)
qed

lemma prime_factorization_exists:
  assumes "n > 1"
  shows "∃l. prime_factorization n = l ∧ (∀p∈set l. is_prime p) ∧ prod_list l = n"
proof (induction n rule: less_induct)
  case (less n)
  show ?case
  proof (cases "is_prime n")
    case True
    then have "prime_factorization n = [n]"
      by (simp add: prime_factorization_def is_prime_def)
    then show ?thesis using True by auto
  next
    case False
    then obtain p where p: "is_prime p" "p dvd n" "p < n"
      using exists_smallest_prime_divisor[OF less.prems] by auto
    then obtain m where m: "n = p * m" "m > 1"
      by (metis dvd_mult_div_cancel dvd_triv_left less.prems nat_dvd_not_less)
    have "m < n" using p m by simp
    then obtain l where l: "prime_factorization m = l" "∀p∈set l. is_prime p" "prod_list l = m"
      using less.IH[OF ‹m > 1›] by auto
    then have "prime_factorization n = p # l"
      by (simp add: prime_factorization_def m p)
    then show ?thesis using p l by auto
  qed
qed

theorem fundamental_theorem_arithmetic:
  assumes "n > 1"
  shows "∃!l. (∀p∈set l. is_prime p) ∧ sorted l ∧ prod_list l = n"
proof -
  obtain l where l: "∀p∈set l. is_prime p" "prod_list l = n"
    using prime_factorization_exists[OF assms] by auto
  let ?l = "sort l"
  have "∀p∈set ?l. is_prime p" using l by simp
  have "prod_list ?l = n" using l by (simp add: mult.commute)
  have "sorted ?l" by simp
  show ?thesis
  proof (rule ex_ex1I)
    show "(∀p∈set ?l. is_prime p) ∧ sorted ?l ∧ prod_list ?l = n"
      using ‹∀p∈set ?l. is_prime p› ‹sorted ?l› ‹prod_list ?l = n› by blast
  next
    fix l'
    assume assm: "(∀p∈set l'. is_prime p) ∧ sorted l' ∧ prod_list l' = n"
    have "set l = set l'" using l assm
      by (metis prime_factorization_unique_nat)
    then have "l = l'" using ‹sorted ?l› assm
      by (metis sorted_list_of_set_unique)
    then show "l' = ?l" by simp
  qed
qed

end
```

### Isabelle/HOL Proof for Program Correctness

```isabelle
theory Binary_Search_Correctness
imports Main
begin

text ‹Binary Search Algorithm Correctness›

fun binary_search :: "nat list ⇒ nat ⇒ nat option" where
  "binary_search [] target = None" |
  "binary_search [x] target = (if x = target then Some 0 else None)" |
  "binary_search xs target = (
    let mid = length xs div 2;
        mid_val = xs ! mid
    in if mid_val = target then Some mid
       else if mid_val < target then
         (case binary_search (drop (mid + 1) xs) target of
            None ⇒ None
          | Some idx ⇒ Some (mid + 1 + idx))
       else binary_search (take mid xs) target)"

lemma sorted_nth_mono:
  assumes "sorted xs" "i < length xs" "j < length xs" "i ≤ j"
  shows "xs ! i ≤ xs ! j"
  using assms by (simp add: sorted_nth_mono)

lemma binary_search_correct_aux:
  assumes "sorted xs" "target ∈ set xs"
  shows "∃i. binary_search xs target = Some i ∧ xs ! i = target"
  using assms
proof (induction xs arbitrary: target rule: binary_search.induct)
  case (1 target)
  then show ?case by simp
next
  case (2 x target)
  then show ?case by (cases "x = target") auto
next
  case (3 xs target)
  let ?mid = "length xs div 2"
  let ?mid_val = "xs ! ?mid"
  
  show ?case
  proof (cases "?mid_val = target")
    case True
    then show ?thesis by simp
  next
    case False
    show ?thesis
    proof (cases "?mid_val < target")
      case True
      have "target ∈ set (drop (?mid + 1) xs)"
        using 3.prems False True by (auto simp: sorted_nth_mono)
      then obtain idx where "binary_search (drop (?mid + 1) xs) target = Some idx"
        using 3.IH by blast
      then show ?thesis using True by auto
    next
      case False
      then have "?mid_val > target" using False by simp
      have "target ∈ set (take ?mid xs)"
        using 3.prems False ‹?mid_val > target› by (auto simp: sorted_nth_mono)
      then obtain idx where "binary_search (take ?mid xs) target = Some idx"
        using 3.IH by blast
      then show ?thesis by auto
    qed
  qed
qed

theorem binary_search_correct:
  assumes "sorted xs" "target ∈ set xs"
  shows "binary_search xs target ≠ None"
  using binary_search_correct_aux[OF assms] by auto

text ‹Complexity Analysis›

fun binary_search_complexity :: "nat list ⇒ nat ⇒ nat" where
  "binary_search_complexity [] target = 0" |
  "binary_search_complexity [x] target = 1" |
  "binary_search_complexity xs target = (
    let mid = length xs div 2
    in 1 + (if length xs = 1 then 0
           else if target < xs ! mid then binary_search_complexity (take mid xs) target
           else binary_search_complexity (drop (mid + 1) xs) target))"

lemma binary_search_complexity_log:
  assumes "xs ≠ []"
  shows "binary_search_complexity xs target ≤ log 2 (length xs) + 1"
  using assms
proof (induction xs arbitrary: target rule: binary_search_complexity.induct)
  case (1 target)
  then show ?case by simp
next
  case (2 x target)
  then show ?case by simp
next
  case (3 xs target)
  let ?mid = "length xs div 2"
  have "?mid ≤ length xs div 2" by simp
  have "length (take ?mid xs) ≤ length xs div 2" by simp
  have "length (drop (?mid + 1) xs) ≤ length xs div 2" by simp
  
  show ?case
  proof (cases "length xs = 1")
    case True
    then show ?thesis by simp
  next
    case False
    have "binary_search_complexity xs target = 
          1 + (if target < xs ! ?mid then binary_search_complexity (take ?mid xs) target
              else binary_search_complexity (drop (?mid + 1) xs) target)"
      using False by simp
    also have "… ≤ 1 + (log 2 (length xs div 2) + 1)"
      using 3.IH[of "take ?mid xs" target] 3.IH[of "drop (?mid + 1) xs" target]
      by (auto simp: log_mult)
    also have "… = log 2 (length xs) + 1"
      by (simp add: log_mult)
    finally show ?thesis .
  qed
qed

end
```

### Isabelle/HOL Proof for Data Structure Verification

```isabelle
theory Red_Black_Tree_Verification
imports Main
begin

text ‹Red-Black Tree Data Structure Verification›

datatype color = Red | Black

datatype 'a rbtree = Leaf | Node color "'a rbtree" 'a "'a rbtree"

fun height :: "'a rbtree ⇒ nat" where
  "height Leaf = 0" |
  "height (Node _ l _ r) = Suc (max (height l) (height r))"

fun black_height :: "'a rbtree ⇒ nat" where
  "black_height Leaf = 1" |
  "black_height (Node Black l _ r) = Suc (black_height l)" |
  "black_height (Node Red l _ r) = black_height l"

fun is_rbtree :: "'a rbtree ⇒ bool" where
  "is_rbtree Leaf = True" |
  "is_rbtree (Node c l x r) = (
    (c = Black ∨ is_rbtree l ∧ is_rbtree r) ∧
    black_height l = black_height r ∧
    is_rbtree l ∧ is_rbtree r)"

fun balance :: "color ⇒ 'a rbtree ⇒ 'a ⇒ 'a rbtree ⇒ 'a rbtree" where
  "balance Black (Node Red (Node Red a x b) y c) z d =
     Node Red (Node Black a x b) y (Node Black c z d)" |
  "balance Black (Node Red a x (Node Red b y c)) z d =
     Node Red (Node Black a x b) y (Node Black c z d)" |
  "balance Black a x (Node Red (Node Red b y c) z d) =
     Node Red (Node Black a x b) y (Node Black c z d)" |
  "balance Black a x (Node Red b y (Node Red c z d)) =
     Node Red (Node Black a x b) y (Node Black c z d)" |
  "balance color l x r = Node color l x r"

fun rbtree_insert :: "'a::linorder ⇒ 'a rbtree ⇒ 'a rbtree" where
  "rbtree_insert x Leaf = Node Red Leaf x Leaf" |
  "rbtree_insert x (Node color l y r) = (
    if x < y then balance color (rbtree_insert x l) y r
    else if x > y then balance color l y (rbtree_insert x r)
    else Node color l y r)"

lemma balance_preserves_black_height:
  "black_height (balance color l x r) = black_height (Node color l x r)"
  by (cases "(color, l, x, r)" rule: balance.cases) auto

lemma balance_preserves_is_rbtree:
  assumes "is_rbtree l" "is_rbtree r"
  shows "is_rbtree (balance color l x r)"
  using assms
  by (cases "(color, l, x, r)" rule: balance.cases) auto

lemma rbtree_insert_preserves_is_rbtree:
  assumes "is_rbtree t"
  shows "is_rbtree (rbtree_insert x t)"
  using assms
proof (induction t)
  case Leaf
  then show ?case by simp
next
  case (Node color l y r)
  have "is_rbtree (rbtree_insert x (Node color l y r))" if "x ≠ y"
  proof -
    have "is_rbtree (rbtree_insert x l)" using Node.IH(1) by simp
    have "is_rbtree (rbtree_insert x r)" using Node.IH(2) by simp
    then show ?thesis
      using balance_preserves_is_rbtree[OF ‹is_rbtree (rbtree_insert x l)› ‹is_rbtree (rbtree_insert x r)›]
      by (cases "x < y") auto
  qed
  then show ?case by auto
qed

lemma rbtree_insert_correct:
  assumes "is_rbtree t"
  shows "is_rbtree (rbtree_insert x t)"
  using rbtree_insert_preserves_is_rbtree[OF assms] by simp

text ‹Verification using Isar structured proofs›

theorem rbtree_insert_maintains_properties:
  assumes "is_rbtree t"
  shows "is_rbtree (rbtree_insert x t) ∧ 
         black_height (rbtree_insert x t) = black_height t"
proof -
  have "is_rbtree (rbtree_insert x t)"
    using assms by (rule rbtree_insert_correct)
  
  have "black_height (rbtree_insert x t) = black_height t"
  proof (cases t)
    case Leaf
    then show ?thesis by simp
  next
    case (Node color l y r)
    have "black_height (rbtree_insert x (Node color l y r)) = black_height (Node color l y r)"
    proof (cases "x = y")
      case True
      then show ?thesis by simp
    next
      case False
      have "black_height (rbtree_insert x l) = black_height l"
        using Node.IH(1) by simp
      have "black_height (rbtree_insert x r) = black_height r"
        using Node.IH(2) by simp
      then show ?thesis
        using balance_preserves_black_height
        by (cases "x < y") auto
    qed
    then show ?thesis using Node by simp
  qed
  
  then show ?thesis using ‹is_rbtree (rbtree_insert x t)› by simp
qed

end
```

## Input Format

### Isabelle/HOL Proof Specification

```yaml
isabelle_hol_specification:
  theory_name: string             # Name of the Isabelle theory
  imports: array                  # List of theories to import
  
  definitions:
    - definition_name: string
      definition_type: "definition|fun|datatype|record"
      content: string             # Isabelle definition content
      
    - definition_name: string
      definition_type: "definition|fun|datatype|record"
      content: string
  
  lemmas:
    - lemma_name: string
      statement: string           # Isabelle lemma statement
      proof_strategy: string      # Proof strategy to use
      
    - lemma_name: string
      statement: string
      proof_strategy: string
  
  theorems:
    - theorem_name: string
      statement: string           # Isabelle theorem statement
      proof_method: string        # Main proof method
      dependencies: array         # Dependencies on lemmas/theorems
      
    - theorem_name: string
      statement: string
      proof_method: string
      dependencies: array
  
  verification_goals:
    - goal_name: string
      goal_type: "correctness|safety|liveness"
      specification: string       # Formal specification
      
    - goal_name: string
      goal_type: "correctness|safety|liveness"
      specification: string
```

### Isabelle Development Configuration

```yaml
isabelle_development_config:
  project_name: string
  isabelle_version: string        # Required Isabelle version
  
  theories:
    - theory_name: string
      file_path: string
      dependencies: array
      exports: array              # What this theory exports
      
    - theory_name: string
      file_path: string
      dependencies: array
      exports: array
  
  automation:
    sledgehammer_enabled: boolean # Enable Sledgehammer automation
    metis_timeout: number         # Timeout for metis prover
    custom_tactics: array         # Custom Isar tactics
    
  performance:
    parallel_proofs: boolean      # Enable parallel proof checking
    memory_limit: string          # Memory limit for proof checking
    timeout_limit: number         # Timeout limit in seconds
```

## Output Format

### Isabelle/HOL Proof Output

```yaml
isabelle_hol_output:
  theory_name: string
  proof_status: "proved|disproved|open|timeout"
  proof_time: number              # Time taken for proof
  
  if proof_status == "proved":
    proof_script: string          # Generated Isabelle proof script
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

### Isabelle Development Report

```yaml
isabelle_development_report:
  project_summary:
    theories_count: number
    theorems_proved: number
    lemmas_used: number
    definitions_created: number
    
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

### Proof Methods

```yaml
proof_methods:
  isar_structured:
    description: "Structured Isar proofs for readability"
    best_for: ["complex_proofs", "maintainable_developments"]
    complexity: "medium"
    automation_level: "semi_automatic"
    
  sledgehammer:
    description: "Automated proof search with external provers"
    best_for: ["complex_goals", "automated_reasoning"]
    complexity: "high"
    automation_level: "automatic"
    
  metis:
    description: "First-order proof method"
    best_for: ["first_order_goals", "logical_deduction"]
    complexity: "medium"
    automation_level: "automatic"
    
  auto:
    description: "Built-in Isabelle automation"
    best_for: ["simple_goals", "basic_reasoning"]
    complexity: "low"
    automation_level: "automatic"
```

### HOL-Specific Features

```yaml
hol_features:
  higher_order_logic:
    description: "Higher-order logic reasoning capabilities"
    best_for: ["mathematical_theories", "functional_programming"]
    complexity: "high"
    development_effort: "high"
    
  type_classes:
    description: "Type class system for polymorphism"
    best_for: ["algebraic_structures", "generic_programming"]
    complexity: "medium"
    development_effort: "medium"
    
  locales:
    description: "Locale system for modular development"
    best_for: ["mathematical_structures", "modular_theories"]
    complexity: "medium"
    development_effort: "medium"
    
  code_generation:
    description: "Code generation from HOL specifications"
    best_for: ["executable_specifications", "verification"]
    complexity: "medium"
    development_effort: "medium"
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
  theory_conflict:
    detection_strategy: "dependency_analysis"
    recovery_strategy: "theory_resolution"
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

```isabelle
(* Optimization: Proof script optimization *)
lemma optimized_proof:
  assumes "P ⟶ Q" "Q ⟶ R"
  shows "P ⟶ R"
  using assms by blast

(* Optimization: Tactic performance *)
lemma fast_proof:
  fixes x y z :: nat
  assumes "x ≤ y" "y ≤ z"
  shows "x ≤ z"
  using assms by (auto simp: le_trans)

(* Optimization: Memory usage *)
lemma memory_efficient_proof:
  fixes xs :: "nat list"
  assumes "sorted xs"
  shows "distinct xs ⟷ (∀i < length xs - 1. xs ! i < xs ! (i + 1))"
  using assms by (induction xs rule: sorted.induct) auto

(* Optimization: Parallel proof checking *)
ML ‹
  fun parallel_proof_check proofs =
    let
      val results = Par_List.map prove_goal proofs
    in
      results
    end
›
```

### Development Optimization

```yaml
development_optimizations:
  incremental_compilation:
    technique: "isabelle_build"
    compilation_strategy: "dependency_tracking"
    rebuild_efficiency: "high"
    
  proof_caching:
    technique: "isabelle_session"
    cache_strategy: "persistent_storage"
    cache_hit_rate: "variable"
    
  parallel_processing:
    technique: "multithreaded"
    parallelization_strategy: "theory_level"
    speedup_factor: "depends_on_theories"
    
  memory_management:
    technique: "garbage_collection"
    memory_strategy: "lazy_evaluation"
    memory_reduction: "significant"
```

## Integration Examples

### With Formal Verification

```isabelle
theory Software_Verification
imports Main
begin

text ‹Software Verification Framework›

record program_state =
  variables :: "string ⇒ nat"
  memory :: "nat ⇒ nat"

definition program_spec :: "program_state ⇒ program_state ⇒ bool" where
  "program_spec pre post ⟷ 
   (∀var. variables pre var = variables post var) ∧
   (∀addr. memory pre addr = memory post addr)"

definition verification_framework :: "bool" where
  "verification_framework ⟷ 
   (∀pre post. program_spec pre post ⟶ program_correct pre post)"

text ‹Example: Verified sorting algorithm›

fun verified_sort :: "nat list ⇒ nat list" where
  "verified_sort [] = []" |
  "verified_sort (x # xs) = insert x (verified_sort xs)"

lemma verified_sort_correct:
  "sorted (verified_sort xs) ∧ mset (verified_sort xs) = mset xs"
  by (induction xs) auto

end
```

### With Mathematical Libraries

```isabelle
theory Mathematical_Integration
imports "HOL-Analysis.Analysis" "HOL-Algebra.Ring"
begin

text ‹Integration with Mathematical Libraries›

(* Real analysis integration *)
theorem fundamental_theorem_calculus:
  fixes f :: "real ⇒ real"
  assumes "continuous_on {a..b} f" "∀x∈{a..b}. (F has_vector_derivative f x) (at x within {a..b})"
  shows "((λx. f x) has_integral F b - F a) {a..b}"
  using assms by (rule fundamental_theorem_of_calculus)

(* Algebraic structure integration *)
instance real :: field
  by standard (auto simp: field_simps)

(* Ring theory integration *)
interpretation real_ring: ring "real" "op +" "op *" "uminus" "0" "1"
  by unfold_locales auto

end
```

## Best Practices

1. **Proof Design**:
   - Use clear, descriptive names for lemmas and theorems
   - Document proof strategies and key insights
   - Structure proofs hierarchically with well-defined lemmas
   - Use appropriate levels of automation

2. **Isar Structured Proofs**:
   - Write readable, maintainable proofs using Isar language
   - Use proper indentation and formatting
   - Document proof steps clearly
   - Apply structured proof methods

3. **HOL Type System**:
   - Leverage HOL's type system for correctness
   - Use type classes for modularity
   - Apply locales for structured development
   - Use code generation for executable specifications

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

```isabelle
(* Debug mode: Enhanced debugging *)
ML ‹
  fun debug_proof goal =
    let
      val _ = writeln ("Debugging goal: " ^ Syntax.string_of_term @{context} goal)
      val result = prove_goal goal
    in
      result
    end
›

(* Performance profiling *)
ML ‹
  fun profile_proof proof_fn =
    let
      val start = Time.now()
      val result = proof_fn()
      val end_time = Time.now()
      val elapsed = Time.- (end_time, start)
      val _ = writeln ("Proof time: " ^ Time.toString elapsed)
    in
      result
    end
›
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
    theories_created: number
    definitions_used: number
    dependencies_managed: number
```

## Dependencies

- **Isabelle System**: Isabelle/HOL proof assistant with appropriate version
- **Mathematical Libraries**: Analysis, Algebra, Number Theory libraries
- **Automation Tools**: Sledgehammer, metis, blast, auto
- **Development Tools**: Isabelle/jEdit, Proof General, VS Code extensions
- **Integration Frameworks**: APIs for connecting Isabelle with other verification tools

## Version History

- **1.0.0**: Initial release with comprehensive Isabelle/HOL theorem proving frameworks
- **1.1.0**: Added advanced automation techniques and Isar structured proofs
- **1.2.0**: Enhanced integration with formal verification and mathematical libraries
- **1.3.0**: Improved performance optimization and parallel proof checking
- **1.4.0**: Advanced proof search strategies and HOL-specific optimizations

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.