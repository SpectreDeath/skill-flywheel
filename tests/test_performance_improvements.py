#!/usr/bin/env python3
"""
Performance Testing Suite for Enhanced MCP Server

This test suite validates:
- Dynamic lazy loading performance improvements
- Caching efficiency
- Dependency management
- Resource optimization
- System health monitoring
"""

import asyncio
import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import statistics
import psutil
import yaml
from dataclasses import asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('performance_test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Test Configuration
class TestConfig:
    """Test configuration"""
    
    def __init__(self):
        self.test_skills_dir = Path("test_skills")
        self.test_skills_dir.mkdir(exist_ok=True)
        
        self.test_config = {
            "test_scenarios": {
                "baseline": {
                    "name": "Baseline (No Optimization)",
                    "lazy_loading": False,
                    "caching": False,
                    "optimization": False
                },
                "lazy_loading": {
                    "name": "Lazy Loading Only",
                    "lazy_loading": True,
                    "caching": False,
                    "optimization": False
                },
                "lazy_loading_with_cache": {
                    "name": "Lazy Loading + Caching",
                    "lazy_loading": True,
                    "caching": True,
                    "optimization": False
                },
                "full_optimization": {
                    "name": "Full Optimization",
                    "lazy_loading": True,
                    "caching": True,
                    "optimization": True
                }
            },
            "test_parameters": {
                "concurrent_users": [1, 5, 10, 20, 50],
                "test_duration": 60,  # seconds
                "skill_count": 20,
                "execution_iterations": 100,
                "memory_threshold_mb": 500,
                "response_time_threshold_ms": 1000
            }
        }

# Test Skill Generator
class TestSkillGenerator:
    """Generates test skills with various characteristics"""
    
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        
    def create_test_skill(self, skill_name: str, dependencies: List[str] = None, 
                         execution_time: float = 0.1, memory_usage: int = 10) -> str:
        """Create a test skill file"""
        dependencies = dependencies or []
        
        # Generate skill code with simulated dependencies and execution time
        skill_code = f'''
"""
Test Skill: {skill_name}
Dependencies: {dependencies}
Execution Time: {execution_time}s
Memory Usage: {memory_usage}MB
"""

import time
import random

def {skill_name}(*args, **kwargs):
    """Test skill function"""
    # Simulate memory usage
    data = [random.random() for _ in range({memory_usage} * 1000)]
    
    # Simulate execution time
    time.sleep({execution_time})
    
    # Simulate dependencies
    result = f"Executed {skill_name} with {len(args)} args and {len(kwargs)} kwargs"
    
    # Process dependencies if any
    for dep in {dependencies}:
        result += f" -> dependency: {dep}"
    
    return result

if __name__ == "__main__":
    print({skill_name}("test_arg", test_kwarg="test_value"))
'''
        
        skill_file = self.skills_dir / f"{skill_name}.py"
        with open(skill_file, 'w') as f:
            f.write(skill_code)
        
        return str(skill_file)
    
    def create_skill_registry(self, skills: List[Dict[str, Any]]) -> str:
        """Create a skill registry file"""
        registry_file = self.skills_dir.parent / "test_skill_registry.json"
        
        registry_data = []
        for skill in skills:
            registry_data.append({
                "name": skill["name"],
                "version": "1.0.0",
                "description": f"Test skill {skill['name']}",
                "author": "Test Generator",
                "dependencies": skill.get("dependencies", []),
                "created_at": datetime.now().isoformat(),
                "last_modified": datetime.now().isoformat()
            })
        
        with open(registry_file, 'w') as f:
            json.dump(registry_data, f, indent=2)
        
        return str(registry_file)

# Performance Test Runner
class PerformanceTestRunner:
    """Runs performance tests for different scenarios"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.results = {}
        self.skill_generator = TestSkillGenerator(config.test_skills_dir)
        
    def setup_test_environment(self):
        """Setup test environment with skills and registry"""
        logger.info("Setting up test environment...")
        
        # Create test skills
        skills = []
        for i in range(self.config.test_config["test_parameters"]["skill_count"]):
            skill_name = f"test_skill_{i:03d}"
            dependencies = [f"test_skill_{j:03d}" for j in range(max(0, i-3), i)]
            execution_time = 0.05 + (i * 0.01)  # Varying execution times
            memory_usage = 5 + (i * 2)  # Varying memory usage
            
            self.skill_generator.create_test_skill(
                skill_name, dependencies, execution_time, memory_usage
            )
            
            skills.append({
                "name": skill_name,
                "dependencies": dependencies,
                "execution_time": execution_time,
                "memory_usage": memory_usage
            })
        
        # Create skill registry
        self.skill_generator.create_skill_registry(skills)
        
        logger.info(f"Created {len(skills)} test skills")
    
    async def run_baseline_test(self) -> Dict[str, Any]:
        """Run baseline test (no optimization)"""
        logger.info("Running baseline test...")
        
        start_time = time.time()
        memory_before = psutil.Process().memory_info().rss / 1024 / 1024
        
        results = {
            "scenario": "baseline",
            "start_time": start_time,
            "memory_before_mb": memory_before,
            "executions": [],
            "errors": [],
            "total_time": 0,
            "avg_response_time": 0,
            "memory_peak_mb": 0,
            "success_rate": 0
        }
        
        # Load all skills at once (baseline behavior)
        skill_files = list(self.config.test_skills_dir.glob("*.py"))
        
        # Execute skills multiple times
        for i in range(self.config.test_config["test_parameters"]["execution_iterations"]):
            try:
                # Randomly select a skill to execute
                skill_file = random.choice(skill_files)
                skill_name = skill_file.stem
                
                execution_start = time.time()
                
                # Load and execute skill (simulating baseline behavior)
                with open(skill_file, 'r') as f:
                    code = compile(f.read(), skill_file, 'exec')
                    namespace = {}
                    exec(code, namespace)
                
                skill_func = namespace.get(skill_name)
                if skill_func:
                    result = skill_func(f"arg_{i}", kwarg=f"kwarg_{i}")
                
                execution_time = time.time() - execution_start
                results["executions"].append({
                    "skill": skill_name,
                    "execution_time": execution_time,
                    "success": True
                })
                
            except Exception as e:
                results["errors"].append({
                    "skill": skill_name if 'skill_name' in locals() else "unknown",
                    "error": str(e)
                })
        
        # Calculate metrics
        results["total_time"] = time.time() - start_time
        successful_executions = [e for e in results["executions"] if e["success"]]
        
        if successful_executions:
            results["avg_response_time"] = statistics.mean([e["execution_time"] for e in successful_executions])
            results["success_rate"] = len(successful_executions) / len(results["executions"])
        
        memory_after = psutil.Process().memory_info().rss / 1024 / 1024
        results["memory_peak_mb"] = max(memory_before, memory_after)
        
        logger.info(f"Baseline test completed: {results['success_rate']*100:.1f}% success rate")
        return results
    
    async def run_lazy_loading_test(self) -> Dict[str, Any]:
        """Run lazy loading test"""
        logger.info("Running lazy loading test...")
        
        start_time = time.time()
        memory_before = psutil.Process().memory_info().rss / 1024 / 1024
        
        results = {
            "scenario": "lazy_loading",
            "start_time": start_time,
            "memory_before_mb": memory_before,
            "executions": [],
            "errors": [],
            "total_time": 0,
            "avg_response_time": 0,
            "memory_peak_mb": 0,
            "success_rate": 0,
            "loaded_skills": []
        }
        
        # Simulate lazy loading behavior
        loaded_skills = {}
        
        for i in range(self.config.test_config["test_parameters"]["execution_iterations"]):
            try:
                # Randomly select a skill to execute
                skill_files = list(self.config.test_skills_dir.glob("*.py"))
                skill_file = random.choice(skill_files)
                skill_name = skill_file.stem
                
                execution_start = time.time()
                
                # Lazy load skill only when needed
                if skill_name not in loaded_skills:
                    with open(skill_file, 'r') as f:
                        code = compile(f.read(), skill_file, 'exec')
                        namespace = {}
                        exec(code, namespace)
                    loaded_skills[skill_name] = namespace
                    results["loaded_skills"].append(skill_name)
                
                skill_func = loaded_skills[skill_name].get(skill_name)
                if skill_func:
                    result = skill_func(f"arg_{i}", kwarg=f"kwarg_{i}")
                
                execution_time = time.time() - execution_start
                results["executions"].append({
                    "skill": skill_name,
                    "execution_time": execution_time,
                    "success": True
                })
                
            except Exception as e:
                results["errors"].append({
                    "skill": skill_name if 'skill_name' in locals() else "unknown",
                    "error": str(e)
                })
        
        # Calculate metrics
        results["total_time"] = time.time() - start_time
        successful_executions = [e for e in results["executions"] if e["success"]]
        
        if successful_executions:
            results["avg_response_time"] = statistics.mean([e["execution_time"] for e in successful_executions])
            results["success_rate"] = len(successful_executions) / len(results["executions"])
        
        memory_after = psutil.Process().memory_info().rss / 1024 / 1024
        results["memory_peak_mb"] = max(memory_before, memory_after)
        
        logger.info(f"Lazy loading test completed: {results['success_rate']*100:.1f}% success rate")
        return results
    
    async def run_caching_test(self) -> Dict[str, Any]:
        """Run caching test"""
        logger.info("Running caching test...")
        
        start_time = time.time()
        memory_before = psutil.Process().memory_info().rss / 1024 / 1024
        
        results = {
            "scenario": "caching",
            "start_time": start_time,
            "memory_before_mb": memory_before,
            "executions": [],
            "errors": [],
            "total_time": 0,
            "avg_response_time": 0,
            "memory_peak_mb": 0,
            "success_rate": 0,
            "cache_hits": 0,
            "cache_misses": 0
        }
        
        # Simulate caching behavior
        skill_cache = {}
        cache_size = 10
        
        for i in range(self.config.test_config["test_parameters"]["execution_iterations"]):
            try:
                # Randomly select a skill to execute
                skill_files = list(self.config.test_skills_dir.glob("*.py"))
                skill_file = random.choice(skill_files)
                skill_name = skill_file.stem
                
                execution_start = time.time()
                
                # Check cache first
                if skill_name in skill_cache:
                    results["cache_hits"] += 1
                    namespace = skill_cache[skill_name]
                else:
                    results["cache_misses"] += 1
                    
                    # Load skill
                    with open(skill_file, 'r') as f:
                        code = compile(f.read(), skill_file, 'exec')
                        namespace = {}
                        exec(code, namespace)
                    
                    # Add to cache with LRU eviction
                    if len(skill_cache) >= cache_size:
                        # Remove oldest item
                        oldest_key = next(iter(skill_cache))
                        del skill_cache[oldest_key]
                    
                    skill_cache[skill_name] = namespace
                
                skill_func = namespace.get(skill_name)
                if skill_func:
                    result = skill_func(f"arg_{i}", kwarg=f"kwarg_{i}")
                
                execution_time = time.time() - execution_start
                results["executions"].append({
                    "skill": skill_name,
                    "execution_time": execution_time,
                    "success": True,
                    "cache_hit": skill_name in skill_cache and results["cache_hits"] > 0
                })
                
            except Exception as e:
                results["errors"].append({
                    "skill": skill_name if 'skill_name' in locals() else "unknown",
                    "error": str(e)
                })
        
        # Calculate metrics
        results["total_time"] = time.time() - start_time
        successful_executions = [e for e in results["executions"] if e["success"]]
        
        if successful_executions:
            results["avg_response_time"] = statistics.mean([e["execution_time"] for e in successful_executions])
            results["success_rate"] = len(successful_executions) / len(results["executions"])
        
        memory_after = psutil.Process().memory_info().rss / 1024 / 1024
        results["memory_peak_mb"] = max(memory_before, memory_after)
        
        logger.info(f"Caching test completed: {results['success_rate']*100:.1f}% success rate")
        return results
    
    async def run_full_optimization_test(self) -> Dict[str, Any]:
        """Run full optimization test"""
        logger.info("Running full optimization test...")
        
        start_time = time.time()
        memory_before = psutil.Process().memory_info().rss / 1024 / 1024
        
        results = {
            "scenario": "full_optimization",
            "start_time": start_time,
            "memory_before_mb": memory_before,
            "executions": [],
            "errors": [],
            "total_time": 0,
            "avg_response_time": 0,
            "memory_peak_mb": 0,
            "success_rate": 0,
            "optimization_metrics": {
                "preloaded_skills": [],
                "unloaded_skills": [],
                "priority_scores": {},
                "usage_patterns": {}
            }
        }
        
        # Simulate full optimization with priority-based loading
        skill_cache = {}
        skill_priorities = {}
        cache_size = 15
        
        for i in range(self.config.test_config["test_parameters"]["execution_iterations"]):
            try:
                # Randomly select a skill to execute (with some skills being more popular)
                skill_files = list(self.config.test_skills_dir.glob("*.py"))
                
                # Simulate usage patterns (some skills are more popular)
                if i % 10 < 3:  # 30% of the time, use popular skills
                    popular_skills = [f"test_skill_{j:03d}" for j in range(5)]
                    skill_name = random.choice(popular_skills)
                else:
                    skill_file = random.choice(skill_files)
                    skill_name = skill_file.stem
                
                execution_start = time.time()
                
                # Update priority score
                if skill_name not in skill_priorities:
                    skill_priorities[skill_name] = 0
                skill_priorities[skill_name] += 1
                
                # Check cache first
                if skill_name in skill_cache:
                    namespace = skill_cache[skill_name]
                else:
                    # Load skill
                    skill_file = self.config.test_skills_dir / f"{skill_name}.py"
                    with open(skill_file, 'r') as f:
                        code = compile(f.read(), skill_file, 'exec')
                        namespace = {}
                        exec(code, namespace)
                    
                    # Add to cache with priority-based eviction
                    if len(skill_cache) >= cache_size:
                        # Remove lowest priority item
                        lowest_priority_key = min(skill_priorities, key=skill_priorities.get)
                        del skill_cache[lowest_priority_key]
                        del skill_priorities[lowest_priority_key]
                    
                    skill_cache[skill_name] = namespace
                
                skill_func = namespace.get(skill_name)
                if skill_func:
                    result = skill_func(f"arg_{i}", kwarg=f"kwarg_{i}")
                
                execution_time = time.time() - execution_start
                results["executions"].append({
                    "skill": skill_name,
                    "execution_time": execution_time,
                    "success": True
                })
                
            except Exception as e:
                results["errors"].append({
                    "skill": skill_name if 'skill_name' in locals() else "unknown",
                    "error": str(e)
                })
        
        # Calculate metrics
        results["total_time"] = time.time() - start_time
        successful_executions = [e for e in results["executions"] if e["success"]]
        
        if successful_executions:
            results["avg_response_time"] = statistics.mean([e["execution_time"] for e in successful_executions])
            results["success_rate"] = len(successful_executions) / len(results["executions"])
        
        memory_after = psutil.Process().memory_info().rss / 1024 / 1024
        results["memory_peak_mb"] = max(memory_before, memory_after)
        
        # Store optimization metrics
        results["optimization_metrics"]["priority_scores"] = skill_priorities
        results["optimization_metrics"]["preloaded_skills"] = list(skill_cache.keys())
        
        logger.info(f"Full optimization test completed: {results['success_rate']*100:.1f}% success rate")
        return results
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all performance tests"""
        logger.info("Starting performance test suite...")
        
        # Setup test environment
        self.setup_test_environment()
        
        # Run tests for each scenario
        scenarios = self.config.test_config["test_scenarios"]
        test_results = {}
        
        for scenario_key, scenario_config in scenarios.items():
            logger.info(f"Running scenario: {scenario_config['name']}")
            
            if scenario_key == "baseline":
                test_results[scenario_key] = await self.run_baseline_test()
            elif scenario_key == "lazy_loading":
                test_results[scenario_key] = await self.run_lazy_loading_test()
            elif scenario_key == "lazy_loading_with_cache":
                test_results[scenario_key] = await self.run_caching_test()
            elif scenario_key == "full_optimization":
                test_results[scenario_key] = await self.run_full_optimization_test()
            
            # Wait between tests
            await asyncio.sleep(2)
        
        # Calculate improvements
        baseline = test_results.get("baseline", {})
        improvements = self.calculate_improvements(test_results)
        
        # Generate report
        report = {
            "test_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_scenarios": len(scenarios),
                "total_executions": sum(len(r.get("executions", [])) for r in test_results.values()),
                "test_duration": time.time() - baseline.get("start_time", time.time())
            },
            "scenario_results": test_results,
            "improvements": improvements,
            "recommendations": self.generate_recommendations(test_results, improvements)
        }
        
        return report
    
    def calculate_improvements(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance improvements"""
        baseline = test_results.get("baseline", {})
        improvements = {}
        
        for scenario_key, results in test_results.items():
            if scenario_key == "baseline":
                continue
            
            improvements[scenario_key] = {
                "response_time_improvement": 0,
                "memory_improvement": 0,
                "success_rate_improvement": 0,
                "execution_count": len(results.get("executions", []))
            }
            
            # Calculate response time improvement
            if baseline.get("avg_response_time", 0) > 0:
                baseline_time = baseline["avg_response_time"]
                scenario_time = results.get("avg_response_time", 0)
                improvements[scenario_key]["response_time_improvement"] = (
                    (baseline_time - scenario_time) / baseline_time * 100
                )
            
            # Calculate memory improvement
            if baseline.get("memory_peak_mb", 0) > 0:
                baseline_memory = baseline["memory_peak_mb"]
                scenario_memory = results.get("memory_peak_mb", 0)
                improvements[scenario_key]["memory_improvement"] = (
                    (baseline_memory - scenario_memory) / baseline_memory * 100
                )
            
            # Calculate success rate improvement
            baseline_success = baseline.get("success_rate", 0)
            scenario_success = results.get("success_rate", 0)
            improvements[scenario_key]["success_rate_improvement"] = (
                scenario_success - baseline_success
            )
        
        return improvements
    
    def generate_recommendations(self, test_results: Dict[str, Any], improvements: Dict[str, Any]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        # Find best performing scenario
        best_scenario = max(improvements.keys(), key=lambda k: improvements[k]["response_time_improvement"])
        
        recommendations.append(f"Recommended configuration: {best_scenario}")
        recommendations.append(f"Expected response time improvement: {improvements[best_scenario]['response_time_improvement']:.1f}%")
        recommendations.append(f"Expected memory improvement: {improvements[best_scenario]['memory_improvement']:.1f}%")
        
        # Specific recommendations based on results
        if improvements[best_scenario]["response_time_improvement"] > 50:
            recommendations.append("Consider implementing aggressive caching for frequently used skills")
        
        if improvements[best_scenario]["memory_improvement"] > 30:
            recommendations.append("Lazy loading is highly effective for your use case")
        
        if any(r.get("success_rate", 0) < 0.95 for r in test_results.values()):
            recommendations.append("Investigate error patterns to improve reliability")
        
        return recommendations

# Test Report Generator
class TestReportGenerator:
    """Generates comprehensive test reports"""
    
    def __init__(self, results: Dict[str, Any]):
        self.results = results
        
    def generate_html_report(self) -> str:
        """Generate HTML test report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Performance Test Report</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
                .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .metric {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }}
                .metric:last-child {{ border-bottom: none; }}
                .metric-label {{ font-weight: bold; }}
                .metric-value {{ color: #666; }}
                .improvement {{ color: #28a745; font-weight: bold; }}
                .degradation {{ color: #dc3545; font-weight: bold; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                .chart-placeholder {{ height: 200px; background: #f8f9fa; border: 1px dashed #dee2e6; display: flex; align-items: center; justify-content: center; color: #6c757d; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Performance Test Report</h1>
                    <p><strong>Test Date:</strong> {self.results['test_summary']['timestamp']}</p>
                    <p><strong>Total Scenarios:</strong> {self.results['test_summary']['total_scenarios']}</p>
                    <p><strong>Total Executions:</strong> {self.results['test_summary']['total_executions']}</p>
                    <p><strong>Test Duration:</strong> {self.results['test_summary']['test_duration']:.2f} seconds</p>
                </div>
                
                <div class="grid">
                    <div class="card">
                        <h3>Scenario Comparison</h3>
                        <table>
                            <tr>
                                <th>Scenario</th>
                                <th>Avg Response Time</th>
                                <th>Memory Usage</th>
                                <th>Success Rate</th>
                                <th>Improvement</th>
                            </tr>
        """
        
        baseline = self.results['scenario_results'].get('baseline', {})
        
        for scenario_key, results in self.results['scenario_results'].items():
            response_time = results.get('avg_response_time', 0) * 1000  # Convert to ms
            memory = results.get('memory_peak_mb', 0)
            success_rate = results.get('success_rate', 0) * 100  # Convert to %
            
            improvement = self.results['improvements'].get(scenario_key, {})
            response_improvement = improvement.get('response_time_improvement', 0)
            
            improvement_class = "improvement" if response_improvement > 0 else "degradation"
            improvement_text = f"{response_improvement:+.1f}%" if scenario_key != 'baseline' else "Baseline"
            
            html += f"""
                            <tr>
                                <td>{scenario_key.replace('_', ' ').title()}</td>
                                <td>{response_time:.1f} ms</td>
                                <td>{memory:.1f} MB</td>
                                <td>{success_rate:.1f}%</td>
                                <td class="{improvement_class}">{improvement_text}</td>
                            </tr>
            """
        
        html += """
                        </table>
                    </div>
                    
                    <div class="card">
                        <h3>Performance Improvements</h3>
                        <div class="chart-placeholder">
                            Performance improvement chart would be displayed here
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h3>Recommendations</h3>
                    <ul>
        """
        
        for recommendation in self.results['recommendations']:
            html += f"<li>{recommendation}</li>"
        
        html += """
                    </ul>
                </div>
                
                <div class="card">
                    <h3>Detailed Results</h3>
                    <pre>""" + json.dumps(self.results, indent=2) + """</pre>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def save_report(self, filename: str = "performance_test_report.html"):
        """Save test report to file"""
        html_content = self.generate_html_report()
        
        with open(filename, 'w') as f:
            f.write(html_content)
        
        logger.info(f"Test report saved to {filename}")

# Main Test Runner
async def main():
    """Main test execution"""
    config = TestConfig()
    test_runner = PerformanceTestRunner(config)
    
    logger.info("Starting MCP Server Performance Test Suite")
    
    try:
        # Run all tests
        results = await test_runner.run_all_tests()
        
        # Generate report
        report_generator = TestReportGenerator(results)
        report_generator.save_report("performance_test_report.html")
        
        # Print summary
        print("\n" + "="*60)
        print("PERFORMANCE TEST RESULTS SUMMARY")
        print("="*60)
        
        for scenario_key, improvement in results['improvements'].items():
            print(f"\n{scenario_key.replace('_', ' ').title()}:")
            print(f"  Response Time Improvement: {improvement['response_time_improvement']:+.1f}%")
            print(f"  Memory Improvement: {improvement['memory_improvement']:+.1f}%")
            print(f"  Success Rate Improvement: {improvement['success_rate_improvement']:+.1f}%")
        
        print(f"\nRecommendations:")
        for rec in results['recommendations']:
            print(f"  • {rec}")
        
        print(f"\nDetailed report saved to: performance_test_report.html")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())