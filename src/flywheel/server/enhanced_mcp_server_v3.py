#!/usr/bin/env python3
"""
Enhanced MCP Server v3 - Legacy Module

This module is kept for backward compatibility.
All functionality has been split into:
- flywheel.server.config: ServerConfig class
- flywheel.server.server: EnhancedMCPServerV3 class

This file now imports and re-exports from the new modules.
"""

if __name__ == "__main__":
    import logging
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("enhanced_mcp_server_v3.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )

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