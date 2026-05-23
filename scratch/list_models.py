import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
print("Models:")
for model in client.models.list():
    if "embed" in model.name.lower():
        print(f"Model Name: {model.name}")
        print(f"Supported Methods: {model.supported_actions}")
