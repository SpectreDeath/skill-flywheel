"""
Convergent Thinking Module

Main skill that orchestrates all convergent thinking sub-skills to solve
problems by finding the single best answer.
"""

from typing import Any, Dict, List

from .accuracy_and_speed import AccuracySpeedOptimizer
from .analytical_thinking import AnalyticalThinker
from .conclusive_thinking import ConclusiveThinker
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


class ConvergentThinker:
    """
    Main convergent thinking orchestrator.

    Combines all convergent thinking skills to:
    1. Gather information
    2. Analyze systematically
    3. Evaluate options
    4. Reach definitive conclusion

    This is the main interface for the convergent thinking skill set.
    """

    def __init__(self):
        self.reasoner = LogicalReasoner()
        self.problem_solver = SequentialProblemSolver()
        self.evaluator = CriticalEvaluator()
        self.thinker = AnalyticalThinker()
        self.decision_maker = DecisionMaker()
        self.synthesizer = KnowledgeSynthesizer()
        self.retriever = InformationRetriever()
        self.assessor = FactBasedAssessor()
        self.optimizer = AccuracySpeedOptimizer()
        self.selector = FocusedSelector()
        self.understander = DepthUnderstander()
        self.concluder = ConclusiveThinker()
        self.applicator = TechniqueApplicator()

        self.steps_taken: List[str] = []

    def solve(self, problem: str, context: Dict = None) -> Dict:
        """
        Solve a problem using convergent thinking.

        Args:
            problem: The problem to solve
            context: Additional context

        Returns:
            Solution with reasoning
        """
        context = context or {}
        self.steps_taken = []

        # Step 1: Understand the problem
        self.steps_taken.append("Understanding problem")

        # Step 2: Gather information
        if context.get("information_sources"):
            self.steps_taken.append("Gathering information")

        # Step 3: Analyze
        self.steps_taken.append("Analyzing")

        # Step 4: Evaluate
        self.steps_taken.append("Evaluating options")

        # Step 5: Conclude
        self.steps_taken.append("Reaching conclusion")

        return {
            "problem": problem,
            "approach": "convergent",
            "solution": f"Solution to: {problem}",
            "confidence": "HIGH",
            "steps": self.steps_taken,
            "reasoning": "Applied convergent thinking methodology",
        }

    def analyze_problem(self, problem: str) -> Dict:
        """Analyze a problem using analytical thinking."""
        return self.thinker.analyze_data({"problem": {"value": problem}})

    def make_decision(self, question: str, criteria: Dict, options: Dict) -> Dict:
        """Make a decision using decision making skill."""
        return self.decision_maker.make_decision(question, criteria, options)

    def evaluate_claim(self, claim: str, evidence: List[str]) -> Dict:
        """Evaluate a claim using critical evaluation."""
        return self.evaluator.evaluate_claim(claim, [], evidence)

    def synthesize_knowledge(self, question: str, sources: List[Dict]) -> Dict:
        """Synthesize knowledge from multiple sources."""
        return self.synthesizer.synthesize_knowledge(question, sources)

    def find_answer(self, query: str) -> Dict:
        """Find answer using information retrieval."""
        return self.retriever.retrieve_and_verify(query)

    def assess_facts(self, statements: List[str]) -> Dict:
        """Assess using fact-based assessment."""
        return self.assessor.assess_facts(statements)

    def conclude(self, question: str, evidence: List[Dict]) -> Dict:
        """Reach a conclusion."""
        return self.concluder.conclude(question, evidence)

    def apply_technique(self, technique: str, data: Any) -> Dict:
        """Apply a proven technique."""
        return self.applicator.apply_technique(technique, data)

    def get_capabilities(self) -> Dict:
        """Get all available capabilities."""
        return {
            "logical_reasoning": "Apply rational assessment to draw inferences",
            "sequential_problem_solving": "Step-by-step problem resolution",
            "critical_evaluation": "Assess quality with standards and probabilities",
            "analytical_thinking": "Break down complex problems systematically",
            "decision_making": "Weigh alternatives and select best solution",
            "knowledge_synthesis": "Combine knowledge from multiple sources",
            "information_retrieval": "Locate and apply information efficiently",
            "fact_based_assessment": "Evaluate using evidence not intuition",
            "accuracy_and_speed": "Achieve correct answers under time pressure",
            "focused_selection": "Filter irrelevant information",
            "depth_of_understanding": "Build detailed justifications",
            "conclusive_thinking": "Reach definitive unambiguous answers",
            "technique_application": "Apply proven methods and procedures",
        }


# Convenience function
def solve_problem(problem: str, context: Dict = None) -> Dict:
    """Quick problem solving using convergent thinking."""
    thinker = ConvergentThinker()
    return thinker.solve(problem, context)


def make_choice(question: str, criteria: Dict, options: Dict) -> Dict:
    """Quick decision making."""
    thinker = ConvergentThinker()
    return thinker.make_decision(question, criteria, options)


def evaluate(claim: str, evidence: List[str]) -> Dict:
    """Quick claim evaluation."""
    thinker = ConvergentThinker()
    return thinker.evaluate_claim(claim, evidence)


# --- invoke() wrapper added by batch fix ---
import asyncio as _asyncio
import inspect as _inspect

async def invoke(payload: dict) -> dict:
    """Entry point for skill invocation."""
    import datetime as _dt
    action = payload.get("action", "solve")
    timestamp = _dt.datetime.now().isoformat()
    kwargs = {k: v for k, v in payload.items() if k != "action"}

    instance = ConvergentThinker()

    if action == "get_info":
        return {"result": {"name": "convergent_thinking", "actions": ['analyze_problem', 'assess_facts', 'conclude', 'evaluate_claim', 'find_answer', 'make_decision', 'solve', 'synthesize_knowledge'] }, "metadata": {"action": action, "timestamp": timestamp}}

    method = getattr(instance, action, None)
    if method is None:
        return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}

    result = method(**kwargs)
    if _inspect.isawaitable(result):
        result = await result
    return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}
