from __future__ import annotations

import json
import logging
import random
from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, TypeVar

try:
    from darwinian_evolver.evolver import Evolver
    from darwinian_evolver.learning_log_view import (
        AncestorLearningLogView,
        EmptyLearningLogView,
        NeighborhoodLearningLogView,
    )
    from darwinian_evolver.problem import MutatorContext

    DARWINIAN_AVAILABLE = True
except ImportError:
    DARWINIAN_AVAILABLE = False
    from typing import Protocol

    class Evolver(Protocol):
        """Dummy evolver for when darwinian-evolver is not installed."""

        pass

    class MutatorContext(Protocol):
        """Dummy mutator context for when darwinian-evolver is not installed."""

        pass

    class AncestorLearningLogView(Protocol):
        """Dummy learning log view for when darwinian-evolver is not installed."""

        pass

    class EmptyLearningLogView(Protocol):
        """Dummy learning log view for when darwinian-evolver is not installed."""

        pass

    class NeighborhoodLearningLogView(Protocol):
        """Dummy learning log view for when darwinian-evolver is not installed."""

        pass


from .config import EvolutionConfig
from .evaluator import SkillFitnessEvaluator
from .genome import SkillGenome
from .mutator import LLMMutator, ParameterTuningMutator, StructureMutationMutator
from .population import EvolutionStatistics, SkillPopulation

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class SkillEvolver:
    """Main evolver class for skill genome evolution."""

    def __init__(
        self,
        initial_genome: SkillGenome,
        evaluator: SkillFitnessEvaluator,
        mutators: List[LLMMutator],
        config: EvolutionConfig | None = None,
        output_dir: str | None = None,
    ):
        self.config = config or EvolutionConfig()
        self.output_dir = Path(output_dir) if output_dir else Path("evolution_output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if self.config.random_seed is not None:
            random.seed(self.config.random_seed)

        self.evaluator = evaluator
        self.mutators = mutators
        self._initial_genome = initial_genome

        self._setup_learning_log_view()

        self._evolver: Evolver | None = None
        self._population: SkillPopulation | None = None
        self._statistics = EvolutionStatistics()
        self._current_iteration = 0

    def _setup_learning_log_view(self) -> None:
        """Setup the learning log view based on configuration."""
        strategy = self.config.learning_log_strategy

        if strategy == "none":
            self._learning_log_view_type = (EmptyLearningLogView, {})
        elif strategy == "ancestors":
            self._learning_log_view_type = (AncestorLearningLogView, {})
        elif strategy.startswith("neighborhood-"):
            n = int(strategy.split("-")[1])
            self._learning_log_view_type = (
                NeighborhoodLearningLogView,
                {"max_distance": n},
            )
        else:
            self._learning_log_view_type = (EmptyLearningLogView, {})

    def initialize(self) -> None:
        """Initialize the evolver and population."""
        logger.info("Initializing skill evolver...")

        initial_result = self.evaluator.evaluate(self._initial_genome)

        self._population = SkillPopulation(
            initial_genome=self._initial_genome,
            initial_fitness=initial_result,
            config=self.config,
        )

        for mutator in self.mutators:
            mutator.set_context(MutatorContext(population=self._population))

        self._populate_initial_population()

        self._evolver = Evolver(
            population=self._population,
            mutators=self.mutators,
            evaluator=self.evaluator,
            learning_log_view_type=self._learning_log_view_type,
            mutator_concurrency=self.config.mutator_concurrency,
            evaluator_concurrency=self.config.evaluator_concurrency,
            batch_size=self.config.batch_size,
            should_verify_mutations=self.config.should_verify_mutations,
            use_process_pool_executors=self.config.use_process_pool_executors,
        )

        logger.info(f"Initialized with initial fitness: {initial_result.score}")

    def _populate_initial_population(self) -> None:
        """Populate initial population with mutated variants."""

        target_size = self.config.population_size

        while len(self._population.organisms) < target_size:
            for mutator in self.mutators:
                if len(self._population.organisms) >= target_size:
                    break

                try:
                    mutated_genomes = mutator.mutate(
                        self._initial_genome,
                        failure_cases=[],
                        learning_log_entries=[],
                    )

                    for mutated in mutated_genomes:
                        if len(self._population.organisms) >= target_size:
                            break

                        fitness_result = self.evaluator.evaluate(mutated)
                        if fitness_result.is_viable:
                            self._population.add(mutated, fitness_result)
                except Exception as e:
                    logger.warning(f"Failed to create mutated organism: {e}")
                    continue

        logger.info(
            f"Populated initial population with {len(self._population.organisms)} organisms"
        )

    def run(
        self, num_iterations: int | None = None
    ) -> Generator[Dict[str, Any], None, None]:
        """Run the evolution for specified number of iterations."""
        num_iterations = num_iterations or self.config.max_iterations

        if not self._evolver:
            self.initialize()

        logger.info(f"Starting evolution for {num_iterations} iterations...")

        for i in range(num_iterations):
            logger.info(f"Running iteration {i + 1}/{num_iterations}")

            stats = self._evolver.evolve_iteration(
                num_parents=self.config.num_parents_per_iteration,
                iteration=self._current_iteration,
            )

            self._current_iteration += 1

            snapshot_data = self._create_snapshot()
            self._statistics.record_iteration(self._current_iteration, self._population)

            if (i + 1) % self.config.snapshot_interval == 0:
                self._save_snapshot(i)

            yield {
                "iteration": self._current_iteration,
                "population_size": len(self._population.organisms),
                "best_score": snapshot_data["best_score"],
                "stats": stats.model_dump(),
            }

            if self._statistics.should_stop(
                self.config.early_stopping_patience,
                self.config.early_stopping_threshold,
            ):
                logger.info("Early stopping triggered due to stagnation")
                break

        logger.info("Evolution complete!")
        self._save_final_results()

    def _create_snapshot(self) -> Dict[str, Any]:
        """Create a snapshot of current state."""
        best = self._population.get_best()

        return {
            "iteration": self._current_iteration,
            "population_size": len(self._population.organisms),
            "best_score": best[1].score,
            "best_genome": self._serialize_genome(best[0]),
            "population_snapshot": self._population.snapshot(),
        }

    def _serialize_genome(self, genome: SkillGenome) -> Dict[str, Any]:
        """Serialize genome for JSON output."""
        return {
            "skill_selections": genome.skill_selections,
            "skill_parameters": genome.skill_parameters,
            "prompt_templates": genome.prompt_templates,
            "resource_allocation": genome.resource_allocation,
            "orchestration_strategy": genome.orchestration_strategy,
            "timeout_ms": genome.timeout_ms,
        }

    def _save_snapshot(self, iteration: int) -> None:
        """Save iteration snapshot to disk."""
        snapshot_file = self.output_dir / f"snapshot_iter_{iteration}.json"

        snapshot_data = self._create_snapshot()

        with open(snapshot_file, "w") as f:
            json.dump(snapshot_data, f, indent=2, default=str)

        logger.info(f"Saved snapshot to {snapshot_file}")

    def _save_final_results(self) -> None:
        """Save final evolution results."""
        results_file = self.output_dir / "evolution_results.json"

        best = self._population.get_best()

        results = {
            "config": self.config.to_dict(),
            "statistics": self._statistics.get_summary(),
            "best_genome": self._serialize_genome(best[0]),
            "best_fitness": {
                "score": best[1].score,
                "performance_score": best[1].performance_score,
                "accuracy_score": best[1].accuracy_score,
                "resource_efficiency": best[1].resource_efficiency,
            },
        }

        with open(results_file, "w") as f:
            json.dump(results, f, indent=2, default=str)

        logger.info(f"Saved results to {results_file}")

    @property
    def population(self) -> SkillPopulation | None:
        """Get current population."""
        return self._population

    @property
    def statistics(self) -> EvolutionStatistics:
        """Get evolution statistics."""
        return self._statistics


def create_skill_evolver(
    initial_genome: SkillGenome,
    evaluator: SkillFitnessEvaluator,
    config: EvolutionConfig | None = None,
    output_dir: str | None = None,
    llm_client: Any = None,
    mutator_type: str = "auto",
) -> SkillEvolver:
    """Factory function to create a skill evolver.

    Args:
        initial_genome: Starting genome for evolution
        evaluator: Fitness evaluator
        config: Evolution configuration
        output_dir: Output directory for results
        llm_client: Optional LLM client for mutations
        mutator_type: Type of mutator to use ("llm", "research", "parameter", "structure", "auto")
                     - "auto": Use LLM if available, otherwise research-based
                     - "llm": Use LLM mutator only
                     - "research": Use KiloResearchMutator
                     - "parameter": Use parameter tuning only
                     - "structure": Use structure mutation only
    """
    config = config or EvolutionConfig()

    if mutator_type == "llm":
        mutators = [LLMMutator(llm_client=llm_client)]
    elif mutator_type == "research":
        from .kilo_research_mutator import KiloResearchMutator

        mutators = [KiloResearchMutator()]
    elif mutator_type == "parameter":
        mutators = [ParameterTuningMutator(tuning_strategy="random")]
    elif mutator_type == "structure":
        mutators = [StructureMutationMutator()]
    elif mutator_type == "auto":
        if llm_client:
            mutators = [LLMMutator(llm_client=llm_client)]
        else:
            from .kilo_research_mutator import KiloResearchMutator

            mutators = [KiloResearchMutator()]
    else:
        mutators = [LLMMutator(llm_client=llm_client)]

    return SkillEvolver(
        initial_genome=initial_genome,
        evaluator=evaluator,
        mutators=mutators,
        config=config,
        output_dir=output_dir,
    )
