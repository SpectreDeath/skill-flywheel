#!/usr/bin/env python3
"""
Skill: infrastructure-monitoring
Domain: devops
Description: Infrastructure monitoring and alerting system for DevOps
"""

import asyncio
import logging
import time
import uuid
import json
import psutil
import requests
import socket
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import statistics
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types of metrics"""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    PROCESS = "process"
    CUSTOM = "custom"

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertStatus(Enum):
    """Alert statuses"""
    ACTIVE = "active"
    RESOLVED = "resolved"
    ACKNOWLEDGED = "acknowledged"

class ServiceStatus(Enum):
    """Service status"""
    UP = "up"
    DOWN = "down"
    DEGRADED = "degraded"

@dataclass
class Metric:
    """Represents a system metric"""
    metric_id: str
    name: str
    metric_type: MetricType
    value: float
    unit: str
    timestamp: float
    tags: Dict[str, str]

@dataclass
class Alert:
    """Represents an alert"""
    alert_id: str
    name: str
    description: str
    severity: AlertSeverity
    status: AlertStatus
    metric_name: str
    threshold: float
    current_value: float
    triggered_at: float
    resolved_at: Optional[float]
    acknowledged_at: Optional[float]
    acknowledged_by: Optional[str]

@dataclass
class Service:
    """Represents a monitored service"""
    service_id: str
    name: str
    url: Optional[str]
    port: Optional[int]
    process_name: Optional[str]
    status: ServiceStatus
    last_check: float
    response_time: Optional[float]
    error_count: int

@dataclass
class Dashboard:
    """Represents a monitoring dashboard"""
    dashboard_id: str
    name: str
    description: str
    widgets: List[Dict[str, Any]]
    refresh_interval: int
    created_at: float

class InfrastructureMonitor:
    """Infrastructure monitoring and alerting system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the infrastructure monitor
        
        Args:
            config: Configuration dictionary with:
                - collection_interval: Metric collection interval in seconds
                - alert_check_interval: Alert check interval in seconds
                - retention_period: Data retention period in hours
                - alert_webhook: Webhook URL for alerts
        """
        self.collection_interval = config.get("collection_interval", 30)
        self.alert_check_interval = config.get("alert_check_interval", 60)
        self.retention_period = config.get("retention_period", 24)  # hours
        self.alert_webhook = config.get("alert_webhook", "")
        
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.alerts: Dict[str, Alert] = {}
        self.services: Dict[str, Service] = {}
        self.dashboards: Dict[str, Dashboard] = {}
        
        self.alert_rules: Dict[str, Dict[str, Any]] = {}
        self.metric_history: Dict[str, List[Metric]] = defaultdict(list)
        
        self.monitoring_stats = {
            "total_metrics": 0,
            "active_alerts": 0,
            "resolved_alerts": 0,
            "monitored_services": 0,
            "uptime_percentage": 0.0
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Start background monitoring
        self._monitoring_task = asyncio.create_task(self._monitoring_loop())
        self._alert_task = asyncio.create_task(self._alert_loop())
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    def add_metric(self, name: str, value: float, metric_type: MetricType, unit: str = "", tags: Optional[Dict[str, str]] = None) -> str:
        """
        Add a metric reading
        
        Args:
            name: Metric name
            value: Metric value
            metric_type: Type of metric
            unit: Unit of measurement
            tags: Additional tags
            
        Returns:
            Metric ID
        """
        metric_id = str(uuid.uuid4())
        
        metric = Metric(
            metric_id=metric_id,
            name=name,
            metric_type=metric_type,
            value=value,
            unit=unit,
            timestamp=time.time(),
            tags=tags or {}
        )
        
        self.metrics[name].append(metric)
        self.metric_history[name].append(metric)
        self.monitoring_stats["total_metrics"] += 1
        
        return metric_id
    
    def create_alert_rule(self,
                         name: str,
                         description: str,
                         metric_name: str,
                         threshold: float,
                         severity: AlertSeverity,
                         condition: str = "greater_than") -> str:
        """
        Create an alert rule
        
        Args:
            name: Alert rule name
            description: Alert rule description
            metric_name: Name of metric to monitor
            threshold: Alert threshold
            severity: Alert severity
            condition: Condition (greater_than, less_than, equals)
            
        Returns:
            Alert rule ID
        """
        rule_id = str(uuid.uuid4())
        
        self.alert_rules[rule_id] = {
            "name": name,
            "description": description,
            "metric_name": metric_name,
            "threshold": threshold,
            "severity": severity,
            "condition": condition,
            "created_at": time.time()
        }
        
        self.logger.info(f"Created alert rule: {rule_id}")
        return rule_id
    
    def add_service(self,
                   name: str,
                   url: Optional[str] = None,
                   port: Optional[int] = None,
                   process_name: Optional[str] = None) -> str:
        """
        Add a service to monitor
        
        Args:
            name: Service name
            url: Service URL (optional)
            port: Service port (optional)
            process_name: Process name (optional)
            
        Returns:
            Service ID
        """
        service_id = str(uuid.uuid4())
        
        service = Service(
            service_id=service_id,
            name=name,
            url=url,
            port=port,
            process_name=process_name,
            status=ServiceStatus.UP,
            last_check=0.0,
            response_time=None,
            error_count=0
        )
        
        self.services[service_id] = service
        self.monitoring_stats["monitored_services"] += 1
        
        self.logger.info(f"Added service: {service_id}")
        return service_id
    
    def create_dashboard(self,
                        name: str,
                        description: str,
                        widgets: List[Dict[str, Any]],
                        refresh_interval: int = 30) -> str:
        """
        Create a monitoring dashboard
        
        Args:
            name: Dashboard name
            description: Dashboard description
            widgets: List of dashboard widgets
            refresh_interval: Refresh interval in seconds
            
        Returns:
            Dashboard ID
        """
        dashboard_id = str(uuid.uuid4())
        
        dashboard = Dashboard(
            dashboard_id=dashboard_id,
            name=name,
            description=description,
            widgets=widgets,
            refresh_interval=refresh_interval,
            created_at=time.time()
        )
        
        self.dashboards[dashboard_id] = dashboard
        
        self.logger.info(f"Created dashboard: {dashboard_id}")
        return dashboard_id
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        return {
            "cpu": {
                "usage_percent": cpu_percent,
                "count": psutil.cpu_count(),
                "load_avg": list(psutil.getloadavg()) if hasattr(psutil, 'getloadavg') else []
            },
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "used_percent": memory.percent,
                "free_gb": round(memory.free / (1024**3), 2)
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "usage_percent": round((disk.used / disk.total) * 100, 2)
            },
            "network": {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            },
            "timestamp": time.time()
        }
    
    def get_service_status(self, service_id: str) -> Optional[Dict[str, Any]]:
        """Get service status"""
        if service_id not in self.services:
            return None
        
        service = self.services[service_id]
        
        return {
            "service_id": service.service_id,
            "name": service.name,
            "status": service.status.value,
            "last_check": service.last_check,
            "response_time": service.response_time,
            "error_count": service.error_count,
            "url": service.url,
            "port": service.port,
            "process_name": service.process_name
        }
    
    def get_alerts(self, status: Optional[AlertStatus] = None) -> List[Dict[str, Any]]:
        """Get alerts"""
        alerts = list(self.alerts.values())
        
        if status:
            alerts = [a for a in alerts if a.status == status]
        
        return [
            {
                "alert_id": a.alert_id,
                "name": a.name,
                "description": a.description,
                "severity": a.severity.value,
                "status": a.status.value,
                "metric_name": a.metric_name,
                "threshold": a.threshold,
                "current_value": a.current_value,
                "triggered_at": a.triggered_at,
                "resolved_at": a.resolved_at,
                "acknowledged_at": a.acknowledged_at,
                "acknowledged_by": a.acknowledged_by
            }
            for a in alerts
        ]
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert"""
        if alert_id not in self.alerts:
            return False
        
        alert = self.alerts[alert_id]
        alert.status = AlertStatus.ACKNOWLEDGED
        alert.acknowledged_at = time.time()
        alert.acknowledged_by = acknowledged_by
        
        self.logger.info(f"Alert acknowledged: {alert_id} by {acknowledged_by}")
        return True
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert"""
        if alert_id not in self.alerts:
            return False
        
        alert = self.alerts[alert_id]
        alert.status = AlertStatus.RESOLVED
        alert.resolved_at = time.time()
        
        self.monitoring_stats["resolved_alerts"] += 1
        self.monitoring_stats["active_alerts"] -= 1
        
        self.logger.info(f"Alert resolved: {alert_id}")
        return True
    
    def get_monitoring_stats(self) -> Dict[str, Any]:
        """Get monitoring statistics"""
        return {
            "total_metrics": self.monitoring_stats["total_metrics"],
            "active_alerts": self.monitoring_stats["active_alerts"],
            "resolved_alerts": self.monitoring_stats["resolved_alerts"],
            "monitored_services": self.monitoring_stats["monitored_services"],
            "uptime_percentage": self._calculate_uptime_percentage(),
            "collection_interval": self.collection_interval,
            "alert_check_interval": self.alert_check_interval,
            "retention_period": self.retention_period
        }
    
    async def _monitoring_loop(self):
        """Background monitoring loop"""
        while True:
            try:
                # Collect system metrics
                system_metrics = self.get_system_metrics()
                
                # Add CPU metrics
                self.add_metric(
                    name="cpu_usage",
                    value=system_metrics["cpu"]["usage_percent"],
                    metric_type=MetricType.CPU,
                    unit="%"
                )
                
                # Add memory metrics
                self.add_metric(
                    name="memory_usage",
                    value=system_metrics["memory"]["used_percent"],
                    metric_type=MetricType.MEMORY,
                    unit="%"
                )
                
                # Add disk metrics
                self.add_metric(
                    name="disk_usage",
                    value=system_metrics["disk"]["usage_percent"],
                    metric_type=MetricType.DISK,
                    unit="%"
                )
                
                # Monitor services
                await self._check_services()
                
                await asyncio.sleep(self.collection_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(self.collection_interval)
    
    async def _check_services(self):
        """Check service status"""
        for service_id, service in self.services.items():
            try:
                if service.url:
                    await self._check_http_service(service)
                elif service.port:
                    await self._check_tcp_service(service)
                elif service.process_name:
                    await self._check_process_service(service)
                
                service.last_check = time.time()
                
            except Exception as e:
                self.logger.error(f"Error checking service {service.name}: {e}")
                service.error_count += 1
                service.status = ServiceStatus.DOWN
    
    async def _check_http_service(self, service: Service):
        """Check HTTP service"""
        try:
            start_time = time.time()
            response = requests.get(service.url, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                service.status = ServiceStatus.UP
                service.response_time = response_time
                service.error_count = 0
            else:
                service.status = ServiceStatus.DEGRADED
                service.error_count += 1
                
        except requests.RequestException:
            service.status = ServiceStatus.DOWN
            service.error_count += 1
    
    async def _check_tcp_service(self, service: Service):
        """Check TCP service"""
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((socket.gethostname(), service.port))
            response_time = time.time() - start_time
            sock.close()
            
            if result == 0:
                service.status = ServiceStatus.UP
                service.response_time = response_time
                service.error_count = 0
            else:
                service.status = ServiceStatus.DOWN
                service.error_count += 1
                
        except Exception:
            service.status = ServiceStatus.DOWN
            service.error_count += 1
    
    async def _check_process_service(self, service: Service):
        """Check process service"""
        try:
            # Check if process is running
            process_found = False
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == service.process_name:
                    process_found = True
                    break
            
            if process_found:
                service.status = ServiceStatus.UP
                service.error_count = 0
            else:
                service.status = ServiceStatus.DOWN
                service.error_count += 1
                
        except Exception:
            service.status = ServiceStatus.DOWN
            service.error_count += 1
    
    async def _alert_loop(self):
        """Background alert checking loop"""
        while True:
            try:
                await self._check_alert_rules()
                await asyncio.sleep(self.alert_check_interval)
                
            except Exception as e:
                self.logger.error(f"Error in alert loop: {e}")
                await asyncio.sleep(self.alert_check_interval)
    
    async def _check_alert_rules(self):
        """Check alert rules against current metrics"""
        current_time = time.time()
        
        for rule_id, rule in self.alert_rules.items():
            metric_name = rule["metric_name"]
            threshold = rule["threshold"]
            severity = rule["severity"]
            condition = rule["condition"]
            
            # Get latest metric value
            if metric_name in self.metrics and self.metrics[metric_name]:
                latest_metric = self.metrics[metric_name][-1]
                current_value = latest_metric.value
                
                # Check condition
                should_alert = False
                if condition == "greater_than" and current_value > threshold:
                    should_alert = True
                elif condition == "less_than" and current_value < threshold:
                    should_alert = True
                elif condition == "equals" and current_value == threshold:
                    should_alert = True
                
                # Create alert if needed
                if should_alert:
                    await self._create_alert(rule, current_value)
                else:
                    # Check if existing alert should be resolved
                    await self._resolve_alert_if_needed(rule_id, current_value)
    
    async def _create_alert(self, rule: Dict[str, Any], current_value: float):
        """Create an alert"""
        alert_id = str(uuid.uuid4())
        
        alert = Alert(
            alert_id=alert_id,
            name=rule["name"],
            description=rule["description"],
            severity=rule["severity"],
            status=AlertStatus.ACTIVE,
            metric_name=rule["metric_name"],
            threshold=rule["threshold"],
            current_value=current_value,
            triggered_at=time.time(),
            resolved_at=None,
            acknowledged_at=None,
            acknowledged_by=None
        )
        
        self.alerts[alert_id] = alert
        self.monitoring_stats["active_alerts"] += 1
        
        # Send webhook notification
        if self.alert_webhook:
            await self._send_alert_webhook(alert)
        
        self.logger.warning(f"Alert created: {alert_id} - {rule['name']}")
    
    async def _resolve_alert_if_needed(self, rule_id: str, current_value: float):
        """Resolve alert if condition is no longer met"""
        # Find active alerts for this rule
        for alert_id, alert in list(self.alerts.items()):
            if (alert.status == AlertStatus.ACTIVE and 
                alert.metric_name == self.alert_rules[rule_id]["metric_name"] and
                alert.current_value == current_value):
                
                # Check if alert should be resolved (simple hysteresis)
                if abs(current_value - alert.threshold) < 0.1:
                    await self._resolve_alert(alert_id)
    
    async def _send_alert_webhook(self, alert: Alert):
        """Send alert notification via webhook"""
        try:
            payload = {
                "alert_id": alert.alert_id,
                "name": alert.name,
                "description": alert.description,
                "severity": alert.severity.value,
                "status": alert.status.value,
                "metric_name": alert.metric_name,
                "threshold": alert.threshold,
                "current_value": alert.current_value,
                "triggered_at": alert.triggered_at
            }
            
            response = requests.post(self.alert_webhook, json=payload, timeout=10)
            response.raise_for_status()
            
        except Exception as e:
            self.logger.error(f"Failed to send alert webhook: {e}")
    
    async def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            try:
                await self._cleanup_old_data()
                await asyncio.sleep(3600)  # Run every hour
                
            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(3600)
    
    async def _cleanup_old_data(self):
        """Clean up old metric data"""
        cutoff_time = time.time() - (self.retention_period * 3600)
        
        for metric_name, metrics in self.metric_history.items():
            # Keep only recent metrics
            self.metric_history[metric_name] = [
                m for m in metrics if m.timestamp > cutoff_time
            ]
    
    def _calculate_uptime_percentage(self) -> float:
        """Calculate overall uptime percentage"""
        if not self.services:
            return 100.0
        
        total_services = len(self.services)
        up_services = sum(1 for s in self.services.values() if s.status == ServiceStatus.UP)
        
        return (up_services / total_services) * 100.0

# Global infrastructure monitor instance
_monitor = InfrastructureMonitor({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "get_metrics", "create_alert_rule", "add_service", 
                     "get_service_status", "get_alerts", "acknowledge_alert", 
                     "resolve_alert", "get_stats", "create_dashboard"
            - metric_data: Metric information
            - alert_data: Alert rule configuration
            - service_data: Service configuration
            - dashboard_data: Dashboard configuration
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "get_metrics":
            metrics = _monitor.get_system_metrics()
            
            return {
                "result": metrics,
                "metadata": {
                    "action": "get_metrics",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_alert_rule":
            alert_data = payload.get("alert_data", {})
            
            rule_id = _monitor.create_alert_rule(
                name=alert_data.get("name", "Alert Rule"),
                description=alert_data.get("description", ""),
                metric_name=alert_data.get("metric_name", ""),
                threshold=alert_data.get("threshold", 0.0),
                severity=AlertSeverity(alert_data.get("severity", "warning")),
                condition=alert_data.get("condition", "greater_than")
            )
            
            return {
                "result": {
                    "rule_id": rule_id,
                    "message": f"Created alert rule: {rule_id}"
                },
                "metadata": {
                    "action": "create_alert_rule",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "add_service":
            service_data = payload.get("service_data", {})
            
            service_id = _monitor.add_service(
                name=service_data.get("name", "Service"),
                url=service_data.get("url"),
                port=service_data.get("port"),
                process_name=service_data.get("process_name")
            )
            
            return {
                "result": {
                    "service_id": service_id,
                    "message": f"Added service: {service_id}"
                },
                "metadata": {
                    "action": "add_service",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_service_status":
            service_id = payload.get("service_id", "")
            status = _monitor.get_service_status(service_id)
            
            return {
                "result": status,
                "metadata": {
                    "action": "get_service_status",
                    "timestamp": datetime.now().isoformat(),
                    "service_id": service_id
                }
            }
        
        elif action == "get_alerts":
            status = payload.get("status")
            if status:
                status = AlertStatus(status)
            
            alerts = _monitor.get_alerts(status)
            
            return {
                "result": alerts,
                "metadata": {
                    "action": "get_alerts",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "acknowledge_alert":
            alert_data = payload.get("alert_data", {})
            
            success = _monitor.acknowledge_alert(
                alert_id=alert_data.get("alert_id", ""),
                acknowledged_by=alert_data.get("acknowledged_by", "system")
            )
            
            return {
                "result": {
                    "success": success,
                    "message": f"Alert acknowledged: {alert_data.get('alert_id', '')}"
                },
                "metadata": {
                    "action": "acknowledge_alert",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "resolve_alert":
            alert_id = payload.get("alert_id", "")
            success = _monitor.resolve_alert(alert_id)
            
            return {
                "result": {
                    "success": success,
                    "message": f"Alert resolved: {alert_id}"
                },
                "metadata": {
                    "action": "resolve_alert",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_stats":
            stats = _monitor.get_monitoring_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "create_dashboard":
            dashboard_data = payload.get("dashboard_data", {})
            
            dashboard_id = _monitor.create_dashboard(
                name=dashboard_data.get("name", "Dashboard"),
                description=dashboard_data.get("description", ""),
                widgets=dashboard_data.get("widgets", []),
                refresh_interval=dashboard_data.get("refresh_interval", 30)
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
        logger.error(f"Error in infrastructure_monitoring: {e}")
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
    """Example of how to use the infrastructure monitoring skill"""
    
    # Get system metrics
    metrics = await invoke({"action": "get_metrics"})
    print(f"System metrics: {metrics['result']}")
    
    # Create alert rules
    cpu_alert = await invoke({
        "action": "create_alert_rule",
        "alert_data": {
            "name": "High CPU Usage",
            "description": "Alert when CPU usage exceeds 80%",
            "metric_name": "cpu_usage",
            "threshold": 80.0,
            "severity": "warning",
            "condition": "greater_than"
        }
    })
    
    memory_alert = await invoke({
        "action": "create_alert_rule",
        "alert_data": {
            "name": "High Memory Usage",
            "description": "Alert when memory usage exceeds 90%",
            "metric_name": "memory_usage",
            "threshold": 90.0,
            "severity": "critical",
            "condition": "greater_than"
        }
    })
    
    print(f"Created alert rules: {cpu_alert['result']['rule_id']}, {memory_alert['result']['rule_id']}")
    
    # Add services to monitor
    web_service = await invoke({
        "action": "add_service",
        "service_data": {
            "name": "Web Server",
            "url": "http://localhost:8080",
            "port": 8080
        }
    })
    
    db_service = await invoke({
        "action": "add_service",
        "service_data": {
            "name": "Database",
            "process_name": "postgres"
        }
    })
    
    print(f"Added services: {web_service['result']['service_id']}, {db_service['result']['service_id']}")
    
    # Create dashboard
    dashboard = await invoke({
        "action": "create_dashboard",
        "dashboard_data": {
            "name": "System Overview",
            "description": "Overview of system health",
            "widgets": [
                {"type": "cpu_chart", "title": "CPU Usage"},
                {"type": "memory_chart", "title": "Memory Usage"},
                {"type": "service_status", "title": "Service Status"}
            ],
            "refresh_interval": 30
        }
    })
    
    print(f"Created dashboard: {dashboard['result']['dashboard_id']}")
    
    # Get monitoring statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Monitoring stats: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())