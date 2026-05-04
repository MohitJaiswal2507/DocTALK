import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection("documents")

def store_chunks(chunks, embeddings):

    for i in range(len(chunks)):

        collection.add(
            documents=[chunks[i]],
            embeddings=[embeddings[i].tolist()],
            ids=[str(i)]
        )