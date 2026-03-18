from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from typing import Any, Dict, Optional

from .config import EvolutionConfig
from .evolvable_skill_groups import list_evolvable_groups
from .runner import run_evolution

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def load_config_from_file(config_path: str) -> EvolutionConfig:
    """Load evolution configuration from a JSON file."""
    with open(config_path, "r") as f:
        data = json.load(f)
    return EvolutionConfig.from_dict(data)


def save_results(results: Dict[str, Any], output_dir: str) -> None:
    """Save evolution results to the output directory."""
    os.makedirs(output_dir, exist_ok=True)

    best_genome = results.get("best_genome")
    if best_genome:
        genome_path = os.path.join(output_dir, "best_genome.json")
        with open(genome_path, "w") as f:
            json.dump(best_genome.to_dict(), f, indent=2)
        logger.info(f"Best genome saved to {genome_path}")

    stats = results.get("statistics", {})
    stats_path = os.path.join(output_dir, "statistics.json")
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    logger.info(f"Statistics saved to {stats_path}")

    iteration_results = results.get("results", [])
    if iteration_results:
        results_path = os.path.join(output_dir, "iteration_results.json")
        with open(results_path, "w") as f:
            json.dump(iteration_results, f, indent=2)
        logger.info(f"Iteration results saved to {results_path}")

    best_fitness = results.get("best_fitness")
    if best_fitness:
        fitness_path = os.path.join(output_dir, "best_fitness.json")
        with open(fitness_path, "w") as f:
            json.dump(best_fitness.to_dict(), f, indent=2)
        logger.info(f"Best fitness saved to {fitness_path}")


def print_progress(iteration: int, stats: Dict[str, Any]) -> None:
    """Print evolution progress."""
    best_score = stats.get("best_score", "N/A")
    avg_score = stats.get("average_score", "N/A")
    pop_size = stats.get("population_size", "N/A")

    print(
        f"Iteration {iteration}: "
        f"best={best_score}, avg={avg_score}, pop_size={pop_size}"
    )


def build_parser() -> argparse.ArgumentParser:
    """Build and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="skill-evolution",
        description="CLI for running skill evolution",
    )

    parser.add_argument(
        "group",
        nargs="?",
        help="Evolvable skill group to evolve",
    )

    parser.add_argument(
        "--iterations",
        "-i",
        type=int,
        default=10,
        help="Number of evolution iterations (default: 10)",
    )

    parser.add_argument(
        "--population-size",
        "-p",
        type=int,
        default=5,
        help="Population size (default: 5)",
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="evolution_output",
        help="Output directory for results (default: evolution_output)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    parser.add_argument(
        "--config",
        "-c",
        type=str,
        help="Path to evolution config JSON file",
    )

    parser.add_argument(
        "--list-groups",
        action="store_true",
        help="List all available skill groups and exit",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show configuration without running evolution",
    )

    return parser


class EvolutionCLI:
    """CLI interface for running skill evolution."""

    def __init__(self, args: Optional[list] = None):
        """Initialize the CLI with arguments.

        Args:
            args: Command line arguments (uses sys.argv if None)
        """
        self.parser = build_parser()
        self.args = self.parser.parse_args(args)
        self.config: Optional[EvolutionConfig] = None
        self.output_dir: str = "evolution_output"

    def run(self) -> int:
        """Execute the CLI command.

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        setup_logging(self.args.verbose)

        if self.args.list_groups:
            return self._list_groups()

        if not self.args.group:
            self.parser.error("group argument is required (or use --list-groups)")

        self._load_config()

        if self.args.dry_run:
            return self._dry_run()

        return self._run_evolution()

    def _list_groups(self) -> int:
        """List all available skill groups."""
        groups = list_evolvable_groups()
        print("Available evolvable skill groups:")
        for group in groups:
            print(f"  - {group}")
        return 0

    def _load_config(self) -> None:
        """Load or create evolution configuration."""
        if self.args.config:
            try:
                self.config = load_config_from_file(self.args.config)
                logger.info(f"Loaded configuration from {self.args.config}")
            except FileNotFoundError:
                logger.error(f"Config file not found: {self.args.config}")
                sys.exit(1)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in config file: {e}")
                sys.exit(1)
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                sys.exit(1)
        else:
            pop_size = self.args.population_size
            parents = min(3, pop_size - 1)  # Ensure parents < population_size
            self.config = EvolutionConfig(
                population_size=pop_size,
                num_parents_per_iteration=parents,
                max_iterations=self.args.iterations,
            )

        self.output_dir = self.args.output_dir

    def _dry_run(self) -> int:
        """Show configuration without running evolution."""
        print("=" * 60)
        print("Skill Evolution - Dry Run")
        print("=" * 60)
        print(f"Group: {self.args.group}")
        print(f"Iterations: {self.args.iterations}")
        print(f"Population Size: {self.args.population_size}")
        print(f"Output Directory: {self.output_dir}")
        print(f"Config File: {self.args.config or 'default'}")
        print()
        print("Configuration:")
        if self.config:
            for key, value in self.config.to_dict().items():
                print(f"  {key}: {value}")
        print("=" * 60)
        return 0

    def _run_evolution(self) -> int:
        """Run the skill evolution."""
        print("=" * 60)
        print(f"Starting Skill Evolution")
        print(f"Group: {self.args.group}")
        print(f"Iterations: {self.args.iterations}")
        print(f"Population Size: {self.args.population_size}")
        print(f"Output Directory: {self.output_dir}")
        print("=" * 60)
        print()

        groups = list_evolvable_groups()
        if self.args.group not in groups:
            logger.error(f"Unknown skill group: {self.args.group}")
            logger.error(f"Available groups: {', '.join(groups)}")
            return 1

        try:
            results = run_evolution(
                group_name=self.args.group,
                iterations=self.args.iterations,
                config=self.config,
                output_dir=self.output_dir,
            )

            print()
            print("=" * 60)
            print("Evolution Complete")
            print("=" * 60)

            stats = results.get("statistics", {})
            print(f"Iterations completed: {stats.get('iterations_completed', 0)}")
            print(f"Best score: {stats.get('best_score', 'N/A')}")
            print(f"Average score: {stats.get('average_score', 'N/A')}")
            print(f"Worst score: {stats.get('worst_score', 'N/A')}")

            save_results(results, self.output_dir)
            print()
            print(f"Results saved to: {self.output_dir}")

            return 0

        except Exception as e:
            logger.error(f"Evolution failed: {e}", exc_info=self.args.verbose)
            return 1


def main(args: Optional[list] = None) -> int:
    """Main entry point for the CLI.

    Args:
        args: Command line arguments (uses sys.argv if None)

    Returns:
        Exit code
    """
    cli = EvolutionCLI(args)
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
