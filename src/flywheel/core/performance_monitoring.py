#!/usr/bin/env python3
"""
Performance Monitoring and Analytics System for Skill Flywheel

This module provides comprehensive performance monitoring, analytics, and
insights for skill execution, agent orchestration, and system health.
It includes real-time monitoring, historical analysis, and predictive insights.
"""

import asyncio
import json
import logging
import queue
import statistics
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Tuple

import psutil

logger = logging.getLogger(__name__)

class MetricType(Enum):
    EXECUTION_TIME = "execution_time"
    SUCCESS_RATE = "success_rate"
    QUALITY_SCORE = "quality_score"
    RESOURCE_USAGE = "resource_usage"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    LATENCY = "latency"

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    ERROR = "error"

@dataclass
class PerformanceMetric:
    """Individual performance metric."""
    skill_id: str
    metric_type: MetricType
    value: float
    timestamp: datetime
    context: Dict[str, Any]
    agent_framework: str | None = None

@dataclass
class Alert:
    """Performance alert."""
    alert_id: str
    level: AlertLevel
    message: str
    metric_type: MetricType
    skill_id: str | None
    timestamp: datetime
    resolved: bool = False

@dataclass
class PerformanceReport:
    """Performance analysis report."""
    report_id: str
    timestamp: datetime
    time_range: Tuple[datetime, datetime]
    summary: Dict[str, Any]
    trends: Dict[str, List[Dict[str, Any]]]
    alerts: List[Alert]
    recommendations: List[str]

class MetricsCollector:
    """Collects and stores performance metrics."""
    
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.metrics_file = self.storage_path / "metrics.jsonl"
        self.metrics_queue = queue.Queue()
        self.is_collecting = False
        self.collection_thread = None
        
        # In-memory storage for recent metrics
        self.recent_metrics: List[PerformanceMetric] = []
        self.max_recent_metrics = 10000
    
    def start_collection(self):
        """Start background metrics collection."""
        if self.is_collecting:
            return
        
        self.is_collecting = True
        self.collection_thread = threading.Thread(target=self._collection_loop, daemon=True)
        self.collection_thread.start()
        logger.info("Started metrics collection")
    
    def stop_collection(self):
        """Stop background metrics collection."""
        self.is_collecting = False
        if self.collection_thread:
            self.collection_thread.join(timeout=5)
        logger.info("Stopped metrics collection")
    
    def _collection_loop(self):
        """Background collection loop."""
        while self.is_collecting:
            try:
                # Collect system metrics
                system_metrics = self._collect_system_metrics()
                for metric in system_metrics:
                    self.record_metric(metric)
                
                # Process queued metrics
                while not self.metrics_queue.empty():
                    metric = self.metrics_queue.get()
                    self._store_metric(metric)
                
                time.sleep(10)  # Collect every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in metrics collection loop: {e}")
                time.sleep(5)
    
    def _collect_system_metrics(self) -> List[PerformanceMetric]:
        """Collect system-level metrics."""
        metrics = []
        timestamp = datetime.now()
        
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics.append(PerformanceMetric(
                skill_id="system",
                metric_type=MetricType.RESOURCE_USAGE,
                value=cpu_percent,
                timestamp=timestamp,
                context={"resource_type": "cpu", "unit": "percent"}
            ))
            
            # Memory usage
            memory = psutil.virtual_memory()
            metrics.append(PerformanceMetric(
                skill_id="system",
                metric_type=MetricType.RESOURCE_USAGE,
                value=memory.percent,
                timestamp=timestamp,
                context={"resource_type": "memory", "unit": "percent"}
            ))
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            metrics.append(PerformanceMetric(
                skill_id="system",
                metric_type=MetricType.RESOURCE_USAGE,
                value=disk_percent,
                timestamp=timestamp,
                context={"resource_type": "disk", "unit": "percent"}
            ))
            
            # Network I/O
            net_io = psutil.net_io_counters()
            metrics.append(PerformanceMetric(
                skill_id="system",
                metric_type=MetricType.THROUGHPUT,
                value=net_io.bytes_sent + net_io.bytes_recv,
                timestamp=timestamp,
                context={"metric": "network_io", "unit": "bytes"}
            ))
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
        
        return metrics
    
    def record_metric(self, metric: PerformanceMetric):
        """Record a performance metric."""
        # Add to in-memory storage
        self.recent_metrics.append(metric)
        if len(self.recent_metrics) > self.max_recent_metrics:
            self.recent_metrics.pop(0)
        
        # Queue for background storage
        self.metrics_queue.put(metric)
    
    def _store_metric(self, metric: PerformanceMetric):
        """Store metric to persistent storage."""
        try:
            metric_data = {
                "skill_id": metric.skill_id,
                "metric_type": metric.metric_type.value,
                "value": metric.value,
                "timestamp": metric.timestamp.isoformat(),
                "context": metric.context,
                "agent_framework": metric.agent_framework
            }
            
            with open(self.metrics_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(metric_data) + '\n')
                
        except Exception as e:
            logger.error(f"Error storing metric: {e}")
    
    def get_metrics(self, skill_id: str | None = None, 
                   metric_type: MetricType | None = None,
                   time_range: Tuple[datetime, datetime] | None = None) -> List[PerformanceMetric]:
        """Get metrics with optional filtering."""
        filtered_metrics = self.recent_metrics.copy()
        
        if skill_id:
            filtered_metrics = [m for m in filtered_metrics if m.skill_id == skill_id]
        
        if metric_type:
            filtered_metrics = [m for m in filtered_metrics if m.metric_type == metric_type]
        
        if time_range:
            start_time, end_time = time_range
            filtered_metrics = [m for m in filtered_metrics 
                              if start_time <= m.timestamp <= end_time]
        
        return filtered_metrics
    
    def get_skill_stats(self, skill_id: str) -> Dict[str, Any]:
        """Get statistics for a specific skill."""
        metrics = self.get_metrics(skill_id=skill_id)
        
        if not metrics:
            return {"error": f"No metrics found for skill {skill_id}"}
        
        # Group by metric type
        stats = {}
        for metric_type in MetricType:
            type_metrics = [m for m in metrics if m.metric_type == metric_type]
            if type_metrics:
                values = [m.value for m in type_metrics]
                stats[metric_type.value] = {
                    "count": len(values),
                    "mean": statistics.mean(values),
                    "median": statistics.median(values),
                    "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
                    "min": min(values),
                    "max": max(values),
                    "latest": type_metrics[-1].value if type_metrics else None
                }
        
        return stats

class AlertManager:
    """Manages performance alerts and notifications."""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.alerts: List[Alert] = []
        self.alert_rules: List[Dict[str, Any]] = []
        self.alert_callbacks: List[Callable[[Alert], None]] = []
        
        # Default alert rules
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Setup default alert rules."""
        self.add_alert_rule({
            "name": "High CPU Usage",
            "metric_type": MetricType.RESOURCE_USAGE,
            "threshold": 80.0,
            "comparison": "greater_than",
            "resource_type": "cpu",
            "level": AlertLevel.WARNING,
            "description": "CPU usage is above 80%"
        })
        
        self.add_alert_rule({
            "name": "High Memory Usage",
            "metric_type": MetricType.RESOURCE_USAGE,
            "threshold": 90.0,
            "comparison": "greater_than",
            "resource_type": "memory",
            "level": AlertLevel.CRITICAL,
            "description": "Memory usage is above 90%"
        })
        
        self.add_alert_rule({
            "name": "Low Success Rate",
            "metric_type": MetricType.SUCCESS_RATE,
            "threshold": 0.7,
            "comparison": "less_than",
            "level": AlertLevel.ERROR,
            "description": "Skill success rate is below 70%"
        })
    
    def add_alert_rule(self, rule: Dict[str, Any]):
        """Add a new alert rule."""
        self.alert_rules.append(rule)
        logger.info(f"Added alert rule: {rule['name']}")
    
    def add_alert_callback(self, callback: Callable[[Alert], None]):
        """Add a callback function for alerts."""
        self.alert_callbacks.append(callback)
    
    def check_alerts(self):
        """Check for new alerts based on current metrics."""
        current_time = datetime.now()
        time_window = timedelta(minutes=5)
        
        for rule in self.alert_rules:
            try:
                # Get recent metrics for this rule
                metrics = self.metrics_collector.get_metrics(
                    metric_type=MetricType(rule["metric_type"]),
                    time_range=(current_time - time_window, current_time)
                )
                
                # Filter by resource type if specified
                if "resource_type" in rule:
                    metrics = [m for m in metrics 
                             if m.context.get("resource_type") == rule["resource_type"]]
                
                if not metrics:
                    continue
                
                # Calculate aggregate value
                values = [m.value for m in metrics]
                if rule["comparison"] == "greater_than":
                    current_value = max(values)
                    should_alert = current_value > rule["threshold"]
                elif rule["comparison"] == "less_than":
                    current_value = min(values)
                    should_alert = current_value < rule["threshold"]
                else:
                    current_value = statistics.mean(values)
                    should_alert = current_value > rule["threshold"]
                
                # Create alert if needed
                if should_alert:
                    alert = Alert(
                        alert_id=f"{rule['name']}_{current_time.isoformat()}",
                        level=AlertLevel(rule["level"]),
                        message=rule["description"],
                        metric_type=MetricType(rule["metric_type"]),
                        skill_id=None,
                        timestamp=current_time
                    )
                    
                    # Check if this alert already exists and is not resolved
                    existing_alert = next((a for a in self.alerts 
                                         if a.alert_id == alert.alert_id and not a.resolved), None)
                    
                    if not existing_alert:
                        self.alerts.append(alert)
                        self._notify_alert(alert)
                        
            except Exception as e:
                logger.error(f"Error checking alert rule {rule['name']}: {e}")
    
    def _notify_alert(self, alert: Alert):
        """Notify about a new alert."""
        logger.warning(f"ALERT: {alert.level.value.upper()} - {alert.message}")
        
        # Call registered callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")
    
    def resolve_alert(self, alert_id: str):
        """Mark an alert as resolved."""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                logger.info(f"Resolved alert: {alert_id}")
                break
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active (unresolved) alerts."""
        return [alert for alert in self.alerts if not alert.resolved]

class AnalyticsEngine:
    """Provides advanced analytics and insights."""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
    
    def generate_performance_report(self, time_range: Tuple[datetime, datetime]) -> PerformanceReport:
        """Generate a comprehensive performance report."""
        report_id = f"report_{datetime.now().isoformat()}"
        
        # Get metrics for the time range
        all_metrics = self.metrics_collector.get_metrics(time_range=time_range)
        
        # Generate summary
        summary = self._generate_summary(all_metrics)
        
        # Analyze trends
        trends = self._analyze_trends(all_metrics, time_range)
        
        # Get alerts
        alert_manager = AlertManager(self.metrics_collector)
        alert_manager.check_alerts()
        alerts = alert_manager.get_active_alerts()
        
        # Generate recommendations
        recommendations = self._generate_recommendations(summary, trends)
        
        return PerformanceReport(
            report_id=report_id,
            timestamp=datetime.now(),
            time_range=time_range,
            summary=summary,
            trends=trends,
            alerts=alerts,
            recommendations=recommendations
        )
    
    def _generate_summary(self, metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """Generate performance summary."""
        if not metrics:
            return {"error": "No metrics available"}
        
        # Group by skill
        skill_metrics = {}
        for metric in metrics:
            if metric.skill_id not in skill_metrics:
                skill_metrics[metric.skill_id] = []
            skill_metrics[metric.skill_id].append(metric)
        
        summary = {
            "total_metrics": len(metrics),
            "unique_skills": len(skill_metrics),
            "time_range": {
                "start": min(m.timestamp for m in metrics).isoformat(),
                "end": max(m.timestamp for m in metrics).isoformat()
            },
            "skill_summary": {}
        }
        
        # Calculate stats for each skill
        for skill_id, skill_mets in skill_metrics.items():
            execution_times = [m.value for m in skill_mets if m.metric_type == MetricType.EXECUTION_TIME]
            success_rates = [m.value for m in skill_mets if m.metric_type == MetricType.SUCCESS_RATE]
            quality_scores = [m.value for m in skill_mets if m.metric_type == MetricType.QUALITY_SCORE]
            
            skill_summary = {
                "total_executions": len(execution_times),
                "avg_execution_time": statistics.mean(execution_times) if execution_times else 0,
                "success_rate": statistics.mean(success_rates) if success_rates else 0,
                "avg_quality_score": statistics.mean(quality_scores) if quality_scores else 0,
                "performance_rank": self._calculate_performance_rank(execution_times, success_rates, quality_scores)
            }
            
            summary["skill_summary"][skill_id] = skill_summary
        
        # Overall system stats
        all_execution_times = [m.value for m in metrics if m.metric_type == MetricType.EXECUTION_TIME]
        all_success_rates = [m.value for m in metrics if m.metric_type == MetricType.SUCCESS_RATE]
        
        summary.update({
            "system_avg_execution_time": statistics.mean(all_execution_times) if all_execution_times else 0,
            "system_success_rate": statistics.mean(all_success_rates) if all_success_rates else 0,
            "peak_usage_time": self._find_peak_usage_time(metrics)
        })
        
        return summary
    
    def _calculate_performance_rank(self, execution_times: List[float], 
                                  success_rates: List[float], 
                                  quality_scores: List[float]) -> str:
        """Calculate performance rank for a skill."""
        if not execution_times or not success_rates or not quality_scores:
            return "unknown"
        
        # Normalize scores (0-100)
        avg_time = statistics.mean(execution_times)
        avg_success = statistics.mean(success_rates)
        avg_quality = statistics.mean(quality_scores)
        
        # Time score (lower is better, normalized to 0-100)
        time_score = max(0, 100 - (avg_time / 10))  # Assume 1000ms is max acceptable
        
        # Overall score
        overall_score = (time_score * 0.3) + (avg_success * 100 * 0.4) + (avg_quality * 100 * 0.3)
        
        if overall_score >= 80:
            return "excellent"
        elif overall_score >= 60:
            return "good"
        elif overall_score >= 40:
            return "fair"
        else:
            return "poor"
    
    def _analyze_trends(self, metrics: List[PerformanceMetric], 
                       time_range: Tuple[datetime, datetime]) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze performance trends over time."""
        trends = {}
        
        # Analyze by hour
        hourly_data = self._group_by_hour(metrics, time_range)
        
        for metric_type in MetricType:
            type_metrics = [m for m in metrics if m.metric_type == metric_type]
            if not type_metrics:
                continue
            
            trend_data = []
            for hour, hour_metrics in hourly_data.items():
                hour_type_metrics = [m for m in hour_metrics if m.metric_type == metric_type]
                if hour_type_metrics:
                    values = [m.value for m in hour_type_metrics]
                    trend_data.append({
                        "timestamp": hour.isoformat(),
                        "value": statistics.mean(values),
                        "count": len(values)
                    })
            
            if trend_data:
                trends[metric_type.value] = trend_data
        
        return trends
    
    def _group_by_hour(self, metrics: List[PerformanceMetric], 
                      time_range: Tuple[datetime, datetime]) -> Dict[datetime, List[PerformanceMetric]]:
        """Group metrics by hour."""
        hourly_data = {}
        
        current_time = time_range[0]
        while current_time <= time_range[1]:
            hourly_data[current_time] = []
            current_time += timedelta(hours=1)
        
        for metric in metrics:
            hour_key = metric.timestamp.replace(minute=0, second=0, microsecond=0)
            if hour_key in hourly_data:
                hourly_data[hour_key].append(metric)
        
        return hourly_data
    
    def _find_peak_usage_time(self, metrics: List[PerformanceMetric]) -> str:
        """Find the peak usage time."""
        hourly_counts = {}
        
        for metric in metrics:
            hour_key = metric.timestamp.strftime("%Y-%m-%d %H:00")
            hourly_counts[hour_key] = hourly_counts.get(hour_key, 0) + 1
        
        if not hourly_counts:
            return "unknown"
        
        peak_hour = max(hourly_counts, key=hourly_counts.get)
        return peak_hour
    
    def _generate_recommendations(self, summary: Dict[str, Any], 
                                trends: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Generate performance improvement recommendations."""
        recommendations = []
        
        # System-level recommendations
        if summary.get("system_success_rate", 0) < 0.8:
            recommendations.append("System success rate is below 80%. Consider reviewing error handling and resource allocation.")
        
        if summary.get("system_avg_execution_time", 0) > 5.0:  # 5 seconds
            recommendations.append("Average execution time is high. Consider optimizing skill implementations or increasing resources.")
        
        # Skill-specific recommendations
        skill_summary = summary.get("skill_summary", {})
        for skill_id, stats in skill_summary.items():
            if stats.get("success_rate", 0) < 0.7:
                recommendations.append(f"Skill '{skill_id}' has low success rate. Review implementation and error handling.")
            
            if stats.get("avg_execution_time", 0) > 10.0:  # 10 seconds
                recommendations.append(f"Skill '{skill_id}' is slow. Consider optimization or caching strategies.")
        
        # Trend-based recommendations
        if "execution_time" in trends:
            execution_trend = trends["execution_time"]
            if len(execution_trend) >= 2:
                recent_avg = statistics.mean([d["value"] for d in execution_trend[-5:]])
                earlier_avg = statistics.mean([d["value"] for d in execution_trend[:5]])
                
                if recent_avg > earlier_avg * 1.2:  # 20% increase
                    recommendations.append("Execution times are increasing. Monitor for performance degradation.")
        
        if not recommendations:
            recommendations.append("Performance looks good! Continue monitoring for any changes.")
        
        return recommendations

class PerformanceMonitor:
    """Main performance monitoring system."""
    
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.metrics_collector = MetricsCollector(storage_path)
        self.alert_manager = AlertManager(self.metrics_collector)
        self.analytics_engine = AnalyticsEngine(self.metrics_collector)
        
        # Start background collection
        self.metrics_collector.start_collection()
    
    def record_metric(self, skill_id: str, metric_type: MetricType, 
                     value: float, context: Dict[str, Any] = None,
                     agent_framework: str | None = None):
        """Record a performance metric."""
        metric = PerformanceMetric(
            skill_id=skill_id,
            metric_type=metric_type,
            value=value,
            timestamp=datetime.now(),
            context=context or {},
            agent_framework=agent_framework
        )
        self.metrics_collector.record_metric(metric)
    
    def get_skill_performance(self, skill_id: str) -> Dict[str, Any]:
        """Get performance statistics for a skill."""
        return self.metrics_collector.get_skill_stats(skill_id)
    
    def generate_report(self, days: int = 7) -> PerformanceReport:
        """Generate a performance report for the last N days."""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        return self.analytics_engine.generate_performance_report((start_time, end_time))
    
    def add_alert_callback(self, callback: Callable[[Alert], None]):
        """Add a callback for alerts."""
        self.alert_manager.add_alert_callback(callback)
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts."""
        return self.alert_manager.get_active_alerts()
    
    def resolve_alert(self, alert_id: str):
        """Resolve an alert."""
        self.alert_manager.resolve_alert(alert_id)
    
    def stop(self):
        """Stop the performance monitor."""
        self.metrics_collector.stop_collection()

# Global performance monitor instance
global_performance_monitor = PerformanceMonitor(Path("telemetry"))

def record_performance_metric(skill_id: str, metric_type: MetricType, 
                            value: float, context: Dict[str, Any] = None,
                            agent_framework: str | None = None):
    """Record a performance metric using the global monitor."""
    global_performance_monitor.record_metric(skill_id, metric_type, value, context, agent_framework)

def get_skill_performance_stats(skill_id: str) -> Dict[str, Any]:
    """Get performance statistics for a skill using the global monitor."""
    return global_performance_monitor.get_skill_performance(skill_id)

def generate_performance_report(days: int = 7) -> PerformanceReport:
    """Generate a performance report using the global monitor."""
    return global_performance_monitor.generate_report(days)

if __name__ == "__main__":
    # Example usage
    async def main():
        print("Performance Monitoring System Examples")
        
        # Record some sample metrics
        global_performance_monitor.record_metric(
            "test_skill",
            MetricType.EXECUTION_TIME,
            2.5,
            {"test": "sample"},
            "autogen"
        )
        
        global_performance_monitor.record_metric(
            "test_skill",
            MetricType.SUCCESS_RATE,
            0.95,
            {"test": "sample"},
            "autogen"
        )
        
        # Get performance stats
        stats = global_performance_monitor.get_skill_performance("test_skill")
        print(f"Skill stats: {stats}")
        
        # Generate report
        report = global_performance_monitor.generate_report(1)
        print(f"Report generated: {report.report_id}")
        
        # Get alerts
        alerts = global_performance_monitor.get_active_alerts()
        print(f"Active alerts: {len(alerts)}")
        
        print("Performance monitoring system working correctly")
    
    asyncio.run(main())
