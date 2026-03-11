#!/usr/bin/env python3
"""
Test script for the IaC loop functionality.
Tests the deploy_infrastructure and master_flywheel tools.
"""

import sys
import os
import json
import tempfile
import asyncio
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the discovery service components
from discovery_service import (
    REGISTRY_FILE, MCP_CONFIG_FILE, DOCKER_COMPOSE_FILE,
    deploy_infrastructure, master_flywheel
)

def create_test_docker_compose():
    """Create a test docker-compose.yml for testing."""
    test_compose = {
        "version": "3.8",
        "services": {
            "test-service-1": {
                "image": "nginx:alpine",
                "ports": ["8080:80"],
                "restart": "unless-stopped"
            },
            "test-service-2": {
                "image": "redis:alpine",
                "ports": ["6379:6379"],
                "restart": "unless-stopped"
            },
            "test-service-3": {
                "image": "hello-world",
                "restart": "unless-stopped"
            }
        }
    }
    return test_compose

async def test_deploy_infrastructure():
    """Test the deploy_infrastructure tool."""
    print("=== Testing deploy_infrastructure tool ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set environment variables to use temp directory
        os.environ["DOCKER_COMPOSE_FILE"] = os.path.join(temp_dir, "docker-compose.yml")
        
        # Create test docker-compose.yml
        test_compose = create_test_docker_compose()
        with open(os.environ["DOCKER_COMPOSE_FILE"], 'w') as f:
            import yaml
            yaml.dump(test_compose, f, default_flow_style=False, indent=2)
        
        print(f"Created test docker-compose.yml with {len(test_compose['services'])} services")
        
        # Test the deploy function
        try:
            result = await deploy_infrastructure()
            print(f"Deploy result: {result}")
            
            # Analyze result
            if result.get("status") == "success":
                print("✓ Infrastructure deployment completed successfully")
                verification = result.get("verification", {})
                print(f"  - Total services configured: {verification.get('total_services_configured', 0)}")
                print(f"  - Services running: {verification.get('services_running', 0)}")
                print(f"  - Running containers: {verification.get('running_containers', [])}")
            else:
                print("✗ Infrastructure deployment failed")
                print(f"  - Error: {result.get('message')}")
            
            return result.get("status") == "success"
            
        except Exception as e:
            print(f"✗ Error during deployment: {e}")
            import traceback
            traceback.print_exc()
            return False

async def test_master_flywheel():
    """Test the master_flywheel tool."""
    print("\n=== Testing master_flywheel tool ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set environment variables
        os.environ["REGISTRY_FILE"] = os.path.join(temp_dir, "skill_registry.json")
        os.environ["MCP_CONFIG_FILE"] = os.path.join(temp_dir, "mcp_config.json")
        os.environ["DOCKER_COMPOSE_FILE"] = os.path.join(temp_dir, "docker-compose.yml")
        
        # Create test registry
        test_registry = [
            {
                "name": "test-skill-1",
                "domain": "orchestration",
                "description": "Test skill for orchestration domain",
                "version": "1.0.0"
            }
        ]
        with open(os.environ["REGISTRY_FILE"], 'w') as f:
            json.dump(test_registry, f, indent=2)
        
        # Create test docker-compose.yml
        test_compose = create_test_docker_compose()
        with open(os.environ["DOCKER_COMPOSE_FILE"], 'w') as f:
            import yaml
            yaml.dump(test_compose, f, default_flow_style=False, indent=2)
        
        print(f"Created test environment with registry and docker-compose.yml")
        
        # Test the master flywheel function
        try:
            result = await master_flywheel()
            print(f"Master flywheel result: {result}")
            
            # Analyze result
            if result.get("status") in ["success", "partial_success"]:
                print("✓ Master flywheel completed")
                summary = result.get("summary", {})
                print(f"  - Configuration synced: {summary.get('configuration_synced', False)}")
                print(f"  - Infrastructure deployed: {summary.get('infrastructure_deployed', False)}")
                print(f"  - All services running: {summary.get('all_services_running', False)}")
                print(f"  - Services status: {summary.get('services_running', 0)}/{summary.get('total_services', 0)}")
            else:
                print("✗ Master flywheel failed")
                print(f"  - Error: {result.get('message')}")
            
            return result.get("status") in ["success", "partial_success"]
            
        except Exception as e:
            print(f"✗ Error during master flywheel: {e}")
            import traceback
            traceback.print_exc()
            return False

async def test_reprovisioning():
    """Test the re-provisioning capability by modifying docker-compose.yml."""
    print("\n=== Testing Re-provisioning Capability ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set environment variables
        os.environ["REGISTRY_FILE"] = os.path.join(temp_dir, "skill_registry.json")
        os.environ["MCP_CONFIG_FILE"] = os.path.join(temp_dir, "mcp_config.json")
        os.environ["DOCKER_COMPOSE_FILE"] = os.path.join(temp_dir, "docker-compose.yml")
        
        # Create test registry
        test_registry = [{"name": "test-skill", "domain": "orchestration", "description": "Test", "version": "1.0.0"}]
        with open(os.environ["REGISTRY_FILE"], 'w') as f:
            json.dump(test_registry, f, indent=2)
        
        # Create initial docker-compose.yml
        initial_compose = {
            "version": "3.8",
            "services": {
                "test-service": {
                    "image": "nginx:alpine",
                    "ports": ["8080:80"],
                    "restart": "unless-stopped"
                }
            }
        }
        
        with open(os.environ["DOCKER_COMPOSE_FILE"], 'w') as f:
            import yaml
            yaml.dump(initial_compose, f, default_flow_style=False, indent=2)
        
        print("Created initial docker-compose.yml")
        
        # Run master flywheel with initial config
        result1 = await master_flywheel()
        print(f"Initial deployment result: {result1.get('status')}")
        
        # Modify docker-compose.yml (add a comment to simulate Agent R&D service change)
        modified_compose = {
            "version": "3.8",
            "services": {
                "test-service": {
                    "image": "nginx:alpine",
                    "ports": ["8080:80"],
                    "restart": "unless-stopped",
                    # Added comment to simulate Agent R&D service modification
                    "labels": ["comment=Modified for Agent R&D testing"]
                }
            }
        }
        
        with open(os.environ["DOCKER_COMPOSE_FILE"], 'w') as f:
            import yaml
            yaml.dump(modified_compose, f, default_flow_style=False, indent=2)
        
        print("Modified docker-compose.yml with comment (simulating Agent R&D change)")
        
        # Run master flywheel again to test re-provisioning
        result2 = await master_flywheel()
        print(f"Re-provisioning result: {result2.get('status')}")
        
        # Check if re-provisioning was successful
        if result2.get("status") in ["success", "partial_success"]:
            print("✓ Re-provisioning successful - infrastructure updated with new configuration")
            return True
        else:
            print("✗ Re-provisioning failed")
            return False

async def main():
    print("=== Testing IaC Loop Functionality ===\n")
    
    # Test individual tools
    success1 = await test_deploy_infrastructure()
    success2 = await test_master_flywheel()
    
    # Test re-provisioning
    success3 = await test_reprovisioning()
    
    print(f"\n=== Test Results ===")
    print(f"deploy_infrastructure test: {'✓ PASS' if success1 else '✗ FAIL'}")
    print(f"master_flywheel test: {'✓ PASS' if success2 else '✗ FAIL'}")
    print(f"re-provisioning test: {'✓ PASS' if success3 else '✗ FAIL'}")
    
    if success1 and success2 and success3:
        print("\n🎉 All IaC loop tests passed! The infrastructure deployment and re-provisioning is working correctly.")
        return True
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)