"""
Sequential Problem Solving Module

Move from problem statement to solution through logical, ordered steps
with verification at each stage.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class ProblemStatus(Enum):
    IDENTIFIED = "identified"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    VERIFIED = "verified"
    SOLVED = "solved"
    FAILED = "failed"


@dataclass
class ProblemStep:
    """Represents a single step in problem solving."""

    step_number: int
    description: str
    status: ProblemStatus = ProblemStatus.PLANNING
    result: str | None = None
    verified: bool = False
    notes: str | None = None


@dataclass
class Problem:
    """Represents a problem to be solved."""

    statement: str
    constraints: List[str] = field(default_factory=list)
    knowns: List[str] = field(default_factory=list)
    unknowns: List[str] = field(default_factory=list)
    steps: List[ProblemStep] = field(default_factory=list)


class SequentialProblemSolver:
    """
    Solves problems through sequential steps with verification.

    Framework:
    1. Understand the Problem
    2. Devise a Plan
    3. Execute the Plan
    4. Review the Solution
    """

    def __init__(self):
        self.current_problem: Problem | None = None

    def create_problem(self, statement: str, **kwargs) -> Problem:
        """Create a new problem definition."""
        problem = Problem(statement=statement, **kwargs)
        self.current_problem = problem
        return problem

    def add_step(self, description: str) -> ProblemStep:
        """Add a step to the current problem."""
        if not self.current_problem:
            raise ValueError("No current problem. Create one first.")

        step_number = len(self.current_problem.steps) + 1
        step = ProblemStep(step_number=step_number, description=description)
        self.current_problem.steps.append(step)
        return step

    def execute_step(self, step_number: int, result: str) -> bool:
        """Execute a step and record its result."""
        if not self.current_problem:
            return False

        for step in self.current_problem.steps:
            if step.step_number == step_number:
                step.result = result
                step.status = ProblemStatus.EXECUTING
                return True
        return False

    def verify_step(
        self, step_number: int, verified: bool = True, notes: str = ""
    ) -> bool:
        """Verify a step's result."""
        if not self.current_problem:
            return False

        for step in self.current_problem.steps:
            if step.step_number == step_number:
                step.verified = verified
                step.notes = notes
                step.status = (
                    ProblemStatus.VERIFIED if verified else ProblemStatus.FAILED
                )
                return True
        return False

    def solve_math(self, equation: str) -> Dict:
        """
        Solve a mathematical equation step by step.

        Args:
            equation: Mathematical equation to solve

        Returns:
            Dictionary with solution steps
        """
        steps = []

        # Simple linear equation solver
        if "=" in equation and "x" in equation:
            parts = equation.split("=")
            _left, _right = parts[0].strip(), parts[1].strip()

            # Step 1: Identify goal
            steps.append(
                {
                    "step": 1,
                    "action": "Identify goal",
                    "description": f"Isolate x in: {equation}",
                }
            )

            # Step 2: Move constant terms
            steps.append(
                {
                    "step": 2,
                    "action": "Rearrange equation",
                    "description": "Goal: get x alone on one side",
                }
            )

            # Simplified solving
            try:
                # For simple equations like "2x + 5 = 17"
                import re

                match = re.match(
                    r"(\d*)x\s*([+\-])\s*(\d+)\s*=\s*(\d+)", equation.replace(" ", "")
                )
                if match:
                    coef = int(match.group(1)) if match.group(1) else 1
                    op = match.group(2)
                    const = int(match.group(3))
                    result = int(match.group(4))

                    if op == "+":
                        solution = (result - const) / coef
                    else:
                        solution = (result + const) / coef

                    steps.append(
                        {"step": 3, "action": "Solve", "description": f"x = {solution}"}
                    )

                    steps.append(
                        {
                            "step": 4,
                            "action": "Verify",
                            "description": f"Substitute x={solution}: {equation.replace('x', str(solution))} = {eval(equation.replace('x', str(solution)).replace('x', '*' + str(solution)))} ✓",
                        }
                    )

                    return {
                        "problem": equation,
                        "solution": solution,
                        "steps": steps,
                        "verified": True,
                    }
            except:
                pass

            return {
                "problem": equation,
                "solution": "Unable to parse equation",
                "steps": steps,
                "verified": False,
            }

        return {"error": "Unsupported equation format"}

    def solve_algorithm(self, problem_desc: str) -> Dict:
        """
        Solve an algorithmic problem step by step.

        Args:
            problem_desc: Description of the algorithmic problem

        Returns:
            Dictionary with solution approach
        """
        steps = [
            {
                "step": 1,
                "action": "Understand",
                "description": f"Problem: {problem_desc}",
            },
            {
                "step": 2,
                "action": "Analyze input/output",
                "description": "Define inputs and expected outputs",
            },
            {
                "step": 3,
                "action": "Design algorithm",
                "description": "Choose appropriate algorithm pattern",
            },
            {
                "step": 4,
                "action": "Implement",
                "description": "Write pseudocode or code",
            },
            {"step": 5, "action": "Test", "description": "Verify with test cases"},
        ]

        return {"problem": problem_desc, "approach": "step-by-step", "steps": steps}

    def get_solution(self) -> Dict:
        """Get the current problem solution."""
        if not self.current_problem:
            return {"error": "No problem created"}

        all_verified = all(step.verified for step in self.current_problem.steps)

        return {
            "problem": self.current_problem.statement,
            "steps": [
                {
                    "number": s.step_number,
                    "description": s.description,
                    "result": s.result,
                    "verified": s.verified,
                }
                for s in self.current_problem.steps
            ],
            "solved": all_verified,
        }


# Convenience function
def solve_step_by_step(statement: str) -> Dict:
    """Quick sequential problem solving."""
    solver = SequentialProblemSolver()
    solver.create_problem(statement)
    return solver.get_solution()


# --- invoke() wrapper added by batch fix ---
import asyncio as _asyncio
import inspect as _inspect

async def invoke(payload: dict) -> dict:
    """Entry point for skill invocation."""
    import datetime as _dt
    action = payload.get("action", "solve_step_by_step")
    timestamp = _dt.datetime.now().isoformat()
    kwargs = {k: v for k, v in payload.items() if k != "action"}

    instance = SequentialProblemSolver()

    if action == "get_info":
        return {"result": {"name": "sequential_problem_solving", "actions": ['add_step', 'create_problem', 'execute_step', 'get_solution', 'solve_step_by_step', 'verify_step'] }, "metadata": {"action": action, "timestamp": timestamp}}

    method = getattr(instance, action, None)
    if method is None:
        return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}

    result = method(**kwargs)
    if _inspect.isawaitable(result):
        result = await result
    return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}
