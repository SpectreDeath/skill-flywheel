#!/usr/bin/env python3
"""
Skill: memory-management-system
Domain: ai_agent_development
Description: Advanced memory management system for AI agents with hierarchical storage and retrieval
"""

import asyncio
import hashlib
import json
import logging
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class MemoryType(Enum):
    """Types of memory"""
    EPISODIC = "episodic"      # Specific events and experiences
    SEMANTIC = "semantic"      # General knowledge and facts
    PROCEDURAL = "procedural"  # Skills and procedures
    WORKING = "working"        # Short-term active memory
    LONG_TERM = "long_term"    # Long-term storage

class MemoryPriority(Enum):
    """Memory priority levels"""
    CRITICAL = "critical"      # Must be retained
    HIGH = "high"             # Important information
    MEDIUM = "medium"         # Moderate importance
    LOW = "low"               # Can be forgotten
    TEMPORARY = "temporary"   # Short-term only

@dataclass
class MemoryItem:
    """Represents a memory item"""
    memory_id: str
    content: Dict[str, Any]
    memory_type: MemoryType
    priority: MemoryPriority
    created_at: float
    last_accessed: float
    access_count: int
    tags: List[str]
    context: Dict[str, Any]
    embedding: List[float] | None  # For semantic search
    ttl: float | None  # Time to live in seconds

@dataclass
class MemoryQuery:
    """Represents a memory query"""
    query_text: str
    memory_types: List[MemoryType]
    tags: List[str]
    time_range: tuple | None  # (start_time, end_time)
    limit: int
    similarity_threshold: float

class MemoryManagementSystem:
    """Advanced memory management system for AI agents"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the memory management system
        
        Args:
            config: Configuration dictionary with:
                - working_memory_size: Size of working memory
                - long_term_threshold: Time before moving to long-term
                - forgetting_threshold: Threshold for forgetting low-priority items
                - embedding_dim: Dimension of embeddings for semantic search
        """
        self.working_memory: List[MemoryItem] = []
        self.long_term_memory: Dict[str, MemoryItem] = {}
        self.episodic_memory: List[MemoryItem] = []
        self.semantic_memory: Dict[str, MemoryItem] = {}
        self.procedural_memory: Dict[str, MemoryItem] = {}
        
        self.working_memory_size = config.get("working_memory_size", 100)
        self.long_term_threshold = config.get("long_term_threshold", 3600)  # 1 hour
        self.forgetting_threshold = config.get("forgetting_threshold", 0.1)
        self.embedding_dim = config.get("embedding_dim", 128)
        
        self.memory_stats = {
            "total_memories": 0,
            "working_memory_usage": 0,
            "long_term_memory_usage": 0,
            "access_count": 0,
            "forgetting_events": 0
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Start background maintenance tasks
        self._maintenance_task = asyncio.create_task(self._maintenance_loop())
    
    async def store_memory(self, 
                          content: Dict[str, Any],
                          memory_type: MemoryType,
                          priority: MemoryPriority = MemoryPriority.MEDIUM,
                          tags: List[str] | None = None,
                          context: Dict[str, Any] | None = None,
                          ttl: int | None = None) -> str:
        """
        Store a memory item
        
        Args:
            content: The memory content
            memory_type: Type of memory
            priority: Priority level
            tags: Tags for categorization
            context: Additional context
            ttl: Time to live in seconds
            
        Returns:
            Memory ID
        """
        memory_id = str(uuid.uuid4())
        
        # Create embedding for semantic search
        embedding = await self._create_embedding(content)
        
        memory_item = MemoryItem(
            memory_id=memory_id,
            content=content,
            memory_type=memory_type,
            priority=priority,
            created_at=time.time(),
            last_accessed=time.time(),
            access_count=0,
            tags=tags or [],
            context=context or {},
            embedding=embedding,
            ttl=time.time() + ttl if ttl else None
        )
        
        # Store in appropriate memory systems
        self.working_memory.append(memory_item)
        self.memory_stats["total_memories"] += 1
        self.memory_stats["working_memory_usage"] += 1
        
        # Also store in type-specific memory
        if memory_type == MemoryType.EPISODIC:
            self.episodic_memory.append(memory_item)
        elif memory_type == MemoryType.SEMANTIC:
            # Use content hash as key for semantic memory
            content_hash = self._hash_content(content)
            self.semantic_memory[content_hash] = memory_item
        elif memory_type == MemoryType.PROCEDURAL:
            # Use procedure name as key
            procedure_name = content.get("procedure_name", content_hash)
            self.procedural_memory[procedure_name] = memory_item
        
        # Manage working memory size
        await self._manage_working_memory()
        
        self.logger.debug(f"Stored memory: {memory_id} ({memory_type.value})")
        return memory_id
    
    async def retrieve_memory(self, 
                             query: MemoryQuery) -> List[Dict[str, Any]]:
        """
        Retrieve memories based on query
        
        Args:
            query: Memory query
            
        Returns:
            List of matching memories
        """
        self.memory_stats["access_count"] += 1
        
        # Search working memory first (fastest)
        working_results = self._search_working_memory(query)
        
        # If not found in working memory, search long-term
        if len(working_results) < query.limit:
            long_term_results = await self._search_long_term_memory(query)
            working_results.extend(long_term_results)
        
        # Sort by relevance and access recency
        working_results.sort(key=lambda x: (
            x.get("similarity_score", 0),
            -x.get("last_accessed", 0)
        ), reverse=True)
        
        # Update access counts and timestamps
        for result in working_results[:query.limit]:
            memory_id = result["memory_id"]
            # Update in all memory systems
            for memory_list in [self.working_memory, self.episodic_memory]:
                for item in memory_list:
                    if item.memory_id == memory_id:
                        item.last_accessed = time.time()
                        item.access_count += 1
                        break
        
        return working_results[:query.limit]
    
    async def consolidate_memory(self, memory_id: str) -> bool:
        """
        Consolidate a memory from working to long-term storage
        
        Args:
            memory_id: ID of memory to consolidate
            
        Returns:
            True if successfully consolidated
        """
        # Find memory in working memory
        memory_item = None
        for item in self.working_memory:
            if item.memory_id == memory_id:
                memory_item = item
                break
        
        if not memory_item:
            return False
        
        # Move to long-term memory
        self.long_term_memory[memory_id] = memory_item
        self.working_memory = [item for item in self.working_memory if item.memory_id != memory_id]
        
        self.memory_stats["working_memory_usage"] -= 1
        self.memory_stats["long_term_memory_usage"] += 1
        
        self.logger.debug(f"Consolidated memory: {memory_id}")
        return True
    
    async def forget_memory(self, memory_id: str) -> bool:
        """
        Forget a memory (remove from all systems)
        
        Args:
            memory_id: ID of memory to forget
            
        Returns:
            True if successfully forgotten
        """
        # Remove from working memory
        self.working_memory = [item for item in self.working_memory if item.memory_id != memory_id]
        
        # Remove from long-term memory
        if memory_id in self.long_term_memory:
            del self.long_term_memory[memory_id]
            self.memory_stats["long_term_memory_usage"] -= 1
        
        # Remove from type-specific memories
        self.episodic_memory = [item for item in self.episodic_memory if item.memory_id != memory_id]
        
        content_hash = self._hash_content(self.long_term_memory.get(memory_id, MemoryItem("", {}, MemoryType.WORKING, MemoryPriority.LOW, 0, 0, 0, [], {}, None, None)).content)
        if content_hash in self.semantic_memory:
            del self.semantic_memory[content_hash]
        
        procedure_name = self.long_term_memory.get(memory_id, MemoryItem("", {}, MemoryType.WORKING, MemoryPriority.LOW, 0, 0, 0, [], {}, None, None)).content.get("procedure_name", "")
        if procedure_name in self.procedural_memory:
            del self.procedural_memory[procedure_name]
        
        self.memory_stats["total_memories"] -= 1
        self.memory_stats["forgetting_events"] += 1
        
        self.logger.debug(f"Forgot memory: {memory_id}")
        return True
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        return {
            "total_memories": self.memory_stats["total_memories"],
            "working_memory_size": len(self.working_memory),
            "working_memory_capacity": self.working_memory_size,
            "long_term_memory_size": len(self.long_term_memory),
            "episodic_memory_size": len(self.episodic_memory),
            "semantic_memory_size": len(self.semantic_memory),
            "procedural_memory_size": len(self.procedural_memory),
            "access_count": self.memory_stats["access_count"],
            "forgetting_events": self.memory_stats["forgetting_events"],
            "working_memory_utilization": len(self.working_memory) / self.working_memory_size if self.working_memory_size > 0 else 0
        }
    
    async def cleanup_expired_memories(self):
        """Clean up expired memories based on TTL"""
        current_time = time.time()
        expired_memories = []
        
        # Check working memory
        for item in self.working_memory:
            if item.ttl and item.ttl < current_time:
                expired_memories.append(item.memory_id)
        
        # Check long-term memory
        for item in self.long_term_memory.values():
            if item.ttl and item.ttl < current_time:
                expired_memories.append(item.memory_id)
        
        # Remove expired memories
        for memory_id in expired_memories:
            await self.forget_memory(memory_id)
        
        if expired_memories:
            self.logger.info(f"Cleaned up {len(expired_memories)} expired memories")
    
    async def _maintenance_loop(self):
        """Background maintenance loop"""
        while True:
            try:
                # Periodic cleanup
                await self.cleanup_expired_memories()
                
                # Consolidate old working memories
                await self._consolidate_old_memories()
                
                # Forgetting low-priority memories
                await self._forget_low_priority_memories()
                
                await asyncio.sleep(60)  # Run every minute
                
            except Exception as e:
                self.logger.error(f"Error in memory maintenance: {e}")
                await asyncio.sleep(60)
    
    async def _consolidate_old_memories(self):
        """Consolidate old working memories to long-term"""
        current_time = time.time()
        old_memories = []
        
        for item in self.working_memory:
            if current_time - item.created_at > self.long_term_threshold:
                old_memories.append(item.memory_id)
        
        for memory_id in old_memories:
            await self.consolidate_memory(memory_id)
    
    async def _forget_low_priority_memories(self):
        """Forget low-priority memories to free space"""
        if len(self.working_memory) < self.working_memory_size:
            return
        
        # Sort by priority and access count
        self.working_memory.sort(key=lambda x: (
            self._priority_weight(x.priority),
            x.access_count,
            x.last_accessed
        ))
        
        # Remove lowest priority items
        items_to_remove = len(self.working_memory) - self.working_memory_size + 10
        
        for _ in range(items_to_remove):
            if self.working_memory:
                oldest_item = self.working_memory.pop(0)
                await self.forget_memory(oldest_item.memory_id)
    
    def _search_working_memory(self, query: MemoryQuery) -> List[Dict[str, Any]]:
        """Search working memory for matching items"""
        results = []
        
        for item in self.working_memory:
            if self._matches_query(item, query):
                similarity = self._calculate_similarity(query.query_text, item.content)
                if similarity >= query.similarity_threshold:
                    results.append({
                        "memory_id": item.memory_id,
                        "content": item.content,
                        "memory_type": item.memory_type.value,
                        "priority": item.priority.value,
                        "similarity_score": similarity,
                        "access_count": item.access_count,
                        "last_accessed": item.last_accessed,
                        "created_at": item.created_at,
                        "tags": item.tags
                    })
        
        return results
    
    async def _search_long_term_memory(self, query: MemoryQuery) -> List[Dict[str, Any]]:
        """Search long-term memory for matching items"""
        results = []
        
        for item in self.long_term_memory.values():
            if self._matches_query(item, query):
                similarity = self._calculate_similarity(query.query_text, item.content)
                if similarity >= query.similarity_threshold:
                    results.append({
                        "memory_id": item.memory_id,
                        "content": item.content,
                        "memory_type": item.memory_type.value,
                        "priority": item.priority.value,
                        "similarity_score": similarity,
                        "access_count": item.access_count,
                        "last_accessed": item.last_accessed,
                        "created_at": item.created_at,
                        "tags": item.tags
                    })
        
        return results
    
    def _matches_query(self, item: MemoryItem, query: MemoryQuery) -> bool:
        """Check if memory item matches query criteria"""
        # Check memory type
        if item.memory_type not in query.memory_types:
            return False
        
        # Check tags
        if query.tags and not any(tag in item.tags for tag in query.tags):
            return False
        
        # Check time range
        if query.time_range:
            start_time, end_time = query.time_range
            if not (start_time <= item.created_at <= end_time):
                return False
        
        return True
    
    def _calculate_similarity(self, query_text: str, content: Dict[str, Any]) -> float:
        """Calculate semantic similarity between query and content"""
        # Simple text-based similarity for now
        # In a real implementation, this would use embeddings
        content_text = str(content)
        query_words = set(query_text.lower().split())
        content_words = set(content_text.lower().split())
        
        if not query_words or not content_words:
            return 0.0
        
        intersection = query_words & content_words
        union = query_words | content_words
        
        return len(intersection) / len(union)
    
    async def _create_embedding(self, content: Dict[str, Any]) -> List[float]:
        """Create embedding for content (simplified version)"""
        # In a real implementation, this would use a proper embedding model
        content_str = str(content)
        hash_value = hash(content_str) % (2**31)
        
        # Create a simple pseudo-embedding
        embedding = []
        for i in range(self.embedding_dim):
            embedding.append((hash_value * (i + 1)) % 1000 / 1000.0)
        
        return embedding
    
    def _hash_content(self, content: Dict[str, Any]) -> str:
        """Create hash of content for indexing"""
        content_str = json.dumps(content, sort_keys=True)
        return hashlib.md5(content_str.encode()).hexdigest()
    
    def _priority_weight(self, priority: MemoryPriority) -> int:
        """Get numeric weight for priority level"""
        weights = {
            MemoryPriority.CRITICAL: 5,
            MemoryPriority.HIGH: 4,
            MemoryPriority.MEDIUM: 3,
            MemoryPriority.LOW: 2,
            MemoryPriority.TEMPORARY: 1
        }
        return weights.get(priority, 0)
    
    async def _manage_working_memory(self):
        """Manage working memory size and organization"""
        if len(self.working_memory) > self.working_memory_size:
            # Sort by priority and access recency
            self.working_memory.sort(key=lambda x: (
                self._priority_weight(x.priority),
                -x.last_accessed,
                -x.access_count
            ))
            
            # Remove lowest priority items
            excess = len(self.working_memory) - self.working_memory_size
            for _ in range(excess):
                if self.working_memory:
                    item = self.working_memory.pop(0)
                    await self.consolidate_memory(item.memory_id)

# Global memory management system instance
_memory_system = MemoryManagementSystem({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "store", "retrieve", "consolidate", "forget", "get_stats", "cleanup"
            - memory_data: Memory data for storage
            - query_data: Query data for retrieval
            - memory_id: Memory identifier
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "store":
            memory_data = payload.get("memory_data", {})
            
            memory_id = await _memory_system.store_memory(
                content=memory_data.get("content", {}),
                memory_type=MemoryType(memory_data.get("memory_type", "episodic")),
                priority=MemoryPriority(memory_data.get("priority", "medium")),
                tags=memory_data.get("tags", []),
                context=memory_data.get("context", {}),
                ttl=memory_data.get("ttl")
            )
            
            return {
                "result": {
                    "memory_id": memory_id,
                    "message": f"Stored memory: {memory_id}"
                },
                "metadata": {
                    "action": "store",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "retrieve":
            query_data = payload.get("query_data", {})
            
            query = MemoryQuery(
                query_text=query_data.get("query_text", ""),
                memory_types=[MemoryType(t) for t in query_data.get("memory_types", ["episodic"])],
                tags=query_data.get("tags", []),
                time_range=tuple(query_data.get("time_range", (0, time.time()))),
                limit=query_data.get("limit", 10),
                similarity_threshold=query_data.get("similarity_threshold", 0.1)
            )
            
            results = await _memory_system.retrieve_memory(query)
            
            return {
                "result": results,
                "metadata": {
                    "action": "retrieve",
                    "timestamp": datetime.now().isoformat(),
                    "query_text": query.query_text,
                    "result_count": len(results)
                }
            }
        
        elif action == "consolidate":
            memory_id = payload.get("memory_id", "")
            success = await _memory_system.consolidate_memory(memory_id)
            
            return {
                "result": {
                    "memory_id": memory_id,
                    "success": success,
                    "message": f"Consolidated memory: {memory_id}" if success else f"Failed to consolidate memory: {memory_id}"
                },
                "metadata": {
                    "action": "consolidate",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "forget":
            memory_id = payload.get("memory_id", "")
            success = await _memory_system.forget_memory(memory_id)
            
            return {
                "result": {
                    "memory_id": memory_id,
                    "success": success,
                    "message": f"Frogory: {memory_id}" if success else f"Failed to forget memory: {memory_id}"
                },
                "metadata": {
                    "action": "forget",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_stats":
            stats = _memory_system.get_memory_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "cleanup":
            await _memory_system.cleanup_expired_memories()
            
            return {
                "result": {
                    "message": "Memory cleanup completed"
                },
                "metadata": {
                    "action": "cleanup",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        else:
            return {
                "result": {
                    "error": f"Unknown action: {action}"
                },
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat()
                }
            }
    
    except Exception as e:
        logger.error(f"Error in memory_management_system: {e}")
        return {
            "result": {
                "error": str(e)
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat()
            }
        }

# Example usage function
async def example_usage():
    """Example of how to use the memory management system skill"""
    
    # Store some memories
    memory1_id = await invoke({
        "action": "store",
        "memory_data": {
            "content": {"event": "user_login", "user_id": "user123", "timestamp": time.time()},
            "memory_type": "episodic",
            "priority": "high",
            "tags": ["login", "security"],
            "context": {"ip_address": "192.168.1.1"}
        }
    })
    
    memory2_id = await invoke({
        "action": "store",
        "memory_data": {
            "content": {"fact": "Python is a programming language", "created": time.time()},
            "memory_type": "semantic",
            "priority": "medium",
            "tags": ["programming", "python"]
        }
    })
    
    print(f"Stored memories: {memory1_id['result']['memory_id']}, {memory2_id['result']['memory_id']}")
    
    # Retrieve memories
    results = await invoke({
        "action": "retrieve",
        "query_data": {
            "query_text": "login",
            "memory_types": ["episodic"],
            "limit": 5,
            "similarity_threshold": 0.1
        }
    })
    
    print(f"Retrieved {len(results['result'])} memories")
    
    # Get memory statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Memory stats: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
