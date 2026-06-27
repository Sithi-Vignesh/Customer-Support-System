import os
import chromadb
from chromadb.utils import embedding_functions

DOCS_PATH = "docs/"
CHROMA_PATH = "chroma_db/"

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(
    name="support_docs",
    embedding_function=embedding_fn
)

def ingest_documents():
    if collection.count() > 0:
        print("Documents already ingested. Skipping.")
        return

    print("Ingesting documents...")
    doc_files = [f for f in os.listdir(DOCS_PATH) if f.endswith(".txt")]

    for doc_file in doc_files:
        with open(os.path.join(DOCS_PATH, doc_file), "r") as f:
            content = f.read()

        chunks = [c.strip() for c in content.split("\n\n") if c.strip()]

        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                ids=[f"{doc_file}_{i}"]
            )

    print(f"Ingested {collection.count()} chunks.")


def retrieve_context(query: str, top_k: int = 3) -> str:
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    docs = results["documents"][0]
    return "\n\n".join(docs)