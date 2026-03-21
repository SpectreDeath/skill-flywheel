from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from .config import EvolutionConfig
from .evolvable_skill_groups import (
    EVOLVABLE_SKILL_GROUPS,
    create_genome_for_group,
    get_evolvable_group,
)
from .runner import SyncMockSkillExecutor, create_runner, run_evolution
from .evaluator import SkillFitnessEvaluator
from .evolver import create_skill_evolver

LOCAL_LLM_CLIENT_MODULE = None
try:
    from . import local_llm_client

    LOCAL_LLM_CLIENT_MODULE = local_llm_client
except ImportError:
    pass


def get_llm_client() -> Any:
    """Get an LLM client if available.

    Set USE_LOCAL_MODEL=false to disable local model auto-detection.
    Returns None if no LLM is available - experiments will use research mutator.
    """
    if os.environ.get("USE_LOCAL_MODEL", "true").lower() == "false":
        return None

    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        return None

    if LOCAL_LLM_CLIENT_MODULE is None:
        return None

    try:
        client = LOCAL_LLM_CLIENT_MODULE.create_local_llm_client(
            provider=os.environ.get("LOCAL_MODEL_PROVIDER", "ollama"),
            model=os.environ.get("LLM_MODEL", "llama2"),
        )
        return client
    except Exception:
        return None


from .runner import SyncMockSkillExecutor, create_runner, run_evolution
from .evaluator import SkillFitnessEvaluator
from .evolver import create_skill_evolver

try:
    from .local_llm_client import create_local_llm_client, LocalLLMClient

    LOCAL_LLM_AVAILABLE = True
except ImportError:
    LOCAL_LLM_AVAILABLE = False
    LocalLLMClient = None


def get_llm_client() -> Any:
    """Get an LLM client if available (local or API)."""
    if not LOCAL_LLM_AVAILABLE:
        return None

    if os.environ.get("USE_LOCAL_MODEL", "").lower() == "true":
        return create_local_llm_client(
            provider=os.environ.get("LOCAL_MODEL_PROVIDER", "ollama"),
            model=os.environ.get("LLM_MODEL", "llama2"),
        )

    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        return None

    return create_local_llm_client(
        provider="ollama",
        model=os.environ.get("LLM_MODEL", "llama2"),
    )


logger = logging.getLogger(__name__)


@dataclass
class ExperimentResult:
    name: str
    config: Dict[str, Any]
    metrics: Dict[str, Any]
    best_genome: Dict[str, Any] | None = None
    best_fitness: float = 0.0
    iterations_completed: int = 0
    duration_seconds: float = 0.0
    error: str | None = None


@dataclass
class ExperimentSuite:
    output_dir: str = "experiment_results"
    results: List[ExperimentResult] = field(default_factory=list)

    def __post_init__(self):
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def add_result(self, result: ExperimentResult) -> None:
        self.results.append(result)

    def save_summary(self) -> str:
        summary_file = Path(self.output_dir) / "experiment_summary.json"
        summary = {
            "total_experiments": len(self.results),
            "successful": sum(1 for r in self.results if r.error is None),
            "failed": sum(1 for r in self.results if r.error is not None),
            "results": [
                {
                    "name": r.name,
                    "best_fitness": r.best_fitness,
                    "iterations_completed": r.iterations_completed,
                    "duration_seconds": r.duration_seconds,
                    "error": r.error,
                }
                for r in self.results
            ],
        }
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)
        return str(summary_file)


def run_single_experiment(
    name: str,
    group_name: str,
    config: EvolutionConfig,
    iterations: int | None = None,
    output_subdir: str | None = None,
    quick_mode: bool = False,
    llm_client: Any = None,
    mutator_type: str = "auto",
) -> ExperimentResult:
    """Run a single evolution experiment and return results."""
    start_time = time.time()
    output_dir = output_subdir or f"experiment_results/{name}"

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    actual_iterations = iterations or config.max_iterations
    if quick_mode:
        actual_iterations = min(actual_iterations, 2)

    try:
        runner = create_runner(
            group_name=group_name,
            config=config,
            output_dir=output_dir,
            llm_client=llm_client,
            mutator_type=mutator_type,
        )

        results = runner.run_all(iterations=actual_iterations)

        best_genome = runner.get_best_genome()
        best_fitness = runner.get_best_fitness()
        stats = runner.get_statistics()

        duration = time.time() - start_time

        return ExperimentResult(
            name=name,
            config=config.to_dict(),
            metrics=stats,
            best_genome=_serialize_genome(best_genome) if best_genome else None,
            best_fitness=best_fitness.score if best_fitness else 0.0,
            iterations_completed=stats.get("iterations_completed", 0),
            duration_seconds=duration,
        )
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Experiment '{name}' failed: {e}")
        return ExperimentResult(
            name=name,
            config=config.to_dict(),
            metrics={},
            best_fitness=0.0,
            iterations_completed=0,
            duration_seconds=duration,
            error=str(e),
        )


def _serialize_genome(genome: Any) -> Dict[str, Any]:
    """Serialize a genome for JSON output."""
    return {
        "skill_selections": genome.skill_selections,
        "skill_parameters": genome.skill_parameters,
        "prompt_templates": genome.prompt_templates,
        "resource_allocation": genome.resource_allocation,
        "orchestration_strategy": genome.orchestration_strategy,
        "timeout_ms": genome.timeout_ms,
    }


def run_experiment_1_baseline(
    output_dir: str = "experiment_results",
    quick_mode: bool = False,
    llm_client: Any = None,
    mutator_type: str = "auto",
) -> ExperimentResult:
    """Experiment 1: Baseline Evolution Run

    Goal: Verify the system works end-to-end
    Approach: Run evolution on clustering_ensemble with default config
    """
    logger.info("Running Experiment 1: Baseline Evolution")

    config = EvolutionConfig(
        population_size=2,
        num_parents_per_iteration=1,
        max_iterations=3,
        random_seed=42,
        snapshot_interval=2,
    )

    return run_single_experiment(
        name="exp1_baseline",
        group_name="clustering_ensemble",
        config=config,
        output_subdir=f"{output_dir}/exp1_baseline",
        quick_mode=quick_mode,
        llm_client=llm_client,
        mutator_type=mutator_type,
    )


def run_experiment_2_population_size(
    output_dir: str = "experiment_results",
    quick_mode: bool = False,
    llm_client: Any = None,
    mutator_type: str = "auto",
) -> List[ExperimentResult]:
    """Experiment 2: Population Size Impact

    Goal: Measure effect of population size on convergence
    Approach: Run same skill group with populations of 3, 5, 8
    """
    logger.info("Running Experiment 2: Population Size Impact")

    populations = [3, 5, 8]
    results = []

    for pop_size in populations:
        config = EvolutionConfig(
            population_size=pop_size,
            num_parents_per_iteration=min(2, pop_size - 1),
            max_iterations=5,
            random_seed=42,
            snapshot_interval=2,
        )

        result = run_single_experiment(
            name=f"exp2_pop_{pop_size}",
            group_name="clustering_ensemble",
            config=config,
            output_subdir=f"{output_dir}/exp2_pop_{pop_size}",
            quick_mode=quick_mode,
            llm_client=llm_client,
            mutator_type=mutator_type,
        )
        results.append(result)

    return results


def run_experiment_3_fitness_weights(
    output_dir: str = "experiment_results",
    quick_mode: bool = False,
    llm_client: Any = None,
    mutator_type: str = "auto",
) -> List[ExperimentResult]:
    """Experiment 3: Fitness Weight Sensitivity

    Goal: Understand how weighting affects evolved solutions
    Approach: Compare different weight configurations
    """
    logger.info("Running Experiment 3: Fitness Weight Sensitivity")

    weight_configs = [
        {
            "name": "balanced",
            "weights": {
                "performance": 0.4,
                "accuracy": 0.4,
                "resource_efficiency": 0.2,
            },
        },
        {
            "name": "performance_focus",
            "weights": {
                "performance": 0.8,
                "accuracy": 0.1,
                "resource_efficiency": 0.1,
            },
        },
        {
            "name": "accuracy_focus",
            "weights": {
                "performance": 0.1,
                "accuracy": 0.8,
                "resource_efficiency": 0.1,
            },
        },
    ]

    results = []

    for wc in weight_configs:
        config = EvolutionConfig(
            population_size=3,
            num_parents_per_iteration=2,
            max_iterations=5,
            random_seed=42,
            snapshot_interval=2,
            metrics_weights=wc["weights"],
        )

        result = run_single_experiment(
            name=f"exp3_weights_{wc['name']}",
            group_name="clustering_ensemble",
            config=config,
            output_subdir=f"{output_dir}/exp3_weights_{wc['name']}",
            quick_mode=quick_mode,
            llm_client=llm_client,
            mutator_type=mutator_type,
        )
        results.append(result)

    return results


def run_experiment_4_learning_log_strategy(
    output_dir: str = "experiment_results",
    quick_mode: bool = False,
    llm_client: Any = None,
    mutator_type: str = "auto",
) -> List[ExperimentResult]:
    """Experiment 4: Learning Log Strategy Comparison

    Goal: Compare mutation quality with different learning log views
    Approach: Run with none, ancestors, neighborhood-1
    """
    logger.info("Running Experiment 4: Learning Log Strategy Comparison")

    strategies = ["none", "ancestors", "neighborhood-1"]
    results = []

    for strategy in strategies:
        config = EvolutionConfig(
            population_size=3,
            num_parents_per_iteration=2,
            max_iterations=5,
            random_seed=42,
            snapshot_interval=2,
            learning_log_strategy=strategy,
        )

        result = run_single_experiment(
            name=f"exp4_learning_log_{strategy}",
            group_name="clustering_ensemble",
            config=config,
            output_subdir=f"{output_dir}/exp4_learning_log_{strategy}",
            quick_mode=quick_mode,
            llm_client=llm_client,
            mutator_type=mutator_type,
        )
        results.append(result)

    return results


def run_experiment_5_cross_group_transfer(
    output_dir: str = "experiment_results",
    quick_mode: bool = False,
    llm_client: Any = None,
    mutator_type: str = "auto",
) -> List[ExperimentResult]:
    """Experiment 5: Cross-Skill-Group Transfer

    Goal: Test if evolved parameters from one group work in another
    Approach: Run evolution on source group, then apply best genome to target group
    """
    logger.info("Running Experiment 5: Cross-Skill-Group Transfer")

    source_group = "clustering_ensemble"
    target_groups = ["database_optimizer"]

    source_config = EvolutionConfig(
        population_size=3,
        num_parents_per_iteration=2,
        max_iterations=5,
        random_seed=42,
        snapshot_interval=2,
    )

    source_result = run_single_experiment(
        name="exp5_source_clustering",
        group_name=source_group,
        config=source_config,
        output_subdir=f"{output_dir}/exp5_source_clustering",
        quick_mode=quick_mode,
        llm_client=llm_client,
        mutator_type=mutator_type,
    )

    results = [source_result]

    if source_result.best_genome:
        for target in target_groups:
            target_config = EvolutionConfig(
                population_size=3,
                num_parents_per_iteration=2,
                max_iterations=3,
                random_seed=42,
                snapshot_interval=2,
            )

            result = run_single_experiment(
                name=f"exp5_target_{target}",
                group_name=target,
                config=target_config,
                output_subdir=f"{output_dir}/exp5_target_{target}",
                quick_mode=quick_mode,
                llm_client=llm_client,
                mutator_type=mutator_type,
            )
            result.metrics["source_genome"] = source_result.best_genome
            results.append(result)

    return results


def run_experiment_6_early_stopping(
    output_dir: str = "experiment_results",
    quick_mode: bool = False,
    llm_client: Any = None,
    mutator_type: str = "auto",
) -> List[ExperimentResult]:
    """Experiment 6: Early Stopping Behavior

    Goal: Validate early stopping triggers correctly
    Approach: Run with different patience values
    """
    logger.info("Running Experiment 6: Early Stopping Behavior")

    patience_values = [2, 3, 5]
    results = []

    for patience in patience_values:
        config = EvolutionConfig(
            population_size=3,
            num_parents_per_iteration=2,
            max_iterations=10,
            random_seed=42,
            snapshot_interval=2,
            early_stopping_patience=patience,
            early_stopping_threshold=0.01,
        )

        result = run_single_experiment(
            name=f"exp6_patience_{patience}",
            group_name="clustering_ensemble",
            config=config,
            output_subdir=f"{output_dir}/exp6_patience_{patience}",
            quick_mode=quick_mode,
            llm_client=llm_client,
            mutator_type=mutator_type,
        )
        results.append(result)

    return results


def run_all_experiments(
    output_dir: str = "experiment_results", quick_mode: bool = False
) -> ExperimentSuite:
    """Run all experiments and return consolidated results."""
    suite = ExperimentSuite(output_dir=output_dir)

    llm_client = get_llm_client()
    mutator_type = "research"  # Always use research mutator for now

    logger.info("Using research-based mutations")

    logger.info("=" * 60)
    logger.info("Starting Darwinian Evolover Experiment Suite")
    logger.info("=" * 60)

    exp1_result = run_experiment_1_baseline(
        output_dir, quick_mode, llm_client, mutator_type
    )
    suite.add_result(exp1_result)
    logger.info(f"Experiment 1 complete: {exp1_result.best_fitness:.4f}")

    exp2_results = run_experiment_2_population_size(
        output_dir, quick_mode, llm_client, mutator_type
    )
    for r in exp2_results:
        suite.add_result(r)
        logger.info(f"  - {r.name}: {r.best_fitness:.4f}")

    exp3_results = run_experiment_3_fitness_weights(
        output_dir, quick_mode, llm_client, mutator_type
    )
    for r in exp3_results:
        suite.add_result(r)
        logger.info(f"  - {r.name}: {r.best_fitness:.4f}")

    exp4_results = run_experiment_4_learning_log_strategy(
        output_dir, quick_mode, llm_client, mutator_type
    )
    for r in exp4_results:
        suite.add_result(r)
        logger.info(f"  - {r.name}: {r.best_fitness:.4f}")

    exp5_results = run_experiment_5_cross_group_transfer(
        output_dir, quick_mode, llm_client, mutator_type
    )
    for r in exp5_results:
        suite.add_result(r)
        logger.info(f"  - {r.name}: {r.best_fitness:.4f}")

    exp6_results = run_experiment_6_early_stopping(
        output_dir, quick_mode, llm_client, mutator_type
    )
    for r in exp6_results:
        suite.add_result(r)
        logger.info(
            f"  - {r.name}: {r.best_fitness:.4f} ({r.iterations_completed} iterations)"
        )

    summary_file = suite.save_summary()
    logger.info(f"Experiment suite complete. Summary saved to: {summary_file}")

    return suite


def main():
    """Main entry point for running experiments."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    suite = run_all_experiments(quick_mode=True)

    print("\n" + "=" * 60)
    print("EXPERIMENT SUMMARY")
    print("=" * 60)
    for result in suite.results:
        status = "OK" if result.error is None else "FAILED"
        print(
            f"{result.name}: fitness={result.best_fitness:.4f}, iter={result.iterations_completed}, status={status}"
        )
    print("=" * 60)


if __name__ == "__main__":
    main()
