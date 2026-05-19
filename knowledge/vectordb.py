import chromadb

from sentence_transformers import SentenceTransformer


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="document_chunks"
)

model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)

def create_embedding(text):

    embedding = model.encode(text)

    return embedding.tolist()

def store_embedding(
    chunk_text,
    embedding,
    document_id
):

    embedding_id = (
        f"doc_{document_id}_{hash(chunk_text)}"
    )

    collection.add(
        documents=[chunk_text],

        embeddings=[embedding],

        metadatas=[
            {"document_id": document_id}
        ],

        ids=[embedding_id]
    )

    return embedding_id

def search_similar_chunks(
    query,
    n_results=3
):

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],

        n_results=n_results
    )

    documents = results['documents'][0]

    combined_text = "\n".join(documents)

    metadatas = results['metadatas'][0]

    return {
        "context": combined_text,
        "sources": metadatas
    }

