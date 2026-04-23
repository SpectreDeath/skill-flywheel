from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .genome import SkillGenome, create_initial_genome


@dataclass
class EvolableSkillGroup:
    """A group of skills that can be evolved together in the Darwinian evolver."""

    name: str
    description: str
    skills: List[str]
    default_parameters: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    test_cases: List[Dict[str, Any]] = field(default_factory=list)
    orchestration_modes: List[str] = field(
        default_factory=lambda: ["sequential", "parallel", "hierarchical"]
    )


EVOLVABLE_SKILL_GROUPS: Dict[str, EvolableSkillGroup] = {
    "clustering_ensemble": EvolableSkillGroup(
        name="clustering_ensemble",
        description="Ensemble of clustering algorithms for unsupervised learning tasks",
        skills=[
            "kmeans_clustering",
            "gmm_clustering",
            "hierarchical_clustering",
            "dbscan_clustering",
            "cluster_validation_analyzer",
        ],
        default_parameters={
            "kmeans_clustering": {"n_clusters": 5, "max_iter": 300, "n_init": 10},
            "gmm_clustering": {
                "n_components": 5,
                "covariance_type": "full",
                "max_iter": 100,
            },
            "hierarchical_clustering": {"n_clusters": 5, "linkage": "ward"},
            "dbscan_clustering": {"eps": 0.5, "min_samples": 5},
            "cluster_validation_analyzer": {
                "metrics": ["silhouette", "davies_bouldin"]
            },
        },
        test_cases=[
            {
                "name": "synthetic_data_classification",
                "input": {
                    "data": "synthetic_2d_points",
                    "num_samples": 1000,
                    "num_features": 2,
                    "true_clusters": 5,
                },
                "expected": {
                    "min_accuracy": 0.7,
                    "metrics": ["silhouette", "calinski_harabasz"],
                },
            },
            {
                "name": "pattern_discovery",
                "input": {"data": "anomaly_detection_dataset", "detect_outliers": True},
                "expected": {"min_accuracy": 0.65},
            },
            {
                "name": "high_dimensional_clustering",
                "input": {"data": "high_dim_feature_vectors", "num_features": 50},
                "expected": {"min_accuracy": 0.6},
            },
        ],
        orchestration_modes=["sequential", "parallel", "hierarchical"],
    ),
    "game_theory_solver": EvolableSkillGroup(
        name="game_theory_solver",
        description="Game theory analysis and equilibrium finding skills",
        skills=[
            "coordination_game_solver",
            "game_theory_negotiator",
            "prisoners_dilemma_analyzer",
        ],
        default_parameters={
            "coordination_game_solver": {
                "equilibrium_type": "nash",
                "max_iterations": 100,
            },
            "game_theory_negotiator": {
                "strategy": "rational",
                "discount_factor": 0.95,
            },
            "prisoners_dilemma_analyzer": {
                "iterations": 10,
                "strategy_profiles": "all",
            },
        },
        test_cases=[
            {
                "name": "two_player_coordination",
                "input": {"game_matrix": "coordination_game", "players": 2},
                "expected": {"equilibrium_found": True, "payoff_min": 1.0},
            },
            {
                "name": "multi_player_negotiation",
                "input": {"players": 4, "resource_pool": 100, "rounds": 10},
                "expected": {"convergence": True, "fairness_score": 0.7},
            },
            {
                "name": "iterated_prisoners_dilemma",
                "input": {
                    "rounds": 20,
                    "player_strategies": ["tit_for_tat", "defect_always"],
                },
                "expected": {"cooperation_emerges": True},
            },
        ],
        orchestration_modes=["sequential", "hierarchical"],
    ),
    "specification_engineering_pipeline": EvolableSkillGroup(
        name="specification_engineering_pipeline",
        description="Specification validation, evolution, and regression monitoring",
        skills=[
            "spec_guardrail_enforcement",
            "spec_evolution_engine",
            "spec_regression_monitoring",
        ],
        default_parameters={
            "spec_guardrail_enforcement": {
                "strict_mode": True,
                "validation_rules": ["type_check", "range_check"],
            },
            "spec_evolution_engine": {"auto_evolve": True, "max_changes": 10},
            "spec_regression_monitoring": {
                "thresholds": {"accuracy": 0.95, "latency": 1.5}
            },
        },
        test_cases=[
            {
                "name": "spec_validation",
                "input": {"spec_document": "api_spec_v1", "validate_schema": True},
                "expected": {"valid": True, "violations": 0},
            },
            {
                "name": "spec_evolution",
                "input": {"old_spec": "v1", "new_requirements": ["field_add"]},
                "expected": {"backward_compatible": True},
            },
            {
                "name": "regression_detection",
                "input": {
                    "baseline_metrics": "v1_metrics",
                    "current_metrics": "v2_metrics",
                },
                "expected": {"regressions_detected": 0},
            },
        ],
        orchestration_modes=["sequential", "hierarchical"],
    ),
    "model_orchestration_ensemble": EvolableSkillGroup(
        name="model_orchestration_ensemble",
        description="Multi-model routing, fusion, and ensemble orchestration",
        skills=[
            "model_ensemble_orchestrator",
            "multi_model_fusion_engine",
            "dynamic_model_router",
        ],
        default_parameters={
            "model_ensemble_orchestrator": {
                "ensemble_method": "voting",
                "weight_strategy": "performance_based",
            },
            "multi_model_fusion_engine": {
                "fusion_type": "weighted_sum",
                "temperature": 1.0,
            },
            "dynamic_model_router": {
                "routing_strategy": "performance_based",
                "cache_enabled": True,
            },
        },
        test_cases=[
            {
                "name": "multi_model_inference",
                "input": {
                    "models": ["gpt4", "claude", "gemini"],
                    "prompt": "complex_reasoning_task",
                },
                "expected": {"consensus_score": 0.7, "latency_ms": 5000},
            },
            {
                "name": "model_fusion",
                "input": {
                    "model_outputs": ["list_of_logits"],
                    "fusion_method": "weighted",
                },
                "expected": {"improvement_over_single": 0.1},
            },
            {
                "name": "dynamic_routing",
                "input": {"request": "diverse_queries", "model_pool": 5},
                "expected": {"avg_latency_reduction": 0.2},
            },
        ],
        orchestration_modes=["parallel", "hierarchical"],
    ),
    "data_pipeline_optimizer": EvolableSkillGroup(
        name="data_pipeline_optimizer",
        description="Data processing pipeline management, quality checking, and stream processing",
        skills=[
            "data_pipeline_manager",
            "data_quality_checker",
            "stream_processing_engine",
        ],
        default_parameters={
            "data_pipeline_manager": {
                "pipeline_type": "etl",
                "parallel_stages": True,
            },
            "data_quality_checker": {
                "checks": ["null_check", "duplicate_check", "range_check"],
                "threshold": 0.95,
            },
            "stream_processing_engine": {
                "window_size": 100,
                "buffer_size": 1000,
            },
        },
        test_cases=[
            {
                "name": "etl_pipeline",
                "input": {
                    "source": "csv_file",
                    "transforms": ["normalize", "aggregate"],
                },
                "expected": {"records_processed": 1000, "error_rate": 0.01},
            },
            {
                "name": "data_quality",
                "input": {
                    "dataset": "customer_data",
                    "rules": ["completeness", "validity"],
                },
                "expected": {"quality_score": 0.9},
            },
            {
                "name": "stream_processing",
                "input": {"stream_source": "sensor_data", "window_sec": 60},
                "expected": {"throughput_mb_s": 10, "latency_ms": 100},
            },
        ],
        orchestration_modes=["sequential", "parallel"],
    ),
    "database_optimizer": EvolableSkillGroup(
        name="database_optimizer",
        description="Query optimization, index strategy, and database sharding",
        skills=[
            "query_optimizer",
            "index_strategy_optimization",
            "database_sharding_plan",
        ],
        default_parameters={
            "query_optimizer": {
                "optimization_level": 2,
                "use_hints": True,
            },
            "index_strategy_optimization": {
                "index_types": ["btree", "hash"],
                "auto_create": True,
            },
            "database_sharding_plan": {
                "sharding_key": "user_id",
                "num_shards": 4,
            },
        },
        test_cases=[
            {
                "name": "query_optimization",
                "input": {"query": "complex_join_query", "explain": True},
                "expected": {"execution_time_ms": 100, "uses_index": True},
            },
            {
                "name": "index_strategy",
                "input": {
                    "table": "transactions",
                    "query_patterns": ["range", "equality"],
                },
                "expected": {"index_hit_ratio": 0.95},
            },
            {
                "name": "sharding_plan",
                "input": {"table_size_gb": 100, "sharding_key": "user_id"},
                "expected": {"balanced_distribution": True, "cross_shard_joins": 0},
            },
        ],
        orchestration_modes=["sequential", "hierarchical"],
    ),
}


def get_evolvable_group(name: str) -> EvolableSkillGroup | None:
    """Returns a skill group by name, or None if not found."""
    return EVOLVABLE_SKILL_GROUPS.get(name)


def list_evolvable_groups() -> List[str]:
    """Returns all available evolvable group names."""
    return list(EVOLVABLE_SKILL_GROUPS.keys())


def create_genome_for_group(
    group_name: str,
    orchestration_strategy: str | None = None,
    custom_parameters: Dict[str, Dict[str, Any]] | None = None,
) -> SkillGenome | None:
    """
    Creates an initial SkillGenome for a given evolvable group.

    Args:
        group_name: Name of the evolvable skill group
        orchestration_strategy: Override the default orchestration strategy
        custom_parameters: Override or extend the default parameters

    Returns:
        A SkillGenome instance, or None if the group doesn't exist
    """

if __name__ == "__main__":
    group = get_evolvable_group(group_name)
        if group is None:
            return None

        strategy = orchestration_strategy or group.orchestration_modes[0]

        parameters = group.default_parameters.copy()
        if custom_parameters:
            parameters.update(custom_parameters)

        return create_initial_genome(
            skill_selections=group.skills,
            default_parameters=parameters,
            orchestration_strategy=strategy,
        )