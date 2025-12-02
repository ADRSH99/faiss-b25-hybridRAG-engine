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

```
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key_here" >> .env
echo "OPENAI_API_KEY=your_key_here" >> .env
python preprocess.py
python build_index.py
python app.py
```

Then open:

```
http://127.0.0.1:5000
```

---

# Project Structure and File Descriptions

... (truncated for brevity in this tool call)
