"""Extended tests for core modules."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

import pytest


class TestTelemetry:
    """Tests for telemetry module."""

    def test_advanced_performance_metrics(self):
        """Test AdvancedPerformanceMetrics dataclass."""
        from src.core.telemetry import AdvancedPerformanceMetrics
        import datetime
        
        metrics = AdvancedPerformanceMetrics(
            timestamp=datetime.datetime.now(),
            cpu_usage=50.0,
            memory_usage=60.0,
            disk_usage=70.0,
            gpu_usage=80.0,
            active_connections=10,
            request_count=100,
            error_count=5,
            avg_response_time=0.5,
            p95_response_time=1.0,
            p99_response_time=2.0,
            active_skills=20,
            cached_skills=15,
            cache_hit_rate=0.8,
            ml_prediction_accuracy=0.9,
            resource_utilization_score=0.7,
            anomaly_score=0.1
        )
        
        assert metrics.cpu_usage == 50.0
        assert metrics.active_skills == 20

    def test_advanced_skill_metrics(self):
        """Test AdvancedSkillMetrics dataclass."""
        from src.core.telemetry import AdvancedSkillMetrics
        import datetime
        
        metrics = AdvancedSkillMetrics(
            skill_name="test_skill",
            load_count=10,
            execution_count=100,
            total_load_time=5.0,
            total_execution_time=50.0,
            avg_load_time=0.5,
            avg_execution_time=0.5,
            p95_execution_time=1.0,
            p99_execution_time=2.0,
            last_load_time=datetime.datetime.now(),
            last_execution_time=datetime.datetime.now(),
            dependency_count=3,
            memory_usage=100.0,
            success_rate=0.95,
            priority_score=0.8,
            predicted_usage=0.7,
            predicted_performance=0.85,
            anomaly_detected=False,
            resource_optimization_score=0.75
        )
        
        assert metrics.skill_name == "test_skill"
        assert metrics.success_rate == 0.95

    def test_telemetry_manager_init(self):
        """Test AdvancedTelemetryManager initialization."""
        from src.core.telemetry import AdvancedTelemetryManager
        
        config = {"test": "config"}
        manager = AdvancedTelemetryManager(config)
        
        assert manager.config == config
        assert manager.ml_manager is not None
        assert manager.resource_optimizer is not None


class TestSkills:
    """Tests for skills module."""

    def test_skill_manager_init(self):
        """Test EnhancedSkillManager initialization."""
        from src.core.skills import EnhancedSkillManager
        
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = EnhancedSkillManager(tmpdir)
            assert manager is not None


class TestCache:
    """Tests for cache module."""

    def test_cache_init(self):
        """Test AdvancedCache initialization."""
        from src.core.cache import AdvancedCache
        
        config = {"cache": {"type": "memory", "max_size": 100, "ttl": 60}}
        cache = AdvancedCache(config)
        
        assert cache is not None

    def test_cache_put_get(self):
        """Test cache put and get."""
        from src.core.cache import AdvancedCache
        
        config = {"cache": {"type": "memory", "max_size": 100, "ttl": 60}}
        cache = AdvancedCache(config)
        
        cache.put("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_cache_miss(self):
        """Test cache miss returns None."""
        from src.core.cache import AdvancedCache
        
        config = {"cache": {"type": "memory", "max_size": 100, "ttl": 60}}
        cache = AdvancedCache(config)
        
        assert cache.get("nonexistent") is None

    def test_cache_remove(self):
        """Test cache removal."""
        from src.core.cache import AdvancedCache
        
        config = {"cache": {"type": "memory", "max_size": 100, "ttl": 60}}
        cache = AdvancedCache(config)
        
        cache.put("key1", "value1")
        cache.remove("key1")
        assert cache.get("key1") is None


class TestResourceOptimizer:
    """Tests for resource optimizer module."""

    def test_resource_optimizer_init(self):
        """Test ResourceOptimizer initialization."""
        from src.core.resource_optimizer import ResourceOptimizer
        
        config = {"containers": {"max_containers": 10}}
        optimizer = ResourceOptimizer(config)
        
        assert optimizer is not None

    def test_calculate_utilization_score(self):
        """Test utilization score calculation."""
        from src.core.resource_optimizer import ResourceOptimizer
        
        config = {"containers": {"max_containers": 10}}
        optimizer = ResourceOptimizer(config)
        
        score = optimizer.calculate_utilization_score(50.0, 60.0, 30.0)
        assert 0 <= score <= 1


class TestContainers:
    """Tests for containers module."""

    def test_container_manager_init(self):
        """Test ContainerManager initialization."""
        from src.core.containers import ContainerManager
        
        with patch("docker.from_env"):
            config = {"containers": {"enabled": True}}
            manager = ContainerManager(config)
            assert manager is not None


class TestDockerUtils:
    """Tests for docker utils module."""

    def test_docker_utils_init(self):
        """Test DockerUtils initialization."""
        from src.core.docker_utils import DockerUtils
        
        utils = DockerUtils()
        assert utils is not None


class TestExceptions:
    """Tests for exceptions module."""

    def test_skill_flywheel_error(self):
        """Test SkillFlywheelError."""
        from src.core.exceptions import SkillFlywheelError
        
        error = SkillFlywheelError("Test error")
        assert "Test error" in str(error)

    def test_skill_not_found_error(self):
        """Test SkillNotFoundError."""
        from src.core.exceptions import SkillNotFoundError
        
        error = SkillNotFoundError("skill_name")
        assert "skill_name" in str(error)


class TestValidation:
    """Tests for validation module."""

    def test_validation_import(self):
        """Test validation module imports."""
        from src.core import validation_testing
        assert validation_testing is not None


class TestRegistrySearch:
    """Tests for registry search module."""

    def test_registry_search_import(self):
        """Test registry search module imports."""
        from src.core import registry_search
        assert registry_search is not None


class TestEnrichSkills:
    """Tests for enrich skills module."""

    def test_enrich_skills_import(self):
        """Test enrich skills module imports."""
        from src.core import enrich_skills
        assert enrich_skills is not None
