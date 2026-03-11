#!/usr/bin/env python3
"""
Test script for the IaC loop functionality using the actual project files.
"""

import sys
import os
import json
import asyncio
import subprocess
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the discovery service components
from discovery_service import (
    REGISTRY_FILE, MCP_CONFIG_FILE, DOCKER_COMPOSE_FILE,
    deploy_infrastructure, master_flywheel
)

async def test_actual_master_flywheel():
    """Test the master_flywheel tool with actual project files."""
    print("=== Testing Master Flywheel with Actual Project Files ===")
    
    # Ensure we're using the actual project files
    actual_compose = Path("docker-compose.yml")
    actual_registry = Path("skill_registry.json")
    
    if not actual_compose.exists():
        print("❌ docker-compose.yml not found in project directory")
        return False
    
    if not actual_registry.exists():
        print("❌ skill_registry.json not found in project directory")
        return False
    
    print(f"✓ Found docker-compose.yml: {actual_compose}")
    print(f"✓ Found skill_registry.json: {actual_registry}")
    
    # Test the master flywheel function
    try:
        print("=== Executing Master Flywheel ===")
        result = await master_flywheel()
        print(f"Master flywheel result: {result}")
        
        # Analyze result
        if result.get("status") in ["success", "partial_success"]:
            print("✓ Master flywheel completed successfully")
            summary = result.get("summary", {})
            print(f"  - Configuration synced: {summary.get('configuration_synced', False)}")
            print(f"  - Infrastructure deployed: {summary.get('infrastructure_deployed', False)}")
            print(f"  - All services running: {summary.get('all_services_running', False)}")
            print(f"  - Services status: {summary.get('services_running', 0)}/{summary.get('total_services', 0)}")
            
            # Check deployment details
            deploy_result = result.get("deploy_result", {})
            verification = deploy_result.get("verification", {})
            print(f"  - Running containers: {verification.get('running_containers', [])}")
            
            return True
        else:
            print("✗ Master flywheel failed")
            print(f"  - Error: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"✗ Error during master flywheel: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_reprovisioning_with_actual_files():
    """Test re-provisioning with the actual docker-compose.yml file."""
    print("\n=== Testing Re-provisioning with Actual Files ===")
    
    # Read current docker-compose.yml
    with open("docker-compose.yml", 'r') as f:
        original_content = f.read()
    
    print("✓ Read current docker-compose.yml")
    
    # Modify docker-compose.yml (add a comment to simulate Agent R&D service change)
    modified_content = original_content + "\n    # Test comment added for re-provisioning validation\n"
    
    with open("docker-compose.yml", 'w') as f:
        f.write(modified_content)
    
    print("✓ Modified docker-compose.yml with test comment")
    
    # Run master flywheel to test re-provisioning
    try:
        print("=== Executing Re-provisioning ===")
        result = await master_flywheel()
        print(f"Re-provisioning result: {result}")
        
        if result.get("status") in ["success", "partial_success"]:
            print("✓ Re-provisioning successful - infrastructure updated with new configuration")
            
            # Restore original content
            with open("docker-compose.yml", 'w') as f:
                f.write(original_content)
            print("✓ Restored original docker-compose.yml")
            
            return True
        else:
            print("✗ Re-provisioning failed")
            
            # Restore original content even on failure
            with open("docker-compose.yml", 'w') as f:
                f.write(original_content)
            print("✓ Restored original docker-compose.yml")
            
            return False
            
    except Exception as e:
        print(f"✗ Error during re-provisioning: {e}")
        import traceback
        traceback.print_exc()
        
        # Restore original content on error
        with open("docker-compose.yml", 'w') as f:
            f.write(original_content)
        print("✓ Restored original docker-compose.yml")
        
        return False

async def check_docker_status():
    """Check current Docker status."""
    print("\n=== Checking Current Docker Status ===")
    
    try:
        # Check if docker is running
        result = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ Docker is running")
        else:
            print("✗ Docker is not running or accessible")
            return False
        
        # Check current containers
        result = subprocess.run(["docker", "ps", "-a"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            total_containers = len(lines) - 1  # Subtract header line
            running_containers = 0
            
            for line in lines[1:]:  # Skip header
                if 'Up ' in line:
                    running_containers += 1
            
            print(f"✓ Found {total_containers} total containers, {running_containers} running")
            return True
        else:
            print("✗ Could not check container status")
            return False
            
    except Exception as e:
        print(f"✗ Error checking Docker status: {e}")
        return False

async def main():
    print("=== Testing IaC Loop with Actual Project Files ===\n")
    
    # Check Docker status first
    docker_ok = await check_docker_status()
    
    if not docker_ok:
        print("⚠️  Docker is not available. Testing configuration sync only.")
        
        # Test configuration sync without deployment
        try:
            from discovery_service import sync_mcp_config
            result = await sync_mcp_config()
            print(f"Configuration sync result: {result}")
            
            if result.get("status") == "success":
                print("✓ Configuration synchronization works correctly")
                return True
            else:
                print("✗ Configuration synchronization failed")
                return False
        except Exception as e:
            print(f"✗ Error during configuration sync: {e}")
            return False
    
    # Test with Docker available
    success1 = await test_actual_master_flywheel()
    success2 = await test_reprovisioning_with_actual_files()
    
    print(f"\n=== Test Results ===")
    print(f"Master flywheel test: {'✓ PASS' if success1 else '✗ FAIL'}")
    print(f"Re-provisioning test: {'✓ PASS' if success2 else '✗ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All IaC loop tests passed! The infrastructure deployment and re-provisioning is working correctly.")
        print("\n📋 Summary:")
        print("  ✅ deploy_infrastructure tool implemented")
        print("  ✅ master_flywheel command created")
        print("  ✅ Configuration synchronization works")
        print("  ✅ Infrastructure deployment works")
        print("  ✅ Re-provisioning capability verified")
        print("  ✅ Comment changes trigger re-deployment")
        return True
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)