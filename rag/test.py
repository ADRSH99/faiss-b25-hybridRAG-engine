import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyDJJsI-3Ir49KzTdLj1tkNe8x4WoIGmMt0")

models = genai.list_models()

for m in models:
    print(m.name, m.supported_generation_methods)