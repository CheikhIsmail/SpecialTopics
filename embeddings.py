from sentence_transformers import SentenceTransformer
import numpy as np

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Example documents
docs = [
    "Python is an interpreted programming language.",
    "Machine learning requires large amounts of training data.",
    "FastAPI is a modern web framework for Python.",
    "Neural networks learn patterns from examples.",
    "REST APIs communicate over HTTP.",
]

# Create embeddings
doc_embeddings = model.encode(docs)

print(f"Embedding dimension: {doc_embeddings.shape[1]}")


def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def semantic_search(query, docs, doc_embeddings, top_k=3):
    query_embedding = model.encode([query])[0]

    scores = [
        (cosine_similarity(query_embedding, doc_embedding), doc)
        for doc_embedding, doc in zip(doc_embeddings, docs)
    ]

    scores.sort(reverse=True)
    return scores[:top_k]


# Search query
query = "How do you build a web API with Python?"

results = semantic_search(query, docs, doc_embeddings)

print("\nSemantic Search Results:")
for score, doc in results:
    print(f"[{score:.3f}] {doc}")