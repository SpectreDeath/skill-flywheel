#!/usr/bin/env python3
"""
Test script for verifying skill functionality
"""

import asyncio
import sys

# Add src to path
sys.path.append("src")


async def test_skill(skill_path, action="get_stats"):
    """Test a skill with the given action"""
    try:
        # Import the skill module
        module_path = skill_path.replace("/", ".")
        module = __import__(f"skills.{module_path}", fromlist=["invoke"])

        # Call the skill
        result = await module.invoke({"action": action})
        return result.get("result", {})
    except Exception as e:
        return {"error": str(e)}


async def main():
    """Test all implemented skills"""
    print("Testing Skill Flywheel Implementation")
    print("=" * 50)

    # Test skills from different domains
    test_cases = [
        ("agentic_ai/agent_reasoning_engine", "analyze_problem"),
        ("agentic_ai/goal_management_system", "get_goals"),
        ("agentic_ai/self_improvement_engine", "get_improvements"),
        ("cloud_engineering/infrastructure_as_code", "get_resources"),
        ("cloud_engineering/cloud_monitoring_system", "get_metrics"),
        ("cloud_engineering/auto_scaling_manager", "get_scaling_policies"),
        ("data_engineering/data_pipeline_manager", "get_pipelines"),
        ("data_engineering/data_quality_checker", "get_quality_metrics"),
        ("data_engineering/stream_processing_engine", "get_streams"),
        ("database_engineering/database_schema_designer", "get_schemas"),
        ("database_engineering/query_optimizer", "get_optimizations"),
        ("database_engineering/migration_manager", "get_migrations"),
        ("devops/ci_cd_pipeline_manager", "get_pipelines"),
        ("devops/infrastructure_monitoring", "get_monitoring_data"),
        ("devops/deployment_automation", "get_deployments"),
        ("modern_backend/api_gateway", "get_gateways"),
        ("modern_backend/microservices_orchestrator", "get_services"),
        ("modern_backend/event_driven_architecture", "get_stats"),
        ("orchestration/workflow_orchestrator", "get_stats"),
        ("orchestration/resource_orchestrator", "get_stats"),
        ("orchestration/service_orchestrator", "get_stats"),
    ]

    passed = 0
    failed = 0

    for skill_path, action in test_cases:
        print(f"Testing {skill_path}...")
        result = await test_skill(skill_path, action)

        if "error" in result:
            print(f"  ✗ FAILED: {result['error']}")
            failed += 1
        else:
            print(f"  ✓ PASSED: {len(str(result))} characters returned")
            passed += 1

    print("\n" + "=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    print(f"Success Rate: {passed / (passed + failed) * 100:.1f}%")

    if failed == 0:
        print("\n🎉 All skills are working correctly!")
    else:
        print(f"\n⚠️  {failed} skills need attention")


if __name__ == "__main__":
    asyncio.run(main())
