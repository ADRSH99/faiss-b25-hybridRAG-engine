import google.generativeai as genai
import os

genai.configure(api_key="")
model = genai.GenerativeModel("models/gemini-2.5-flash")

def generate_answer(context, question):
    prompt = f"""
Use ONLY the following context to answer:

{context}

Question: {question}

Answer:
"""
    return model.generate_content(prompt).text
