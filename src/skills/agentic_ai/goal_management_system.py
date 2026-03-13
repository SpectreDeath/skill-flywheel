#!/usr/bin/env python3
"""
Skill: goal-management-system
Domain: agentic_ai
Description: Intelligent goal management system for AI agents with priority handling and progress tracking
"""

import asyncio
import logging
import time
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import uuid

logger = logging.getLogger(__name__)

class GoalPriority(Enum):
    """Goal priority levels"""
    CRITICAL = "critical"      # Must be completed immediately
    HIGH = "high"            # Important, should be completed soon
    MEDIUM = "medium"        # Normal priority
    LOW = "low"              # Can be deferred
    BACKGROUND = "background" # Lowest priority, runs when idle

class GoalStatus(Enum):
    """Goal status states"""
    PENDING = "pending"        # Not yet started
    ACTIVE = "active"         # Currently being worked on
    PAUSED = "paused"         # Temporarily stopped
    COMPLETED = "completed"   # Successfully finished
    FAILED = "failed"         # Could not be completed
    CANCELLED = "cancelled"   # Manually cancelled

class GoalType(Enum):
    """Types of goals"""
    TASK = "task"            # Specific task to complete
    LEARNING = "learning"    # Learning objective
    EXPLORATION = "exploration" # Exploration or research goal
    MAINTENANCE = "maintenance" # System maintenance goal
    CREATIVE = "creative"    # Creative or generative goal

@dataclass
class Goal:
    """Represents a goal for an AI agent"""
    goal_id: str
    description: str
    goal_type: GoalType
    priority: GoalPriority
    status: GoalStatus
    created_at: float
    target_completion: Optional[float]
    progress: float  # 0.0 to 1.0
    dependencies: List[str]  # List of goal IDs this goal depends on
    estimated_effort: int   # Estimated effort units required
    actual_effort: int      # Actual effort units spent
    metadata: Dict[str, Any]

@dataclass
class GoalProgress:
    """Represents progress update for a goal"""
    goal_id: str
    progress: float
    effort_spent: int
    timestamp: float
    notes: str

class GoalManagementSystem:
    """Intelligent goal management system for AI agents"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the goal management system
        
        Args:
            config: Configuration dictionary with:
                - max_concurrent_goals: Maximum number of concurrent active goals
                - auto_priority_adjustment: Whether to auto-adjust priorities
                - progress_check_interval: Interval for progress checks
        """
        self.max_concurrent_goals = config.get("max_concurrent_goals", 3)
        self.auto_priority_adjustment = config.get("auto_priority_adjustment", True)
        self.progress_check_interval = config.get("progress_check_interval", 60)
        self.goals: Dict[str, Goal] = {}
        self.active_goals: List[str] = []
        self.logger = logging.getLogger(__name__)
        
    def create_goal(self, 
                   description: str,
                   goal_type: GoalType,
                   priority: GoalPriority,
                   target_completion: Optional[datetime] = None,
                   dependencies: List[str] = None,
                   estimated_effort: int = 1,
                   metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a new goal
        
        Args:
            description: Goal description
            goal_type: Type of goal
            priority: Goal priority
            target_completion: Target completion time
            dependencies: List of goal IDs this goal depends on
            estimated_effort: Estimated effort required
            metadata: Additional goal metadata
            
        Returns:
            Goal ID
        """
        goal_id = str(uuid.uuid4())
        goal = Goal(
            goal_id=goal_id,
            description=description,
            goal_type=goal_type,
            priority=priority,
            status=GoalStatus.PENDING,
            created_at=time.time(),
            target_completion=target_completion.timestamp() if target_completion else None,
            progress=0.0,
            dependencies=dependencies or [],
            estimated_effort=estimated_effort,
            actual_effort=0,
            metadata=metadata or {}
        )
        
        self.goals[goal_id] = goal
        self.logger.info(f"Created goal {goal_id}: {description}")
        
        # Auto-start if no dependencies and high priority
        if not dependencies and priority in [GoalPriority.CRITICAL, GoalPriority.HIGH]:
            asyncio.create_task(self.activate_goal(goal_id))
        
        return goal_id
    
    async def activate_goal(self, goal_id: str) -> bool:
        """
        Activate a goal for execution
        
        Args:
            goal_id: ID of the goal to activate
            
        Returns:
            True if successfully activated, False otherwise
        """
        if goal_id not in self.goals:
            self.logger.error(f"Goal {goal_id} not found")
            return False
        
        goal = self.goals[goal_id]
        
        # Check if goal can be activated
        if not self._can_activate_goal(goal):
            self.logger.warning(f"Cannot activate goal {goal_id}: dependencies not met or max concurrent goals reached")
            return False
        
        # Check dependencies
        for dep_id in goal.dependencies:
            if dep_id not in self.goals:
                self.logger.error(f"Dependency {dep_id} not found for goal {goal_id}")
                return False
            
            dep_goal = self.goals[dep_id]
            if dep_goal.status != GoalStatus.COMPLETED:
                self.logger.warning(f"Cannot activate goal {goal_id}: dependency {dep_id} not completed")
                return False
        
        # Activate goal
        goal.status = GoalStatus.ACTIVE
        goal.actual_effort += 1  # Initial effort
        self.active_goals.append(goal_id)
        
        self.logger.info(f"Activated goal {goal_id}: {goal.description}")
        
        # Start goal execution in background
        asyncio.create_task(self._execute_goal(goal_id))
        
        return True
    
    def pause_goal(self, goal_id: str) -> bool:
        """Pause an active goal"""
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        if goal.status == GoalStatus.ACTIVE:
            goal.status = GoalStatus.PAUSED
            if goal_id in self.active_goals:
                self.active_goals.remove(goal_id)
            self.logger.info(f"Paused goal {goal_id}")
            return True
        
        return False
    
    def complete_goal(self, goal_id: str, success: bool = True, notes: str = "") -> bool:
        """Mark a goal as completed or failed"""
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        if goal.status in [GoalStatus.ACTIVE, GoalStatus.PAUSED]:
            goal.status = GoalStatus.COMPLETED if success else GoalStatus.FAILED
            goal.progress = 1.0 if success else goal.progress
            goal.metadata["completion_notes"] = notes
            goal.metadata["completed_at"] = time.time()
            
            if goal_id in self.active_goals:
                self.active_goals.remove(goal_id)
            
            self.logger.info(f"Goal {goal_id} {'completed' if success else 'failed'}: {notes}")
            
            # Activate dependent goals
            asyncio.create_task(self._activate_dependent_goals(goal_id))
            
            return True
        
        return False
    
    async def update_progress(self, goal_id: str, progress: float, effort_spent: int = 1, notes: str = "") -> bool:
        """Update goal progress"""
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        if goal.status == GoalStatus.ACTIVE:
            # Clamp progress between 0 and 1
            goal.progress = max(0.0, min(1.0, progress))
            goal.actual_effort += effort_spent
            
            # Check if goal is completed
            if goal.progress >= 1.0:
                await self.complete_goal(goal_id, success=True, notes=f"Completed via progress update: {notes}")
            else:
                self.logger.debug(f"Updated progress for goal {goal_id}: {progress:.2%}")
            
            return True
        
        return False
    
    def get_goals(self, status: Optional[GoalStatus] = None, 
                  priority: Optional[GoalPriority] = None) -> List[Dict[str, Any]]:
        """Get goals filtered by status and priority"""
        filtered_goals = []
        
        for goal in self.goals.values():
            if status and goal.status != status:
                continue
            if priority and goal.priority != priority:
                continue
            
            goal_dict = asdict(goal)
            goal_dict['created_at'] = datetime.fromtimestamp(goal.created_at).isoformat()
            if goal.target_completion:
                goal_dict['target_completion'] = datetime.fromtimestamp(goal.target_completion).isoformat()
            
            filtered_goals.append(goal_dict)
        
        # Sort by priority and creation time
        priority_order = {
            GoalPriority.CRITICAL: 0,
            GoalPriority.HIGH: 1,
            GoalPriority.MEDIUM: 2,
            GoalPriority.LOW: 3,
            GoalPriority.BACKGROUND: 4
        }
        
        filtered_goals.sort(key=lambda g: (
            priority_order.get(GoalPriority(g['priority']), 5),
            -g['created_at']  # Most recent first
        ))
        
        return filtered_goals
    
    def get_active_goals(self) -> List[Dict[str, Any]]:
        """Get all active goals"""
        return self.get_goals(status=GoalStatus.ACTIVE)
    
    def get_goal_stats(self) -> Dict[str, Any]:
        """Get goal statistics"""
        total_goals = len(self.goals)
        active_count = len(self.active_goals)
        
        status_counts = {}
        for status in GoalStatus:
            status_counts[status.value] = sum(1 for g in self.goals.values() if g.status == status)
        
        priority_counts = {}
        for priority in GoalPriority:
            priority_counts[priority.value] = sum(1 for g in self.goals.values() if g.priority == priority)
        
        # Calculate average progress
        active_goals = [g for g in self.goals.values() if g.status == GoalStatus.ACTIVE]
        avg_progress = sum(g.progress for g in active_goals) / len(active_goals) if active_goals else 0.0
        
        return {
            "total_goals": total_goals,
            "active_goals": active_count,
            "max_concurrent_goals": self.max_concurrent_goals,
            "status_distribution": status_counts,
            "priority_distribution": priority_counts,
            "average_progress": avg_progress,
            "completion_rate": status_counts.get(GoalStatus.COMPLETED.value, 0) / total_goals if total_goals > 0 else 0.0
        }
    
    def _can_activate_goal(self, goal: Goal) -> bool:
        """Check if a goal can be activated"""
        # Check if max concurrent goals limit reached
        if len(self.active_goals) >= self.max_concurrent_goals:
            return False
        
        # Check if goal is already active
        if goal.status == GoalStatus.ACTIVE:
            return False
        
        # Check dependencies
        for dep_id in goal.dependencies:
            if dep_id not in self.goals:
                return False
            if self.goals[dep_id].status != GoalStatus.COMPLETED:
                return False
        
        return True
    
    async def _execute_goal(self, goal_id: str):
        """Execute a goal (simulated execution)"""
        if goal_id not in self.goals:
            return
        
        goal = self.goals[goal_id]
        self.logger.info(f"Starting execution of goal {goal_id}: {goal.description}")
        
        try:
            # Simulate goal execution
            while goal.status == GoalStatus.ACTIVE and goal.progress < 1.0:
                # Simulate work being done
                await asyncio.sleep(2)
                
                # Update progress
                progress_increment = 0.1
                new_progress = min(1.0, goal.progress + progress_increment)
                await self.update_progress(goal_id, new_progress, effort_spent=1, notes="Simulated progress")
                
                # Check for goal completion
                if new_progress >= 1.0:
                    await self.complete_goal(goal_id, success=True, notes="Goal completed through execution")
                    break
                
                # Check for timeout or failure conditions
                if goal.target_completion and time.time() > goal.target_completion:
                    await self.complete_goal(goal_id, success=False, notes="Goal failed due to timeout")
                    break
        
        except Exception as e:
            self.logger.error(f"Error executing goal {goal_id}: {e}")
            await self.complete_goal(goal_id, success=False, notes=f"Execution failed: {str(e)}")
    
    async def _activate_dependent_goals(self, completed_goal_id: str):
        """Activate goals that depend on the completed goal"""
        for goal in self.goals.values():
            if completed_goal_id in goal.dependencies and goal.status == GoalStatus.PENDING:
                # Check if all dependencies are now satisfied
                all_deps_completed = all(
                    self.goals[dep_id].status == GoalStatus.COMPLETED 
                    for dep_id in goal.dependencies
                )
                
                if all_deps_completed:
                    await self.activate_goal(goal.goal_id)
    
    def cancel_goal(self, goal_id: str, reason: str = "") -> bool:
        """Cancel a goal"""
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        if goal.status in [GoalStatus.PENDING, GoalStatus.ACTIVE, GoalStatus.PAUSED]:
            goal.status = GoalStatus.CANCELLED
            goal.metadata["cancellation_reason"] = reason
            goal.metadata["cancelled_at"] = time.time()
            
            if goal_id in self.active_goals:
                self.active_goals.remove(goal_id)
            
            self.logger.info(f"Cancelled goal {goal_id}: {reason}")
            return True
        
        return False
    
    def adjust_goal_priority(self, goal_id: str, new_priority: GoalPriority) -> bool:
        """Adjust goal priority"""
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        old_priority = goal.priority
        goal.priority = new_priority
        
        self.logger.info(f"Adjusted priority for goal {goal_id}: {old_priority.value} -> {new_priority.value}")
        return True

# Global goal management system instance
_goal_system = GoalManagementSystem({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "create", "activate", "pause", "complete", "update_progress", 
                     "get_goals", "get_stats", "cancel", "adjust_priority"
            - goal_data: Goal configuration data
            - goal_id: Goal identifier
            - progress: Progress value (0.0 to 1.0)
            - config: Configuration for the goal system
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_goals")
    
    try:
        if action == "create":
            goal_data = payload.get("goal_data", {})
            
            goal_id = _goal_system.create_goal(
                description=goal_data.get("description", ""),
                goal_type=GoalType(goal_data.get("goal_type", "task")),
                priority=GoalPriority(goal_data.get("priority", "medium")),
                target_completion=None,  # Could be parsed from string
                dependencies=goal_data.get("dependencies", []),
                estimated_effort=goal_data.get("estimated_effort", 1),
                metadata=goal_data.get("metadata", {})
            )
            
            return {
                "result": {
                    "goal_id": goal_id,
                    "message": f"Created goal: {goal_id}"
                },
                "metadata": {
                    "action": "create",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "activate":
            goal_id = payload.get("goal_id", "")
            success = await _goal_system.activate_goal(goal_id)
            
            return {
                "result": {
                    "goal_id": goal_id,
                    "success": success,
                    "message": f"Activated goal: {goal_id}" if success else f"Failed to activate goal: {goal_id}"
                },
                "metadata": {
                    "action": "activate",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "pause":
            goal_id = payload.get("goal_id", "")
            success = _goal_system.pause_goal(goal_id)
            
            return {
                "result": {
                    "goal_id": goal_id,
                    "success": success,
                    "message": f"Paused goal: {goal_id}" if success else f"Failed to pause goal: {goal_id}"
                },
                "metadata": {
                    "action": "pause",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "complete":
            goal_id = payload.get("goal_id", "")
            success_param = payload.get("success", True)
            notes = payload.get("notes", "")
            success = _goal_system.complete_goal(goal_id, success_param, notes)
            
            return {
                "result": {
                    "goal_id": goal_id,
                    "success": success,
                    "message": f"Completed goal: {goal_id}" if success else f"Failed goal: {goal_id}"
                },
                "metadata": {
                    "action": "complete",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "update_progress":
            goal_id = payload.get("goal_id", "")
            progress = payload.get("progress", 0.0)
            effort_spent = payload.get("effort_spent", 1)
            notes = payload.get("notes", "")
            
            success = await _goal_system.update_progress(goal_id, progress, effort_spent, notes)
            
            return {
                "result": {
                    "goal_id": goal_id,
                    "success": success,
                    "progress": progress,
                    "message": f"Updated progress for goal: {goal_id}" if success else f"Failed to update progress for goal: {goal_id}"
                },
                "metadata": {
                    "action": "update_progress",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_goals":
            status = payload.get("status")
            priority = payload.get("priority")
            
            if status:
                status = GoalStatus(status)
            if priority:
                priority = GoalPriority(priority)
            
            goals = _goal_system.get_goals(status=status, priority=priority)
            
            return {
                "result": goals,
                "metadata": {
                    "action": "get_goals",
                    "timestamp": datetime.now().isoformat(),
                    "filter_status": status.value if status else None,
                    "filter_priority": priority.value if priority else None
                }
            }
        
        elif action == "get_stats":
            stats = _goal_system.get_goal_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "cancel":
            goal_id = payload.get("goal_id", "")
            reason = payload.get("reason", "")
            success = _goal_system.cancel_goal(goal_id, reason)
            
            return {
                "result": {
                    "goal_id": goal_id,
                    "success": success,
                    "message": f"Cancelled goal: {goal_id}" if success else f"Failed to cancel goal: {goal_id}"
                },
                "metadata": {
                    "action": "cancel",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "adjust_priority":
            goal_id = payload.get("goal_id", "")
            new_priority = GoalPriority(payload.get("new_priority", "medium"))
            success = _goal_system.adjust_goal_priority(goal_id, new_priority)
            
            return {
                "result": {
                    "goal_id": goal_id,
                    "success": success,
                    "message": f"Adjusted priority for goal: {goal_id}" if success else f"Failed to adjust priority for goal: {goal_id}"
                },
                "metadata": {
                    "action": "adjust_priority",
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
        logger.error(f"Error in goal_management_system: {e}")
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
    """Example of how to use the goal management system skill"""
    
    # Create some goals
    goal1_id = await invoke({
        "action": "create",
        "goal_data": {
            "description": "Implement user authentication system",
            "goal_type": "task",
            "priority": "high",
            "estimated_effort": 5
        }
    })
    
    goal2_id = await invoke({
        "action": "create",
        "goal_data": {
            "description": "Write unit tests for authentication",
            "goal_type": "task",
            "priority": "medium",
            "dependencies": [goal1_id["result"]["goal_id"]]
        }
    })
    
    # Activate goals
    await invoke({"action": "activate", "goal_id": goal1_id["result"]["goal_id"]})
    
    # Get goal stats
    stats = await invoke({"action": "get_stats"})
    print(f"Goal stats: {stats['result']}")
    
    # Update progress
    await invoke({
        "action": "update_progress",
        "goal_id": goal1_id["result"]["goal_id"],
        "progress": 0.5,
        "notes": "Halfway through implementation"
    })

if __name__ == "__main__":
    asyncio.run(example_usage())