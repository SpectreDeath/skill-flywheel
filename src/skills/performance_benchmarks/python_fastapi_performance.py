#!/usr/bin/env python3
"""
Python FastAPI Performance Optimization Skill

This skill provides high-throughput optimization for Python FastAPI applications,
focusing on async performance, database optimization, caching strategies, and
concurrency patterns for maximum throughput.

Key Features:
- FastAPI async performance optimization
- Database query optimization
- Caching strategy implementation
- Concurrency pattern analysis
- Memory usage optimization
- Response time reduction techniques
"""

import time
import datetime
import logging
import json
import asyncio
import statistics
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import psutil
import sys

logger = logging.getLogger(__name__)

@dataclass
class FastAPIPerformanceMetrics:
    """Performance metrics for FastAPI application"""
    request_count: int
    avg_response_time: float
    p95_response_time: float
    p99_response_time: float
    error_rate: float
    throughput_rps: float
    memory_usage_mb: float
    cpu_usage_percent: float
    active_connections: int
    database_query_count: int
    cache_hit_rate: float
    timestamp: datetime.datetime

@dataclass
class OptimizationSuggestion:
    """Optimization suggestion for FastAPI"""
    category: str
    severity: str  # low, medium, high, critical
    issue: str
    suggestion: str
    expected_improvement: str
    implementation_effort: str

class FastAPIPerformanceOptimizer:
    """Optimizer for FastAPI application performance"""
    
    def __init__(self, app_process: Optional[psutil.Process] = None):
        self.app_process = app_process
        self.metrics_history: List[FastAPIPerformanceMetrics] = []
        self.request_times: List[float] = []
        self.error_count: int = 0
        self.total_requests: int = 0
    
    def _get_app_process(self) -> Optional[psutil.Process]:
        """Find FastAPI application process"""
        if self.app_process and self.app_process.is_running():
            return self.app_process
        
        # Try to find Python processes that might be FastAPI
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = proc.info.get('cmdline', [])
                    if cmdline and any('uvicorn' in cmd or 'gunicorn' in cmd or 'fastapi' in cmd.lower() for cmd in cmdline):
                        self.app_process = proc
                        return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return None
    
    def measure_response_time(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Measure response time of a function"""
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            success = True
            error_msg = None
        except Exception as e:
            result = None
            success = False
            error_msg = str(e)
        
        end_time = time.perf_counter()
        response_time = (end_time - start_time) * 1000  # Convert to ms
        
        return {
            "response_time": response_time,
            "success": success,
            "error_message": error_msg,
            "result": result
        }
    
    async def measure_async_response_time(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Measure response time of an async function"""
        start_time = time.perf_counter()
        
        try:
            result = await func(*args, **kwargs)
            success = True
            error_msg = None
        except Exception as e:
            result = None
            success = False
            error_msg = str(e)
        
        end_time = time.perf_counter()
        response_time = (end_time - start_time) * 1000  # Convert to ms
        
        return {
            "response_time": response_time,
            "success": success,
            "error_message": error_msg,
            "result": result
        }
    
    def analyze_database_queries(self, query_times: List[float]) -> Dict[str, Any]:
        """Analyze database query performance"""
        if not query_times:
            return {"error": "No query data available"}
        
        stats = {
            "total_queries": len(query_times),
            "avg_query_time": statistics.mean(query_times),
            "max_query_time": max(query_times),
            "min_query_time": min(query_times),
            "slow_queries": len([q for q in query_times if q > 100])  # > 100ms
        }
        
        # Calculate percentiles
        query_times_sorted = sorted(query_times)
        if len(query_times_sorted) > 0:
            stats.update({
                "p50_query_time": query_times_sorted[len(query_times_sorted) // 2],
                "p95_query_time": query_times_sorted[int(0.95 * len(query_times_sorted))],
                "p99_query_time": query_times_sorted[int(0.99 * len(query_times_sorted))]
            })
        
        return stats
    
    def analyze_memory_usage(self) -> Dict[str, float]:
        """Analyze memory usage patterns"""
        if not self._get_app_process():
            return {"error": "No FastAPI process found"}
        
        try:
            process = self.app_process
            memory_info = process.memory_info()
            memory_percent = process.memory_percent()
            
            return {
                "rss": memory_info.rss / (1024 * 1024),  # MB
                "vms": memory_info.vms / (1024 * 1024),  # MB
                "percent": memory_percent,
                "available": psutil.virtual_memory().available / (1024 * 1024 * 1024)  # GB
            }
        except Exception as e:
            logger.error(f"Error analyzing memory usage: {e}")
            return {"error": str(e)}
    
    def analyze_concurrency_patterns(self) -> Dict[str, Any]:
        """Analyze concurrency and async patterns"""
        # This would require detailed profiling of the FastAPI app
        # For now, return basic process info
        return {
            "active_threads": self.app_process.num_threads() if self.app_process else 0,
            "async_tasks": 0,  # Would need asyncio introspection
            "connection_pool_size": 0,  # Would need database connection analysis
            "worker_processes": 1  # Would need gunicorn/uvicorn config analysis
        }
    
    def simulate_load_test(self, endpoint_func: Callable, users: int, duration: float) -> FastAPIPerformanceMetrics:
        """Simulate load test on an endpoint"""
        logger.info(f"Running load test with {users} users for {duration}s")
        
        start_time = time.time()
        results = []
        errors = []
        
        async def worker():
            while time.time() - start_time < duration:
                try:
                    measurement = await self.measure_async_response_time(endpoint_func)
                    results.append(measurement)
                except Exception as e:
                    errors.append(str(e))
        
        # Run concurrent workers
        async def run_workers():
            tasks = [worker() for _ in range(users)]
            await asyncio.gather(*tasks)
        
        asyncio.run(run_workers())
        
        # Process results
        successful_results = [r for r in results if r["success"]]
        response_times = [r["response_time"] for r in successful_results]
        
        # Calculate metrics
        if response_times:
            response_stats = {
                "mean": statistics.mean(response_times),
                "std_dev": statistics.stdev(response_times) if len(response_times) > 1 else 0,
                "min": min(response_times),
                "max": max(response_times)
            }
            
            # Calculate percentiles
            response_times_sorted = sorted(response_times)
            percentiles = [50, 95, 99]
            for p in percentiles:
                idx = int((p / 100) * (len(response_times_sorted) - 1))
                response_stats[f"p{p}"] = response_times_sorted[idx]
        else:
            response_stats = {"mean": 0, "std_dev": 0, "min": 0, "max": 0, "p50": 0, "p95": 0, "p99": 0}
        
        memory_usage = self.analyze_memory_usage()
        concurrency_stats = self.analyze_concurrency_patterns()
        
        metrics = FastAPIPerformanceMetrics(
            request_count=len(results),
            avg_response_time=response_stats["mean"],
            p95_response_time=response_stats["p95"],
            p99_response_time=response_stats["p99"],
            error_rate=len(errors) / len(results) if results else 0,
            throughput_rps=len(successful_results) / duration if duration > 0 else 0,
            memory_usage_mb=memory_usage.get("rss", 0),
            cpu_usage_percent=0,  # Would need CPU monitoring
            active_connections=concurrency_stats.get("active_threads", 0),
            database_query_count=0,  # Would need database monitoring
            cache_hit_rate=0,  # Would need cache monitoring
            timestamp=datetime.datetime.now()
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def generate_optimization_suggestions(self, metrics: FastAPIPerformanceMetrics) -> List[OptimizationSuggestion]:
        """Generate optimization suggestions based on metrics"""
        suggestions = []
        
        # Response time suggestions
        if metrics.avg_response_time > 200:  # > 200ms
            suggestions.append(OptimizationSuggestion(
                category="Response Time",
                severity="high" if metrics.avg_response_time > 500 else "medium",
                issue=f"High average response time: {metrics.avg_response_time:.1f}ms",
                suggestion="Implement caching for frequently accessed data. Review database queries and add appropriate indexes.",
                expected_improvement="30-50% response time reduction",
                implementation_effort="medium"
            ))
        
        # Error rate suggestions
        if metrics.error_rate > 0.05:  # > 5%
            suggestions.append(OptimizationSuggestion(
                category="Error Handling",
                severity="high",
                issue=f"High error rate: {metrics.error_rate:.1%}",
                suggestion="Review error handling and implement proper retry mechanisms. Add circuit breakers for external dependencies.",
                expected_improvement="Reduced error rate and improved reliability",
                implementation_effort="high"
            ))
        
        # Memory usage suggestions
        if metrics.memory_usage_mb > 500:  # > 500MB
            suggestions.append(OptimizationSuggestion(
                category="Memory Management",
                severity="medium",
                issue=f"High memory usage: {metrics.memory_usage_mb:.1f}MB",
                suggestion="Review object lifecycle and implement proper cleanup. Consider using streaming responses for large data.",
                expected_improvement="Reduced memory footprint and GC pressure",
                implementation_effort="medium"
            ))
        
        # Throughput suggestions
        if metrics.throughput_rps < 100:  # < 100 RPS
            suggestions.append(OptimizationSuggestion(
                category="Concurrency",
                severity="medium",
                issue=f"Low throughput: {metrics.throughput_rps:.1f} RPS",
                suggestion="Increase worker processes and optimize async patterns. Review database connection pooling.",
                expected_improvement="2-5x throughput improvement",
                implementation_effort="medium"
            ))
        
        # Database query suggestions
        if metrics.database_query_count > 1000:
            suggestions.append(OptimizationSuggestion(
                category="Database Optimization",
                severity="medium",
                issue=f"High database query count: {metrics.database_query_count}",
                suggestion="Implement query optimization and caching. Review N+1 query patterns.",
                expected_improvement="Reduced database load and faster responses",
                implementation_effort="high"
            ))
        
        # Cache hit rate suggestions
        if metrics.cache_hit_rate < 0.8:  # < 80%
            suggestions.append(OptimizationSuggestion(
                category="Caching Strategy",
                severity="medium",
                issue=f"Low cache hit rate: {metrics.cache_hit_rate:.1%}",
                suggestion="Review cache invalidation strategy and increase cache TTL for stable data.",
                expected_improvement="Reduced database load and faster responses",
                implementation_effort="low"
            ))
        
        return suggestions
    
    def analyze_fastapi_app(self, app_path: str) -> Dict[str, Any]:
        """Analyze FastAPI application code for optimization opportunities"""
        app_file = Path(app_path)
        
        if not app_file.exists():
            return {"error": "FastAPI app file not found"}
        
        try:
            with open(app_file, 'r') as f:
                content = f.read()
            
            analysis = {
                "async_endpoints": content.count("async def"),
                "sync_endpoints": content.count("def ") - content.count("async def"),
                "database_queries": content.count("SELECT") + content.count("INSERT") + content.count("UPDATE") + content.count("DELETE"),
                "cache_usage": content.count("cache") + content.count("redis") + content.count("memcached"),
                "middleware_count": content.count("add_middleware"),
                "optimization_opportunities": []
            }
            
            # Check for optimization opportunities
            if analysis["sync_endpoints"] > analysis["async_endpoints"]:
                analysis["optimization_opportunities"].append({
                    "issue": "More sync than async endpoints",
                    "recommendation": "Convert sync endpoints to async for better concurrency"
                })
            
            if analysis["database_queries"] > 10:
                analysis["optimization_opportunities"].append({
                    "issue": "High number of database queries",
                    "recommendation": "Review for N+1 queries and implement eager loading"
                })
            
            if analysis["cache_usage"] == 0:
                analysis["optimization_opportunities"].append({
                    "issue": "No caching implementation found",
                    "recommendation": "Add caching for frequently accessed data"
                })
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing FastAPI app: {e}")
            return {"error": str(e)}
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        if not self.metrics_history:
            return {"error": "No performance data available"}
        
        latest_metrics = self.metrics_history[-1]
        suggestions = self.generate_optimization_suggestions(latest_metrics)
        
        # Calculate trends
        if len(self.metrics_history) > 1:
            previous_metrics = self.metrics_history[-2]
            trends = {
                "response_time_trend": latest_metrics.avg_response_time - previous_metrics.avg_response_time,
                "throughput_trend": latest_metrics.throughput_rps - previous_metrics.throughput_rps,
                "memory_trend": latest_metrics.memory_usage_mb - previous_metrics.memory_usage_mb
            }
        else:
            trends = {"no_previous_data": True}
        
        return {
            "current_metrics": asdict(latest_metrics),
            "optimization_suggestions": [asdict(sug) for sug in suggestions],
            "trends": trends,
            "summary": {
                "performance_health": "good" if latest_metrics.avg_response_time < 100 and latest_metrics.error_rate < 0.01 else "warning" if latest_metrics.avg_response_time < 500 and latest_metrics.error_rate < 0.05 else "poor",
                "total_suggestions": len(suggestions),
                "high_priority_suggestions": len([s for s in suggestions if s.severity in ["high", "critical"]]),
                "recommendations_by_category": {
                    category: len([s for s in suggestions if s.category == category])
                    for category in set(s.category for s in suggestions)
                }
            }
        }

def invoke(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for the FastAPI performance optimization skill
    
    Args:
        config: Configuration dictionary with the following structure:
            {
                "action": "simulate_load_test" | "generate_suggestions" | "analyze_app" | "generate_report",
                "parameters": {
                    # Action-specific parameters
                }
            }
    
    Returns:
        Result dictionary with success status and data
    """
    try:
        action = config.get("action")
        parameters = config.get("parameters", {})
        
        if action == "simulate_load_test":
            # Parameters: endpoint_func, users, duration
            users = parameters["users"]
            duration = parameters["duration"]
            
            # Create a mock endpoint function for testing
            async def mock_endpoint():
                await asyncio.sleep(0.01)  # Simulate async work
                return {"status": "ok"}
            
            optimizer = FastAPIPerformanceOptimizer()
            metrics = optimizer.simulate_load_test(mock_endpoint, users, duration)
            
            return {
                "success": True,
                "message": f"Load test completed with {users} users",
                "result": {
                    "request_count": metrics.request_count,
                    "avg_response_time": metrics.avg_response_time,
                    "p95_response_time": metrics.p95_response_time,
                    "p99_response_time": metrics.p99_response_time,
                    "error_rate": metrics.error_rate,
                    "throughput_rps": metrics.throughput_rps,
                    "memory_usage_mb": metrics.memory_usage_mb
                }
            }
        
        elif action == "generate_suggestions":
            # Parameters: metrics_data
            metrics_data = parameters["metrics_data"]
            
            # Reconstruct metrics object
            metrics = FastAPIPerformanceMetrics(
                request_count=metrics_data["request_count"],
                avg_response_time=metrics_data["avg_response_time"],
                p95_response_time=metrics_data["p95_response_time"],
                p99_response_time=metrics_data["p99_response_time"],
                error_rate=metrics_data["error_rate"],
                throughput_rps=metrics_data["throughput_rps"],
                memory_usage_mb=metrics_data["memory_usage_mb"],
                cpu_usage_percent=metrics_data["cpu_usage_percent"],
                active_connections=metrics_data["active_connections"],
                database_query_count=metrics_data["database_query_count"],
                cache_hit_rate=metrics_data["cache_hit_rate"],
                timestamp=datetime.datetime.fromisoformat(metrics_data["timestamp"])
            )
            
            optimizer = FastAPIPerformanceOptimizer()
            suggestions = optimizer.generate_optimization_suggestions(metrics)
            
            return {
                "success": True,
                "message": f"Generated {len(suggestions)} optimization suggestions",
                "result": {
                    "suggestions": [asdict(sug) for sug in suggestions],
                    "summary": {
                        "total_suggestions": len(suggestions),
                        "by_category": {
                            category: len([s for s in suggestions if s.category == category])
                            for category in set(s.category for s in suggestions)
                        }
                    }
                }
            }
        
        elif action == "analyze_app":
            # Parameters: app_path
            app_path = parameters["app_path"]
            
            optimizer = FastAPIPerformanceOptimizer()
            analysis = optimizer.analyze_fastapi_app(app_path)
            
            return {
                "success": True,
                "message": "FastAPI application analysis completed",
                "result": analysis
            }
        
        elif action == "generate_report":
            # Parameters: app_process_id (optional)
            app_process_id = parameters.get("app_process_id")
            optimizer = FastAPIPerformanceOptimizer()
            
            if app_process_id:
                try:
                    optimizer.app_process = psutil.Process(app_process_id)
                except psutil.NoSuchProcess:
                    return {
                        "success": False,
                        "message": f"FastAPI process with ID {app_process_id} not found",
                        "error": "Process not found"
                    }
            
            # Generate a mock report
            mock_metrics = FastAPIPerformanceMetrics(
                request_count=1000,
                avg_response_time=150.0,
                p95_response_time=300.0,
                p99_response_time=500.0,
                error_rate=0.02,
                throughput_rps=50.0,
                memory_usage_mb=250.0,
                cpu_usage_percent=45.0,
                active_connections=10,
                database_query_count=500,
                cache_hit_rate=0.75,
                timestamp=datetime.datetime.now()
            )
            
            optimizer.metrics_history.append(mock_metrics)
            report = optimizer.generate_performance_report()
            
            return {
                "success": True,
                "message": "Performance report generated",
                "result": report
            }
        
        else:
            return {
                "success": False,
                "message": f"Unknown action: {action}",
                "error": "Invalid action specified"
            }
    
    except Exception as e:
        logger.error(f"Error in FastAPI performance optimizer: {e}")
        return {
            "success": False,
            "message": f"Error executing FastAPI performance optimizer: {str(e)}",
            "error": str(e)
        }

if __name__ == "__main__":
    # Example usage
    example_config = {
        "action": "simulate_load_test",
        "parameters": {
            "users": 10,
            "duration": 2.0
        }
    }
    
    result = invoke(example_config)
    print(json.dumps(result, indent=2))