#!/usr/bin/env python3
"""
Skill: auto-scaling-manager
Domain: cloud_engineering
Description: Auto scaling management system for cloud resources based on metrics and policies
"""

import asyncio
import logging
import statistics
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class ScalingAction(Enum):
    """Types of scaling actions"""
    SCALE_OUT = "scale_out"      # Increase capacity
    SCALE_IN = "scale_in"        # Decrease capacity
    NO_OP = "no_op"              # No action

class ScalingPolicyType(Enum):
    """Types of scaling policies"""
    THRESHOLD = "threshold"      # Based on metric thresholds
    SCHEDULE = "schedule"        # Based on time schedules
    PREDICTIVE = "predictive"    # Based on predictions

class ResourceState(Enum):
    """States of resources"""
    PENDING = "pending"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    TERMINATED = "terminated"

@dataclass
class ScalingPolicy:
    """Represents a scaling policy"""
    policy_id: str
    name: str
    description: str
    policy_type: ScalingPolicyType
    resource_type: str
    min_capacity: int
    max_capacity: int
    target_capacity: Optional[int]
    cooldown_period: int  # seconds
    enabled: bool
    created_at: float
    last_modified: float

@dataclass
class ThresholdPolicy:
    """Threshold-based scaling policy"""
    policy_id: str
    metric_name: str
    scale_out_threshold: float
    scale_in_threshold: float
    evaluation_periods: int
    scale_out_adjustment: int
    scale_in_adjustment: int

@dataclass
class SchedulePolicy:
    """Schedule-based scaling policy"""
    policy_id: str
    schedule: Dict[str, int]  # time -> capacity mapping
    timezone: str

@dataclass
class Resource:
    """Represents a scalable resource"""
    resource_id: str
    name: str
    resource_type: str
    state: ResourceState
    created_at: float
    last_modified: float
    tags: Dict[str, str]
    metrics: Dict[str, float]

@dataclass
class ScalingEvent:
    """Represents a scaling event"""
    event_id: str
    policy_id: str
    action: ScalingAction
    resource_type: str
    target_capacity: int
    current_capacity: int
    triggered_at: float
    completed_at: Optional[float]
    status: str  # pending, in_progress, completed, failed
    resources_affected: List[str]

class AutoScalingManager:
    """Auto scaling management system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the auto scaling manager
        
        Args:
            config: Configuration dictionary with:
                - evaluation_interval: How often to evaluate policies
                - max_concurrent_scaling: Maximum concurrent scaling operations
                - default_cooldown: Default cooldown period
        """
        self.evaluation_interval = config.get("evaluation_interval", 60)
        self.max_concurrent_scaling = config.get("max_concurrent_scaling", 3)
        self.default_cooldown = config.get("default_cooldown", 300)
        
        self.policies: Dict[str, ScalingPolicy] = {}
        self.threshold_policies: Dict[str, ThresholdPolicy] = {}
        self.schedule_policies: Dict[str, SchedulePolicy] = {}
        self.resources: Dict[str, Resource] = {}
        self.scaling_events: Dict[str, ScalingEvent] = {}
        
        self.active_scaling_operations = 0
        self.total_scaling_events = 0
        self.scaling_stats = {
            "scale_out_count": 0,
            "scale_in_count": 0,
            "failed_operations": 0,
            "average_response_time": 0.0
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Start background evaluation
        self._evaluation_task = asyncio.create_task(self._evaluation_loop())
    
    def create_scaling_policy(self, 
                             name: str,
                             description: str,
                             policy_type: ScalingPolicyType,
                             resource_type: str,
                             min_capacity: int,
                             max_capacity: int,
                             target_capacity: Optional[int] = None,
                             cooldown_period: Optional[int] = None) -> str:
        """
        Create a scaling policy
        
        Args:
            name: Policy name
            description: Policy description
            policy_type: Type of scaling policy
            resource_type: Type of resource to scale
            min_capacity: Minimum capacity
            max_capacity: Maximum capacity
            target_capacity: Target capacity (for predictive policies)
            cooldown_period: Cooldown period in seconds
            
        Returns:
            Policy ID
        """
        policy_id = str(uuid.uuid4())
        
        policy = ScalingPolicy(
            policy_id=policy_id,
            name=name,
            description=description,
            policy_type=policy_type,
            resource_type=resource_type,
            min_capacity=min_capacity,
            max_capacity=max_capacity,
            target_capacity=target_capacity,
            cooldown_period=cooldown_period or self.default_cooldown,
            enabled=True,
            created_at=time.time(),
            last_modified=time.time()
        )
        
        self.policies[policy_id] = policy
        self.logger.info(f"Created scaling policy: {policy_id}")
        
        return policy_id
    
    def create_threshold_policy(self,
                               policy_id: str,
                               metric_name: str,
                               scale_out_threshold: float,
                               scale_in_threshold: float,
                               evaluation_periods: int,
                               scale_out_adjustment: int,
                               scale_in_adjustment: int) -> str:
        """
        Create a threshold-based scaling policy
        
        Args:
            policy_id: Parent policy ID
            metric_name: Metric to monitor
            scale_out_threshold: Threshold for scaling out
            scale_in_threshold: Threshold for scaling in
            evaluation_periods: Number of periods to evaluate
            scale_out_adjustment: Number of instances to add
            scale_in_adjustment: Number of instances to remove
            
        Returns:
            Policy ID
        """
        threshold_policy = ThresholdPolicy(
            policy_id=policy_id,
            metric_name=metric_name,
            scale_out_threshold=scale_out_threshold,
            scale_in_threshold=scale_in_threshold,
            evaluation_periods=evaluation_periods,
            scale_out_adjustment=scale_out_adjustment,
            scale_in_adjustment=scale_in_adjustment
        )
        
        self.threshold_policies[policy_id] = threshold_policy
        self.logger.info(f"Created threshold policy: {policy_id}")
        
        return policy_id
    
    def create_schedule_policy(self,
                              policy_id: str,
                              schedule: Dict[str, int],
                              timezone: str = "UTC") -> str:
        """
        Create a schedule-based scaling policy
        
        Args:
            policy_id: Parent policy ID
            schedule: Schedule mapping (time -> capacity)
            timezone: Timezone for the schedule
            
        Returns:
            Policy ID
        """
        schedule_policy = SchedulePolicy(
            policy_id=policy_id,
            schedule=schedule,
            timezone=timezone
        )
        
        self.schedule_policies[policy_id] = schedule_policy
        self.logger.info(f"Created schedule policy: {policy_id}")
        
        return policy_id
    
    def register_resource(self,
                         name: str,
                         resource_type: str,
                         tags: Optional[Dict[str, str]] = None) -> str:
        """
        Register a resource for scaling
        
        Args:
            name: Resource name
            resource_type: Type of resource
            tags: Resource tags
            
        Returns:
            Resource ID
        """
        resource_id = str(uuid.uuid4())
        
        resource = Resource(
            resource_id=resource_id,
            name=name,
            resource_type=resource_type,
            state=ResourceState.PENDING,
            created_at=time.time(),
            last_modified=time.time(),
            tags=tags or {},
            metrics={}
        )
        
        self.resources[resource_id] = resource
        self.logger.info(f"Registered resource: {resource_id}")
        
        return resource_id
    
    def update_resource_metrics(self, resource_id: str, metrics: Dict[str, float]):
        """Update resource metrics"""
        if resource_id in self.resources:
            self.resources[resource_id].metrics.update(metrics)
    
    async def trigger_scaling(self, policy_id: str, action: ScalingAction) -> str:
        """
        Manually trigger scaling action
        
        Args:
            policy_id: Policy ID
            action: Scaling action
            
        Returns:
            Event ID
        """
        if policy_id not in self.policies:
            raise ValueError(f"Policy {policy_id} not found")
        
        policy = self.policies[policy_id]
        
        # Check if scaling is allowed
        if not policy.enabled:
            raise ValueError(f"Policy {policy_id} is disabled")
        
        if self.active_scaling_operations >= self.max_concurrent_scaling:
            raise ValueError("Maximum concurrent scaling operations reached")
        
        # Calculate target capacity
        current_capacity = self._get_current_capacity(policy.resource_type)
        target_capacity = self._calculate_target_capacity(policy, current_capacity, action)
        
        # Create scaling event
        event_id = str(uuid.uuid4())
        event = ScalingEvent(
            event_id=event_id,
            policy_id=policy_id,
            action=action,
            resource_type=policy.resource_type,
            target_capacity=target_capacity,
            current_capacity=current_capacity,
            triggered_at=time.time(),
            completed_at=None,
            status="in_progress",
            resources_affected=[]
        )
        
        self.scaling_events[event_id] = event
        self.active_scaling_operations += 1
        self.total_scaling_events += 1
        
        # Execute scaling asynchronously
        asyncio.create_task(self._execute_scaling(event))
        
        self.logger.info(f"Triggered scaling: {event_id} ({action.value})")
        return event_id
    
    def get_scaling_status(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get scaling event status"""
        if event_id not in self.scaling_events:
            return None
        
        event = self.scaling_events[event_id]
        
        return {
            "event_id": event.event_id,
            "policy_id": event.policy_id,
            "action": event.action.value,
            "resource_type": event.resource_type,
            "target_capacity": event.target_capacity,
            "current_capacity": event.current_capacity,
            "status": event.status,
            "triggered_at": datetime.fromtimestamp(event.triggered_at).isoformat(),
            "completed_at": datetime.fromtimestamp(event.completed_at).isoformat() if event.completed_at else None,
            "resources_affected": event.resources_affected
        }
    
    def get_scaling_stats(self) -> Dict[str, Any]:
        """Get scaling statistics"""
        active_policies = len([p for p in self.policies.values() if p.enabled])
        active_resources = len([r for r in self.resources.values() if r.state == ResourceState.RUNNING])
        
        return {
            "total_policies": len(self.policies),
            "active_policies": active_policies,
            "total_resources": len(self.resources),
            "active_resources": active_resources,
            "active_scaling_operations": self.active_scaling_operations,
            "total_scaling_events": self.total_scaling_events,
            "scale_out_count": self.scaling_stats["scale_out_count"],
            "scale_in_count": self.scaling_stats["scale_in_count"],
            "failed_operations": self.scaling_stats["failed_operations"],
            "average_response_time": self.scaling_stats["average_response_time"],
            "evaluation_interval": self.evaluation_interval,
            "max_concurrent_scaling": self.max_concurrent_scaling
        }
    
    def _get_current_capacity(self, resource_type: str) -> int:
        """Get current capacity for resource type"""
        return len([
            r for r in self.resources.values()
            if r.resource_type == resource_type and r.state == ResourceState.RUNNING
        ])
    
    def _calculate_target_capacity(self, 
                                 policy: ScalingPolicy,
                                 current_capacity: int,
                                 action: ScalingAction) -> int:
        """Calculate target capacity based on policy and action"""
        if action == ScalingAction.SCALE_OUT:
            target = current_capacity + self.threshold_policies[policy.policy_id].scale_out_adjustment
        elif action == ScalingAction.SCALE_IN:
            target = current_capacity - self.threshold_policies[policy.policy_id].scale_in_adjustment
        else:
            target = current_capacity
        
        # Apply bounds
        target = max(policy.min_capacity, min(target, policy.max_capacity))
        
        return target
    
    async def _execute_scaling(self, event: ScalingEvent):
        """Execute scaling operation"""
        try:
            start_time = time.time()
            
            # Simulate resource creation/deletion
            if event.action == ScalingAction.SCALE_OUT:
                await self._scale_out(event)
            elif event.action == ScalingAction.SCALE_IN:
                await self._scale_in(event)
            
            # Update statistics
            if event.action == ScalingAction.SCALE_OUT:
                self.scaling_stats["scale_out_count"] += 1
            elif event.action == ScalingAction.SCALE_IN:
                self.scaling_stats["scale_in_count"] += 1
            
            # Calculate response time
            response_time = time.time() - start_time
            self.scaling_stats["average_response_time"] = (
                (self.scaling_stats["average_response_time"] * (self.total_scaling_events - 1) + response_time) 
                / self.total_scaling_events
            )
            
            event.status = "completed"
            event.completed_at = time.time()
            
            self.logger.info(f"Scaling completed: {event.event_id}")
            
        except Exception as e:
            event.status = "failed"
            event.completed_at = time.time()
            self.scaling_stats["failed_operations"] += 1
            
            self.logger.error(f"Scaling failed: {event.event_id} - {e}")
        
        finally:
            self.active_scaling_operations -= 1
    
    async def _scale_out(self, event: ScalingEvent):
        """Scale out by creating new resources"""
        needed_capacity = event.target_capacity - event.current_capacity
        
        for i in range(needed_capacity):
            resource_id = self._create_resource(event.resource_type)
            event.resources_affected.append(resource_id)
            
            # Simulate resource startup time
            await asyncio.sleep(2)
            
            if resource_id in self.resources:
                self.resources[resource_id].state = ResourceState.RUNNING
    
    async def _scale_in(self, event: ScalingEvent):
        """Scale in by terminating resources"""
        resources_to_terminate = []
        
        # Find resources to terminate (oldest first)
        running_resources = [
            r for r in self.resources.values()
            if r.resource_type == event.resource_type and r.state == ResourceState.RUNNING
        ]
        
        running_resources.sort(key=lambda r: r.created_at)
        
        needed_reduction = event.current_capacity - event.target_capacity
        
        for i in range(min(needed_reduction, len(running_resources))):
            resource = running_resources[i]
            resources_to_terminate.append(resource.resource_id)
            resource.state = ResourceState.STOPPING
            
            # Simulate termination time
            await asyncio.sleep(1)
            resource.state = ResourceState.TERMINATED
        
        event.resources_affected = resources_to_terminate
    
    def _create_resource(self, resource_type: str) -> str:
        """Create a new resource"""
        resource_id = str(uuid.uuid4())
        resource = Resource(
            resource_id=resource_id,
            name=f"{resource_type}-{resource_id[:8]}",
            resource_type=resource_type,
            state=ResourceState.PENDING,
            created_at=time.time(),
            last_modified=time.time(),
            tags={"auto_scaling": "true"},
            metrics={}
        )
        
        self.resources[resource_id] = resource
        return resource_id
    
    def _evaluation_loop(self):
        """Background policy evaluation loop"""
        while True:
            try:
                self._evaluate_policies()
                time.sleep(self.evaluation_interval)
            except Exception as e:
                self.logger.error(f"Error in evaluation loop: {e}")
                time.sleep(self.evaluation_interval)
    
    def _evaluate_policies(self):
        """Evaluate all active policies"""
        current_time = datetime.now()
        
        for policy in self.policies.values():
            if not policy.enabled:
                continue
            
            # Check cooldown period
            last_event = self._get_last_scaling_event(policy.policy_id)
            if last_event and (current_time.timestamp() - last_event.triggered_at) < policy.cooldown_period:
                continue
            
            # Evaluate based on policy type
            if policy.policy_type == ScalingPolicyType.THRESHOLD:
                self._evaluate_threshold_policy(policy)
            elif policy.policy_type == ScalingPolicyType.SCHEDULE:
                self._evaluate_schedule_policy(policy, current_time)
            elif policy.policy_type == ScalingPolicyType.PREDICTIVE:
                self._evaluate_predictive_policy(policy)
    
    def _evaluate_threshold_policy(self, policy: ScalingPolicy):
        """Evaluate threshold-based policy"""
        if policy.policy_id not in self.threshold_policies:
            return
        
        threshold_policy = self.threshold_policies[policy.policy_id]
        current_capacity = self._get_current_capacity(policy.resource_type)
        
        # Get recent metrics for the resource type
        recent_metrics = self._get_recent_metrics(
            threshold_policy.metric_name, 
            threshold_policy.evaluation_periods
        )
        
        if not recent_metrics:
            return
        
        avg_value = statistics.mean(recent_metrics)
        
        # Determine action
        action = ScalingAction.NO_OP
        
        if avg_value > threshold_policy.scale_out_threshold:
            action = ScalingAction.SCALE_OUT
        elif avg_value < threshold_policy.scale_in_threshold:
            action = ScalingAction.SCALE_IN
        
        # Trigger scaling if needed
        if action != ScalingAction.NO_OP and self.active_scaling_operations < self.max_concurrent_scaling:
            asyncio.create_task(self._auto_trigger_scaling(policy.policy_id, action))
    
    def _evaluate_schedule_policy(self, policy: ScalingPolicy, current_time: datetime):
        """Evaluate schedule-based policy"""
        if policy.policy_id not in self.schedule_policies:
            return
        
        schedule_policy = self.schedule_policies[policy.policy_id]
        current_hour = current_time.hour
        
        # Find target capacity for current time
        target_capacity = policy.min_capacity  # Default to minimum
        
        for time_str, capacity in schedule_policy.schedule.items():
            if self._time_matches_schedule(time_str, current_hour):
                target_capacity = capacity
                break
        
        # Calculate current capacity
        current_capacity = self._get_current_capacity(policy.resource_type)
        
        # Determine action
        action = ScalingAction.NO_OP
        
        if target_capacity > current_capacity:
            action = ScalingAction.SCALE_OUT
        elif target_capacity < current_capacity:
            action = ScalingAction.SCALE_IN
        
        # Trigger scaling if needed
        if action != ScalingAction.NO_OP and self.active_scaling_operations < self.max_concurrent_scaling:
            asyncio.create_task(self._auto_trigger_scaling(policy.policy_id, action))
    
    def _evaluate_predictive_policy(self, policy: ScalingPolicy):
        """Evaluate predictive policy (simplified)"""
        # In a real implementation, this would use ML models to predict load
        # For now, we'll use a simple heuristic based on time of day
        current_hour = datetime.now().hour
        
        # Simple prediction: higher load during business hours
        if 9 <= current_hour <= 17:
            target_capacity = policy.max_capacity
        else:
            target_capacity = policy.min_capacity
        
        current_capacity = self._get_current_capacity(policy.resource_type)
        
        action = ScalingAction.NO_OP
        if target_capacity > current_capacity:
            action = ScalingAction.SCALE_OUT
        elif target_capacity < current_capacity:
            action = ScalingAction.SCALE_IN
        
        if action != ScalingAction.NO_OP and self.active_scaling_operations < self.max_concurrent_scaling:
            asyncio.create_task(self._auto_trigger_scaling(policy.policy_id, action))
    
    async def _auto_trigger_scaling(self, policy_id: str, action: ScalingAction):
        """Automatically trigger scaling"""
        try:
            await self.trigger_scaling(policy_id, action)
        except Exception as e:
            self.logger.error(f"Auto scaling failed: {policy_id} - {e}")
    
    def _get_recent_metrics(self, metric_name: str, periods: int) -> List[float]:
        """Get recent metrics for evaluation"""
        # This would integrate with the monitoring system
        # For now, return simulated data
        return [75.0, 80.0, 85.0, 90.0][:periods]
    
    def _time_matches_schedule(self, time_str: str, current_hour: int) -> bool:
        """Check if current time matches schedule entry"""
        try:
            if "-" in time_str:
                start_hour, end_hour = map(int, time_str.split("-"))
                return start_hour <= current_hour <= end_hour
            else:
                return int(time_str) == current_hour
        except:
            return False
    
    def _get_last_scaling_event(self, policy_id: str) -> Optional[ScalingEvent]:
        """Get the last scaling event for a policy"""
        policy_events = [
            event for event in self.scaling_events.values()
            if event.policy_id == policy_id
        ]
        
        if not policy_events:
            return None
        
        return max(policy_events, key=lambda e: e.triggered_at)

# Global auto scaling manager instance
_scaling_manager = AutoScalingManager({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "create_policy", "register_resource", "trigger_scaling", 
                     "get_status", "get_stats", "update_metrics"
            - policy_data: Policy configuration
            - resource_data: Resource data
            - scaling_data: Scaling parameters
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "create_policy":
            policy_data = payload.get("policy_data", {})
            
            policy_id = _scaling_manager.create_scaling_policy(
                name=policy_data.get("name", "Scaling Policy"),
                description=policy_data.get("description", ""),
                policy_type=ScalingPolicyType(policy_data.get("policy_type", "threshold")),
                resource_type=policy_data.get("resource_type", "instance"),
                min_capacity=policy_data.get("min_capacity", 1),
                max_capacity=policy_data.get("max_capacity", 10),
                target_capacity=policy_data.get("target_capacity"),
                cooldown_period=policy_data.get("cooldown_period")
            )
            
            # Create specific policy configuration
            if policy_data.get("policy_type") == "threshold":
                await _scaling_manager.create_threshold_policy(
                    policy_id=policy_id,
                    metric_name=policy_data.get("metric_name", "cpu_usage"),
                    scale_out_threshold=policy_data.get("scale_out_threshold", 80.0),
                    scale_in_threshold=policy_data.get("scale_in_threshold", 40.0),
                    evaluation_periods=policy_data.get("evaluation_periods", 5),
                    scale_out_adjustment=policy_data.get("scale_out_adjustment", 2),
                    scale_in_adjustment=policy_data.get("scale_in_adjustment", 1)
                )
            elif policy_data.get("policy_type") == "schedule":
                await _scaling_manager.create_schedule_policy(
                    policy_id=policy_id,
                    schedule=policy_data.get("schedule", {"9-17": 5, "18-22": 3, "23-8": 1}),
                    timezone=policy_data.get("timezone", "UTC")
                )
            
            return {
                "result": {
                    "policy_id": policy_id,
                    "message": f"Created scaling policy: {policy_id}"
                },
                "metadata": {
                    "action": "create_policy",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "register_resource":
            resource_data = payload.get("resource_data", {})
            
            resource_id = _scaling_manager.register_resource(
                name=resource_data.get("name", "Resource"),
                resource_type=resource_data.get("resource_type", "instance"),
                tags=resource_data.get("tags", {})
            )
            
            return {
                "result": {
                    "resource_id": resource_id,
                    "message": f"Registered resource: {resource_id}"
                },
                "metadata": {
                    "action": "register_resource",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "trigger_scaling":
            scaling_data = payload.get("scaling_data", {})
            
            event_id = await _scaling_manager.trigger_scaling(
                policy_id=scaling_data.get("policy_id", ""),
                action=ScalingAction(scaling_data.get("action", "scale_out"))
            )
            
            return {
                "result": {
                    "event_id": event_id,
                    "message": f"Triggered scaling: {event_id}"
                },
                "metadata": {
                    "action": "trigger_scaling",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_status":
            event_id = payload.get("event_id", "")
            status = _scaling_manager.get_scaling_status(event_id)
            
            return {
                "result": status,
                "metadata": {
                    "action": "get_status",
                    "timestamp": datetime.now().isoformat(),
                    "event_id": event_id
                }
            }
        
        elif action == "get_stats":
            stats = _scaling_manager.get_scaling_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "update_metrics":
            resource_id = payload.get("resource_id", "")
            metrics = payload.get("metrics", {})
            
            _scaling_manager.update_resource_metrics(resource_id, metrics)
            
            return {
                "result": {
                    "resource_id": resource_id,
                    "metrics": metrics,
                    "message": f"Updated metrics for resource: {resource_id}"
                },
                "metadata": {
                    "action": "update_metrics",
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
        logger.error(f"Error in auto_scaling_manager: {e}")
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
    """Example of how to use the auto scaling manager skill"""
    
    # Create a scaling policy
    policy_id = await invoke({
        "action": "create_policy",
        "policy_data": {
            "name": "Web Server Auto Scaling",
            "description": "Auto scale web servers based on CPU usage",
            "policy_type": "threshold",
            "resource_type": "web-server",
            "min_capacity": 2,
            "max_capacity": 10,
            "metric_name": "cpu_usage",
            "scale_out_threshold": 70.0,
            "scale_in_threshold": 30.0,
            "evaluation_periods": 5,
            "scale_out_adjustment": 2,
            "scale_in_adjustment": 1
        }
    })
    
    print(f"Created policy: {policy_id['result']['policy_id']}")
    
    # Register some resources
    for i in range(3):
        resource_id = await invoke({
            "action": "register_resource",
            "resource_data": {
                "name": f"web-server-{i+1}",
                "resource_type": "web-server",
                "tags": {"environment": "production"}
            }
        })
        print(f"Registered resource: {resource_id['result']['resource_id']}")
    
    # Update metrics to trigger scaling
    await invoke({
        "action": "update_metrics",
        "resource_id": "web-server-1",
        "metrics": {"cpu_usage": 85.0, "memory_usage": 70.0}
    })
    
    # Get scaling statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Scaling stats: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
