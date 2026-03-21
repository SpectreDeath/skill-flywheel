from __future__ import annotations

import logging
import time
from collections.abc import Generator
from typing import Any, Dict, List, Union

from .config import EvolutionConfig
from .evaluator import SkillExecutor, SkillFitnessEvaluator
from .evolvable_skill_groups import (
    EVOLVABLE_SKILL_GROUPS,
    EvolableSkillGroup,
    create_genome_for_group,
    get_evolvable_group,
)
from .evolver import SkillEvolver, create_skill_evolver
from .genome import SkillFitnessResult, SkillGenome

logger = logging.getLogger(__name__)


class SyncMockSkillExecutor(SkillExecutor):
    """Synchronous mock executor for testing that returns mixed results."""

    _execution_count = 0

    def execute(
        self, skill_name: str, input_data: Dict[str, Any], parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Mock execution that returns simulated results with occasional failures."""
        time.sleep(0.01)

        SyncMockSkillExecutor._execution_count += 1

        should_fail = (
            SyncMockSkillExecutor._execution_count > 15
            and SyncMockSkillExecutor._execution_count % 4 == 0
        )

        if should_fail:
            raise RuntimeError(f"Simulated failure in {skill_name}")

        return {
            "result": f"Processed {skill_name} with {input_data}",
            "success": True,
            "skill_name": skill_name,
        }


class SkillEvolutionRunner:
    """High-level interface for running skill evolution.

    Provides a simplified API for initializing and running evolutionary
    optimization of skill configurations.
    """

    def __init__(
        self,
        skill_group: Union[str, EvolableSkillGroup],
        config: EvolutionConfig | None = None,
        output_dir: str | None = None,
        llm_client: Any = None,
        mutator_type: str = "auto",
    ):
        """Initialize the runner with a skill group.

        Args:
            skill_group: Either a group name (str) or an EvolableSkillGroup instance
            config: Evolution configuration (uses defaults if not provided)
            output_dir: Directory for evolution output files
            llm_client: Optional LLM client for mutations (supports local models)
            mutator_type: Type of mutator ("auto", "llm", "research", "parameter", "structure")
        """
        if isinstance(skill_group, str):
            group = get_evolvable_group(skill_group)
            if group is None:
                available = ", ".join(list_evolvable_groups())
                raise ValueError(
                    f"Unknown skill group: '{skill_group}'. Available: {available}"
                )
            self._group = group
        else:
            self._group = skill_group

        self._config = config or EvolutionConfig()
        self._output_dir = output_dir
        self._llm_client = llm_client
        self._mutator_type = mutator_type
        self._evolver: SkillEvolver | None = None
        self._initialized = False

    @property
    def group_name(self) -> str:
        """Get the name of the skill group being evolved."""
        return self._group.name

    @property
    def test_cases(self) -> List[Dict[str, Any]]:
        """Get the test cases for this skill group."""
        return self._group.test_cases

    def initialize(self) -> None:
        """Set up the evolver with the skill group's test cases.

        Creates an initial genome from the skill group configuration,
        sets up the evaluator with test cases, and initializes the evolver.
        """
        logger.info(f"Initializing evolution runner for group: {self.group_name}")

        initial_genome = create_genome_for_group(
            self._group.name,
            orchestration_strategy=self._group.orchestration_modes[0],
            custom_parameters=self._group.default_parameters,
        )

        if initial_genome is None:
            raise RuntimeError(
                f"Failed to create initial genome for group: {self.group_name}"
            )

        executor = SyncMockSkillExecutor()

        evaluator = SkillFitnessEvaluator(
            skill_executor=executor,
            test_cases=self._group.test_cases,
            config=self._config,
            output_dir=self._output_dir,
        )

        self._evolver = create_skill_evolver(
            initial_genome=initial_genome,
            evaluator=evaluator,
            config=self._config,
            output_dir=self._output_dir,
            llm_client=self._llm_client,
            mutator_type=self._mutator_type,
        )

        self._evolver.initialize()
        self._initialized = True

        logger.info(f"Evolution runner initialized for {self.group_name}")

    def run(
        self, iterations: int | None = None
    ) -> Generator[Dict[str, Any], None, None]:
        """Run evolution for the specified number of iterations.

        Args:
            iterations: Number of iterations to run (uses config default if not provided)

        Yields:
            Dictionary containing iteration statistics
        """
        if not self._initialized:
            self.initialize()

        if self._evolver is None:
            raise RuntimeError("Evolver not initialized. Call initialize() first.")

        yield from self._evolver.run(num_iterations=iterations)

    def run_all(self, iterations: int | None = None) -> List[Dict[str, Any]]:
        """Run evolution and collect all results.

        Args:
            iterations: Number of iterations to run

        Returns:
            List of iteration results
        """
        return list(self.run(iterations=iterations))

    def get_best_genome(self) -> SkillGenome | None:
        """Returns the best evolved genome.

        Returns:
            The best performing SkillGenome, or None if evolution hasn't run
        """
        if self._evolver is None or self._evolver.population is None:
            return None

        best = self._evolver.population.get_best()
        return best[0] if best else None

    def get_best_fitness(self) -> SkillFitnessResult | None:
        """Returns the fitness result for the best genome.

        Returns:
            The fitness result for the best genome, or None if evolution hasn't run
        """
        if self._evolver is None or self._evolver.population is None:
            return None

        best = self._evolver.population.get_best()
        return best[1] if best else None

    def get_statistics(self) -> Dict[str, Any]:
        """Returns evolution statistics.

        Returns:
            Dictionary containing evolution statistics
        """
        if self._evolver is None:
            return {
                "initialized": False,
                "iterations_completed": 0,
            }

        stats = self._evolver.statistics.get_summary()
        return {
            "initialized": self._initialized,
            "iterations_completed": self._evolver.statistics.iteration,
            "best_score": stats.get("best_score"),
            "average_score": stats.get("average_score"),
            "worst_score": stats.get("worst_score"),
            "population_size": stats.get("population_size"),
        }


def create_runner(
    group_name: str,
    config: EvolutionConfig | None = None,
    output_dir: str | None = None,
    llm_client: Any = None,
    mutator_type: str = "auto",
) -> SkillEvolutionRunner:
    """Factory function to create a runner from a group name.

    Args:
        group_name: Name of the evolvable skill group
        config: Evolution configuration
        output_dir: Directory for output files
        llm_client: Optional LLM client for mutations (supports local models)
        mutator_type: Type of mutator ("auto", "llm", "research", "parameter", "structure")

    Returns:
        Configured SkillEvolutionRunner instance

    Raises:
        ValueError: If the group name is not recognized
    """
    return SkillEvolutionRunner(
        skill_group=group_name,
        config=config,
        output_dir=output_dir,
        llm_client=llm_client,
        mutator_type=mutator_type,
    )


def run_evolution(
    group_name: str,
    iterations: int | None = None,
    config: EvolutionConfig | None = None,
    output_dir: str | None = None,
    llm_client: Any = None,
    mutator_type: str = "auto",
) -> Dict[str, Any]:
    """Convenience function to run evolution in one call.

    Args:
        group_name: Name of the evolvable skill group
        iterations: Number of iterations to run
        config: Evolution configuration
        output_dir: Directory for output files
        llm_client: Optional LLM client for mutations (supports local models)
        mutator_type: Type of mutator ("auto", "llm", "research", "parameter", "structure")

    Returns:
        Dictionary containing:
            - best_genome: The best evolved genome
            - best_fitness: Fitness result for the best genome
            - statistics: Evolution statistics
            - results: List of iteration results
    """
    runner = create_runner(
        group_name=group_name,
        config=config,
        output_dir=output_dir,
        llm_client=llm_client,
        mutator_type=mutator_type,
    )

    results = runner.run_all(iterations=iterations)

    return {
        "best_genome": runner.get_best_genome(),
        "best_fitness": runner.get_best_fitness(),
        "statistics": runner.get_statistics(),
        "results": results,
    }


def list_evolvable_groups() -> List[str]:
    """Returns all available evolvable group names."""
    return list(EVOLVABLE_SKILL_GROUPS.keys())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    print("=" * 60)
    print("Skill Evolution Runner Demo")
    print("=" * 60)

    available_groups = list_evolvable_groups()
    print(f"\nAvailable skill groups: {', '.join(available_groups)}")

    print("\n" + "-" * 60)
    print("Creating runner for 'clustering_ensemble' group")
    print("-" * 60 + "\n")

    config = EvolutionConfig(
        max_iterations=3,
        snapshot_interval=1,
        random_seed=42,
    )

    runner = create_runner(
        group_name="clustering_ensemble",
        config=config,
        output_dir="evolution_output_demo",
    )

    print(f"Created runner for: {runner.group_name}")
    print(f"Number of test cases: {len(runner.test_cases)}")

    print("\nTest cases:")
    for tc in runner.test_cases:
        print(f"  - {tc['name']}")

    print("\nInitializing runner...")
    runner.initialize()

    print("Runner initialized successfully!")
    print(f"Evolution statistics: {runner.get_statistics()}")

    print("\nNote: Full evolution requires LLM client configuration for the mutator.")
    print("The darwinian-evolver integration requires a properly configured")
    print("environment with an LLM provider to generate meaningful mutations.")
