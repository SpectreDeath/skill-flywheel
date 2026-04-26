#!/usr/bin/env python3
"""
Assumptions Constraint

Enforces Karpathy's 'Think Before Coding' principle:
- Explicitly state all assumptions
- Surface confusion and uncertainties
- Don't hide behind implicit interpretations
"""

import logging
import re
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Assumption:
    """Represents a single assumption made during reasoning."""
    text: str
    type: str = "implicit"  # explicit, implicit, inferred
    status: str = "uncertain"  # certain, uncertain, testable, verified
    context: Optional[str] = None
    impact: str = "medium"  # low, medium, high


@dataclass
class AssumptionReport:
    """Report of all assumptions identified."""
    assumptions: List[Assumption] = field(default_factory=list)
    total_count: int = 0
    testable_count: int = 0
    critical_count: int = 0


@dataclass
class PreCheckResult:
    passed: bool
    assumptions_identified: List[Assumption] = field(default_factory=list)
    message: str = ""
    requires_clarification: bool = False
    clarification_questions: List[str] = field(default_factory=list)


class AssumptionsConstraint:
    """Enforces explicit and testable assumptions throughout reasoning."""
    
    def __init__(self, require_testable: bool = True, max_critical: int = 3):
        """
        Args:
            require_testable: Whether assumptions must be testable
            max_critical: Maximum allowed high-impact assumptions
        """
        self.require_testable = require_testable
        self.max_critical = max_critical
    
    def pre_check(self, payload: Dict[str, Any], context: Dict[str, Any] = None) -> PreCheckResult:
        """
        Pre-execution: Extract and validate assumptions from input.
        
        Args:
            payload: Input parameters to the skill
            context: Additional context
            
        Returns:
            PreCheckResult with identified assumptions
        """
        assumptions = self._extract_assumptions(payload)
        report = self._analyze_assumptions(assumptions)
        
        clarification_questions = []
        requires_clarification = False
        
        # Check for problematic assumptions
        if self.require_testable:
            untestable = [a for a in report.assumptions if a.status != "testable"]
            if untestable:
                requires_clarification = True
                clarification_questions.extend(
                    self._generate_clarifications(untestable)
                )
        
        if report.critical_count > self.max_critical:
            requires_clarification = True
            clarification_questions.append(
                f"{report.critical_count} high-impact assumptions detected. "
                "Can we reduce uncertainty?"
            )
        
        return PreCheckResult(
            passed=not requires_clarification,
            assumptions_identified=report.assumptions,
            message=f"Identified {len(assumptions)} assumption(s)",
            requires_clarification=requires_clarification,
            clarification_questions=clarification_questions,
        )
    
    def track_assumptions(self, reasoning_trace: List[str]) -> AssumptionReport:
        """
        Track assumptions throughout reasoning process.
        
        Args:
            reasoning_trace: List of reasoning steps
            
        Returns:
            Comprehensive assumption report
        """
        all_assumptions = []
        
        for step in reasoning_trace:
            step_assumptions = self._extract_from_step(step)
            all_assumptions.extend(step_assumptions)
        
        return self._analyze_assumptions(all_assumptions)
    
    def validate(self, assumptions: List[Assumption]) -> Dict[str, Any]:
        """
        Validate that assumptions are acceptable.
        
        Args:
            assumptions: List of assumptions to validate
            
        Returns:
            Validation result
        """
        report = self._analyze_assumptions(assumptions)
        
        passed = True
        issues = []
        
        if self.require_testable:
            untestable = [a for a in assumptions if a.status != "testable"]
            if untestable:
                passed = False
                issues.append({
                    "type": "untestable_assumptions",
                    "count": len(untestable),
                    "assumptions": [a.text for a in untestable[:3]],
                    "recommendation": "Make assumptions explicit and testable",
                })
        
        if report.critical_count > self.max_critical:
            passed = False
            issues.append({
                "type": "too_many_critical",
                "count": report.critical_count,
                "max_allowed": self.max_critical,
                "recommendation": "Reduce uncertainty or gather more information",
            })
        
        return {
            "passed": passed,
            "assumption_count": report.total_count,
            "critical_count": report.critical_count,
            "testable_count": report.testable_count,
            "issues": issues,
        }
    
    def _extract_assumptions(self, payload: Dict[str, Any]) -> List[Assumption]:
        """Extract assumptions from payload."""
        assumptions = []
        
        # Check for explicit assumption fields
        if "assumptions" in payload:
            for assump in payload["assumptions"]:
                assumptions.append(Assumption(
                    text=str(assump),
                    type="explicit",
                    status="testable",
                ))
        
        # Scan for uncertainty indicators in parameter descriptions
        indicators = [
            (r"(probably|likely|maybe|perhaps)", "implicit", "uncertain"),
            (r"(assume|assuming|given that)", "explicit", "uncertain"),
            (r"(should|could|might|may)", "implicit", "uncertain"),
        ]
        
        payload_str = str(payload).lower()
        for pattern, assump_type, status in indicators:
            for match in re.finditer(pattern, payload_str):
                context = match.group(0)
                # Extract surrounding text
                start = max(0, match.start() - 20)
                end = min(len(payload_str), match.end() + 20)
                text = payload_str[start:end].strip()
                
                assumptions.append(Assumption(
                    text=f"'{context}' in context: {text}",
                    type=assump_type,
                    status=status,
                ))
        
        return assumptions
    
    def _extract_from_step(self, step: str) -> List[Assumption]:
        """Extract assumptions from a reasoning step."""
        assumptions = []
        step_lower = step.lower()
        
        # Direct assumption statements
        if "assume" in step_lower or "assuming" in step_lower:
            assumptions.append(Assumption(
                text=step[:100],
                type="explicit",
                status="uncertain",
                context=step[:200],
            ))
        
        # Probabilistic language
        if any(word in step_lower for word in ["probably", "likely", "might"]):
            assumptions.append(Assumption(
                text=step[:100],
                type="implicit",
                status="uncertain",
                impact="medium",
            ))
        
        return assumptions
    
    def _analyze_assumptions(self, assumptions: List[Assumption]) -> AssumptionReport:
        """Analyze a list of assumptions."""
        testable = sum(1 for a in assumptions if a.status == "testable")
        critical = sum(1 for a in assumptions if a.impact == "high")
        
        return AssumptionReport(
            assumptions=assumptions,
            total_count=len(assumptions),
            testable_count=testable,
            critical_count=critical,
        )
    
    def _generate_clarifications(self, untestable: List[Assumption]) -> List[str]:
        """Generate clarification questions for untestable assumptions."""
        questions = []
        
        for assumption in untestable[:3]:  # Limit to first 3
            if assumption.type == "implicit":
                questions.append(
                    f"Is this implicit assumption '{assumption.text[:50]}...' valid?"
                )
            else:
                questions.append(
                    f"Can we test the assumption: {assumption.text[:50]}...?"
                )
        
        if not questions:
            questions.append(
                "There are untestable assumptions. Can we clarify them?"
            )
        
        return questions
    
    def to_prolog_rules(self) -> str:
        """
        Generate Prolog rules for assumption tracking and validation.
        """
        return """
% === Assumptions Constraint Rules ===
% Track and validate assumptions made during reasoning

% Declare an assumption with metadata
% assumption(Text, Type, Status, Impact)
% Type: explicit, implicit, inferred
% Status: certain, uncertain, testable, verified
% Impact: low, medium, high

% Check if all assumptions are valid
valid_assumptions :-
    findall(_, assumption(_, _, _, _), Assumptions),
    forall(member(Assumption, Assumptions),
           valid_assumption(Assumption)).

valid_assumption(assumption(Text, _, Status, _)) :-
    Status == testable, !.
valid_assumption(assumption(Text, explicit, _, _)) :-
    !, format('Note: Explicit assumption made: ~w~n', [Text]).
valid_assumption(assumption(Text, _, uncertain, high)) :-
    !, format('WARNING: High-impact uncertain assumption: ~w~n', [Text]).
valid_assumption(_).

% Count assumptions by type
count_assumptions(Type, Count) :-
    findall(_, assumption(_, Type, _, _), Assumptions),
    length(Assumptions, Count).

% List critical assumptions (high impact, uncertain)
critical_assumptions(Critical) :-
    findall(Text, 
            assumption(Text, _, uncertain, high), 
            Critical).

% Check for too many critical assumptions
check_assumption_count :-
    critical_assumptions(Critical),
    length(Critical, Count),
    Max is 3,
    (   Count > Max
    ->  format('WARNING: ~w critical assumptions (max: ~w)~n', [Count, Max])
    ;   true
    ).

% Verify an assumption is testable
verify_assumption(Text) :-
    assumption(Text, _, testable, _),
    !, format('Assumption verified as testable: ~w~n', [Text]).
verify_assumption(Text) :-
    format('Assumption not testable: ~w~n', [Text]).

% Log all assumptions made
log_assumptions :-
    findall(assumption(Text, Type, Status, Impact),
            assumption(Text, Type, Status, Impact),
            Assumptions),
    length(Assumptions, Count),
    format('~n--- Assumptions (~w) ---~n', [Count]),
    forall(member(assumption(Text, Type, Status, Impact), Assumptions),
           format('  [~w/~w] ~w~n', [Status, Impact, Text])).
        """
    
    def to_hy_heuristics(self) -> str:
        """
        Generate Hy/Lisp heuristics for assumption management.
        """
        return """
;; === Assumption Management Heuristics ===
;; Track, validate, and surface assumptions during reasoning

(def assumptions (atom []))

(defn capture-assumption [text & {:keys [type status impact context]
                                 :or {type :implicit
                                      status :uncertain
                                      impact :medium}}]
  "Record an assumption made during reasoning"
  (swap! assumptions conj
         {:text text
          :type type
          :status status
          :impact impact
          :context context
          :timestamp (datetime.now.)}))

(defn find-assumptions [reasoning-step]
  "Extract assumptions from a reasoning step"
  (let [step-lower (.lower (str reasoning-step))
        indicators {"assume" :explicit
                    "assuming" :explicit
                    "probably" :implicit
                    "likely" :implicit
                    "might" :implicit}]
    (for [[indicator ind-type] indicators
          :when (in indicator step-lower)]
      (capture-assumption reasoning-step
                         :type ind-type
                         :status :uncertain))))

(defn validate-assumptions [assumptions]
  "Check if assumptions are acceptable"
  (let [untestable (filter #(not= (:status %) :testable) assumptions)
        critical (filter #(= (:impact %) :high) assumptions)]
    {:total (count assumptions)
     :untestable untestable
     :critical critical
     :valid (and (empty? untestable) (< (count critical) 3))}))

(defn check-critical-count []
  "Warn if too many high-impact assumptions"
  (let [critical (filter #(and (= (:impact %) :high)
                               (= (:status %) :uncertain))
                        @assumptions)]
    (when (> (count critical) 3)
      (warn "More than 3 critical uncertain assumptions"))))

(defn surface-uncertainty [reasoning-step]
  "Detect and surface uncertainty in reasoning"
  (let [uncertainty-indicators ["uncertain" "unknown" "maybe" "possibly"]
        has-uncertainty (some #(in % (.lower (str reasoning-step))) 
                             uncertainty-indicators)]
    (when has-uncertainty
      (log-warning "Uncertainty detected - should clarify"))))

(defn assumption-report []
  "Generate report of all assumptions"
  (let [total (count @assumptions)
        by-status (group-by :status @assumptions)
        by-impact (group-by :impact @assumptions)]
    {:total total
     :by-status (into {} (map (fn [[k v]] [k (count v)])) by-status)
     :by-impact (into {} (map (fn [[k v]] [k (count v)])) by-impact)}))
        """
