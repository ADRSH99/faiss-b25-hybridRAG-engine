# preprocess.py
import re, json, os
from transformers import AutoTokenizer

os.makedirs("data", exist_ok=True)

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def parse_documents(raw_text):
    documents = []
    sections = raw_text.split("### ")
    for sec in sections[1:]:
        parts = sec.split("\n", 1)
        title = parts[0].strip()
        body = parts[1] if len(parts) > 1 else ""
        documents.append({
            "title": title,
            "content": clean_text(body)
        })
    return documents

def incremental_tokenize(t):
    tokens = []
    step = 1000
    for i in range(0, len(t), step):
        slice_tokens = tokenizer.encode(t[i:i+step], add_special_tokens=False)
        tokens.extend(slice_tokens)
    return tokens

def chunk_tokens(tokens, max_tokens=500):
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunks.append(tokens[i:i+max_tokens])
    return chunks

def build_chunks_from_documents(docs):
    chunks = []
    chunk_id = 0
    for doc_id, doc in enumerate(docs):
        tokens = incremental_tokenize(doc["content"])
        token_chunks = chunk_tokens(tokens)
        for tc in token_chunks:
            text = tokenizer.decode(tc, skip_special_tokens=True)
            chunks.append({
                "chunk_id": chunk_id,
                "doc_id": doc_id,
                "title": doc["title"],
                "text": text
            })
            chunk_id += 1
    return chunks

if __name__ == "__main__":
    raw = open("music_wiki_dump.txt", "r", encoding="utf-8").read()
    docs = parse_documents(raw)
    chunks = build_chunks_from_documents(docs)
    json.dump(chunks, open("data/chunks.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Saved {len(chunks)} chunks → data/chunks.json")
