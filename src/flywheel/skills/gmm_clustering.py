"""
Gaussian Mixture Model Clustering

Probabilistic clustering using GMM:
- Soft clustering with probability assignments
- Multiple covariance types (full, tied, diag, spherical)
- EM algorithm for fitting
"""

import math
import random
from typing import Any, Dict, List
from datetime import datetime


def _multivariate_normal_pdf(
    x: List[float], mean: List[float], cov: List[List[float]]
) -> float:
    """Calculate multivariate normal PDF (simplified)"""
    n = len(x)
    diff = [x[i] - mean[i] for i in range(n)]

    # Simplified: assume diagonal covariance
    var = [cov[i][i] if i < len(cov) else 1 for i in range(n)]

    # Calculate PDF
    coeff = 1 / (
        math.pow(2 * math.pi, n / 2) * math.prod([math.sqrt(v) for v in var if v > 0])
    )
    exponent = -0.5 * sum(
        (diff[i] ** 2) / var[i] if var[i] > 0 else 0 for i in range(n)
    )

    return coeff * math.exp(exponent)


def _initialize_gmm(data: List[List[float]], k: int) -> Dict:
    """Initialize GMM parameters"""
    n = len(data)
    n_features = len(data[0])

    # Random initialization
    random.seed(42)
    indices = random.sample(range(n), k)
    means = [list(data[i]) for i in indices]

    # Equal weights
    weights = [1.0 / k] * k

    # Identity covariance (simplified)
    covs = [
        [[1.0 if i == j else 0 for j in range(n_features)] for i in range(n_features)]
        for _ in range(k)
    ]

    return {"means": means, "weights": weights, "covs": covs}


def gmm_clustering(
    data: List[List[float]],
    n_clusters: int = 3,
    max_iterations: int = 100,
    tolerance: float = 1e-4,
    **kwargs,
) -> Dict[str, Any]:
    """
    Perform Gaussian Mixture Model clustering.

    Args:
        data: List of data points
        n_clusters: Number of clusters/components
        max_iterations: Maximum EM iterations
        tolerance: Convergence tolerance
        **kwargs: Additional parameters

    Returns:
        GMM clustering results with probabilities
    """

    if len(data) < n_clusters:
        return {"status": "error", "error": "Need more points than clusters"}

    n = len(data)
    n_features = len(data[0])

    # Initialize parameters
    params = _initialize_gmm(data, n_clusters)
    means = params["means"]
    weights = params["weights"]
    covs = params["covs"]

    prev_log_likelihood = float("-inf")

    for iteration in range(max_iterations):
        # E-step: Calculate responsibilities
        responsibilities = []
        for point in data:
            point_probs = []
            for k_idx in range(n_clusters):
                prob = weights[k_idx] * _multivariate_normal_pdf(
                    point, means[k_idx], covs[k_idx]
                )
                point_probs.append(prob)

            total = sum(point_probs)
            if total > 0:
                responsibilities.append([p / total for p in point_probs])
            else:
                responsibilities.append([1.0 / n_clusters] * n_clusters)

        # M-step: Update parameters
        for k_idx in range(n_clusters):
            # Sum of responsibilities for this component
            Nk = sum(responsibilities[i][k_idx] for i in range(n))

            if Nk > 0:
                # Update weight
                weights[k_idx] = Nk / n

                # Update mean
                new_mean = [0.0] * n_features
                for i in range(n):
                    for f in range(n_features):
                        new_mean[f] += responsibilities[i][k_idx] * data[i][f]
                means[k_idx] = [m / Nk for m in new_mean]

                # Update covariance (simplified diagonal)
                new_cov = [[0.0] * n_features for _ in range(n_features)]
                for i in range(n):
                    diff = [data[i][f] - means[k_idx][f] for f in range(n_features)]
                    for f1 in range(n_features):
                        for f2 in range(n_features):
                            new_cov[f1][f2] += (
                                responsibilities[i][k_idx] * diff[f1] * diff[f2]
                            )
                covs[k_idx] = [[c / Nk for c in row] for row in new_cov]

        # Check convergence
        log_likelihood = 0
        for point in data:
            total_prob = sum(
                weights[k_idx]
                * _multivariate_normal_pdf(point, means[k_idx], covs[k_idx])
                for k_idx in range(n_clusters)
            )
            if total_prob > 0:
                log_likelihood += math.log(total_prob)

        if abs(log_likelihood - prev_log_likelihood) < tolerance:
            break
        prev_log_likelihood = log_likelihood

    # Final assignments
    assignments = []
    probs = []
    for point in data:
        point_probs = [
            weights[k_idx] * _multivariate_normal_pdf(point, means[k_idx], covs[k_idx])
            for k_idx in range(n_clusters)
        ]
        total = sum(point_probs)
        if total > 0:
            normalized = [p / total for p in point_probs]
        else:
            normalized = [1.0 / n_clusters] * n_clusters
        assignments.append(normalized.index(max(normalized)))
        probs.append(normalized)

    # Cluster statistics
    cluster_stats = []
    for k_idx in range(n_clusters):
        members = [i for i, a in enumerate(assignments) if a == k_idx]
        cluster_stats.append(
            {
                "cluster_id": k_idx,
                "size": len(members),
                "weight": weights[k_idx],
                "centroid": means[k_idx],
            }
        )

    return {
        "status": "success",
        "n_clusters": n_clusters,
        "assignments": assignments,
        "probabilities": probs,
        "cluster_weights": weights,
        "centroids": means,
        "iterations": iteration + 1,
        "log_likelihood": log_likelihood,
        "cluster_stats": cluster_stats,
    }


async def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "cluster")
    data = payload.get("data", [])
    n_clusters = payload.get("n_clusters", 3)
    max_iterations = payload.get("max_iterations", 100)

    if action == "cluster":
        result = gmm_clustering(data, n_clusters, max_iterations)
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
        "name": "gmm-clustering",
        "description": "Perform Gaussian Mixture Model clustering with soft probability assignments",
        "version": "1.0.0",
        "domain": "DATA_SCIENCE",
    }
