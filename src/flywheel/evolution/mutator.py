from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any, Dict, List, TypeVar

try:
    from darwinian_evolver.learning_log import LearningLogEntry
    from darwinian_evolver.problem import Mutator as BaseMutator
    from darwinian_evolver.problem import MutatorContext

    DARWINIAN_AVAILABLE = True
except ImportError:
    DARWINIAN_AVAILABLE = False
    from typing import Protocol

    _G = TypeVar("_G")
    _F = TypeVar("_F")

    class BaseMutator(Protocol[_G, _F]):
        """Dummy mutator protocol for when darwinian-evolver is not installed."""

        pass

    class MutatorContext(Protocol):
        """Dummy mutator context for when darwinian-evolver is not installed."""

        pass

    class LearningLogEntry:
        """Dummy learning log entry for when darwinian-evolver is not installed."""

        pass


from .genome import SkillFailureCase, SkillGenome

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class LLMMutator(BaseMutator[SkillGenome, SkillFailureCase]):
    """Mutator that uses an LLM to generate improved skill configurations."""

    MUTATION_PROMPT_TEMPLATE = """
You are an expert at optimizing skill orchestration configurations.

CURRENT SKILL GENOME:
- Skills: {skill_selections}
- Parameters: {parameters}
- Prompt Templates: {prompt_templates}
- Resource Allocation: {resource_allocation}
- Orchestration Strategy: {orchestration_strategy}
- Timeout: {timeout_ms}ms

FAILURE CASES TO ADDRESS:
{failures}

LEARNING LOG (previous attempts):
{learning_log}

Based on the failure cases above, suggest an improved skill genome configuration.
Consider:
1. Which skills to add/remove/reorder
2. How to adjust parameters for better performance
3. Whether to change the orchestration strategy
4. How to optimize resource allocation
5. Whether prompt templates need adjustment

Respond with a JSON object containing the improved configuration:
{{
    "skill_selections": [...],
    "skill_parameters": {{...}},
    "prompt_templates": {{...}},
    "resource_allocation": {{...}},
    "orchestration_strategy": "...",
    "timeout_ms": ...,
    "change_summary": "..."
}}
"""

    def __init__(self, llm_client: Any = None, mutation_strategy: str = "default"):
        super().__init__()
        self.llm_client = llm_client
        self.mutation_strategy = mutation_strategy
        self._context: MutatorContext | None = None

    @property
    def supports_batch_mutation(self) -> bool:
        """Whether this mutator supports batch mutation."""
        return True

    def mutate(
        self,
        genome: SkillGenome,
        failure_cases: List[SkillFailureCase],
        learning_log_entries: List[LearningLogEntry],
    ) -> List[SkillGenome]:
        """Generate mutated offspring based on failure cases."""
        if not self.llm_client:
            logger.warning("No LLM client configured, using fallback mutation")
            return self._fallback_mutate(genome, failure_cases)

        try:
            return self._llm_mutate(genome, failure_cases, learning_log_entries)
        except Exception as e:
            logger.error(f"LLM mutation failed: {e}")
            return self._fallback_mutate(genome, failure_cases)

    def _llm_mutate(
        self,
        genome: SkillGenome,
        failure_cases: List[SkillFailureCase],
        learning_log_entries: List[LearningLogEntry],
    ) -> List[SkillGenome]:
        """Use LLM to generate mutations."""
        prompt = self._build_mutation_prompt(
            genome, failure_cases, learning_log_entries
        )

        response = self._call_llm(prompt)

        try:
            parsed = json.loads(response)
            mutated = self._parse_llm_response(genome, parsed)
            return [mutated] if mutated else []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return []

    def _build_mutation_prompt(
        self,
        genome: SkillGenome,
        failure_cases: List[SkillFailureCase],
        learning_log_entries: List[LearningLogEntry],
    ) -> str:
        """Build the mutation prompt for the LLM."""
        failures_text = ""
        for i, fc in enumerate(failure_cases):
            failures_text += f"""
Failure {i + 1}:
- Skill: {fc.skill_name}
- Category: {fc.failure_category}
- Input: {fc.input_data}
- Expected: {fc.expected_output}
- Actual: {fc.actual_output}
- Execution time: {fc.execution_time_ms}ms
"""

        learning_log_text = ""
        for entry in learning_log_entries[-5:]:
            learning_log_text += (
                f"- {entry.attempted_change}: {entry.observed_outcome}\n"
            )

        return self.MUTATION_PROMPT_TEMPLATE.format(
            skill_selections=genome.skill_selections,
            parameters=json.dumps(genome.skill_parameters, indent=2),
            prompt_templates=json.dumps(genome.prompt_templates, indent=2),
            resource_allocation=json.dumps(genome.resource_allocation, indent=2),
            orchestration_strategy=genome.orchestration_strategy,
            timeout_ms=genome.timeout_ms,
            failures=failures_text or "No specific failures provided.",
            learning_log=learning_log_text or "No previous attempts.",
        )

    def _call_llm(self, prompt: str) -> str:
        """Call the LLM with the mutation prompt."""
        if hasattr(self.llm_client, "generate"):
            return self.llm_client.generate(prompt)
        elif hasattr(self.llm_client, "complete"):
            return self.llm_client.complete(prompt)
        else:
            raise ValueError("LLM client must have 'generate' or 'complete' method")

    def _parse_llm_response(
        self, parent: SkillGenome, response: Dict[str, Any]
    ) -> SkillGenome | None:
        """Parse LLM response into a new genome."""
        try:
            mutated = SkillGenome(
                skill_selections=response.get(
                    "skill_selections", parent.skill_selections
                ),
                skill_parameters=response.get(
                    "skill_parameters", parent.skill_parameters
                ),
                prompt_templates=response.get(
                    "prompt_templates", parent.prompt_templates
                ),
                resource_allocation=response.get(
                    "resource_allocation", parent.resource_allocation
                ),
                orchestration_strategy=response.get(
                    "orchestration_strategy", parent.orchestration_strategy
                ),
                timeout_ms=response.get("timeout_ms", parent.timeout_ms),
                retry_config=response.get("retry_config", parent.retry_config),
                parent=parent,
                from_change_summary=response.get(
                    "change_summary", "LLM-guided mutation"
                ),
            )
            return mutated
        except Exception as e:
            logger.error(f"Failed to create mutated genome: {e}")
            return None

    def _fallback_mutate(
        self, genome: SkillGenome, failure_cases: List[SkillFailureCase]
    ) -> List[SkillGenome]:
        """Fallback mutation when LLM is unavailable."""
        mutated_params = dict(genome.skill_parameters)
        failed_skills = {fc.skill_name for fc in failure_cases}

        for skill in failed_skills:
            if skill in mutated_params:
                current = mutated_params[skill]
                if isinstance(current, dict):
                    for key in current:
                        if isinstance(current[key], (int, float)):
                            current[key] = current[key] * 1.2

        mutated = SkillGenome(
            skill_selections=genome.skill_selections,
            skill_parameters=mutated_params,
            prompt_templates=dict(genome.prompt_templates),
            resource_allocation=dict(genome.resource_allocation),
            orchestration_strategy=genome.orchestration_strategy,
            timeout_ms=int(genome.timeout_ms * 1.2),
            retry_config=dict(genome.retry_config),
            parent=genome,
            from_change_summary="Fallback parameter adjustment",
        )

        return [mutated]


class ParameterTuningMutator(BaseMutator[SkillGenome, SkillFailureCase]):
    """Mutator that performs parameter tuning without LLM."""

    def __init__(self, tuning_strategy: str = "random"):
        super().__init__()
        self.tuning_strategy = tuning_strategy

    @property
    def supports_batch_mutation(self) -> bool:
        return False

    def mutate(
        self,
        genome: SkillGenome,
        failure_cases: List[SkillFailureCase],
        learning_log_entries: List[LearningLogEntry],
    ) -> List[SkillGenome]:
        """Mutate by tuning parameters based on failure patterns."""
        if not failure_cases:
            return []

        import random

        mutated_params = {k: dict(v) for k, v in genome.skill_parameters.items()}

        affected_skills = {fc.skill_name for fc in failure_cases}

        for skill in affected_skills:
            if skill not in mutated_params:
                mutated_params[skill] = {}

            params = mutated_params[skill]

            if self.tuning_strategy == "random":
                for key in list(params.keys()):
                    if isinstance(params[key], (int, float)):
                        params[key] *= random.uniform(0.8, 1.25)
            elif self.tuning_strategy == "increase":
                for key in list(params.keys()):
                    if isinstance(params[key], (int, float)):
                        params[key] = params[key] * 1.1

        change_summary = f"Parameter tuning ({self.tuning_strategy}) for: {', '.join(affected_skills)}"

        mutated = SkillGenome(
            skill_selections=genome.skill_selections,
            skill_parameters=mutated_params,
            prompt_templates=dict(genome.prompt_templates),
            resource_allocation=dict(genome.resource_allocation),
            orchestration_strategy=genome.orchestration_strategy,
            timeout_ms=genome.timeout_ms,
            retry_config=dict(genome.retry_config),
            parent=genome,
            from_change_summary=change_summary,
        )

        return [mutated]


class StructureMutationMutator(BaseMutator[SkillGenome, SkillFailureCase]):
    """Mutator that changes the structure of skill orchestration."""

    STRATEGIES = ["sequential", "parallel", "hierarchical"]

    def __init__(self):
        super().__init__()

    @property
    def supports_batch_mutation(self) -> bool:
        return False

    def mutate(
        self,
        genome: SkillGenome,
        failure_cases: List[SkillFailureCase],
        learning_log_entries: List[LearningLogEntry],
    ) -> List[SkillGenome]:
        """Mutate by changing orchestration structure or skill ordering."""
        import random

        available_strategies = [
            s for s in self.STRATEGIES if s != genome.orchestration_strategy
        ]
        new_strategy = random.choice(available_strategies)

        new_selections = list(genome.skill_selections)
        if len(new_selections) > 1:
            random.shuffle(new_selections)

        mutated = SkillGenome(
            skill_selections=new_selections,
            skill_parameters=dict(genome.skill_parameters),
            prompt_templates=dict(genome.prompt_templates),
            resource_allocation=dict(genome.resource_allocation),
            orchestration_strategy=new_strategy,
            timeout_ms=genome.timeout_ms,
            retry_config=dict(genome.retry_config),
            parent=genome,
            from_change_summary=f"Structure change: {genome.orchestration_strategy} -> {new_strategy}",
        )

        return [mutated]
