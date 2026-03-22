"""Tests for evolution experiments module - behavior verification."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest


class TestExperimentResult:
    """Test ExperimentResult dataclass behavior."""

    def test_create_result_with_fitness(self):
        """Verify result captures best fitness score correctly."""
        from flywheel.evolution.experiments import ExperimentResult

        result = ExperimentResult(
            name="test_exp",
            config={"population_size": 10},
            metrics={"generations": 5},
            best_fitness=0.95,
            iterations_completed=100,
            duration_seconds=12.5,
        )

        assert result.best_fitness == 0.95
        assert result.best_fitness <= 1.0  # Fitness should be normalized
        assert result.best_fitness >= 0.0

    def test_create_result_with_error(self):
        """Verify failed experiment captures error message."""
        from flywheel.evolution.experiments import ExperimentResult

        result = ExperimentResult(
            name="failed_exp",
            config={},
            metrics={},
            error="Connection timeout",
        )

        assert result.error == "Connection timeout"
        assert result.best_fitness == 0.0  # Default when failed
        assert result.iterations_completed == 0  # Default when failed

    def test_fitness_is_optional(self):
        """Verify fitness defaults to 0.0 when not provided."""
        from flywheel.evolution.experiments import ExperimentResult

        result = ExperimentResult(
            name="empty_exp",
            config={},
            metrics={},
        )

        assert result.best_fitness == 0.0
        assert result.best_genome is None


class TestExperimentSuite:
    """Test ExperimentSuite behavior."""

    def test_suite_creates_output_directory(self, tmp_path):
        """Verify suite creates output directory on initialization."""
        from flywheel.evolution.experiments import ExperimentSuite

        suite = ExperimentSuite(output_dir=str(tmp_path / "experiments"))

        assert (tmp_path / "experiments").exists()
        assert (tmp_path / "experiments").is_dir()

    def test_add_result_increases_count(self, tmp_path):
        """Verify adding results increases the suite count."""
        from flywheel.evolution.experiments import ExperimentSuite, ExperimentResult

        suite = ExperimentSuite(output_dir=str(tmp_path / "exp"))

        assert len(suite.results) == 0

        suite.add_result(ExperimentResult(name="exp1", config={}, metrics={}))
        assert len(suite.results) == 1

        suite.add_result(ExperimentResult(name="exp2", config={}, metrics={}))
        assert len(suite.results) == 2

    def test_save_summary_counts_success_and_failure(self, tmp_path):
        """Verify summary correctly counts successful vs failed experiments."""
        from flywheel.evolution.experiments import ExperimentSuite, ExperimentResult

        suite = ExperimentSuite(output_dir=str(tmp_path / "results"))

        # Add successful experiment
        suite.add_result(
            ExperimentResult(name="success", config={}, metrics={}, best_fitness=0.9)
        )
        # Add failed experiment
        suite.add_result(
            ExperimentResult(name="failure", config={}, metrics={}, error="timeout")
        )

        summary_file = suite.save_summary()

        # Verify file was created
        assert Path(summary_file).exists()

        # Verify content
        with open(summary_file) as f:
            data = json.load(f)

        assert data["total_experiments"] == 2
        assert data["successful"] == 1
        assert data["failed"] == 1

    def test_save_summary_contains_fitness_values(self, tmp_path):
        """Verify summary includes fitness scores for comparison."""
        from flywheel.evolution.experiments import ExperimentSuite, ExperimentResult

        suite = ExperimentSuite(output_dir=str(tmp_path / "results"))

        suite.add_result(
            ExperimentResult(name="best", config={}, metrics={}, best_fitness=0.95)
        )
        suite.add_result(
            ExperimentResult(name="worst", config={}, metrics={}, best_fitness=0.3)
        )

        summary_file = suite.save_summary()

        with open(summary_file) as f:
            data = json.load(f)

        assert len(data["results"]) == 2
        fitness_values = [r["best_fitness"] for r in data["results"]]
        assert 0.95 in fitness_values
        assert 0.3 in fitness_values


class TestRunSingleExperiment:
    """Test experiment execution behavior."""

    def test_returns_experiment_result_on_success(self, tmp_path):
        """Verify experiment returns result with fitness score."""
        from flywheel.evolution.experiments import run_single_experiment
        from flywheel.evolution.config import EvolutionConfig

        # Create config with valid parameters
        config = EvolutionConfig(
            max_iterations=1,
            population_size=5,
            num_parents_per_iteration=2,
        )

        # Mock the runner to avoid actual evolution
        mock_runner = Mock()
        mock_fitness = Mock()
        mock_fitness.score = 0.75
        mock_runner.get_best_genome.return_value = Mock()
        mock_runner.get_best_fitness.return_value = mock_fitness
        mock_runner.get_statistics.return_value = {"generations": 1}

        with patch(
            "flywheel.evolution.experiments.create_runner", return_value=mock_runner
        ):
            result = run_single_experiment(
                name="test",
                group_name="test_group",
                config=config,
                iterations=1,
                output_subdir=str(tmp_path / "output"),
            )

        assert result.name == "test"
        assert result.best_fitness == 0.75
        assert result.error is None

    def test_returns_error_on_exception(self, tmp_path):
        """Verify experiment captures exceptions as errors."""
        from flywheel.evolution.experiments import run_single_experiment
        from flywheel.evolution.config import EvolutionConfig

        config = EvolutionConfig(
            max_iterations=1,
            population_size=5,
            num_parents_per_iteration=2,
        )

        # Mock runner that raises exception
        with patch(
            "flywheel.evolution.experiments.create_runner",
            side_effect=RuntimeError("OOM"),
        ):
            result = run_single_experiment(
                name="failing_test",
                group_name="test",
                config=config,
                output_subdir=str(tmp_path / "out"),
            )

        assert result.error is not None
        assert "OOM" in result.error
        assert result.best_fitness == 0.0  # Fitness should be 0 on failure

    def test_records_duration(self, tmp_path):
        """Verify experiment records how long it took."""
        from flywheel.evolution.experiments import run_single_experiment
        from flywheel.evolution.config import EvolutionConfig

        config = EvolutionConfig(
            max_iterations=1,
            population_size=5,
            num_parents_per_iteration=2,
        )

        mock_runner = Mock()
        mock_runner.get_best_genome.return_value = None
        mock_runner.get_best_fitness.return_value = None
        mock_runner.get_statistics.return_value = {}

        with patch(
            "flywheel.evolution.experiments.create_runner", return_value=mock_runner
        ):
            result = run_single_experiment(
                name="timing_test",
                group_name="test",
                config=config,
                output_subdir=str(tmp_path / "out"),
            )

        assert result.duration_seconds >= 0
        assert result.iterations_completed == 0


class TestEvolutionConfigValidation:
    """Test EvolutionConfig validation rules."""

    def test_population_size_must_exceed_parents(self):
        """Verify config requires population_size > num_parents_per_iteration."""
        from flywheel.evolution.config import EvolutionConfig

        with pytest.raises(
            ValueError,
            match="num_parents_per_iteration must be less than population_size",
        ):
            EvolutionConfig(
                population_size=3,
                num_parents_per_iteration=3,  # Equal is not allowed
            )

    def test_valid_config_accepts_small_population(self):
        """Verify valid small population works."""
        from flywheel.evolution.config import EvolutionConfig

        # This should not raise
        config = EvolutionConfig(
            population_size=4,
            num_parents_per_iteration=2,
        )

        assert config.population_size == 4
        assert config.num_parents_per_iteration == 2

    def test_config_has_valid_parameters(self):
        """Verify config has required parameters."""
        from flywheel.evolution.config import EvolutionConfig

        config = EvolutionConfig(population_size=5, num_parents_per_iteration=2)

        assert config.population_size == 5
        assert config.num_parents_per_iteration == 2
        assert config.max_iterations > 0
        assert config.early_stopping_threshold >= 0
        assert isinstance(config.metrics_weights, dict)
