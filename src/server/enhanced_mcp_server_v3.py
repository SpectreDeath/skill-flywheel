#!/usr/bin/env python3
"""
Legacy compatibility shim for src.server.enhanced_mcp_server_v3

This module exists to maintain backward compatibility with existing tests and
code that import from src.server. All functionality is delegated to the new
flywheel.server module structure.
"""

if __name__ == "__main__":
    from flywheel.server.config import ServerConfig
    from flywheel.server.server import EnhancedMCPServerV3
    from flywheel.core.cache import AdvancedCache
    from flywheel.core.containers import ContainerManager
    from flywheel.core.ml_models import MLModelManager
    from flywheel.core.resource_optimizer import ResourceOptimizer
    from flywheel.core.skills import EnhancedSkillManager
    from flywheel.core.telemetry import AdvancedTelemetryManager
    from flywheel.monitoring.auto_scaler import AutoScaler

    __all__ = [
        "ServerConfig",
        "EnhancedMCPServerV3",
        "AdvancedCache",
        "ContainerManager",
        "MLModelManager",
        "ResourceOptimizer",
        "EnhancedSkillManager",
        "AdvancedTelemetryManager",
        "AutoScaler",
    ]