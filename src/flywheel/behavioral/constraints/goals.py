#!/usr/bin/env python3
"""
Goals Constraint

Enforces Karpathy's 'Goal-Driven Execution' principle:
- Define verifiable success criteria
- Transform imperative tasks into declarative goals
- Loop until criteria are met
- Provide clear verification steps
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable

logger = logging.getLogger(__name__)


@dataclass
class SuccessCriterion:
    """Represents a verifiable success criterion."""
    name: str
    description: str
    type: str  # unit_test, integration_test, property_check, performance, manual
    target: Any
    current: Any = None
    tolerance: float = 0.0
    verified: bool = False
    verification_method: Optional[str] = None


@dataclass
class GoalVerification:
    """Result of verifying goals against criteria."""
    passed: bool
    criteria: List[SuccessCriterion]
    results: Dict[str, Any] = field(default_factory=dict)
    unmet_criteria: List[str] = field(default_factory=list)
    verification_steps: List[str] = field(default_factory=list)


@dataclass
class GoalsConstraint:
    """Enforces goal-driven execution with verifiable success criteria."""
    
    require_criteria: bool = True
    auto_generate: bool = True

    def extract_criteria(self, payload: Dict[str, Any]) -> List[SuccessCriterion]:
        """Extract success criteria from payload and intent."""
        criteria = []
        
        # Use explicit criteria if provided
        if "success_criteria" in payload:
            for crit in payload["success_criteria"]:
                if isinstance(crit, dict):
                    crit_dict = dict(crit)
                    if "description" not in crit_dict:
                        crit_dict["description"] = crit_dict.get("name", "Unknown criterion")
                    criteria.append(SuccessCriterion(**crit_dict))
                else:
                    criteria.append(SuccessCriterion(
                        name=str(crit),
                        description=str(crit),
                        type="manual",
                        target=True,
                    ))
            return criteria
        
        # Auto-generate from context if enabled
        if self.auto_generate:
            criteria.extend(self._infer_criteria(payload))
        
        return criteria

    def _infer_criteria(self, payload: Dict[str, Any]) -> List[SuccessCriterion]:
        """Infer success criteria from task type and parameters."""
        criteria = []
        payload_str = str(payload).lower()
        
        if any(word in payload_str for word in ["optimize", "optimum", "optimal"]):
            criteria.append(SuccessCriterion(
                name="performance_improvement",
                description="Achieve measurable performance improvement",
                type="performance",
                target="improved",
                verification_method="benchmark_comparison",
            ))
        
        if any(word in payload_str for word in ["fix", "bug", "error", "defect"]):
            criteria.append(SuccessCriterion(
                name="bug_reproduction",
                description="Reproduce the reported bug",
                type="unit_test",
                target=True,
                verification_method="test_execution",
            ))
            criteria.append(SuccessCriterion(
                name="bug_resolution",
                description="Verify bug is fixed",
                type="unit_test",
                target=False,
                verification_method="regression_test",
            ))
        
        if any(word in payload_str for word in ["validate", "verify", "check"]):
            criteria.append(SuccessCriterion(
                name="validation_completeness",
                description="All validation checks pass",
                type="unit_test",
                target=True,
                verification_method="test_suite",
            ))
        
        if any(word in payload_str for word in ["correct", "accurate", "valid"]):
            criteria.append(SuccessCriterion(
                name="correctness_verification",
                description="Output matches expected results",
                type="property_check",
                target="correct",
                verification_method="comparison_test",
            ))
        
        if "sat" in payload_str or "satisfiable" in payload_str:
            criteria.append(SuccessCriterion(
                name="satisfiability_check",
                description="Determine satisfiability correctly",
                type="property_check",
                target="determined",
                verification_method="independent_verification",
            ))
        
        if any(word in payload_str for word in ["network", "inference", "probability"]):
            criteria.append(SuccessCriterion(
                name="inference_accuracy",
                description="Inference results are probabilistically sound",
                type="property_check",
                target="sound",
                tolerance=0.01,
                verification_method="sanity_check",
            ))
        
        return criteria

    def _verify_criterion(self, criterion: Any, result: Dict[str, Any]) -> tuple:
        """Verify a single criterion against the result."""
        details = {'steps': [], 'actual': None}
        
        if isinstance(criterion, dict):
            from collections import namedtuple
            TempCriterion = namedtuple('TempCriterion', 
                ['name', 'description', 'type', 'target', 'current'])
            criterion = TempCriterion(
                name=criterion.get('name', ''),
                description=criterion.get('description', ''),
                type=criterion.get('type', 'manual'),
                target=criterion.get('target', True),
                current=None
            )
        
        try:
            if criterion.type == "unit_test":
                passed = self._verify_unit_test(criterion, result, details)
            elif criterion.type == "property_check":
                passed = self._verify_property(criterion, result, details)
            elif criterion.type == "performance":
                passed = self._verify_performance(criterion, result, details)
            else:
                passed = self._verify_generic(criterion, result, details)
        except Exception as e:
            logger.warning(f"Criterion verification failed: {e}")
            details['error'] = str(e)
            passed = False
        
        return passed, details

    def verify(self, result: Dict[str, Any], criteria: List[SuccessCriterion]) -> GoalVerification:
        """Verify result against success criteria."""
        if not criteria:
            return GoalVerification(
                passed=True,
                criteria=[],
                results={},
                unmet_criteria=[],
                verification_steps=["No criteria to verify"],
            )
        
        results = {}
        verification_steps = []
        unmet = []
        all_passed = True
        
        for criterion in criteria:
            passed, details = self._verify_criterion(criterion, result)
            
            if isinstance(criterion, dict):
                criterion_name = criterion.get('name', '')
                criterion_target = criterion.get('target', None)
                criterion_current = None
            else:
                criterion_name = criterion.name
                criterion_target = criterion.target
                criterion_current = getattr(criterion, 'current', None)
            
            results[criterion_name] = {
                'passed': passed,
                'expected': criterion_target,
                'actual': details.get('actual', criterion_current),
                'verified': passed,
                'details': details,
            }
            
            verification_steps.extend(details.get('steps', []))
            
            if not passed:
                all_passed = False
                unmet.append(criterion_name)
        
        return GoalVerification(
            passed=all_passed,
            criteria=criteria,
            results=results,
            unmet_criteria=unmet,
            verification_steps=verification_steps,
        )

    def _verify_unit_test(self, criterion: SuccessCriterion, result: Dict[str, Any], details: Dict) -> bool:
        """Verify unit test criterion."""
        tests_passed = result.get('tests_passed', 0)
        tests_total = result.get('tests_total', 1)
        
        if 'test_results' in result:
            passed = all(t.get('passed', False) for t in result['test_results'])
        else:
            passed = tests_passed >= tests_total
        
        details['actual'] = f"{tests_passed}/{tests_total} tests passed"
        details['steps'] = [
            "Run test suite",
            f"Expected: {criterion.target}",
            f"Actual: {tests_passed} of {tests_total} passed",
            f"Result: {'PASS' if passed else 'FAIL'}",
        ]
        
        return passed

    def _verify_property(self, criterion: Any, result: Dict[str, Any], details: Dict) -> bool:
        """Verify property-based criterion."""
        if 'satisfiable' in result:
            actual = result['satisfiable']
        elif 'valid' in result:
            actual = result['valid']
        elif 'correct' in result:
            actual = result['correct']
        else:
            status = result.get('status', '')
            actual = 'success' in status or status == 'success'
        
        details['actual'] = actual
        tolerance = getattr(criterion, 'tolerance', 0.0)
        
        if isinstance(criterion.target, bool):
            passed = actual == criterion.target
        elif isinstance(criterion.target, (int, float)):
            passed = abs(actual - criterion.target) <= tolerance
        else:
            passed = str(actual) == str(criterion.target)
        
        details['steps'] = [
            f"Check property: {criterion.description}",
            f"Expected: {criterion.target}",
            f"Actual: {actual}",
            f"Result: {'PASS' if passed else 'FAIL'}",
        ]
        
        return passed

    def _verify_performance(self, criterion: Any, result: Dict[str, Any], details: Dict) -> bool:
        """Verify performance criterion."""
        perf_metrics = result.get('performance', {})
        
        if 'execution_time' in perf_metrics:
            actual = perf_metrics['execution_time']
            passed = actual < criterion.target if isinstance(criterion.target, (int, float)) else True
        elif 'throughput' in perf_metrics:
            actual = perf_metrics['throughput']
            passed = actual >= criterion.target if isinstance(criterion.target, (int, float)) else True
        else:
            actual = "N/A"
            passed = True
        
        details['actual'] = actual
        details['steps'] = [
            f"Measure performance: {criterion.target}",
            f"Expected: {criterion.target}",
            f"Actual: {actual}",
            f"Result: {'PASS' if passed else 'FAIL'}",
        ]
        
        return passed

    def _verify_generic(self, criterion: Any, result: Dict[str, Any], details: Dict) -> bool:
        """Generic criterion verification."""
        if criterion.name in result:
            actual = result[criterion.name]
        elif 'result' in result:
            r = result['result']
            if isinstance(r, dict) and criterion.name in r:
                actual = r[criterion.name]
            else:
                actual = r
        else:
            actual = result
        
        details['actual'] = actual
        passed = str(actual) == str(criterion.target)
        
        details['steps'] = [
            f"Verify: {criterion.description}",
            f"Expected: {criterion.target}",
            f"Actual: {actual}",
            f"Result: {'PASS' if passed else 'FAIL'}",
        ]
        
        return passed

    def generate_plan(self, criteria: List[SuccessCriterion]) -> str:
        """Generate step-by-step plan with verification points."""
        if not criteria:
            return "No criteria defined."
        
        steps = []
        for i, criterion in enumerate(criteria, 1):
            step = f"{i}. {criterion.description}"
            verify = f"   → verify: {criterion.verification_method or 'manual check'}"
            steps.append(f"{step}\n{verify}")
        
        return "\n".join(steps)

    def to_prolog_rules(self) -> str:
        """Generate Prolog rules for goal verification."""
        return """
% === Goals Constraint Rules ===
% Define and verify success criteria
verify_goal(Solution, Criteria, Result) :-
    verify_all_criteria(Solution, Criteria, Results),
    (   all_passed(Results)
    ->  Result = passed
    ;   Result = failed).
verify_all_criteria(_, [], []).
verify_all_criteria(Solution, [Criterion | Rest], [Result | Results]) :-
    verify_criterion(Solution, Criterion, Result),
    verify_all_criteria(Solution, Rest, Results).
check_criterion(Solution, unit_test, Expected, Passed) :-
    run_unit_tests(Solution, Expected, Passed).
check_criterion(Solution, property_check, Expected, Passed) :-
    check_property(Solution, Expected, Passed).
check_criterion(Solution, performance, Bound, Passed) :-
    measure_performance(Solution, Perf),
    Perf =< Bound, !,
    Passed = true.
check_criterion(_, _, _, true).
        """

    def to_hy_heuristics(self) -> str:
        """Generate Hy/Lisp heuristics for goal-driven execution."""
        return """
(defn verify-criterion [criterion result]
  (let [ctype (:type criterion)]
    (case ctype
      :unit-test (verify-unit-test criterion result)
      :property-check (verify-property criterion result)
      :performance (verify-performance criterion result)
      (verify-generic criterion result))))

(defn verify-unit-test [criterion result]
  (let [passed (>= (:tests-passed result 0) (:tests-total result 1))]
    {:passed passed
     :actual (str (:tests-passed result 0) "/" (:tests-total result 1))
     :steps ["Run tests" (str "Expected: " (:target criterion))]}))

(defn verify-property [criterion result]
  (let [actual (or (:satisfiable result) (:valid result) (:success result))
        target (:target criterion)]
    {:passed (= actual target)
     :actual actual
     :steps ["Check property" (str "Expected: " target)]}))

(defn verify-all-criteria [result criteria]
  (if (empty? criteria)
    {:passed true :unmet []}
    (let [results (map #(verify-criterion % result) criteria)
          passed (every? :passed results)
          unmet (keep-indexed #(when-not (:passed %2) (:name (nth criteria %1))) results)]
      {:passed passed :unmet unmet :results results})))
        """
