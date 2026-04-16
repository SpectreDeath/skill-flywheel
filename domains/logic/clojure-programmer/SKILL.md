---
Domain: logic
Version: 1.0.0
Complexity: Advanced
Type: Process
Category: Development
Estimated Execution Time: 100ms - 5 minutes
name: clojure-programmer
---

## Description

Clojure programming for agent systems with emphasis on functional patterns, immutable state, core.logic (miniKanren) for relational programming, and core.async for concurrent data streams. Based on patterns from Strategify's Clojure implementation.

## Purpose

To provide guidance for building agent systems in Clojure, leveraging its strengths in immutable data, concurrent programming, and Lisp-style meta-programming.

## When to Use

- Building agent systems with immutable state management
- Implementing relational/logic programming (via core.logic)
- Creating concurrent data processing pipelines (core.async)
- DSL creation and code-as-data patterns
- Symbol manipulation and reflective programming

## When NOT to Use

- When Java interop or JVM is not available
- Performance-critical code requiring mutable state
- Simple scripts better handled in Python/JS

## Input Format

```yaml
clojure_request:
  task: string              # Task description
  use_case: string          # "agent-state", "logic", "async", "dsl"
  requires: array           # ["core.logic", "core.async"]
```

## Output Format

```yaml
clojure_result:
  code: string              # Generated Clojure code
  deps: array               # Required dependencies
  explanation: string
```

## Capabilities

### 1. Immutable Agent State

```clojure
(defrecord Agent [id strategy resources history beliefs tom-level])

(defn create-agent [id strategy-type resources]
  (->Agent id strategy-type resources [] [] 0))

(defn update-belief [agent belief]
  (update agent :beliefs conj belief))
```

### 2. core.logic (miniKanren) - Prolog-style Rules

```clojure
(require '[clojure.core.logic :as logic])

;; Define relations
(logic/defrel strategy-decides ?player ?strategy ?action)
(logic/defrel dominated ?dominator ?dominated)
(logic/defrel alliance ?player1 ?player2)

;; Rules using defrule
(logic/defrule hawk-dominates
  ([player opp]
   (hawk? player)
   (resources> player opp)))

(logic/defrule alliance-formed
  ([p1 p2]
   (alliance p1 p2)
   (diplomatic-relation p1 p2)))

;; Query
(logic/run 1 [q]
  (logic/fresh [p s a]
    (strategy-decides p s a)
    (logic/== q {:player p :strategy s :action a})))
```

### 3. core.async Concurrent Pipelines

```clojure
(require '[clojure.core.async :as async])

(defrecord EventStream [channel subscribers buffer-size])

(defn create-stream [buffer-size]
  (->EventStream (async/chan buffer-size) #{} buffer-size))

(defn subscribe [stream handler]
  (async/>!! (:channel stream) handler)
  stream)

(defn publish [stream event]
  (async/>!! (:channel stream) event)
  stream)

;; Pipeline example
(->> source-chan
     (async/pipe transform-fn)
     (async/pipe sink-chan))
```

### 4. Timeline Branching (Counterfactual)

```clojure
(defn branch-timeline [state move]
  "Create a new timeline branch without modifying original"
  (apply-move state move))

(defn branch-timelines [state possible-moves]
  (map #(apply-move state %) possible-moves))

(defn compare-timelines [timelines player scorer]
  (map #(scorer % player) timelines))
```

### 5. DSL Creation (Code as Data)

```clojure
;; Macro for strategy definition
(defmacro defstrategy [name & body]
  `(def ~name (fn ~@body)))

(defstrategy hawk
  [state player]
  (let [opp (opponent player)]
    (if (dominates? state player opp)
      :attack
      :retreat)))

;; Quoted data as code
'(+ 1 2)  ; Data
(eval '(+ 1 2))  ; Code
```

### 6. Payoff Matrix Pattern

```clojure
(def ^:private payoff-matrix
  {:hawk   {:hawk -25 :dove 50 :retreat 0}
   :dove   {:hawk 0   :dove 25 :retreat 10}
   :retreat {:hawk -10 :dove 5  :retreat 15}})

(defn get-payoff [my-action opp-action]
  (get-in payoff-matrix [my-action opp-action] 0))
```

## Implementation Notes

- Use `->` threading for readable data transformations
- Prefer immutable data structures (vectors, maps, sets)
- Use atoms/refs/vars for mutable references when needed
- Leverage `core.logic` for constraint solving

## Dependencies

```clojure
;; project.clj
:dependencies [[org.clojure/clojure "1.11.1"]
               [org.clojure/core.logic "1.0.0"]
               [org.clojure/core.async "1.6.0"]]
```

## Best Practices

1. **Immutability First**: Use persistent data structures
2. **Threading**: Use `->` and `->>` for readability
3. **Lazy Sequences**: Process large data lazily
4. **Namespaces**: Organize code into focused modules
5. **REPL-Driven**: Iterate quickly in REPL

## Error Handling

```clojure
(try
  (execute-agent-strategy agent state)
  (catch Exception e
    (println "Agent error:" (.getMessage e))
    ;; Fallback behavior
    :retreat))
```

## Version History

- **1.0.0**: Initial Clojure programmer skill

## Constraints

- MUST use qualified keywords for namespaced keys
- ALWAYS provide fallback for logic failures
- STOP if async pipeline deadlocks (add timeout)