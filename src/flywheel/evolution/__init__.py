"""
Skill Flywheel Evolution Module

This module provides Darwinian evolution capabilities for optimizing skill
configurations in the Skill Flywheel system.
"""

if __name__ == "__main__":
    from .cli import EvolutionCLI
    from .cli import main as cli_main
    from .config import EvolutionConfig
    from .evaluator import MockSkillExecutor, SkillExecutor, SkillFitnessEvaluator
    from .evolvable_skill_groups import (
        EVOLVABLE_SKILL_GROUPS,
        EvolableSkillGroup,
        create_genome_for_group,
        get_evolvable_group,
        list_evolvable_groups,
    )
    from .evolver import SkillEvolver, create_skill_evolver
    from .genome import (
        SkillFailureCase,
        SkillFitnessResult,
        SkillGenome,
        create_initial_genome,
    )
    from .mutator import LLMMutator, ParameterTuningMutator, StructureMutationMutator
    from .population import EvolutionStatistics, SkillPopulation
    from .runner import (
        SkillEvolutionRunner,
        create_runner,
        run_evolution,
    )
    from .skill_executor import (
        ExecutionResult,
        RealSkillExecutor,
        SkillExecutionError,
        SkillLoader,
        SkillMetadata,
        SkillNotFoundError,
        create_real_executor,
    )

    __all__ = [
        # Config
        "EvolutionConfig",
        # Genome
        "SkillGenome",
        "SkillFailureCase",
        "SkillFitnessResult",
        "create_initial_genome",
        # Evaluator
        "SkillExecutor",
        "MockSkillExecutor",
        "SkillFitnessEvaluator",
        # Mutators
        "LLMMutator",
        "ParameterTuningMutator",
        "StructureMutationMutator",
        # Population
        "SkillPopulation",
        "EvolutionStatistics",
        # Evolver
        "SkillEvolver",
        "create_skill_evolver",
        # Evolable Skill Groups
        "EvolableSkillGroup",
        "EVOLVABLE_SKILL_GROUPS",
        "get_evolvable_group",
        "list_evolvable_groups",
        "create_genome_for_group",
        # Runner
        "SkillEvolutionRunner",
        "create_runner",
        "run_evolution",
        # Skill Executor
        "RealSkillExecutor",
        "SkillLoader",
        "create_real_executor",
        "SkillExecutionError",
        "SkillNotFoundError",
        "ExecutionResult",
        "SkillMetadata",
        # CLI
        "EvolutionCLI",
        "cli_main",
    ]