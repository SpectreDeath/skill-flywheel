from __future__ import annotations

from typing import Any, Dict, List
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, computed_field


class SkillFailureCase(BaseModel):
    """Failure case representing a skill execution that did not meet criteria."""

    model_config = ConfigDict(frozen=True)

    data_point_id: str = Field(description="Unique identifier for this failure case")
    skill_name: str = Field(description="Name of the skill that produced the failure")
    input_data: Dict[str, Any] = Field(
        default_factory=dict, description="Input data passed to the skill"
    )
    expected_output: Dict[str, Any] = Field(
        default_factory=dict, description="Expected output from skill execution"
    )
    actual_output: Dict[str, Any] = Field(
        default_factory=dict, description="Actual output from skill execution"
    )
    failure_category: str = Field(
        default="error",
        description="Category of failure: performance, accuracy, timeout, error",
    )
    execution_time_ms: float | None = Field(
        default=None, description="Time taken to execute the skill"
    )


class SkillFitnessResult(BaseModel):
    """Fitness evaluation result for a skill genome."""

    model_config = ConfigDict(frozen=True)

    score: float = Field(description="Overall fitness score")
    trainable_failure_cases: List[SkillFailureCase] = Field(
        default_factory=list,
        description="Failure cases that can be used to inform mutations",
    )
    holdout_failure_cases: List[SkillFailureCase] = Field(
        default_factory=list, description="Holdout failure cases not passed to mutators"
    )
    is_viable: bool = Field(
        default=True, description="Whether the organism is viable for reproduction"
    )
    performance_score: float = Field(
        default=0.0, description="Score based on execution performance metrics"
    )
    accuracy_score: float = Field(
        default=0.0, description="Score based on output accuracy"
    )
    resource_efficiency: float = Field(
        default=0.0, description="Score based on resource utilization"
    )
    execution_metrics: Dict[str, Any] = Field(
        default_factory=dict, description="Detailed execution metrics"
    )

    def sample_trainable_failure_cases(
        self, batch_size: int = 1
    ) -> List[SkillFailureCase]:
        """Sample failure cases for mutation."""
        if not self.trainable_failure_cases:
            return []
        return self.trainable_failure_cases[
            : min(batch_size, len(self.trainable_failure_cases))
        ]

    @property
    def failure_type_weights(self) -> Dict[str, float]:
        """Weights for sampling different failure types."""
        return {"performance": 2.0, "accuracy": 1.5, "timeout": 1.0, "error": 3.0}

    @property
    def failure_cases(self) -> List[SkillFailureCase]:
        """Get all failure cases."""
        return self.trainable_failure_cases + self.holdout_failure_cases

    def format_observed_outcome(
        self, parent_result: SkillFitnessResult | None = None, ndigits: int = 2
    ) -> str:
        """Format observed outcome with detailed metrics."""
        if not self.is_viable:
            return "Inconclusive - the resulting organism was not viable."

        rounded_score = round(self.score, ndigits)
        outcome = f"Overall fitness: {rounded_score} (perf: {self.performance_score:.2f}, acc: {self.accuracy_score:.2f}, res: {self.resource_efficiency:.2f})"

        if parent_result is not None:
            rounded_parent_score = round(parent_result.score, ndigits)
            if rounded_score > rounded_parent_score:
                outcome += f" Improved from {rounded_parent_score}."
            elif rounded_score < rounded_parent_score:
                outcome += f" Regressed from {rounded_parent_score}."
            else:
                outcome += f" Same as parent ({rounded_parent_score})."

        return outcome


class SkillGenome(BaseModel):
    """Genome representing a skill configuration to be evolved."""

    model_config = ConfigDict(frozen=False)

    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    parent: SkillGenome | None = Field(default=None, description="Parent genome")
    additional_parents: List[SkillGenome] = Field(default_factory=list)
    from_failure_cases: List[SkillFailureCase] | None = Field(default=None)
    from_learning_log_entries: List[Any] | None = Field(default=None)
    from_change_summary: str | None = Field(default=None)

    skill_selections: List[str] = Field(
        default_factory=list, description="Ordered list of skill names to use"
    )
    skill_parameters: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Per-skill configuration parameters"
    )
    prompt_templates: Dict[str, str] = Field(
        default_factory=dict, description="Prompt templates for each skill"
    )
    resource_allocation: Dict[str, float] = Field(
        default_factory=dict,
        description="Resource allocation weights per skill (CPU, memory)",
    )
    orchestration_strategy: str = Field(
        default="sequential",
        description="How skills are orchestrated: sequential, parallel, hierarchical",
    )
    timeout_ms: int = Field(
        default=30000, description="Maximum execution timeout in milliseconds"
    )
    retry_config: Dict[str, Any] = Field(
        default_factory=lambda: {"max_retries": 3, "backoff_ms": 100},
        description="Retry configuration for failed executions",
    )

    @computed_field
    @property
    def visualizer_props(self) -> Dict[str, Any]:
        """Properties for visualization."""
        return {
            "num_skills": len(self.skill_selections),
            "strategy": self.orchestration_strategy,
            "total_params": sum(len(p) for p in self.skill_parameters.values()),
            "timeout_ms": self.timeout_ms,
        }

    def get_skill_count(self) -> int:
        """Get the number of skills in this genome."""
        return len(self.skill_selections)

    def get_parameter_count(self) -> int:
        """Get total number of configured parameters."""
        return sum(len(params) for params in self.skill_parameters.values())

    def is_valid(self) -> bool:
        """Check if genome configuration is valid."""
        if not self.skill_selections:
            return False
        if self.orchestration_strategy not in [
            "sequential",
            "parallel",
            "hierarchical",
        ]:
            return False
        return not self.timeout_ms <= 0


def create_initial_genome(
    skill_selections: List[str],
    default_parameters: Dict[str, Dict[str, Any]] | None = None,
    orchestration_strategy: str = "sequential",
) -> SkillGenome:
    """Create an initial skill genome with sensible defaults."""

if __name__ == "__main__":
    default_params = default_parameters or {}

        return SkillGenome(
            skill_selections=skill_selections,
            skill_parameters=default_params,
            prompt_templates={},
            resource_allocation=dict.fromkeys(skill_selections, 1.0),
            orchestration_strategy=orchestration_strategy,
        )