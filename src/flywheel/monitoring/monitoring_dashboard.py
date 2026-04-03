#!/usr/bin/env python3
"""
Enhanced Monitoring Dashboard for MCP Server

This dashboard provides:
- Real-time performance monitoring
- Skill usage analytics and visualization
- System health metrics
- Optimization recommendations
- Historical trend analysis
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

try:
    import GPUtil
except ImportError:
    GPUtil = None

from contextlib import asynccontextmanager
import psutil
import uvicorn
import yaml
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("monitoring_dashboard.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    dashboard = app.state.dashboard
    dashboard.background_tasks = []
    dashboard.background_tasks.append(
        asyncio.create_task(dashboard._data_collection_loop())
    )
    logger.info("Monitoring Dashboard started successfully")
    yield
    for task in dashboard.background_tasks:
        task.cancel()
    logger.info("Monitoring Dashboard shutting down")


# Dashboard Configuration
class DashboardConfig:
    """Dashboard configuration"""

    def __init__(self, config_path: str = "mcp_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        default_config = {
            "dashboard": {
                "host": "0.0.0.0",
                "port": 8080,
                "refresh_interval": 30,
                "history_days": 7,
                "chart_update_interval": 10,
            },
            "monitoring": {
                "enabled": True,
                "metrics_interval": 60,
                "log_level": "INFO",
            },
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path) as f:
                    user_config = yaml.safe_load(f)
                    if user_config and "dashboard" in user_config:
                        default_config["dashboard"].update(user_config["dashboard"])
            except Exception as e:
                logger.warning(f"Failed to load dashboard config: {e}")

        return default_config


# Dashboard Data Collector
class DashboardDataCollector:
    """Collects data for dashboard visualization"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.metrics_history: List[Dict[str, Any]] = []
        self.skill_usage_history: List[Dict[str, Any]] = []
        self.system_health_history: List[Dict[str, Any]] = []

    def collect_system_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics"""
        try:
            # CPU and Memory
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            # GPU (if available)
            gpu_usage = None
            if GPUtil is not None:
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        gpu_usage = gpus[0].load * 100
                except:
                    pass

            # Network and Process stats
            connections = len(psutil.net_connections())
            processes = len(psutil.pids())

            metrics = {
                "timestamp": datetime.now().isoformat(),
                "cpu_usage": cpu_usage,
                "memory_usage": memory.percent,
                "memory_total": memory.total / (1024**3),  # GB
                "memory_available": memory.available / (1024**3),  # GB
                "disk_usage": disk.percent,
                "disk_total": disk.total / (1024**3),  # GB
                "disk_free": disk.free / (1024**3),  # GB
                "gpu_usage": gpu_usage,
                "active_connections": connections,
                "process_count": processes,
                "load_average": os.getloadavg()
                if hasattr(os, "getloadavg")
                else [0, 0, 0],
            }

            self.metrics_history.append(metrics)

            # Keep only recent history
            max_history = (
                self.config["dashboard"]["history_days"]
                * 24
                * 60
                * 60
                // self.config["monitoring"]["metrics_interval"]
            )
            if len(self.metrics_history) > max_history:
                self.metrics_history.pop(0)

            return metrics

        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            return {}

    def collect_skill_metrics(self) -> Dict[str, Any]:
        """Collect skill usage metrics"""
        # NOTE: This is a stub implementation that returns empty data.
        # Integration with MCP server's telemetry (EnhancedSkillManager) is required.
        skill_metrics = {
            "timestamp": datetime.now().isoformat(),
            "status": "stub",
            "message": "Skill metrics integration not implemented - requires connection to EnhancedSkillManager",
            "total_skills": 0,
            "loaded_skills": 0,
            "active_skills": 0,
            "skill_performance": [],
            "usage_patterns": [],
            "optimization_status": {},
        }

        self.skill_usage_history.append(skill_metrics)

        # Keep only recent history
        if len(self.skill_usage_history) > 1000:
            self.skill_usage_history.pop(0)

        return skill_metrics

    def get_health_status(self) -> Dict[str, Any]:
        """Get current system health status"""
        latest_metrics = self.metrics_history[-1] if self.metrics_history else {}

        health_status = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "issues": [],
            "metrics": latest_metrics,
            "recommendations": [],
        }

        # Check for issues
        if latest_metrics.get("cpu_usage", 0) > 80:
            health_status["status"] = "warning"
            health_status["issues"].append(
                f"High CPU usage: {latest_metrics['cpu_usage']:.1f}%"
            )

        if latest_metrics.get("memory_usage", 0) > 80:
            health_status["status"] = "warning"
            health_status["issues"].append(
                f"High memory usage: {latest_metrics['memory_usage']:.1f}%"
            )

        if latest_metrics.get("disk_usage", 0) > 90:
            health_status["status"] = "warning"
            health_status["issues"].append(
                f"High disk usage: {latest_metrics['disk_usage']:.1f}%"
            )

        # Generate recommendations
        if health_status["status"] == "warning":
            health_status["recommendations"] = [
                "Consider reducing concurrent requests",
                "Monitor memory usage patterns",
                "Check for memory leaks in long-running processes",
            ]

        self.system_health_history.append(health_status)

        # Keep only recent history
        if len(self.system_health_history) > 1000:
            self.system_health_history.pop(0)

        return health_status

    def get_performance_trends(self) -> Dict[str, Any]:
        """Get performance trends over time"""
        if not self.metrics_history:
            return {"error": "No metrics data available"}

        # Calculate trends for the last 24 hours
        cutoff_time = datetime.now() - timedelta(hours=24)
        recent_metrics = [
            m
            for m in self.metrics_history
            if datetime.fromisoformat(m["timestamp"]) > cutoff_time
        ]

        if not recent_metrics:
            return {"error": "No recent metrics data available"}

        # Calculate averages and trends
        cpu_values = [m["cpu_usage"] for m in recent_metrics]
        memory_values = [m["memory_usage"] for m in recent_metrics]

        trends = {
            "timestamp": datetime.now().isoformat(),
            "time_range": "24 hours",
            "cpu": {
                "average": sum(cpu_values) / len(cpu_values),
                "min": min(cpu_values),
                "max": max(cpu_values),
                "current": cpu_values[-1] if cpu_values else 0,
            },
            "memory": {
                "average": sum(memory_values) / len(memory_values),
                "min": min(memory_values),
                "max": max(memory_values),
                "current": memory_values[-1] if memory_values else 0,
            },
            "data_points": len(recent_metrics),
        }

        return trends


# Dashboard Web Application
class MonitoringDashboard:
    """Web-based monitoring dashboard"""

    def __init__(self):
        self.config = DashboardConfig()
        self.app = FastAPI(
            title="MCP Server Monitoring Dashboard",
            description="Real-time monitoring and analytics for MCP Server",
            version="1.0.0",
            lifespan=lifespan,
        )

        self.app.state.dashboard = self

        # Setup CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Initialize data collector
        self.data_collector = DashboardDataCollector(self.config.config)

        # Setup templates and static files
        self.templates_dir = Path(__file__).parent / "templates"
        self.static_dir = Path(__file__).parent / "static"

        if self.templates_dir.exists():
            self.templates = Jinja2Templates(directory=str(self.templates_dir))
        else:
            self.templates = None

        if self.static_dir.exists():
            self.app.mount(
                "/static", StaticFiles(directory=str(self.static_dir)), name="static"
            )

        # Setup routes
        self._setup_routes()

        # Background tasks
        self.background_tasks = []

    def _setup_routes(self):
        """Setup dashboard routes"""

        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard_home(request: Request):
            """Main dashboard page"""
            if self.templates:
                return self.templates.TemplateResponse(
                    "dashboard.html", {"request": request}
                )
            else:
                return HTMLResponse(self._generate_dashboard_html())

        @self.app.get("/api/system/metrics", response_class=JSONResponse)
        async def get_system_metrics():
            """Get current system metrics"""
            return self.data_collector.collect_system_metrics()

        @self.app.get("/api/system/health", response_class=JSONResponse)
        async def get_system_health():
            """Get system health status"""
            return self.data_collector.get_health_status()

        @self.app.get("/api/system/trends", response_class=JSONResponse)
        async def get_performance_trends():
            """Get performance trends"""
            return self.data_collector.get_performance_trends()

        @self.app.get("/api/skills/metrics", response_class=JSONResponse)
        async def get_skill_metrics():
            """Get skill usage metrics"""
            return self.data_collector.collect_skill_metrics()

        @self.app.get("/api/history/metrics", response_class=JSONResponse)
        async def get_metrics_history(hours: int = 24):
            """Get historical metrics"""
            cutoff_time = datetime.now() - timedelta(hours=hours)
            history = [
                m
                for m in self.data_collector.metrics_history
                if datetime.fromisoformat(m["timestamp"]) > cutoff_time
            ]
            return {"history": history, "count": len(history)}

        @self.app.get("/api/summary", response_class=JSONResponse)
        async def get_dashboard_summary():
            """Get dashboard summary"""
            current_metrics = self.data_collector.collect_system_metrics()
            health_status = self.data_collector.get_health_status()
            trends = self.data_collector.get_performance_trends()

            summary = {
                "timestamp": datetime.now().isoformat(),
                "current_metrics": current_metrics,
                "health_status": health_status,
                "trends": trends,
                "history_stats": {
                    "metrics_count": len(self.data_collector.metrics_history),
                    "skill_metrics_count": len(self.data_collector.skill_usage_history),
                    "health_checks": len(self.data_collector.system_health_history),
                },
            }

            return summary

    def _generate_dashboard_html(self) -> str:
        """Generate basic HTML dashboard if templates not available"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>MCP Server Monitoring Dashboard</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
                .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
                .metric { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }
                .metric:last-child { border-bottom: none; }
                .metric-label { font-weight: bold; }
                .metric-value { color: #666; }
                .status-healthy { color: #28a745; }
                .status-warning { color: #ffc107; }
                .status-error { color: #dc3545; }
                .chart-placeholder { height: 200px; background: #f8f9fa; border: 1px dashed #dee2e6; display: flex; align-items: center; justify-content: center; color: #6c757d; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>MCP Server Monitoring Dashboard</h1>
                
                <div class="grid">
                    <div class="card">
                        <h3>System Health</h3>
                        <div id="health-status" class="metric">
                            <span class="metric-label">Status:</span>
                            <span class="metric-value status-healthy">Healthy</span>
                        </div>
                        <div id="health-issues" class="metric">
                            <span class="metric-label">Issues:</span>
                            <span class="metric-value">None</span>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h3>Current Metrics</h3>
                        <div id="current-metrics">
                            <div class="metric">
                                <span class="metric-label">CPU Usage:</span>
                                <span class="metric-value">--</span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Memory Usage:</span>
                                <span class="metric-value">--</span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Disk Usage:</span>
                                <span class="metric-value">--</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h3>Performance Trends</h3>
                    <div class="chart-placeholder">
                        Performance trend chart would be displayed here
                    </div>
                </div>
                
                <div class="card">
                    <h3>Skill Usage Analytics</h3>
                    <div class="chart-placeholder">
                        Skill usage analytics would be displayed here
                    </div>
                </div>
            </div>
            
            <script>
                // Basic JavaScript for real-time updates
                async function updateDashboard() {
                    try {
                        const [metrics, health, trends] = await Promise.all([
                            fetch('/api/system/metrics').then(r => r.json()),
                            fetch('/api/system/health').then(r => r.json()),
                            fetch('/api/system/trends').then(r => r.json())
                        ]);
                        
                        // Update health status
                        const healthElement = document.getElementById('health-status').querySelector('.metric-value');
                        healthElement.textContent = health.status;
                        healthElement.className = 'metric-value status-' + health.status;
                        
                        // Update issues
                        const issuesElement = document.getElementById('health-issues').querySelector('.metric-value');
                        issuesElement.textContent = health.issues.length > 0 ? health.issues.join(', ') : 'None';
                        
                        // Update current metrics
                        const metricsContainer = document.getElementById('current-metrics');
                        metricsContainer.innerHTML = `
                            <div class="metric">
                                <span class="metric-label">CPU Usage:</span>
                                <span class="metric-value">${metrics.cpu_usage || '--'}%</span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Memory Usage:</span>
                                <span class="metric-value">${metrics.memory_usage || '--'}%</span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Disk Usage:</span>
                                <span class="metric-value">${metrics.disk_usage || '--'}%</span>
                            </div>
                        `;
                    } catch (error) {
                        console.error('Failed to update dashboard:', error);
                    }
                }
                
                // Update every 30 seconds
                setInterval(updateDashboard, 30000);
                updateDashboard();
            </script>
        </body>
        </html>
        """

    async def _data_collection_loop(self):
        """Background data collection loop"""
        while True:
            try:
                # Collect system metrics
                self.data_collector.collect_system_metrics()

                # Collect skill metrics
                self.data_collector.collect_skill_metrics()

                # Get health status
                self.data_collector.get_health_status()

                await asyncio.sleep(
                    self.config.config["monitoring"]["metrics_interval"]
                )
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Data collection loop error: {e}")
                await asyncio.sleep(10)

    def run(self):
        """Run the dashboard server"""
        config = self.config.config["dashboard"]
        uvicorn.run(
            self.app, host=config["host"], port=config["port"], log_level="info"
        )


# CLI Interface
def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="MCP Server Monitoring Dashboard")
    parser.add_argument(
        "--config", default="mcp_config.yaml", help="Configuration file path"
    )
    parser.add_argument("--host", default=None, help="Dashboard host")
    parser.add_argument("--port", type=int, default=None, help="Dashboard port")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    # Update config if CLI args provided
    if args.config:
        os.environ["MCP_CONFIG"] = args.config
    if args.host:
        os.environ["DASHBOARD_HOST"] = args.host
    if args.port:
        os.environ["DASHBOARD_PORT"] = str(args.port)
    if args.debug:
        os.environ["DASHBOARD_DEBUG"] = "true"

    # Start dashboard
    dashboard = MonitoringDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
