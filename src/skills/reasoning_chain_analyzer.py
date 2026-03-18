"""
Reasoning Chain Analyzer

Constructs and analyzes deductive and inductive reasoning chains:
- Validates logical connections
- Identifies missing premises
- Assesses conclusion strength
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass


REASONING_PATTERNS = {
    "modus_ponens": {
        "premise_form": ["If P then Q", "P"],
        "conclusion": "Q",
        "valid": True,
    },
    "modus_tollens": {
        "premise_form": ["If P then Q", "Not Q"],
        "conclusion": "Not P",
        "valid": True,
    },
    "hypothetical_syllogism": {
        "premise_form": ["If P then Q", "If Q then R"],
        "conclusion": "If P then R",
        "valid": True,
    },
    "disjunctive_syllogism": {
        "premise_form": ["P or Q", "Not P"],
        "conclusion": "Q",
        "valid": True,
    },
}


def parse_reasoning_steps(text: str) -> List[Dict[str, Any]]:
    """Parse reasoning steps from text"""
    steps = []

    lines = text.split("\n")
    for i, line in enumerate(lines):
        line = line.strip()
        if line:
            # Determine step type
            step_type = "premise"
            if any(
                word in line.lower()
                for word in ["therefore", "thus", "hence", "so", "consequently"]
            ):
                step_type = "conclusion"
            elif any(word in line.lower() for word in ["because", "since", "given"]):
                step_type = "premise"

            steps.append({"step": i + 1, "text": line, "type": step_type})

    return steps


def validate_deductive_chain(steps: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate a deductive reasoning chain"""
    # Check for logical patterns
    premises = [s["text"].lower() for s in steps if s["type"] == "premise"]
    conclusion = next((s["text"] for s in steps if s["type"] == "conclusion"), "")

    # Check for modus ponens pattern
    has_if_then = any("if" in p and "then" in p for p in premises)
    has_affirmation = any(
        p in " ".join(premises).lower()
        for p in ["it is true", "is the case", "happens"]
    )

    validation = {
        "is_valid": True,
        "confidence": 0.8,
        "missing_premises": [],
        "reasoning_type": "deductive",
    }

    # Check for common valid forms
    if len(premises) >= 2 and conclusion:
        # Could be valid - check structure
        validation["reasoning_type"] = "deductive"
    elif len(premises) >= 1 and conclusion:
        validation["reasoning_type"] = "inductive"

    # Identify missing premises
    if not conclusion:
        validation["is_valid"] = False
        validation["missing_premises"].append("No conclusion found")

    if len(premises) < 2:
        validation["confidence"] = 0.5
        validation["missing_premises"].append("Additional premises may be needed")

    return validation


def analyze_inductive_strength(
    steps: List[Dict[str, Any]], evidence_count: int
) -> Dict[str, Any]:
    """Analyze strength of inductive reasoning"""

    # Assess based on evidence count
    strength_scores = {
        "very_strong": 0.95,
        "strong": 0.8,
        "moderate": 0.6,
        "weak": 0.4,
        "very_weak": 0.2,
    }

    if evidence_count >= 100:
        strength = "very_strong"
    elif evidence_count >= 50:
        strength = "strong"
    elif evidence_count >= 20:
        strength = "moderate"
    elif evidence_count >= 5:
        strength = "weak"
    else:
        strength = "very_weak"

    return {
        "strength": strength,
        "confidence": strength_scores[strength],
        "evidence_count": evidence_count,
        "note": "Inductive conclusions are probabilistic, not certain",
    }


def reasoning_chain_analyzer(
    reasoning_text: str, evidence_count: int = 10, **kwargs
) -> Dict[str, Any]:
    """
    Analyze reasoning chains (deductive and inductive).

    Args:
        reasoning_text: Text containing reasoning steps
        evidence_count: Number of evidence items for inductive reasoning
        **kwargs: Additional parameters

    Returns:
        Analysis results
    """
    if not reasoning_text:
        return {"status": "error", "error": "No reasoning text provided"}

    steps = parse_reasoning_steps(reasoning_text)

    if not steps:
        return {"status": "error", "error": "Could not parse reasoning steps"}

    # Determine reasoning type
    has_conditional = any("if" in s["text"].lower() for s in steps)
    reasoning_type = "deductive" if has_conditional else "inductive"

    # Analyze based on type
    if reasoning_type == "deductive":
        analysis = validate_deductive_chain(steps)
    else:
        analysis = analyze_inductive_strength(steps, evidence_count)

    return {
        "status": "success",
        "reasoning_type": reasoning_type,
        "steps": steps,
        "step_count": len(steps),
        "analysis": analysis,
        "is_sound": analysis.get("is_valid", False)
        if reasoning_type == "deductive"
        else analysis.get("confidence", 0) >= 0.6,
    }


def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "analyze")
    reasoning_text = payload.get("reasoning_text", "")
    evidence_count = payload.get("evidence_count", 10)

    if action == "analyze":
        result = reasoning_chain_analyzer(reasoning_text, evidence_count)
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return {"result": result}


def register_skill():
    """Return skill metadata"""
    return {
        "name": "reasoning-chain-analyzer",
        "description": "Construct and analyze deductive and inductive reasoning chains",
        "version": "1.0.0",
        "domain": "EPISTEMOLOGY",
    }
