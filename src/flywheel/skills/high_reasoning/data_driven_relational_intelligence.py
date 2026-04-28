#!/usr/bin/env python3
"""
Data-Driven Relational Intelligence with Datalog + Python Surfaces

Uses Datalog for modeling complex relational knowledge bases and Python
for data processing, analytics, and machine learning integration.

This skill demonstrates how relational database-like reasoning (Datalog)
can be combined with Python's rich data science ecosystem for intelligent
data-driven decision making.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Surface definitions
_base_path = Path(__file__).parent

# Datalog surface for relational knowledge modeling
DATALOG_SURFACE = (_base_path / "relational_intelligence.dl").read_text()


def data_driven_relational_intelligence(dataset: Dict[str, Any], query_type: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Perform data-driven relational intelligence analysis.

    Args:
        dataset: Input data with entities and relationships
        query_type: Type of analysis ('clustering', 'pattern_discovery', 'anomaly_detection', 'prediction')
        parameters: Analysis parameters

    Returns:
        Relational intelligence analysis results
    """
    parameters = parameters or {}

    # Python surface: Data preprocessing and analysis
    processed_data = _python_data_processing(dataset, parameters)

    # Datalog surface: Relational knowledge modeling
    relational_model = _datalog_knowledge_modeling(processed_data, query_type)

    # Combined analysis
    integrated_analysis = _integrate_relational_intelligence(
        processed_data, relational_model, query_type, parameters
    )

    return {
        "dataset_info": {
            "entities": len(processed_data.get("entities", [])),
            "relationships": len(processed_data.get("relationships", [])),
            "features": len(processed_data.get("features", []))
        },
        "query_type": query_type,
        "parameters": parameters,
        "data_processing": processed_data,
        "relational_modeling": relational_model,
        "integrated_analysis": integrated_analysis,
        "intelligence_score": _calculate_intelligence_score(integrated_analysis)
    }


def _python_data_processing(dataset: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Python surface: Data preprocessing and feature engineering"""

    # Extract entities and relationships
    entities = dataset.get("entities", [])
    relationships = dataset.get("relationships", [])
    features = dataset.get("features", {})

    # Create feature matrix
    if features:
        feature_matrix = _create_feature_matrix(entities, features)
        processed_features = _process_features(feature_matrix, parameters)
    else:
        processed_features = {"matrix": None, "scaled": None}

    # Relationship analysis
    relationship_patterns = _analyze_relationship_patterns(relationships)

    # Statistical summaries
    statistical_summary = _compute_statistical_summary(entities, features)

    # Clustering analysis (if requested)
    clustering_results = {}
    if parameters.get("include_clustering", False) and processed_features["matrix"] is not None:
        clustering_results = _perform_clustering_analysis(processed_features["matrix"], parameters)

    return {
        "entities": entities,
        "relationships": relationships,
        "features": features,
        "processed_features": processed_features,
        "relationship_patterns": relationship_patterns,
        "statistical_summary": statistical_summary,
        "clustering_results": clustering_results,
        "data_quality_score": _assess_data_quality(entities, relationships, features)
    }


def _create_feature_matrix(entities: List[Dict], features: Dict[str, List]) -> np.ndarray:
    """Create feature matrix from entity features"""
    if not entities or not features:
        return np.array([])

    # Get feature columns
    feature_cols = list(features.keys())
    n_entities = len(entities)
    n_features = len(feature_cols)

    # Create matrix
    matrix = np.zeros((n_entities, n_features))

    # Fill matrix
    for i, entity in enumerate(entities):
        for j, feature in enumerate(feature_cols):
            entity_id = entity.get("id", entity.get("name", f"entity_{i}"))
            feature_values = features[feature]
            if entity_id in feature_values:
                matrix[i, j] = feature_values[entity_id]
            else:
                matrix[i, j] = 0  # Default value

    return matrix


def _process_features(feature_matrix: np.ndarray, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Process and scale features"""
    if feature_matrix.size == 0:
        return {"matrix": None, "scaled": None}

    # Feature scaling
    scaler = StandardScaler()
    scaled_matrix = scaler.fit_transform(feature_matrix)

    # Feature selection (simplified)
    feature_importance = _calculate_feature_importance(scaled_matrix)

    return {
        "matrix": feature_matrix,
        "scaled": scaled_matrix,
        "feature_importance": feature_importance,
        "dimensionality": feature_matrix.shape
    }


def _calculate_feature_importance(matrix: np.ndarray) -> Dict[str, float]:
    """Calculate feature importance using variance"""
    if matrix.size == 0:
        return {}

    variances = np.var(matrix, axis=0)
    total_variance = np.sum(variances)

    importance = {}
    for i, variance in enumerate(variances):
        importance[f"feature_{i}"] = variance / total_variance if total_variance > 0 else 0

    return importance


def _analyze_relationship_patterns(relationships: List[Dict]) -> Dict[str, Any]:
    """Analyze patterns in relationships"""
    if not relationships:
        return {"patterns": [], "density": 0.0}

    # Count relationship types
    type_counts = {}
    for rel in relationships:
        rel_type = rel.get("type", "unknown")
        type_counts[rel_type] = type_counts.get(rel_type, 0) + 1

    # Calculate density
    unique_entities = set()
    for rel in relationships:
        unique_entities.add(rel.get("from", ""))
        unique_entities.add(rel.get("to", ""))

    n_entities = len(unique_entities)
    n_relationships = len(relationships)
    density = (2 * n_relationships) / (n_entities * (n_entities - 1)) if n_entities > 1 else 0

    return {
        "relationship_types": type_counts,
        "total_relationships": n_relationships,
        "unique_entities": n_entities,
        "density": density,
        "most_common_type": max(type_counts.items(), key=lambda x: x[1]) if type_counts else None
    }


def _compute_statistical_summary(entities: List[Dict], features: Dict[str, List]) -> Dict[str, Any]:
    """Compute statistical summary of the data"""
    summary = {
        "entity_count": len(entities),
        "feature_count": len(features),
        "feature_distributions": {}
    }

    # Feature distributions
    for feature_name, values in features.items():
        if values:
            numeric_values = [v for v in values.values() if isinstance(v, (int, float))]
            if numeric_values:
                summary["feature_distributions"][feature_name] = {
                    "mean": np.mean(numeric_values),
                    "std": np.std(numeric_values),
                    "min": np.min(numeric_values),
                    "max": np.max(numeric_values),
                    "count": len(numeric_values)
                }

    return summary


def _perform_clustering_analysis(feature_matrix: np.ndarray, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Perform clustering analysis on the feature matrix"""
    if feature_matrix.size == 0:
        return {"error": "No feature matrix available"}

    n_clusters = parameters.get("n_clusters", min(5, max(2, feature_matrix.shape[0] // 10)))

    try:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(feature_matrix)

        # Calculate silhouette score
        if feature_matrix.shape[0] > n_clusters:
            silhouette_avg = silhouette_score(feature_matrix, clusters)
        else:
            silhouette_avg = None

        return {
            "n_clusters": n_clusters,
            "cluster_labels": clusters.tolist(),
            "cluster_centers": kmeans.cluster_centers_.tolist(),
            "inertia": kmeans.inertia_,
            "silhouette_score": silhouette_avg,
            "cluster_sizes": [int(np.sum(clusters == i)) for i in range(n_clusters)]
        }
    except Exception as e:
        return {"error": str(e)}


def _assess_data_quality(entities: List[Dict], relationships: List[Dict], features: Dict[str, List]) -> float:
    """Assess overall data quality"""
    quality_scores = []

    # Entity completeness
    if entities:
        complete_entities = sum(1 for e in entities if e.get("id") or e.get("name"))
        quality_scores.append(complete_entities / len(entities))

    # Relationship completeness
    if relationships:
        complete_rels = sum(1 for r in relationships if r.get("from") and r.get("to") and r.get("type"))
        quality_scores.append(complete_rels / len(relationships))

    # Feature completeness
    if features:
        total_values = sum(len(values) for values in features.values())
        expected_values = len(entities) * len(features) if entities else 0
        if expected_values > 0:
            quality_scores.append(total_values / expected_values)

    return np.mean(quality_scores) if quality_scores else 0.0


def _datalog_knowledge_modeling(processed_data: Dict[str, Any], query_type: str) -> Dict[str, Any]:
    """Datalog surface: Relational knowledge modeling and querying"""
    try:
        from pyDatalog import pyDatalog
    except ImportError:
        return {"error": "pyDatalog not available", "relational_analysis": {}}

    pyDatalog.clear()
    pyDatalog.create_terms('entity, relationship, feature, pattern, cluster, anomaly')
    pyDatalog.create_terms('X, Y, Z, Type, Value, ClusterId')

    # Load relational knowledge base
    try:
        pyDatalog.load(DATALOG_SURFACE)
    except Exception as e:
        return {"error": f"Failed to load Datalog surface: {e}", "relational_analysis": {}}

    # Add data-specific facts
    entities = processed_data.get("entities", [])
    relationships = processed_data.get("relationships", [])
    features = processed_data.get("features", {})

    for entity in entities:
        entity_id = entity.get("id", entity.get("name", "unknown"))
        pyDatalog.assert_fact('entity', entity_id)

    for rel in relationships:
        rel_from = rel.get("from", "")
        rel_to = rel.get("to", "")
        rel_type = rel.get("type", "unknown")
        pyDatalog.assert_fact('relationship', rel_from, rel_to, rel_type)

    # Query relational patterns based on analysis type
    relational_patterns = _query_relational_patterns(pyDatalog, query_type, entities, relationships)

    return {
        "entities_loaded": len(entities),
        "relationships_loaded": len(relationships),
        "relational_patterns": relational_patterns,
        "knowledge_consistency": _check_knowledge_consistency(pyDatalog, entities, relationships)
    }


def _query_relational_patterns(datalog_engine, query_type: str, entities: List[Dict], relationships: List[Dict]) -> Dict[str, Any]:
    """Query relational patterns based on analysis type"""

    patterns = {}

    if query_type == "clustering":
        # Query cluster relationships
        cluster_query = datalog_engine.ask("cluster_relationship(X, Y, Similarity)")
        patterns["cluster_relationships"] = [{"entity1": r[0], "entity2": r[1], "similarity": r[2]}
                                           for r in (cluster_query.answers if cluster_query else [])]

    elif query_type == "pattern_discovery":
        # Query frequent patterns
        pattern_query = datalog_engine.ask("frequent_pattern(Pattern, Support)")
        patterns["frequent_patterns"] = [{"pattern": r[0], "support": r[1]}
                                       for r in (pattern_query.answers if pattern_query else [])]

    elif query_type == "anomaly_detection":
        # Query anomalous relationships
        anomaly_query = datalog_engine.ask("anomalous_relationship(X, Y, Score)")
        patterns["anomalous_relationships"] = [{"entity1": r[0], "entity2": r[1], "anomaly_score": r[2]}
                                             for r in (anomaly_query.answers if anomaly_query else [])]

    elif query_type == "prediction":
        # Query predictive relationships
        prediction_query = datalog_engine.ask("predictive_relationship(X, Y, Confidence)")
        patterns["predictive_relationships"] = [{"predictor": r[0], "target": r[1], "confidence": r[2]}
                                              for r in (prediction_query.answers if prediction_query else [])]

    # General relationship analysis
    degree_query = datalog_engine.ask("entity_degree(Entity, Degree)")
    patterns["entity_degrees"] = [{"entity": r[0], "degree": r[1]}
                                for r in (degree_query.answers if degree_query else [])]

    return patterns


def _check_knowledge_consistency(datalog_engine, entities: List[Dict], relationships: List[Dict]) -> float:
    """Check consistency of the relational knowledge base"""
    # Simplified consistency check
    consistency_checks = []

    # Check for orphaned relationships
    entity_ids = {e.get("id", e.get("name", "")) for e in entities}
    orphaned_rels = 0
    for rel in relationships:
        if rel.get("from") not in entity_ids or rel.get("to") not in entity_ids:
            orphaned_rels += 1

    if relationships:
        consistency_checks.append(1.0 - (orphaned_rels / len(relationships)))

    # Check for self-references
    self_refs = sum(1 for rel in relationships if rel.get("from") == rel.get("to"))
    if relationships:
        consistency_checks.append(1.0 - (self_refs / len(relationships)))

    return np.mean(consistency_checks) if consistency_checks else 1.0


def _integrate_relational_intelligence(processed_data: Dict, relational_model: Dict,
                                     query_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Integrate Python data processing with Datalog relational modeling"""

    integrated_results = {
        "query_type": query_type,
        "data_driven_insights": {},
        "relational_insights": {},
        "combined_recommendations": []
    }

    # Data-driven insights from Python processing
    if processed_data.get("clustering_results"):
        integrated_results["data_driven_insights"]["clustering"] = processed_data["clustering_results"]

    if processed_data.get("relationship_patterns"):
        integrated_results["data_driven_insights"]["patterns"] = processed_data["relationship_patterns"]

    # Relational insights from Datalog modeling
    if relational_model.get("relational_patterns"):
        integrated_results["relational_insights"] = relational_model["relational_patterns"]

    # Generate combined recommendations
    recommendations = []

    # Clustering recommendations
    if query_type == "clustering" and processed_data.get("clustering_results"):
        cluster_results = processed_data["clustering_results"]
        if cluster_results.get("silhouette_score", 0) > 0.5:
            recommendations.append("Strong cluster structure detected - consider segmentation strategies")
        else:
            recommendations.append("Weak cluster structure - review feature engineering")

    # Pattern discovery recommendations
    if query_type == "pattern_discovery" and relational_model.get("relational_patterns", {}).get("frequent_patterns"):
        patterns = relational_model["relational_patterns"]["frequent_patterns"]
        if patterns:
            recommendations.append(f"Found {len(patterns)} frequent patterns - leverage for prediction")

    # Anomaly detection recommendations
    if query_type == "anomaly_detection" and relational_model.get("relational_patterns", {}).get("anomalous_relationships"):
        anomalies = relational_model["relational_patterns"]["anomalous_relationships"]
        if anomalies:
            recommendations.append(f"Detected {len(anomalies)} anomalous relationships - investigate outliers")

    # Prediction recommendations
    if query_type == "prediction" and relational_model.get("relational_patterns", {}).get("predictive_relationships"):
        predictions = relational_model["relational_patterns"]["predictive_relationships"]
        if predictions:
            high_conf_predictions = [p for p in predictions if p.get("confidence", 0) > 0.8]
            recommendations.append(f"Found {len(high_conf_predictions)} high-confidence predictive relationships")

    integrated_results["combined_recommendations"] = recommendations

    return integrated_results


def _calculate_intelligence_score(integrated_analysis: Dict[str, Any]) -> float:
    """Calculate overall intelligence score"""

    scores = []

    # Data quality contribution
    data_insights = len(integrated_analysis.get("data_driven_insights", {}))
    if data_insights > 0:
        scores.append(min(1.0, data_insights / 5.0))

    # Relational insights contribution
    relational_insights = len(integrated_analysis.get("relational_insights", {}))
    if relational_insights > 0:
        scores.append(min(1.0, relational_insights / 10.0))

    # Recommendations quality
    recommendations = integrated_analysis.get("combined_recommendations", [])
    if recommendations:
        scores.append(min(1.0, len(recommendations) / 5.0))

    return np.mean(scores) if scores else 0.5


def register_skill():
    """Register this skill with metadata"""
    return {
        "name": "data_driven_relational_intelligence",
        "description": "Multi-surface relational intelligence combining data processing with knowledge modeling",
        "version": "1.0.0",
        "domain": "HIGH_REASONING",
        "surfaces": ["python", "datalog"],
        "capabilities": [
            "data_processing_and_analytics",
            "relational_knowledge_modeling",
            "clustering_analysis",
            "pattern_discovery",
            "anomaly_detection",
            "predictive_modeling"
        ]
    }