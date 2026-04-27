#!/usr/bin/env python3
"""
Knowledge Graph Skill with Datalog Surface

Uses Datalog for efficient relational querying of knowledge relationships.
Demonstrates the power of declarative relational reasoning for fact retrieval
and inference over graph-structured knowledge.

This skill shows how Datalog excels at:
- Complex relationship queries
- Transitive relationship inference
- Pattern matching over relational data
- Declarative knowledge representation
"""

import os
from pathlib import Path
from typing import List, Dict, Any

# Surface definitions
_base_path = Path(__file__).parent
DATALOG_SURFACE = (_base_path / "knowledge_graph.dl").read_text()


def knowledge_graph(query_type: str, **params) -> Dict[str, Any]:
    """
    Query the knowledge graph using Datalog reasoning.

    Args:
        query_type: Type of query ('collaborators', 'tech_stack', 'networks')
        **params: Query parameters

    Returns:
        Dictionary with query results
    """
    try:
        from pyDatalog import pyDatalog
    except ImportError:
        return {"error": "pyDatalog not available", "results": []}

    # Initialize Datalog environment
    pyDatalog.clear()  # Clear any previous facts/rules

    # Load the Datalog surface
    try:
        pyDatalog.load(DATALOG_SURFACE)
    except Exception as e:
        return {"error": f"Failed to load Datalog surface: {e}", "results": []}

    results = []

    if query_type == "collaborators":
        # Find all collaborators for a person
        person = params.get("person", "alice")

        # Query for direct collaborators
        collaborators = []
        for result in pyDatalog.ask(f"collaborates_with('{person}', Y)"):
            if result and len(result) > 0:
                collaborators.append(result[0])

        results = collaborators

    elif query_type == "tech_stack":
        # Find technology stack for an organization
        org = params.get("organization", "google")

        # Query for technologies used by organization
        tech_stack = []
        for result in pyDatalog.ask(f"org_uses('{org}', Tech)"):
            if result and len(result) > 0:
                tech_stack.append(result[0])

        results = list(set(tech_stack))  # Remove duplicates

    elif query_type == "networks":
        # Find collaboration networks around shared technologies
        networks = []
        for result in pyDatalog.ask("collaboration_network(Person1, Person2, Tech)"):
            if result and len(result) >= 3:
                networks.append({
                    "person1": result[0],
                    "person2": result[1],
                    "shared_technology": result[2]
                })

        results = networks

    elif query_type == "entity_types":
        # Get all entity types
        types = []
        for result in pyDatalog.ask("entity_type(Entity, Type)"):
            if result and len(result) >= 2:
                types.append({
                    "entity": result[0],
                    "type": result[1]
                })

        results = types

    else:
        return {"error": f"Unknown query type: {query_type}", "results": []}

    return {
        "query_type": query_type,
        "params": params,
        "results": results,
        "count": len(results)
    }


def register_skill():
    """Register this skill with metadata"""
    return {
        "name": "knowledge_graph",
        "description": "Relational knowledge graph querying using Datalog",
        "version": "1.0.0",
        "domain": "HIGH_REASONING",
        "surfaces": ["datalog"],
        "capabilities": [
            "collaborator_discovery",
            "technology_relationships",
            "network_analysis",
            "entity_classification"
        ]
    }