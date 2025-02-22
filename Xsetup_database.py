import os
import openai

api_key = os.getenv("OPENAI_API_KEY")  # No quotes needed in getenv

client = openai.OpenAI(api_key=api_key)  # ✅ api_key is already a string
