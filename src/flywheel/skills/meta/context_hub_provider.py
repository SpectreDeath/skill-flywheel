#!/usr/bin/env python3
"
Context Hub Provider Skill

This skill provides a Python wrapper for the chub CLI tool, exposing its functionality
as MCP tools. It enables agents to search for, retrieve, and annotate documentation
and skills from the Context Hub system.

Domain: Strategy & Analysis
Tools:
- search: Search for documentation and skills
- get_doc: Retrieve documentation by ID with language support
- annotate: Add persistent annotations to entries

Safety: Verifies chub binary existence before execution
"

import asyncio
import json
import logging
from datetime import datetime
import shutil
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class ChubError(Exception):
    "Custom exception for chub-related errors"
    pass

class Language(Enum):
    "Supported languages for documentation retrieval"
    PYTHON = "py"
    JAVASCRIPT = "js"
    TYPESCRIPT = "ts"
    RUBY = "rb"
    CSHARP = "cs"
    PYTHON_FULL = "python"
    JAVASCRIPT_FULL = "javascript"
    TYPESCRIPT_FULL = "typescript"
    RUBY_FULL = "ruby"
    CSHARP_FULL = "csharp"

@dataclass
class SearchResult:
    "Represents a search result from chub"
    id: str
    name: str
    description: str
    type: str  # "doc" or "skill"
    source: str | None = None
    tags: List[str] | None = None
    languages: List[str] | None = None

@dataclass
class DocumentContent:
    "Represents retrieved document content"
    id: str
    content: str
    path: str
    language: str | None = None
    version: str | None = None
    additional_files: List[str] | None = None
    annotation: str | None = None

@dataclass
class AnnotationResult:
    "Represents annotation operation result"
    id: str
    success: bool
    message: str
    annotation: str | None = None

class ContextHubProvider:
    "Main class for the context_hub_provider skill"
    
    def __init__(self):
        self.chub_path = self._find_chub_binary()
    
    def _find_chub_binary(self) -> str:
        "Find the chub binary in system PATH"
        chub_path = shutil.which("chub")
        if not chub_path:
            raise ChubError(
                "chub binary not found in system PATH. Please install Context Hub: "
                "npm install -g @aisuite/chub"
            )
        logger.info(f"Found chub binary at: {chub_path}")
        return chub_path
    
    async def _run_chub_command(self, args: List[str], timeout: int = 30) -> Dict[str, Any]:
        "
        Execute a chub command and return parsed JSON output
        
        Args:
            args: Command arguments (e.g., ["search", "query"])
            timeout: Command timeout in seconds
            
        Returns:
            Parsed JSON response from chub
            
        Raises:
            ChubError: If command fails or returns invalid JSON
        "
        try:
            # Add --json flag for structured output
            full_args = [self.chub_path] + args + ["--json"]
            
            logger.debug(f"Executing: {' '.join(full_args)}")
            
            # Run command with timeout
            process = await asyncio.create_subprocess_exec(
                *full_args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            
            # Check for errors
            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                raise ChubError(f"chub command failed: {error_msg}")
            
            # Parse JSON output
            try:
                result = json.loads(stdout.decode())
                return result
            except json.JSONDecodeError as e:
                raise ChubError(f"Invalid JSON output from chub: {e}")
                
        except asyncio.TimeoutError:
            raise ChubError(f"chub command timed out after {timeout} seconds")
        except Exception as e:
            raise ChubError(f"Failed to execute chub command: {e}")
    
    async def search(self, query: str = ", tags: List[str] | None = None, 
                    limit: int = 20) -> List[SearchResult]:
        "
        Search for documentation and skills in the Context Hub
        
        Args:
            query: Search query (empty string lists all entries)
            tags: Optional list of tags to filter by
            limit: Maximum number of results to return
            
        Returns:
            List of search results
        "
        args = ["search"]
        
        if query:
            args.append(query)
        
        if tags:
            args.extend(["--tags", ",".join(tags)])
        
        args.extend(["--limit", str(limit)])
        
        try:
            result = await self._run_chub_command(args)
            
            # Handle different result formats
            if "results" in result:
                entries = result["results"]
            elif "entries" in result:
                entries = result["entries"]
            else:
                # Single entry result (exact match)
                entries = [result]
            
            search_results = []
            for entry in entries:
                search_results.append(SearchResult(
                    id=entry.get("id", "),
                    name=entry.get("name", "),
                    description=entry.get("description", "),
                    type=entry.get("_type", "doc"),
                    source=entry.get("source"),
                    tags=entry.get("tags"),
                    languages=[lang.get("language") for lang in entry.get("languages", [])] if entry.get("languages") else None
                ))
            
            logger.info(f"Found {len(search_results)} results for query: '{query}'")
            return search_results
            
        except ChubError as e:
            logger.error(f"Search failed: {e}")
            raise
    
    async def get_doc(self, doc_id: str, language: str | None = None, 
                     version: str | None = None) -> DocumentContent:
        "
        Retrieve documentation content by ID
        
        Args:
            doc_id: Document identifier
            language: Language variant (required for multi-language docs)
            version: Specific version (optional)
            
        Returns:
            Document content and metadata
        "
        args = ["get", doc_id]
        
        if language:
            args.extend(["--lang", language])
        
        if version:
            args.extend(["--version", version])
        
        try:
            result = await self._run_chub_command(args)
            
            # Handle different result formats
            if isinstance(result, dict):
                if "content" in result:
                    # Single document result
                    content = result["content"]
                    path = result.get("path", ")
                    additional_files = result.get("additionalFiles", [])
                    annotation = result.get("annotation", {}).get("note") if result.get("annotation") else None
                    
                    return DocumentContent(
                        id=doc_id,
                        content=content,
                        path=path,
                        language=language,
                        version=version,
                        additional_files=additional_files,
                        annotation=annotation
                    )
                elif "files" in result:
                    # Multiple files result (--full)
                    # For now, return the main content if available
                    main_file = next((f for f in result["files"] if f["name"] in ["DOC.md", "SKILL.md"]), None)
                    if main_file:
                        return DocumentContent(
                            id=doc_id,
                            content=main_file["content"],
                            path=result.get("path", "),
                            language=language,
                            version=version
                        )
            
            # Fallback for unexpected format
            raise ChubError(f"Unexpected result format: {result}")
            
        except ChubError as e:
            logger.error(f"Failed to retrieve document {doc_id}: {e}")
            raise
    
    async def annotate(self, doc_id: str, note: str) -> AnnotationResult:
        "
        Add or update an annotation for a document/skill
        
        Args:
            doc_id: Document or skill identifier
            note: Annotation text
            
        Returns:
            Annotation operation result
        "
        args = ["annotate", doc_id, note]
        
        try:
            result = await self._run_chub_command(args)
            
            # Check if annotation was successful
            if isinstance(result, dict):
                if "id" in result and "cleared" in result:
                    # Clear operation result
                    return AnnotationResult(
                        id=doc_id,
                        success=True,
                        message=f"Annotation {'cleared' if result['cleared'] else 'not found'} for {doc_id}"
                    )
                elif "id" in result:
                    # Set annotation result
                    return AnnotationResult(
                        id=doc_id,
                        success=True,
                        message=f"Annotation saved for {doc_id}",
                        annotation=note
                    )
            
            # Fallback
            return AnnotationResult(
                id=doc_id,
                success=False,
                message=f"Unexpected result format: {result}"
            )
            
        except ChubError as e:
            logger.error(f"Failed to annotate {doc_id}: {e}")
            return AnnotationResult(
                id=doc_id,
                success=False,
                message=str(e)
            )
    
    async def clear_annotation(self, doc_id: str) -> AnnotationResult:
        "
        Clear annotation for a document/skill
        
        Args:
            doc_id: Document or skill identifier
            
        Returns:
            Annotation operation result
        "
        args = ["annotate", doc_id, "--clear"]
        
        try:
            result = await self._run_chub_command(args)
            
            if isinstance(result, dict) and "cleared" in result:
                return AnnotationResult(
                    id=doc_id,
                    success=True,
                    message=f"Annotation {'cleared' if result['cleared'] else 'not found'} for {doc_id}"
                )
            
            return AnnotationResult(
                id=doc_id,
                success=False,
                message=f"Unexpected result format: {result}"
            )
            
        except ChubError as e:
            logger.error(f"Failed to clear annotation for {doc_id}: {e}")
            return AnnotationResult(
                id=doc_id,
                success=False,
                message=str(e)
            )

# Global instance
_context_hub_provider = ContextHubProvider()

async def search(query: str = ", tags: List[str] | None = None, 
                limit: int = 20) -> List[Dict[str, Any]]:
    "
    Search for documentation and skills in the Context Hub
    
    Args:
        query: Search query (empty string lists all entries)
        tags: Optional list of tags to filter by
        limit: Maximum number of results to return
        
    Returns:
        List of search results with id, name, description, type, source, tags, languages
    "
    results = await _context_hub_provider.search(query, tags, limit)
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

async def get_doc(doc_id: str, language: str | None = None, 
                 version: str | None = None) -> Dict[str, Any]:
    "
    Retrieve documentation content by ID
    
    Args:
        doc_id: Document identifier
        language: Language variant (required for multi-language docs)
        version: Specific version (optional)
        
    Returns:
        Document content with id, content, path, language, version, additional_files, annotation
    "
    result = await _context_hub_provider.get_doc(doc_id, language, version)
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
    "
    Add or update an annotation for a document/skill
    
    Args:
        doc_id: Document or skill identifier
        note: Annotation text
        
    Returns:
        Annotation operation result with success status and message
    "
    result = await _context_hub_provider.annotate(doc_id, note)
    return {
        "id": result.id,
        "success": result.success,
        "message": result.message,
        "annotation": result.annotation
    }

async def clear_annotation(doc_id: str) -> Dict[str, Any]:
    "
    Clear annotation for a document/skill
    
    Args:
        doc_id: Document or skill identifier
        
    Returns:
        Annotation operation result with success status and message
    "
    result = await _context_hub_provider.clear_annotation(doc_id)
    return {
        "id": result.id,
        "success": result.success,
        "message": result.message
    }

# Example usage function
async def example_usage():
    "Example of how to use the context_hub_provider skill"
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


# --- invoke() wrapper added by batch fix ---
async def invoke(payload: dict) -> dict:
    "Entry point for skill invocation."
    import datetime as _dt
    action = payload.get("action", "search")
    timestamp = _dt.datetime.now().isoformat()

    actions_available = ["search", "get_doc", "annotate", "clear_annotation", "get_info"]

    if action == "get_info":
        return {"result": {"name": "context-hub-provider", "actions": actions_available}, "metadata": {"action": action, "timestamp": timestamp}}

    try:
        if action == "search":
            result = await search(query=payload.get("query", "), tags=payload.get("tags"), limit=payload.get("limit", 20))
            return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

        elif action == "get_doc":
            result = await get_doc(doc_id=payload.get("doc_id", "), language=payload.get("language"))
            return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

        elif action == "annotate":
            result = await annotate(doc_id=payload.get("doc_id", "), note=payload.get("note", "))
            return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

        elif action == "clear_annotation":
            result = await clear_annotation(doc_id=payload.get("doc_id", "))
            return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}

        else:
            return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}

    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action, "timestamp": timestamp}}


def register_skill() -> dict:
    "Return skill metadata."
    return {
        "name": "context_hub_provider",
        "domain": "meta",
        "version": "1.0.0",
    }
