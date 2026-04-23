"""
DBSCAN Clustering

Density-based spatial clustering:
- Automatic cluster detection
- Noise/outlier identification
- No need to specify number of clusters
"""

import math
from typing import Any, Dict, List, Set
from datetime import datetime


def _euclidean_distance(p1: List[float], p2: List[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2, strict=False)))


def _get_neighbors(data: List[List[float]], point_idx: int, eps: float) -> Set[int]:
    """Get all points within eps distance of point_idx"""
    neighbors = set()
    for i in range(len(data)):
        if i != point_idx and _euclidean_distance(data[point_idx], data[i]) <= eps:
            neighbors.add(i)
    return neighbors


def dbscan_clustering(
    data: List[List[float]],
    eps: float = 0.5,
    min_samples: int = 5,
    **kwargs,
) -> Dict[str, Any]:
    """
    Perform DBSCAN density-based clustering.

    Args:
        data: List of data points
        eps: Maximum distance between two points to be neighbors
        min_samples: Minimum points to form a dense region
        **kwargs: Additional parameters

    Returns:
        DBSCAN results with core points, clusters, and noise
    """

    if len(data) < 2:
        return {"status": "error", "error": "Need at least 2 data points"}

    n = len(data)
    assignments = [-1] * n  # -1 = unvisited
    cluster_id = 0

    # Identify core points
    core_points = set()
    for i in range(n):
        neighbors = _get_neighbors(data, i, eps)
        if len(neighbors) >= min_samples:
            core_points.add(i)

    # Cluster assignment
    for i in range(n):
        if assignments[i] != -1:
            continue

        neighbors = _get_neighbors(data, i, eps)

        if len(neighbors) >= min_samples:
            # Start new cluster
            _expand_cluster(
                data, assignments, i, neighbors, cluster_id, eps, min_samples
            )
            cluster_id += 1
        else:
            # Mark as noise (will be updated if reachable from core point)
            assignments[i] = -2

    # Count clusters, noise, core points
    n_clusters = cluster_id
    n_noise = sum(1 for a in assignments if a == -2)
    core_count = len(core_points)

    # Cluster statistics
    cluster_stats = []
    for cid in range(n_clusters):
        members = [i for i, a in enumerate(assignments) if a == cid]
        cluster_stats.append(
            {
                "cluster_id": cid,
                "size": len(members),
                "member_indices": members[:20],  # Sample
                "is_core": sum(1 for m in members if m in core_points),
            }
        )

    return {
        "status": "success",
        "n_clusters": n_clusters,
        "n_noise": n_noise,
        "n_core_points": core_count,
        "eps": eps,
        "min_samples": min_samples,
        "assignments": assignments,
        "core_point_indices": list(core_points)[:50],
        "cluster_stats": cluster_stats,
    }


def _expand_cluster(
    data: List[List[float]],
    assignments: List[int],
    point_idx: int,
    neighbors: Set[int],
    cluster_id: int,
    eps: float,
    min_samples: int,
):
    """Expand cluster from seed point"""
    assignments[point_idx] = cluster_id
    seeds = set(neighbors)
    seeds.discard(point_idx)

    while seeds:
        new_point = seeds.pop()

        if assignments[new_point] == -2:
            # Noise point becomes border point
            assignments[new_point] = cluster_id
        elif assignments[new_point] == -1:
            # Not visited yet
            assignments[new_point] = cluster_id

            # Check if core point
            new_neighbors = _get_neighbors(data, new_point, eps)
            if len(new_neighbors) >= min_samples:
                seeds.update(new_neighbors)


async def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "cluster")
    data = payload.get("data", [])
    eps = payload.get("eps", 0.5)
    min_samples = payload.get("min_samples", 5)

    if action == "cluster":
        result = dbscan_clustering(data, eps, min_samples)
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return{
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
def register_skill():
    """Return skill metadata"""
    return {
        "name": "dbscan-clustering",
        "description": "Perform DBSCAN density-based clustering with automatic cluster detection",
        "version": "1.0.0",
        "domain": "DATA_SCIENCE",
    }
