from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(text_list):
    return np.array(model.encode(text_list, show_progress_bar=True))

def embed_query(q):
    return np.array(model.encode([q])[0])
