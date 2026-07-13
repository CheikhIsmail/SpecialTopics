from sentence_transformers import SentenceTransformer
from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv
from chunking import chunk_by_sentences

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

with open("mein_dokument.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_by_sentences(text, max_sentences=2)
chunk_embeddings = embed_model.encode(chunks)

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def retrieve(query, top_k=3):
    q_emb = embed_model.encode([query])[0]
    scores = [
        cosine_similarity(q_emb, c_emb)
        for c_emb in chunk_embeddings
    ]
    top_idx = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]

    return [(scores[i], chunks[i]) for i in top_idx]

def ask(question):
    retrieved = retrieve(question)
    context = "\n---\n".join([chunk for score, chunk in retrieved])

    resp = client.responses.create(
        model="openai/gpt-4o-mini",
        input=(
            "Answer only using the context below.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}"
        )
    )

    return resp.output_text, retrieved

question = "Why is chunking useful in RAG?"

answer, retrieved_chunks = ask(question)

print("Question:")
print(question)

print("\nRetrieved Chunks:")
for score, chunk in retrieved_chunks:
    print(f"[{score:.3f}] {chunk}")

print("\nAnswer:")
print(answer)