import json
from rag.embedder import embed_texts
from rag.indexer import build_index

chunks = json.load(open("data/chunks.json","r",encoding="utf-8"))
texts = [c["text"] for c in chunks]

print("Embedding", len(texts), "chunks...")
emb = embed_texts(texts)

print("Building FAISS index...")
build_index(emb)
print("Done!")
