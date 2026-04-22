#!/usr/bin/env python3
"""
MCP Client Script for Skill Flywheel

Connects to the Discovery service, performs MCP initialize handshake,
lists available skills, and performs health checks on each skill.
"""

import asyncio
import json
import logging
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Tuple

import aiohttp

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MCPClient:
    """Main MCP client for connecting to Skill Flywheel services."""

    def __init__(self, discovery_url: str = "http://localhost:8000"):
        self.discovery_url = discovery_url
        self.session = None
        self.skills = []
        self.domain_servers = {
            "orchestration": "http://localhost:8001",
            "security": "http://localhost:8002",
            "data-ai": "http://localhost:8003",
            "devops": "http://localhost:8004",
            "engineering": "http://localhost:8005",
            "ux-mobile": "http://localhost:8006",
            "advanced": "http://localhost:8007",
            "strategy": "http://localhost:8008",
            "agent-rd": "http://localhost:8009",
            "model-orchestration": "http://localhost:8012",
        }

    async def initialize(self) -> bool:
        """Perform MCP initialize handshake with Discovery service."""
        logger.info(
            f"Initializing MCP client with Discovery service at {self.discovery_url}"
        )

        try:
            # MCP Initialize handshake
            init_payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-09-03",
                    "capabilities": {"resources": {}, "tools": {}, "notifications": {}},
                    "clientInfo": {
                        "name": "skill-flywheel-mcp-client",
                        "version": "1.0.0",
                    },
                },
            }

            async with (
                aiohttp.ClientSession() as session,
                session.post(
                    f"{self.discovery_url}/",
                    json=init_payload,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response,
            ):
                if response.status == 200:
                    await response.json()
                    logger.info("MCP initialize handshake successful")
                    return True
                else:
                    logger.error(f"Initialize failed with status {response.status}")
                    return False

        except Exception as e:
            logger.error(f"Initialize handshake failed: {e}")
            return False

    async def list_skills(self) -> List[Dict[str, Any]]:
        """Get list of available skills from Discovery service."""
        logger.info("Fetching skill list from Discovery service")

        try:
            # Call tools/list
            list_payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {},
            }

            async with (
                aiohttp.ClientSession() as session,
                session.post(
                    f"{self.discovery_url}/",
                    json=list_payload,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response,
            ):
                if response.status == 200:
                    result = await response.json()
                    if "result" in result:
                        self.skills = result["result"]
                        logger.info(f"Found {len(self.skills)} skills")
                        return self.skills
                    else:
                        logger.error("No skills found in response")
                        return []
                else:
                    logger.error(f"tools/list failed with status {response.status}")
                    return []

        except Exception as e:
            logger.error(f"Failed to list skills: {e}")
            return []

    def categorize_skills(self) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize skills by domain."""
        categorized = {}
        for skill in self.skills:
            domain = skill.get("domain", "unknown")
            if domain not in categorized:
                categorized[domain] = []
            categorized[domain].append(skill)
        return categorized

    async def health_check_skill(
        self, skill: Dict[str, Any]
    ) -> Tuple[str, bool, float, str | None]:
        """
        Perform health check on a skill.
        Returns: (skill_name, is_healthy, response_time, error_message)
        """
        skill_name = skill.get("name", "unknown")
        domain = skill.get("domain", "unknown")

        # Get domain server URL
        domain_server = self.domain_servers.get(domain.lower())
        if not domain_server:
            return skill_name, False, 0.0, f"Unknown domain: {domain}"

        start_time = time.time()

        try:
            # Try to connect to the domain server
            async with (
                aiohttp.ClientSession() as session,
                session.get(
                    domain_server, timeout=aiohttp.ClientTimeout(total=10)
                ) as response,
            ):
                response_time = time.time() - start_time

                if response.status in [200, 404]:  # 404 is OK for MCP servers
                    return skill_name, True, response_time, None
                else:
                    return skill_name, False, response_time, f"HTTP {response.status}"

        except asyncio.TimeoutError:
            response_time = time.time() - start_time
            return skill_name, False, response_time, "Timeout"
        except Exception as e:
            response_time = time.time() - start_time
            return skill_name, False, response_time, str(e)

    async def health_check_all_skills(self) -> Dict[str, Any]:
        """Perform health checks on all skills concurrently."""
        logger.info("Starting health checks on all skills")

        if not self.skills:
            logger.warning("No skills to check")
            return {}

        # Create tasks for all skills
        tasks = [self.health_check_skill(skill) for skill in self.skills]

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        health_report = {
            "total_skills": len(self.skills),
            "healthy_skills": 0,
            "failed_skills": 0,
            "skills": {},
            "by_domain": {},
        }

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Handle exceptions from gather
                skill_name = self.skills[i].get("name", "unknown")
                health_report["skills"][skill_name] = {
                    "healthy": False,
                    "response_time": 0.0,
                    "error": str(result),
                }
                health_report["failed_skills"] += 1
            else:
                skill_name, is_healthy, response_time, error = result
                health_report["skills"][skill_name] = {
                    "healthy": is_healthy,
                    "response_time": response_time,
                    "error": error,
                }

                if is_healthy:
                    health_report["healthy_skills"] += 1
                else:
                    health_report["failed_skills"] += 1

        # Categorize by domain
        categorized = self.categorize_skills()
        for domain, skills in categorized.items():
            domain_healthy = 0
            domain_failed = 0
            domain_avg_time = 0.0

            for skill in skills:
                skill_name = skill.get("name")
                skill_result = health_report["skills"].get(skill_name, {})

                if skill_result.get("healthy"):
                    domain_healthy += 1
                else:
                    domain_failed += 1

                domain_avg_time += skill_result.get("response_time", 0.0)

            if len(skills) > 0:
                domain_avg_time /= len(skills)

            health_report["by_domain"][domain] = {
                "total": len(skills),
                "healthy": domain_healthy,
                "failed": domain_failed,
                "avg_response_time": domain_avg_time,
            }

        return health_report


class ReportGenerator:
    """Generate comprehensive reports from health check results."""

    @staticmethod
    def generate_console_report(health_report: Dict[str, Any]):
        """Generate console-friendly report."""
        print("\n" + "=" * 80)
        print("MCP SKILL HEALTH CHECK REPORT")
        print("=" * 80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Summary
        total = health_report["total_skills"]
        healthy = health_report["healthy_skills"]
        failed = health_report["failed_skills"]
        success_rate = (healthy / total * 100) if total > 0 else 0

        print("SUMMARY")
        print("-" * 40)
        print(f"Total Skills:     {total}")
        print(f"Healthy Skills:   {healthy}")
        print(f"Failed Skills:    {failed}")
        print(f"Success Rate:     {success_rate:.1f}%")
        print()

        # By Domain
        print("BY DOMAIN")
        print("-" * 40)
        for domain, stats in health_report["by_domain"].items():
            rate = (
                (stats["healthy"] / stats["total"] * 100) if stats["total"] > 0 else 0
            )
            print(
                f"{domain:20} | {stats['healthy']:3}/{stats['total']:3} | {rate:5.1f}% | {stats['avg_response_time']:.3f}s"
            )
        print()

        # Failed Skills
        if failed > 0:
            print("FAILED SKILLS")
            print("-" * 40)
            for skill_name, result in health_report["skills"].items():
                if not result["healthy"]:
                    error = result["error"] or "Unknown error"
                    print(f"{skill_name:40} | {error}")
            print()

        # Recommendations
        print("RECOMMENDATIONS")
        print("-" * 40)
        if failed > 0:
            print("• Check network connectivity to domain servers")
            print("• Verify domain servers are running and accessible")
            print("• Review failed skills for configuration issues")
        else:
            print("• All skills are responding successfully!")
            print("• Consider monitoring response times for performance optimization")
        print()

    @staticmethod
    def generate_detailed_report(
        health_report: Dict[str, Any], filename: str = "mcp_health_report.json"
    ):
        """Generate detailed JSON report."""
        with open(filename, "w") as f:
            json.dump(health_report, f, indent=2)
        logger.info(f"Detailed report saved to {filename}")


async def main():
    """Main execution function."""
    print("Skill Flywheel MCP Client")
    print("=" * 50)

    # Initialize client
    client = MCPClient()

    # Step 1: Initialize connection
    print("Step 1: Initializing MCP connection...")
    if not await client.initialize():
        print("❌ Failed to initialize MCP connection")
        sys.exit(1)
    print("✅ MCP connection initialized successfully")

    # Step 2: List skills
    print("\nStep 2: Fetching skill list...")
    skills = await client.list_skills()
    if not skills:
        print("❌ No skills found or failed to fetch skills")
        sys.exit(1)
    print(f"✅ Found {len(skills)} skills")

    # Step 3: Health checks
    print(f"\nStep 3: Performing health checks on {len(skills)} skills...")
    print("This may take a few minutes...")

    start_time = time.time()
    health_report = await client.health_check_all_skills()
    total_time = time.time() - start_time

    print(f"✅ Health checks completed in {total_time:.2f} seconds")

    # Step 4: Generate reports
    print("\nStep 4: Generating reports...")
    ReportGenerator.generate_console_report(health_report)
    ReportGenerator.generate_detailed_report(health_report)

    # Final summary
    healthy = health_report["healthy_skills"]
    total = health_report["total_skills"]
    success_rate = (healthy / total * 100) if total > 0 else 0

    print("FINAL SUMMARY")
    print("=" * 50)
    if success_rate >= 90:
        print(
            f"🎉 Excellent! {healthy}/{total} skills ({success_rate:.1f}%) are healthy"
        )
    elif success_rate >= 75:
        print(
            f"⚠️  Good, but needs attention. {healthy}/{total} skills ({success_rate:.1f}%) are healthy"
        )
    else:
        print(
            f"🚨 Critical issues detected. Only {healthy}/{total} skills ({success_rate:.1f}%) are healthy"
        )

    print("\nReport generation complete!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
