from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EvolutionConfig:
    """Configuration for the skill evolution process."""

    population_size: int = 20
    num_parents_per_iteration: int = 5
    batch_size: int = 2
    sharpness: float = 10.0
    midpoint_score_percentile: float = 75.0
    fixed_midpoint_score: Optional[float] = None
    novelty_weight: float = 1.0
    should_verify_mutations: bool = True
    max_iterations: int = 50
    mutator_concurrency: int = 5
    evaluator_concurrency: int = 5
    learning_log_strategy: str = "neighborhood-1"
    use_process_pool_executors: bool = False
    random_seed: Optional[int] = None
    snapshot_interval: int = 5
    early_stopping_patience: int = 10
    early_stopping_threshold: float = 0.01
    timeout_ms: int = 30000
    metrics_weights: Dict[str, float] = field(
        default_factory=lambda: {
            "performance": 0.4,
            "accuracy": 0.4,
            "resource_efficiency": 0.2,
        }
    )

    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.population_size < 2:
            raise ValueError("population_size must be at least 2")
        if self.num_parents_per_iteration >= self.population_size:
            raise ValueError(
                "num_parents_per_iteration must be less than population_size"
            )
        if self.batch_size < 1:
            raise ValueError("batch_size must be at least 1")
        if self.sharpness <= 0:
            raise ValueError("sharpness must be positive")
        if not 0 <= self.midpoint_score_percentile <= 100:
            raise ValueError("midpoint_score_percentile must be between 0 and 100")
        if self.max_iterations < 1:
            raise ValueError("max_iterations must be positive")
        if self.mutator_concurrency < 1:
            raise ValueError("mutator_concurrency must be positive")
        if self.evaluator_concurrency < 1:
            raise ValueError("evaluator_concurrency must be positive")
        if self.learning_log_strategy not in [
            "none",
            "ancestors",
        ] and not self.learning_log_strategy.startswith("neighborhood-"):
            raise ValueError(
                "learning_log_strategy must be 'none', 'ancestors', or 'neighborhood-N'"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "population_size": self.population_size,
            "num_parents_per_iteration": self.num_parents_per_iteration,
            "batch_size": self.batch_size,
            "sharpness": self.sharpness,
            "midpoint_score_percentile": self.midpoint_score_percentile,
            "fixed_midpoint_score": self.fixed_midpoint_score,
            "novelty_weight": self.novelty_weight,
            "should_verify_mutations": self.should_verify_mutations,
            "max_iterations": self.max_iterations,
            "mutator_concurrency": self.mutator_concurrency,
            "evaluator_concurrency": self.evaluator_concurrency,
            "learning_log_strategy": self.learning_log_strategy,
            "use_process_pool_executors": self.use_process_pool_executors,
            "random_seed": self.random_seed,
            "snapshot_interval": self.snapshot_interval,
            "early_stopping_patience": self.early_stopping_patience,
            "early_stopping_threshold": self.early_stopping_threshold,
            "metrics_weights": self.metrics_weights,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EvolutionConfig:
        """Create config from dictionary."""
        return cls(**data)
