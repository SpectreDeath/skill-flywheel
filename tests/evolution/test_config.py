import pytest

from flywheel.evolution.config import EvolutionConfig


class TestEvolutionConfig:
    """Tests for EvolutionConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = EvolutionConfig()

        assert config.population_size == 20
        assert config.num_parents_per_iteration == 5
        assert config.batch_size == 2
        assert config.sharpness == 10.0
        assert config.midpoint_score_percentile == 75.0
        assert config.novelty_weight == 1.0
        assert config.should_verify_mutations is True
        assert config.max_iterations == 50

    def test_custom_config(self):
        """Test custom configuration."""
        config = EvolutionConfig(
            population_size=50,
            num_parents_per_iteration=10,
            max_iterations=100,
            random_seed=42,
        )

        assert config.population_size == 50
        assert config.num_parents_per_iteration == 10
        assert config.max_iterations == 100
        assert config.random_seed == 42

    def test_invalid_population_size(self):
        """Test validation of population size."""
        with pytest.raises(ValueError):
            EvolutionConfig(population_size=1)

    def test_invalid_parents(self):
        """Test validation of parents per iteration."""
        with pytest.raises(ValueError):
            EvolutionConfig(num_parents_per_iteration=100)

    def test_invalid_batch_size(self):
        """Test validation of batch size."""
        with pytest.raises(ValueError):
            EvolutionConfig(batch_size=0)

    def test_invalid_sharpness(self):
        """Test validation of sharpness."""
        with pytest.raises(ValueError):
            EvolutionConfig(sharpness=0)

    def test_invalid_percentile(self):
        """Test validation of percentile."""
        with pytest.raises(ValueError):
            EvolutionConfig(midpoint_score_percentile=150)

    def test_invalid_learning_log_strategy(self):
        """Test validation of learning log strategy."""
        with pytest.raises(ValueError):
            EvolutionConfig(learning_log_strategy="invalid")

    def test_valid_learning_log_strategies(self):
        """Test valid learning log strategies."""
        config1 = EvolutionConfig(learning_log_strategy="none")
        assert config1.learning_log_strategy == "none"

        config2 = EvolutionConfig(learning_log_strategy="ancestors")
        assert config2.learning_log_strategy == "ancestors"

        config3 = EvolutionConfig(learning_log_strategy="neighborhood-2")
        assert config3.learning_log_strategy == "neighborhood-2"

    def test_to_dict(self):
        """Test serialization to dictionary."""
        config = EvolutionConfig(population_size=30, max_iterations=25)
        d = config.to_dict()

        assert d["population_size"] == 30
        assert d["max_iterations"] == 25

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {"population_size": 40, "max_iterations": 20, "sharpness": 15.0}
        config = EvolutionConfig.from_dict(data)

        assert config.population_size == 40
        assert config.max_iterations == 20
        assert config.sharpness == 15.0

    def test_metrics_weights_default(self):
        """Test default metrics weights."""
        config = EvolutionConfig()

        assert config.metrics_weights["performance"] == 0.4
        assert config.metrics_weights["accuracy"] == 0.4
        assert config.metrics_weights["resource_efficiency"] == 0.2

    def test_metrics_weights_custom(self):
        """Test custom metrics weights."""
        weights = {"performance": 0.5, "accuracy": 0.3, "resource_efficiency": 0.2}
        config = EvolutionConfig(metrics_weights=weights)

        assert config.metrics_weights == weights
