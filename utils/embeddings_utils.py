# utils/embeddings_utils.py
from openai import AzureOpenAI
import os

client = AzureOpenAI(
    api_key=os.getenv("AZURE_AI_KEY"),
    azure_endpoint=os.getenv("AZURE_AI_ENDPOINT"),
    api_version="2024-12-01-preview"
)

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-large"
    )
    return response.data[0].embedding
