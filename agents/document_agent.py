# agents/document_agent.py
import os
from openai import AzureOpenAI
from utils.search_utils import search_documents

client = AzureOpenAI(
    api_key=os.getenv("AZURE_AI_KEY"),
    azure_endpoint=os.getenv("AZURE_AI_ENDPOINT"),
    api_version="2024-12-01-preview"
)
deployment = os.getenv("AI_MODEL_DEPLOYMENT")

def call_document_agent(user_query: str) -> str:
    results = search_documents(user_query)
    context = "\n\n".join([f"Titre: {doc['title']}\nContenu: {doc['content']}" for doc in results])

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": f"Voici des procédures extraites d'une base documentaire :\n{context}"},
            {"role": "user", "content": user_query}
        ],
        max_tokens=1024,
        temperature=0.5
    )

    return response.choices[0].message.content
