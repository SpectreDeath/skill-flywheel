from __future__ import annotations

import functools
from collections.abc import Callable
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    List,
    TypeVar,
    overload,
)

try:
    from darwinian_evolver.learning_log import LearningLogEntry
    from darwinian_evolver.problem import Evaluator as BaseEvaluator
    from darwinian_evolver.problem import Mutator as BaseMutator
    from darwinian_evolver.problem import MutatorContext

    DARWINIAN_AVAILABLE = True
except ImportError:
    DARWINIAN_AVAILABLE = False
    from typing import Protocol

    _G = TypeVar("_G")
    _R = TypeVar("_R")
    _E = TypeVar("_E")
    _F = TypeVar("_F")

    class BaseEvaluator(Protocol[_G, _R, _E]):
        """Dummy evaluator protocol for when darwinian-evolver is not installed."""

        pass

    class BaseMutator(Protocol[_G, _F]):
        """Dummy mutator protocol for when darwinian-evolver is not installed."""

        pass

    class MutatorContext(Protocol):
        """Dummy mutator context for when darwinian-evolver is not installed."""

        pass

    class LearningLogEntry:
        """Dummy learning log entry for when darwinian-evolver is not installed."""

        pass


if TYPE_CHECKING:
    pass

from .genome import SkillFailureCase, SkillFitnessResult, SkillGenome

_T = TypeVar("_T")
_U = TypeVar("_U")
_O = TypeVar("_O")
_F = TypeVar("_F")
_E = TypeVar("_E")

OrganismT = TypeVar("OrganismT", bound=SkillGenome)
EvaluationT = TypeVar("EvaluationT", bound=SkillFitnessResult)
FailureT = TypeVar("FailureT", bound=SkillFailureCase)


class TypeSafeEvaluator(Generic[OrganismT, EvaluationT, FailureT]):
    """Type-safe wrapper for Evaluator to handle type mismatches."""

    def __init__(self, evaluator: BaseEvaluator):
        self._evaluator = evaluator

    def evaluate(self, genome: OrganismT) -> EvaluationT:
        return self._evaluator.evaluate(genome)  # type: ignore[return-value]

    def verify_mutation(self, genome: OrganismT) -> bool:
        if hasattr(self._evaluator, "verify_mutation"):
            return self._evaluator.verify_mutation(genome)  # type: ignore[return-value]
        return True

    def set_output_dir(self, output_dir: str) -> None:
        if hasattr(self._evaluator, "set_output_dir"):
            self._evaluator.set_output_dir(output_dir)

    @property
    def inner(self) -> BaseEvaluator:
        return self._evaluator

    def __getattr__(self, name: str) -> Any:
        return getattr(self._evaluator, name)


class TypeSafeMutator(Generic[OrganismT, FailureT]):
    """Type-safe wrapper for Mutator to handle type mismatches."""

    def __init__(self, mutator: BaseMutator):
        self._mutator = mutator
        self._context: MutatorContext | None = None

    def mutate(
        self,
        genome: OrganismT,
        failure_cases: List[FailureT],
        learning_log_entries: List[LearningLogEntry] | None = None,
    ) -> List[OrganismT]:
        return self._mutator.mutate(
            genome,
            failure_cases,
            learning_log_entries or [],  # type: ignore[arg-type]
        )  # type: ignore[return-value]

    def set_context(self, context: MutatorContext) -> None:
        self._context = context
        if hasattr(self._mutator, "set_context"):
            self._mutator.set_context(context)

    @property
    def supports_batch_mutation(self) -> bool:
        if hasattr(self._mutator, "supports_batch_mutation"):
            return self._mutator.supports_batch_mutation
        return False

    @property
    def inner(self) -> BaseMutator:
        return self._mutator

    def __getattr__(self, name: str) -> Any:
        return getattr(self._mutator, name)


class TypeSafePopulation(Generic[OrganismT, EvaluationT]):
    """Type-safe wrapper for Population to handle type mismatches."""

    def __init__(self, population: Any):
        self._population = population

    def add(self, organism: OrganismT, evaluation_result: EvaluationT) -> None:
        self._population.add(organism, evaluation_result)

    def get_best(self) -> tuple[OrganismT, EvaluationT]:
        return self._population.get_best()  # type: ignore[return-value]

    @property
    def organisms(
        self,
    ) -> list[tuple[OrganismT, EvaluationT]]:
        return self._population.organisms  # type: ignore[return-value]

    def get_children(self, organism: OrganismT) -> list[OrganismT]:
        return self._population.get_children(organism)  # type: ignore[return-value]

    def get_score_percentiles(self) -> Dict[str, float]:
        return self._population.get_score_percentiles()  # type: ignore[return-value]

    def snapshot(self) -> bytes:
        return self._population.snapshot()

    @classmethod
    def from_snapshot(
        cls, snapshot: bytes, config: Any | None = None
    ) -> TypeSafePopulation[OrganismT, EvaluationT]:
        population = cls._original_from_snapshot(snapshot)  # type: ignore[attr-defined]
        return cls(population)

    @property
    def inner(self) -> Any:
        return self._population

    def __getattr__(self, name: str) -> Any:
        return getattr(self._population, name)


def bridge_evaluator(
    evaluator: BaseEvaluator,
) -> TypeSafeEvaluator[SkillGenome, SkillFitnessResult, SkillFailureCase]:
    """Create a type-safe evaluator wrapper.

    Args:
        evaluator: The underlying evaluator to wrap

    Returns:
        TypeSafeEvaluator wrapper for type-safe access
    """
    return TypeSafeEvaluator[SkillGenome, SkillFitnessResult, SkillFailureCase](
        evaluator
    )


def bridge_mutator(
    mutator: BaseMutator,
) -> TypeSafeMutator[SkillGenome, SkillFailureCase]:
    """Create a type-safe mutator wrapper.

    Args:
        mutator: The underlying mutator to wrap

    Returns:
        TypeSafeMutator wrapper for type-safe access
    """
    return TypeSafeMutator[SkillGenome, SkillFailureCase](mutator)


def bridge_population(
    population: Any,
) -> TypeSafePopulation[SkillGenome, SkillFitnessResult]:
    """Create a type-safe population wrapper.

    Args:
        population: The underlying population to wrap

    Returns:
        TypeSafePopulation wrapper for type-safe access
    """
    return TypeSafePopulation[SkillGenome, SkillFitnessResult](population)


def type_ignore(
    func: Callable[..., _T] | None = None,
    *error_codes: str,
) -> Callable[..., _T] | Callable[[Callable[..., _T]], Callable[..., _T]]:
    """Decorator to suppress LSP type errors for specific function calls.

    Usage:
        @type_ignore("return-value", "arg-type")
        def some_function(x: int) -> str:
            return str(x)  # May cause type mismatch
    """
    error_str = (
        "[{errors}]".format(errors=", ".join(error_codes)) if error_codes else ""
    )

    def decorator(func: Callable[..., _T]) -> Callable[..., _T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> _T:
            return func(*args, **kwargs)  # type: ignore[return-value]

        if error_str:
            wrapper.__annotations__["return"] = Any  # type: ignore[assignment]

        return wrapper  # type: ignore[return-value]

    if func is None:
        return decorator
    return decorator(func)


def suppress_lsp_errors(*error_codes: str) -> Callable[[_T], _T]:
    """Decorator factory to suppress specific LSP errors on a function.

    Args:
        *error_codes: Error codes to suppress (e.g., "return-value", "arg-type")

    Returns:
        Decorator that marks function to suppress specified errors
    """
    ", ".join(error_codes) if error_codes else ""

    def decorator(func: _T) -> _T:
        if hasattr(func, "__annotations__"):
            original_annotations = dict(func.__annotations__)
            func.__annotations__ = original_annotations

        return func  # type: ignore[return-value]

    return decorator


def cast_to_organism(value: Any) -> SkillGenome:
    """Cast a value to SkillGenome, suppressing type errors."""
    return value  # type: ignore[return-value]


def cast_to_evaluation(value: Any) -> SkillFitnessResult:
    """Cast a value to SkillFitnessResult, suppressing type errors."""
    return value  # type: ignore[return-value]


def cast_to_failure_case(value: Any) -> SkillFailureCase:
    """Cast a value to SkillFailureCase, suppressing type errors."""
    return value  # type: ignore[return-value]


@overload
def unsafe_cast(value: _T) -> _U: ...


@overload
def unsafe_cast(value: _T, target_type: type[_U]) -> _U: ...


def unsafe_cast(value: _T, target_type: type[_U] | None = None) -> _U:
    """Cast a value to target type, suppressing LSP errors.

    This should be used sparingly and only when runtime type checking
    has verified the value is correct.
    """
    if target_type is not None:
        return value  # type: ignore[return-value]
    return value  # type: ignore[return-value]


class TypeBridge:
    """Utility class for bridging types between darwinian-evolver and Skill Flywheel."""

if __name__ == "__main__":
    @staticmethod
        def to_organism(value: Any) -> SkillGenome:
            return cast_to_organism(value)

        @staticmethod
        def to_evaluation(value: Any) -> SkillFitnessResult:
            return cast_to_evaluation(value)

        @staticmethod
        def to_failure_case(value: Any) -> SkillFailureCase:
            return cast_to_failure_case(value)

        @staticmethod
        def wrap_evaluator(
            evaluator: BaseEvaluator,
        ) -> TypeSafeEvaluator[SkillGenome, SkillFitnessResult, SkillFailureCase]:
            return bridge_evaluator(evaluator)

        @staticmethod
        def wrap_mutator(
            mutator: BaseMutator,
        ) -> TypeSafeMutator[SkillGenome, SkillFailureCase]:
            return bridge_mutator(mutator)

        @staticmethod
        def wrap_population(
            population: Any,
        ) -> TypeSafePopulation[SkillGenome, SkillFitnessResult]:
            return bridge_population(population)