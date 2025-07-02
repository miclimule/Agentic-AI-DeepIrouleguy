# utils/search_utils.py
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from utils.embeddings_utils import get_embedding
import os

search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

credential = AzureKeyCredential(search_key)
search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=credential)

def index_documents(documents: list):
    docs_with_vector = []
    for doc in documents:
        docs_with_vector.append({
            "id": str(doc["id"]),
            "title": doc["title"],
            "content": doc["content"],
            "content_vector": get_embedding(doc["content"])
        })

    result = search_client.upload_documents(documents=docs_with_vector)
    return result

def search_documents(query: str, k: int = 3):
    vector = get_embedding(query)

    results = search_client.search(
        search_text=None,
        vectors=[
            {
                "value": vector,
                "fields": "content_vector",
                "k": k,
                "kind": "vector"
            }
        ],
        select=["id", "title", "content"]
    )

    return [doc for doc in results]
