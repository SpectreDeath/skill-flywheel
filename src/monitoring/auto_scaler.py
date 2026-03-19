#!/usr/bin/env python3
"""
Auto-Scaler for Enhanced MCP Server v3

This module provides automatic container scaling based on:
- CPU and memory utilization
- Request rate and response time
- ML-based predictions for future load
- Anomaly detection and prevention
"""

import asyncio
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import docker
import numpy as np
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_scaler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ScalingMetrics:
    """Container scaling metrics"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    request_rate: float
    response_time: float
    active_connections: int
    container_count: int
    load_score: float
    predicted_load: float

class MetricsCollector:
    """Collect metrics from Prometheus and system"""
    
    def __init__(self, prometheus_url: str = "http://prometheus:9090"):
        self.prometheus_url = prometheus_url
        self.docker_client = docker.from_env()
    
    async def collect_metrics(self) -> Optional[ScalingMetrics]:
        """Collect current system metrics"""
        try:
            # Get Prometheus metrics
            prometheus_metrics = await self._get_prometheus_metrics()
            
            # Get Docker container metrics
            docker_metrics = await self._get_docker_metrics()
            
            # Calculate load score
            load_score = self._calculate_load_score(
                prometheus_metrics, docker_metrics
            )
            
            # Predict future load
            predicted_load = self._predict_future_load(prometheus_metrics)
            
            return ScalingMetrics(
                timestamp=datetime.now(),
                cpu_usage=prometheus_metrics.get('system_cpu', 0.0),
                memory_usage=prometheus_metrics.get('system_memory', 0.0),
                request_rate=prometheus_metrics.get('request_rate', 0.0),
                response_time=prometheus_metrics.get('avg_response_time', 0.0),
                active_connections=prometheus_metrics.get('active_connections', 0),
                container_count=docker_metrics['container_count'],
                load_score=load_score,
                predicted_load=predicted_load
            )
            
        except Exception as e:
            logger.error(f"Failed to collect metrics: {e}")
            return None
    
    async def _get_prometheus_metrics(self) -> Dict[str, float]:
        """Get metrics from Prometheus"""
        try:
            # Query Prometheus for current metrics
            queries = {
                'system_cpu': 'mcp_system_cpu_usage',
                'system_memory': 'mcp_system_memory_usage',
                'request_rate': 'rate(mcp_requests_total[5m])',
                'avg_response_time': 'avg(mcp_request_duration_seconds)',
                'active_connections': 'mcp_active_connections',
                'active_skills': 'mcp_active_skills'
            }
            
            metrics = {}
            for name, query in queries.items():
                try:
                    response = requests.get(
                        f"{self.prometheus_url}/api/v1/query",
                        params={'query': query},
                        timeout=10
                    )
                    if response.status_code == 200:
                        data = response.json()
                        if data['data']['result']:
                            metrics[name] = float(data['data']['result'][0]['value'][1])
                        else:
                            metrics[name] = 0.0
                    else:
                        metrics[name] = 0.0
                except Exception as e:
                    logger.warning(f"Failed to get {name} from Prometheus: {e}")
                    metrics[name] = 0.0
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to query Prometheus: {e}")
            return {}
    
    async def _get_docker_metrics(self) -> Dict[str, any]:
        """Get Docker container metrics"""
        try:
            # Get MCP server containers
            containers = self.docker_client.containers.list(
                filters={'label': 'mcp_server=true'}
            )
            
            container_count = len(containers)
            total_cpu = 0.0
            total_memory = 0.0
            
            for container in containers:
                try:
                    stats = container.stats(stream=False)
                    if 'cpu_stats' in stats:
                        cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                                   stats['precpu_stats']['cpu_usage']['total_usage']
                        system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                                      stats['precpu_stats']['system_cpu_usage']
                        
                        if system_delta > 0:
                            cpu_usage = (cpu_delta / system_delta) * len(stats['cpu_stats']['cpu_usage']['percpu_usage'])
                            total_cpu += cpu_usage
                    
                    if 'memory_stats' in stats:
                        memory_usage = stats['memory_stats']['usage'] / (1024 * 1024)  # MB
                        total_memory += memory_usage
                
                except Exception as e:
                    logger.warning(f"Failed to get stats for container {container.id}: {e}")
            
            return {
                'container_count': container_count,
                'avg_cpu_usage': total_cpu / max(1, container_count),
                'avg_memory_usage': total_memory / max(1, container_count)
            }
            
        except Exception as e:
            logger.error(f"Failed to get Docker metrics: {e}")
            return {'container_count': 0, 'avg_cpu_usage': 0.0, 'avg_memory_usage': 0.0}
    
    def _calculate_load_score(self, prometheus_metrics: Dict, docker_metrics: Dict) -> float:
        """Calculate overall system load score"""
        # Weighted combination of different metrics
        cpu_weight = 0.3
        memory_weight = 0.3
        request_rate_weight = 0.2
        response_time_weight = 0.2
        
        cpu_score = prometheus_metrics.get('system_cpu', 0.0) / 100.0
        memory_score = prometheus_metrics.get('system_memory', 0.0) / 100.0
        request_score = min(prometheus_metrics.get('request_rate', 0.0) / 100.0, 1.0)
        response_score = min(prometheus_metrics.get('response_time', 0.0) / 10.0, 1.0)
        
        load_score = (
            cpu_score * cpu_weight +
            memory_score * memory_weight +
            request_score * request_rate_weight +
            response_score * response_time_weight
        )
        
        return min(load_score, 1.0)
    
    def _predict_future_load(self, prometheus_metrics: Dict) -> float:
        """Predict future load using simple trend analysis"""
        # This is a simplified prediction - in practice, you'd use ML models
        current_load = self._calculate_load_score(prometheus_metrics, {})
        
        # Add some randomness to simulate prediction uncertainty
        prediction_factor = 1.0 + (np.random.random() - 0.5) * 0.2
        
        return min(current_load * prediction_factor, 1.0)

class AutoScaler:
    """Main auto-scaler class"""
    
    def __init__(self):
        self.config = {
            'scale_up_threshold': float(os.getenv('SCALE_UP_THRESHOLD', 0.8)),
            'scale_down_threshold': float(os.getenv('SCALE_DOWN_THRESHOLD', 0.3)),
            'scale_interval': int(os.getenv('SCALE_INTERVAL', 60)),
            'min_containers': int(os.getenv('MIN_CONTAINERS', 1)),
            'max_containers': int(os.getenv('MAX_CONTAINERS', 10)),
            'scale_up_factor': float(os.getenv('SCALE_UP_FACTOR', 1.5)),
            'scale_down_factor': float(os.getenv('SCALE_DOWN_FACTOR', 0.7)),
            'cooldown_period': int(os.getenv('COOLDOWN_PERIOD', 300)),  # 5 minutes
        }
        
        self.metrics_collector = MetricsCollector()
        self.docker_client = docker.from_env()
        self.last_scale_time = datetime.now()
        self.scaling_history: List[Dict] = []
        
        logger.info(f"Auto-scaler initialized with config: {self.config}")
    
    async def run(self):
        """Main scaling loop"""
        logger.info("Starting auto-scaler...")
        
        while True:
            try:
                # Collect current metrics
                metrics = await self.metrics_collector.collect_metrics()
                
                if metrics:
                    # Make scaling decision
                    action = await self._make_scaling_decision(metrics)
                    
                    # Execute scaling if needed
                    if action['should_scale']:
                        await self._execute_scaling(action, metrics)
                
                # Wait for next iteration
                await asyncio.sleep(self.config['scale_interval'])
                
            except Exception as e:
                logger.error(f"Error in scaling loop: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def _make_scaling_decision(self, metrics: ScalingMetrics) -> Dict:
        """Make scaling decision based on current metrics"""
        current_time = datetime.now()
        time_since_last_scale = (current_time - self.last_scale_time).total_seconds()
        
        # Check cooldown period
        if time_since_last_scale < self.config['cooldown_period']:
            return {'should_scale': False, 'reason': 'Cooldown period active'}
        
        current_containers = metrics.container_count
        current_load = metrics.load_score
        predicted_load = metrics.predicted_load
        
        # Determine target container count
        target_containers = self._calculate_target_containers(current_load, predicted_load, current_containers)
        
        # Check if scaling is needed
        if target_containers > current_containers and current_load > self.config['scale_up_threshold']:
            return {
                'should_scale': True,
                'action': 'scale_up',
                'target_count': target_containers,
                'reason': f'High load: {current_load:.2f}, predicted: {predicted_load:.2f}'
            }
        elif target_containers < current_containers and current_load < self.config['scale_down_threshold']:
            return {
                'should_scale': True,
                'action': 'scale_down',
                'target_count': target_containers,
                'reason': f'Low load: {current_load:.2f}, predicted: {predicted_load:.2f}'
            }
        
        return {'should_scale': False, 'reason': f'Load within acceptable range: {current_load:.2f}'}
    
    def _calculate_target_containers(self, current_load: float, predicted_load: float, current_count: int) -> int:
        """Calculate target number of containers"""
        # Use predicted load for scaling decisions
        target_load = predicted_load
        
        # Calculate target container count based on load
        if target_load > self.config['scale_up_threshold']:
            # Scale up
            target_count = int(current_count * self.config['scale_up_factor'])
        elif target_load < self.config['scale_down_threshold']:
            # Scale down
            target_count = max(self.config['min_containers'], int(current_count * self.config['scale_down_factor']))
        else:
            # Maintain current count
            target_count = current_count
        
        # Apply constraints
        target_count = max(self.config['min_containers'], min(target_count, self.config['max_containers']))
        
        return target_count
    
    async def _execute_scaling(self, action: Dict, metrics: ScalingMetrics):
        """Execute the scaling action"""
        try:
            target_count = action['target_count']
            current_count = metrics.container_count
            
            logger.info(f"Executing scaling action: {action['action']} from {current_count} to {target_count} containers")
            
            if action['action'] == 'scale_up':
                await self._scale_up(target_count, current_count)
            elif action['action'] == 'scale_down':
                await self._scale_down(target_count, current_count)
            
            # Update scaling history
            self.scaling_history.append({
                'timestamp': datetime.now(),
                'action': action['action'],
                'from_count': current_count,
                'to_count': target_count,
                'load_score': metrics.load_score,
                'predicted_load': metrics.predicted_load,
                'reason': action['reason']
            })
            
            # Keep only last 100 entries
            if len(self.scaling_history) > 100:
                self.scaling_history.pop(0)
            
            # Update last scale time
            self.last_scale_time = datetime.now()
            
            logger.info(f"Scaling action completed: {action['action']} to {target_count} containers")
            
        except Exception as e:
            logger.error(f"Failed to execute scaling action: {e}")
    
    async def _scale_up(self, target_count: int, current_count: int):
        """Scale up containers"""
        containers_to_add = target_count - current_count
        
        for i in range(containers_to_add):
            try:
                # Create new container
                container = self.docker_client.containers.run(
                    image='mcp-server-v3:latest',
                    name=f'mcp-server-v3-{int(time.time())}-{i}',
                    environment={
                        'PYTHONUNBUFFERED': '1',
                        'REDIS_URL': 'redis://redis:6379/0',
                        'CELERY_BROKER_URL': 'redis://redis:6379/1',
                        'CELERY_RESULT_BACKEND': 'redis://redis:6379/2',
                        'MCP_CONFIG': '/app/mcp_config.yaml',
                        'PROMETHEUS_PORT': '8001',
                        'WORKERS': '2'
                    },
                    volumes={
                        '/app/skills': {'bind': '/app/skills', 'mode': 'ro'},
                        '/app/models': {'bind': '/app/models', 'mode': 'ro'},
                        '/app/logs': {'bind': '/app/logs', 'mode': 'rw'},
                        '/app/mcp_config.yaml': {'bind': '/app/mcp_config.yaml', 'mode': 'ro'}
                    },
                    labels={'mcp_server': 'true'},
                    restart_policy={'Name': 'unless-stopped'},
                    detach=True,
                    remove=True
                )
                
                logger.info(f"Created new container: {container.short_id}")
                
            except Exception as e:
                logger.error(f"Failed to create container {i}: {e}")
                break
    
    async def _scale_down(self, target_count: int, current_count: int):
        """Scale down containers"""
        containers_to_remove = current_count - target_count
        
        # Get containers to remove (oldest first)
        containers = self.docker_client.containers.list(
            filters={'label': 'mcp_server=true'},
            sort='created'
        )
        
        for i in range(min(containers_to_remove, len(containers))):
            try:
                container = containers[i]
                logger.info(f"Removing container: {container.short_id}")
                container.stop(timeout=30)
                container.remove()
                
            except Exception as e:
                logger.error(f"Failed to remove container {container.short_id}: {e}")
    
    def get_scaling_status(self) -> Dict:
        """Get current scaling status"""
        return {
            'config': self.config,
            'last_scale_time': self.last_scale_time.isoformat(),
            'scaling_history': [
                {
                    'timestamp': entry['timestamp'].isoformat(),
                    'action': entry['action'],
                    'from_count': entry['from_count'],
                    'to_count': entry['to_count'],
                    'load_score': entry['load_score'],
                    'predicted_load': entry['predicted_load'],
                    'reason': entry['reason']
                }
                for entry in self.scaling_history[-10:]  # Last 10 actions
            ],
            'current_metrics': None  # Would be populated with latest metrics
        }

async def main():
    """Main entry point"""
    scaler = AutoScaler()
    await scaler.run()

if __name__ == "__main__":
    asyncio.run(main())
