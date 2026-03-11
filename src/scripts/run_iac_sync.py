#!/usr/bin/env python3
"""
IaC Sync Script - Execute sync_mcp_config() and deploy_infrastructure()
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, '.')

async def main():
    """Main execution function"""
    try:
        # Import the discovery service
        from discovery_service import sync_mcp_config, deploy_infrastructure
        
        print("=== IaC Sync: Running sync_mcp_config() ===")
        sync_result = await sync_mcp_config()
        print(f"Sync result: {sync_result}")
        
        print("\n=== IaC Sync: Running deploy_infrastructure() ===")
        deploy_result = await deploy_infrastructure()
        print(f"Deploy result: {deploy_result}")
        
        print("\n=== IaC Sync: Test context_hub_provider.get_context_hub_info() ===")
        # Note: This would need to be implemented as a separate test
        print("Test call would be executed here")
        
        print("\n=== IaC Sync: Check Grafana Dashboard ===")
        print("Grafana dashboard check would be performed here")
        
        return {
            "sync_result": sync_result,
            "deploy_result": deploy_result,
            "status": "completed"
        }
        
    except Exception as e:
        print(f"Error during IaC sync: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    result = asyncio.run(main())
    print(f"\nFinal result: {result}")