#!/usr/bin/env python3
"""
Simplicity Constraint

Enforces Karpathy's 'Simplicity First' principle:
- Minimum code that solves the problem
- No speculative features or over-engineering
- Prefer simpler solutions
"""

import logging
from typing import Any, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class PreCheckResult:
    passed: bool
    suggestions: list = None
    message: str = ""

    def __post_init__(self):
        if self.suggestions is None:
            self.suggestions = []


@dataclass
class PostCheckResult:
    passed: bool
    violation: str = ""
    severity: str = "warning"  # warning, error
    suggestion: str = ""
    automated_fix: Optional[str] = None


class SimplicityConstraint:
    """Enforces minimal complexity and avoidance of over-engineering."""
    
    def __init__(self, max_complexity: int = 10, prefer_minimal: bool = True):
        """
        Args:
            max_complexity: Maximum acceptable complexity score
            prefer_minimal: Whether to prefer minimal solutions
        """
        self.max_complexity = max_complexity
        self.prefer_minimal = prefer_minimal
    
    def pre_check(self, payload: Dict[str, Any], context: Dict[str, Any]) -> PreCheckResult:
        """
        Pre-execution check: Warn if likely to overcomplicate.
        
        Args:
            payload: Input parameters to the skill
            context: Behavioral profile context
            
        Returns:
            PreCheckResult with suggestions
        """
        suggestions = []
        
        # Heuristic: Simple-looking problems should have simple solutions
        if self._looks_simple(payload):
            suggestions.append(
                "Prefer minimal solution (< 50 lines of code)"
            )
            if self.prefer_minimal:
                suggestions.append(
                    "Consider simplest possible approach first"
                )
        
        # Check for common over-engineering patterns
        if self._has_over_engineering_risk(payload):
            suggestions.append(
                "Warning: Problem may tempt over-engineering - stay minimal"
            )
        
        return PreCheckResult(
            passed=True,  # Pre-checks don't fail, they warn
            suggestions=suggestions,
            message="Simplicity pre-check completed"
        )
    
    def post_check(self, result: Dict[str, Any], original_payload: Dict[str, Any]) -> PostCheckResult:
        """
        Post-execution check: Verify solution isn't over-engineered.
        
        Args:
            result: Skill output to validate
            original_payload: Original input parameters
            
        Returns:
            PostCheckResult with violations if any
        """
        complexity = self._measure_complexity(result)
        
        if complexity > self.max_complexity:
            return PostCheckResult(
                passed=False,
                violation=f"Solution complexity ({complexity}) exceeds threshold ({self.max_complexity})",
                severity="warning",
                suggestion=f"Simplify: reduce from {complexity} to < {self.max_complexity}",
                automated_fix=self._suggest_simplification(result)
            )
        
        # Check for unnecessary features
        unnecessary = self._detect_unnecessary_features(result, original_payload)
        if unnecessary:
            return PostCheckResult(
                passed=False,
                violation=f"Unnecessary features detected: {unnecessary}",
                severity="warning",
                suggestion="Remove features beyond what was requested",
            )
        
        return PostCheckResult(passed=True)
    
    def _looks_simple(self, payload: Dict[str, Any]) -> bool:
        """Heuristic: Does this look like a simple problem?"""
        # Small input sizes often indicate simple problems
        if "variables" in payload:
            return len(payload["variables"]) <= 5
        if "clauses" in payload:
            return len(payload["clauses"]) <= 3
        
        return False
    
    def _has_over_engineering_risk(self, payload: Dict[str, Any]) -> bool:
        """Detect patterns that often lead to over-engineering."""
        # Request for lots of flexibility/configurability
        if "flexible" in str(payload).lower():
            return True
        if "configurable" in str(payload).lower():
            return True
        
        return False
    
    def _measure_complexity(self, result: Dict[str, Any]) -> float:
        """
        Multi-dimensional complexity metric.
        
        Returns a float score where higher = more complex.
        """
        # Extract code if present
        code = result.get("generated_code", "") or result.get("code", "") or ""
        steps = result.get("reasoning_steps", []) or []
        components = result.get("components", []) or []
        
        # Cyclomatic complexity approximation
        branches = (
            code.count("if ") + code.count("elif ") + 
            code.count("for ") + code.count("while ") +
            code.count("except ")
        )
        
        # Conceptual complexity (reasoning steps)
        conceptual = len(steps)
        
        # Structural complexity (components/modules)
        structural = len(components)
        
        # Code volume
        volume = len([l for l in code.split("\n") if l.strip()])
        
        # Weighted combination
        score = (
            branches * 1.5 +      # Branches are expensive
            conceptual * 1.0 +     # Each step adds complexity
            structural * 2.0 +     # Components multiply complexity
            volume / 10.0          # Lines of code (diminishing returns)
        )
        
        return round(score, 2)
    
    def _detect_unnecessary_features(
        self, result: Dict[str, Any], payload: Dict[str, Any]
    ) -> list:
        """Detect features in result that weren't requested."""
        unnecessary = []
        
        # Check for common unnecessary additions
        result_str = str(result).lower()
        
        # These features are often added unnecessarily
        common_unnecessary = [
            "config",
            "setting",
            "option",
            "flexibility",
            "extensibility",
            "plugin",
            "hook",
        ]
        
        for feature in common_unnecessary:
            # Only flag if explicitly mentioned in result
            if feature in result_str:
                # Check if it was requested
                if feature not in str(payload).lower():
                    unnecessary.append(feature)
        
        return unnecessary
    
    def _suggest_simplification(self, result: Dict[str, Any]) -> Optional[str]:
        """Suggest specific simplifications for the solution."""
        code = result.get("generated_code", "") or result.get("code", "")
        
        if not code:
            return None
        
        suggestions = []
        
        # Too many branches?
        if code.count("if ") > 3:
            suggestions.append("Consider combining conditional checks")
        
        # Too many nested structures?
        if code.count("    ") > 10:  # Indentation levels
            suggestions.append("Flatten nested structures where possible")
        
        # Too long?
        if len(code.split("\n")) > 100:
            suggestions.append("Break into smaller, focused functions")
        
        if suggestions:
            return " | ".join(suggestions)
        
        return "Review for simpler approach opportunities"
    
    def to_prolog_rules(self) -> str:
        """
        Generate Prolog rules for this constraint.
        
        These rules can be consulted during reasoning to enforce simplicity.
        """
        return """
% === Simplicity Constraint Rules ===
% Enforces minimal complexity and avoids over-engineering

% Maximum allowed proof complexity
max_complexity(10).

% Compute complexity of a proof/plan
complexity(Proof, Score) :-
    length(Proof, Steps),
    num_distinct_clauses(Proof, Clauses),
    Score is Steps + Clauses * 2.

% Count distinct clauses used in a proof
num_distinct_clauses(Proof, Count) :-
    findall(Clause, (member(Step, Proof), uses_clause(Step, Clause)), Clauses),
    sort(Clauses, UniqueClauses),
    length(UniqueClauses, Count).

% Check if a solution is simplest possible
simplest_solution(Goal, Solution) :-
    findall(S, solve(Goal, S), Solutions),
    min_by_complexity(Solutions, Solution).

min_by_complexity([S], S).
min_by_complexity([S1, S2 | Rest], Min) :-
    complexity(S1, C1),
    complexity(S2, C2),
    (   C1 =< C2
    ->  min_by_complexity([S1 | Rest], Min)
    ;   min_by_complexity([S2 | Rest], Min)
    ).

% Warn about overcomplex solutions
check_simplicity(Solution) :-
    complexity(Solution, Score),
    max_complexity(Max),
    (   Score > Max
    ->  format('Warning: Solution complexity ~w exceeds threshold ~w~n', 
               [Score, Max])
    ;   true
    ).

% Prefer simpler options when multiple exist
prefer_simple(List, Simple) :-
    member(Simple, List),
    complexity(Simple, C),
    max_complexity(Max),
    C =< Max,
    !.

% Discard overly complex options
filter_complex(List, SimpleList) :-
    include(is_simple, List, SimpleList).

is_simple(Item) :-
    complexity(Item, C),
    max_complexity(Max),
    C =< Max.
        """
    
    def to_hy_heuristics(self) -> str:
        """
        Generate Hy/Lisp heuristics for this constraint.
        
        These provide runtime guidance for maintaining simplicity.
        """
        return """
;; === Simplicity Heuristics ===
;; Guide the system toward minimal, focused solutions

(defn calculate-complexity [solution]
  "Compute complexity score for a solution"
  (let [code (get solution :code "")
        steps (get solution :steps [])
        branches (count (re-seq (re-pattern #"(if|elif|for|while)") code))
        conceptual (count steps)
        volume (count (clojure.string/split-lines code))]
    (+ (* branches 1.5) conceptual (* volume 0.1))))

(defn check-simplicity [solution]
  "Verify solution meets simplicity threshold"
  (let [threshold 10
        score (calculate-complexity solution)]
    (if (> score threshold)
      (do
        (log-warning (str "Complex solution (score: " score ")"))
        {:passed false :score score :threshold threshold})
      {:passed true :score score})))

(defn prefer-minimal [solutions]
  "Return simplest solution from candidates"
  (first (sort-by calculate-complexity solutions)))

(defn suggest-simplification [solution]
  "Provide specific suggestions for simplification"
  (let [code (get solution :code "")
        suggestions []]
    (when (> (count (re-seq (re-pattern #"(if )") code)) 3)
      (conj suggestions "Combine conditional checks"))
    (when (> (count (clojure.string/split-lines code)) 100)
      (conj suggestions "Break into smaller functions"))
    suggestions))

(defn is-simple? [solution]
  "Check if solution meets simplicity criteria"
  (let [score (calculate-complexity solution)]
    (<= score 10)))
        """
