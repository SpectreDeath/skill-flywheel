import logging
from typing import Any, Dict, List

import numpy as np

logger = logging.getLogger(__name__)

class ResourceOptimizer:
    """Advanced resource optimization logic separated from server."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.resource_history: List[Dict[str, float]] = []
    
    def calculate_utilization_score(self, cpu: float, memory: float, disk: float) -> float:
        """Calculate overall resource utilization score."""
        score = (cpu * 0.4 + memory * 0.4 + disk * 0.2) / 100.0
        return min(score, 1.0)
    
    def optimize_allocation(self, current_allocation: Dict[str, float]) -> Dict[str, float]:
        """Optimize resource allocation based on historical usage."""
        if not self.resource_history:
            return current_allocation
        
        recent_usage = self.resource_history[-10:]
        avg_cpu = np.mean([r["cpu"] for r in recent_usage])
        avg_memory = np.mean([r["memory"] for r in recent_usage])
        
        predicted_cpu = avg_cpu * 1.2
        predicted_memory = avg_memory * 1.2
        
        optimized = current_allocation.copy()
        optimized["cpu"] = max(predicted_cpu, current_allocation.get("cpu", 50.0))
        optimized["memory"] = max(predicted_memory, current_allocation.get("memory", 50.0))
        
        return optimized
