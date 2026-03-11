#!/usr/bin/env python3
"""
Test script for the Self-Healing Watchdog

This script provides functionality to test the watchdog monitoring system
by simulating service failures and verifying the recovery process.
"""

import asyncio
import subprocess
import time
import json
import datetime
from pathlib import Path
import requests
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def check_service_health(service_name: str, port: int) -> bool:
    """Check if a service is healthy"""
    try:
        response = requests.get(f"http://mcp-{service_name}:{port}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def stop_service(service_name: str) -> bool:
    """Stop a Docker service"""
    try:
        result = subprocess.run(
            ["docker", "stop", f"mcp-{service_name}"],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error stopping service {service_name}: {e}")
        return False

def start_service(service_name: str) -> bool:
    """Start a Docker service"""
    try:
        result = subprocess.run(
            ["docker", "start", f"mcp-{service_name}"],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error starting service {service_name}: {e}")
        return False

def check_log_file(log_file: str = "flywheel_events.log") -> list:
    """Read and parse the log file"""
    events = []
    if Path(log_file).exists():
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    events.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
    return events

async def test_health_check():
    """Test the health checking functionality"""
    print_section("Testing Health Check Functionality")
    
    # Import the watchdog components
    from watchdog_monitor import HealthChecker, SERVICES
    
    health_checker = HealthChecker()
    
    print("Checking health of all services...")
    failed_services = []
    
    for service in SERVICES:
        result = health_checker.check_service_health(service)
        status = "✓" if result["status"] == "HEALTHY" else "✗"
        print(f"  {status} {service['name']}: {result['status']}")
        if result["status"] != "HEALTHY":
            failed_services.append(result)
    
    if failed_services:
        print(f"\nFound {len(failed_services)} unhealthy services:")
        for service in failed_services:
            print(f"  - {service['service']}: {service['error']}")
    else:
        print("\n✓ All services are healthy")
    
    return failed_services

async def test_recovery_simulation():
    """Test the recovery simulation by stopping and starting a service"""
    print_section("Testing Recovery Simulation")
    
    # Choose a service to test with (preferably one that's not critical)
    test_service = "mcp-discovery"  # This is a good test service
    test_port = 8000
    
    print(f"Testing with service: {test_service}")
    
    # Check initial state
    initial_healthy = check_service_health(test_service, test_port)
    print(f"Initial state: {'Healthy' if initial_healthy else 'Unhealthy'}")
    
    if not initial_healthy:
        print("Service is already unhealthy, skipping test")
        return
    
    # Stop the service
    print(f"Stopping service {test_service}...")
    if stop_service(test_service):
        print("✓ Service stopped successfully")
    else:
        print("✗ Failed to stop service")
        return
    
    # Wait a moment
    await asyncio.sleep(2)
    
    # Check if service is down
    after_stop_healthy = check_service_health(test_service, test_port)
    print(f"After stop: {'Still healthy' if after_stop_healthy else 'Successfully stopped'}")
    
    if after_stop_healthy:
        print("✗ Service is still responding after stop - test may not work properly")
    else:
        print("✓ Service successfully stopped")
    
    # Start the service again
    print(f"Starting service {test_service}...")
    if start_service(test_service):
        print("✓ Service started successfully")
    else:
        print("✗ Failed to start service")
        return
    
    # Wait for service to come back online
    print("Waiting for service to come back online...")
    max_wait = 30
    wait_time = 0
    while wait_time < max_wait:
        if check_service_health(test_service, test_port):
            print(f"✓ Service is back online after {wait_time} seconds")
            break
        await asyncio.sleep(1)
        wait_time += 1
    else:
        print(f"✗ Service did not come back online after {max_wait} seconds")
    
    print("\nRecovery simulation test completed")

def test_log_file():
    """Test the log file functionality"""
    print_section("Testing Log File Functionality")
    
    log_file = "flywheel_events.log"
    
    # Check if log file exists
    if Path(log_file).exists():
        print(f"✓ Log file exists: {log_file}")
        
        # Read recent events
        events = check_log_file(log_file)
        print(f"✓ Found {len(events)} log entries")
        
        if events:
            print("\nRecent log entries:")
            for i, event in enumerate(events[-5:], 1):  # Show last 5 entries
                print(f"  {i}. {event['event_type']} - {event.get('timestamp', 'No timestamp')}")
                if 'failed_services' in event:
                    services = [svc['service'] for svc in event['failed_services']]
                    print(f"     Services: {', '.join(services)}")
    else:
        print(f"✗ Log file does not exist: {log_file}")
        print("This is expected if the watchdog hasn't run yet")

def test_docker_services():
    """Test Docker service status"""
    print_section("Testing Docker Services Status")
    
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            mcp_services = [line for line in lines if 'mcp-' in line]
            
            if mcp_services:
                print("MCP Services Status:")
                for service in mcp_services:
                    print(f"  {service}")
            else:
                print("No MCP services found running")
        else:
            print(f"Error running docker ps: {result.stderr}")
            
    except Exception as e:
        print(f"Error checking Docker services: {e}")

def main():
    """Main test function"""
    print("=== Self-Healing Watchdog Test Suite ===")
    print("This script tests the watchdog functionality without running the full monitor")
    
    # Test 1: Health check functionality
    asyncio.run(test_health_check())
    
    # Test 2: Docker services status
    test_docker_services()
    
    # Test 3: Log file functionality
    test_log_file()
    
    # Test 4: Recovery simulation (optional, requires user confirmation)
    print_section("Recovery Simulation Test")
    print("This test will stop and restart a service to simulate a failure.")
    print("This is optional and requires Docker services to be running.")
    
    response = input("Do you want to run the recovery simulation test? (y/N): ").strip().lower()
    
    if response in ['y', 'yes']:
        asyncio.run(test_recovery_simulation())
    else:
        print("Skipping recovery simulation test")
    
    print_section("Test Suite Complete")
    print("To run the full watchdog monitor, use: python watchdog_monitor.py")
    print("The watchdog will monitor services every 5 minutes and auto-recover on failures.")

if __name__ == "__main__":
    main()