#!/usr/bin/env python3
"""
Skill: self-improvement-engine
Domain: agentic_ai
Description: Self-improvement engine for AI agents that learns from experience and optimizes performance
"""

import asyncio
import logging
import time
import json
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import uuid
import statistics

logger = logging.getLogger(__name__)

class ImprovementType(Enum):
    """Types of improvements"""
    PERFORMANCE = "performance"      # Speed, efficiency improvements
    ACCURACY = "accuracy"           # Correctness improvements
    STRATEGY = "strategy"           # Approach and method improvements
    LEARNING = "learning"           # Knowledge and pattern improvements
    ADAPTATION = "adaptation"       # Environmental adaptation

class FeedbackSource(Enum):
    """Sources of feedback for improvement"""
    USER = "user"                  # Direct user feedback
    SELF_ASSESSMENT = "self_assessment" # Self-evaluation
    COMPARISON = "comparison"      # Comparison with expected results
    METRICS = "metrics"            # Performance metrics
    ERROR_ANALYSIS = "error_analysis" # Analysis of failures

@dataclass
class Experience:
    """Represents a learning experience"""
    experience_id: str
    timestamp: float
    task_description: str
    input_data: Dict[str, Any]
    output_result: Dict[str, Any]
    performance_metrics: Dict[str, float]
    success: bool
    feedback: List[Dict[str, Any]]
    lessons_learned: List[str]

@dataclass
class ImprovementAction:
    """Represents an improvement action to be taken"""
    action_id: str
    improvement_type: ImprovementType
    description: str
    priority: int  # 1-10 scale
    estimated_impact: float  # 0.0 to 1.0
    implementation_cost: int  # Effort units required
    status: str  # pending, in_progress, completed, failed
    created_at: float
    completed_at: Optional[float]
    results: Optional[Dict[str, Any]]

class SelfImprovementEngine:
    """Self-improvement engine for AI agents"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the self-improvement engine
        
        Args:
            config: Configuration dictionary with:
                - learning_rate: How quickly to adapt (0.0 to 1.0)
                - memory_size: Number of experiences to remember
                - improvement_threshold: Minimum improvement needed to act
                - feedback_weight: Weight given to different feedback sources
        """
        self.learning_rate = config.get("learning_rate", 0.1)
        self.memory_size = config.get("memory_size", 100)
        self.improvement_threshold = config.get("improvement_threshold", 0.05)
        self.feedback_weights = config.get("feedback_weights", {
            "user": 0.4,
            "self_assessment": 0.2,
            "comparison": 0.2,
            "metrics": 0.1,
            "error_analysis": 0.1
        })
        
        self.experiences: List[Experience] = []
        self.improvement_actions: List[ImprovementAction] = []
        self.performance_history: List[Dict[str, Any]] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)
        
    def record_experience(self, 
                         task_description: str,
                         input_data: Dict[str, Any],
                         output_result: Dict[str, Any],
                         performance_metrics: Dict[str, float],
                         success: bool,
                         feedback: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Record a learning experience
        
        Args:
            task_description: Description of the task performed
            input_data: Input data for the task
            output_result: Output result of the task
            performance_metrics: Performance metrics (time, accuracy, etc.)
            success: Whether the task was successful
            feedback: List of feedback from various sources
            
        Returns:
            Experience ID
        """
        experience_id = str(uuid.uuid4())
        experience = Experience(
            experience_id=experience_id,
            timestamp=time.time(),
            task_description=task_description,
            input_data=input_data,
            output_result=output_result,
            performance_metrics=performance_metrics,
            success=success,
            feedback=feedback or [],
            lessons_learned=[]
        )
        
        self.experiences.append(experience)
        
        # Maintain memory size limit
        if len(self.experiences) > self.memory_size:
            self.experiences.pop(0)
        
        # Analyze experience for improvement opportunities
        asyncio.create_task(self._analyze_experience(experience))
        
        self.logger.info(f"Recorded experience: {experience_id}")
        return experience_id
    
    async def _analyze_experience(self, experience: Experience):
        """Analyze an experience for improvement opportunities"""
        try:
            # Extract patterns and lessons
            lessons = await self._extract_lessons(experience)
            experience.lessons_learned = lessons
            
            # Generate improvement actions
            actions = await self._generate_improvement_actions(experience, lessons)
            
            # Add to improvement actions
            for action in actions:
                self.improvement_actions.append(action)
            
            # Update knowledge base
            await self._update_knowledge_base(experience, lessons)
            
            self.logger.info(f"Analyzed experience {experience.experience_id}: {len(lessons)} lessons, {len(actions)} actions")
            
        except Exception as e:
            self.logger.error(f"Error analyzing experience: {e}")
    
    async def _extract_lessons(self, experience: Experience) -> List[str]:
        """Extract lessons from an experience"""
        lessons = []
        
        # Analyze performance metrics
        metrics = experience.performance_metrics
        if "execution_time" in metrics:
            if metrics["execution_time"] > 5.0:  # Arbitrary threshold
                lessons.append("Task took too long, need optimization")
        
        if "accuracy" in metrics:
            if metrics["accuracy"] < 0.8:  # 80% threshold
                lessons.append("Accuracy below threshold, need better approach")
        
        # Analyze feedback
        for feedback in experience.feedback:
            feedback_type = feedback.get("type", "")
            content = feedback.get("content", "")
            
            if feedback_type == "user" and "improve" in content.lower():
                lessons.append(f"User requested improvement: {content}")
            elif feedback_type == "error_analysis" and not experience.success:
                lessons.append(f"Error analysis: {content}")
        
        # Analyze patterns with previous experiences
        similar_experiences = self._find_similar_experiences(experience)
        if similar_experiences:
            avg_performance = self._calculate_avg_performance(similar_experiences)
            current_performance = experience.performance_metrics
            
            for metric, avg_value in avg_performance.items():
                if metric in current_performance:
                    if current_performance[metric] < avg_value * 0.8:
                        lessons.append(f"Performance below average for similar tasks in {metric}")
        
        return lessons
    
    def _find_similar_experiences(self, experience: Experience, threshold: float = 0.7) -> List[Experience]:
        """Find similar experiences based on task description"""
        similar = []
        
        # Simple similarity check based on task description keywords
        current_keywords = set(experience.task_description.lower().split())
        
        for exp in self.experiences[:-1]:  # Exclude current experience
            exp_keywords = set(exp.task_description.lower().split())
            similarity = len(current_keywords & exp_keywords) / len(current_keywords | exp_keywords)
            
            if similarity >= threshold:
                similar.append(exp)
        
        return similar
    
    def _calculate_avg_performance(self, experiences: List[Experience]) -> Dict[str, float]:
        """Calculate average performance metrics for a list of experiences"""
        if not experiences:
            return {}
        
        metrics = {}
        for exp in experiences:
            for key, value in exp.performance_metrics.items():
                if key not in metrics:
                    metrics[key] = []
                metrics[key].append(value)
        
        avg_metrics = {}
        for key, values in metrics.items():
            avg_metrics[key] = statistics.mean(values)
        
        return avg_metrics
    
    async def _generate_improvement_actions(self, experience: Experience, lessons: List[str]) -> List[ImprovementAction]:
        """Generate improvement actions based on lessons learned"""
        actions = []
        
        for lesson in lessons:
            # Determine improvement type based on lesson
            if "optimization" in lesson or "too long" in lesson:
                improvement_type = ImprovementType.PERFORMANCE
                priority = 7
                impact = 0.3
            elif "accuracy" in lesson or "better approach" in lesson:
                improvement_type = ImprovementType.ACCURACY
                priority = 8
                impact = 0.4
            elif "user requested" in lesson:
                improvement_type = ImprovementType.ADAPTATION
                priority = 9
                impact = 0.5
            elif "below average" in lesson:
                improvement_type = ImprovementType.STRATEGY
                priority = 6
                impact = 0.2
            else:
                improvement_type = ImprovementType.LEARNING
                priority = 5
                impact = 0.1
            
            action = ImprovementAction(
                action_id=str(uuid.uuid4()),
                improvement_type=improvement_type,
                description=lesson,
                priority=priority,
                estimated_impact=impact,
                implementation_cost=priority * 2,  # Higher priority = higher cost
                status="pending",
                created_at=time.time(),
                completed_at=None,
                results=None
            )
            
            actions.append(action)
        
        return actions
    
    async def _update_knowledge_base(self, experience: Experience, lessons: List[str]):
        """Update the knowledge base with new insights"""
        # Extract key concepts from task description
        keywords = experience.task_description.lower().split()
        
        for keyword in keywords:
            if keyword not in self.knowledge_base:
                self.knowledge_base[keyword] = {
                    "success_rate": 0.0,
                    "avg_performance": {},
                    "common_issues": [],
                    "best_practices": []
                }
            
            # Update success rate
            kb_entry = self.knowledge_base[keyword]
            total_attempts = len([e for e in self.experiences if keyword in e.task_description.lower()])
            successful_attempts = len([e for e in self.experiences if keyword in e.task_description.lower() and e.success])
            
            if total_attempts > 0:
                kb_entry["success_rate"] = successful_attempts / total_attempts
            
            # Update average performance
            similar_experiences = [e for e in self.experiences if keyword in e.task_description.lower()]
            if similar_experiences:
                kb_entry["avg_performance"] = self._calculate_avg_performance(similar_experiences)
            
            # Add lessons as best practices or common issues
            for lesson in lessons:
                if "improve" in lesson or "better" in lesson:
                    if lesson not in kb_entry["best_practices"]:
                        kb_entry["best_practices"].append(lesson)
                else:
                    if lesson not in kb_entry["common_issues"]:
                        kb_entry["common_issues"].append(lesson)
    
    def get_improvement_suggestions(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get prioritized improvement suggestions"""
        pending_actions = [a for a in self.improvement_actions if a.status == "pending"]
        
        # Sort by priority and estimated impact
        pending_actions.sort(key=lambda a: (a.priority, a.estimated_impact), reverse=True)
        
        suggestions = []
        for action in pending_actions[:limit]:
            suggestions.append({
                "action_id": action.action_id,
                "improvement_type": action.improvement_type.value,
                "description": action.description,
                "priority": action.priority,
                "estimated_impact": action.estimated_impact,
                "implementation_cost": action.implementation_cost,
                "created_at": datetime.fromtimestamp(action.created_at).isoformat()
            })
        
        return suggestions
    
    def implement_improvement(self, action_id: str) -> bool:
        """Implement an improvement action"""
        action = next((a for a in self.improvement_actions if a.action_id == action_id), None)
        
        if not action or action.status != "pending":
            return False
        
        # Simulate implementation
        action.status = "in_progress"
        
        # Simulate the improvement process
        asyncio.create_task(self._execute_improvement(action))
        
        return True
    
    async def _execute_improvement(self, action: ImprovementAction):
        """Execute an improvement action"""
        try:
            # Simulate improvement implementation
            await asyncio.sleep(1)
            
            # Simulate results
            results = {
                "improvement_applied": True,
                "performance_gain": action.estimated_impact * 0.8,  # 80% of estimated impact
                "implementation_time": action.implementation_cost * 0.5,
                "side_effects": []
            }
            
            action.status = "completed"
            action.completed_at = time.time()
            action.results = results
            
            # Apply the improvement to the learning rate
            if action.improvement_type == ImprovementType.PERFORMANCE:
                self.learning_rate += 0.01
            elif action.improvement_type == ImprovementType.ACCURACY:
                self.learning_rate += 0.02
            
            self.logger.info(f"Completed improvement: {action.description}")
            
        except Exception as e:
            action.status = "failed"
            action.results = {"error": str(e)}
            self.logger.error(f"Failed to implement improvement: {e}")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get a performance improvement report"""
        total_experiences = len(self.experiences)
        successful_experiences = len([e for e in self.experiences if e.success])
        
        # Calculate improvement trends
        if len(self.experiences) >= 2:
            recent_experiences = self.experiences[-10:]  # Last 10 experiences
            older_experiences = self.experiences[-20:-10]  # Previous 10 experiences
            
            recent_success_rate = len([e for e in recent_experiences if e.success]) / len(recent_experiences)
            older_success_rate = len([e for e in older_experiences if e.success]) / len(older_experiences) if older_experiences else 0
            
            success_trend = recent_success_rate - older_success_rate
        else:
            success_trend = 0
        
        # Improvement actions summary
        completed_actions = [a for a in self.improvement_actions if a.status == "completed"]
        pending_actions = [a for a in self.improvement_actions if a.status == "pending"]
        
        return {
            "total_experiences": total_experiences,
            "success_rate": successful_experiences / total_experiences if total_experiences > 0 else 0,
            "success_trend": success_trend,
            "completed_improvements": len(completed_actions),
            "pending_improvements": len(pending_actions),
            "learning_rate": self.learning_rate,
            "knowledge_base_size": len(self.knowledge_base),
            "avg_performance_metrics": self._calculate_avg_performance(self.experiences) if self.experiences else {},
            "improvement_summary": {
                "performance": len([a for a in completed_actions if a.improvement_type == ImprovementType.PERFORMANCE]),
                "accuracy": len([a for a in completed_actions if a.improvement_type == ImprovementType.ACCURACY]),
                "strategy": len([a for a in completed_actions if a.improvement_type == ImprovementType.STRATEGY]),
                "learning": len([a for a in completed_actions if a.improvement_type == ImprovementType.LEARNING]),
                "adaptation": len([a for a in completed_actions if a.improvement_type == ImprovementType.ADAPTATION])
            }
        }
    
    def get_knowledge_insights(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """Get knowledge base insights"""
        if topic:
            if topic.lower() in self.knowledge_base:
                return self.knowledge_base[topic.lower()]
            else:
                return {"error": f"No knowledge found for topic: {topic}"}
        
        # Return summary of all knowledge
        return {
            "topics": list(self.knowledge_base.keys()),
            "total_topics": len(self.knowledge_base),
            "avg_success_rate": statistics.mean([entry["success_rate"] for entry in self.knowledge_base.values()]) if self.knowledge_base else 0,
            "common_issues": sum(len(entry["common_issues"]) for entry in self.knowledge_base.values()),
            "best_practices": sum(len(entry["best_practices"]) for entry in self.knowledge_base.values())
        }

# Global self-improvement engine instance
_improvement_engine = SelfImprovementEngine({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "record_experience", "get_suggestions", "implement_improvement", 
                     "get_report", "get_insights", "analyze_performance"
            - experience_data: Experience data for recording
            - action_id: Improvement action ID
            - config: Configuration for the improvement engine
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_report")
    
    try:
        if action == "record_experience":
            exp_data = payload.get("experience_data", {})
            
            experience_id = _improvement_engine.record_experience(
                task_description=exp_data.get("task_description", ""),
                input_data=exp_data.get("input_data", {}),
                output_result=exp_data.get("output_result", {}),
                performance_metrics=exp_data.get("performance_metrics", {}),
                success=exp_data.get("success", False),
                feedback=exp_data.get("feedback", [])
            )
            
            return {
                "result": {
                    "experience_id": experience_id,
                    "message": f"Recorded experience: {experience_id}"
                },
                "metadata": {
                    "action": "record_experience",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_suggestions":
            limit = payload.get("limit", 5)
            suggestions = _improvement_engine.get_improvement_suggestions(limit)
            
            return {
                "result": suggestions,
                "metadata": {
                    "action": "get_suggestions",
                    "timestamp": datetime.now().isoformat(),
                    "limit": limit
                }
            }
        
        elif action == "implement_improvement":
            action_id = payload.get("action_id", "")
            success = _improvement_engine.implement_improvement(action_id)
            
            return {
                "result": {
                    "action_id": action_id,
                    "success": success,
                    "message": f"Implemented improvement: {action_id}" if success else f"Failed to implement improvement: {action_id}"
                },
                "metadata": {
                    "action": "implement_improvement",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_report":
            report = _improvement_engine.get_performance_report()
            
            return {
                "result": report,
                "metadata": {
                    "action": "get_report",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_insights":
            topic = payload.get("topic")
            insights = _improvement_engine.get_knowledge_insights(topic)
            
            return {
                "result": insights,
                "metadata": {
                    "action": "get_insights",
                    "timestamp": datetime.now().isoformat(),
                    "topic": topic
                }
            }
        
        elif action == "analyze_performance":
            # Analyze current performance and suggest improvements
            report = _improvement_engine.get_performance_report()
            suggestions = _improvement_engine.get_improvement_suggestions(3)
            
            return {
                "result": {
                    "performance_report": report,
                    "improvement_suggestions": suggestions,
                    "recommendations": self._generate_recommendations(report, suggestions)
                },
                "metadata": {
                    "action": "analyze_performance",
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
        logger.error(f"Error in self_improvement_engine: {e}")
        return {
            "result": {
                "error": str(e)
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def _generate_recommendations(self, report: Dict[str, Any], suggestions: List[Dict[str, Any]]) -> List[str]:
        """Generate improvement recommendations based on report and suggestions"""
        recommendations = []
        
        if report["success_trend"] < 0:
            recommendations.append("Success rate is declining. Focus on accuracy improvements.")
        
        if report["learning_rate"] < 0.1:
            recommendations.append("Learning rate is low. Increase feedback processing.")
        
        if report["pending_improvements"] > 10:
            recommendations.append("Too many pending improvements. Prioritize and implement.")
        
        for suggestion in suggestions[:3]:  # Top 3 suggestions
            recommendations.append(f"High priority: {suggestion['description']}")
        
        return recommendations

# Example usage function
async def example_usage():
    """Example of how to use the self-improvement engine skill"""
    
    # Record some experiences
    await invoke({
        "action": "record_experience",
        "experience_data": {
            "task_description": "Process user query",
            "input_data": {"query": "How to optimize code?"},
            "output_result": {"answer": "Use profiling tools"},
            "performance_metrics": {"execution_time": 2.5, "accuracy": 0.8},
            "success": True,
            "feedback": [{"type": "user", "content": "Good answer but could be more detailed"}]
        }
    })
    
    # Get improvement suggestions
    suggestions = await invoke({"action": "get_suggestions", "limit": 3})
    print(f"Improvement suggestions: {suggestions['result']}")
    
    # Get performance report
    report = await invoke({"action": "get_report"})
    print(f"Performance report: {report['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())