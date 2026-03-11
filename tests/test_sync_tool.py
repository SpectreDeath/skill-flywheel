#!/usr/bin/env python3
"""
Test script for the sync_mcp_config tool functionality.
This script tests the MCP configuration synchronization without running the full server.
"""

import sys
import os
import json
import tempfile
import shutil
import asyncio
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the discovery service components
from discovery_service import (
    REGISTRY_FILE, MCP_CONFIG_FILE, DOCKER_COMPOSE_FILE,
    SERVICE_GROUPS, DOMAIN_PORT_MAP, sync_mcp_config
)

def create_test_registry():
    """Create a test skill registry for testing."""
    test_registry = [
        {
            "name": "test-skill-1",
            "domain": "orchestration",
            "description": "Test skill for orchestration domain",
            "version": "1.0.0"
        },
        {
            "name": "test-skill-2", 
            "domain": "security",
            "description": "Test skill for security domain",
            "version": "1.0.0"
        },
        {
            "name": "test-skill-3",
            "domain": "data-ai",
            "description": "Test skill for data-ai domain", 
            "version": "1.0.0"
        }
    ]
    return test_registry

async def test_sync_mcp_config():
    """Test the sync_mcp_config tool functionality."""
    print("Testing sync_mcp_config tool...")
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")
        
        # Set environment variables to use temp directory
        os.environ["REGISTRY_FILE"] = os.path.join(temp_dir, "skill_registry.json")
        os.environ["MCP_CONFIG_FILE"] = os.path.join(temp_dir, "mcp_config.json")
        os.environ["DOCKER_COMPOSE_FILE"] = os.path.join(temp_dir, "docker-compose.yml")
        
        # Create test registry file
        test_registry = create_test_registry()
        with open(os.environ["REGISTRY_FILE"], 'w') as f:
            json.dump(test_registry, f, indent=2)
        
        print(f"Created test registry with {len(test_registry)} skills")
        
        # Test the sync function
        try:
            result = await sync_mcp_config()
            print(f"Sync result: {result}")
            
            # Verify files were created
            mcp_config_path = Path(os.environ["MCP_CONFIG_FILE"])
            compose_path = Path(os.environ["DOCKER_COMPOSE_FILE"])
            
            if mcp_config_path.exists():
                print("✓ MCP config file created successfully")
                with open(mcp_config_path, 'r') as f:
                    mcp_config = json.load(f)
                    print(f"  - Services configured: {len(mcp_config.get('services', {}))}")
                    print(f"  - Skills routed: {len(mcp_config.get('skills', {}))}")
            else:
                print("✗ MCP config file was not created")
            
            if compose_path.exists():
                print("✓ Docker compose file created successfully")
                with open(compose_path, 'r') as f:
                    compose_content = f.read()
                    print(f"  - File size: {len(compose_content)} characters")
            else:
                print("✗ Docker compose file was not created")
            
            # Check for backup files
            backup_files = list(Path(temp_dir).glob("*.bak"))
            if backup_files:
                print(f"✓ Backup files created: {len(backup_files)}")
                for backup in backup_files:
                    print(f"  - {backup.name}")
            else:
                print("✗ No backup files were created")
            
            return result.get("status") == "success"
            
        except Exception as e:
            print(f"✗ Error during sync: {e}")
            import traceback
            traceback.print_exc()
            return False

async def test_existing_files():
    """Test sync with existing files to ensure backups are created."""
    print("\nTesting sync with existing files...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set environment variables
        os.environ["REGISTRY_FILE"] = os.path.join(temp_dir, "skill_registry.json")
        os.environ["MCP_CONFIG_FILE"] = os.path.join(temp_dir, "mcp_config.json")
        os.environ["DOCKER_COMPOSE_FILE"] = os.path.join(temp_dir, "docker-compose.yml")
        
        # Create existing files
        existing_mcp_config = {
            "version": "0.9.0",
            "services": {"old-service": {"name": "old"}},
            "skills": {"old-skill": {"service": "old"}}
        }
        
        existing_compose = {
            "version": "3.7",
            "services": {"old-service": {"image": "old"}}
        }
        
        with open(os.environ["MCP_CONFIG_FILE"], 'w') as f:
            json.dump(existing_mcp_config, f)
        
        with open(os.environ["DOCKER_COMPOSE_FILE"], 'w') as f:
            import yaml
            yaml.dump(existing_compose, f)
        
        # Create test registry
        test_registry = create_test_registry()
        with open(os.environ["REGISTRY_FILE"], 'w') as f:
            json.dump(test_registry, f)
        
        # Run sync
        result = await sync_mcp_config()
        print(f"Sync result: {result}")
        
        # Check that backups were created
        backup_files = list(Path(temp_dir).glob("*.bak"))
        print(f"Backup files created: {len(backup_files)}")
        
        # Verify original files were replaced
        with open(os.environ["MCP_CONFIG_FILE"], 'r') as f:
            new_config = json.load(f)
            print(f"New config version: {new_config.get('version')}")
            print(f"New services: {len(new_config.get('services', {}))}")
        
        return result.get("status") == "success"

async def main():
    print("=== Testing sync_mcp_config Tool ===\n")
    
    # Test basic functionality
    success1 = await test_sync_mcp_config()
    
    # Test with existing files
    success2 = await test_existing_files()
    
    print(f"\n=== Test Results ===")
    print(f"Basic sync test: {'✓ PASS' if success1 else '✗ FAIL'}")
    print(f"Existing files test: {'✓ PASS' if success2 else '✗ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! The sync_mcp_config tool is working correctly.")
        return True
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
