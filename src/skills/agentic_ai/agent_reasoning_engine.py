#!/usr/bin/env python3
"""
Skill: agent-reasoning-engine
Domain: agentic_ai
Description: Advanced reasoning engine for AI agents using chain-of-thought and logical inference
"""

import asyncio
import logging
import time
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class ReasoningType(Enum):
    """Types of reasoning"""
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    ANALOGICAL = "analogical"
    CAUSAL = "causal"

class ConfidenceLevel(Enum):
    """Confidence levels for reasoning results"""
    VERY_LOW = "very_low"    # 0-20%
    LOW = "low"             # 21-40%
    MEDIUM = "medium"       # 41-60%
    HIGH = "high"           # 61-80%
    VERY_HIGH = "very_high" # 81-100%

@dataclass
class ReasoningStep:
    """Represents a single step in the reasoning process"""
    step_number: int
    description: str
    reasoning_type: ReasoningType
    premises: List[str]
    conclusion: str
    confidence: float
    timestamp: float

@dataclass
class ReasoningResult:
    """Result of the reasoning process"""
    final_conclusion: str
    reasoning_chain: List[ReasoningStep]
    overall_confidence: float
    reasoning_type: ReasoningType
    execution_time: float
    metadata: Dict[str, Any]

class AgentReasoningEngine:
    """Advanced reasoning engine for AI agents"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the reasoning engine
        
        Args:
            config: Configuration dictionary with:
                - max_chain_length: Maximum number of reasoning steps
                - confidence_threshold: Minimum confidence for valid conclusions
                - enable_self_reflection: Whether to enable self-reflection
        """
        self.max_chain_length = config.get("max_chain_length", 10)
        self.confidence_threshold = config.get("confidence_threshold", 0.5)
        self.enable_self_reflection = config.get("enable_self_reflection", True)
        self.logger = logging.getLogger(__name__)
        
    async def reason(self, 
                    problem: str, 
                    context: Optional[Dict[str, Any]] = None,
                    reasoning_type: ReasoningType = ReasoningType.DEDUCTIVE) -> ReasoningResult:
        """
        Perform reasoning on a given problem
        
        Args:
            problem: The problem to reason about
            context: Additional context for reasoning
            reasoning_type: Type of reasoning to apply
            
        Returns:
            ReasoningResult with conclusion and reasoning chain
        """
        start_time = time.time()
        reasoning_chain: List[ReasoningStep] = []
        
        try:
            # Step 1: Problem analysis
            analysis_step = await self._analyze_problem(problem, reasoning_type)
            reasoning_chain.append(analysis_step)
            
            # Step 2: Generate premises
            premises_step = await self._generate_premises(problem, context, reasoning_type)
            reasoning_chain.append(premises_step)
            
            # Step 3: Apply reasoning logic
            conclusion_step = await self._apply_reasoning_logic(
                problem, premises_step.premises, reasoning_type
            )
            reasoning_chain.append(conclusion_step)
            
            # Step 4: Self-reflection (if enabled)
            if self.enable_self_reflection:
                reflection_step = await self._self_reflection(
                    reasoning_chain, reasoning_type
                )
                reasoning_chain.append(reflection_step)
            
            # Calculate overall confidence
            overall_confidence = self._calculate_overall_confidence(reasoning_chain)
            
            execution_time = time.time() - start_time
            
            result = ReasoningResult(
                final_conclusion=conclusion_step.conclusion,
                reasoning_chain=reasoning_chain,
                overall_confidence=overall_confidence,
                reasoning_type=reasoning_type,
                execution_time=execution_time,
                metadata={
                    "problem": problem,
                    "context_provided": context is not None,
                    "chain_length": len(reasoning_chain)
                }
            )
            
            self.logger.info(f"Reasoning completed: {result.final_conclusion[:100]}...")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in reasoning: {e}")
            return self._create_error_result(problem, str(e), start_time)
    
    async def _analyze_problem(self, problem: str, reasoning_type: ReasoningType) -> ReasoningStep:
        """Analyze the problem to understand its structure"""
        description = f"Analyzing problem for {reasoning_type.value} reasoning"
        
        # Simulate problem analysis
        await asyncio.sleep(0.1)
        
        # Generate analysis conclusion
        analysis_conclusion = f"Problem identified as suitable for {reasoning_type.value} reasoning"
        
        return ReasoningStep(
            step_number=1,
            description=description,
            reasoning_type=reasoning_type,
            premises=[f"Problem: {problem}"],
            conclusion=analysis_conclusion,
            confidence=0.8,
            timestamp=time.time()
        )
    
    async def _generate_premises(self, 
                               problem: str, 
                               context: Optional[Dict[str, Any]],
                               reasoning_type: ReasoningType) -> ReasoningStep:
        """Generate premises for reasoning"""
        description = f"Generating premises for {reasoning_type.value} reasoning"
        
        # Simulate premise generation
        await asyncio.sleep(0.2)
        
        # Generate premises based on reasoning type
        base_premises = [
            f"Given: {problem}",
            f"Reasoning type: {reasoning_type.value}"
        ]
        
        if context:
            for key, value in context.items():
                base_premises.append(f"Context {key}: {value}")
        
        # Add reasoning-type specific premises
        if reasoning_type == ReasoningType.DEDUCTIVE:
            base_premises.append("If A implies B, and A is true, then B is true")
        elif reasoning_type == ReasoningType.INDUCTIVE:
            base_premises.append("Patterns observed in specific cases can suggest general rules")
        elif reasoning_type == ReasoningType.ABDUCTIVE:
            base_premises.append("Best explanation is the most likely cause")
        elif reasoning_type == ReasoningType.ANALOGICAL:
            base_premises.append("Similar cases suggest similar solutions")
        elif reasoning_type == ReasoningType.CAUSAL:
            base_premises.append("Cause precedes effect")
        
        conclusion = f"Generated {len(base_premises)} premises for reasoning"
        
        return ReasoningStep(
            step_number=2,
            description=description,
            reasoning_type=reasoning_type,
            premises=base_premises,
            conclusion=conclusion,
            confidence=0.75,
            timestamp=time.time()
        )
    
    async def _apply_reasoning_logic(self, 
                                   problem: str,
                                   premises: List[str], 
                                   reasoning_type: ReasoningType) -> ReasoningStep:
        """Apply specific reasoning logic based on type"""
        description = f"Applying {reasoning_type.value} reasoning logic"
        
        # Simulate reasoning computation
        await asyncio.sleep(0.3)
        
        # Generate conclusion based on reasoning type
        if reasoning_type == ReasoningType.DEDUCTIVE:
            conclusion = self._deductive_reasoning(problem, premises)
        elif reasoning_type == ReasoningType.INDUCTIVE:
            conclusion = self._inductive_reasoning(problem, premises)
        elif reasoning_type == ReasoningType.ABDUCTIVE:
            conclusion = self._abductive_reasoning(problem, premises)
        elif reasoning_type == ReasoningType.ANALOGICAL:
            conclusion = self._analogical_reasoning(problem, premises)
        elif reasoning_type == ReasoningType.CAUSAL:
            conclusion = self._causal_reasoning(problem, premises)
        else:
            conclusion = "Unable to apply reasoning logic"
        
        confidence = self._calculate_step_confidence(reasoning_type, len(premises))
        
        return ReasoningStep(
            step_number=3,
            description=description,
            reasoning_type=reasoning_type,
            premises=premises,
            conclusion=conclusion,
            confidence=confidence,
            timestamp=time.time()
        )
    
    async def _self_reflection(self, 
                             reasoning_chain: List[ReasoningStep],
                             reasoning_type: ReasoningType) -> ReasoningStep:
        """Perform self-reflection on the reasoning process"""
        description = "Performing self-reflection on reasoning process"
        
        # Simulate reflection
        await asyncio.sleep(0.2)
        
        # Analyze reasoning quality
        total_confidence = sum(step.confidence for step in reasoning_chain)
        avg_confidence = total_confidence / len(reasoning_chain)
        
        reflection_points = []
        if avg_confidence < 0.5:
            reflection_points.append("Low confidence detected - consider additional evidence")
        if len(reasoning_chain) > self.max_chain_length:
            reflection_points.append("Reasoning chain too long - may indicate overcomplication")
        
        conclusion = f"Self-reflection completed. Average confidence: {avg_confidence:.2f}"
        if reflection_points:
            conclusion += f" Issues: {', '.join(reflection_points)}"
        
        return ReasoningStep(
            step_number=4,
            description=description,
            reasoning_type=reasoning_type,
            premises=[f"Reasoning chain length: {len(reasoning_chain)}"],
            conclusion=conclusion,
            confidence=avg_confidence,
            timestamp=time.time()
        )
    
    def _deductive_reasoning(self, problem: str, premises: List[str]) -> str:
        """Apply deductive reasoning logic"""
        return f"Deductive conclusion: Based on premises, {problem} must be true if premises are valid"
    
    def _inductive_reasoning(self, problem: str, premises: List[str]) -> str:
        """Apply inductive reasoning logic"""
        return f"Inductive conclusion: Based on observed patterns, {problem} is likely true"
    
    def _abductive_reasoning(self, problem: str, premises: List[str]) -> str:
        """Apply abductive reasoning logic"""
        return f"Abductive conclusion: Best explanation for {problem} is the most plausible cause"
    
    def _analogical_reasoning(self, problem: str, premises: List[str]) -> str:
        """Apply analogical reasoning logic"""
        return f"Analogical conclusion: Similar to known cases, {problem} suggests similar solution"
    
    def _causal_reasoning(self, problem: str, premises: List[str]) -> str:
        """Apply causal reasoning logic"""
        return f"Causal conclusion: {problem} is caused by factors identified in premises"
    
    def _calculate_step_confidence(self, reasoning_type: ReasoningType, premise_count: int) -> float:
        """Calculate confidence for a reasoning step"""
        base_confidence = 0.6
        
        # Adjust based on reasoning type
        if reasoning_type == ReasoningType.DEDUCTIVE:
            confidence_modifier = 0.2
        elif reasoning_type == ReasoningType.INDUCTIVE:
            confidence_modifier = 0.1
        elif reasoning_type == ReasoningType.ABDUCTIVE:
            confidence_modifier = 0.05
        else:
            confidence_modifier = 0.1
        
        # Adjust based on premise count
        premise_modifier = min(premise_count * 0.05, 0.3)
        
        confidence = base_confidence + confidence_modifier + premise_modifier
        return min(confidence, 1.0)
    
    def _calculate_overall_confidence(self, reasoning_chain: List[ReasoningStep]) -> float:
        """Calculate overall confidence from reasoning chain"""
        if not reasoning_chain:
            return 0.0
        
        # Weighted average with more recent steps having higher weight
        total_weight = 0
        weighted_confidence = 0
        
        for i, step in enumerate(reasoning_chain):
            weight = i + 1  # Linear weighting
            total_weight += weight
            weighted_confidence += step.confidence * weight
        
        return weighted_confidence / total_weight if total_weight > 0 else 0.0
    
    def _create_error_result(self, problem: str, error: str, start_time: float) -> ReasoningResult:
        """Create an error result"""
        return ReasoningResult(
            final_conclusion=f"Error in reasoning: {error}",
            reasoning_chain=[],
            overall_confidence=0.0,
            reasoning_type=ReasoningType.DEDUCTIVE,  # Default
            execution_time=time.time() - start_time,
            metadata={
                "problem": problem,
                "error": error,
                "chain_length": 0
            }
        )

# Global reasoning engine instance
_reasoning_engine = AgentReasoningEngine({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "reason", "analyze", "validate"
            - problem: The problem to reason about
            - context: Additional context (optional)
            - reasoning_type: Type of reasoning to apply (optional)
            - config: Configuration for the reasoning engine (optional)
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "reason")
    
    try:
        if action == "reason":
            problem = payload.get("problem", "")
            context = payload.get("context")
            reasoning_type_str = payload.get("reasoning_type", "deductive")
            
            # Convert string to enum
            try:
                reasoning_type = ReasoningType(reasoning_type_str.lower())
            except ValueError:
                reasoning_type = ReasoningType.DEDUCTIVE
            
            # Update engine config if provided
            config = payload.get("config", {})
            if config:
                _reasoning_engine.max_chain_length = config.get("max_chain_length", _reasoning_engine.max_chain_length)
                _reasoning_engine.confidence_threshold = config.get("confidence_threshold", _reasoning_engine.confidence_threshold)
                _reasoning_engine.enable_self_reflection = config.get("enable_self_reflection", _reasoning_engine.enable_self_reflection)
            
            result = await _reasoning_engine.reason(problem, context, reasoning_type)
            
            return {
                "result": {
                    "final_conclusion": result.final_conclusion,
                    "reasoning_chain": [asdict(step) for step in result.reasoning_chain],
                    "overall_confidence": result.overall_confidence,
                    "reasoning_type": result.reasoning_type.value,
                    "execution_time": result.execution_time,
                    "metadata": result.metadata
                },
                "metadata": {
                    "action": "reason",
                    "timestamp": datetime.now().isoformat(),
                    "problem_length": len(problem)
                }
            }
        
        elif action == "analyze":
            problem = payload.get("problem", "")
            context = payload.get("context")
            
            # Perform quick analysis without full reasoning
            analysis = {
                "problem_length": len(problem),
                "context_provided": context is not None,
                "estimated_complexity": "medium" if len(problem) > 100 else "simple",
                "suggested_reasoning_type": "deductive" if "?" in problem else "inductive"
            }
            
            return {
                "result": analysis,
                "metadata": {
                    "action": "analyze",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "validate":
            reasoning_result = payload.get("reasoning_result", {})
            
            # Validate reasoning result structure
            required_fields = ["final_conclusion", "reasoning_chain", "overall_confidence"]
            missing_fields = [field for field in required_fields if field not in reasoning_result]
            
            validation_result = {
                "valid": len(missing_fields) == 0,
                "missing_fields": missing_fields,
                "confidence_valid": 0.0 <= reasoning_result.get("overall_confidence", 0.0) <= 1.0,
                "chain_length": len(reasoning_result.get("reasoning_chain", []))
            }
            
            return {
                "result": validation_result,
                "metadata": {
                    "action": "validate",
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
        logger.error(f"Error in agent_reasoning_engine: {e}")
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
    """Example of how to use the agent reasoning engine skill"""
    
    # Example 1: Deductive reasoning
    result1 = await invoke({
        "action": "reason",
        "problem": "All humans are mortal. Socrates is a human. Is Socrates mortal?",
        "reasoning_type": "deductive"
    })
    
    print(f"Deductive reasoning result: {result1['result']['final_conclusion']}")
    
    # Example 2: Inductive reasoning
    result2 = await invoke({
        "action": "reason",
        "problem": "Every swan I've seen is white. Are all swans white?",
        "reasoning_type": "inductive"
    })
    
    print(f"Inductive reasoning result: {result2['result']['final_conclusion']}")
    
    # Example 3: Problem analysis
    result3 = await invoke({
        "action": "analyze",
        "problem": "How can we improve user engagement on our platform?"
    })
    
    print(f"Analysis result: {result3['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())