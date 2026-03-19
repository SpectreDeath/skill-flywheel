from uuid import uuid4

import pytest

from src.core.evolution.genome import (
    SkillFailureCase,
    SkillFitnessResult,
    SkillGenome,
    create_initial_genome,
)


class TestSkillGenome:
    """Tests for SkillGenome class."""

    def test_create_genome(self):
        """Test creating a basic skill genome."""
        genome = SkillGenome(
            skill_selections=["skill_a", "skill_b"],
            skill_parameters={"skill_a": {"threshold": 0.5}},
            prompt_templates={"skill_a": "Template: {input}"},
            resource_allocation={"skill_a": 0.5, "skill_b": 0.5},
            orchestration_strategy="sequential",
            timeout_ms=30000,
        )

        assert genome.skill_selections == ["skill_a", "skill_b"]
        assert genome.skill_parameters == {"skill_a": {"threshold": 0.5}}
        assert genome.orchestration_strategy == "sequential"
        assert genome.timeout_ms == 30000
        assert genome.id is not None
        assert genome.parent is None

    def test_genome_with_parent(self):
        """Test creating a genome with a parent."""
        parent = SkillGenome(
            skill_selections=["skill_a"],
            skill_parameters={},
            prompt_templates={},
            resource_allocation={},
            orchestration_strategy="sequential",
        )

        child = SkillGenome(
            skill_selections=["skill_a", "skill_b"],
            skill_parameters={"skill_b": {}},
            prompt_templates={},
            resource_allocation={},
            orchestration_strategy="parallel",
            parent=parent,
            from_change_summary="Added skill_b",
        )

        assert child.parent == parent
        assert child.from_change_summary == "Added skill_b"

    def test_get_skill_count(self):
        """Test getting skill count."""
        genome = SkillGenome(
            skill_selections=["a", "b", "c"],
            skill_parameters={},
            prompt_templates={},
            resource_allocation={},
            orchestration_strategy="sequential",
        )
        assert genome.get_skill_count() == 3

    def test_get_parameter_count(self):
        """Test getting parameter count."""
        genome = SkillGenome(
            skill_selections=["a", "b"],
            skill_parameters={"a": {"x": 1, "y": 2}, "b": {"z": 3}},
            prompt_templates={},
            resource_allocation={},
            orchestration_strategy="sequential",
        )
        assert genome.get_parameter_count() == 3

    def test_validate_valid(self):
        """Test validation with valid genome."""
        genome = SkillGenome(
            skill_selections=["skill_a"],
            skill_parameters={},
            prompt_templates={},
            resource_allocation={},
            orchestration_strategy="sequential",
            timeout_ms=1000,
        )
        assert genome.is_valid() is True

    def test_validate_empty_skills(self):
        """Test validation with empty skills."""
        genome = SkillGenome(
            skill_selections=[],
            skill_parameters={},
            prompt_templates={},
            resource_allocation={},
            orchestration_strategy="sequential",
            timeout_ms=1000,
        )
        assert genome.is_valid() is False

    def test_validate_invalid_strategy(self):
        """Test validation with invalid strategy."""
        genome = SkillGenome(
            skill_selections=["skill_a"],
            skill_parameters={},
            prompt_templates={},
            resource_allocation={},
            orchestration_strategy="invalid",
            timeout_ms=1000,
        )
        assert genome.is_valid() is False

    def test_validate_negative_timeout(self):
        """Test validation with negative timeout."""
        genome = SkillGenome(
            skill_selections=["skill_a"],
            skill_parameters={},
            prompt_templates={},
            resource_allocation={},
            orchestration_strategy="sequential",
            timeout_ms=-1000,
        )
        assert genome.is_valid() is False


class TestSkillFailureCase:
    """Tests for SkillFailureCase class."""

    def test_create_failure_case(self):
        """Test creating a failure case."""
        fc = SkillFailureCase(
            data_point_id="test_1",
            skill_name="skill_a",
            input_data={"query": "test"},
            expected_output={"result": "expected"},
            actual_output={"result": "actual"},
            failure_category="accuracy",
        )

        assert fc.data_point_id == "test_1"
        assert fc.skill_name == "skill_a"
        assert fc.failure_category == "accuracy"

    def test_default_failure_category(self):
        """Test default failure category."""
        fc = SkillFailureCase(data_point_id="test_1", skill_name="skill_a")
        assert fc.failure_category == "error"


class TestSkillFitnessResult:
    """Tests for SkillFitnessResult class."""

    def test_create_result(self):
        """Test creating a fitness result."""
        result = SkillFitnessResult(
            score=0.85,
            trainable_failure_cases=[],
            holdout_failure_cases=[],
            is_viable=True,
            performance_score=0.9,
            accuracy_score=0.8,
            resource_efficiency=0.85,
        )

        assert result.score == 0.85
        assert result.is_viable is True
        assert result.performance_score == 0.9
        assert result.accuracy_score == 0.8

    def test_failure_type_weights(self):
        """Test failure type weights."""
        result = SkillFitnessResult(score=0.5, trainable_failure_cases=[])

        weights = result.failure_type_weights
        assert weights["performance"] == 2.0
        assert weights["accuracy"] == 1.5
        assert weights["error"] == 3.0

    def test_format_observed_outcome_improvement(self):
        """Test outcome formatting for improvement."""
        parent = SkillFitnessResult(score=0.7, trainable_failure_cases=[])
        result = SkillFitnessResult(
            score=0.85,
            trainable_failure_cases=[],
            is_viable=True,
            performance_score=0.9,
            accuracy_score=0.8,
            resource_efficiency=0.85,
        )

        outcome = result.format_observed_outcome(parent)
        assert "Improved" in outcome
        assert "0.7" in outcome

    def test_format_observed_outcome_non_viable(self):
        """Test outcome formatting for non-viable result."""
        result = SkillFitnessResult(
            score=0.0, trainable_failure_cases=[], is_viable=False
        )

        outcome = result.format_observed_outcome(None)
        assert "inconclusive" in outcome.lower()


class TestCreateInitialGenome:
    """Tests for create_initial_genome factory function."""

    def test_create_with_defaults(self):
        """Test creating genome with defaults."""
        genome = create_initial_genome(["skill_a", "skill_b"])

        assert genome.skill_selections == ["skill_a", "skill_b"]
        assert genome.orchestration_strategy == "sequential"
        assert "skill_a" in genome.resource_allocation

    def test_create_with_custom_params(self):
        """Test creating genome with custom parameters."""
        params = {"skill_a": {"threshold": 0.8}}
        genome = create_initial_genome(
            ["skill_a"], default_parameters=params, orchestration_strategy="parallel"
        )

        assert genome.skill_parameters == params
        assert genome.orchestration_strategy == "parallel"
