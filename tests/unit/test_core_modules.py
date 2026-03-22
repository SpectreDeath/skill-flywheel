"""
Unit tests for Skill Flywheel core modules
"""

import os
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDiscoveryServiceAPI:
    """Test discovery service API endpoints"""

    @pytest.fixture
    def client(self):
        from flywheel.server.unified_server import UnifiedMCPServer

        server = UnifiedMCPServer()
        return TestClient(server.app)

    def test_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert "status" in response.json()


class TestSecretValidation:
    """Test secret validation functions"""

    def test_insecure_patterns(self):
        from flywheel.server.constants import INSECURE_SECRET_PATTERNS

        insecure = ["your-openai-api-key-here", "test-key-for-local-development"]
        for val in insecure:
            assert any(p in val.lower() for p in INSECURE_SECRET_PATTERNS)

    def test_secure_values(self):
        from flywheel.server.constants import INSECURE_SECRET_PATTERNS

        secure = ["sk-abc123def456ghi789jkl012mno345pqr"]
        for val in secure:
            assert not any(p in val.lower() for p in INSECURE_SECRET_PATTERNS)


class TestClustering:
    """Test clustering skills"""

    def test_kmeans(self):
        from flywheel.skills.kmeans_clustering import kmeans_clustering

        data = [[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]]
        result = kmeans_clustering(data, k=2)
        assert result["status"] == "success"

    def test_hierarchical(self):
        from flywheel.skills.hierarchical_clustering import hierarchical_clustering

        data = [[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]]
        result = hierarchical_clustering(data, n_clusters=2)
        assert result["status"] == "success"

    def test_dbscan(self):
        from flywheel.skills.dbscan_clustering import dbscan_clustering

        data = [[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]]
        result = dbscan_clustering(data, eps=1.5, min_samples=2)
        assert result["status"] == "success"

    def test_validation(self):
        from flywheel.skills.cluster_validation_analyzer import (
            cluster_validation_analyzer,
        )

        data = [[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]]
        assignments = [0, 0, 0, 1, 1, 1]
        result = cluster_validation_analyzer(data, assignments)
        assert result["status"] == "success"


class TestGameTheory:
    """Test game theory skills"""

    def test_prisoner_single(self):
        from flywheel.skills.prisoners_dilemma_analyzer import (
            prisoners_dilemma_analyzer,
        )

        result = prisoners_dilemma_analyzer("Test", num_rounds=1)
        assert result["status"] == "success"

    def test_prisoner_iterated(self):
        from flywheel.skills.prisoners_dilemma_analyzer import (
            prisoners_dilemma_analyzer,
        )

        result = prisoners_dilemma_analyzer("Test", num_rounds=10)
        assert result["status"] == "success"

    def test_auction(self):
        from flywheel.skills.auction_strategy_optimizer import (
            auction_strategy_optimizer,
        )

        result = auction_strategy_optimizer("first_price", 3, 100)
        assert result["status"] == "success"

    def test_evolutionary(self):
        from flywheel.skills.evolutionary_game_solver import evolutionary_game_solver

        result = evolutionary_game_solver("hawk_dove")
        assert result["status"] == "success"

    def test_coordination(self):
        from flywheel.skills.coordination_game_solver import coordination_game_solver

        result = coordination_game_solver("stag_hunt", ["p1", "p2"])
        assert result["status"] == "success"

    def test_signaling(self):
        from flywheel.skills.signaling_game_analyzer import signaling_game_analyzer

        result = signaling_game_analyzer("costly")
        assert result["status"] == "success"

    def test_repeated(self):
        from flywheel.skills.repeated_game_analyzer import repeated_game_analyzer

        result = repeated_game_analyzer("prisoner", ["p1", "p2"], horizon=10)
        assert result["status"] == "success"


class TestAppConstants:
    """Test constants"""

    def test_constants(self):
        from flywheel.server.constants import (
            CACHE_THRESHOLD,
            DEFAULT_LIMIT,
            MIN_JWT_SECRET_LENGTH,
        )

        assert DEFAULT_LIMIT == 100
        assert CACHE_THRESHOLD == 10
        assert MIN_JWT_SECRET_LENGTH == 32


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
