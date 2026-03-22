"""Tests for kilo_research_mutator module - research-based mutation behavior."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from flywheel.evolution.kilo_research_mutator import (
    KiloResearchMutator,
    MockResearchMutator,
)
from flywheel.evolution.genome import SkillGenome, SkillFailureCase


class TestKiloResearchMutator:
    """Test KiloResearchMutator behavior."""

    def test_supports_batch_mutation_returns_true(self):
        """Verify mutator supports batch mutation."""
        mutator = KiloResearchMutator()
        assert mutator.supports_batch_mutation is True

    def test_set_context_stores_context(self):
        """Verify set_context() stores the context."""
        mutator = KiloResearchMutator()
        context = MagicMock()

        mutator.set_context(context)

        assert mutator._context is context

    def test_mutate_with_no_failures_generates_exploratory_mutations(self):
        """Verify mutate() returns exploratory mutations when no failures."""
        mutator = KiloResearchMutator(use_web_search=False, use_code_search=False)
        genome = SkillGenome(
            skill_selections=["skill1", "skill2"],
            skill_parameters={"skill1": {"param1": 10}},
            timeout_ms=5000,
        )

        result = mutator.mutate(genome, failure_cases=[], learning_log_entries=[])

        assert len(result) >= 1
        assert all(isinstance(m, SkillGenome) for m in result)

    def test_mutate_with_failures_creates_research_based_mutations(self):
        """Verify mutate() uses failure cases to guide mutations."""
        mutator = KiloResearchMutator(use_web_search=False, use_code_search=False)
        genome = SkillGenome(
            skill_selections=["skill1"],
            skill_parameters={"skill1": {"threshold": 0.5}},
            orchestration_strategy="sequential",
            timeout_ms=5000,
        )
        failures = [
            SkillFailureCase(
                data_point_id="1",
                skill_name="skill1",
                failure_category="timeout",
            )
        ]

        result = mutator.mutate(genome, failures, learning_log_entries=[])

        assert len(result) >= 1

    def test_identify_patterns_detects_timeout_issues(self):
        """Verify _identify_patterns() detects timeout failures."""
        mutator = KiloResearchMutator()
        failures = [
            SkillFailureCase(
                data_point_id="1", skill_name="s1", failure_category="timeout"
            ),
            SkillFailureCase(
                data_point_id="2", skill_name="s2", failure_category="timeout"
            ),
        ]

        patterns = mutator._identify_patterns(failures)

        assert "timeout_issues" in patterns

    def test_identify_patterns_detects_accuracy_issues(self):
        """Verify _identify_patterns() detects accuracy failures."""
        mutator = KiloResearchMutator()
        failures = [
            SkillFailureCase(
                data_point_id="1", skill_name="s1", failure_category="accuracy"
            ),
        ]

        patterns = mutator._identify_patterns(failures)

        assert "accuracy_issues" in patterns

    def test_identify_patterns_detects_error_issues(self):
        """Verify _identify_patterns() detects error failures."""
        mutator = KiloResearchMutator()
        failures = [
            SkillFailureCase(
                data_point_id="1", skill_name="s1", failure_category="error"
            ),
        ]

        patterns = mutator._identify_patterns(failures)

        assert "error_issues" in patterns

    def test_identify_patterns_empty_for_no_failures(self):
        """Verify _identify_patterns() returns empty list for no failures."""
        mutator = KiloResearchMutator()

        patterns = mutator._identify_patterns([])

        assert patterns == []

    def test_generate_web_queries_respects_research_depth(self):
        """Verify _generate_web_queries() limits queries to research_depth."""
        mutator = KiloResearchMutator(research_depth=1)

        queries = mutator._generate_web_queries("clustering", "timeout")

        assert len(queries) == 1

    def test_generate_web_queries_contains_skill_name(self):
        """Verify web queries include the skill name."""
        mutator = KiloResearchMutator()

        queries = mutator._generate_web_queries("clustering", "timeout")

        assert any("clustering" in q for q in queries)

    def test_generate_code_queries_respects_research_depth(self):
        """Verify _generate_code_queries() limits queries to research_depth."""
        mutator = KiloResearchMutator(research_depth=2)

        queries = mutator._generate_code_queries("skill", "error")

        assert len(queries) == 2

    def test_create_parameter_mutation_increases_timeout_for_timeout_issues(self):
        """Verify timeout increases when timeout_issues pattern present."""
        mutator = KiloResearchMutator()
        genome = SkillGenome(
            skill_selections=["skill1"],
            skill_parameters={"skill1": {"timeout": 1000}},
            timeout_ms=5000,
        )

        mutation = mutator._create_parameter_mutation(genome, ["timeout_issues"])

        assert isinstance(mutation, SkillGenome)
        assert mutation.parent is genome

    def test_create_parameter_mutation_decreases_threshold_for_accuracy_issues(self):
        """Verify threshold decreases when accuracy_issues pattern present."""
        mutator = KiloResearchMutator()
        genome = SkillGenome(
            skill_selections=["skill1"],
            skill_parameters={"skill1": {"threshold": 0.8}},
            timeout_ms=5000,
        )

        mutation = mutator._create_parameter_mutation(genome, ["accuracy_issues"])

        assert isinstance(mutation, SkillGenome)

    def test_create_parameter_mutation_increases_retries_for_error_issues(self):
        """Verify max_retries increases when error_issues pattern present."""
        mutator = KiloResearchMutator()
        genome = SkillGenome(
            skill_selections=["skill1"],
            skill_parameters={"skill1": {"max_retries": 2}},
            retry_config={"max_retries": 2},
            timeout_ms=5000,
        )

        mutation = mutator._create_parameter_mutation(genome, ["error_issues"])

        assert isinstance(mutation, SkillGenome)

    def test_create_structure_mutation_changes_strategy(self):
        """Verify structure mutation changes orchestration strategy."""
        mutator = KiloResearchMutator()
        genome = SkillGenome(
            skill_selections=["skill1", "skill2"],
            orchestration_strategy="sequential",
            timeout_ms=5000,
        )

        mutation = mutator._create_structure_mutation(genome, [])

        assert isinstance(mutation, SkillGenome)
        assert mutation.orchestration_strategy in [
            "parallel",
            "hierarchical",
            "sequential",
        ]

    def test_create_structure_mutation_preserves_skills(self):
        """Verify structure mutation keeps same skills."""
        mutator = KiloResearchMutator()
        genome = SkillGenome(
            skill_selections=["skill1", "skill2"],
            orchestration_strategy="sequential",
            timeout_ms=5000,
        )

        mutation = mutator._create_structure_mutation(genome, [])

        assert set(mutation.skill_selections) == {"skill1", "skill2"}

    def test_create_structure_mutation_has_parent_reference(self):
        """Verify structure mutation references parent genome."""
        mutator = KiloResearchMutator()
        genome = SkillGenome(
            skill_selections=["skill1"],
            orchestration_strategy="sequential",
            timeout_ms=5000,
        )

        mutation = mutator._create_structure_mutation(genome, [])

        assert mutation.parent is genome

    def test_create_exploratory_mutation_modifies_timeout(self):
        """Verify exploratory mutation changes timeout."""
        mutator = KiloResearchMutator()
        genome = SkillGenome(
            skill_selections=["skill1"],
            skill_parameters={},
            timeout_ms=5000,
        )

        mutation = mutator._create_exploratory_mutation(genome)

        assert isinstance(mutation, SkillGenome)
        assert mutation.timeout_ms > 0

    def test_create_exploratory_mutation_has_change_summary(self):
        """Verify exploratory mutation includes change summary."""
        mutator = KiloResearchMutator()
        genome = SkillGenome(
            skill_selections=["skill1"],
            timeout_ms=5000,
        )

        mutation = mutator._create_exploratory_mutation(genome)

        assert mutation.from_change_summary is not None
        assert "Exploratory" in mutation.from_change_summary

    def test_reorder_skills_reverses_for_timeout_issues(self):
        """Verify skill reorder reverses list for timeout issues."""
        mutator = KiloResearchMutator()
        skills = ["skill1", "skill2", "skill3"]

        results = [
            mutator._reorder_skills(skills, ["timeout_issues"]) for _ in range(20)
        ]

        first_elements = [r[0] for r in results]
        assert "skill3" in first_elements

    def test_reorder_skills_empty_input(self):
        """Verify reorder handles empty skills list."""
        mutator = KiloResearchMutator()

        result = mutator._reorder_skills([], [])

        assert result == []

    def test_synthesize_mutations_returns_list(self):
        """Verify _synthesize_mutations() returns a list of genomes."""
        mutator = KiloResearchMutator()
        genome = SkillGenome(
            skill_selections=["skill1"],
            skill_parameters={},
            timeout_ms=5000,
        )
        failures = [
            SkillFailureCase(
                data_point_id="1", skill_name="s1", failure_category="timeout"
            )
        ]
        research_results = {"patterns": ["timeout_issues"]}

        result = mutator._synthesize_mutations(genome, failures, research_results)

        assert isinstance(result, list)
        assert len(result) >= 2

    def test_generate_exploratory_mutations_returns_multiple(self):
        """Verify _generate_exploratory_mutations() returns multiple mutations."""
        mutator = KiloResearchMutator()
        genome = SkillGenome(
            skill_selections=["skill1"],
            timeout_ms=5000,
        )

        result = mutator._generate_exploratory_mutations(genome)

        assert len(result) == 3
        assert all(isinstance(m, SkillGenome) for m in result)


class TestMockResearchMutator:
    """Test MockResearchMutator behavior."""

    def test_mock_research_returns_mock_findings(self):
        """Verify mock mutator returns mock findings."""
        mutator = MockResearchMutator()
        failures = [
            SkillFailureCase(
                data_point_id="1", skill_name="s1", failure_category="timeout"
            )
        ]

        result = mutator._perform_research(failures)

        assert "web_findings" in result
        assert "code_findings" in result
        assert "patterns" in result
        assert len(result["web_findings"]) == 2

    def test_mock_research_identifies_patterns(self):
        """Verify mock mutator still identifies patterns."""
        mutator = MockResearchMutator()
        failures = [
            SkillFailureCase(
                data_point_id="1", skill_name="s1", failure_category="accuracy"
            )
        ]

        result = mutator._perform_research(failures)

        assert "accuracy_issues" in result["patterns"]
