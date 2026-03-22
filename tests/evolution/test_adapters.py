"""Tests for evolution adapters module - type bridging behavior."""

import pytest
from unittest.mock import Mock, MagicMock

from flywheel.evolution.adapters import (
    TypeSafeEvaluator,
    TypeSafeMutator,
    TypeSafePopulation,
    bridge_evaluator,
    bridge_mutator,
    bridge_population,
    cast_to_organism,
    cast_to_evaluation,
    cast_to_failure_case,
    unsafe_cast,
    TypeBridge,
)
from flywheel.evolution.genome import SkillGenome, SkillFitnessResult, SkillFailureCase


class TestTypeSafeEvaluator:
    """Test TypeSafeEvaluator wrapper behavior."""

    def test_evaluate_passes_through_to_inner_evaluator(self):
        """Verify evaluate() calls inner evaluator and returns result."""
        mock_inner = Mock()
        mock_inner.evaluate.return_value = SkillFitnessResult(score=0.85)

        wrapper = TypeSafeEvaluator(mock_inner)
        genome = SkillGenome(skill_selections=["skill1"])

        result = wrapper.evaluate(genome)

        mock_inner.evaluate.assert_called_once_with(genome)
        assert result.score == 0.85

    def test_verify_mutation_returns_true_when_inner_has_method(self):
        """Verify verify_mutation() returns inner result when method exists."""
        mock_inner = Mock()
        mock_inner.verify_mutation.return_value = False

        wrapper = TypeSafeEvaluator(mock_inner)
        genome = SkillGenome(skill_selections=["skill1"])

        result = wrapper.verify_mutation(genome)

        assert result is False

    def test_verify_mutation_returns_true_when_inner_lacks_method(self):
        """Verify verify_mutation() defaults to True when method missing."""
        mock_inner = Mock(spec=[])  # No verify_mutation method

        wrapper = TypeSafeEvaluator(mock_inner)
        genome = SkillGenome(skill_selections=["skill1"])

        result = wrapper.verify_mutation(genome)

        assert result is True

    def test_set_output_dir_passes_to_inner(self):
        """Verify set_output_dir() calls inner method when present."""
        mock_inner = Mock()

        wrapper = TypeSafeEvaluator(mock_inner)
        wrapper.set_output_dir("/tmp/output")

        mock_inner.set_output_dir.assert_called_once_with("/tmp/output")

    def test_inner_property_returns_underlying_evaluator(self):
        """Verify inner property returns the wrapped evaluator."""
        mock_inner = Mock()
        wrapper = TypeSafeEvaluator(mock_inner)

        assert wrapper.inner is mock_inner

    def test_delegates_unknown_attributes_to_inner(self):
        """Verify unknown attributes are delegated to inner evaluator."""
        mock_inner = Mock()
        mock_inner.some_method.return_value = 42

        wrapper = TypeSafeEvaluator(mock_inner)

        assert wrapper.some_method() == 42


class TestTypeSafeMutator:
    """Test TypeSafeMutator wrapper behavior."""

    def test_mutate_passes_arguments_to_inner(self):
        """Verify mutate() forwards all arguments to inner mutator."""
        mock_inner = Mock()
        mock_inner.mutate.return_value = []

        wrapper = TypeSafeMutator(mock_inner)
        genome = SkillGenome(skill_selections=["skill1"])
        failures = [SkillFailureCase(data_point_id="1", skill_name="skill1")]

        wrapper.mutate(genome, failures)

        mock_inner.mutate.assert_called_once_with(genome, failures, [])

    def test_mutate_accepts_learning_log(self):
        """Verify mutate() passes learning log entries when provided."""
        mock_inner = Mock()
        mock_inner.mutate.return_value = []

        wrapper = TypeSafeMutator(mock_inner)
        genome = SkillGenome(skill_selections=["skill1"])
        failures = []
        learning_log = ["entry1", "entry2"]

        wrapper.mutate(genome, failures, learning_log)

        mock_inner.mutate.assert_called_once_with(genome, failures, learning_log)

    def test_set_context_passes_to_inner(self):
        """Verify set_context() forwards to inner mutator."""
        mock_inner = Mock()
        context = MagicMock()

        wrapper = TypeSafeMutator(mock_inner)
        wrapper.set_context(context)

        mock_inner.set_context.assert_called_once_with(context)

    def test_supports_batch_mutation_true_when_inner_has_property(self):
        """Verify returns True when inner supports batch mutation."""
        mock_inner = Mock()
        mock_inner.supports_batch_mutation = True

        wrapper = TypeSafeMutator(mock_inner)

        assert wrapper.supports_batch_mutation is True

    def test_supports_batch_mutation_false_when_inner_lacks_property(self):
        """Verify defaults to False when inner lacks property."""
        mock_inner = Mock(spec=[])  # No supports_batch_mutation

        wrapper = TypeSafeMutator(mock_inner)

        assert wrapper.supports_batch_mutation is False

    def test_inner_property_returns_underlying_mutator(self):
        """Verify inner property returns the wrapped mutator."""
        mock_inner = Mock()
        wrapper = TypeSafeMutator(mock_inner)

        assert wrapper.inner is mock_inner


class TestTypeSafePopulation:
    """Test TypeSafePopulation wrapper behavior."""

    def test_add_passes_to_inner(self):
        """Verify add() forwards to inner population."""
        mock_inner = Mock()
        wrapper = TypeSafePopulation(mock_inner)

        genome = SkillGenome(skill_selections=["skill1"])
        evaluation = SkillFitnessResult(score=0.8)

        wrapper.add(genome, evaluation)

        mock_inner.add.assert_called_once_with(genome, evaluation)

    def test_get_best_returns_tuple_from_inner(self):
        """Verify get_best() returns tuple from inner."""
        mock_inner = Mock()
        mock_inner.get_best.return_value = ("genome", "evaluation")

        wrapper = TypeSafePopulation(mock_inner)

        result = wrapper.get_best()

        assert result == ("genome", "evaluation")

    def test_organisms_property_proxies_to_inner(self):
        """Verify organisms property returns inner value."""
        mock_inner = Mock()
        mock_inner.organisms = ["item1", "item2"]

        wrapper = TypeSafePopulation(mock_inner)

        assert wrapper.organisms == ["item1", "item2"]

    def test_get_children_passes_to_inner(self):
        """Verify get_children() forwards to inner."""
        mock_inner = Mock()
        mock_inner.get_children.return_value = ["child1"]

        wrapper = TypeSafePopulation(mock_inner)
        parent = SkillGenome(skill_selections=["skill1"])

        result = wrapper.get_children(parent)

        mock_inner.get_children.assert_called_once_with(parent)
        assert result == ["child1"]

    def test_get_score_percentiles_returns_dict(self):
        """Verify get_score_percentiles() returns dict from inner."""
        mock_inner = Mock()
        mock_inner.get_score_percentiles.return_value = {"p50": 0.5, "p90": 0.9}

        wrapper = TypeSafePopulation(mock_inner)

        result = wrapper.get_score_percentiles()

        assert result == {"p50": 0.5, "p90": 0.9}

    def test_snapshot_returns_bytes(self):
        """Verify snapshot() returns bytes from inner."""
        mock_inner = Mock()
        mock_inner.snapshot.return_value = b"serialized_data"

        wrapper = TypeSafePopulation(mock_inner)

        result = wrapper.snapshot()

        assert result == b"serialized_data"

    def test_inner_property_returns_underlying_population(self):
        """Verify inner property returns the wrapped population."""
        mock_inner = Mock()
        wrapper = TypeSafePopulation(mock_inner)

        assert wrapper.inner is mock_inner


class TestBridgeFunctions:
    """Test factory functions for creating bridges."""

    def test_bridge_evaluator_returns_type_safe_evaluator(self):
        """Verify bridge_evaluator() returns TypeSafeEvaluator instance."""
        mock_evaluator = Mock()

        result = bridge_evaluator(mock_evaluator)

        assert isinstance(result, TypeSafeEvaluator)
        assert result.inner is mock_evaluator

    def test_bridge_mutator_returns_type_safe_mutator(self):
        """Verify bridge_mutator() returns TypeSafeMutator instance."""
        mock_mutator = Mock()

        result = bridge_mutator(mock_mutator)

        assert isinstance(result, TypeSafeMutator)
        assert result.inner is mock_mutator

    def test_bridge_population_returns_type_safe_population(self):
        """Verify bridge_population() returns TypeSafePopulation instance."""
        mock_population = Mock()

        result = bridge_population(mock_population)

        assert isinstance(result, TypeSafePopulation)
        assert result.inner is mock_population


class TestCastFunctions:
    """Test type casting functions."""

    def test_cast_to_organism_returns_input(self):
        """Verify cast_to_organism returns the input value."""
        genome = SkillGenome(skill_selections=["skill1"])

        result = cast_to_organism(genome)

        assert result is genome

    def test_cast_to_evaluation_returns_input(self):
        """Verify cast_to_evaluation returns the input value."""
        evaluation = SkillFitnessResult(score=0.9)

        result = cast_to_evaluation(evaluation)

        assert result is evaluation

    def test_cast_to_failure_case_returns_input(self):
        """Verify cast_to_failure_case returns the input value."""
        failure = SkillFailureCase(data_point_id="1", skill_name="skill1")

        result = cast_to_failure_case(failure)

        assert result is failure


class TestUnsafeCast:
    """Test unsafe_cast function behavior."""

    def test_unsafe_cast_returns_value(self):
        """Verify unsafe_cast returns the value regardless of type."""
        value = "test"
        result = unsafe_cast(value)
        assert result == value

    def test_unsafe_cast_with_target_type(self):
        """Verify unsafe_cast handles target_type argument."""
        value = "test"
        result = unsafe_cast(value, str)
        assert result == value


class TestTypeBridge:
    """Test TypeBridge utility class."""

    def test_to_organism_uses_cast_function(self):
        """Verify TypeBridge.to_organism() calls cast_to_organism."""
        genome = SkillGenome(skill_selections=["skill1"])

        result = TypeBridge.to_organism(genome)

        assert result is genome

    def test_to_evaluation_uses_cast_function(self):
        """Verify TypeBridge.to_evaluation() calls cast_to_evaluation."""
        evaluation = SkillFitnessResult(score=0.7)

        result = TypeBridge.to_evaluation(evaluation)

        assert result is evaluation

    def test_to_failure_case_uses_cast_function(self):
        """Verify TypeBridge.to_failure_case() calls cast_to_failure_case."""
        failure = SkillFailureCase(data_point_id="1", skill_name="skill1")

        result = TypeBridge.to_failure_case(failure)

        assert result is failure

    def test_wrap_evaluator_returns_type_safe_evaluator(self):
        """Verify TypeBridge.wrap_evaluator() returns TypeSafeEvaluator."""
        mock_evaluator = Mock()

        result = TypeBridge.wrap_evaluator(mock_evaluator)

        assert isinstance(result, TypeSafeEvaluator)

    def test_wrap_mutator_returns_type_safe_mutator(self):
        """Verify TypeBridge.wrap_mutator() returns TypeSafeMutator."""
        mock_mutator = Mock()

        result = TypeBridge.wrap_mutator(mock_mutator)

        assert isinstance(result, TypeSafeMutator)

    def test_wrap_population_returns_type_safe_population(self):
        """Verify TypeBridge.wrap_population() returns TypeSafePopulation."""
        mock_population = Mock()

        result = TypeBridge.wrap_population(mock_population)

        assert isinstance(result, TypeSafePopulation)
