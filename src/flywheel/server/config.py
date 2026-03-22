"""
Server Configuration Module

Contains ServerConfig class for managing server configuration.
"""

import logging
import os
from typing import Any, Dict

import yaml

logger = logging.getLogger(__name__)


class ServerConfig:
    """Enhanced server configuration with ML and container support"""

    def __init__(self, config_path: str = "mcp_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file with defaults"""
        default_config = {
            "server": {
                "host": "0.0.0.0",
                "port": 8000,
                "debug": False,
                "cors_origins": [
                    "http://localhost:3000",
                    "http://localhost:5173",
                    "http://localhost:8080",
                    "http://127.0.0.1:3000",
                    "http://127.0.0.1:5173",
                    "http://127.0.0.1:8080",
                ],
                "max_concurrent_requests": 100,
                "request_timeout": 300,
                "workers": 1,
                "worker_class": "uvicorn.workers.UvicornWorker",
            },
            "monitoring": {
                "enabled": True,
                "metrics_interval": 30,
                "log_level": "INFO",
                "telemetry_endpoint": None,
                "prometheus_port": 8001,
                "performance_thresholds": {
                    "cpu_warning": 80.0,
                    "memory_warning": 80.0,
                    "response_time_warning": 5.0,
                    "cache_hit_rate_warning": 0.7,
                },
            },
            "agents": {
                "max_agents": 100,
                "agent_timeout": 300,
                "retry_attempts": 3,
                "parallel_execution": True,
                "load_balancing": "round_robin",
                "auto_scaling": {
                    "enabled": True,
                    "min_agents": 5,
                    "max_agents": 50,
                    "scale_up_threshold": 0.8,
                    "scale_down_threshold": 0.3,
                    "scale_interval": 60,
                },
            },
            "skills": {
                "auto_discovery": True,
                "validation_enabled": True,
                "cache_ttl": 3600,
                "max_skill_size": 1024 * 1024,
                "lazy_loading": {
                    "enabled": True,
                    "cache_size": 100,
                    "ttl_seconds": 1800,
                    "pre_load_threshold": 0.8,
                    "unload_threshold": 0.2,
                    "parallel_loading": True,
                    "max_parallel_loads": 5,
                },
                "optimization": {
                    "enabled": True,
                    "learning_rate": 0.1,
                    "prediction_window": 100,
                    "resource_aware": True,
                    "adaptive_thresholds": True,
                    "ml_models": {
                        "usage_prediction": "random_forest",
                        "performance_optimization": "linear_regression",
                        "anomaly_detection": "isolation_forest",
                    },
                },
            },
            "ml": {
                "enabled": True,
                "model_path": "models/",
                "training_frequency": 3600,
                "prediction_horizon": 3600,
                "feature_window": 100,
                "algorithms": {
                    "usage_prediction": "RandomForest",
                    "performance_optimization": "LinearRegression",
                    "anomaly_detection": "IsolationForest",
                    "resource_optimization": "KMeans",
                },
            },
            "cache": {
                "type": "redis",
                "redis_url": "redis://localhost:6379/0",
                "ttl": 3600,
                "max_size": 1000,
                "compression": True,
            },
            "containers": {
                "enabled": True,
                "orchestrator": "docker",
                "auto_scaling": True,
                "max_containers": 10,
                "resource_limits": {"cpu": "1.0", "memory": "1G", "gpu": False},
            },
            "celery": {
                "broker_url": "redis://localhost:6379/1",
                "result_backend": "redis://localhost:6379/2",
                "task_serializer": "json",
                "result_serializer": "json",
                "accept_content": ["json"],
                "timezone": "UTC",
                "enable_utc": True,
            },
            "security": {
                "api_key_required": False,
                "allowed_ips": [],
                "rate_limit": 1000,
                "jwt_secret": "${MCP_JWT_SECRET}",
                "encryption_enabled": True,
            },
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path) as f:
                    user_config = yaml.safe_load(f)
                    self._merge_config(default_config, user_config)
            except Exception as e:
                logger.warning(f"Failed to load config from {self.config_path}: {e}")

        return default_config

    def _merge_config(self, default: Dict, user: Dict) -> None:
        """Recursively merge user config with defaults"""
        for key, value in user.items():
            if (
                key in default
                and isinstance(default[key], dict)
                and isinstance(value, dict)
            ):
                self._merge_config(default[key], value)
            else:
                default[key] = value
