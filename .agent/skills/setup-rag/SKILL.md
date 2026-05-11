---
name: setup-rag
description: >
  Generates a RAG (Retrieval-Augmented Generation) pipeline with chunking strategy, embedding, vector
  store setup, retrieval configuration, and reranking. Use this skill whenever the user wants to build
  a RAG system, implement document retrieval for an LLM, create a semantic search pipeline, build a
  knowledge base Q&A system, or asks to "set up RAG", "build a RAG pipeline", "implement retrieval
  augmented generation", "create a document Q&A system", "set up vector search", "implement semantic
  search with LLM", "add knowledge base to my chatbot", or "build a document retrieval system".
  Also trigger for "embedding pipeline", "vector database setup", "LlamaIndex setup", "LangChain RAG",
  "Chroma setup", "Pinecone integration", "Weaviate setup", and "reranking pipeline". Distinct from
  setup-eval-harness (which evaluates model outputs) and writer-prompt (which designs prompts).
---

# setup-rag

Generate a **RAG pipeline** with document ingestion, chunking, embedding, vector store, retrieval, and generation.

## RAG Pipeline Overview

```
Documents → Chunking → Embedding → Vector Store
                                      ↓
User Query → Embedding → Retrieval → Reranking → LLM → Response
```

## Technology selection

| Component | Options | Default |
|-----------|---------|---------|
| **Vector store** | Chroma (local), Pinecone, Weaviate, pgvector, FAISS | Chroma (local dev) |
| **Embedding model** | OpenAI text-embedding-3-small, sentence-transformers, Cohere | OpenAI text-embedding-3-small |
| **LLM** | GPT-4o, Claude, Llama, Mistral | GPT-4o-mini |
| **Framework** | LlamaIndex, LangChain, custom | Custom (explicit, no magic) |
| **Reranker** | Cohere rerank, cross-encoder, none | None (for simplicity) |

Detect from context (imports, existing code, explicit mention). Default to the simplest stack.

## Output structure

```
rag/
├── README.md
├── requirements.txt
├── config.py               # Configuration
├── ingest.py               # Document ingestion pipeline
├── retriever.py            # Retrieval + reranking
├── rag.py                  # Main RAG chain
└── data/
    └── documents/          # Source documents
```

## Configuration (`config.py`)

```python
import os
from dataclasses import dataclass, field

@dataclass
class RAGConfig:
    # Embedding
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    
    # Chunking
    chunk_size: int = 512          # Characters (or tokens)
    chunk_overlap: int = 64        # Overlap between chunks for context continuity
    
    # Retrieval
    top_k: int = 5                 # Number of chunks to retrieve
    similarity_threshold: float = 0.7  # Minimum similarity score
    
    # Vector store
    vector_store: str = "chroma"   # "chroma", "pinecone", "pgvector"
    collection_name: str = "knowledge_base"
    persist_dir: str = "./chroma_db"
    
    # LLM
    llm_model: str = "gpt-4o-mini"
    max_tokens: int = 1024
    temperature: float = 0.0       # Deterministic for factual Q&A
    
    # System prompt
    system_prompt: str = """You are a helpful assistant that answers questions based on the provided context.
    
If the answer is not in the context, say "I don't have information about that in the provided documents."
Always cite the source document(s) you used to answer."""

CONFIG = RAGConfig()
```

## Ingestion pipeline (`ingest.py`)

```python
import hashlib
from pathlib import Path
from typing import Generator
import chromadb
from openai import OpenAI

from config import CONFIG

client = OpenAI()

# ── Chunking ──────────────────────────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = CONFIG.chunk_size, overlap: int = CONFIG.chunk_overlap) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        # Prefer to break at sentence boundaries
        if end < len(text):
            last_period = chunk.rfind(". ")
            if last_period > chunk_size * 0.5:  # Only break at sentence if not too early
                chunk = chunk[:last_period + 1]
                end = start + last_period + 1
        
        if chunk.strip():
            chunks.append(chunk.strip())
        
        start = end - overlap
    
    return chunks

def chunk_by_tokens(text: str, max_tokens: int = 512) -> list[str]:
    """Token-aware chunking using tiktoken."""
    import tiktoken
    enc = tiktoken.encoding_for_model("text-embedding-3-small")
    tokens = enc.encode(text)
    
    chunks = []
    for i in range(0, len(tokens), max_tokens - 50):  # 50 token overlap
        chunk_tokens = tokens[i:i + max_tokens]
        chunks.append(enc.decode(chunk_tokens))
    
    return chunks

# ── Document loading ──────────────────────────────────────────────────────

def load_document(path: str) -> tuple[str, dict]:
    """Load document text and extract metadata."""
    path = Path(path)
    
    if path.suffix == ".pdf":
        import pypdf
        reader = pypdf.PdfReader(path)
        text = "\n\n".join(page.extract_text() for page in reader.pages)
        metadata = {"source": str(path), "type": "pdf", "pages": len(reader.pages)}
    
    elif path.suffix in [".md", ".txt"]:
        text = path.read_text(encoding="utf-8")
        metadata = {"source": str(path), "type": path.suffix.lstrip(".")}
    
    elif path.suffix == ".json":
        import json
        data = json.loads(path.read_text())
        # Assume JSON has a "text" or "content" field
        text = data.get("text") or data.get("content") or str(data)
        metadata = {"source": str(path), "type": "json", **data.get("metadata", {})}
    
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    
    return text, metadata

# ── Embedding ─────────────────────────────────────────────────────────────

def embed_texts(texts: list[str], model: str = CONFIG.embedding_model) -> list[list[float]]:
    """Embed a batch of texts."""
    response = client.embeddings.create(input=texts, model=model)
    return [item.embedding for item in response.data]

# ── Ingestion ─────────────────────────────────────────────────────────────

def ingest_documents(paths: list[str], collection_name: str = CONFIG.collection_name):
    """Ingest documents into the vector store."""
    chroma_client = chromadb.PersistentClient(path=CONFIG.persist_dir)
    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )
    
    for path in paths:
        print(f"Ingesting: {path}")
        text, base_metadata = load_document(path)
        chunks = chunk_text(text)
        
        if not chunks:
            print(f"  Skipping — no content extracted")
            continue
        
        # Batch embed
        embeddings = embed_texts(chunks)
        
        # Create unique IDs (based on content hash)
        ids = [
            hashlib.md5(f"{path}:{i}:{chunk}".encode()).hexdigest()
            for i, chunk in enumerate(chunks)
        ]
        
        metadatas = [
            {**base_metadata, "chunk_index": i, "chunk_total": len(chunks)}
            for i in range(len(chunks))
        ]
        
        # Upsert (skip if already indexed)
        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )
        
        print(f"  ✓ Ingested {len(chunks)} chunks")
    
    print(f"\nIngestion complete. Collection '{collection_name}' has {collection.count()} chunks.")
```

## Retrieval (`retriever.py`)

```python
import chromadb
from openai import OpenAI
from config import CONFIG

client = OpenAI()

def retrieve(
    query: str,
    top_k: int = CONFIG.top_k,
    collection_name: str = CONFIG.collection_name,
    filter: dict = None,   # Optional metadata filter
) -> list[dict]:
    """Retrieve relevant chunks for a query."""
    
    # Embed query
    query_embedding = client.embeddings.create(
        input=[query], model=CONFIG.embedding_model
    ).data[0].embedding
    
    # Query vector store
    chroma_client = chromadb.PersistentClient(path=CONFIG.persist_dir)
    collection = chroma_client.get_collection(collection_name)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=filter,
        include=["documents", "metadatas", "distances"],
    )
    
    # Format results
    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        similarity = 1 - dist  # Cosine distance to similarity
        if similarity >= CONFIG.similarity_threshold:
            chunks.append({"text": doc, "metadata": meta, "similarity": similarity})
    
    return chunks

def rerank(query: str, chunks: list[dict]) -> list[dict]:
    """Rerank chunks using Cohere (optional; improves precision)."""
    try:
        import cohere
        co = cohere.Client()
        response = co.rerank(
            query=query,
            documents=[c["text"] for c in chunks],
            top_n=CONFIG.top_k,
            model="rerank-english-v3.0",
        )
        return [
            {**chunks[r.index], "rerank_score": r.relevance_score}
            for r in response.results
        ]
    except ImportError:
        return chunks  # Graceful fallback if Cohere not installed
```

## RAG chain (`rag.py`)

```python
from openai import OpenAI
from retriever import retrieve, rerank
from config import CONFIG

client = OpenAI()

def format_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into a context block."""
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk["metadata"].get("source", "Unknown")
        context_parts.append(f"[Source {i}: {source}]\n{chunk['text']}")
    return "\n\n---\n\n".join(context_parts)

def ask(
    question: str,
    chat_history: list[dict] = None,
    top_k: int = CONFIG.top_k,
    model: str = CONFIG.llm_model,
) -> dict:
    """Answer a question using RAG."""
    
    # Retrieve
    chunks = retrieve(question, top_k=top_k)
    if not chunks:
        return {"answer": "I don't have information about that in the provided documents.", "sources": []}
    
    # Optional reranking
    chunks = rerank(question, chunks)
    context = format_context(chunks)
    
    # Generate
    messages = [
        {"role": "system", "content": CONFIG.system_prompt},
        *(chat_history or []),
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        },
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=CONFIG.max_tokens,
        temperature=CONFIG.temperature,
    )
    
    answer = response.choices[0].message.content
    sources = list({c["metadata"].get("source") for c in chunks})
    
    return {"answer": answer, "sources": sources, "chunks_used": len(chunks)}

# ── CLI ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    from ingest import ingest_documents
    
    if len(sys.argv) > 1 and sys.argv[1] == "ingest":
        paths = sys.argv[2:]
        ingest_documents(paths)
    else:
        print("RAG Q&A System (type 'quit' to exit)")
        history = []
        while True:
            q = input("\nQuestion: ").strip()
            if q.lower() in ("quit", "exit"): break
            result = ask(q, chat_history=history)
            print(f"\nAnswer: {result['answer']}")
            print(f"Sources: {', '.join(result['sources'])}")
            # Maintain multi-turn history
            history.append({"role": "user", "content": q})
            history.append({"role": "assistant", "content": result["answer"]})
```

## Calibration

- **Pinecone instead of Chroma**: Show `pinecone.init()`, upsert, and query API
- **pgvector**: Show `CREATE EXTENSION vector`, `CREATE TABLE embeddings (... embedding vector(1536))`, and similarity search SQL
- **LangChain**: Show `RetrievalQA` chain with `Chroma.from_documents()`
- **LlamaIndex**: Show `VectorStoreIndex.from_documents()` and `index.as_query_engine()`
- **Streaming response**: Show `client.chat.completions.create(stream=True)` with SSE output
