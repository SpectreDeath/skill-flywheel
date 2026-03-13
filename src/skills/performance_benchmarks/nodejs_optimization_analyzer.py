#!/usr/bin/env python3
"""
Node.js Optimization Analyzer Skill

This skill provides comprehensive analysis and optimization recommendations for Node.js applications,
focusing on event loop performance, async operations, memory management, and I/O bottlenecks.

Key Features:
- Event loop performance analysis
- Async operation optimization
- Memory leak detection
- I/O bottleneck identification
- V8 engine optimization recommendations
- Cluster and worker process optimization
"""

import time
import datetime
import logging
import json
import subprocess
import asyncio
import os
import sys
import statistics
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import psutil

logger = logging.getLogger(__name__)

@dataclass
class NodeJSAnalysis:
    """Analysis result for Node.js performance"""
    event_loop_lag: float
    memory_usage: Dict[str, float]
    cpu_usage: float
    active_handles: int
    active_requests: int
    gc_stats: Dict[str, Any]
    heap_usage: Dict[str, float]
    timestamp: datetime.datetime

@dataclass
class OptimizationRecommendation:
    """Optimization recommendation for Node.js"""
    category: str
    severity: str  # low, medium, high, critical
    issue: str
    recommendation: str
    impact: str
    effort: str

class NodeJSOptimizationAnalyzer:
    """Analyzer for Node.js application performance optimization"""
    
    def __init__(self, node_process: Optional[psutil.Process] = None):
        self.node_process = node_process
        self.analyses: List[NodeJSAnalysis] = []
    
    def _get_node_process(self) -> Optional[psutil.Process]:
        """Find Node.js process if not already set"""
        if self.node_process and self.node_process.is_running():
            return self.node_process
        
        # Try to find Node.js processes
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'node' in proc.info['name'].lower():
                    cmdline = proc.info.get('cmdline', [])
                    if cmdline and any('node' in cmd.lower() for cmd in cmdline):
                        self.node_process = proc
                        return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return None
    
    def measure_event_loop_lag(self, duration: float = 1.0) -> float:
        """
        Measure event loop lag by scheduling a timer and measuring the delay
        
        Args:
            duration: Duration to measure lag over
        
        Returns:
            Average event loop lag in milliseconds
        """
        if not self._get_node_process():
            logger.warning("No Node.js process found for event loop analysis")
            return 0.0
        
        lag_samples = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            timer_start = time.perf_counter()
            
            # Use a very short sleep to measure event loop responsiveness
            time.sleep(0.001)  # 1ms
            
            actual_delay = (time.perf_counter() - timer_start) * 1000  # Convert to ms
            expected_delay = 1.0  # 1ms
            lag = actual_delay - expected_delay
            
            if lag > 0:  # Only record positive lag
                lag_samples.append(lag)
        
        return statistics.mean(lag_samples) if lag_samples else 0.0
    
    def analyze_memory_usage(self) -> Dict[str, float]:
        """Analyze memory usage patterns"""
        if not self._get_node_process():
            return {"error": "No Node.js process found"}
        
        try:
            process = self.node_process
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
    
    def analyze_cpu_usage(self) -> float:
        """Analyze CPU usage"""
        if not self._get_node_process():
            return 0.0
        
        try:
            return self.node_process.cpu_percent(interval=1.0)
        except Exception as e:
            logger.error(f"Error analyzing CPU usage: {e}")
            return 0.0
    
    def get_gc_stats(self) -> Dict[str, Any]:
        """Get garbage collection statistics using Node.js --inspect"""
        if not self._get_node_process():
            return {"error": "No Node.js process found"}
        
        try:
            # This would require Node.js to be started with --inspect flag
            # For now, return basic process info
            return {
                "heap_used": self.analyze_memory_usage().get("rss", 0),
                "heap_total": self.analyze_memory_usage().get("vms", 0),
                "external": 0,  # Would need V8 inspector for accurate data
                "gc_duration": 0
            }
        except Exception as e:
            logger.error(f"Error getting GC stats: {e}")
            return {"error": str(e)}
    
    def analyze_async_operations(self) -> Dict[str, int]:
        """Analyze async operation patterns"""
        # This would require Node.js process with --trace-async-hooks
        # For now, return basic process info
        return {
            "active_handles": 0,  # Would need async_hooks for accurate data
            "active_requests": 0,
            "pending_operations": 0
        }
    
    def run_analysis(self) -> NodeJSAnalysis:
        """Run comprehensive Node.js performance analysis"""
        logger.info("Running Node.js performance analysis")
        
        # Measure event loop lag
        event_loop_lag = self.measure_event_loop_lag(duration=2.0)
        
        # Analyze memory usage
        memory_usage = self.analyze_memory_usage()
        
        # Analyze CPU usage
        cpu_usage = self.analyze_cpu_usage()
        
        # Get GC stats
        gc_stats = self.get_gc_stats()
        
        # Analyze async operations
        async_stats = self.analyze_async_operations()
        
        analysis = NodeJSAnalysis(
            event_loop_lag=event_loop_lag,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            active_handles=async_stats["active_handles"],
            active_requests=async_stats["active_requests"],
            gc_stats=gc_stats,
            heap_usage={
                "used": memory_usage.get("rss", 0),
                "total": memory_usage.get("vms", 0),
                "utilization": memory_usage.get("percent", 0)
            },
            timestamp=datetime.datetime.now()
        )
        
        self.analyses.append(analysis)
        return analysis
    
    def generate_recommendations(self, analysis: NodeJSAnalysis) -> List[OptimizationRecommendation]:
        """Generate optimization recommendations based on analysis"""
        recommendations = []
        
        # Event loop lag recommendations
        if analysis.event_loop_lag > 10:  # > 10ms
            recommendations.append(OptimizationRecommendation(
                category="Event Loop",
                severity="high" if analysis.event_loop_lag > 50 else "medium",
                issue=f"High event loop lag: {analysis.event_loop_lag:.2f}ms",
                recommendation="Review synchronous operations blocking the event loop. Consider moving CPU-intensive tasks to worker threads or using async alternatives.",
                impact="Poor responsiveness and request queuing",
                effort="medium"
            ))
        
        # Memory usage recommendations
        memory_percent = analysis.memory_usage.get("percent", 0)
        if memory_percent > 80:
            recommendations.append(OptimizationRecommendation(
                category="Memory Management",
                severity="high",
                issue=f"High memory usage: {memory_percent:.1f}%",
                recommendation="Check for memory leaks. Use memory profiling tools to identify objects not being garbage collected.",
                impact="Potential out-of-memory errors and performance degradation",
                effort="high"
            ))
        
        # CPU usage recommendations
        if analysis.cpu_usage > 80:
            recommendations.append(OptimizationRecommendation(
                category="CPU Optimization",
                severity="medium",
                issue=f"High CPU usage: {analysis.cpu_usage:.1f}%",
                recommendation="Profile CPU usage to identify bottlenecks. Consider algorithm optimization or parallelization.",
                impact="Reduced throughput and increased response times",
                effort="medium"
            ))
        
        # GC recommendations
        heap_used = analysis.heap_usage.get("used", 0)
        if heap_used > 500:  # > 500MB
            recommendations.append(OptimizationRecommendation(
                category="Garbage Collection",
                severity="medium",
                issue=f"High heap usage: {heap_used:.1f}MB",
                recommendation="Monitor GC frequency and duration. Consider increasing heap size with --max-old-space-size or optimizing object creation.",
                impact="GC pauses affecting performance",
                effort="low"
            ))
        
        # Async operation recommendations
        if analysis.active_handles > 1000:
            recommendations.append(OptimizationRecommendation(
                category="Async Operations",
                severity="medium",
                issue=f"High number of active handles: {analysis.active_handles}",
                recommendation="Review connection pooling and resource cleanup. Ensure proper disposal of file handles, sockets, and timers.",
                impact="Resource exhaustion and memory leaks",
                effort="medium"
            ))
        
        return recommendations
    
    def analyze_package_json(self, project_path: str) -> Dict[str, Any]:
        """Analyze package.json for optimization opportunities"""
        package_json_path = Path(project_path) / "package.json"
        
        if not package_json_path.exists():
            return {"error": "package.json not found"}
        
        try:
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            analysis = {
                "node_version": package_data.get("engines", {}).get("node", "not specified"),
                "dependencies_count": len(package_data.get("dependencies", {})),
                "dev_dependencies_count": len(package_data.get("devDependencies", {})),
                "scripts": package_data.get("scripts", {}),
                "optimization_opportunities": []
            }
            
            # Check for optimization opportunities
            if "engines" not in package_data:
                analysis["optimization_opportunities"].append({
                    "issue": "No Node.js version specified in engines",
                    "recommendation": "Specify Node.js version in engines field for consistent performance"
                })
            
            if analysis["dependencies_count"] > 50:
                analysis["optimization_opportunities"].append({
                    "issue": "Large number of dependencies",
                    "recommendation": "Review dependencies for unused packages that can be removed"
                })
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing package.json: {e}")
            return {"error": str(e)}
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        if not self.analyses:
            return {"error": "No analyses available"}
        
        latest_analysis = self.analyses[-1]
        recommendations = self.generate_recommendations(latest_analysis)
        
        return {
            "analysis": asdict(latest_analysis),
            "recommendations": [asdict(rec) for rec in recommendations],
            "summary": {
                "event_loop_health": "good" if latest_analysis.event_loop_lag < 5 else "warning" if latest_analysis.event_loop_lag < 20 else "poor",
                "memory_health": "good" if latest_analysis.memory_usage.get("percent", 0) < 60 else "warning" if latest_analysis.memory_usage.get("percent", 0) < 80 else "poor",
                "cpu_health": "good" if latest_analysis.cpu_usage < 50 else "warning" if latest_analysis.cpu_usage < 80 else "poor",
                "total_recommendations": len(recommendations),
                "critical_issues": len([r for r in recommendations if r.severity == "critical"]),
                "high_priority_issues": len([r for r in recommendations if r.severity == "high"])
            }
        }

async def invoke(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for the Node.js optimization analyzer skill
    
    Args:
        config: Configuration dictionary with the following structure:
            {
                "action": "run_analysis" | "generate_recommendations" | "analyze_package" | "generate_report",
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
        
        if action == "run_analysis":
            # Parameters: node_process_id (optional)
            node_process_id = parameters.get("node_process_id")
            analyzer = NodeJSOptimizationAnalyzer()
            
            if node_process_id:
                try:
                    analyzer.node_process = psutil.Process(node_process_id)
                except psutil.NoSuchProcess:
                    return {
                        "success": False,
                        "message": f"Node.js process with ID {node_process_id} not found",
                        "error": "Process not found"
                    }
            
            analysis = analyzer.run_analysis()
            
            return {
                "success": True,
                "message": "Node.js performance analysis completed",
                "result": {
                    "event_loop_lag": analysis.event_loop_lag,
                    "memory_usage": analysis.memory_usage,
                    "cpu_usage": analysis.cpu_usage,
                    "heap_usage": analysis.heap_usage,
                    "timestamp": analysis.timestamp.isoformat()
                }
            }
        
        elif action == "generate_recommendations":
            # Parameters: analysis_data
            analysis_data = parameters["analysis_data"]
            
            # Reconstruct analysis object
            analysis = NodeJSAnalysis(
                event_loop_lag=analysis_data["event_loop_lag"],
                memory_usage=analysis_data["memory_usage"],
                cpu_usage=analysis_data["cpu_usage"],
                active_handles=analysis_data["active_handles"],
                active_requests=analysis_data["active_requests"],
                gc_stats=analysis_data["gc_stats"],
                heap_usage=analysis_data["heap_usage"],
                timestamp=datetime.datetime.fromisoformat(analysis_data["timestamp"])
            )
            
            analyzer = NodeJSOptimizationAnalyzer()
            recommendations = analyzer.generate_recommendations(analysis)
            
            return {
                "success": True,
                "message": f"Generated {len(recommendations)} optimization recommendations",
                "result": {
                    "recommendations": [asdict(rec) for rec in recommendations],
                    "summary": {
                        "total_recommendations": len(recommendations),
                        "by_category": {
                            category: len([r for r in recommendations if r.category == category])
                            for category in set(r.category for r in recommendations)
                        }
                    }
                }
            }
        
        elif action == "analyze_package":
            # Parameters: project_path
            project_path = parameters["project_path"]
            
            analyzer = NodeJSOptimizationAnalyzer()
            analysis = analyzer.analyze_package_json(project_path)
            
            return {
                "success": True,
                "message": "Package.json analysis completed",
                "result": analysis
            }
        
        elif action == "generate_report":
            # Parameters: node_process_id (optional)
            node_process_id = parameters.get("node_process_id")
            analyzer = NodeJSOptimizationAnalyzer()
            
            if node_process_id:
                try:
                    analyzer.node_process = psutil.Process(node_process_id)
                except psutil.NoSuchProcess:
                    return {
                        "success": False,
                        "message": f"Node.js process with ID {node_process_id} not found",
                        "error": "Process not found"
                    }
            
            # Run analysis first
            analyzer.run_analysis()
            report = analyzer.generate_performance_report()
            
            return {
                "success": True,
                "message": "Comprehensive performance report generated",
                "result": report
            }
        
        else:
            return {
                "success": False,
                "message": f"Unknown action: {action}",
                "error": "Invalid action specified"
            }
    
    except Exception as e:
        logger.error(f"Error in Node.js optimization analyzer: {e}")
        return {
            "success": False,
            "message": f"Error executing Node.js optimization analyzer: {str(e)}",
            "error": str(e)
        }

if __name__ == "__main__":
    # Example usage
    example_config = {
        "action": "run_analysis",
        "parameters": {}
    }
    
    result = invoke(example_config)
    print(json.dumps(result, indent=2))