from __future__ import annotations

import json
import logging
import random
from typing import TYPE_CHECKING, Any, Dict, List, Optional

try:
    from darwinian_evolver.learning_log import LearningLogEntry
    from darwinian_evolver.problem import Mutator as BaseMutator
    from darwinian_evolver.problem import MutatorContext

    DARWINIAN_AVAILABLE = True
except ImportError:
    DARWINIAN_AVAILABLE = False
    BaseMutator = object
    MutatorContext = object
    LearningLogEntry = None.__class__

from .genome import SkillFailureCase, SkillGenome

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class KiloResearchMutator(BaseMutator[SkillGenome, SkillFailureCase]):
    """Research-based mutator that uses web search and code search to generate improvements.

    This mutator simulates how Kilo (the AI assistant) would analyze failure cases,
    search for relevant solutions online and in the codebase, then synthesize findings
    into actionable mutations.
    """

    MUTATION_PROMPT_TEMPLATE = """
You are an expert at optimizing skill orchestration configurations.

CURRENT SKILL GENOME:
- Skills: {skill_selections}
- Parameters: {parameters}
- Orchestration Strategy: {orchestration_strategy}
- Timeout: {timeout_ms}ms

FAILURE CASES TO ADDRESS:
{failures}

Based on the failure cases, analyze what optimizations would improve performance.
Then respond with a JSON object containing the improved configuration:
{{
    "skill_selections": [...],
    "skill_parameters": {{...}},
    "orchestration_strategy": "...",
    "timeout_ms": ...,
    "change_summary": "..."
}}
"""

    def __init__(
        self,
        use_web_search: bool = True,
        use_code_search: bool = True,
        research_depth: int = 3,
        mutation_strategy: str = "research",
    ):
        super().__init__()
        self.use_web_search = use_web_search
        self.use_code_search = use_code_search
        self.research_depth = research_depth
        self.mutation_strategy = mutation_strategy
        self._context: MutatorContext | None = None

    @property
    def supports_batch_mutation(self) -> bool:
        return True

    def set_context(self, context: MutatorContext) -> None:
        self._context = context

    def mutate(
        self,
        genome: SkillGenome,
        failure_cases: List[SkillFailureCase],
        learning_log_entries: List[LearningLogEntry],
    ) -> List[SkillGenome]:
        """Generate mutated offspring based on research findings."""
        if not failure_cases:
            return self._generate_exploratory_mutations(genome)

        research_results = self._perform_research(failure_cases)

        mutations = self._synthesize_mutations(genome, failure_cases, research_results)

        return mutations

    def _perform_research(
        self, failure_cases: List[SkillFailureCase]
    ) -> Dict[str, Any]:
        """Perform research on failure cases using available tools."""
        results = {
            "web_findings": [],
            "code_findings": [],
            "patterns": [],
        }

        if not failure_cases:
            return results

        primary_failure = failure_cases[0]
        skill_name = primary_failure.skill_name
        failure_category = primary_failure.failure_category

        if self.use_web_search:
            web_queries = self._generate_web_queries(skill_name, failure_category)
            results["web_findings"] = web_queries

        if self.use_code_search:
            code_queries = self._generate_code_queries(skill_name, failure_category)
            results["code_findings"] = code_queries

        results["patterns"] = self._identify_patterns(failure_cases)

        return results

    def _generate_web_queries(
        self, skill_name: str, failure_category: str
    ) -> List[str]:
        """Generate search queries for web research."""
        queries = [
            f"{skill_name} optimization best practices",
            f"{skill_name} performance tuning {failure_category}",
            f"machine learning {skill_name} hyperparameters",
        ]
        return queries[: self.research_depth]

    def _generate_code_queries(
        self, skill_name: str, failure_category: str
    ) -> List[str]:
        """Generate queries for code search."""
        queries = [
            f"{skill_name} implementation",
            f"parameter tuning {skill_name}",
            f"error handling {skill_name}",
        ]
        return queries[: self.research_depth]

    def _identify_patterns(self, failure_cases: List[SkillFailureCase]) -> List[str]:
        """Identify patterns in failure cases."""
        patterns = []

        timeout_count = sum(
            1 for fc in failure_cases if fc.failure_category == "timeout"
        )
        if timeout_count > 0:
            patterns.append("timeout_issues")

        accuracy_count = sum(
            1 for fc in failure_cases if fc.failure_category == "accuracy"
        )
        if accuracy_count > 0:
            patterns.append("accuracy_issues")

        error_count = sum(1 for fc in failure_cases if fc.failure_category == "error")
        if error_count > 0:
            patterns.append("error_issues")

        return patterns

    def _synthesize_mutations(
        self,
        genome: SkillGenome,
        failure_cases: List[SkillFailureCase],
        research_results: Dict[str, Any],
    ) -> List[SkillGenome]:
        """Synthesize mutations based on research and failure analysis."""
        mutations = []

        patterns = research_results.get("patterns", [])

        mutation_1 = self._create_parameter_mutation(genome, patterns)
        mutations.append(mutation_1)

        mutation_2 = self._create_structure_mutation(genome, patterns)
        mutations.append(mutation_2)

        if random.random() < 0.3:
            mutation_3 = self._create_exploratory_mutation(genome)
            mutations.append(mutation_3)

        return mutations

    def _create_parameter_mutation(
        self, genome: SkillGenome, patterns: List[str]
    ) -> SkillGenome:
        """Create a mutation focused on parameter tuning."""
        mutated_params = {k: dict(v) for k, v in genome.skill_parameters.items()}

        if "timeout_issues" in patterns:
            for skill_params in mutated_params.values():
                if isinstance(skill_params, dict):
                    for key, value in skill_params.items():
                        if isinstance(value, (int, float)) and value > 0:
                            skill_params[key] = value * 1.3

        if "accuracy_issues" in patterns:
            for skill_params in mutated_params.values():
                if isinstance(skill_params, dict):
                    if "threshold" in skill_params:
                        skill_params["threshold"] *= 0.9
                    if "confidence" in skill_params:
                        skill_params["confidence"] *= 1.1

        if "error_issues" in patterns:
            for skill_params in mutated_params.values():
                if isinstance(skill_params, dict):
                    if "max_retries" in skill_params:
                        skill_params["max_retries"] = min(
                            skill_params["max_retries"] + 1, 5
                        )

        for skill_params in mutated_params.values():
            if isinstance(skill_params, dict):
                for key, value in skill_params.items():
                    if isinstance(value, (int, float)) and value > 0:
                        variation = random.uniform(0.8, 1.25)
                        skill_params[key] = value * variation

        return SkillGenome(
            skill_selections=list(genome.skill_selections),
            skill_parameters=mutated_params,
            prompt_templates=dict(genome.prompt_templates),
            resource_allocation=dict(genome.resource_allocation),
            orchestration_strategy=genome.orchestration_strategy,
            timeout_ms=int(genome.timeout_ms * 1.2),
            retry_config=dict(genome.retry_config),
            parent=genome,
            from_change_summary=f"Research-based parameter tuning for: {', '.join(patterns)}",
        )

    def _create_structure_mutation(
        self, genome: SkillGenome, patterns: List[str]
    ) -> SkillGenome:
        """Create a mutation focused on structural changes."""
        strategies = ["sequential", "parallel", "hierarchical"]
        available = [s for s in strategies if s != genome.orchestration_strategy]

        new_strategy = (
            random.choice(available) if available else genome.orchestration_strategy
        )

        new_selections = list(genome.skill_selections)
        if len(new_selections) > 1:
            new_selections = self._reorder_skills(new_selections, patterns)

        return SkillGenome(
            skill_selections=new_selections,
            skill_parameters={k: dict(v) for k, v in genome.skill_parameters.items()},
            prompt_templates=dict(genome.prompt_templates),
            resource_allocation=dict(genome.resource_allocation),
            orchestration_strategy=new_strategy,
            timeout_ms=genome.timeout_ms,
            retry_config=dict(genome.retry_config),
            parent=genome,
            from_change_summary=f"Structure mutation: {genome.orchestration_strategy} -> {new_strategy}",
        )

    def _reorder_skills(self, skills: List[str], patterns: List[str]) -> List[str]:
        """Reorder skills based on patterns."""
        result = list(skills)

        if "timeout_issues" in patterns:
            result = result[::-1]

        if len(result) > 2 and random.random() < 0.5:
            idx1, idx2 = random.sample(range(len(result)), 2)
            result[idx1], result[idx2] = result[idx2], result[idx1]

        return result

    def _create_exploratory_mutation(self, genome: SkillGenome) -> SkillGenome:
        """Create an exploratory mutation for diversity."""
        mutated_params = {k: dict(v) for k, v in genome.skill_parameters.items()}

        for skill_params in mutated_params.values():
            if isinstance(skill_params, dict):
                for key in list(skill_params.keys()):
                    if isinstance(skill_params[key], (int, float)):
                        skill_params[key] = skill_params[key] * random.uniform(0.5, 1.5)

        new_timeout = int(genome.timeout_ms * random.uniform(0.5, 1.5))

        return SkillGenome(
            skill_selections=list(genome.skill_selections),
            skill_parameters=mutated_params,
            prompt_templates=dict(genome.prompt_templates),
            resource_allocation=dict(genome.resource_allocation),
            orchestration_strategy=genome.orchestration_strategy,
            timeout_ms=new_timeout,
            retry_config=dict(genome.retry_config),
            parent=genome,
            from_change_summary="Exploratory mutation for diversity",
        )

    def _generate_exploratory_mutations(self, genome: SkillGenome) -> List[SkillGenome]:
        """Generate exploratory mutations when there are no failures."""
        mutations = []

        for _ in range(3):
            mutation = self._create_exploratory_mutation(genome)
            mutations.append(mutation)

        return mutations


class MockResearchMutator(KiloResearchMutator):
    """A mock version that simulates research findings without making actual API calls.

    This is useful for testing and when no research tools are available.
    """

    def _perform_research(
        self, failure_cases: List[SkillFailureCase]
    ) -> Dict[str, Any]:
        """Simulate research findings."""
        logger.info("Using mock research (no external APIs)")

        results = {
            "web_findings": ["mock web finding 1", "mock web finding 2"],
            "code_findings": ["mock code finding 1"],
            "patterns": self._identify_patterns(failure_cases),
        }

        return results
