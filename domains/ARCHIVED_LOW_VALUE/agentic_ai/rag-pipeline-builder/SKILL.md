---
name: rag-pipeline-builder
description: "Use when: building RAG pipelines, creating retrieval-augmented generation systems, implementing document question answering, or setting up knowledge base Q&A. Triggers: 'RAG', 'retrieval', 'rag pipeline', 'knowledge base', 'document Q&A', 'vector search', 'semantic search'. NOT for: when simple LLM-only responses are sufficient, no document retrieval needed, or when data is static without retrieval."
---

# RAG Pipeline Builder

Builds complete retrieval-augmented generation pipelines with document loading, chunking, embedding, and retrieval. This skill creates production-ready RAG systems.

## When to Use This Skill

Use this skill when:
- Building RAG pipelines
- Creating retrieval-augmented generation
- Implementing document Q&A
- Setting up knowledge base Q&A
- Creating semantic search systems

Do NOT use this skill when:
- Simple LLM-only responses
- No document retrieval needed
- Data is static without retrieval
- Simple Q&A without context

## Input Format

```yaml
rag_request:
  data_sources: array             # Documents to index
  chunk_strategy: string         # How to chunk documents
  embedding_model: string        # Embedding model to use
  vector_store: string          # Vector database
  retrieval_config: object      # Retrieval settings
```

## Output Format

```yaml
rag_result:
  pipeline_config: object       # Complete pipeline config
  indexing_code: string          # Code for document indexing
  retrieval_code: string        # Code for retrieval
  query_engine: string          # Full query engine
  example_queries: array       # Test queries
```

## Capabilities

### 1. Data Source Integration (15 min)

- Connect to various data sources
- Handle multiple formats (PDF, MD, HTML, JSON)
- Implement document loaders
- Handle large documents

### 2. Chunking Strategy (10 min)

- Design chunking strategies
- Implement overlap handling
- Handle special content (code, tables)
- Optimize for retrieval

### 3. Embedding & Indexing (15 min)

- Select embedding models
- Create vector indexes
- Configure similarity search
- Handle index updates

### 4. Retrieval Optimization (15 min)

- Implement hybrid search
- Add reranking
- Configure filters
- Optimize recall/precision

### 5. Query Engine (15 min)

- Build query processing
- Implement context windows
- Add follow-up questions
- Create streaming responses

## Usage Examples

### Basic Usage

"Build a RAG pipeline for my documents."

### Advanced Usage

"Create RAG with hybrid search, reranking, and streaming."

## Configuration Options

- `framework`: llama-index, langchain, custom
- `chunk_size`: 512, 1024, 2048
- `embedding`: openai, huggingface, local
- `vector_store`: pinecone, chroma, weaviate, faiss

## Constraints

- MUST handle various document formats
- SHOULD optimize for retrieval quality
- MUST include error handling
- SHOULD support updates

## Integration Examples

- LlamaIndex: Build with LlamaHub
- LangChain: Use LangChain abstractions
- Custom: Generate custom implementations
- Streaming: Add streaming responses

## Dependencies

- Python 3.10+
- LlamaIndex or LangChain
- Embedding models
- Vector databases
