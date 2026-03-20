"""
Cluster Validation Analyzer

Evaluates cluster quality using multiple metrics:
- Silhouette score
- Calinski-Harabasz index
- Davies-Bouldin index
- Dunn index
"""

import math
from typing import Any, Dict, List


def _euclidean_distance(p1: List[float], p2: List[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2, strict=False)))


def _centroid(cluster_points: List[List[float]]) -> List[float]:
    """Calculate centroid of a cluster"""
    if not cluster_points:
        return []
    n_features = len(cluster_points[0])
    return [
        sum(p[f] for p in cluster_points) / len(cluster_points)
        for f in range(n_features)
    ]


def cluster_validation_analyzer(
    data: List[List[float]],
    assignments: List[int],
    **kwargs,
) -> Dict[str, Any]:
    """
    Evaluate cluster quality using multiple validation metrics.

    Args:
        data: List of data points
        assignments: Cluster assignments for each point
        **kwargs: Additional parameters

    Returns:
        Validation metrics and quality assessment
    """

    if len(data) != len(assignments):
        return {"status": "error", "error": "Data and assignments length mismatch"}

    if len(data) < 2:
        return {"status": "error", "error": "Need at least 2 data points"}

    n = len(data)
    unique_clusters = set(assignments)
    k = len(unique_clusters)

    if k < 2:
        return {"status": "error", "error": "Need at least 2 clusters for validation"}

    # Group points by cluster
    clusters = {}
    for i, cid in enumerate(assignments):
        if cid not in clusters:
            clusters[cid] = []
        clusters[cid].append(data[i])

    # Calculate centroids
    centroids = {cid: _centroid(points) for cid, points in clusters.items()}

    # Calculate silhouette score for each point
    silhouettes = []
    for i in range(n):
        point = data[i]
        cid = assignments[i]

        # a(i): mean distance to points in same cluster
        same_cluster = [data[j] for j in range(n) if j != i and assignments[j] == cid]
        if same_cluster:
            a_i = sum(_euclidean_distance(point, p) for p in same_cluster) / len(
                same_cluster
            )
        else:
            a_i = 0

        # b(i): min mean distances to other clusters
        b_i = float("inf")
        for other_cid, other_points in clusters.items():
            if other_cid != cid and other_points:
                mean_dist = sum(
                    _euclidean_distance(point, p) for p in other_points
                ) / len(other_points)
                b_i = min(b_i, mean_dist)

        # Silhouette for this point
        s_i = (b_i - a_i) / max(a_i, b_i) if max(a_i, b_i) > 0 else 0
        silhouettes.append(s_i)

    # Overall metrics
    silhouette_score = sum(silhouettes) / n

    # Calinski-Harabasz Index (variance ratio)
    # Between-cluster variance / within-cluster variance * (n - k) / (k - 1)
    global_centroid = _centroid(data)

    between_var = sum(
        len(clusters[cid]) * _euclidean_distance(centroids[cid], global_centroid) ** 2
        for cid in clusters
    )

    within_var = 0
    for cid, points in clusters.items():
        for p in points:
            within_var += _euclidean_distance(p, centroids[cid]) ** 2

    ch_index = between_var / within_var * (n - k) / (k - 1) if within_var > 0 else 0

    # Davies-Bouldin Index (avg similarity between clusters)
    db_index = 0
    for cid in clusters:
        max_sim = 0
        for other_cid in clusters:
            if other_cid != cid:
                # Similarity = (s_i + s_j) / d(i,j)
                if centroids[cid] and centroids[other_cid]:
                    dist = _euclidean_distance(centroids[cid], centroids[other_cid])
                    if dist > 0:
                        # Average within-cluster distances
                        s_i = sum(
                            _euclidean_distance(p, centroids[cid])
                            for p in clusters[cid]
                        ) / len(clusters[cid])
                        s_j = sum(
                            _euclidean_distance(p, centroids[other_cid])
                            for p in clusters[other_cid]
                        ) / len(clusters[other_cid])
                        sim = (s_i + s_j) / dist
                        max_sim = max(max_sim, sim)
        db_index += max_sim
    db_index /= k

    # Dunn Index (min inter-cluster dist / max intra-cluster diam)
    # Simplified: using centroid distances
    min_inter = float("inf")
    for cid1 in clusters:
        for cid2 in clusters:
            if cid1 < cid2:
                dist = _euclidean_distance(centroids[cid1], centroids[cid2])
                min_inter = min(min_inter, dist)

    max_intra = 0
    for cid, points in clusters.items():
        if len(points) > 1:
            max_dist = max(
                _euclidean_distance(p1, p2) for p1 in points for p2 in points
            )
            max_intra = max(max_intra, max_dist)

    dunn_index = min_inter / max_intra if max_intra > 0 else 0

    # Interpretation
    interpretation = _interpret_metrics(
        silhouette_score, ch_index, db_index, dunn_index, k
    )

    return {
        "status": "success",
        "n_clusters": k,
        "n_points": n,
        "metrics": {
            "silhouette_score": round(silhouette_score, 4),
            "calinski_harabasz_index": round(ch_index, 4),
            "davies_bouldin_index": round(db_index, 4),
            "dunn_index": round(dunn_index, 4),
        },
        "interpretation": interpretation,
        "per_point_silhouette": {
            "min": round(min(silhouettes), 4),
            "max": round(max(silhouettes), 4),
            "avg": round(sum(silhouettes) / n, 4),
        },
    }


def _interpret_metrics(
    sil: float, ch: float, db: float, dunn: float, k: int
) -> Dict[str, Any]:
    """Interpret validation metrics"""

    # Silhouette: -1 to 1, higher is better
    if sil >= 0.5:
        sil_interp = "Strong structure"
    elif sil >= 0.25:
        sil_interp = "Reasonable structure"
    elif sil >= 0:
        sil_interp = "Weak structure"
    else:
        sil_interp = "No structure"

    # Calinski-Harabasz: higher is better
    ch_interp = "Good" if ch > 100 else "Moderate" if ch > 50 else "Poor"

    # Davies-Bouldin: lower is better
    db_interp = "Good" if db < 1 else "Moderate" if db < 2 else "Poor"

    # Overall
    good_count = sum(
        [
            sil >= 0.25,
            ch > 50,
            db < 1.5,
        ]
    )

    if good_count >= 2:
        overall = "Good clustering quality"
    elif good_count >= 1:
        overall = "Moderate clustering quality"
    else:
        overall = "Poor clustering quality - consider different k or algorithm"

    return {
        "silhouette": sil_interp,
        "calinski_harabasz": ch_interp,
        "davies_bouldin": db_interp,
        "overall": overall,
    }


def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "validate")
    data = payload.get("data", [])
    assignments = payload.get("assignments", [])

    if action == "validate":
        result = cluster_validation_analyzer(data, assignments)
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return {"result": result}


def register_skill():
    """Return skill metadata"""
    return {
        "name": "cluster-validation-analyzer",
        "description": "Evaluate cluster quality using silhouette, Calinski-Harabasz, Davies-Bouldin, and Dunn indices",
        "version": "1.0.0",
        "domain": "DATA_SCIENCE",
    }
