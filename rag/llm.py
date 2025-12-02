import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def generate_answer(context, question):
    prompt = f"""
Use ONLY the following context to answer:

{context}

Question: {question}

Answer:
"""
    return model.generate_content(prompt).text
