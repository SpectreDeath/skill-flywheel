#!/usr/bin/env python3
"""
Skill: dynamic-model-router
Domain: model_orchestration
Description: An intelligent traffic controller that monitors QoS metrics and performs "hot-swaps" between model endpoints during active missions.
"""

import asyncio
import contextlib
import logging
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class ModelStatus(Enum):
    """Model endpoint status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class ModelEndpoint:
    """Represents a model endpoint configuration"""
    name: str
    url: str
    api_key: str | None = None
    headers: Dict[str, str] | None = None
    weight: float = 1.0
    status: ModelStatus = ModelStatus.HEALTHY
    last_health_check: datetime | None = None
    latency_history: List[float] = None
    error_count: int = 0
    total_requests: int = 0

@dataclass
class QoSMetrics:
    """Quality of Service metrics for a model"""
    latency_ms: float
    error_rate: float
    success_rate: float
    cost_per_token: float

@dataclass
class RoutingDecision:
    """Result of routing decision"""
    selected_model: str
    reason: str
    metrics: QoSMetrics | None = None

class DynamicModelRouter:
    """Intelligent traffic controller for model endpoints"""
    
    def __init__(self, 
                 latency_threshold_ms: int = 2000,
                 success_rate_threshold: float = 0.95,
                 health_check_interval: int = 30,
                 swap_cooldown: int = 60):
        """
        Initialize the dynamic model router
        
        Args:
            latency_threshold_ms: Maximum acceptable latency in milliseconds
            success_rate_threshold: Minimum acceptable success rate (0.0 to 1.0)
            health_check_interval: Health check interval in seconds
            swap_cooldown: Minimum time between swaps in seconds
        """
        self.latency_threshold_ms = latency_threshold_ms
        self.success_rate_threshold = success_rate_threshold
        self.health_check_interval = health_check_interval
        self.swap_cooldown = swap_cooldown
        
        self.endpoints: Dict[str, ModelEndpoint] = {}
        self.last_swap_time: datetime | None = None
        self.total_swaps = 0
        self.downtime_prevented = 0
        
        # Health check task
        self._health_check_task: asyncio.Task | None = None
        
    def add_endpoint(self, endpoint: ModelEndpoint):
        """Add a model endpoint to the router"""
        self.endpoints[endpoint.name] = endpoint
        logger.info(f"Added endpoint: {endpoint.name} at {endpoint.url}")
    
    def remove_endpoint(self, name: str):
        """Remove a model endpoint from the router"""
        if name in self.endpoints:
            del self.endpoints[name]
            logger.info(f"Removed endpoint: {name}")
    
    async def route_request(self, request_payload: Dict[str, Any]) -> RoutingDecision:
        """
        Route a request to the optimal model endpoint
        
        Args:
            request_payload: The request payload to route
            
        Returns:
            RoutingDecision with selected model and reasoning
        """
        # Check if we're in cooldown period
        if self._is_in_swap_cooldown():
            logger.debug("Currently in swap cooldown period")
        
        # Get healthy endpoints
        healthy_endpoints = self._get_healthy_endpoints()
        
        if not healthy_endpoints:
            logger.warning("No healthy endpoints available")
            return RoutingDecision(
                selected_model="",
                reason="No healthy endpoints available",
                metrics=None
            )
        
        # Evaluate QoS metrics for each endpoint
        endpoint_metrics = {}
        for endpoint in healthy_endpoints:
            metrics = await self._calculate_qos_metrics(endpoint)
            endpoint_metrics[endpoint.name] = metrics
        
        # Select best endpoint based on metrics
        best_endpoint = self._select_best_endpoint(healthy_endpoints, endpoint_metrics)
        
        decision = RoutingDecision(
            selected_model=best_endpoint.name,
            reason=f"Selected {best_endpoint.name} based on QoS metrics",
            metrics=endpoint_metrics[best_endpoint.name]
        )
        
        logger.info(f"Routed request to {decision.selected_model}: {decision.reason}")
        return decision
    
    def _get_healthy_endpoints(self) -> List[ModelEndpoint]:
        """Get list of healthy endpoints"""
        return [
            endpoint for endpoint in self.endpoints.values()
            if endpoint.status == ModelStatus.HEALTHY
        ]
    
    def _is_in_swap_cooldown(self) -> bool:
        """Check if we're in the swap cooldown period"""
        if not self.last_swap_time:
            return False
        
        time_since_last_swap = datetime.now() - self.last_swap_time
        return time_since_last_swap < timedelta(seconds=self.swap_cooldown)
    
    async def _calculate_qos_metrics(self, endpoint: ModelEndpoint) -> QoSMetrics:
        """Calculate QoS metrics for an endpoint"""
        # Calculate latency (average of recent history)
        if endpoint.latency_history:
            avg_latency = sum(endpoint.latency_history) / len(endpoint.latency_history)
        else:
            avg_latency = 0.0
        
        # Calculate success rate
        if endpoint.total_requests > 0:
            success_rate = 1.0 - (endpoint.error_count / endpoint.total_requests)
        else:
            success_rate = 1.0
        
        error_rate = 1.0 - success_rate
        
        # Default cost (could be configured per endpoint)
        cost_per_token = 0.0001  # Default placeholder
        
        return QoSMetrics(
            latency_ms=avg_latency,
            error_rate=error_rate,
            success_rate=success_rate,
            cost_per_token=cost_per_token
        )
    
    def _select_best_endpoint(self, endpoints: List[ModelEndpoint], 
                            metrics: Dict[str, QoSMetrics]) -> ModelEndpoint:
        """Select the best endpoint based on QoS metrics"""
        best_endpoint = None
        best_score = -1
        
        for endpoint in endpoints:
            metric = metrics[endpoint.name]
            
            # Calculate a score based on latency and success rate
            # Lower latency and higher success rate get higher scores
            latency_score = max(0, 100 - (metric.latency_ms / self.latency_threshold_ms * 100))
            success_score = metric.success_rate * 100
            
            # Combined score (could be weighted differently)
            total_score = (latency_score * 0.6) + (success_score * 0.4)
            
            if total_score > best_score:
                best_score = total_score
                best_endpoint = endpoint
        
        return best_endpoint or endpoints[0]  # Fallback to first endpoint
    
    async def perform_health_check(self, endpoint: ModelEndpoint) -> bool:
        """
        Perform health check on an endpoint
        
        Args:
            endpoint: The endpoint to check
            
        Returns:
            True if healthy, False otherwise
        """
        try:
            # Simulate health check (in real implementation, this would make an actual HTTP request)
            start_time = time.time()
            
            # Simulate network delay and processing
            await asyncio.sleep(0.1)
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Update endpoint metrics
            endpoint.latency_history = endpoint.latency_history or []
            endpoint.latency_history.append(response_time)
            
            # Keep only last 10 measurements
            if len(endpoint.latency_history) > 10:
                endpoint.latency_history.pop(0)
            
            endpoint.last_health_check = datetime.now()
            endpoint.total_requests += 1
            
            # Determine health status based on latency
            if response_time > self.latency_threshold_ms:
                endpoint.status = ModelStatus.DEGRADED
                endpoint.error_count += 1
                logger.warning(f"Endpoint {endpoint.name} degraded: latency {response_time:.2f}ms > {self.latency_threshold_ms}ms")
                return False
            else:
                endpoint.status = ModelStatus.HEALTHY
                return True
                
        except Exception as e:
            logger.error(f"Health check failed for {endpoint.name}: {e}")
            endpoint.status = ModelStatus.UNHEALTHY
            endpoint.error_count += 1
            return False
    
    async def start_health_monitoring(self):
        """Start background health monitoring"""
        if self._health_check_task:
            return
        
        self._health_check_task = asyncio.create_task(self._health_check_loop())
        logger.info("Started health monitoring")
    
    async def stop_health_monitoring(self):
        """Stop background health monitoring"""
        if self._health_check_task:
            self._health_check_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._health_check_task
            self._health_check_task = None
        logger.info("Stopped health monitoring")
    
    async def _health_check_loop(self):
        """Background loop for health checking"""
        while True:
            try:
                for endpoint in self.endpoints.values():
                    await self.perform_health_check(endpoint)
                
                await asyncio.sleep(self.health_check_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in health check loop: {e}")
                await asyncio.sleep(5)  # Wait before retrying
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing statistics"""
        return {
            "total_swaps": self.total_swaps,
            "downtime_prevented_seconds": self.downtime_prevented,
            "active_endpoints": len([e for e in self.endpoints.values() if e.status == ModelStatus.HEALTHY]),
            "total_endpoints": len(self.endpoints),
            "last_swap_time": self.last_swap_time.isoformat() if self.last_swap_time else None
        }
    
    def get_endpoint_status(self) -> List[Dict[str, Any]]:
        """Get status of all endpoints"""
        statuses = []
        for _name, endpoint in self.endpoints.items():
            asyncio.run(self._calculate_qos_metrics(endpoint)) if endpoint.latency_history else None
            statuses.append({
                "name": endpoint.name,
                "status": endpoint.status.value,
                "url": endpoint.url,
                "last_health_check": endpoint.last_health_check.isoformat() if endpoint.last_health_check else None,
                "total_requests": endpoint.total_requests,
                "error_count": endpoint.error_count,
                "avg_latency_ms": sum(endpoint.latency_history) / len(endpoint.latency_history) if endpoint.latency_history else 0,
                "success_rate": 1.0 - (endpoint.error_count / endpoint.total_requests) if endpoint.total_requests > 0 else 1.0
            })
        return statuses

# Global router instance
_router = DynamicModelRouter()

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "route", "add_endpoint", "remove_endpoint", "get_stats", "get_status"
            - request_payload: for routing requests
            - endpoint_config: for adding endpoints
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "route")
    
    try:
        if action == "route":
            request_payload = payload.get("request_payload", {})
            decision = await _router.route_request(request_payload)
            
            return {
                "result": {
                    "selected_model": decision.selected_model,
                    "reason": decision.reason,
                    "metrics": asdict(decision.metrics) if decision.metrics else None
                },
                "metadata": {
                    "action": "route",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "add_endpoint":
            endpoint_config = payload.get("endpoint_config", {})
            endpoint = ModelEndpoint(
                name=endpoint_config.get("name"),
                url=endpoint_config.get("url"),
                api_key=endpoint_config.get("api_key"),
                headers=endpoint_config.get("headers"),
                weight=endpoint_config.get("weight", 1.0)
            )
            _router.add_endpoint(endpoint)
            
            return {
                "result": {
                    "message": f"Added endpoint: {endpoint.name}",
                    "endpoint": {
                        "name": endpoint.name,
                        "url": endpoint.url,
                        "status": "added"
                    }
                },
                "metadata": {
                    "action": "add_endpoint",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "remove_endpoint":
            name = payload.get("name")
            if name in _router.endpoints:
                _router.remove_endpoint(name)
                return {
                    "result": {
                        "message": f"Removed endpoint: {name}",
                        "name": name
                    },
                    "metadata": {
                        "action": "remove_endpoint",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            else:
                return {
                    "result": {
                        "error": f"Endpoint {name} not found"
                    },
                    "metadata": {
                        "action": "remove_endpoint",
                        "timestamp": datetime.now().isoformat()
                    }
                }
        
        elif action == "get_stats":
            stats = _router.get_routing_stats()
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_status":
            status = _router.get_endpoint_status()
            return {
                "result": status,
                "metadata": {
                    "action": "get_status",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "start_monitoring":
            await _router.start_health_monitoring()
            return {
                "result": {
                    "message": "Started health monitoring"
                },
                "metadata": {
                    "action": "start_monitoring",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "stop_monitoring":
            await _router.stop_health_monitoring()
            return {
                "result": {
                    "message": "Stopped health monitoring"
                },
                "metadata": {
                    "action": "stop_monitoring",
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
        logger.error(f"Error in dynamic_model_router: {e}")
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
    """Example of how to use the dynamic model router skill"""
    
    # Add some example endpoints
    await invoke({
        "action": "add_endpoint",
        "endpoint_config": {
            "name": "openai-gpt4",
            "url": "https://api.openai.com/v1/chat/completions",
            "api_key": "sk-...",
            "weight": 1.0
        }
    })
    
    await invoke({
        "action": "add_endpoint", 
        "endpoint_config": {
            "name": "anthropic-claude",
            "url": "https://api.anthropic.com/v1/messages",
            "api_key": "sk-ant-...",
            "weight": 1.0
        }
    })
    
    # Start monitoring
    await invoke({"action": "start_monitoring"})
    
    # Route a request
    result = await invoke({
        "action": "route",
        "request_payload": {
            "messages": [{"role": "user", "content": "Hello, how are you?"}],
            "model": "gpt-4"
        }
    })
    
    print(f"Routing result: {result}")
    
    # Get stats
    stats = await invoke({"action": "get_stats"})
    print(f"Stats: {stats}")

if __name__ == "__main__":
    asyncio.run(example_usage())
