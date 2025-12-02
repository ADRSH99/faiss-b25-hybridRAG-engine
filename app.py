from flask import Flask, request, jsonify, send_from_directory
from rag.retriever import HybridRetriever
from rag.llm import generate_answer

app = Flask(__name__, static_folder="static")
retriever = HybridRetriever()

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/retrieve", methods=["POST"])
def retrieve():
    q = request.json["question"]
    alpha = float(request.json.get("alpha", 0.5))
    res = retriever.hybrid_retrieve(q, alpha=alpha)
    return jsonify({"results": res})

@app.route("/ask", methods=["POST"])
def ask():
    q = request.json["question"]
    alpha = float(request.json.get("alpha", 0.5))
    retrieved = retriever.hybrid_retrieve(q, alpha=alpha)
    context = "\n\n".join([f"Title: {r['title']}\n{r['text']}" for r in retrieved])
    ans = generate_answer(context, q)
    return jsonify({"answer": ans, "retrieved": retrieved})

@app.route("/static/<path:f>")
def staticfiles(f):
    return send_from_directory("static", f)

if __name__ == "__main__":
    app.run(debug=True)
