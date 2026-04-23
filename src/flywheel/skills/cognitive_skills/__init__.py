"""
Cognitive Skills Package

This package provides implementations of convergent thinking skills derived from
Vertical thinking (Edward de Bono) and Convergent thinking (Joy Paul Guilford).

Skills include:
- Logical Reasoning
- Sequential Problem Solving
- Critical Evaluation
- Analytical Thinking
- Decision Making
- Knowledge Synthesis
- Information Retrieval
- Fact-Based Assessment
- Accuracy and Speed
- Focused Selection
- Depth of Understanding
- Conclusive Thinking
- Technique Application
"""

from .accuracy_and_speed import AccuracySpeedOptimizer
from .analytical_thinking import AnalyticalThinker
from .conclusive_thinking import ConclusiveThinker
from .convergent_thinking import ConvergentThinker
from .critical_evaluation import CriticalEvaluator
from .decision_making import DecisionMaker
from .depth_of_understanding import DepthUnderstander
from .fact_based_assessment import FactBasedAssessor
from .focused_selection import FocusedSelector
from .information_retrieval import InformationRetriever
from .knowledge_synthesis import KnowledgeSynthesizer
from .logical_reasoning import LogicalReasoner
from .sequential_problem_solving import SequentialProblemSolver
from .technique_application import TechniqueApplicator

__all__ = [
    "LogicalReasoner",
    "SequentialProblemSolver",
    "CriticalEvaluator",
    "AnalyticalThinker",
    "DecisionMaker",
    "KnowledgeSynthesizer",
    "InformationRetriever",
    "FactBasedAssessor",
    "AccuracySpeedOptimizer",
    "FocusedSelector",
    "DepthUnderstander",
    "ConclusiveThinker",
    "TechniqueApplicator",
    "ConvergentThinker",
]
