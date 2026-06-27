"""
retriever.py
Implements the RAG (Retrieval-Augmented Generation) pipeline.
Ingests company knowledge base documents into ChromaDB vector store
and retrieves relevant context chunks based on customer queries.
"""
import os
import chromadb
from chromadb.utils import embedding_functions

DOCS_PATH = "docs/"
CHROMA_PATH = "chroma_db/"

# SentenceTransformer embedding model for semantic search
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Initialize persistent ChromaDB client and collection
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(
    name="support_docs",
    embedding_function=embedding_fn
)

def ingest_documents():
    """
    Loads all .txt documents from the docs/ folder, splits them into
    paragraph-level chunks, and stores them in ChromaDB.
    Skips ingestion if documents are already loaded.
    """
    if collection.count() > 0:
        print("Documents already ingested. Skipping.")
        return

    print("Ingesting documents...")
    doc_files = [f for f in os.listdir(DOCS_PATH) if f.endswith(".txt")]

    for doc_file in doc_files:
        with open(os.path.join(DOCS_PATH, doc_file), "r") as f:
            content = f.read()

        # Chunk by paragraph breaks for semantic coherence
        chunks = [c.strip() for c in content.split("\n\n") if c.strip()]

        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                ids=[f"{doc_file}_{i}"]
            )

    print(f"Ingested {collection.count()} chunks.")


def retrieve_context(query: str, top_k: int = 3) -> str:
    """
    Retrieves the top-k most semantically relevant chunks
    from ChromaDB based on the customer query.
    Returns chunks joined as a single context string.
    """
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    docs = results["documents"][0]
    return "\n\n".join(docs)