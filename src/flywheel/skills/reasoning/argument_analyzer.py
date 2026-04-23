"""
Argument Analysis and Fallacy Detection

Analyzes philosophical arguments for:
- Logical validity and soundness
- Common logical fallacies
- Argument structure and components
"""

import re
from typing import Any, Dict, List
from datetime import datetime

FALLACIES = {
    "ad_hominem": {
        "pattern": r"(?:attack|insult|criticize|dismiss)\s+(?:the\s+)?(person|character|personality|motivation)",
        "description": "Attacking the person rather than the argument",
        "severity": "high",
    },
    "straw_man": {
        "pattern": r"(?:misrepresent|distort|exaggerate|oversimplify)\s+(?:the\s+)?(position|argument|claim)",
        "description": "Misrepresenting an argument to make it easier to attack",
        "severity": "high",
    },
    "appeal_to_authority": {
        "pattern": r"(?:according\s+to|as\s+said\s+by|expert|says\s+)(?:the\s+)?(?:famous|well-known|respected)\s+\w+",
        "description": "Using authority as evidence without proper justification",
        "severity": "medium",
    },
    "false_dilemma": {
        "pattern": r"(?:either|only\s+two|there\s+are\s+two|must\s+be|has\s+to\s+be)",
        "description": "Presenting only two options when more exist",
        "severity": "medium",
    },
    "circular_reasoning": {
        "pattern": r"(.+)\s+because\s+\1",
        "description": "Using the conclusion as a premise",
        "severity": "high",
    },
    "slippery_slope": {
        "pattern": r"(?:if\s+.+\s+then\s+(?:inevitably|certainly|will\s+lead\s+to|will\s+result\s+in))",
        "description": "Assuming a chain of events without evidence",
        "severity": "medium",
    },
    "hasty_generalization": {
        "pattern": r"(?:all\s+|every\s+|always\s+|never\s+).{0,20}(?:prove|demonstrate|show|evidence)",
        "description": "Making broad conclusions from limited evidence",
        "severity": "medium",
    },
}


def analyze_argument_structure(argument: str) -> Dict[str, Any]:
    "Analyze the structure of an argument"
    # Extract premises and conclusion
    indicators = {
        "premises": ["because", "since", "given that", "as", "for", "assuming"],
        "conclusion": ["therefore", "thus", "hence", "so", "consequently", "therefore"],
    }

    sentences = re.split(r"[.!?]", argument)
    sentences = [s.strip() for s in sentences if s.strip()]

    premises = []
    conclusion = "

    for i, sentence in enumerate(sentences):
        sentence_lower = sentence.lower()
        if any(ind in sentence_lower for ind in indicators["conclusion"]):
            conclusion = sentence
        elif any(ind in sentence_lower for ind in indicators["premises"]):
            premises.append(sentence)
        elif i == len(sentences) - 1:
            conclusion = sentence  # Last sentence is likely conclusion

    return {
        "total_statements": len(sentences),
        "premises": premises,
        "conclusion": conclusion,
        "premise_count": len(premises),
    }


def detect_fallacies(argument: str) -> List[Dict[str, Any]]:
    "Detect logical fallacies in argument"
    found_fallacies = []
    argument_lower = argument.lower()

    for fallacy_name, info in FALLACIES.items():
        pattern = info["pattern"]
        matches = re.finditer(pattern, argument_lower)

        for match in matches:
            found_fallacies.append(
                {
                    "type": fallacy_name,
                    "description": info["description"],
                    "severity": info["severity"],
                    "match": match.group(),
                    "position": match.start(),
                }
            )

    return found_fallacies


def evaluate_argument_strength(argument: str) -> Dict[str, Any]:
    "
    Evaluate the strength of a philosophical argument.

    Args:
        argument: The argument text to analyze

    Returns:
        Analysis results with validity and fallacies
    "
    structure = analyze_argument_structure(argument)
    fallacies = detect_fallacies(argument)

    # Calculate strength score
    base_score = 100

    # Deduct for fallacies
    severity_scores = {"critical": 30, "high": 20, "medium": 10, "low": 5}
    fallacy_penalty = sum(severity_scores.get(f["severity"], 10) for f in fallacies)

    # Deduct for weak structure
    if structure["premise_count"] == 0:
        penalty = 30
    elif structure["premise_count"] < 2:
        penalty = 15
    else:
        penalty = 0

    if not structure["conclusion"]:
        penalty += 25

    score = max(0, base_score - fallacy_penalty - penalty)

    # Determine validity
    is_valid = (
        score >= 70 and len([f for f in fallacies if f["severity"] == "high"]) == 0
    )

    return {
        "status": "success",
        "argument": argument[:200] + "..." if len(argument) > 200 else argument,
        "structure": structure,
        "fallacies": fallacies,
        "fallacy_count": len(fallacies),
        "score": score,
        "is_valid": is_valid,
        "assessment": "Strong"
        if score >= 80
        else "Moderate"
        if score >= 60
        else "Weak",
    }


def argument_analyzer(argument: str, **kwargs) -> Dict[str, Any]:
    "
    Main entry point for argument analysis.

    Args:
        argument: The argument text to analyze
        **kwargs: Additional parameters

    Returns:
        Analysis results
    "
    if not argument:
        return {"status": "error", "error": "No argument provided"}

    return evaluate_argument_strength(argument)


async def invoke(payload: dict) -> dict:
    "MCP skill invocation"
    action = payload.get("action", "analyze")
    argument = payload.get("argument", ")

    if action == "analyze":
        result = argument_analyzer(argument)
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return{
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
def register_skill():
    """ Return skill metadata """

if __name__ == "__main__":
    return {
            "name": "argument-analyzer",
            "description": "Evaluate philosophical arguments and detect logical fallacies",
            "version": "1.0.0",
            "domain": "EPISTEMOLOGY",
        }