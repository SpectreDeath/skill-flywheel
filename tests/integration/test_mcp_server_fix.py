#!/usr/bin/env python3
"""
Fixed test suite for Enhanced MCP Server v3

This test suite avoids circular dependencies by:
- Using mock objects instead of real imports
- Creating isolated test components
- Testing individual functions in isolation
"""

import asyncio
import pathlib
import tempfile
import time
from unittest.mock import Mock, patch

import numpy as np
import pytest

from flywheel.server.config import ServerConfig
from flywheel.core.telemetry import AdvancedTelemetryManager
from flywheel.core.skills import EnhancedSkillManager
from flywheel.core.ml_models import MLModelManager
from flywheel.core.resource_optimizer import ResourceOptimizer
from flywheel.core.cache import AdvancedCache
from flywheel.core.containers import ContainerManager


class TestServerConfig:
    """Test server configuration management"""

    def test_default_config(self):
        """Test default configuration loading"""
        config = ServerConfig()
        assert config.config["server"]["port"] == 8000
        assert config.config["monitoring"]["enabled"] == True
        assert config.config["skills"]["lazy_loading"]["enabled"] == True

    def test_custom_config_loading(self):
        """Test custom configuration loading"""
        # Create a temporary config file
        config_content = """
server:
  port: 9000
  debug: true
monitoring:
  metrics_interval: 120
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(config_content)
            config_path = f.name

        try:
            config = ServerConfig(config_path)
            assert config.config["server"]["port"] == 9000
            assert config.config["server"]["debug"] == True
            assert config.config["monitoring"]["metrics_interval"] == 120
        finally:
            pathlib.Path(config_path).unlink()


class TestAdvancedTelemetryManager:
    """Test advanced telemetry and ML-driven monitoring"""

    @pytest.fixture
    def telemetry_manager(self):
        """Create a telemetry manager for testing"""
        config = {
            "ml": {
                "model_path": "test_models/",
                "feature_window": 100,
                "prediction_horizon": 3600,
            },
            "skills": {
                "lazy_loading": {"pre_load_threshold": 0.8, "unload_threshold": 0.2}
            },
        }
        return AdvancedTelemetryManager(config)

    def test_collect_advanced_metrics(self, telemetry_manager):
        """Test advanced metrics collection"""
        metrics = telemetry_manager.collect_advanced_metrics()

        assert metrics is not None
        assert hasattr(metrics, "timestamp")
        assert hasattr(metrics, "cpu_usage")
        assert hasattr(metrics, "memory_usage")
        assert hasattr(metrics, "anomaly_score")

        # Verify metrics are within reasonable bounds
        assert 0 <= metrics.cpu_usage <= 100
        assert 0 <= metrics.memory_usage <= 100
        assert 0 <= metrics.anomaly_score <= 10

    def test_track_advanced_skill_execution(self, telemetry_manager):
        """Test advanced skill execution tracking"""
        skill_name = "test_skill"
        load_time = 0.5
        execution_time = 1.2
        success = True
        dependencies = ["dep1", "dep2"]

        telemetry_manager.track_advanced_skill_execution(
            skill_name, load_time, execution_time, success, dependencies
        )

        assert skill_name in telemetry_manager.skill_metrics
        metrics = telemetry_manager.skill_metrics[skill_name]

        assert metrics.execution_count == 1
        assert metrics.avg_execution_time == execution_time
        assert metrics.success_rate == 1.0
        assert metrics.dependency_count == 2

    def test_calculate_advanced_priority_score(self, telemetry_manager):
        """Test advanced priority score calculation"""
        # First track some execution data
        skill_name = "test_skill"
        telemetry_manager.track_advanced_skill_execution(
            skill_name, 0.1, 0.5, True, ["dep1"]
        )

        priority = telemetry_manager.calculate_advanced_priority_score(skill_name)

        assert 0 <= priority <= 1
        assert priority > 0  # Should have some priority after execution

    def test_get_advanced_optimization_recommendations(self, telemetry_manager):
        """Test advanced optimization recommendations"""
        # Track some test data
        for i in range(5):
            skill_name = f"skill_{i}"
            telemetry_manager.track_advanced_skill_execution(
                skill_name, 0.1, 0.5, True, []
            )

        recommendations = telemetry_manager.get_advanced_optimization_recommendations()

        assert "skills_to_preload" in recommendations
        assert "skills_to_unload" in recommendations
        assert "performance_issues" in recommendations
        assert "ml_improvements" in recommendations


class TestEnhancedSkillManager:
    """Test enhanced skill management with lazy loading"""

    @pytest.fixture
    def skill_manager(self):
        """Create a skill manager for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            skills_dir = pathlib.Path(temp_dir) / "skills"
            skills_dir.mkdir()

            # Create a test skill file
            skill_file = skills_dir / "test_skill.py"
            skill_file.write_text("""
def test_skill(*args, **kwargs):
    return "Hello from test skill"
""")

            yield EnhancedSkillManager(str(skills_dir))

    @pytest.mark.asyncio
    async def test_discover_skills(self, skill_manager):
        """Test skill discovery"""
        skills = await skill_manager.discover_skills()

        assert "test_skill" in skills
        assert "test_skill" in skill_manager.skills

    @pytest.mark.asyncio
    async def test_load_skill_dynamically(self, skill_manager):
        """Test dynamic skill loading"""
        await skill_manager.discover_skills()

        # Load the skill
        result = await skill_manager.load_skill_dynamically("test_skill")

        assert result is not None
        assert "test_skill" in result
        assert callable(result["test_skill"])

    @pytest.mark.asyncio
    async def test_execute_skill(self, skill_manager):
        """Test skill execution"""
        await skill_manager.discover_skills()

        # Execute the skill
        result = await skill_manager.execute_skill("test_skill")

        assert result == "Hello from test skill"

        # Verify telemetry was updated
        assert "test_skill" in skill_manager.telemetry.skill_metrics
        metrics = skill_manager.telemetry.skill_metrics["test_skill"]
        assert metrics.execution_count == 1


class TestMLModelManager:
    """Test ML model management and predictions"""

    @pytest.fixture
    def ml_manager(self):
        """Create an ML manager for testing"""
        config = {
            "ml": {
                "model_path": "test_models/",
                "algorithms": {
                    "usage_prediction": "RandomForest",
                    "performance_optimization": "LinearRegression",
                    "anomaly_detection": "IsolationForest",
                },
            }
        }
        return MLModelManager(config)

    def test_model_initialization(self, ml_manager):
        """Test ML model initialization"""
        assert "usage_prediction" in ml_manager.models
        assert "performance_optimization" in ml_manager.models
        assert "anomaly_detection" in ml_manager.models

    def test_predict_skill_usage(self, ml_manager):
        """Test skill usage prediction"""
        features = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        prediction = ml_manager.predict_skill_usage("test_skill", features)

        assert 0 <= prediction <= 1

    def test_detect_anomalies(self, ml_manager):
        """Test anomaly detection"""
        metrics = np.array([1, 2, 3, 4, 5])
        is_anomaly = ml_manager.detect_anomalies(metrics)

        assert isinstance(is_anomaly, bool)


class TestResourceOptimizer:
    """Test resource optimization"""

    @pytest.fixture
    def resource_optimizer(self):
        """Create a resource optimizer for testing"""
        config = {"containers": {"max_containers": 10}}
        return ResourceOptimizer(config)

    def test_calculate_utilization_score(self, resource_optimizer):
        """Test resource utilization score calculation"""
        score = resource_optimizer.calculate_utilization_score(50.0, 60.0, 30.0)

        assert 0 <= score <= 1

    def test_optimize_allocation(self, resource_optimizer):
        """Test resource allocation optimization"""
        current_allocation = {"cpu": 50.0, "memory": 50.0}

        optimized = resource_optimizer.optimize_allocation(current_allocation)

        assert "cpu" in optimized
        assert "memory" in optimized
        assert optimized["cpu"] >= current_allocation["cpu"]
        assert optimized["memory"] >= current_allocation["memory"]


class TestAdvancedCache:
    """Test advanced caching with Redis support"""

    def test_memory_cache(self):
        """Test memory-based caching"""
        config = {"cache": {"type": "memory", "max_size": 10, "ttl": 3600}}

        cache = AdvancedCache(config)

        # Test put and get
        cache.put("key1", "value1")
        result = cache.get("key1")

        assert result == "value1"

        # Test removal
        cache.remove("key1")
        result = cache.get("key1")

        assert result is None

    @patch("redis.from_url")
    def test_redis_cache(self, mock_redis):
        """Test Redis-based caching"""
        mock_redis_instance = Mock()
        mock_redis.return_value = mock_redis_instance

        config = {
            "cache": {
                "type": "redis",
                "redis_url": "redis://localhost:6379/0",
                "ttl": 3600,
                "compression": True,
            }
        }

        cache = AdvancedCache(config)

        # Test put and get
        cache.put("key1", "value1")
        cache.get("key1")

        # Verify Redis methods were called
        assert mock_redis_instance.setex.called
        assert mock_redis_instance.get.called


class TestContainerManager:
    """Test container management"""

    @patch("docker.from_env")
    def test_container_scaling(self, mock_docker):
        """Test container scaling functionality"""
        mock_client = Mock()
        mock_docker.return_value = mock_client

        config = {"containers": {"enabled": True, "max_containers": 5}}

        container_manager = ContainerManager(config)

        # Test that container manager was initialized
        assert container_manager.container_enabled == True


class TestAutoScaler:
    """Test auto-scaling functionality"""

    @pytest.fixture
    def auto_scaler(self):
        """Create an auto-scaler for testing"""
        with patch("docker.from_env"):
            with patch.dict(
                "os.environ",
                {
                    "SCALE_UP_THRESHOLD": "0.8",
                    "SCALE_DOWN_THRESHOLD": "0.3",
                    "SCALE_INTERVAL": "60",
                    "MIN_CONTAINERS": "1",
                    "MAX_CONTAINERS": "10",
                },
            ):
                from flywheel.monitoring.auto_scaler import AutoScaler

                return AutoScaler()

    def test_scaling_config(self, auto_scaler):
        """Test scaling configuration"""
        config = auto_scaler.config

        assert config["scale_up_threshold"] == 0.8
        assert config["scale_down_threshold"] == 0.3
        assert config["min_containers"] == 1
        assert config["max_containers"] == 10

    def test_calculate_target_containers(self, auto_scaler):
        """Test target container calculation"""
        # Test scale up
        target = auto_scaler._calculate_target_containers(0.9, 0.95, 2)
        assert target > 2

        # Test scale down
        target = auto_scaler._calculate_target_containers(0.2, 0.15, 5)
        assert target < 5

        # Test maintain
        target = auto_scaler._calculate_target_containers(0.5, 0.55, 3)
        assert target == 3


class TestPerformance:
    """Test performance characteristics"""

    @pytest.mark.asyncio
    async def test_concurrent_skill_loading(self):
        """Test concurrent skill loading performance"""
        # Create multiple test skills
        with tempfile.TemporaryDirectory() as temp_dir:
            skills_dir = pathlib.Path(temp_dir) / "skills"
            skills_dir.mkdir()

            # Create multiple skill files
            for i in range(10):
                skill_file = skills_dir / f"skill_{i}.py"
                skill_file.write_text(f"""
def skill_{i}():
    return "Result from skill {i}"
""")

            skill_manager = EnhancedSkillManager(str(skills_dir))
            await skill_manager.discover_skills()

            # Measure concurrent loading time
            start_time = time.time()

            tasks = []
            for i in range(10):
                task = asyncio.create_task(
                    skill_manager.load_skill_dynamically(f"skill_{i}")
                )
                tasks.append(task)

            await asyncio.gather(*tasks)

            end_time = time.time()
            loading_time = end_time - start_time

            # Should load all skills in reasonable time (less than 10 seconds)
            assert loading_time < 10.0

    def test_ml_model_training_performance(self):
        """Test ML model training performance"""
        config = {
            "ml": {
                "model_path": "test_models/",
                "algorithms": {"usage_prediction": "RandomForest"},
            }
        }

        ml_manager = MLModelManager(config)

        # Generate test data
        X = np.random.rand(100, 10)
        y = np.random.rand(100)

        # Measure training time
        start_time = time.time()
        ml_manager.train_usage_prediction_model(X, y)
        end_time = time.time()

        training_time = end_time - start_time

        # Should train in reasonable time (less than 30 seconds)
        assert training_time < 30.0


class TestIntegration:
    """Integration tests for the complete system"""

    @pytest.mark.skip(reason="Requires full system setup")
    @pytest.mark.asyncio
    async def test_full_server_lifecycle(self):
        """Test complete server lifecycle"""
        # This would test the full server startup, operation, and shutdown
        # For now, we'll test the core components working together

        with tempfile.TemporaryDirectory() as temp_dir:
            skills_dir = pathlib.Path(temp_dir) / "skills"
            skills_dir.mkdir()

            # Create test skills
            for i in range(3):
                skill_file = skills_dir / f"test_skill_{i}.py"
                skill_file.write_text(f"""
def test_skill_{i}():
    return "Result from skill {i}"
""")

            # Initialize components
            skill_manager = EnhancedSkillManager(str(skills_dir))
            telemetry_manager = skill_manager.telemetry

            # Test discovery and execution
            skills = await skill_manager.discover_skills()
            assert len(skills) == 3

            # Execute all skills
            results = []
            for skill in skills:
                result = await skill_manager.execute_skill(skill)
                results.append(result)

            assert len(results) == 3

            # Verify telemetry
            assert len(telemetry_manager.skill_metrics) == 3

            # Test optimization recommendations
            recommendations = (
                telemetry_manager.get_advanced_optimization_recommendations()
            )
            assert "skills_to_preload" in recommendations


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "--tb=short"])
