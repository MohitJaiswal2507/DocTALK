# from backend.vector_store.chroma_store import collection
from backend.vector_store.chroma_store import collection

def retrieve(query_embedding):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    documents = results["documents"][0]

    return documents  # return LIST, not joined text