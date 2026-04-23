from __future__ import annotations

import pickle
from typing import TYPE_CHECKING, Any, Dict, TypeVar

try:
    from darwinian_evolver.population import (
        WeightedSamplingPopulation as BaseWeightedPopulation,
    )

    DARWINIAN_AVAILABLE = True
except ImportError:
    DARWINIAN_AVAILABLE = False
    from typing import Protocol

    _O = TypeVar("_O")

    class BaseWeightedPopulation(Protocol[_O]):
        """Dummy population for when darwinian-evolver is not installed."""

        pass


from .config import EvolutionConfig
from .genome import SkillFitnessResult, SkillGenome

if TYPE_CHECKING:
    pass


class SkillPopulation(BaseWeightedPopulation):
    """Population implementation for skill genomes with weighted sampling."""

    def __init__(
        self,
        initial_genome: SkillGenome,
        initial_fitness: SkillFitnessResult,
        config: EvolutionConfig | None = None,
    ):
        self.config = config or EvolutionConfig()

        super().__init__(
            initial_organism=initial_genome,
            initial_evaluation_result=initial_fitness,
            sharpness=self.config.sharpness,
            fixed_midpoint_score=self.config.fixed_midpoint_score,
            midpoint_score_percentile=self.config.midpoint_score_percentile,
            novelty_weight=self.config.novelty_weight,
        )

    @classmethod
    def from_snapshot(
        cls, snapshot: bytes, config: EvolutionConfig | None = None
    ) -> SkillPopulation:
        """Restore population from snapshot."""
        population = super().from_snapshot(snapshot)
        population.config = config or EvolutionConfig()

        if isinstance(population, cls):
            population.config = config or EvolutionConfig()

        return population

    def snapshot(self) -> bytes:
        """Create snapshot of current population."""
        snapshot_dict = pickle.loads(super().snapshot())
        snapshot_dict["config"] = self.config.to_dict()
        return pickle.dumps(snapshot_dict)

    def get_statistics(self) -> Dict[str, Any]:
        """Get population statistics."""
        return {
            "population_size": len(self.organisms),
            "score_percentiles": self.get_score_percentiles(),
            "best_score": self.get_best()[1].score if self.organisms else 0.0,
            "viable_count": sum(1 for _, result in self.organisms if result.is_viable),
            "total_mutations": sum(
                len(self.get_children(org)) for org, _ in self.organisms
            ),
        }


class EvolutionStatistics:
    """Track evolution statistics over time."""

    def __init__(self):
        self.iteration_scores: list[float] = []
        self.iteration_population_sizes: list[int] = []
        self.best_scores: list[float] = []
        self.stagnation_count: int = 0

    def record_iteration(self, iteration: int, population: SkillPopulation) -> None:
        """Record statistics for an iteration."""
        best = population.get_best()
        self.iteration_scores.append(best[1].score)
        self.iteration_population_sizes.append(len(population.organisms))
        self.best_scores.append(best[1].score)

    def should_stop(self, patience: int, threshold: float) -> bool:
        """Determine if evolution should stop based on stagnation."""
        if len(self.best_scores) < 2:
            return False

        recent_improvement = self.best_scores[-1] - self.best_scores[-2]

        if abs(recent_improvement) < threshold:
            self.stagnation_count += 1
        else:
            self.stagnation_count = 0

        return self.stagnation_count >= patience

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of evolution statistics."""

if __name__ == "__main__":
    if not self.best_scores:
                return {}

            return {
                "total_iterations": len(self.best_scores),
                "initial_best": self.best_scores[0],
                "final_best": self.best_scores[-1],
                "improvement": self.best_scores[-1] - self.best_scores[0],
                "max_score": max(self.best_scores),
                "stagnation_periods": self.stagnation_count,
            }