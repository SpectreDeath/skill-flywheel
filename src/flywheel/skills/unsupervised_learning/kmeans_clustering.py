"
K-Means Clustering

Performs k-means clustering analysis:
- Optimal k selection via elbow method
- Multiple initialization methods
- Cluster assignment and centroids
"

import math
from datetime import datetime
from typing import Any, Dict, List


def _euclidean_distance(p1: List[float], p2: List[float]) -> float:
    "Calculate Euclidean distance"
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2, strict=False)))


def _initialize_centroids(
    data: List[List[float]], k: int, method: str
) -> List[List[float]]:
    "Initialize cluster centroids"
    if method == "random":
        import random

        random.shuffle(data)
        return [list(data[i]) for i in range(min(k, len(data)))]

    # K-means++ initialization
    centroids = [data[0]]
    for _ in range(1, k):
        distances = []
        for point in data:
            min_dist = min(_euclidean_distance(point, c) for c in centroids)
            distances.append(min_dist**2)

        total = sum(distances)
        if total == 0:
            break

        import random

        r = random.random() * total
        cumsum = 0
        for i, d in enumerate(distances):
            cumsum += d
            if cumsum >= r:
                centroids.append(list(data[i]))
                break

    return centroids


def kmeans_clustering(
    data: List[List[float]],
    k: int | None = None,
    max_iterations: int = 100,
    tolerance: float = 1e-4,
    initialization: str = "kmeans++",
    **kwargs,
) -> Dict[str, Any]:
    "
    Perform k-means clustering.

    Args:
        data: List of data points (each point is a list of features)
        k: Number of clusters (if None, uses elbow method)
        max_iterations: Maximum iterations
        tolerance: Convergence tolerance
        initialization: 'random' or 'kmeans++'
        **kwargs: Additional parameters

    Returns:
        Clustering results with assignments and centroids
    "

    if len(data) < 2:
        return {"status": "error", "error": "Need at least 2 data points"}

    n_features = len(data[0])

    # Determine optimal k using elbow method if not provided
    if k is None:
        k = _find_optimal_k(data, max(2, len(data) // 3))

    # Initialize centroids
    centroids = _initialize_centroids(data, k, initialization)

    assignments = []
    prev_inertia = float("inf")

    for iteration in range(max_iterations):
        # Assign points to nearest centroid
        new_assignments = []
        for point in data:
            distances = [_euclidean_distance(point, c) for c in centroids]
            new_assignments.append(distances.index(min(distances)))

        # Update centroids
        new_centroids = []
        for i in range(k):
            cluster_points = [
                data[j] for j in range(len(data)) if new_assignments[j] == i
            ]
            if cluster_points:
                new_centroid = [
                    sum(p[f] for p in cluster_points) / len(cluster_points)
                    for f in range(n_features)
                ]
            else:
                new_centroid = list(centroids[i])
            new_centroids.append(new_centroid)

        # Check convergence
        movement = sum(
            _euclidean_distance(centroids[i], new_centroids[i]) for i in range(k)
        )

        # Calculate inertia (within-cluster sum of squares)
        inertia = 0
        for j, point in enumerate(data):
            inertia += _euclidean_distance(point, centroids[new_assignments[j]]) ** 2

        if movement < tolerance or abs(prev_inertia - inertia) < tolerance:
            centroids = new_centroids
            assignments = new_assignments
            break

        centroids = new_centroids
        assignments = new_assignments
        prev_inertia = inertia

    # Compute cluster statistics
    cluster_stats = []
    for i in range(k):
        cluster_points = [data[j] for j in range(len(data)) if assignments[j] == i]
        if cluster_points:
            distances = [
                _euclidean_distance(p, centroids[i]) ** 2 for p in cluster_points
            ]
            cluster_stats.append(
                {
                    "cluster_id": i,
                    "size": len(cluster_points),
                    "inertia": sum(distances),
                    "avg_distance": math.sqrt(sum(distances) / len(distances))
                    if distances
                    else 0,
                }
            )

    return {
        "status": "success",
        "k": k,
        "centroids": centroids,
        "assignments": assignments,
        "inertia": prev_inertia,
        "cluster_stats": cluster_stats,
        "iterations": iteration + 1,
    }


def _find_optimal_k(data: List[List[float]], max_k: int) -> int:
    "Find optimal k using elbow method"
    if max_k < 2:
        return 2

    inertias = []
    for k in range(1, min(max_k + 1, len(data))):
        if k == 1:
            inertias.append(sum(_euclidean_distance(p, data[0]) ** 2 for p in data))
        else:
            centroids = _initialize_centroids(data, k, "kmeans++")
            assignments = []
            for _ in range(10):  # Few iterations
                assignments = [
                    min(range(k), key=lambda i: _euclidean_distance(p, centroids[i]))
                    for p in data
                ]
                for i in range(k):
                    cluster_points = [
                        data[j] for j in range(len(data)) if assignments[j] == i
                    ]
                    if cluster_points:
                        centroids[i] = [
                            sum(p[f] for p in cluster_points) / len(cluster_points)
                            for f in range(len(data[0]))
                        ]

            inertia = sum(
                _euclidean_distance(data[j], centroids[assignments[j]]) ** 2
                for j in range(len(data))
            )
            inertias.append(inertia)

    # Find elbow using second derivative
    if len(inertias) < 3:
        return 2

    diffs = [inertias[i] - inertias[i + 1] for i in range(len(inertias) - 1)]
    second_diffs = [diffs[i] - diffs[i + 1] for i in range(len(diffs) - 1)]

    elbow_idx = second_diffs.index(max(second_diffs)) + 2
    return max(2, elbow_idx)


async def invoke(payload: dict) -> dict:
    "MCP skill invocation"
    action = payload.get("action", "cluster")
    data = payload.get("data", [])
    k = payload.get("k")
    max_iterations = payload.get("max_iterations", 100)
    initialization = payload.get("initialization", "kmeans++")

    if action == "cluster":
        result = kmeans_clustering(
            data, k, max_iterations, initialization=initialization
        )
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return {
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }


def register_skill():
    "Return skill metadata"
    return {
        "name": "kmeans-clustering",
        "description": "Perform k-means clustering with elbow method for optimal k selection",
        "version": "1.0.0",
        "domain": "DATA_SCIENCE",
    }
