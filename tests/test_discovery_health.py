import asyncio
import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

import pytest

def test_health_routing():
    """Test health routing logic."""
    async def run_test():
        print("Testing Discovery Service Health Routing...")
        
        # We can't easily start a real MCP server in this environment without blocking,
        # but we can test the check_service_health logic directly.
        from src.discovery.discovery_service import check_service_health
        
        # Test a port that should be closed (unless something is running on 9999)
        is_up = await check_service_health("localhost", 9999, timeout=0.5)
        print(f"Health check for localhost:9999 (expected DOWN): {'UP' if is_up else 'DOWN'}")
        assert is_up == False, "Port 9999 should be down"
    
    asyncio.run(run_test())
    print("Health routing logic verified (Network connection handling).")

if __name__ == "__main__":
    asyncio.run(test_health_routing())
