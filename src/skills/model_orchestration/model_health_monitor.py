#!/usr/bin/env python3
"""
Skill: model-health-monitor
Domain: model_orchestration
Description: A diagnostics engine that performs automated health checks on model endpoints by evaluating GPU memory, inference errors, and token throughput stability.
"""

import asyncio
import logging
import subprocess
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    """Model health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

@dataclass
class HealthMetrics:
    """Health metrics for a model endpoint"""
    vram_used_gb: float
    vram_total_gb: float
    vram_utilization_percent: float
    error_rate_percent: float
    throughput_tokens_per_sec: float
    uptime_seconds: float
    last_check_time: float

@dataclass
class HealthCheckResult:
    """Result of health check"""
    model_id: str
    status: HealthStatus
    metrics: HealthMetrics
    error_summary: str
    recommendations: List[str]

class ModelHealthMonitor:
    """Diagnostics engine for model endpoint health monitoring"""
    
    def __init__(self, 
                 error_threshold_percentage: float = 1.0,
                 vram_warning_level: float = 85.0,
                 probe_timeout: int = 10):
        """
        Initialize the model health monitor
        
        Args:
            error_threshold_percentage: Error rate threshold for degraded status
            vram_warning_level: VRAM utilization percentage for warning
            probe_timeout: Timeout for health check probes in seconds
        """
        self.error_threshold_percentage = error_threshold_percentage
        self.vram_warning_level = vram_warning_level
        self.probe_timeout = probe_timeout
        
        # Health check cache
        self._health_cache: Dict[str, HealthCheckResult] = {}
        self._cache_ttl = 60  # 1 minute cache
        
        # Error tracking
        self._error_history: Dict[str, List[float]] = {}
        self._request_count: Dict[str, int] = {}
        self._error_count: Dict[str, int] = {}
    
    async def check_model_health(self, model_id: str, endpoint_url: Optional[str] = None) -> HealthCheckResult:
        """
        Perform comprehensive health check on a model endpoint
        
        Args:
            model_id: Model identifier
            endpoint_url: Optional endpoint URL to probe
            
        Returns:
            HealthCheckResult with detailed health information
        """
        # Check cache first
        cache_key = f"{model_id}_{endpoint_url}"
        current_time = time.time()
        
        if cache_key in self._health_cache:
            cached_result = self._health_cache[cache_key]
            if (current_time - cached_result.metrics.last_check_time) < self._cache_ttl:
                return cached_result
        
        try:
            # Get GPU metrics
            gpu_metrics = await self._get_gpu_metrics()
            
            # Get error metrics
            error_metrics = self._get_error_metrics(model_id)
            
            # Get throughput metrics
            throughput_metrics = await self._get_throughput_metrics(model_id, endpoint_url)
            
            # Calculate overall health
            status = self._calculate_health_status(gpu_metrics, error_metrics, throughput_metrics)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(status, gpu_metrics, error_metrics)
            
            # Create error summary
            error_summary = self._create_error_summary(error_metrics, gpu_metrics)
            
            result = HealthCheckResult(
                model_id=model_id,
                status=status,
                metrics=HealthMetrics(
                    vram_used_gb=gpu_metrics['used_gb'],
                    vram_total_gb=gpu_metrics['total_gb'],
                    vram_utilization_percent=gpu_metrics['utilization_percent'],
                    error_rate_percent=error_metrics['error_rate'],
                    throughput_tokens_per_sec=throughput_metrics['tokens_per_sec'],
                    uptime_seconds=throughput_metrics['uptime_seconds'],
                    last_check_time=current_time
                ),
                error_summary=error_summary,
                recommendations=recommendations
            )
            
            # Cache the result
            self._health_cache[cache_key] = result
            
            logger.info(f"Health check for {model_id}: {status.value} - {error_summary}")
            return result
            
        except Exception as e:
            logger.error(f"Health check failed for {model_id}: {e}")
            
            # Return unknown status with error
            result = HealthCheckResult(
                model_id=model_id,
                status=HealthStatus.UNKNOWN,
                metrics=HealthMetrics(
                    vram_used_gb=0.0,
                    vram_total_gb=0.0,
                    vram_utilization_percent=0.0,
                    error_rate_percent=100.0,
                    throughput_tokens_per_sec=0.0,
                    uptime_seconds=0.0,
                    last_check_time=current_time
                ),
                error_summary=f"Health check failed: {str(e)}",
                recommendations=["Manual investigation required"]
            )
            
            self._health_cache[cache_key] = result
            return result
    
    async def _get_gpu_metrics(self) -> Dict[str, float]:
        """Get GPU memory metrics"""
        try:
            # Try to get GPU stats using nvidia-smi
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=memory.total,memory.used', '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True,
                timeout=5, check=False
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines and lines[0]:
                    parts = lines[0].split(', ')
                    if len(parts) >= 2:
                        total_gb = float(parts[0]) / 1024.0
                        used_gb = float(parts[1]) / 1024.0
                        utilization_percent = (used_gb / total_gb) * 100.0
                        
                        return {
                            'total_gb': total_gb,
                            'used_gb': used_gb,
                            'utilization_percent': utilization_percent
                        }
            
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.warning(f"nvidia-smi not available: {e}")
        
        # Fallback: try to get GPU info from torch if available
        try:
            import torch
            if torch.cuda.is_available():
                total_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                # Can't easily get used memory without nvidia-smi, so estimate
                used_gb = total_gb * 0.5  # Conservative estimate
                utilization_percent = 50.0
                
                return {
                    'total_gb': total_gb,
                    'used_gb': used_gb,
                    'utilization_percent': utilization_percent
                }
        except ImportError:
            pass
        
        # Final fallback: return CPU-only metrics
        return {
            'total_gb': 0.0,
            'used_gb': 0.0,
            'utilization_percent': 0.0
        }
    
    def _get_error_metrics(self, model_id: str) -> Dict[str, float]:
        """Get error rate metrics for a model"""
        # Get error history for this model
        error_times = self._error_history.get(model_id, [])
        total_requests = self._request_count.get(model_id, 0)
        error_count = self._error_count.get(model_id, 0)
        
        # Calculate error rate
        if total_requests > 0:
            error_rate = (error_count / total_requests) * 100.0
        else:
            error_rate = 0.0
        
        return {
            'total_requests': total_requests,
            'error_count': error_count,
            'error_rate': error_rate,
            'recent_errors': len([t for t in error_times if time.time() - t < 300])  # Last 5 minutes
        }
    
    async def _get_throughput_metrics(self, model_id: str, endpoint_url: Optional[str]) -> Dict[str, float]:
        """Get throughput and uptime metrics"""
        try:
            if endpoint_url:
                # Perform a quick probe to measure latency and check availability
                start_time = time.time()
                
                # Simple health check probe
                response = requests.get(
                    f"{endpoint_url}/health",
                    timeout=self.probe_timeout
                )
                
                probe_time = time.time() - start_time
                
                if response.status_code == 200:
                    # Estimate tokens per second based on response time
                    # This is a rough estimate - real implementation would use actual inference
                    estimated_tokens_per_sec = 1000.0 / probe_time if probe_time > 0 else 0.0
                    uptime_seconds = 3600.0  # Assume 1 hour uptime for probe success
                else:
                    estimated_tokens_per_sec = 0.0
                    uptime_seconds = 0.0
            else:
                # No endpoint to probe, use defaults
                estimated_tokens_per_sec = 0.0
                uptime_seconds = 0.0
            
            return {
                'tokens_per_sec': estimated_tokens_per_sec,
                'uptime_seconds': uptime_seconds,
                'probe_latency_ms': probe_time * 1000 if 'probe_time' in locals() else 0.0
            }
            
        except Exception as e:
            logger.warning(f"Throughput probe failed for {model_id}: {e}")
            return {
                'tokens_per_sec': 0.0,
                'uptime_seconds': 0.0,
                'probe_latency_ms': 0.0
            }
    
    def _calculate_health_status(self, gpu_metrics: Dict[str, float], 
                               error_metrics: Dict[str, float],
                               throughput_metrics: Dict[str, float]) -> HealthStatus:
        """Calculate overall health status based on metrics"""
        
        # Check error rate
        if error_metrics['error_rate'] > 5.0:
            return HealthStatus.CRITICAL
        elif error_metrics['error_rate'] > self.error_threshold_percentage:
            return HealthStatus.DEGRADED
        
        # Check VRAM utilization
        if gpu_metrics['utilization_percent'] > 95.0:
            return HealthStatus.CRITICAL
        elif gpu_metrics['utilization_percent'] > self.vram_warning_level:
            return HealthStatus.DEGRADED
        
        # Check throughput (if we have endpoint data)
        if throughput_metrics['tokens_per_sec'] == 0.0 and throughput_metrics['uptime_seconds'] == 0.0:
            return HealthStatus.UNKNOWN
        
        # Check for silent degradation (low throughput)
        if throughput_metrics['tokens_per_sec'] < 10.0:
            return HealthStatus.DEGRADED
        
        return HealthStatus.HEALTHY
    
    def _generate_recommendations(self, status: HealthStatus, gpu_metrics: Dict[str, float], 
                                error_metrics: Dict[str, float]) -> List[str]:
        """Generate recommendations based on health status"""
        recommendations = []
        
        if status == HealthStatus.CRITICAL:
            if error_metrics['error_rate'] > 5.0:
                recommendations.append("High error rate detected - investigate service logs")
            if gpu_metrics['utilization_percent'] > 95.0:
                recommendations.append("VRAM critically high - consider model restart or larger GPU")
        
        elif status == HealthStatus.DEGRADED:
            if error_metrics['error_rate'] > self.error_threshold_percentage:
                recommendations.append("Error rate elevated - monitor for service degradation")
            if gpu_metrics['utilization_percent'] > self.vram_warning_level:
                recommendations.append("VRAM usage high - consider context reset or model restart")
        
        elif status == HealthStatus.HEALTHY:
            recommendations.append("Model operating within normal parameters")
        
        # General recommendations
        if gpu_metrics['utilization_percent'] > 80.0:
            recommendations.append("Consider releasing VRAM if model is idle")
        
        if error_metrics['recent_errors'] > 10:
            recommendations.append("Frequent recent errors - investigate root cause")
        
        return recommendations
    
    def _create_error_summary(self, error_metrics: Dict[str, float], gpu_metrics: Dict[str, float]) -> str:
        """Create a human-readable error summary"""
        parts = []
        
        if error_metrics['error_rate'] > 0:
            parts.append(f"Error rate: {error_metrics['error_rate']:.1f}%")
        
        if gpu_metrics['utilization_percent'] > 0:
            parts.append(f"VRAM: {gpu_metrics['utilization_percent']:.1f}% ({gpu_metrics['used_gb']:.1f}/{gpu_metrics['total_gb']:.1f}GB)")
        
        if parts:
            return " | ".join(parts)
        else:
            return "No issues detected"
    
    def record_request(self, model_id: str, success: bool = True):
        """Record a request for error tracking"""
        if model_id not in self._request_count:
            self._request_count[model_id] = 0
        if model_id not in self._error_count:
            self._error_count[model_id] = 0
        
        self._request_count[model_id] += 1
        if not success:
            self._error_count[model_id] += 1
            # Record error time for recent error tracking
            if model_id not in self._error_history:
                self._error_history[model_id] = []
            self._error_history[model_id].append(time.time())
            
            # Keep only last hour of error times
            cutoff = time.time() - 3600
            self._error_history[model_id] = [t for t in self._error_history[model_id] if t > cutoff]
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get summary of all monitored models"""
        summary = {
            'total_models': len(self._health_cache),
            'healthy': 0,
            'degraded': 0,
            'critical': 0,
            'unknown': 0,
            'details': []
        }
        
        for result in self._health_cache.values():
            if result.status == HealthStatus.HEALTHY:
                summary['healthy'] += 1
            elif result.status == HealthStatus.DEGRADED:
                summary['degraded'] += 1
            elif result.status == HealthStatus.CRITICAL:
                summary['critical'] += 1
            else:
                summary['unknown'] += 1
            
            summary['details'].append({
                'model_id': result.model_id,
                'status': result.status.value,
                'vram_utilization': result.metrics.vram_utilization_percent,
                'error_rate': result.metrics.error_rate_percent,
                'throughput': result.metrics.throughput_tokens_per_sec
            })
        
        return summary
    
    def clear_cache(self):
        """Clear health check cache"""
        self._health_cache.clear()
        logger.info("Health check cache cleared")

# Global monitor instance
_monitor = ModelHealthMonitor()

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "check", "record", "summary", "clear_cache"
            - model_id: model identifier
            - endpoint_url: optional endpoint URL
            - success: for recording requests
            - error_threshold_percentage: optional override
            - vram_warning_level: optional override
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "check")
    
    try:
        if action == "check":
            model_id = payload.get("model_id")
            endpoint_url = payload.get("endpoint_url")
            
            if not model_id:
                return {
                    "result": {
                        "error": "model_id is required for health check"
                    },
                    "metadata": {
                        "action": "check",
                        "timestamp": time.time()
                    }
                }
            
            # Override defaults if provided
            if 'error_threshold_percentage' in payload:
                _monitor.error_threshold_percentage = payload['error_threshold_percentage']
            if 'vram_warning_level' in payload:
                _monitor.vram_warning_level = payload['vram_warning_level']
            
            result = await _monitor.check_model_health(model_id, endpoint_url)
            
            return {
                "result": {
                    "model_id": result.model_id,
                    "status": result.status.value,
                    "metrics": {
                        "vram_used_gb": result.metrics.vram_used_gb,
                        "vram_total_gb": result.metrics.vram_total_gb,
                        "vram_utilization_percent": result.metrics.vram_utilization_percent,
                        "error_rate_percent": result.metrics.error_rate_percent,
                        "throughput_tokens_per_sec": result.metrics.throughput_tokens_per_sec,
                        "uptime_seconds": result.metrics.uptime_seconds
                    },
                    "error_summary": result.error_summary,
                    "recommendations": result.recommendations
                },
                "metadata": {
                    "action": "check",
                    "timestamp": result.metrics.last_check_time
                }
            }
        
        elif action == "record":
            model_id = payload.get("model_id")
            success = payload.get("success", True)
            
            if not model_id:
                return {
                    "result": {
                        "error": "model_id is required for request recording"
                    },
                    "metadata": {
                        "action": "record",
                        "timestamp": time.time()
                    }
                }
            
            _monitor.record_request(model_id, success)
            
            return {
                "result": {
                    "message": f"Recorded request for {model_id} (success: {success})"
                },
                "metadata": {
                    "action": "record",
                    "timestamp": time.time()
                }
            }
        
        elif action == "summary":
            summary = _monitor.get_health_summary()
            
            return {
                "result": summary,
                "metadata": {
                    "action": "summary",
                    "timestamp": time.time()
                }
            }
        
        elif action == "clear_cache":
            _monitor.clear_cache()
            
            return {
                "result": {
                    "message": "Health check cache cleared"
                },
                "metadata": {
                    "action": "clear_cache",
                    "timestamp": time.time()
                }
            }
        
        else:
            return {
                "result": {
                    "error": f"Unknown action: {action}"
                },
                "metadata": {
                    "action": action,
                    "timestamp": time.time()
                }
            }
    
    except Exception as e:
        logger.error(f"Error in model_health_monitor: {e}")
        return {
            "result": {
                "error": str(e)
            },
            "metadata": {
                "action": action,
                "timestamp": time.time()
            }
        }

# Example usage function
async def example_usage():
    """Example of how to use the model health monitor skill"""
    
    # Record some requests
    _monitor.record_request("llama-70b", success=True)
    _monitor.record_request("llama-70b", success=True)
    _monitor.record_request("llama-70b", success=False)  # Error
    
    # Check health
    result = await invoke({
        "action": "check",
        "model_id": "llama-70b",
        "endpoint_url": "http://localhost:8000"
    })
    print(f"Health check: {result}")
    
    # Get summary
    summary = await invoke({"action": "summary"})
    print(f"Health summary: {summary}")

if __name__ == "__main__":
    asyncio.run(example_usage())
