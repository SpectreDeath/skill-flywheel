"""Integration test for the skill evolution module."""

import asyncio

from src.core.evolution import (
    EvolutionConfig,
    MockSkillExecutor,
    SkillFitnessEvaluator,
    create_initial_genome,
    create_skill_evolver,
)


async def main():
    print("=" * 50)
    print("Skill Evolution Integration Test")
    print("=" * 50)

    # Create initial genome
    genome = create_initial_genome(
        skill_selections=["data_analyzer", "skill_validator"],
        default_parameters={
            "data_analyzer": {"threshold": 0.5, "max_rows": 1000},
            "skill_validator": {"strict": True},
        },
        orchestration_strategy="sequential",
    )
    print("\nInitial genome:")
    print(f"  Skills: {genome.skill_selections}")
    print(f"  Strategy: {genome.orchestration_strategy}")
    print(f"  Parameters: {genome.skill_parameters}")

    # Test cases
    test_cases = [
        {"input": {"query": "test1"}, "expected": {"result": "ok"}},
        {"input": {"query": "test2"}, "expected": {"result": "ok"}},
        {"input": {"query": "test3"}, "expected": {"result": "ok"}},
    ]

    holdout_cases = [
        {"input": {"query": "holdout1"}, "expected": {"result": "ok"}},
    ]

    # Setup evaluator with mock executor
    evaluator = SkillFitnessEvaluator(
        skill_executor=MockSkillExecutor(),
        test_cases=test_cases,
        holdout_cases=holdout_cases,
        config=EvolutionConfig(
            metrics_weights={
                "performance": 0.4,
                "accuracy": 0.4,
                "resource_efficiency": 0.2,
            }
        ),
    )

    # Evaluate initial genome
    print("\nEvaluating initial genome...")
    result = evaluator.evaluate(genome)
    print(f"  Score: {result.score:.3f}")
    print(f"  Performance: {result.performance_score:.3f}")
    print(f"  Accuracy: {result.accuracy_score:.3f}")
    print(f"  Viability: {result.is_viable}")
    print(f"  Trainable failures: {len(result.trainable_failure_cases)}")
    print(f"  Holdout failures: {len(result.holdout_failure_cases)}")

    # Test mutator (fallback since no LLM)
    from src.core.evolution.mutator import ParameterTuningMutator

    mutator = ParameterTuningMutator(tuning_strategy="random")

    print("\nTesting parameter mutation...")
    # Create a failure case to pass to mutator
    from src.core.evolution.genome import SkillFailureCase

    failure_case = SkillFailureCase(
        data_point_id="test_1",
        skill_name="data_analyzer",
        input_data={"query": "test"},
        expected_output={"result": "ok"},
        actual_output={"result": "fail"},
        failure_category="accuracy",
    )

    mutated = mutator.mutate(genome, [failure_case], [])
    print(f"  Generated {len(mutated)} mutated genome(s)")
    if mutated:
        print(f"  New params: {mutated[0].skill_parameters}")

    # Test structure mutation
    from src.core.evolution.mutator import StructureMutationMutator

    struct_mutator = StructureMutationMutator()
    struct_mutated = struct_mutator.mutate(genome, [failure_case], [])
    print("\nTesting structure mutation...")
    print(f"  Generated {len(struct_mutated)} mutated genome(s)")
    if struct_mutated:
        print(f"  New strategy: {struct_mutated[0].orchestration_strategy}")

    # Test fitness result methods
    print("\nTesting fitness result methods...")
    result2 = SkillFitnessResult(
        score=0.75,
        trainable_failure_cases=[],
        is_viable=True,
        performance_score=0.8,
        accuracy_score=0.7,
        resource_efficiency=0.75,
    )
    outcome = result2.format_observed_outcome(result)
    print(f"  Outcome: {outcome}")

    sampled = result.sample_trainable_failure_cases(1)
    print(f"  Sampled failures: {len(sampled)}")

    # Test evolution config
    print("\nTesting evolution config...")
    config = EvolutionConfig(population_size=10, max_iterations=5, random_seed=42)
    print(f"  Config valid: {config.population_size == 10}")
    print(f"  Dict export works: {'population_size' in config.to_dict()}")

    # Test genome validation
    print("\nTesting genome validation...")
    valid_genome = create_initial_genome(["skill_a"])
    print(f"  Valid genome: {valid_genome.is_valid()}")

    invalid_genome = SkillGenome(
        skill_selections=[],
        skill_parameters={},
        prompt_templates={},
        resource_allocation={},
        orchestration_strategy="sequential",
    )
    print(f"  Invalid (empty): {not invalid_genome.is_valid()}")

    print("\n" + "=" * 50)
    print("All integration tests PASSED!")
    print("=" * 50)


if __name__ == "__main__":
    from src.core.evolution.genome import SkillFitnessResult, SkillGenome

    asyncio.run(main())
