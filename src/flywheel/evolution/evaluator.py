from __future__ import annotations

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, TypeVar

from .config import EvolutionConfig
from .genome import SkillFailureCase, SkillFitnessResult, SkillGenome

try:
    from darwinian_evolver.problem import Evaluator as BaseEvaluator

    DARWINIAN_AVAILABLE = True
except ImportError:
    DARWINIAN_AVAILABLE = False
    from typing import Protocol

    # Define type variables and protocol for type checking
    _T = TypeVar("_T")
    _R = TypeVar("_R")
    _E = TypeVar("_E")

    class BaseEvaluator(Protocol[_T, _R, _E]):
        """Dummy evaluator protocol for when darwinian-evolver is not installed."""

        pass


logger = logging.getLogger(__name__)


class SkillExecutor(ABC):
    """Abstract interface for executing skills."""

    @abstractmethod
    async def execute(
        self, skill_name: str, input_data: Dict[str, Any], parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a skill with given input and parameters."""
        pass


class MockSkillExecutor(SkillExecutor):
    """Mock executor for testing."""

    async def execute(
        self, skill_name: str, input_data: Dict[str, Any], parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Mock execution that returns simulated results."""
        await asyncio.sleep(0.01)
        return {"result": f"Processed {skill_name} with {input_data}", "success": True}


class SkillFitnessEvaluator(
    BaseEvaluator[SkillGenome, SkillFitnessResult, SkillFailureCase]
):
    """Evaluator for skill genomes that measures fitness based on execution results."""

    def __init__(
        self,
        skill_executor: SkillExecutor,
        test_cases: List[Dict[str, Any]],
        holdout_cases: List[Dict[str, Any]] | None = None,
        config: EvolutionConfig | None = None,
        output_dir: str | None = None,
    ):
        self.skill_executor = skill_executor
        self.test_cases = test_cases
        self.holdout_cases = holdout_cases or []
        self.config = config or EvolutionConfig()
        self._output_dir = output_dir

    def set_output_dir(self, output_dir: str) -> None:
        """Set output directory for evaluator results."""
        self._output_dir = output_dir

    def evaluate(self, genome: SkillGenome) -> SkillFitnessResult:
        """Evaluate a skill genome against test cases."""
        trainable_failures: List[SkillFailureCase] = []
        holdout_failures: List[SkillFailureCase] = []

        trainable_results = self._execute_test_cases(genome, self.test_cases)

        for i, (case, result) in enumerate(trainable_results):
            if not result.get("success", False):
                trainable_failures.append(
                    SkillFailureCase(
                        data_point_id=f"trainable_{i}",
                        skill_name=result.get("skill_name", "unknown"),
                        input_data=case.get("input", {}),
                        expected_output=case.get("expected", {}),
                        actual_output=result.get("output", {}),
                        failure_category=result.get("failure_category", "error"),
                        execution_time_ms=result.get("execution_time_ms"),
                    )
                )

        holdout_results = self._execute_test_cases(genome, self.holdout_cases)

        for i, (case, result) in enumerate(holdout_results):
            if not result.get("success", False):
                holdout_failures.append(
                    SkillFailureCase(
                        data_point_id=f"holdout_{i}",
                        skill_name=result.get("skill_name", "unknown"),
                        input_data=case.get("input", {}),
                        expected_output=case.get("expected", {}),
                        actual_output=result.get("output", {}),
                        failure_category=result.get("failure_category", "error"),
                        execution_time_ms=result.get("execution_time_ms"),
                    )
                )

        performance_score = self._calculate_performance_score(trainable_results)
        accuracy_score = self._calculate_accuracy_score(trainable_results)
        resource_efficiency = self._calculate_resource_efficiency(trainable_results)

        weights = self.config.metrics_weights
        overall_score = (
            weights["performance"] * performance_score
            + weights["accuracy"] * accuracy_score
            + weights["resource_efficiency"] * resource_efficiency
        )

        is_viable = len(trainable_results) > 0 and any(
            r.get("success", False) for r in [r for _, r in trainable_results]
        )

        return SkillFitnessResult(
            score=overall_score,
            trainable_failure_cases=trainable_failures,
            holdout_failure_cases=holdout_failures,
            is_viable=is_viable,
            performance_score=performance_score,
            accuracy_score=accuracy_score,
            resource_efficiency=resource_efficiency,
            execution_metrics={
                "total_cases": len(trainable_results),
                "successful": sum(
                    1 for _, r in trainable_results if r.get("success", False)
                ),
                "failed": len(trainable_failures),
            },
        )

    def verify_mutation(self, genome: SkillGenome) -> bool:
        """Verify that a mutation has addressed at least one failure case."""
        result = self.evaluate(genome)
        return len(result.trainable_failure_cases) < len(self.test_cases)

    def _execute_test_cases(
        self, genome: SkillGenome, cases: List[Dict[str, Any]]
    ) -> List[tuple[Dict[str, Any], Dict[str, Any]]]:
        """Execute test cases with the given genome."""
        results = []
        for case in cases:
            start_time = time.time()
            try:
                result = self._execute_genome(genome, case.get("input", {}))
                execution_time_ms = (time.time() - start_time) * 1000

                result["execution_time_ms"] = execution_time_ms

                expected = case.get("expected", {})
                if expected:
                    result["matches_expected"] = self._check_output_match(
                        result.get("output", {}), expected
                    )

                results.append((case, result))
            except Exception as e:
                results.append(
                    (
                        case,
                        {
                            "success": False,
                            "error": str(e),
                            "failure_category": "error",
                        },
                    )
                )

        return results

    def _execute_genome(
        self, genome: SkillGenome, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a genome's skill configuration."""
        import asyncio

        outputs = {}
        current_input = input_data

        for skill_name in genome.skill_selections:
            parameters = genome.skill_parameters.get(skill_name, {})
            skill_output = self.skill_executor.execute(
                skill_name, current_input, parameters
            )

            if asyncio.iscoroutine(skill_output):
                skill_output = asyncio.run(skill_output)

            outputs[skill_name] = skill_output

            if genome.orchestration_strategy == "sequential":
                current_input = {"previous_output": skill_output, **input_data}

        return {
            "success": True,
            "output": outputs,
            "skills_executed": list(genome.skill_selections),
        }

    def _calculate_performance_score(
        self, results: List[tuple[Dict[str, Any], Dict[str, Any]]]
    ) -> float:
        """Calculate performance score based on execution time."""
        if not results:
            return 0.0

        execution_times = [
            r.get("execution_time_ms", 0) for _, r in results if r.get("success", False)
        ]

        if not execution_times:
            return 0.0

        avg_time = sum(execution_times) / len(execution_times)
        max_acceptable_time = self.config.timeout_ms or 30000

        return max(0.0, 1.0 - (avg_time / max_acceptable_time))

    def _calculate_accuracy_score(
        self, results: List[tuple[Dict[str, Any], Dict[str, Any]]]
    ) -> float:
        """Calculate accuracy score based on expected outputs."""
        if not results:
            return 0.0

        matches = sum(
            1
            for _, r in results
            if r.get("success", False) and r.get("matches_expected", True)
        )

        return matches / len(results) if results else 0.0

    def _calculate_resource_efficiency(
        self, results: List[tuple[Dict[str, Any], Dict[str, Any]]]
    ) -> float:
        """Calculate resource efficiency score."""
        if not results:
            return 0.0

        successful = [r for _, r in results if r.get("success", False)]
        if not successful:
            return 0.0

        return 1.0

    def _check_output_match(self, actual: Any, expected: Dict[str, Any]) -> bool:
        """Check if actual output matches expected."""

if __name__ == "__main__":
    if not expected:
                return True

            for key, expected_value in expected.items():
                actual_value = (
                    actual.get(key)
                    if isinstance(actual, dict)
                    else getattr(actual, key, None)
                )
                if actual_value != expected_value:
                    return False

            return True