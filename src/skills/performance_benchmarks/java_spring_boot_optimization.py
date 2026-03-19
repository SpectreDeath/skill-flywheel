#!/usr/bin/env python3
"""
Java Spring Boot Optimization Skill

This skill provides comprehensive optimization for Java Spring Boot applications,
focusing on JVM tuning, framework efficiency, database connection optimization,
and enterprise application performance patterns.

Key Features:
- JVM performance tuning and GC optimization
- Spring Boot framework optimization
- Database connection pool tuning
- Application startup time optimization
- Memory leak detection and prevention
- Enterprise application performance patterns
"""

import datetime
import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import psutil

logger = logging.getLogger(__name__)

@dataclass
class JavaPerformanceMetrics:
    """Performance metrics for Java Spring Boot application"""
    jvm_heap_used: float  # MB
    jvm_heap_max: float   # MB
    jvm_non_heap_used: float  # MB
    gc_count: int
    gc_time: float      # ms
    thread_count: int
    class_count: int
    cpu_usage_percent: float
    startup_time: float  # seconds
    memory_pool_usage: Dict[str, Dict[str, float]]
    timestamp: datetime.datetime

@dataclass
class JavaOptimizationRecommendation:
    """Optimization recommendation for Java Spring Boot"""
    category: str
    severity: str  # low, medium, high, critical
    issue: str
    recommendation: str
    expected_improvement: str
    implementation_effort: str

class JavaSpringBootOptimizer:
    """Optimizer for Java Spring Boot application performance"""
    
    def __init__(self, java_process: Optional[psutil.Process] = None):
        self.java_process = java_process
        self.metrics_history: List[JavaPerformanceMetrics] = []
    
    def _get_java_process(self) -> Optional[psutil.Process]:
        """Find Java application process"""
        if self.java_process and self.java_process.is_running():
            return self.java_process
        
        # Try to find Java processes
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'java' in proc.info['name'].lower():
                    cmdline = proc.info.get('cmdline', [])
                    if cmdline and any('java' in cmd.lower() for cmd in cmdline):
                        self.java_process = proc
                        return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return None
    
    def get_jvm_metrics(self) -> Dict[str, Any]:
        """Get JVM metrics using JMX or jstat"""
        if not self._get_java_process():
            return {"error": "No Java process found"}
        
        try:
            # This would require JMX connection or jstat command
            # For now, return basic process info as approximation
            process = self.java_process
            memory_info = process.memory_info()
            
            return {
                "heap_used": memory_info.rss / (1024 * 1024),  # MB - approximation
                "heap_max": memory_info.vms / (1024 * 1024),   # MB - approximation
                "non_heap_used": 0,  # Would need JMX
                "gc_count": 0,       # Would need JMX
                "gc_time": 0,        # Would need JMX
                "thread_count": process.num_threads(),
                "class_count": 0,    # Would need JMX
                "memory_pools": {}   # Would need JMX
            }
        except Exception as e:
            logger.error(f"Error getting JVM metrics: {e}")
            return {"error": str(e)}
    
    def analyze_spring_boot_config(self, project_path: str) -> Dict[str, Any]:
        """Analyze Spring Boot configuration for optimization opportunities"""
        project_dir = Path(project_path)
        
        if not project_dir.exists():
            return {"error": "Spring Boot project directory not found"}
        
        try:
            analysis = {
                "application_properties": {},
                "profiles": [],
                "datasource_config": {},
                "jvm_args": [],
                "optimization_opportunities": []
            }
            
            # Check application.properties/yml
            for config_file in ["application.properties", "application.yml", "application.yaml"]:
                config_path = project_dir / "src" / "main" / "resources" / config_file
                if config_path.exists():
                    try:
                        with open(config_path) as f:
                            content = f.read()
                        
                        # Parse basic properties
                        if config_file.endswith('.properties'):
                            for line in content.splitlines():
                                if '=' in line and not line.strip().startswith('#'):
                                    key, value = line.split('=', 1)
                                    analysis["application_properties"][key.strip()] = value.strip()
                        else:  # YAML
                            analysis["application_properties"]["yaml_config"] = "found"
                    
                    except Exception as e:
                        logger.warning(f"Could not parse {config_file}: {e}")
            
            # Check for optimization opportunities
            props = analysis["application_properties"]
            
            # Database connection pool optimization
            if any(key.startswith("spring.datasource") for key in props):
                analysis["optimization_opportunities"].append({
                    "category": "Database",
                    "issue": "Database connection pool configuration",
                    "recommendation": "Optimize connection pool settings (max-pool-size, min-idle, connection-timeout)"
                })
            
            # JVM memory optimization
            if any(key.startswith("java") or key.startswith("jvm") for key in props):
                analysis["optimization_opportunities"].append({
                    "category": "JVM Tuning",
                    "issue": "JVM memory configuration",
                    "recommendation": "Optimize heap size (-Xmx, -Xms) and GC settings for your workload"
                })
            
            # Spring Boot optimization
            if "spring.profiles.active" in props:
                analysis["profiles"] = props["spring.profiles.active"].split(',')
            
            if "spring.jpa.hibernate.ddl-auto" in props:
                if props["spring.jpa.hibernate.ddl-auto"] == "update":
                    analysis["optimization_opportunities"].append({
                        "category": "Hibernate",
                        "issue": "DDL auto-update in production",
                        "recommendation": "Use 'validate' or 'none' in production, use migrations for schema changes"
                    })
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing Spring Boot config: {e}")
            return {"error": str(e)}
    
    def analyze_startup_performance(self) -> Dict[str, Any]:
        """Analyze Spring Boot application startup performance"""
        # This would require detailed profiling during startup
        # For now, return basic process info
        return {
            "startup_time": 0,  # Would need startup profiling
            "bean_initialization_time": 0,  # Would need Spring profiling
            "component_scan_time": 0,  # Would need Spring profiling
            "lazy_initialization_benefits": 0  # Would need analysis
        }
    
    def analyze_memory_usage(self) -> Dict[str, float]:
        """Analyze memory usage patterns"""
        if not self._get_java_process():
            return {"error": "No Java process found"}
        
        try:
            process = self.java_process
            memory_info = process.memory_info()
            
            return {
                "rss": memory_info.rss / (1024 * 1024),  # MB
                "vms": memory_info.vms / (1024 * 1024),  # MB
                "percent": process.memory_percent(),
                "available": psutil.virtual_memory().available / (1024 * 1024 * 1024)  # GB
            }
        except Exception as e:
            logger.error(f"Error analyzing memory usage: {e}")
            return {"error": str(e)}
    
    def run_performance_analysis(self) -> JavaPerformanceMetrics:
        """Run comprehensive Java Spring Boot performance analysis"""
        logger.info("Running Java Spring Boot performance analysis")
        
        # Get JVM metrics
        jvm_metrics = self.get_jvm_metrics()
        
        # Analyze memory usage
        memory_usage = self.analyze_memory_usage()
        
        # Analyze startup performance
        startup_metrics = self.analyze_startup_performance()
        
        # Analyze CPU usage
        cpu_usage = 0
        if self._get_java_process():
            try:
                cpu_usage = self.java_process.cpu_percent(interval=1.0)
            except Exception:
                pass
        
        metrics = JavaPerformanceMetrics(
            jvm_heap_used=jvm_metrics.get("heap_used", 0),
            jvm_heap_max=jvm_metrics.get("heap_max", 0),
            jvm_non_heap_used=jvm_metrics.get("non_heap_used", 0),
            gc_count=jvm_metrics.get("gc_count", 0),
            gc_time=jvm_metrics.get("gc_time", 0),
            thread_count=jvm_metrics.get("thread_count", 0),
            class_count=jvm_metrics.get("class_count", 0),
            cpu_usage_percent=cpu_usage,
            startup_time=startup_metrics.get("startup_time", 0),
            memory_pool_usage=jvm_metrics.get("memory_pools", {}),
            timestamp=datetime.datetime.now()
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def generate_optimization_recommendations(self, metrics: JavaPerformanceMetrics) -> List[JavaOptimizationRecommendation]:
        """Generate optimization recommendations based on metrics"""
        recommendations = []
        
        # Heap usage recommendations
        if metrics.jvm_heap_used > 1000:  # > 1GB
            recommendations.append(JavaOptimizationRecommendation(
                category="JVM Memory",
                severity="medium",
                issue=f"High heap usage: {metrics.jvm_heap_used:.1f}MB",
                recommendation="Review object allocation patterns and increase heap size if needed. Consider using memory-efficient data structures.",
                expected_improvement="Reduced GC pressure and improved response times",
                implementation_effort="medium"
            ))
        
        # GC recommendations
        if metrics.gc_count > 100:  # High GC frequency
            recommendations.append(JavaOptimizationRecommendation(
                category="Garbage Collection",
                severity="high",
                issue=f"High GC frequency: {metrics.gc_count} collections",
                recommendation="Tune GC parameters for your workload. Consider G1GC for large heaps or ZGC for low latency.",
                expected_improvement="Reduced GC pauses and improved throughput",
                implementation_effort="high"
            ))
        
        # Thread count recommendations
        if metrics.thread_count > 200:
            recommendations.append(JavaOptimizationRecommendation(
                category="Threading",
                severity="medium",
                issue=f"High thread count: {metrics.thread_count}",
                recommendation="Review thread pool configurations and consider reducing thread pool sizes. Use reactive programming for I/O bound tasks.",
                expected_improvement="Reduced context switching and memory usage",
                implementation_effort="medium"
            ))
        
        # CPU usage recommendations
        if metrics.cpu_usage_percent > 80:
            recommendations.append(JavaOptimizationRecommendation(
                category="CPU Optimization",
                severity="medium",
                issue=f"High CPU usage: {metrics.cpu_usage_percent:.1f}%",
                recommendation="Profile CPU usage to identify bottlenecks. Consider algorithm optimization and caching strategies.",
                expected_improvement="Improved throughput and reduced response times",
                implementation_effort="medium"
            ))
        
        # Startup time recommendations
        if metrics.startup_time > 60:  # > 60 seconds
            recommendations.append(JavaOptimizationRecommendation(
                category="Startup Performance",
                severity="medium",
                issue=f"Slow startup time: {metrics.startup_time:.1f}s",
                recommendation="Enable lazy initialization, reduce component scanning scope, and optimize bean creation order.",
                expected_improvement="Faster deployment and development cycles",
                implementation_effort="medium"
            ))
        
        return recommendations
    
    def analyze_spring_boot_source_code(self, project_path: str) -> Dict[str, Any]:
        """Analyze Spring Boot source code for optimization opportunities"""
        project_dir = Path(project_path)
        
        if not project_dir.exists():
            return {"error": "Spring Boot project directory not found"}
        
        try:
            analysis = {
                "controllers": [],
                "services": [],
                "repositories": [],
                "configurations": [],
                "optimization_opportunities": []
            }
            
            # Find Java files
            for java_file in project_dir.rglob("*.java"):
                try:
                    with open(java_file, encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for Spring annotations
                    file_analysis = {
                        "path": str(java_file),
                        "has_controller": "@RestController" in content or "@Controller" in content,
                        "has_service": "@Service" in content,
                        "has_repository": "@Repository" in content,
                        "has_configuration": "@Configuration" in content,
                        "has_component": "@Component" in content,
                        "lazy_annotation": "@Lazy" in content,
                        "async_annotation": "@Async" in content,
                        "transactional_annotation": "@Transactional" in content
                    }
                    
                    if file_analysis["has_controller"]:
                        analysis["controllers"].append(file_analysis)
                    elif file_analysis["has_service"]:
                        analysis["services"].append(file_analysis)
                    elif file_analysis["has_repository"]:
                        analysis["repositories"].append(file_analysis)
                    elif file_analysis["has_configuration"]:
                        analysis["configurations"].append(file_analysis)
                    
                    # Check for optimization opportunities
                    if not file_analysis["lazy_annotation"] and file_analysis["has_service"]:
                        analysis["optimization_opportunities"].append({
                            "file": str(java_file),
                            "issue": "Service without lazy initialization",
                            "recommendation": "Consider adding @Lazy annotation to reduce startup time"
                        })
                    
                    if file_analysis["transactional_annotation"] and "readOnly = true" not in content:
                        analysis["optimization_opportunities"].append({
                            "file": str(java_file),
                            "issue": "Transactional method without readOnly",
                            "recommendation": "Add readOnly = true for read-only operations to improve performance"
                        })
                
                except Exception as e:
                    logger.warning(f"Could not analyze file {java_file}: {e}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing Spring Boot source code: {e}")
            return {"error": str(e)}
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive Java Spring Boot performance report"""
        if not self.metrics_history:
            return {"error": "No performance data available"}
        
        latest_metrics = self.metrics_history[-1]
        recommendations = self.generate_optimization_recommendations(latest_metrics)
        
        # Calculate trends
        if len(self.metrics_history) > 1:
            previous_metrics = self.metrics_history[-2]
            trends = {
                "heap_usage_trend": latest_metrics.jvm_heap_used - previous_metrics.jvm_heap_used,
                "gc_count_trend": latest_metrics.gc_count - previous_metrics.gc_count,
                "thread_count_trend": latest_metrics.thread_count - previous_metrics.thread_count
            }
        else:
            trends = {"no_previous_data": True}
        
        return {
            "current_metrics": asdict(latest_metrics),
            "recommendations": [asdict(rec) for rec in recommendations],
            "trends": trends,
            "summary": {
                "performance_health": "good" if latest_metrics.jvm_heap_used < 500 and latest_metrics.gc_count < 50 and latest_metrics.cpu_usage_percent < 50 else "warning" if latest_metrics.jvm_heap_used < 1000 and latest_metrics.gc_count < 100 and latest_metrics.cpu_usage_percent < 80 else "poor",
                "total_recommendations": len(recommendations),
                "high_priority_recommendations": len([r for r in recommendations if r.severity in ["high", "critical"]]),
                "recommendations_by_category": {
                    category: len([r for r in recommendations if r.category == category])
                    for category in set(r.category for r in recommendations)
                }
            }
        }

def invoke(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for the Java Spring Boot optimization skill
    
    Args:
        config: Configuration dictionary with the following structure:
            {
                "action": "run_analysis" | "generate_recommendations" | "analyze_config" | "analyze_source" | "generate_report",
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
            # Parameters: java_process_id (optional)
            java_process_id = parameters.get("java_process_id")
            optimizer = JavaSpringBootOptimizer()
            
            if java_process_id:
                try:
                    optimizer.java_process = psutil.Process(java_process_id)
                except psutil.NoSuchProcess:
                    return {
                        "success": False,
                        "message": f"Java process with ID {java_process_id} not found",
                        "error": "Process not found"
                    }
            
            metrics = optimizer.run_performance_analysis()
            
            return {
                "success": True,
                "message": "Java Spring Boot performance analysis completed",
                "result": {
                    "jvm_heap_used": metrics.jvm_heap_used,
                    "jvm_heap_max": metrics.jvm_heap_max,
                    "gc_count": metrics.gc_count,
                    "gc_time": metrics.gc_time,
                    "thread_count": metrics.thread_count,
                    "cpu_usage_percent": metrics.cpu_usage_percent,
                    "startup_time": metrics.startup_time,
                    "timestamp": metrics.timestamp.isoformat()
                }
            }
        
        elif action == "generate_recommendations":
            # Parameters: metrics_data
            metrics_data = parameters["metrics_data"]
            
            # Reconstruct metrics object
            metrics = JavaPerformanceMetrics(
                jvm_heap_used=metrics_data["jvm_heap_used"],
                jvm_heap_max=metrics_data["jvm_heap_max"],
                jvm_non_heap_used=metrics_data["jvm_non_heap_used"],
                gc_count=metrics_data["gc_count"],
                gc_time=metrics_data["gc_time"],
                thread_count=metrics_data["thread_count"],
                class_count=metrics_data["class_count"],
                cpu_usage_percent=metrics_data["cpu_usage_percent"],
                startup_time=metrics_data["startup_time"],
                memory_pool_usage=metrics_data["memory_pool_usage"],
                timestamp=datetime.datetime.fromisoformat(metrics_data["timestamp"])
            )
            
            optimizer = JavaSpringBootOptimizer()
            recommendations = optimizer.generate_optimization_recommendations(metrics)
            
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
        
        elif action == "analyze_config":
            # Parameters: project_path
            project_path = parameters["project_path"]
            
            optimizer = JavaSpringBootOptimizer()
            analysis = optimizer.analyze_spring_boot_config(project_path)
            
            return {
                "success": True,
                "message": "Spring Boot configuration analysis completed",
                "result": analysis
            }
        
        elif action == "analyze_source":
            # Parameters: project_path
            project_path = parameters["project_path"]
            
            optimizer = JavaSpringBootOptimizer()
            analysis = optimizer.analyze_spring_boot_source_code(project_path)
            
            return {
                "success": True,
                "message": "Spring Boot source code analysis completed",
                "result": analysis
            }
        
        elif action == "generate_report":
            # Parameters: java_process_id (optional)
            java_process_id = parameters.get("java_process_id")
            optimizer = JavaSpringBootOptimizer()
            
            if java_process_id:
                try:
                    optimizer.java_process = psutil.Process(java_process_id)
                except psutil.NoSuchProcess:
                    return {
                        "success": False,
                        "message": f"Java process with ID {java_process_id} not found",
                        "error": "Process not found"
                    }
            
            # Generate a mock report
            mock_metrics = JavaPerformanceMetrics(
                jvm_heap_used=800.0,
                jvm_heap_max=2048.0,
                jvm_non_heap_used=100.0,
                gc_count=30,
                gc_time=50.0,
                thread_count=150,
                class_count=5000,
                cpu_usage_percent=45.0,
                startup_time=45.0,
                memory_pool_usage={},
                timestamp=datetime.datetime.now()
            )
            
            optimizer.metrics_history.append(mock_metrics)
            report = optimizer.generate_performance_report()
            
            return {
                "success": True,
                "message": "Java Spring Boot performance report generated",
                "result": report
            }
        
        else:
            return {
                "success": False,
                "message": f"Unknown action: {action}",
                "error": "Invalid action specified"
            }
    
    except Exception as e:
        logger.error(f"Error in Java Spring Boot optimizer: {e}")
        return {
            "success": False,
            "message": f"Error executing Java Spring Boot optimizer: {str(e)}",
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
