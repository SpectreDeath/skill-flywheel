"""
Unit tests for Skill Flywheel core modules
"""

import os
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDiscoveryServiceEndpoints:
    """Test discovery service API endpoints"""

    @pytest.fixture
    def client(self):
        from src.server.discovery_service import app

        return TestClient(app)

    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    def test_metrics_endpoint(self, client):
        response = client.get("/metrics")
        assert response.status_code == 200

    def test_list_skills_endpoint(self, client):
        response = client.get("/skills")
        assert response.status_code == 200

    def test_search_skills_endpoint(self, client):
        response = client.get("/skills/search?q=test")
        assert response.status_code == 200

    def test_domains_endpoint(self, client):
        response = client.get("/domains")
        assert response.status_code == 200


class TestSkillValidation:
    """Test skill validation functions"""

    def test_insecure_secret_patterns(self):
        from src.server.discovery_service import INSECURE_SECRET_PATTERNS

        insecure_values = [
            "your-openai-api-key-here",
            "test-key-for-local-development",
        ]
        for val in insecure_values:
            matches = any(
                pattern in val.lower() for pattern in INSECURE_SECRET_PATTERNS
            )
            assert matches

    def test_secure_secrets_not_flagged(self):
        from src.server.discovery_service import INSECURE_SECRET_PATTERNS

        secure_values = [
            "sk-abc123def456ghi789jkl012mno345pqr",
        ]
        for val in secure_values:
            matches = any(
                pattern in val.lower() for pattern in INSECURE_SECRET_PATTERNS
            )
            assert not matches


class TestClusteringSkills:
    """Test clustering skills"""

    def test_kmeans_clustering(self):
        from src.skills.kmeans_clustering import kmeans_clustering

        data = [[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]]
        result = kmeans_clustering(data, k=2)
        assert result["status"] == "success"

    def test_hierarchical_clustering(self):
        from src.skills.hierarchical_clustering import hierarchical_clustering

        data = [[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]]
        result = hierarchical_clustering(data, n_clusters=2)
        assert result["status"] == "success"

    def test_dbscan_clustering(self):
        from src.skills.dbscan_clustering import dbscan_clustering

        data = [[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]]
        result = dbscan_clustering(data, eps=3, min_samples=2)
        assert result["status"] == "success"

    def test_cluster_validation(self):
        from src.skills.cluster_validation_analyzer import cluster_validation_analyzer

        data = [[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]]
        assignments = [0, 0, 0, 1, 1, 1]
        result = cluster_validation_analyzer(data, assignments)
        assert result["status"] == "success"


class TestGameTheorySkills:
    """Test game theory skills"""

    def test_prisoners_dilemma_single_shot(self):
        from src.skills.prisoners_dilemma_analyzer import prisoners_dilemma_analyzer

        result = prisoners_dilemma_analyzer("Test", num_rounds=1)
        assert result["status"] == "success"

    def test_prisoners_dilemma_iterated(self):
        from src.skills.prisoners_dilemma_analyzer import prisoners_dilemma_analyzer

        result = prisoners_dilemma_analyzer("Test", num_rounds=10)
        assert result["status"] == "success"

    def test_auction_strategy(self):
        from src.skills.auction_strategy_optimizer import auction_strategy_optimizer

        result = auction_strategy_optimizer("first_price", 3, 100)
        assert result["status"] == "success"

    def test_evolutionary_game(self):
        from src.skills.evolutionary_game_solver import evolutionary_game_solver

        result = evolutionary_game_solver("hawk_dove")
        assert result["status"] == "success"

    def test_coordination_game(self):
        from src.skills.coordination_game_solver import coordination_game_solver

        result = coordination_game_solver("stag_hunt", ["p1", "p2"])
        assert result["status"] == "success"

    def test_signaling_game(self):
        from src.skills.signaling_game_analyzer import signaling_game_analyzer

        result = signaling_game_analyzer("costly")
        assert result["status"] == "success"

    def test_repeated_game(self):
        from src.skills.repeated_game_analyzer import repeated_game_analyzer

        result = repeated_game_analyzer("prisoner", ["p1", "p2"], horizon=10)
        assert result["status"] == "success"


class TestConstants:
    """Test constants and configuration"""

    def test_discovery_service_constants(self):
        from src.server.discovery_service import (
            CACHE_THRESHOLD,
            DEFAULT_LIMIT,
            MIN_JWT_SECRET_LENGTH,
        )

        assert DEFAULT_LIMIT == 100
        assert CACHE_THRESHOLD == 10
        assert MIN_JWT_SECRET_LENGTH == 32


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
