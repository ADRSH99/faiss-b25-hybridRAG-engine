
# README — Hybrid RAG System with BM25, FAISS, MiniLM, and Cross-Encoder Reranking

This repository implements a complete hybrid Retrieval-Augmented Generation (RAG) system over a Wikipedia Music dump. The pipeline integrates:

- Document cleaning and chunking  
- MiniLM vector embeddings  
- FAISS vector search  
- BM25 lexical retrieval  
- Hybrid scoring  
- Cross-Encoder reranking  
- LLM-based generation (Gemini/OpenAI)  
- A Flask backend  
- A web UI with evidence highlighting  

The system demonstrates how modern RAG architectures work internally without relying on external frameworks such as LangChain or LlamaIndex.

---

# Quick Start (How to Run)

To preprocess → index → run server:

```
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add API keys
Create a .env file with:
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# 3. Preprocess raw Wikipedia dump (creates chunks.json)
python preprocess.py

# 4. Build MiniLM embeddings + FAISS index
python build_index.py

# 5. Run the RAG Flask server
python app.py

# 6. Open the Web UI
http://127.0.0.1:5000
```

All commands must be run from the repository root.

---

# Project Structure and File Descriptions

```
mini_rag/
│
├── preprocess.py
├── build_index.py
├── app.py
├── music_wiki_dump.txt
│
├── data/
│   └── chunks.json
│
├── store/
│   ├── index.faiss
│   └── embeddings.npy
│
├── rag/
│   ├── embedder.py
│   ├── indexer.py
│   ├── llm.py
│   └── retriever.py
│
└── static/
    ├── index.html
    ├── main.js
    └── style.css
```

---

## Top-Level Files

### preprocess.py
- Reads the raw Wikipedia dump (`music_wiki_dump.txt`)
- Splits by headings (`### Title`)
- Cleans and normalizes text
- Builds token-based chunks (300–500 tokens)
- Saves to `data/chunks.json`

### build_index.py
- Loads chunks from `data/chunks.json`
- Embeds all chunks using MiniLM (`all-MiniLM-L6-v2`)
- Builds a FAISS vector index for fast similarity search
- Saves embeddings and index to `store/`

### app.py
The main Flask server. It:
- Loads the hybrid retriever
- Serves the UI at `/`
- Provides API endpoints:
  - `/api/retrieve` – BM25 + FAISS + hybrid + reranking
  - `/api/generate` – retrieve + LLM answer generation

### music_wiki_dump.txt
Raw dataset containing Wikipedia music articles in:

```
### Title
content...
```

format.

---

# Data Folder

### data/chunks.json
Created by `preprocess.py`, containing text chunks with:

- chunk_id  
- title  
- cleaned text  
- word boundaries  

This is the main corpus for retrieval.

---

# Store Folder

### store/index.faiss
FAISS index storing vector embeddings for fast k-NN lookup.

### store/embeddings.npy
Numpy file storing the MiniLM embeddings for redundancy and quick reload.

---

# rag/ — Retrieval Logic

### embedder.py
- Loads MiniLM embedding model
- Embeds text lists
- Embeds queries individually

### indexer.py
- Builds FAISS index  
- Saves and loads index  
- Provides nearest-neighbor search  

### llm.py
Wrapper for Gemini-Pro or OpenAI GPT with a stable structured prompt.

### retriever.py
Implements the full hybrid retrieval pipeline:

1. Simple regex tokenizer (no NLTK)
2. BM25 lexical retrieval
3. FAISS semantic retrieval
4. Score normalization
5. Weighted hybrid scoring
6. Cross-Encoder reranking
7. Returns final top chunks with relevance scores

---

# static/ — Frontend UI

### index.html
Frontend interface for:
- Entering a query
- Adjusting semantic/lexical weighting
- Viewing retrieved chunks
- Asking the LLM for an answer

### main.js
Implements:
- API calls to Flask
- Evidence highlighting
- Dynamic display updates

### style.css
Defines UI layout, evidence card styling, highlighted tokens, buttons, typography.

---

# Theoretical Overview of the RAG System

This project showcases a full RAG pipeline used widely in modern LLM applications.

---

## 1. Preprocessing and Chunking
Chunking allows:
- Better retrieval granularity  
- Reduced noise  
- Easier matching  
- Avoiding overlong inputs to the LLM  

Chunks are kept between 300–500 tokens for optimal semantic retrieval performance.

---

## 2. Semantic Embeddings (MiniLM)
MiniLM converts text into dense vectors encoding meaning.  
Capabilities:
- Captures topic similarity  
- Handles paraphrasing  
- Provides robust retrieval when keywords differ  

Embedding dimension: **384**

---

## 3. FAISS Vector Search
FAISS enables:
- Extremely fast nearest-neighbor search  
- Scalable vector similarity lookup  
- Efficient L2-based semantic scoring  

FAISS alone captures semantic meaning but may miss keyword-specific queries.

---

## 4. BM25 Lexical Retrieval
BM25 identifies documents based on exact word matches and term importance.

Advantages:
- Good for definitions  
- Good for rare terms  
- Strong for names, dates, specific references  

Weakness: does not understand semantics.

---

## 5. Hybrid Retrieval
To combine strengths of both approaches, we compute:

```
HybridScore = α * SemanticScore + (1 − α) * BM25Score
```

α is adjustable in the UI.

Hybrid retrieval improves recall significantly.

---

## 6. Cross-Encoder Reranking
A cross-encoder looks at query and chunk together and outputs a deep relevance score.

This stage yields the most accurate ordering.

Model used:
- `cross-encoder/ms-marco-MiniLM-L-6-v2`

Only the top hybrid results are reranked for efficiency.

---

## 7. LLM Answering
Top chunks form the context.  
The LLM (Gemini or GPT) answers with:

```
Use only the provided context to answer the question.
```

This minimizes hallucinations and grounds the output.

---

# Conclusion

This repository demonstrates a complete RAG system with:

- Preprocessing  
- Chunking  
- Embeddings  
- FAISS  
- BM25  
- Hybrid scoring  
- Reranking  
- LLM answering  
- Evidence highlighting UI  

It is ideal for:
- Academic assignments  
- Learning RAG internals  
- Building fast search engines  
- Experimenting with retrieval pipelines  

---

