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

pyDatalog embeds Datalog syntax in Python, so the surface is defined
as Python code that creates Datalog predicates and rules.
"""

from pathlib import Path
from typing import Dict, Any

# Surface definitions - pyDatalog embeds Datalog in Python
_base_path = Path(__file__).parent

# Define the Datalog surface as Python code that will be executed
DATALOG_SURFACE = """
from pyDatalog import pyDatalog

# Clear any existing facts/rules
pyDatalog.clear()

# Define terms
pyDatalog.create_terms('entity_type, relationship, collaborates_with, uses, org_uses, collaboration_network')
pyDatalog.create_terms('X, Y, Z, Person, Person1, Person2, Tech, Entity, Type, Org')

# Entity type facts
entity_type('person', 'human')
entity_type('organization', 'group')
entity_type('technology', 'artifact')

# Relationship facts
relationship('alice', 'works_at', 'openai')
relationship('bob', 'works_at', 'google')
relationship('charlie', 'collaborates_with', 'alice')
relationship('charlie', 'uses', 'python')
relationship('alice', 'uses', 'pytorch')
relationship('google', 'develops', 'tensorflow')

# Direct collaboration (bidirectional)
(collaborates_with(X, Y) <= relationship(X, 'collaborates_with', Y))
(collaborates_with(X, Y) <= relationship(Y, 'collaborates_with', X))

# Transitive collaboration
(collaborates_with(X, Z) <= (collaborates_with(X, Y) & collaborates_with(Y, Z) & (X != Z)))

# Technology usage through collaboration
(uses(X, Tech) <= (collaborates_with(X, Y) & relationship(Y, 'uses', Tech)))

# Organization technology stack
(org_uses(Org, Tech) <= (relationship(Person, 'works_at', Org) & relationship(Person, 'uses', Tech)))

# Collaboration networks around shared technologies
(collaboration_network(Person1, Person2, Tech) <= (
    collaborates_with(Person1, Person2) &
    uses(Person1, Tech) &
    uses(Person2, Tech) &
    (Person1 != Person2)
))
"""


def knowledge_graph(query_type: str, **params) -> Dict[str, Any]:
    """
    Query the knowledge graph using Datalog reasoning.

    Args:
        query_type: Type of query ('collaborators', 'tech_stack', 'networks', 'entity_types')
        **params: Query parameters

    Returns:
        Dictionary with query results
    """
    try:
        from pyDatalog import pyDatalog
    except ImportError:
        return {"error": "pyDatalog not available", "results": []}

    # Initialize fresh Datalog environment and load knowledge base
    pyDatalog.clear()

    try:
        # Create terms and predicates
        pyDatalog.create_terms('entity_type, relationship, collaborates_with, uses, org_uses, collaboration_network')
        pyDatalog.create_terms('X, Y, Z, Person, Person1, Person2, Tech, Entity, Type, Org')

        # Add facts using assert_fact
        pyDatalog.assert_fact('entity_type', 'person', 'human')
        pyDatalog.assert_fact('entity_type', 'organization', 'group')
        pyDatalog.assert_fact('entity_type', 'technology', 'artifact')

        pyDatalog.assert_fact('relationship', 'alice', 'works_at', 'openai')
        pyDatalog.assert_fact('relationship', 'bob', 'works_at', 'google')
        pyDatalog.assert_fact('relationship', 'charlie', 'collaborates_with', 'alice')
        pyDatalog.assert_fact('relationship', 'charlie', 'uses', 'python')
        pyDatalog.assert_fact('relationship', 'alice', 'uses', 'pytorch')
        pyDatalog.assert_fact('relationship', 'google', 'develops', 'tensorflow')

        # Add rules using string-based loading
        rules = '''
        collaborates_with(X, Y) <= relationship(X, 'collaborates_with', Y)
        collaborates_with(X, Y) <= relationship(Y, 'collaborates_with', X)
        collaborates_with(X, Z) <= (collaborates_with(X, Y) & collaborates_with(Y, Z) & (X != Z))

        uses(X, Tech) <= (collaborates_with(X, Y) & relationship(Y, 'uses', Tech))
        org_uses(Org, Tech) <= (relationship(Person, 'works_at', Org) & relationship(Person, 'uses', Tech))

        collaboration_network(Person1, Person2, Tech) <= (
            collaborates_with(Person1, Person2) &
            uses(Person1, Tech) &
            uses(Person2, Tech) &
            (Person1 != Person2)
        )
        '''
        pyDatalog.load(rules)

    except Exception as e:
        return {"error": f"Failed to initialize Datalog knowledge base: {e}", "results": []}

    results = []

    if query_type == "collaborators":
        # Find all collaborators for a person
        person = params.get("person", "alice")

        collaborators = []
        try:
            query_result = pyDatalog.ask(f"collaborates_with('{person}', Y)")
            if query_result and hasattr(query_result, 'answers'):
                collaborators = [result[1] for result in query_result.answers if len(result) > 1]
        except Exception as e:
            return {"error": f"Query failed: {e}", "results": []}

        results = collaborators

    elif query_type == "tech_stack":
        # Find technology stack for an organization
        org = params.get("organization", "google")

        tech_stack = []
        try:
            query_result = pyDatalog.ask(f"org_uses('{org}', Tech)")
            if query_result and hasattr(query_result, 'answers'):
                tech_stack = [result[1] for result in query_result.answers if len(result) > 1]
        except Exception as e:
            return {"error": f"Query failed: {e}", "results": []}

        results = list(set(tech_stack))  # Remove duplicates

    elif query_type == "networks":
        # Find collaboration networks around shared technologies
        networks = []
        try:
            query_result = pyDatalog.ask("collaboration_network(Person1, Person2, Tech)")
            if query_result and hasattr(query_result, 'answers'):
                for result in query_result.answers:
                    if len(result) >= 3:
                        networks.append({
                            "person1": result[0],
                            "person2": result[1],
                            "shared_technology": result[2]
                        })
        except Exception as e:
            return {"error": f"Query failed: {e}", "results": []}

        results = networks

    elif query_type == "entity_types":
        # Get all entity types
        types = []
        try:
            query_result = pyDatalog.ask("entity_type(Entity, Type)")
            if query_result and hasattr(query_result, 'answers'):
                for result in query_result.answers:
                    if len(result) >= 2:
                        types.append({
                            "entity": result[0],
                            "type": result[1]
                        })
        except Exception as e:
            return {"error": f"Query failed: {e}", "results": []}

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