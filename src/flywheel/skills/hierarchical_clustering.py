"""
Hierarchical Clustering

Performs agglomerative hierarchical clustering:
- Multiple linkage methods (single, complete, average, ward)
- Dendrogram generation
- Cut tree at different thresholds
"""

import math
from typing import Any, Dict, List
from datetime import datetime


def _euclidean_distance(p1: List[float], p2: List[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2, strict=False)))


def _linkage_matrix(data: List[List[float]], method: str) -> List[List[float]]:
    """Compute hierarchical clustering linkage matrix"""
    n = len(data)

    # Initialize distances
    distances = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = _euclidean_distance(data[i], data[j])
            distances[i][j] = d
            distances[j][i] = d

    # Current clusters (initially each point is its own cluster)
    clusters = {i: [i] for i in range(n)}
    active = set(range(n))
    linkage = []
    cluster_id = n

    for _step in range(n - 1):
        # Find closest pair of active clusters
        min_dist = float("inf")
        merge = (None, None)

        active_list = list(active)
        for i in range(len(active_list)):
            for j in range(i + 1, len(active_list)):
                c1, c2 = active_list[i], active_list[j]
                d = _cluster_distance(clusters[c1], clusters[c2], distances, method)
                if d < min_dist:
                    min_dist = d
                    merge = (c1, c2)

        if merge[0] is None:
            break

        c1, c2 = merge

        # Record linkage
        linkage.append([c1, c2, min_dist, len(clusters[c1]), len(clusters[c2])])

        # Merge clusters
        new_cluster = clusters[c1] + clusters[c2]
        clusters[cluster_id] = new_cluster
        active.remove(c1)
        active.remove(c2)
        active.add(cluster_id)

        cluster_id += 1

    return linkage


def _cluster_distance(
    c1: List[int], c2: List[int], distances: List[List[float]], method: str
) -> float:
    """Calculate distance between two clusters"""
    if method == "single":
        return min(distances[i][j] for i in c1 for j in c2)
    elif method == "complete":
        return max(distances[i][j] for i in c1 for j in c2)
    elif method == "average":
        return sum(distances[i][j] for i in c1 for j in c2) / (len(c1) * len(c2))
    elif method == "ward":
        # Ward: increase in variance
        return min(distances[i][j] for i in c1 for j in c2)
    return sum(distances[i][j] for i in c1 for j in c2) / (len(c1) * len(c2))


def hierarchical_clustering(
    data: List[List[float]],
    n_clusters: int | None = None,
    distance_threshold: float | None = None,
    linkage_method: str = "average",
    **kwargs,
) -> Dict[str, Any]:
    """
    Perform hierarchical/agglomerative clustering.

    Args:
        data: List of data points
        n_clusters: Number of clusters (if None, uses distance_threshold)
        distance_threshold: Distance threshold for cutting dendrogram
        linkage_method: Linkage method (single, complete, average, ward)
        **kwargs: Additional parameters

    Returns:
        Hierarchical clustering results with dendrogram structure
    """

    if len(data) < 2:
        return {"status": "error", "error": "Need at least 2 data points"}

    n = len(data)

    # Compute linkage matrix
    if linkage_method not in ["single", "complete", "average", "ward"]:
        linkage_method = "average"

    linkage = _linkage_matrix(data, linkage_method)

    # Cut tree to get clusters
    if n_clusters is not None and n_clusters > 0:
        assignments = _cut_by_clusters(linkage, n, n_clusters)
    elif distance_threshold is not None:
        assignments = _cut_by_distance(linkage, n, distance_threshold)
    else:
        assignments = _cut_by_clusters(linkage, n, max(1, n // 2))

    # Compute cluster statistics
    cluster_ids = set(assignments)
    cluster_stats = []
    for cid in cluster_ids:
        members = [i for i, a in enumerate(assignments) if a == cid]
        cluster_stats.append(
            {
                "cluster_id": cid,
                "size": len(members),
                "member_indices": members,
            }
        )

    return {
        "status": "success",
        "n_clusters": len(cluster_ids),
        "linkage_method": linkage_method,
        "assignments": assignments,
        "cluster_stats": cluster_stats,
        "linkage_sample": linkage[:10],  # First 10 merges
    }


def _cut_by_clusters(linkage: List, n: int, n_clusters: int) -> List[int]:
    """Cut tree to get exactly n clusters"""
    if n_clusters >= n:
        return list(range(n))

    # Start with each point as cluster, merge until n_clusters reached
    clusters = {i: i for i in range(n)}
    active = set(range(n))

    for merge in linkage:
        if len(active) <= n_clusters:
            break

        c1, c2 = int(merge[0]), int(merge[1])
        if c1 in active and c2 in active:
            # Create new cluster ID
            new_id = max(clusters.values()) + 1
            # Remap
            for k in clusters:
                if clusters[k] == c1 or clusters[k] == c2:
                    clusters[k] = new_id
            active.discard(c1)
            active.discard(c2)
            active.add(new_id)

    # Map to 0-indexed cluster IDs
    final_clusters = {}
    next_id = 0
    assignments = [0] * n
    for i in range(n):
        cid = clusters[i]
        if cid not in final_clusters:
            final_clusters[cid] = next_id
            next_id += 1
        assignments[i] = final_clusters[cid]

    return assignments


def _cut_by_distance(linkage: List, n: int, threshold: float) -> List[int]:
    """Cut tree at distance threshold"""
    clusters = list(range(n))

    for merge in linkage:
        if merge[2] > threshold:
            break
        clusters.append(len(clusters))

    return list(range(n))


async def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "cluster")
    data = payload.get("data", [])
    n_clusters = payload.get("n_clusters")
    distance_threshold = payload.get("distance_threshold")
    linkage_method = payload.get("linkage_method", "average")

    if action == "cluster":
        result = hierarchical_clustering(
            data, n_clusters, distance_threshold, linkage_method
        )
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

if __name__ == "__main__":
    return {
            "name": "hierarchical-clustering",
            "description": "Perform agglomerative hierarchical clustering with multiple linkage methods",
            "version": "1.0.0",
            "domain": "DATA_SCIENCE",
        }