# rag/retriever.py
import json
import numpy as np
import re
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder
from rag.embedder import embed_query
from rag.indexer import load_index, search

TOP_K_FAISS = 100
TOP_K_BM25 = 100
HYBRID_TOP_N = 50
FINAL_K = 5
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

def simple_tokenize(text):
    """Simple regex tokenizer to replace NLTK."""
    return re.findall(r"\b\w+\b", text.lower())

class HybridRetriever:
    def __init__(self):
        # Load chunks
        self.chunks = json.load(open("data/chunks.json","r",encoding="utf-8"))
        self.texts = [c["text"] for c in self.chunks]

        # Build BM25 corpus using simple tokenizer
        corpus = [simple_tokenize(t) for t in self.texts]
        self.bm25 = BM25Okapi(corpus)

        # Load FAISS index
        self.index, self.embeddings = load_index()

        # Load Reranker model
        self.rerank = CrossEncoder(RERANK_MODEL)

    def bm25_search(self, query):
        q_tokens = simple_tokenize(query)
        scores = self.bm25.get_scores(q_tokens)
        idx = np.argsort(scores)[::-1][:TOP_K_BM25]
        return idx, scores[idx]

    def faiss_search(self, query):
        q_emb = embed_query(query)
        idx, dists = search(self.index, q_emb, TOP_K_FAISS)
        scores = -np.array(dists)  # convert distance→score
        return idx, scores

    def hybrid_retrieve(self, query, alpha=0.5):
        # BM25
        bm_idx, bm_scores = self.bm25_search(query)

        # FAISS
        fs_idx, fs_scores = self.faiss_search(query)

        # union of candidates
        candidates = np.unique(np.concatenate([bm_idx, fs_idx]))

        # map scores
        bm_map = {int(i): float(s) for i, s in zip(bm_idx, bm_scores)}
        fs_map = {int(i): float(s) for i, s in zip(fs_idx, fs_scores)}

        # Get arrays aligned with candidates
        bm_vals = np.array([bm_map.get(int(i), 0.0) for i in candidates])
        fs_vals = np.array([fs_map.get(int(i), -1e9) for i in candidates])

        # normalize scores
        def norm(x):
            return (x - x.min()) / (x.max() - x.min() + 1e-9)

        combined = alpha * norm(fs_vals) + (1 - alpha) * norm(bm_vals)

        # pick top candidates for reranking
        top = np.argsort(combined)[::-1][:HYBRID_TOP_N]
        cand_ids = [int(candidates[i]) for i in top]

        # rerank using cross-encoder
        pairs = [[query, self.texts[i]] for i in cand_ids]
        rerank_scores = self.rerank.predict(pairs)

        # pick final ranked
        order = np.argsort(rerank_scores)[::-1][:FINAL_K]
        final_ids = [cand_ids[i] for i in order]
        final_scores = [float(rerank_scores[i]) for i in order]

        # return chunk metadata
        results = []
        for cid, score in zip(final_ids, final_scores):
            c = self.chunks[cid].copy()
            c["score"] = score
            results.append(c)

        return results
