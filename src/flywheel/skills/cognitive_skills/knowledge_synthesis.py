"""
Knowledge Synthesis Module

Combine existing knowledge from multiple sources to form coherent
solutions and new insights.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class KnowledgeSource:
    """Represents a knowledge source."""

    name: str
    content: str
    relevance_score: float = 1.0


@dataclass
class KnowledgeInsight:
    """Represents a synthesized insight."""

    statement: str
    sources: List[str]
    confidence: float
    connections: List[str] = field(default_factory=list)


class KnowledgeSynthesizer:
    """
    Combines knowledge from multiple sources.

    Framework:
    1. Gather Knowledge
    2. Identify Connections
    3. Integrate
    4. Synthesize New Insight
    """

    def __init__(self):
        self.sources: List[KnowledgeSource] = []
        self.insights: List[KnowledgeInsight] = []

    def add_source(
        self, name: str, content: str, relevance: float = 1.0
    ) -> KnowledgeSource:
        """Add a knowledge source."""
        source = KnowledgeSource(name=name, content=content, relevance_score=relevance)
        self.sources.append(source)
        return source

    def identify_connections(self) -> Dict[str, List[str]]:
        """Identify connections between sources."""
        connections = {}
        keywords_per_source = {}

        for source in self.sources:
            keywords = self._extract_keywords(source.content)
            keywords_per_source[source.name] = keywords

        for name1, kw1 in keywords_per_source.items():
            for name2, kw2 in keywords_per_source.items():
                if name1 != name2:
                    common = kw1 & kw2
                    if common:
                        connections[f"{name1} <-> {name2}"] = list(common)

        return connections

    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text."""
        words = text.lower().split()
        # Simple keyword extraction - remove common words
        stopwords = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "shall",
            "can",
            "need",
            "dare",
            "to",
            "of",
            "in",
            "for",
            "on",
            "with",
            "at",
            "by",
            "from",
            "as",
            "into",
            "through",
            "during",
            "before",
            "after",
            "above",
            "below",
        }
        return {w for w in words if w not in stopwords and len(w) > 3}

    def resolve_conflicts(self, conflicting_sources: List[str]) -> Dict:
        """
        Resolve conflicts between sources.

        Args:
            conflicting_sources: List of source names with conflicting info

        Returns:
            Resolution recommendation
        """
        # Simplified conflict resolution - prefer peer-reviewed, then recent
        return {
            "conflict_sources": conflicting_sources,
            "resolution": "Consider weighting by source credibility and recency",
            "recommendation": "Further investigation needed",
        }

    def synthesize(self, target_question: str) -> Dict:
        """
        Synthesize knowledge to answer a question.

        Args:
            target_question: The question to answer

        Returns:
            Synthesized answer with supporting sources
        """
        if not self.sources:
            return {"error": "No sources added"}

        # Find relevant sources
        relevant = []
        for source in self.sources:
            keywords = self._extract_keywords(source.content)
            question_keywords = self._extract_keywords(target_question)
            overlap = keywords & question_keywords
            if overlap:
                relevant.append(
                    {
                        "source": source.name,
                        "overlap": list(overlap),
                        "relevance": len(overlap) / len(question_keywords),
                    }
                )

        # Generate insight
        insight = KnowledgeInsight(
            statement=f"Based on {len(relevant)} relevant sources, addressing: {target_question}",
            sources=[r["source"] for r in relevant],
            confidence=sum(r["relevance"] for r in relevant) / len(relevant)
            if relevant
            else 0,
            connections=self.identify_connections(),
        )
        self.insights.append(insight)

        return {
            "question": target_question,
            "relevant_sources": relevant,
            "connections": insight.connections,
            "confidence": insight.confidence,
            "synthesized_answer": insight.statement,
        }

    def build_knowledge_graph(self) -> Dict:
        """Build a simple knowledge graph."""
        connections = self.identify_connections()

        nodes = [{"id": s.name, "label": s.name} for s in self.sources]
        edges = []

        for connection, keywords in connections.items():
            parts = connection.split(" <-> ")
            if len(parts) == 2:
                edges.append({"from": parts[0], "to": parts[1], "keywords": keywords})

        return {"nodes": nodes, "edges": edges}


# Convenience function
def synthesize_knowledge(question: str, sources: List[Dict]) -> Dict:
    """Quick knowledge synthesis."""
    synthesizer = KnowledgeSynthesizer()
    for s in sources:
        synthesizer.add_source(s.get("name", "Unknown"), s.get("content", ""))
    return synthesizer.synthesize(question)


# --- invoke() wrapper added by batch fix ---
import asyncio as _asyncio
import inspect as _inspect

async def invoke(payload: dict) -> dict:
    """Entry point for skill invocation."""
    import datetime as _dt
    action = payload.get("action", "synthesize_knowledge")
    timestamp = _dt.datetime.now().isoformat()
    kwargs = {k: v for k, v in payload.items() if k != "action"}

    instance = KnowledgeSynthesizer()

    if action == "get_info":
        return {"result": {"name": "knowledge_synthesis", "actions": ['add_source', 'build_knowledge_graph', 'identify_connections', 'resolve_conflicts', 'synthesize', 'synthesize_knowledge'] }, "metadata": {"action": action, "timestamp": timestamp}}

    method = getattr(instance, action, None)
    if method is None:
        return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}

    result = method(**kwargs)
    if _inspect.isawaitable(result):
        result = await result
    return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}
