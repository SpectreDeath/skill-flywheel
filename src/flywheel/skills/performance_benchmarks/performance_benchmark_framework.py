#!/usr/bin/env python3
"""
Performance Benchmark Framework Skill

This skill provides standardized benchmarking frameworks for consistent 
performance measurement across projects and teams. It enables systematic 
performance engineering practices that support data-driven optimization decisions.

Key Features:
- Standardized benchmarking frameworks
- Performance measurement consistency
- Baseline establishment and tracking
- Cross-project performance comparison
- Automated performance regression detection
"""

import asyncio
import datetime
import json
import logging
import statistics
import sys
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

import psutil

logger = logging.getLogger(__name__)

class BenchmarkType(Enum):
    MICRO = "micro"
    MACRO = "macro"
    LOAD = "load"
    STRESS = "stress"
    SOAK = "soak"

class MetricType(Enum):
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    RESOURCE_UTILIZATION = "resource_utilization"
    ERROR_RATE = "error_rate"

@dataclass
class BenchmarkResult:
    """Result of a benchmark execution"""
    name: str
    benchmark_type: BenchmarkType
    duration: float
    metrics: Dict[str, Any]
    environment: Dict[str, Any]
    timestamp: datetime.datetime
    success: bool
    error_message: str | None = None

@dataclass
class PerformanceBaseline:
    """Performance baseline for comparison"""
    name: str
    metrics: Dict[str, Dict[str, float]]  # metric_name -> {mean, std_dev, min, max}
    environment: Dict[str, Any]
    created_at: datetime.datetime

class PerformanceBenchmarkFramework:
    """Framework for standardized performance benchmarking"""
    
    def __init__(self, output_dir: str | None = None):
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "benchmark_results"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.baselines: Dict[str, PerformanceBaseline] = {}
        self.results: List[BenchmarkResult] = []
        
    def _get_system_info(self) -> Dict[str, Any]:
        """Collect system information for environment context"""
        try:
            return {
                "cpu_count": psutil.cpu_count(),
                "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available,
                "platform": sys.platform,
                "python_version": sys.version,
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            logger.warning(f"Failed to collect system info: {e}")
            return {"error": str(e)}
    
    def _measure_execution_time(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Measure execution time and resource usage of a function"""
        start_time = time.perf_counter()
        start_cpu = psutil.Process().cpu_percent()
        start_memory = psutil.Process().memory_info().rss
        
        try:
            result = func(*args, **kwargs)
            success = True
            error_msg = None
        except Exception as e:
            result = None
            success = False
            error_msg = str(e)
        
        end_time = time.perf_counter()
        end_cpu = psutil.Process().cpu_percent()
        end_memory = psutil.Process().memory_info().rss
        
        return {
            "execution_time": end_time - start_time,
            "cpu_usage": end_cpu - start_cpu,
            "memory_delta": end_memory - start_memory,
            "success": success,
            "error_message": error_msg,
            "result": result
        }
    
    async def _measure_async_execution_time(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Measure execution time and resource usage of an async function"""
        start_time = time.perf_counter()
        start_cpu = psutil.Process().cpu_percent()
        start_memory = psutil.Process().memory_info().rss
        
        try:
            result = await func(*args, **kwargs)
            success = True
            error_msg = None
        except Exception as e:
            result = None
            success = False
            error_msg = str(e)
        
        end_time = time.perf_counter()
        end_cpu = psutil.Process().cpu_percent()
        end_memory = psutil.Process().memory_info().rss
        
        return {
            "execution_time": end_time - start_time,
            "cpu_usage": end_cpu - start_cpu,
            "memory_delta": end_memory - start_memory,
            "success": success,
            "error_message": error_msg,
            "result": result
        }
    
    def _calculate_statistics(self, values: List[float]) -> Dict[str, float]:
        """Calculate statistical metrics for a list of values"""
        if not values:
            return {"count": 0, "mean": 0, "std_dev": 0, "min": 0, "max": 0}
        
        return {
            "count": len(values),
            "mean": statistics.mean(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values)
        }
    
    def create_micro_benchmark(self, name: str, func: Callable, iterations: int = 100) -> BenchmarkResult:
        """
        Create a micro-benchmark for isolated component performance
        
        Args:
            name: Benchmark name
            func: Function to benchmark
            iterations: Number of iterations to run
        
        Returns:
            Benchmark result
        """
        logger.info(f"Running micro-benchmark: {name}")
        
        execution_times = []
        memory_deltas = []
        errors = []
        
        for _i in range(iterations):
            measurement = self._measure_execution_time(func)
            
            if measurement["success"]:
                execution_times.append(measurement["execution_time"])
                memory_deltas.append(measurement["memory_delta"])
            else:
                errors.append(measurement["error_message"])
        
        # Calculate metrics
        time_stats = self._calculate_statistics(execution_times)
        memory_stats = self._calculate_statistics(memory_deltas)
        
        metrics = {
            "execution_time": time_stats,
            "memory_usage": memory_stats,
            "error_count": len(errors),
            "error_rate": len(errors) / iterations if iterations > 0 else 0
        }
        
        # Calculate percentiles
        if execution_times:
            execution_times.sort()
            percentiles = [50, 90, 95, 99]
            for p in percentiles:
                idx = int((p / 100) * (len(execution_times) - 1))
                metrics[f"p{p}_response_time"] = execution_times[idx]
        
        result = BenchmarkResult(
            name=name,
            benchmark_type=BenchmarkType.MICRO,
            duration=time.perf_counter(),
            metrics=metrics,
            environment=self._get_system_info(),
            timestamp=datetime.datetime.now(),
            success=len(errors) == 0,
            error_message=f"{len(errors)} errors out of {iterations} iterations" if errors else None
        )
        
        self.results.append(result)
        return result
    
    async def create_async_micro_benchmark(self, name: str, func: Callable, iterations: int = 100) -> BenchmarkResult:
        """
        Create a micro-benchmark for async functions
        
        Args:
            name: Benchmark name
            func: Async function to benchmark
            iterations: Number of iterations to run
        
        Returns:
            Benchmark result
        """
        logger.info(f"Running async micro-benchmark: {name}")
        
        execution_times = []
        memory_deltas = []
        errors = []
        
        for _i in range(iterations):
            measurement = await self._measure_async_execution_time(func)
            
            if measurement["success"]:
                execution_times.append(measurement["execution_time"])
                memory_deltas.append(measurement["memory_delta"])
            else:
                errors.append(measurement["error_message"])
        
        # Calculate metrics
        time_stats = self._calculate_statistics(execution_times)
        memory_stats = self._calculate_statistics(memory_deltas)
        
        metrics = {
            "execution_time": time_stats,
            "memory_usage": memory_stats,
            "error_count": len(errors),
            "error_rate": len(errors) / iterations if iterations > 0 else 0
        }
        
        # Calculate percentiles
        if execution_times:
            execution_times.sort()
            percentiles = [50, 90, 95, 99]
            for p in percentiles:
                idx = int((p / 100) * (len(execution_times) - 1))
                metrics[f"p{p}_response_time"] = execution_times[idx]
        
        result = BenchmarkResult(
            name=name,
            benchmark_type=BenchmarkType.MICRO,
            duration=time.perf_counter(),
            metrics=metrics,
            environment=self._get_system_info(),
            timestamp=datetime.datetime.now(),
            success=len(errors) == 0,
            error_message=f"{len(errors)} errors out of {iterations} iterations" if errors else None
        )
        
        self.results.append(result)
        return result
    
    def create_load_test(self, name: str, func: Callable, users: int, duration: float) -> BenchmarkResult:
        """
        Create a load test to measure performance under expected load
        
        Args:
            name: Benchmark name
            func: Function to test
            users: Number of concurrent users
            duration: Test duration in seconds
        
        Returns:
            Benchmark result
        """
        logger.info(f"Running load test: {name} with {users} users for {duration}s")
        
        start_time = time.time()
        results = []
        errors = []
        
        def worker():
            while time.time() - start_time < duration:
                try:
                    measurement = self._measure_execution_time(func)
                    results.append(measurement)
                except Exception as e:
                    errors.append(str(e))
        
        # Run concurrent workers
        import threading
        threads = []
        for _ in range(users):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Process results
        successful_results = [r for r in results if r["success"]]
        execution_times = [r["execution_time"] for r in successful_results]
        memory_deltas = [r["memory_delta"] for r in successful_results]
        
        time_stats = self._calculate_statistics(execution_times)
        memory_stats = self._calculate_statistics(memory_deltas)
        
        metrics = {
            "execution_time": time_stats,
            "memory_usage": memory_stats,
            "total_requests": len(results),
            "successful_requests": len(successful_results),
            "error_count": len(errors),
            "error_rate": len(errors) / len(results) if results else 0,
            "requests_per_second": len(successful_results) / duration if duration > 0 else 0
        }
        
        # Calculate percentiles
        if execution_times:
            execution_times.sort()
            percentiles = [50, 90, 95, 99]
            for p in percentiles:
                idx = int((p / 100) * (len(execution_times) - 1))
                metrics[f"p{p}_response_time"] = execution_times[idx]
        
        result = BenchmarkResult(
            name=name,
            benchmark_type=BenchmarkType.LOAD,
            duration=duration,
            metrics=metrics,
            environment=self._get_system_info(),
            timestamp=datetime.datetime.now(),
            success=len(errors) == 0,
            error_message=f"{len(errors)} errors out of {len(results)} requests" if errors else None
        )
        
        self.results.append(result)
        return result
    
    def establish_baseline(self, name: str, benchmark_result: BenchmarkResult) -> PerformanceBaseline:
        """
        Establish a performance baseline from benchmark results
        
        Args:
            name: Baseline name
            benchmark_result: Benchmark result to use as baseline
        
        Returns:
            Performance baseline
        """
        metrics = {}
        for metric_name, metric_data in benchmark_result.metrics.items():
            if isinstance(metric_data, dict) and "mean" in metric_data:
                metrics[metric_name] = {
                    "mean": metric_data["mean"],
                    "std_dev": metric_data["std_dev"],
                    "min": metric_data["min"],
                    "max": metric_data["max"]
                }
        
        baseline = PerformanceBaseline(
            name=name,
            metrics=metrics,
            environment=benchmark_result.environment,
            created_at=datetime.datetime.now()
        )
        
        self.baselines[name] = baseline
        return baseline
    
    def compare_with_baseline(self, baseline_name: str, benchmark_result: BenchmarkResult) -> Dict[str, Any]:
        """
        Compare benchmark results with a baseline
        
        Args:
            baseline_name: Name of the baseline to compare against
            benchmark_result: Benchmark result to compare
        
        Returns:
            Comparison analysis
        """
        if baseline_name not in self.baselines:
            raise ValueError(f"Baseline '{baseline_name}' not found")
        
        baseline = self.baselines[baseline_name]
        comparison = {
            "baseline_name": baseline_name,
            "benchmark_name": benchmark_result.name,
            "timestamp": datetime.datetime.now().isoformat(),
            "metric_comparisons": {}
        }
        
        for metric_name, baseline_metric in baseline.metrics.items():
            if metric_name in benchmark_result.metrics:
                benchmark_metric = benchmark_result.metrics[metric_name]
                
                if isinstance(baseline_metric, dict) and isinstance(benchmark_metric, dict):
                    # Compare statistical metrics
                    comparison["metric_comparisons"][metric_name] = {
                        "baseline_mean": baseline_metric["mean"],
                        "benchmark_mean": benchmark_metric["mean"],
                        "difference": benchmark_metric["mean"] - baseline_metric["mean"],
                        "percentage_change": ((benchmark_metric["mean"] - baseline_metric["mean"]) / baseline_metric["mean"]) * 100 if baseline_metric["mean"] != 0 else 0,
                        "regression_detected": benchmark_metric["mean"] > baseline_metric["mean"] * 1.1  # 10% degradation
                    }
        
        return comparison
    
    def save_results(self, filename: str | None = None) -> Path:
        """
        Save benchmark results to a JSON file
        
        Args:
            filename: Optional filename (defaults to timestamp-based name)
        
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        # Convert results to serializable format
        serializable_results = []
        for result in self.results:
            result_dict = asdict(result)
            result_dict["benchmark_type"] = result.benchmark_type.value
            result_dict["timestamp"] = result.timestamp.isoformat()
            serializable_results.append(result_dict)
        
        with open(filepath, 'w') as f:
            json.dump({
                "results": serializable_results,
                "baselines": {name: asdict(baseline) for name, baseline in self.baselines.items()}
            }, f, indent=2)
        
        logger.info(f"Results saved to {filepath}")
        return filepath
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive performance report
        
        Returns:
            Performance report
        """
        report = {
            "summary": {
                "total_benchmarks": len(self.results),
                "benchmark_types": list({r.benchmark_type.value for r in self.results}),
                "total_baselines": len(self.baselines),
                "report_generated": datetime.datetime.now().isoformat()
            },
            "benchmarks": [],
            "baselines": {name: asdict(baseline) for name, baseline in self.baselines.items()}
        }
        
        for result in self.results:
            benchmark_summary = {
                "name": result.name,
                "type": result.benchmark_type.value,
                "duration": result.duration,
                "success": result.success,
                "timestamp": result.timestamp.isoformat(),
                "key_metrics": {}
            }
            
            # Extract key metrics
            for metric_name, metric_data in result.metrics.items():
                if isinstance(metric_data, dict) and "mean" in metric_data:
                    benchmark_summary["key_metrics"][metric_name] = {
                        "mean": metric_data["mean"],
                        "std_dev": metric_data["std_dev"],
                        "min": metric_data["min"],
                        "max": metric_data["max"]
                    }
            
            report["benchmarks"].append(benchmark_summary)
        
        return report

def invoke(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for the performance benchmark framework skill
    
    Args:
        config: Configuration dictionary with the following structure:
            {
                "action": "create_micro_benchmark" | "create_load_test" | "establish_baseline" | "compare_with_baseline" | "save_results" | "generate_report",
                "parameters": {
                    # Action-specific parameters
                }
            }
    
    Returns:
        Result dictionary with success status and data
    """
    try:
        # Initialize framework
        framework = PerformanceBenchmarkFramework()
        
        action = config.get("action")
        parameters = config.get("parameters", {})
        
        if action == "create_micro_benchmark":
            # Parameters: name, func, iterations
            name = parameters["name"]
            iterations = parameters.get("iterations", 100)
            
            # For this example, we'll create a simple test function
            def test_function():
                return sum(range(1000))
            
            result = framework.create_micro_benchmark(name, test_function, iterations)
            
            return {
                "success": True,
                "message": f"Micro-benchmark '{name}' completed successfully",
                "result": {
                    "name": result.name,
                    "type": result.benchmark_type.value,
                    "duration": result.duration,
                    "metrics": result.metrics,
                    "success": result.success
                }
            }
        
        elif action == "create_async_micro_benchmark":
            # Parameters: name, async_func, iterations
            name = parameters["name"]
            iterations = parameters.get("iterations", 100)
            
            async def test_async_function():
                await asyncio.sleep(0.001)  # Simulate async work
                return sum(range(100))
            
            result = asyncio.run(framework.create_async_micro_benchmark(name, test_async_function, iterations))
            
            return {
                "success": True,
                "message": f"Async micro-benchmark '{name}' completed successfully",
                "result": {
                    "name": result.name,
                    "type": result.benchmark_type.value,
                    "duration": result.duration,
                    "metrics": result.metrics,
                    "success": result.success
                }
            }
        
        elif action == "create_load_test":
            # Parameters: name, func, users, duration
            name = parameters["name"]
            users = parameters["users"]
            duration = parameters["duration"]
            
            def test_function():
                return sum(range(100))
            
            result = framework.create_load_test(name, test_function, users, duration)
            
            return {
                "success": True,
                "message": f"Load test '{name}' completed successfully",
                "result": {
                    "name": result.name,
                    "type": result.benchmark_type.value,
                    "duration": result.duration,
                    "metrics": result.metrics,
                    "success": result.success
                }
            }
        
        elif action == "establish_baseline":
            # Parameters: name, benchmark_result
            name = parameters["name"]
            benchmark_data = parameters["benchmark_result"]
            
            # Reconstruct benchmark result
            benchmark_result = BenchmarkResult(
                name=benchmark_data["name"],
                benchmark_type=BenchmarkType(benchmark_data["benchmark_type"]),
                duration=benchmark_data["duration"],
                metrics=benchmark_data["metrics"],
                environment=benchmark_data["environment"],
                timestamp=datetime.datetime.fromisoformat(benchmark_data["timestamp"]),
                success=benchmark_data["success"],
                error_message=benchmark_data.get("error_message")
            )
            
            baseline = framework.establish_baseline(name, benchmark_result)
            
            return {
                "success": True,
                "message": f"Baseline '{name}' established successfully",
                "result": {
                    "name": baseline.name,
                    "metrics": baseline.metrics,
                    "created_at": baseline.created_at.isoformat()
                }
            }
        
        elif action == "compare_with_baseline":
            # Parameters: baseline_name, benchmark_result
            baseline_name = parameters["baseline_name"]
            benchmark_data = parameters["benchmark_result"]
            
            # Reconstruct benchmark result
            benchmark_result = BenchmarkResult(
                name=benchmark_data["name"],
                benchmark_type=BenchmarkType(benchmark_data["benchmark_type"]),
                duration=benchmark_data["duration"],
                metrics=benchmark_data["metrics"],
                environment=benchmark_data["environment"],
                timestamp=datetime.datetime.fromisoformat(benchmark_data["timestamp"]),
                success=benchmark_data["success"],
                error_message=benchmark_data.get("error_message")
            )
            
            comparison = framework.compare_with_baseline(baseline_name, benchmark_result)
            
            return {
                "success": True,
                "message": f"Comparison with baseline '{baseline_name}' completed",
                "result": comparison
            }
        
        elif action == "save_results":
            # Parameters: filename (optional)
            filename = parameters.get("filename")
            filepath = framework.save_results(filename)
            
            return {
                "success": True,
                "message": f"Results saved to {filepath}",
                "result": {
                    "filepath": str(filepath)
                }
            }
        
        elif action == "generate_report":
            report = framework.generate_report()
            
            return {
                "success": True,
                "message": "Performance report generated successfully",
                "result": report
            }
        
        else:
            return {
                "success": False,
                "message": f"Unknown action: {action}",
                "error": "Invalid action specified"
            }
    
    except Exception as e:
        logger.error(f"Error in performance benchmark framework: {e}")
        return {
            "success": False,
            "message": f"Error executing performance benchmark framework: {str(e)}",
            "error": str(e)
        }

if __name__ == "__main__":
    # Example usage
    example_config = {
        "action": "create_micro_benchmark",
        "parameters": {
            "name": "example_benchmark",
            "iterations": 10
        }
    }
    
    result = invoke(example_config)
    print(json.dumps(result, indent=2))
