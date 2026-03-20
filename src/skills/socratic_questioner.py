"""
Socratic Questioner

Applies Socratic questioning to explore concepts:
- Clarification questions
- Assumption probing
- Evidence examination
- Perspective exploration
- Implication analysis
- Meta-questioning
"""

from typing import Any, Dict, List

QUESTION_TYPES = {
    "clarification": [
        "What do you mean by {concept}?",
        "Can you give me an example?",
        "How does this relate to what we discussed?",
        "What specifically do you mean?",
        "Could you define {concept} more precisely?",
    ],
    "assumptions": [
        "What are you assuming here?",
        "What could we assume instead?",
        "What prevents us from assuming otherwise?",
        "Is there an alternative framework?",
        "What would need to be true for this to work?",
    ],
    "evidence": [
        "What evidence supports this?",
        "What would change your mind?",
        "How do you know this is true?",
        "What sources support your view?",
        "Could the evidence be interpreted differently?",
    ],
    "perspectives": [
        "How would others see this?",
        "What would a critic say?",
        "How does this look from another angle?",
        "What alternative viewpoints exist?",
        "Who might disagree with this?",
    ],
    "implications": [
        "What follows from this?",
        "Where does this lead?",
        "What are the consequences?",
        "If true, what else must be true?",
        "What are the broader implications?",
    ],
    "meta": [
        "Why is this question important?",
        "What are we really asking here?",
        "How does this connect to our goal?",
        "What kind of question is this?",
        "Are we asking the right question?",
    ],
}


def analyze_concept(concept: str) -> Dict[str, Any]:
    """Analyze a concept for questioning paths"""

    # Identify potential question targets
    nouns = concept.split()
    key_terms = [w for w in nouns if len(w) > 3][:3]

    return {
        "key_terms": key_terms,
        "concept_length": len(concept),
        "has_definition": "is" in concept.lower() or "means" in concept.lower(),
    }


def generate_questions(concept: str, depth: int = 2) -> Dict[str, Any]:
    """Generate Socratic questions for a concept"""

    analysis = analyze_concept(concept)
    questions = {}

    # Generate questions for each type
    for q_type, templates in QUESTION_TYPES.items():
        type_questions = []
        for template in templates:
            # Replace {concept} placeholder
            if "{concept}" in template:
                for term in analysis["key_terms"]:
                    type_questions.append(template.format(concept=term))
            else:
                type_questions.append(template)

        questions[q_type] = type_questions[:3]  # Top 3 per type

    # Create a questioning sequence
    sequence = []
    for i in range(depth):
        for q_type in QUESTION_TYPES:
            if questions[q_type]:
                q = questions[q_type][i % len(questions[q_type])]
                sequence.append(
                    {"type": q_type, "question": q, "step": len(sequence) + 1}
                )

    return {
        "status": "success",
        "concept": concept,
        "analysis": analysis,
        "questions_by_type": questions,
        "questioning_sequence": sequence,
        "total_questions": len(sequence),
    }


def socratic_questioner(
    concept: str, depth: int = 2, focus: List[str] | None = None, **kwargs
) -> Dict[str, Any]:
    """
    Apply Socratic questioning to explore a concept.

    Args:
        concept: The concept or question to explore
        depth: How many rounds of questioning
        focus: Specific question types to focus on
        **kwargs: Additional parameters

    Returns:
        Socratic questioning exploration
    """
    if not concept:
        return {"status": "error", "error": "No concept provided"}

    result = generate_questions(concept, depth)

    # Filter by focus if specified
    if focus:
        filtered_sequence = [
            q for q in result["questioning_sequence"] if q["type"] in focus
        ]
        result["questioning_sequence"] = filtered_sequence
        result["total_questions"] = len(filtered_sequence)

    return result


def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "question")
    concept = payload.get("concept", "")
    depth = payload.get("depth", 2)
    focus = payload.get("focus")

    if action == "question":
        result = socratic_questioner(concept, depth, focus)
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return {"result": result}


def register_skill():
    """Return skill metadata"""
    return {
        "name": "socratic-questioner",
        "description": "Apply Socratic questioning to explore concepts deeply",
        "version": "1.0.0",
        "domain": "PHILOSOPHY",
    }
