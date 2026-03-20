#!/usr/bin/env python3
"""
Skill: cloud-monitoring-system
Domain: cloud_engineering
Description: Cloud monitoring and observability system for infrastructure and applications
"""

import asyncio
import logging
import statistics
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types of metrics"""
    COUNTER = "counter"        # Monotonically increasing
    GAUGE = "gauge"           # Point-in-time value
    HISTOGRAM = "histogram"   # Distribution of values
    TIMER = "timer"           # Time-based measurements

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class AlertStatus(Enum):
    """Alert statuses"""
    FIRING = "firing"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"

@dataclass
class Metric:
    """Represents a metric"""
    metric_id: str
    name: str
    metric_type: MetricType
    value: float
    timestamp: float
    tags: Dict[str, str]
    unit: str
    source: str

@dataclass
class AlertRule:
    """Represents an alert rule"""
    rule_id: str
    name: str
    description: str
    metric_name: str
    condition: str  # e.g., "value > 90"
    severity: AlertSeverity
    threshold: float
    evaluation_window: int  # seconds
    cooldown_period: int    # seconds
    enabled: bool
    created_at: float

@dataclass
class Alert:
    """Represents an alert"""
    alert_id: str
    rule_id: str
    metric_name: str
    severity: AlertSeverity
    status: AlertStatus
    message: str
    triggered_at: float
    resolved_at: float | None
    tags: Dict[str, str]
    value: float

@dataclass
class Dashboard:
    """Represents a dashboard"""
    dashboard_id: str
    name: str
    description: str
    widgets: List[Dict[str, Any]]
    tags: List[str]
    created_at: float
    last_modified: float

class CloudMonitoringSystem:
    """Cloud monitoring and observability system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the monitoring system
        
        Args:
            config: Configuration dictionary with:
                - retention_days: Data retention period
                - evaluation_interval: How often to evaluate alerts
                - max_metrics: Maximum number of metrics to store
        """
        self.retention_days = config.get("retention_days", 30)
        self.evaluation_interval = config.get("evaluation_interval", 60)
        self.max_metrics = config.get("max_metrics", 100000)
        
        self.metrics: Dict[str, List[Metric]] = {}
        self.alert_rules: Dict[str, AlertRule] = {}
        self.alerts: Dict[str, Alert] = {}
        self.dashboards: Dict[str, Dashboard] = {}
        self.active_alerts: Dict[str, Alert] = {}
        
        self.metric_stats = {
            "total_metrics": 0,
            "metrics_per_second": 0.0,
            "storage_size": 0,
            "retention_days": self.retention_days
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Start background tasks
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        self._evaluation_task = asyncio.create_task(self._evaluation_loop())
    
    def record_metric(self, 
                     name: str,
                     value: float,
                     metric_type: MetricType = MetricType.GAUGE,
                     tags: Dict[str, str] | None = None,
                     unit: str = "",
                     source: str = "unknown") -> str:
        """
        Record a metric
        
        Args:
            name: Metric name
            value: Metric value
            metric_type: Type of metric
            tags: Additional tags
            unit: Unit of measurement
            source: Source of the metric
            
        Returns:
            Metric ID
        """
        metric_id = str(uuid.uuid4())
        
        metric = Metric(
            metric_id=metric_id,
            name=name,
            metric_type=metric_type,
            value=value,
            timestamp=time.time(),
            tags=tags or {},
            unit=unit,
            source=source
        )
        
        # Store metric
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append(metric)
        self.metric_stats["total_metrics"] += 1
        self.metric_stats["storage_size"] += len(str(metric))
        
        # Maintain storage limits
        self._maintain_storage_limits(name)
        
        # Evaluate alert rules
        self._evaluate_alert_rules(name, value)
        
        return metric_id
    
    def create_alert_rule(self, 
                         name: str,
                         description: str,
                         metric_name: str,
                         condition: str,
                         severity: AlertSeverity,
                         threshold: float,
                         evaluation_window: int = 300,
                         cooldown_period: int = 600) -> str:
        """
        Create an alert rule
        
        Args:
            name: Rule name
            description: Rule description
            metric_name: Name of metric to monitor
            condition: Alert condition
            severity: Alert severity
            threshold: Threshold value
            evaluation_window: Evaluation window in seconds
            cooldown_period: Cooldown period in seconds
            
        Returns:
            Rule ID
        """
        rule_id = str(uuid.uuid4())
        
        rule = AlertRule(
            rule_id=rule_id,
            name=name,
            description=description,
            metric_name=metric_name,
            condition=condition,
            severity=severity,
            threshold=threshold,
            evaluation_window=evaluation_window,
            cooldown_period=cooldown_period,
            enabled=True,
            created_at=time.time()
        )
        
        self.alert_rules[rule_id] = rule
        self.logger.info(f"Created alert rule: {rule_id}")
        
        return rule_id
    
    def create_dashboard(self, 
                        name: str,
                        description: str,
                        widgets: List[Dict[str, Any]],
                        tags: List[str] | None = None) -> str:
        """
        Create a dashboard
        
        Args:
            name: Dashboard name
            description: Dashboard description
            widgets: List of dashboard widgets
            tags: Dashboard tags
            
        Returns:
            Dashboard ID
        """
        dashboard_id = str(uuid.uuid4())
        
        dashboard = Dashboard(
            dashboard_id=dashboard_id,
            name=name,
            description=description,
            widgets=widgets,
            tags=tags or [],
            created_at=time.time(),
            last_modified=time.time()
        )
        
        self.dashboards[dashboard_id] = dashboard
        self.logger.info(f"Created dashboard: {dashboard_id}")
        
        return dashboard_id
    
    def get_metric_data(self, 
                       metric_name: str,
                       start_time: float | None = None,
                       end_time: float | None = None,
                       limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Get metric data
        
        Args:
            metric_name: Name of metric
            start_time: Start time (timestamp)
            end_time: End time (timestamp)
            limit: Maximum number of data points
            
        Returns:
            List of metric data points
        """
        if metric_name not in self.metrics:
            return []
        
        # Filter by time range
        if start_time is None:
            start_time = time.time() - (24 * 3600)  # Default: last 24 hours
        if end_time is None:
            end_time = time.time()
        
        filtered_metrics = [
            m for m in self.metrics[metric_name]
            if start_time <= m.timestamp <= end_time
        ]
        
        # Sort by timestamp and limit
        filtered_metrics.sort(key=lambda x: x.timestamp, reverse=True)
        filtered_metrics = filtered_metrics[:limit]
        
        return [
            {
                "timestamp": m.timestamp,
                "value": m.value,
                "tags": m.tags,
                "unit": m.unit,
                "source": m.source
            }
            for m in filtered_metrics
        ]
    
    def get_metric_stats(self, 
                        metric_name: str,
                        time_window: int = 3600) -> Dict[str, Any]:
        """
        Get statistical summary of a metric
        
        Args:
            metric_name: Name of metric
            time_window: Time window in seconds
            
        Returns:
            Statistical summary
        """
        if metric_name not in self.metrics:
            return {}
        
        end_time = time.time()
        start_time = end_time - time_window
        
        recent_metrics = [
            m for m in self.metrics[metric_name]
            if start_time <= m.timestamp <= end_time
        ]
        
        if not recent_metrics:
            return {}
        
        values = [m.value for m in recent_metrics]
        
        return {
            "metric_name": metric_name,
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0.0,
            "p95": self._percentile(values, 95),
            "p99": self._percentile(values, 99),
            "time_window": time_window,
            "start_time": start_time,
            "end_time": end_time
        }
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get all active alerts"""
        return [
            {
                "alert_id": alert.alert_id,
                "rule_name": self.alert_rules[alert.rule_id].name,
                "severity": alert.severity.value,
                "status": alert.status.value,
                "message": alert.message,
                "triggered_at": alert.triggered_at,
                "value": alert.value,
                "tags": alert.tags
            }
            for alert in self.active_alerts.values()
        ]
    
    def get_dashboard_data(self, dashboard_id: str) -> Dict[str, Any] | None:
        """Get dashboard data"""
        if dashboard_id not in self.dashboards:
            return None
        
        dashboard = self.dashboards[dashboard_id]
        
        # Process widgets to get current data
        widget_data = []
        for widget in dashboard.widgets:
            widget_type = widget.get("type")
            metric_name = widget.get("metric_name")
            
            if widget_type == "gauge" and metric_name:
                metric_data = self.get_metric_data(metric_name, limit=1)
                if metric_data:
                    widget_data.append({
                        "widget_id": widget.get("id"),
                        "type": widget_type,
                        "current_value": metric_data[0]["value"],
                        "unit": metric_data[0]["unit"]
                    })
            
            elif widget_type == "chart" and metric_name:
                time_window = widget.get("time_window", 3600)
                stats = self.get_metric_stats(metric_name, time_window)
                widget_data.append({
                    "widget_id": widget.get("id"),
                    "type": widget_type,
                    "stats": stats
                })
        
        return {
            "dashboard_id": dashboard.dashboard_id,
            "name": dashboard.name,
            "description": dashboard.description,
            "widgets": widget_data,
            "tags": dashboard.tags,
            "created_at": dashboard.created_at,
            "last_modified": dashboard.last_modified
        }
    
    def get_monitoring_stats(self) -> Dict[str, Any]:
        """Get monitoring system statistics"""
        total_alerts = len(self.alerts)
        firing_alerts = len([a for a in self.alerts.values() if a.status == AlertStatus.FIRING])
        resolved_alerts = len([a for a in self.alerts.values() if a.status == AlertStatus.RESOLVED])
        
        return {
            "total_metrics": self.metric_stats["total_metrics"],
            "metrics_per_second": self.metric_stats["metrics_per_second"],
            "storage_size_mb": self.metric_stats["storage_size"] / (1024 * 1024),
            "retention_days": self.metric_stats["retention_days"],
            "total_alert_rules": len(self.alert_rules),
            "total_alerts": total_alerts,
            "firing_alerts": firing_alerts,
            "resolved_alerts": resolved_alerts,
            "active_alerts": len(self.active_alerts),
            "total_dashboards": len(self.dashboards)
        }
    
    def _evaluate_alert_rules(self, metric_name: str, value: float):
        """Evaluate alert rules for a metric"""
        current_time = time.time()
        
        for rule in self.alert_rules.values():
            if rule.metric_name != metric_name or not rule.enabled:
                continue
            
            # Check condition
            condition_met = self._evaluate_condition(rule.condition, value, rule.threshold)
            
            if condition_met:
                self._trigger_alert(rule, value, current_time)
            else:
                self._resolve_alert(rule.rule_id, current_time)
    
    def _evaluate_condition(self, condition: str, value: float, threshold: float) -> bool:
        """Evaluate alert condition"""
        try:
            # Simple condition evaluation
            if condition == "value > threshold":
                return value > threshold
            elif condition == "value < threshold":
                return value < threshold
            elif condition == "value >= threshold":
                return value >= threshold
            elif condition == "value <= threshold":
                return value <= threshold
            elif condition == "value == threshold":
                return value == threshold
            else:
                # For complex conditions, you might use eval() with proper sandboxing
                return eval(condition.replace("value", str(value)).replace("threshold", str(threshold)))
        except:
            return False
    
    def _trigger_alert(self, rule: AlertRule, value: float, current_time: float):
        """Trigger an alert"""
        # Check if alert already exists and is not in cooldown
        existing_alert = None
        for alert in self.active_alerts.values():
            if alert.rule_id == rule.rule_id:
                existing_alert = alert
                break
        
        if existing_alert:
            # Check cooldown period
            if current_time - existing_alert.triggered_at < rule.cooldown_period:
                return
        
        # Create new alert
        alert_id = str(uuid.uuid4())
        
        alert = Alert(
            alert_id=alert_id,
            rule_id=rule.rule_id,
            metric_name=rule.metric_name,
            severity=rule.severity,
            status=AlertStatus.FIRING,
            message=f"Alert triggered: {rule.description} (value: {value})",
            triggered_at=current_time,
            resolved_at=None,
            tags={"rule_name": rule.name, "metric_name": rule.metric_name},
            value=value
        )
        
        self.alerts[alert_id] = alert
        self.active_alerts[alert_id] = alert
        
        self.logger.warning(f"Alert triggered: {alert_id} - {rule.name}")
    
    def _resolve_alert(self, rule_id: str, current_time: float):
        """Resolve an alert"""
        for alert_id, alert in list(self.active_alerts.items()):
            if alert.rule_id == rule_id:
                alert.status = AlertStatus.RESOLVED
                alert.resolved_at = current_time
                del self.active_alerts[alert_id]
                
                self.logger.info(f"Alert resolved: {alert_id}")
                break
    
    def _maintain_storage_limits(self, metric_name: str):
        """Maintain storage limits by removing old data"""
        if len(self.metrics[metric_name]) > self.max_metrics:
            # Remove oldest 10% of data
            remove_count = len(self.metrics[metric_name]) // 10
            self.metrics[metric_name] = self.metrics[metric_name][remove_count:]
    
    def _cleanup_loop(self):
        """Background cleanup task"""
        while True:
            try:
                self._cleanup_old_data()
                self._update_metrics_stats()
                time.sleep(3600)  # Run every hour
            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")
                time.sleep(3600)
    
    def _cleanup_old_data(self):
        """Clean up old metric data based on retention policy"""
        cutoff_time = time.time() - (self.retention_days * 24 * 3600)
        
        for metric_name in list(self.metrics.keys()):
            self.metrics[metric_name] = [
                m for m in self.metrics[metric_name]
                if m.timestamp > cutoff_time
            ]
            
            if not self.metrics[metric_name]:
                del self.metrics[metric_name]
    
    def _update_metrics_stats(self):
        """Update metrics statistics"""
        current_time = time.time()
        one_hour_ago = current_time - 3600
        
        recent_metrics = []
        for metric_list in self.metrics.values():
            recent_metrics.extend([
                m for m in metric_list
                if m.timestamp > one_hour_ago
            ])
        
        self.metric_stats["metrics_per_second"] = len(recent_metrics) / 3600.0
    
    def _evaluation_loop(self):
        """Background alert evaluation task"""
        while True:
            try:
                self._evaluate_all_alerts()
                time.sleep(self.evaluation_interval)
            except Exception as e:
                self.logger.error(f"Error in evaluation loop: {e}")
                time.sleep(self.evaluation_interval)
    
    def _evaluate_all_alerts(self):
        """Evaluate all alert rules"""
        current_time = time.time()
        
        for rule in self.alert_rules.values():
            if not rule.enabled:
                continue
            
            # Get recent metrics for this rule
            if rule.metric_name not in self.metrics:
                continue
            
            recent_metrics = [
                m for m in self.metrics[rule.metric_name]
                if current_time - m.timestamp <= rule.evaluation_window
            ]
            
            if recent_metrics:
                latest_value = recent_metrics[-1].value
                self._evaluate_alert_rules(rule.metric_name, latest_value)
    
    def _percentile(self, values: List[float], p: float) -> float:
        """Calculate percentile"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = int((p / 100) * len(sorted_values))
        return sorted_values[min(index, len(sorted_values) - 1)]

# Global monitoring system instance
_monitoring_system = CloudMonitoringSystem({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "record_metric", "create_alert", "create_dashboard", 
                     "get_metrics", "get_stats", "get_alerts", "get_dashboard"
            - metric_data: Metric data
            - alert_data: Alert rule data
            - dashboard_data: Dashboard data
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "record_metric":
            metric_data = payload.get("metric_data", {})
            
            metric_id = _monitoring_system.record_metric(
                name=metric_data.get("name", "unknown"),
                value=metric_data.get("value", 0.0),
                metric_type=MetricType(metric_data.get("metric_type", "gauge")),
                tags=metric_data.get("tags", {}),
                unit=metric_data.get("unit", ""),
                source=metric_data.get("source", "unknown")
            )
            
            return {
                "result": {
                    "metric_id": metric_id,
                    "message": f"Recorded metric: {metric_id}"
                },
                "metadata": {
                    "action": "record_metric",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_alert":
            alert_data = payload.get("alert_data", {})
            
            rule_id = _monitoring_system.create_alert_rule(
                name=alert_data.get("name", "Alert Rule"),
                description=alert_data.get("description", ""),
                metric_name=alert_data.get("metric_name", ""),
                condition=alert_data.get("condition", "value > threshold"),
                severity=AlertSeverity(alert_data.get("severity", "warning")),
                threshold=alert_data.get("threshold", 0.0),
                evaluation_window=alert_data.get("evaluation_window", 300),
                cooldown_period=alert_data.get("cooldown_period", 600)
            )
            
            return {
                "result": {
                    "rule_id": rule_id,
                    "message": f"Created alert rule: {rule_id}"
                },
                "metadata": {
                    "action": "create_alert",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_dashboard":
            dashboard_data = payload.get("dashboard_data", {})
            
            dashboard_id = _monitoring_system.create_dashboard(
                name=dashboard_data.get("name", "Dashboard"),
                description=dashboard_data.get("description", ""),
                widgets=dashboard_data.get("widgets", []),
                tags=dashboard_data.get("tags", [])
            )
            
            return {
                "result": {
                    "dashboard_id": dashboard_id,
                    "message": f"Created dashboard: {dashboard_id}"
                },
                "metadata": {
                    "action": "create_dashboard",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_metrics":
            metric_name = payload.get("metric_name", "")
            start_time = payload.get("start_time")
            end_time = payload.get("end_time")
            limit = payload.get("limit", 1000)
            
            data = _monitoring_system.get_metric_data(
                metric_name=metric_name,
                start_time=start_time,
                end_time=end_time,
                limit=limit
            )
            
            return {
                "result": data,
                "metadata": {
                    "action": "get_metrics",
                    "timestamp": datetime.now().isoformat(),
                    "metric_name": metric_name
                }
            }
        
        elif action == "get_stats":
            metric_name = payload.get("metric_name")
            time_window = payload.get("time_window", 3600)
            
            if metric_name:
                stats = _monitoring_system.get_metric_stats(metric_name, time_window)
            else:
                stats = _monitoring_system.get_monitoring_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat(),
                    "metric_name": metric_name
                }
            }
        
        elif action == "get_alerts":
            alerts = _monitoring_system.get_active_alerts()
            
            return {
                "result": alerts,
                "metadata": {
                    "action": "get_alerts",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_dashboard":
            dashboard_id = payload.get("dashboard_id", "")
            data = _monitoring_system.get_dashboard_data(dashboard_id)
            
            return {
                "result": data,
                "metadata": {
                    "action": "get_dashboard",
                    "timestamp": datetime.now().isoformat(),
                    "dashboard_id": dashboard_id
                }
            }
        
        else:
            return {
                "result": {
                    "error": f"Unknown action: {action}"
                },
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat()
                }
            }
    
    except Exception as e:
        logger.error(f"Error in cloud_monitoring_system: {e}")
        return {
            "result": {
                "error": str(e)
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat()
            }
        }

# Example usage function
async def example_usage():
    """Example of how to use the cloud monitoring system skill"""
    
    # Record some metrics
    await invoke({
        "action": "record_metric",
        "metric_data": {
            "name": "cpu_usage",
            "value": 75.5,
            "metric_type": "gauge",
            "unit": "%",
            "tags": {"service": "web", "instance": "i-12345"},
            "source": "cloudwatch"
        }
    })
    
    await invoke({
        "action": "record_metric",
        "metric_data": {
            "name": "memory_usage",
            "value": 85.2,
            "metric_type": "gauge",
            "unit": "%",
            "tags": {"service": "web", "instance": "i-12345"},
            "source": "cloudwatch"
        }
    })
    
    # Create an alert rule
    alert_id = await invoke({
        "action": "create_alert",
        "alert_data": {
            "name": "High CPU Usage",
            "description": "CPU usage is above 80%",
            "metric_name": "cpu_usage",
            "condition": "value > threshold",
            "severity": "warning",
            "threshold": 80.0,
            "evaluation_window": 300,
            "cooldown_period": 600
        }
    })
    
    print(f"Created alert rule: {alert_id['result']['rule_id']}")
    
    # Get monitoring statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Monitoring stats: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
