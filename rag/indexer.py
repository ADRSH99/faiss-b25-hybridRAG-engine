import faiss
import numpy as np

INDEX_PATH = "store/index.faiss"
EMB_PATH = "store/embeddings.npy"

def build_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    np.save(EMB_PATH, embeddings)

def load_index():
    return faiss.read_index(INDEX_PATH), np.load(EMB_PATH)

def search(index, query_emb, k):
    D, I = index.search(query_emb.reshape(1,-1), k)
    return I[0], D[0]
