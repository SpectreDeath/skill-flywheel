---
Domain: logic
Version: 2.0.0
Complexity: Advanced
Type: Process
Category: Development
Estimated Execution Time: 100ms - 5 minutes
name: clojure-programmer
surfaces: [python, prolog, hy]
description: "Clojure code generation for agent systems using functional patterns, immutable state, and concurrent pipelines. Reasoning surfaces handle symbolic constraint logic (Prolog) and heuristic payoff/strategy evaluation (Hy). Python handles I/O and dispatches to the appropriate surface. Use when building agent systems, logic programming constructs, async pipelines, or DSLs in Clojure."
---

# Clojure Programmer Skill

## Purpose

Generate Clojure code for agent systems. Symbolic rules (domination, alliance, strategy
constraints) are resolved by the Prolog surface. Heuristic judgments (payoff scoring,
strategy ranking, timeline comparison) are resolved by the Hy surface. Python assembles
inputs, dispatches, and formats outputs.

## When to Use

- Building agent systems with immutable state management
- Implementing relational/logic programming constructs (core.logic targets)
- Creating concurrent data processing pipelines (core.async)
- DSL creation and code-as-data patterns
- Strategy evaluation with payoff matrices

## When NOT to Use

- When JVM/Java interop is not available in the target environment
- Simple scripts better handled in pure Python
- Performance-critical mutable state work

---

## Input Format

```yaml
clojure_request:
  task: string              # Task description
  use_case: string          # "agent-state" | "logic" | "async" | "dsl" | "strategy"
  requires: array           # ["core.logic", "core.async"]
  agents: array             # Optional: agent descriptors for logic/strategy use cases
  strategies: array         # Optional: strategy names for payoff evaluation
```

## Output Format

```yaml
clojure_result:
  code: string              # Generated Clojure code
  deps: array               # Required lein/deps.edn dependencies
  reasoning:
    constraints_used: array # Which Prolog goals fired
    heuristics_used: array  # Which Hy evaluations contributed
  explanation: string
```

---

## Prolog Surface — Symbolic Constraint Logic

Handles hard rules: domination relations, alliance validity, strategy legality,
agent classification. Called by Python via Janus before code generation when
the use_case involves logic, agent relationships, or strategy constraints.

```prolog
% ── Agent Classification ─────────────────────────────────────────────────────

agent_type(Agent, hawk) :-
    aggressive(Agent),
    resource_advantage(Agent).

agent_type(Agent, dove) :-
    \+ aggressive(Agent).

agent_type(Agent, retreat) :-
    aggressive(Agent),
    \+ resource_advantage(Agent).

% ── Domination Relations ──────────────────────────────────────────────────────

dominates(Player, Opponent) :-
    agent_type(Player, hawk),
    agent_type(Opponent, dove).

dominates(Player, Opponent) :-
    resource_advantage(Player),
    \+ resource_advantage(Opponent).

% ── Alliance Validity ─────────────────────────────────────────────────────────

valid_alliance(P1, P2) :-
    diplomatic_relation(P1, P2),
    \+ at_war(P1, P2),
    \+ dominates(P1, P2),
    \+ dominates(P2, P1).

% ── Strategy Legality ─────────────────────────────────────────────────────────

legal_strategy(Player, attack) :-
    agent_type(Player, hawk),
    dominates(Player, _).

legal_strategy(Player, negotiate) :-
    valid_alliance(Player, _).

legal_strategy(Player, retreat) :-
    \+ dominates(Player, _).

legal_strategy(_, wait).     % always legal

% ── core.logic Template Selection ────────────────────────────────────────────
% Determines which core.logic pattern to emit in generated Clojure code.

use_defrel(Task) :-
    requires_relation(Task).

use_defrule(Task) :-
    requires_inference(Task).

use_run(Task, N) :-
    requires_query(Task),
    query_limit(Task, N).
```

---

## Hy Surface — Heuristic Evaluation

Handles soft judgment: payoff scoring, strategy ranking, timeline comparison,
resource weighting. Called by Python via Hy runtime when use_case involves
strategy evaluation or comparative analysis.

```hy
;; ── Payoff Matrix ─────────────────────────────────────────────────────────────

(setv payoff-matrix
  {"hawk"    {"hawk" -25  "dove" 50   "retreat" 0}
   "dove"    {"hawk" 0    "dove" 25   "retreat" 10}
   "retreat" {"hawk" -10  "dove" 5    "retreat" 15}})

(defn get-payoff [my-action opp-action]
  (-> payoff-matrix
      (.get my-action {})
      (.get opp-action 0)))

;; ── Strategy Scoring ──────────────────────────────────────────────────────────

(defn score-strategy [strategy opponent-distribution]
  "Score a strategy against a probability distribution of opponent strategies.
   opponent-distribution: dict of {strategy: probability}"
  (sum (lfor [opp-strat prob] (.items opponent-distribution)
             (* prob (get-payoff strategy opp-strat)))))

(defn rank-strategies [strategies opponent-distribution]
  "Return strategies sorted by expected payoff descending."
  (sorted strategies
          :key (fn [s] (score-strategy s opponent-distribution))
          :reverse True))

;; ── Timeline Comparison ───────────────────────────────────────────────────────

(defn score-timeline [timeline player weights]
  "Score a timeline branch for a player given feature weights.
   weights: dict of {feature: weight}"
  (sum (lfor [feature weight] (.items weights)
             (* weight (.get (timeline.get player {}) feature 0)))))

(defn compare-timelines [timelines player weights]
  "Return timelines sorted by score descending with scores attached."
  (sorted
    (lfor t timelines
          {"timeline" t
           "score" (score-timeline t player weights)})
    :key (fn [x] (get x "score"))
    :reverse True))

;; ── Resource Advantage Heuristic ─────────────────────────────────────────────

(defn resource-advantage? [agent-a agent-b threshold]
  "Heuristic: does agent-a have meaningful resource advantage over agent-b?"
  (let [ra (.get agent-a "resources" 0)
        rb (.get agent-b "resources" 0)]
    (> (- ra rb) threshold)))

;; ── Template Selector ─────────────────────────────────────────────────────────

(defn select-async-pattern [buffer-size subscriber-count]
  "Heuristically select core.async pattern based on load characteristics."
  (cond
    (> subscriber-count 10) "pub-sub"
    (> buffer-size 100)     "pipeline"
    True                    "basic-chan"))
```

---

## Python Surface — Hands

Entry point. Parses input, calls Prolog surface for constraint resolution,
calls Hy surface for heuristic evaluation, assembles and returns generated
Clojure code.

```python
from janus_swi import query_once, consult
import hy
import hy.importer
from pathlib import Path

# ── Runtime Setup ──────────────────────────────────────────────────────────────

def load_surfaces(skill_dir: str):
    """Load Prolog clauses and Hy heuristics from skill surfaces."""
    consult(f"{skill_dir}/clojure-programmer.pl")
    hy.importer.runhy.run_path(f"{skill_dir}/clojure-programmer.hy")

# ── Prolog Dispatch ────────────────────────────────────────────────────────────

def resolve_constraints(task: dict) -> dict:
    """Query Prolog surface for constraint resolution."""
    results = {}

    # Classify agents
    agents = task.get("agents", [])
    classifications = {}
    for agent in agents:
        r = query_once(f"agent_type({agent['id']}, Type)")
        if r:
            classifications[agent["id"]] = r["Type"]
    results["agent_types"] = classifications

    # Resolve legal strategies
    legal = {}
    for agent_id in classifications:
        r = list(query_once(f"legal_strategy({agent_id}, S)") or [])
        legal[agent_id] = [x["S"] for x in r] if r else ["wait"]
    results["legal_strategies"] = legal

    # Select core.logic template
    use_case = task.get("use_case", "")
    r = query_once(f"use_defrel({use_case})")
    results["use_defrel"] = bool(r)
    r = query_once(f"use_defrule({use_case})")
    results["use_defrule"] = bool(r)

    return results

# ── Hy Dispatch ───────────────────────────────────────────────────────────────

def evaluate_heuristics(task: dict, constraints: dict) -> dict:
    """Call Hy surface for heuristic evaluation."""
    from clojure_programmer_hy import rank_strategies, select_async_pattern

    results = {}

    strategies = task.get("strategies", [])
    if strategies:
        # Assume uniform opponent distribution if not provided
        opp_dist = task.get("opponent_distribution",
                            {s: 1/len(strategies) for s in strategies})
        results["ranked_strategies"] = rank_strategies(strategies, opp_dist)

    if task.get("use_case") == "async":
        buffer = task.get("buffer_size", 32)
        subs = task.get("subscriber_count", 1)
        results["async_pattern"] = select_async_pattern(buffer, subs)

    return results

# ── Code Assembly ─────────────────────────────────────────────────────────────

def generate_clojure(task: dict, constraints: dict, heuristics: dict) -> str:
    """Assemble Clojure code from constraint and heuristic results."""
    use_case = task.get("use_case", "agent-state")
    lines = [f"(ns {task.get('ns', 'agent.core')})"]

    if "core.logic" in task.get("requires", []):
        lines.append("(require '[clojure.core.logic :as logic])")
        if constraints.get("use_defrel"):
            lines.append(DEFREL_TEMPLATE)
        if constraints.get("use_defrule"):
            lines.append(DEFRULE_TEMPLATE)

    if "core.async" in task.get("requires", []):
        lines.append("(require '[clojure.core.async :as async])")
        pattern = heuristics.get("async_pattern", "basic-chan")
        lines.append(ASYNC_TEMPLATES[pattern])

    if use_case == "agent-state":
        lines.append(AGENT_STATE_TEMPLATE)

    return "\n\n".join(lines)

# ── Entry Point ───────────────────────────────────────────────────────────────

def execute(task: dict, skill_dir: str = ".") -> dict:
    load_surfaces(skill_dir)
    constraints = resolve_constraints(task)
    heuristics  = evaluate_heuristics(task, constraints)
    code        = generate_clojure(task, constraints, heuristics)

    return {
        "clojure_result": {
            "code": code,
            "deps": _resolve_deps(task),
            "reasoning": {
                "constraints_used": list(constraints.keys()),
                "heuristics_used":  list(heuristics.keys()),
            },
            "explanation": f"Generated {task.get('use_case')} pattern "
                           f"with {len(constraints)} constraint resolutions "
                           f"and {len(heuristics)} heuristic evaluations."
        }
    }

def _resolve_deps(task: dict) -> list:
    deps = ["[org.clojure/clojure \"1.11.1\"]"]
    if "core.logic" in task.get("requires", []):
        deps.append("[org.clojure/core.logic \"1.0.0\"]")
    if "core.async" in task.get("requires", []):
        deps.append("[org.clojure/core.async \"1.6.0\"]")
    return deps
```

---

## Clojure Templates (Python constants)

These are the code-as-data payloads Python assembles into generated output.
They are Clojure strings, not executed locally.

```python
AGENT_STATE_TEMPLATE = """
(defrecord Agent [id strategy resources history beliefs tom-level])

(defn create-agent [id strategy-type resources]
  (->Agent id strategy-type resources [] [] 0))

(defn update-belief [agent belief]
  (update agent :beliefs conj belief))
"""

DEFREL_TEMPLATE = """
(logic/defrel strategy-decides ?player ?strategy ?action)
(logic/defrel dominated ?dominator ?dominated)
(logic/defrel alliance ?player1 ?player2)
"""

DEFRULE_TEMPLATE = """
(logic/defrule hawk-dominates
  ([player opp]
   (hawk? player)
   (resources> player opp)))

(logic/defrule alliance-formed
  ([p1 p2]
   (alliance p1 p2)
   (diplomatic-relation p1 p2)))
"""

ASYNC_TEMPLATES = {
    "basic-chan": """
(defrecord EventStream [channel subscribers buffer-size])

(defn create-stream [buffer-size]
  (->EventStream (async/chan buffer-size) #{} buffer-size))
""",
    "pipeline": """
(->> source-chan
     (async/pipe transform-fn)
     (async/pipe sink-chan))
""",
    "pub-sub": """
(def pub-chan (async/chan 256))
(def publication (async/pub pub-chan :topic))

(defn subscribe-topic [topic]
  (let [sub-chan (async/chan 32)]
    (async/sub publication topic sub-chan)
    sub-chan))
"""
}
```

---

## Error Handling

```python
# Prolog surface failure — degrade gracefully to defaults
try:
    constraints = resolve_constraints(task)
except Exception as e:
    constraints = {"agent_types": {}, "legal_strategies": {}, "error": str(e)}

# Hy surface failure — skip heuristics, use first available strategy
try:
    heuristics = evaluate_heuristics(task, constraints)
except Exception as e:
    heuristics = {"ranked_strategies": task.get("strategies", []), "error": str(e)}
```

---

## Implementation Notes

- Prolog surface is **authoritative** for hard constraints — if Prolog rejects a strategy
  as illegal, Python does not generate code for it regardless of heuristic score.
- Hy surface is **advisory** — heuristic rankings influence template selection and
  ordering but do not override constraint results.
- Python surface is **stateless** — all context passed in via task dict, no shared
  mutable state between calls.
- Clojure templates are **inert strings** — they are not executed locally, only
  assembled and returned as output.

## Constraints

- MUST consult Prolog surface before generating logic/strategy code
- ALWAYS provide fallback when either reasoning surface fails
- NEVER allow Hy heuristic output to override a Prolog constraint violation
- STOP and return error if task use_case is unrecognized

## Version History

- **1.0.0**: Initial Clojure programmer skill (single Python surface)
- **2.0.0**: Three-surface refactor — Prolog for symbolic constraints,
             Hy for heuristic evaluation, Python for I/O and dispatch
