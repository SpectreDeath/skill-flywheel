#!/usr/bin/env python3
"""
Mock Context Hub Provider Skill

This is a mock version of the context_hub_provider skill that provides
the same MCP tools but with mock implementations that don't require
the chub CLI tool to be installed.

Domain: Strategy & Analysis
Tools:
- search: Mock search for documentation and skills
- get_doc: Mock retrieve documentation by ID
- annotate: Mock add persistent annotations to entries

Safety: No external dependencies required
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass

@dataclass
class SearchResult:
    """Represents a search result from chub"""
    id: str
    name: str
    description: str
    type: str  # "doc" or "skill"
    source: Optional[str] = None
    tags: Optional[List[str]] = None
    languages: Optional[List[str]] = None

@dataclass
class DocumentContent:
    """Represents retrieved document content"""
    id: str
    content: str
    path: str
    language: Optional[str] = None
    version: Optional[str] = None
    additional_files: Optional[List[str]] = None
    annotation: Optional[str] = None

@dataclass
class AnnotationResult:
    """Represents annotation operation result"""
    id: str
    success: bool
    message: str
    annotation: Optional[str] = None

class MockContextHubProvider:
    """Mock implementation of ContextHubProvider"""
    
    def __init__(self):
        # Mock data for testing
        self.mock_skills = [
            {
                "id": "openai-api-reference",
                "name": "OpenAI API Reference",
                "description": "Complete reference for OpenAI API endpoints and parameters",
                "type": "doc",
                "source": "OpenAI",
                "tags": ["api", "reference", "openai"],
                "languages": ["python", "javascript"]
            },
            {
                "id": "context_hub_provider",
                "name": "Context Hub Provider",
                "description": "Python wrapper for chub CLI tool",
                "type": "skill",
                "source": "Custom",
                "tags": ["mcp", "context", "hub"],
                "languages": ["python"]
            },
            {
                "id": "mcp-tutorial-server",
                "name": "MCP Tutorial Server",
                "description": "Tutorial server for MCP protocol",
                "type": "doc",
                "source": "MCP",
                "tags": ["tutorial", "server", "mcp"],
                "languages": ["python"]
            }
        ]
        
        self.annotations = {}
    
    async def search(self, query: str = "", tags: Optional[List[str]] = None, 
                    limit: int = 20) -> List[SearchResult]:
        """
        Mock search for documentation and skills in the Context Hub
        
        Args:
            query: Search query (empty string lists all entries)
            tags: Optional list of tags to filter by
            limit: Maximum number of results to return
            
        Returns:
            List of search results
        """
        # Filter by query if provided
        if query:
            results = [
                skill for skill in self.mock_skills 
                if query.lower() in skill["name"].lower() or query.lower() in skill["description"].lower()
            ]
        else:
            results = self.mock_skills.copy()
        
        # Filter by tags if provided
        if tags:
            results = [
                skill for skill in results
                if skill.get("tags") and any(tag in skill["tags"] for tag in tags)
            ]
        
        # Limit results
        results = results[:limit]
        
        # Convert to SearchResult objects
        search_results = []
        for entry in results:
            search_results.append(SearchResult(
                id=entry["id"],
                name=entry["name"],
                description=entry["description"],
                type=entry["type"],
                source=entry.get("source"),
                tags=entry.get("tags"),
                languages=entry.get("languages")
            ))
        
        return search_results
    
    async def get_doc(self, doc_id: str, language: Optional[str] = None, 
                     version: Optional[str] = None) -> DocumentContent:
        """
        Mock retrieve documentation content by ID
        
        Args:
            doc_id: Document identifier
            language: Language variant (required for multi-language docs)
            version: Specific version (optional)
            
        Returns:
            Document content and metadata
        """
        # Find the document
        doc = next((skill for skill in self.mock_skills if skill["id"] == doc_id), None)
        
        if not doc:
            raise ValueError(f"Document {doc_id} not found")
        
        # Generate mock content
        content = f"""
# {doc["name"]}

**ID**: {doc["id"]}
**Type**: {doc["type"]}
**Source**: {doc.get("source", "Unknown")}

## Description

{doc["description"]}

## Tags

{", ".join(doc.get("tags", []))}

## Supported Languages

{", ".join(doc.get("languages", []))}

## Mock Content

This is mock documentation content for testing purposes.

- Feature 1: Implemented
- Feature 2: In progress
- Feature 3: Planned

## Code Example

```python
# Mock code example
result = await search("openai")
print(f"Found {len(result)} results")
```

## Additional Files

- README.md
- examples/
- tests/
"""
        
        # Get annotation if exists
        annotation = self.annotations.get(doc_id)
        
        return DocumentContent(
            id=doc_id,
            content=content,
            path=f"/docs/{doc_id}/SKILL.md",
            language=language,
            version=version,
            additional_files=["README.md", "examples/", "tests/"],
            annotation=annotation
        )
    
    async def annotate(self, doc_id: str, note: str) -> AnnotationResult:
        """
        Mock add or update an annotation for a document/skill
        
        Args:
            doc_id: Document or skill identifier
            note: Annotation text
            
        Returns:
            Annotation operation result
        """
        self.annotations[doc_id] = note
        
        return AnnotationResult(
            id=doc_id,
            success=True,
            message=f"Annotation saved for {doc_id}",
            annotation=note
        )
    
    async def clear_annotation(self, doc_id: str) -> AnnotationResult:
        """
        Mock clear annotation for a document/skill
        
        Args:
            doc_id: Document or skill identifier
            
        Returns:
            Annotation operation result
        """
        if doc_id in self.annotations:
            del self.annotations[doc_id]
            return AnnotationResult(
                id=doc_id,
                success=True,
                message=f"Annotation cleared for {doc_id}"
            )
        else:
            return AnnotationResult(
                id=doc_id,
                success=False,
                message=f"No annotation found for {doc_id}"
            )

# Global mock instance
_mock_context_hub_provider = MockContextHubProvider()

async def search(query: str = "", tags: Optional[List[str]] = None, 
                limit: int = 20) -> List[Dict[str, Any]]:
    """
    Mock search for documentation and skills in the Context Hub
    
    Args:
        query: Search query (empty string lists all entries)
        tags: Optional list of tags to filter by
        limit: Maximum number of results to return
        
    Returns:
        List of search results with id, name, description, type, source, tags, languages
    """
    results = await _mock_context_hub_provider.search(query, tags, limit)
    return [
        {
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "type": r.type,
            "source": r.source,
            "tags": r.tags,
            "languages": r.languages
        }
        for r in results
    ]

async def get_doc(doc_id: str, language: Optional[str] = None, 
                 version: Optional[str] = None) -> Dict[str, Any]:
    """
    Mock retrieve documentation content by ID
    
    Args:
        doc_id: Document identifier
        language: Language variant (required for multi-language docs)
        version: Specific version (optional)
        
    Returns:
        Document content with id, content, path, language, version, additional_files, annotation
    """
    result = await _mock_context_hub_provider.get_doc(doc_id, language, version)
    return {
        "id": result.id,
        "content": result.content,
        "path": result.path,
        "language": result.language,
        "version": result.version,
        "additional_files": result.additional_files,
        "annotation": result.annotation
    }

async def annotate(doc_id: str, note: str) -> Dict[str, Any]:
    """
    Mock add or update an annotation for a document/skill
    
    Args:
        doc_id: Document or skill identifier
        note: Annotation text
        
    Returns:
        Annotation operation result with success status and message
    """
    result = await _mock_context_hub_provider.annotate(doc_id, note)
    return {
        "id": result.id,
        "success": result.success,
        "message": result.message,
        "annotation": result.annotation
    }

async def clear_annotation(doc_id: str) -> Dict[str, Any]:
    """
    Mock clear annotation for a document/skill
    
    Args:
        doc_id: Document or skill identifier
        
    Returns:
        Annotation operation result with success status and message
    """
    result = await _mock_context_hub_provider.clear_annotation(doc_id)
    return {
        "id": result.id,
        "success": result.success,
        "message": result.message
    }

# Example usage function
async def example_usage():
    """Example of how to use the mock context_hub_provider skill"""
    try:
        # Search for OpenAI documentation
        print("Searching for OpenAI docs...")
        results = await search("openai", limit=5)
        for result in results:
            print(f"- {result['id']}: {result['name']} ({result['type']})")
        
        # Get specific documentation
        if results:
            doc_id = results[0]['id']
            print(f"\nRetrieving {doc_id}...")
            doc = await get_doc(doc_id, language="python")
            print(f"Content length: {len(doc['content'])} characters")
            print(f"Additional files: {doc['additional_files']}")
        
        # Add annotation
        if results:
            doc_id = results[0]['id']
            print(f"\nAdding annotation to {doc_id}...")
            annotation_result = await annotate(doc_id, "This is a useful OpenAI API reference")
            print(f"Annotation success: {annotation_result['success']}")
            
    except Exception as e:
        print(f"Example failed: {e}")

if __name__ == "__main__":
    asyncio.run(example_usage())