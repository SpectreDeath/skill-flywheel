---
name: llm-agent-integration
description: "Use when: integrating LLMs (Claude/GPT/Gemini), building RAG systems, implementing agent tool-use/function-calling, handling streaming responses, managing multi-turn conversations, building AI agents, creating embeddings, or building production AI applications. Triggers: 'LLM', 'Claude', 'OpenAI', 'GPT', 'Gemini', 'prompt', 'embedding', 'RAG', 'tool use', 'function calling', 'streaming', 'AI agent', 'chat completion'. NOT for: pure code generation (use coding skills), or when no AI/LLM involvement."
---

# LLM Agent Integration

Comprehensive skill for integrating LLMs, building RAG systems, implementing agent workflows, and production AI reliability patterns.

## Supported Providers

- Anthropic (Claude)
- OpenAI (GPT-4)
- Google Gemini
- Local models (Ollama, LM Studio)

## Core API Integration

```python
from anthropic import Anthropic
from openai import OpenAI
import google.genai as genai

class LLMClient:
    """Unified LLM client."""
    
    def __init__(self, provider: str, api_key: str):
        self.provider = provider
        if provider == "anthropic":
            self.client = Anthropic(api_key=api_key)
        elif provider == "openai":
            self.client = OpenAI(api_key=api_key)
        elif provider == "gemini":
            self.client = genai.Client(api_key=api_key)
            
    def chat(self, messages: list, **kwargs) -> str:
        """Send chat request."""
        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=kwargs.get("model", "claude-3-5-sonnet-20241022"),
                messages=messages,
                max_tokens=kwargs.get("max_tokens", 4096),
                temperature=kwargs.get("temperature", 0.7)
            )
            return response.content[0].text
            
        elif self.provider == "openai":
            response = self.client.chat.completions.create(
                model=kwargs.get("model", "gpt-4o"),
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 4096)
            )
            return response.choices[0].message.content
            
        elif self.provider == "gemini":
            response = self.client.models.generate_content(
                model=kwargs.get("model", "gemini-2.0-flash"),
                contents=messages
            )
            return response.text
```

## Streaming Responses

```python
def stream_response(client: LLMClient, messages: list):
    """Handle streaming responses."""
    
    # Anthropic
    with client.client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        messages=messages
    ) as stream:
        for text in stream.text_stream:
            yield text
            
    # OpenAI
    response = client.client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True
    )
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

## Tool Use / Function Calling

```python
from typing import List, Dict, Any

class Tool:
    """Define a tool for LLM."""
    
    def __init__(self, name: str, description: str, input_schema: dict):
        self.name = name
        self.description = description
        self.input_schema = input_schema

def execute_tool(name: str, args: dict) -> Any:
    """Execute tool and return result."""
    tools = {
        "weather": lambda args: get_weather(args["location"]),
        "calculator": lambda args: eval(args["expression"]),
        "search": lambda args: search_web(args["query"])
    }
    return tools[name](args)

class AgentWithTools:
    """LLM agent with tool execution."""
    
    def __init__(self, client: LLMClient, tools: List[Tool]):
        self.client = client
        self.tools = tools
        
    def run(self, user_message: str, max_iterations=10) -> str:
        """Run agent with tool use loop."""
        
        messages = [{"role": "user", "content": user_message}]
        
        for _ in range(max_iterations):
            response = self.client.chat(
                messages=messages,
                tools=self.get_tool_definitions()
            )
            
            # Check for tool calls
            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tool_call in response.tool_calls:
                    result = execute_tool(
                        tool_call.name,
                        tool_call.arguments
                    )
                    # Add result to conversation
                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    messages.append({
                        "role": "user",
                        "content": f"Tool result: {result}"
                    })
            else:
                return response
                
        return "Max iterations reached"
        
    def get_tool_definitions(self) -> list:
        """Get tool definitions for API."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema
            }
            for tool in self.tools
        ]
```

## RAG System Implementation

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

class RAGSystem:
    """Retrieval Augmented Generation system."""
    
    def __init__(self, embedding_model="text-embedding-3-small"):
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
    def add_documents(self, documents: List[str], ids: List[str] = None):
        """Add documents to vector store."""
        
        # Split into chunks
        chunks = []
        for doc in documents:
            chunks.extend(self.text_splitter.split_text(doc))
            
        # Create vector store
        self.vectorstore = Chroma.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            ids=ids
        )
        
    def retrieve(self, query: str, top_k=5) -> List[str]:
        """Retrieve relevant documents."""
        
        docs = self.vectorstore.similarity_search(query, k=top_k)
        return [doc.page_content for doc in docs]
        
    def query(self, user_query: str, system_prompt: str = None) -> str:
        """Query with retrieved context."""
        
        # Retrieve context
        context = self.retrieve(user_query)
        
        # Build messages
        if system_prompt is None:
            system_prompt = """You are a helpful assistant. 
            Use the provided context to answer questions."""
            
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{chr(10).join(context)}\n\nQuestion: {user_query}"}
        ]
        
        return self.client.chat(messages)

class HybridRetriever:
    """Hybrid retrieval (keyword + semantic)."""
    
    def __init__(self, vectorstore, keyword_index):
        self.vectorstore = vectorstore
        self.keyword_index = keyword_index
        
    def retrieve(self, query: str, top_k=5) -> List[Document]:
        """Retrieve from both indexes and combine."""
        
        # Semantic search
        semantic_docs = self.vectorstore.similarity_search(query, k=top_k)
        
        # Keyword search
        keyword_docs = self.keyword_index.search(query, k=top_k)
        
        # Reciprocal rank fusion
        return self.rrf_merge(semantic_docs, keyword_docs, k=60)
        
    @staticmethod
    def rrf_merge(docs1, docs2, k=60):
        """Reciprocal rank fusion."""
        scores = {}
        for rank, doc in enumerate(docs1):
            scores[doc.id] = scores.get(doc.id, 0) + 1 / (k + rank + 1)
        for rank, doc in enumerate(docs2):
            scores[doc.id] = scores.get(doc.id, 0) + 1 / (k + rank + 1)
            
        return sorted(docs1 + docs2, key=lambda d: scores[d.id], reverse=True)[:10]
```

## Multi-turn Conversation

```python
class ConversationManager:
    """Manage multi-turn conversations."""
    
    def __init__(self, client: LLMClient, max_history=20):
        self.client = client
        self.max_history = max_history
        self.conversations = {}
        
    def create_session(self, session_id: str, system_prompt: str = None):
        """Create new conversation session."""
        self.conversations[session_id] = {
            "messages": [],
            "system": system_prompt or "You are a helpful assistant."
        }
        
    def add_message(self, session_id: str, role: str, content: str):
        """Add message to conversation."""
        conv = self.conversations[session_id]
        conv["messages"].append({"role": role, "content": content})
        
        # Trim if too long
        if len(conv["messages"]) > self.max_history:
            conv["messages"] = conv["messages"][-self.max_history:]
            
    def get_messages(self, session_id: str) -> list:
        """Get formatted messages for API."""
        conv = self.conversations[session_id]
        messages = [{"role": "system", "content": conv["system"]}]
        messages.extend(conv["messages"])
        return messages
        
    def chat(self, session_id: str, user_message: str) -> str:
        """Send message and get response."""
        
        self.add_message(session_id, "user", user_message)
        messages = self.get_messages(session_id)
        
        response = self.client.chat(messages)
        
        self.add_message(session_id, "assistant", response)
        return response
```

## Production Reliability Patterns

```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, backoff_factor=2):
    """Retry decorator with exponential backoff."""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(backoff_factor ** attempt)
        return wrapper
    return decorator

class RateLimiter:
    """Rate limiter for API calls."""
    
    def __init__(self, calls_per_minute=60):
        self.calls_per_minute = calls_per_minute
        self.calls = []
        
    def wait_if_needed(self):
        """Wait if rate limit reached."""
        now = time.time()
        self.calls = [t for t in self.calls if now - t < 60]
        
        if len(self.calls) >= self.calls_per_minute:
            sleep_time = 60 - (now - self.calls[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
                
        self.calls.append(now)

class CircuitBreaker:
    """Circuit breaker for failed requests."""
    
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
        
    def call(self, func, *args, **kwargs):
        """Execute with circuit breaker."""
        
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise CircuitBreakerOpen()
                
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
            
    def on_success(self):
        self.failures = 0
        self.state = "closed"
        
    def on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "open"
```

## Prompt Engineering Patterns

```python
class PromptTemplates:
    """Common prompt patterns."""
    
    @staticmethod
    def with_context(context: str, question: str) -> str:
        return f"""Context: {context}

Question: {question}

Answer:"""
        
    @staticmethod
    def with_examples(examples: list, input: str) -> str:
        example_text = "\n".join([
            f"Input: {ex['input']}\nOutput: {ex['output']}"
            for ex in examples
        ])
        return f"""Examples:
{example_text}

Input: {input}

Output:"""
        
    @staticmethod
    def chain_of_thought() -> str:
        return """Think step by step. Show your reasoning process.
        
Question: {question}

Let's think through this:"""
        
    @staticmethod
    def structured_output(schema: dict) -> str:
        return f"""Provide output in the following JSON format:
{json.dumps(schema)}

Input: {input}

Output:"""
```

## Token Estimation

```python
def estimate_tokens(text: str) -> int:
    """Estimate token count (rough approximation)."""
    # Average ~4 characters per token
    return len(text) // 4

def estimate_messages_tokens(messages: list, model: str) -> int:
    """Estimate tokens for message history."""
    # Different models have different overhead
    overhead = {
        "claude-3-5-sonnet-20241022": 4,
        "gpt-4o": 3,
        "gemini-2.0-flash": 4
    }
    base = overhead.get(model, 4)
    
    total = 0
    for msg in messages:
        total += base  # role overhead
        total += estimate_tokens(msg["content"])
    return total
```

## Constraints

- MUST handle API errors gracefully with retries
- SHOULD implement rate limiting to avoid quota exhaustion
- MUST track token usage for cost management
- SHOULD use streaming for long responses
- MUST implement proper tool schema definitions
- SHOULD use circuit breaker for resilience
- MUST handle context window limits