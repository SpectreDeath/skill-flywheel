#!/usr/bin/env python3
"""
Simple test suite for MCP Server components

This test suite avoids circular dependencies by:
- Testing individual components in isolation
- Using mock objects for external dependencies
- Testing basic functionality without complex imports
"""

import asyncio
import pytest
import time
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Test basic imports first
def test_basic_imports():
    """Test that we can import basic components without errors"""
    try:
        # Test config import
        from enhanced_mcp_server_v3 import ServerConfig
        config = ServerConfig()
        assert config.config["server"]["port"] == 8000
        print("✅ ServerConfig import successful")
        
        # Test telemetry import
        from enhanced_mcp_server_v3 import AdvancedTelemetryManager
        telemetry_config = {
            "ml": {"model_path": "test_models/", "feature_window": 100},
            "skills": {"lazy_loading": {"pre_load_threshold": 0.8}}
        }
        telemetry = AdvancedTelemetryManager(telemetry_config)
        print("✅ AdvancedTelemetryManager import successful")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

class TestServerConfig:
    """Test server configuration management"""
    
    def test_default_config(self):
        """Test default configuration loading"""
        try:
            from enhanced_mcp_server_v3 import ServerConfig
            config = ServerConfig()
            assert config.config["server"]["port"] == 8000
            assert config.config["monitoring"]["enabled"] == True
            assert config.config["skills"]["lazy_loading"]["enabled"] == True
            print("✅ Default config test passed")
            return True
        except Exception as e:
            print(f"❌ Default config test failed: {e}")
            return False
    
    def test_custom_config_loading(self):
        """Test custom configuration loading"""
        try:
            from enhanced_mcp_server_v3 import ServerConfig
            
            # Create a temporary config file
            config_content = """
server:
  port: 9000
  debug: true
monitoring:
  metrics_interval: 120
"""
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                f.write(config_content)
                config_path = f.name
            
            try:
                config = ServerConfig(config_path)
                assert config.config["server"]["port"] == 9000
                assert config.config["server"]["debug"] == True
                assert config.config["monitoring"]["metrics_interval"] == 120
                print("✅ Custom config test passed")
                return True
            finally:
                Path(config_path).unlink()
        except Exception as e:
            print(f"❌ Custom config test failed: {e}")
            return False

class TestBasicComponents:
    """Test basic component functionality"""
    
    def test_telemetry_manager_creation(self):
        """Test telemetry manager creation"""
        try:
            from enhanced_mcp_server_v3 import AdvancedTelemetryManager
            
            config = {
                "ml": {
                    "model_path": "test_models/",
                    "feature_window": 100,
                    "prediction_horizon": 3600
                },
                "skills": {
                    "lazy_loading": {
                        "pre_load_threshold": 0.8,
                        "unload_threshold": 0.2
                    }
                }
            }
            
            telemetry = AdvancedTelemetryManager(config)
            assert telemetry is not None
            assert hasattr(telemetry, 'skill_metrics')
            assert hasattr(telemetry, 'metrics_history')
            print("✅ Telemetry manager creation test passed")
            return True
        except Exception as e:
            print(f"❌ Telemetry manager creation test failed: {e}")
            return False
    
    def test_cache_creation(self):
        """Test cache creation"""
        try:
            from enhanced_mcp_server_v3 import AdvancedCache
            
            config = {
                "cache": {
                    "type": "memory",
                    "max_size": 10,
                    "ttl": 3600
                }
            }
            
            cache = AdvancedCache(config)
            assert cache is not None
            
            # Test basic cache operations
            cache.put("key1", "value1")
            result = cache.get("key1")
            assert result == "value1"
            
            cache.remove("key1")
            result = cache.get("key1")
            assert result is None
            
            print("✅ Cache creation test passed")
            return True
        except Exception as e:
            print(f"❌ Cache creation test failed: {e}")
            return False
    
    def test_resource_optimizer_creation(self):
        """Test resource optimizer creation"""
        try:
            from enhanced_mcp_server_v3 import ResourceOptimizer
            
            config = {
                "containers": {
                    "max_containers": 10
                }
            }
            
            optimizer = ResourceOptimizer(config)
            assert optimizer is not None
            
            # Test utilization calculation
            score = optimizer.calculate_utilization_score(50.0, 60.0, 30.0)
            assert 0 <= score <= 1
            
            print("✅ Resource optimizer creation test passed")
            return True
        except Exception as e:
            print(f"❌ Resource optimizer creation test failed: {e}")
            return False

class TestMLComponents:
    """Test ML components"""
    
    def test_ml_model_manager_creation(self):
        """Test ML model manager creation"""
        try:
            from enhanced_mcp_server_v3 import MLModelManager
            
            config = {
                "ml": {
                    "model_path": "test_models/",
                    "algorithms": {
                        "usage_prediction": "RandomForest",
                        "performance_optimization": "LinearRegression",
                        "anomaly_detection": "IsolationForest"
                    }
                }
            }
            
            ml_manager = MLModelManager(config)
            assert ml_manager is not None
            assert "usage_prediction" in ml_manager.models
            assert "performance_optimization" in ml_manager.models
            assert "anomaly_detection" in ml_manager.models
            
            print("✅ ML model manager creation test passed")
            return True
        except Exception as e:
            print(f"❌ ML model manager creation test failed: {e}")
            return False
    
    def test_ml_predictions(self):
        """Test ML predictions"""
        try:
            from enhanced_mcp_server_v3 import MLModelManager
            
            config = {
                "ml": {
                    "model_path": "test_models/",
                    "algorithms": {
                        "usage_prediction": "RandomForest",
                        "performance_optimization": "LinearRegression",
                        "anomaly_detection": "IsolationForest"
                    }
                }
            }
            
            ml_manager = MLModelManager(config)
            
            # Test usage prediction
            features = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
            prediction = ml_manager.predict_skill_usage("test_skill", features)
            assert 0 <= prediction <= 1
            
            # Test anomaly detection
            metrics = np.array([1, 2, 3, 4, 5])
            is_anomaly = ml_manager.detect_anomalies(metrics)
            assert isinstance(is_anomaly, bool)
            
            print("✅ ML predictions test passed")
            return True
        except Exception as e:
            print(f"❌ ML predictions test failed: {e}")
            return False

class TestPerformance:
    """Test performance characteristics"""
    
    def test_config_performance(self):
        """Test configuration loading performance"""
        try:
            from enhanced_mcp_server_v3 import ServerConfig
            
            start_time = time.time()
            
            # Load config multiple times
            for i in range(10):
                config = ServerConfig()
                assert config.config["server"]["port"] == 8000
            
            end_time = time.time()
            loading_time = end_time - start_time
            
            # Should load configs quickly (less than 1 second for 10 configs)
            assert loading_time < 1.0
            
            print(f"✅ Config performance test passed ({loading_time:.3f}s)")
            return True
        except Exception as e:
            print(f"❌ Config performance test failed: {e}")
            return False
    
    def test_cache_performance(self):
        """Test cache performance"""
        try:
            from enhanced_mcp_server_v3 import AdvancedCache
            
            config = {
                "cache": {
                    "type": "memory",
                    "max_size": 1000,
                    "ttl": 3600
                }
            }
            
            cache = AdvancedCache(config)
            
            start_time = time.time()
            
            # Test cache operations
            for i in range(100):
                cache.put(f"key_{i}", f"value_{i}")
                result = cache.get(f"key_{i}")
                assert result == f"value_{i}"
            
            end_time = time.time()
            operation_time = end_time - start_time
            
            # Should perform 100 cache operations quickly (less than 1 second)
            assert operation_time < 1.0
            
            print(f"✅ Cache performance test passed ({operation_time:.3f}s)")
            return True
        except Exception as e:
            print(f"❌ Cache performance test failed: {e}")
            return False

def run_all_tests():
    """Run all tests and return summary"""
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Default Config", TestServerConfig().test_default_config),
        ("Custom Config", TestServerConfig().test_custom_config_loading),
        ("Telemetry Manager", TestBasicComponents().test_telemetry_manager_creation),
        ("Cache", TestBasicComponents().test_cache_creation),
        ("Resource Optimizer", TestBasicComponents().test_resource_optimizer_creation),
        ("ML Manager", TestMLComponents().test_ml_model_manager_creation),
        ("ML Predictions", TestMLComponents().test_ml_predictions),
        ("Config Performance", TestPerformance().test_config_performance),
        ("Cache Performance", TestPerformance().test_cache_performance),
    ]
    
    results = []
    
    print("Running MCP Server Component Tests")
    print("=" * 50)
    
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:<25} {status}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)