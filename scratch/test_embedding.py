import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

try:
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents="Hello world",
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=256,
        ),
    )
    print("Success with gemini-embedding-2. Dimension:", len(response.embeddings[0].values))
except Exception as e:
    print("Error:", e)

try:
    response = client.models.embed_content(
        model="text-embedding-004",
        contents="Hello world",
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=256,
        ),
    )
    print("Success with text-embedding-004. Dimension:", len(response.embeddings[0].values))
except Exception as e:
    print("Error with text-embedding-004:", e)
