from haystack import Document, Pipeline
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder,
)
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore

from openai import OpenAI
from dotenv import load_dotenv
import os


# ---------------------------
# OpenRouter client
# ---------------------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


# ---------------------------
# Document store
# ---------------------------

store = InMemoryDocumentStore(
    embedding_similarity_function="cosine"
)


# ---------------------------
# Load document
# ---------------------------

with open("mein_dokument.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

docs = [
    Document(
        content=raw_text,
        meta={"source": "mein_dokument.txt"}
    )
]


# ---------------------------
# Indexing pipeline
# ---------------------------

indexing = Pipeline()

indexing.add_component(
    "splitter",
    DocumentSplitter(
        split_by="sentence",
        split_length=4,
        split_overlap=1
    )
)

indexing.add_component(
    "embedder",
    SentenceTransformersDocumentEmbedder(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
)

indexing.add_component(
    "writer",
    DocumentWriter(document_store=store)
)

indexing.connect("splitter.documents", "embedder.documents")
indexing.connect("embedder.documents", "writer.documents")

indexing.run({
    "splitter": {
        "documents": docs
    }
})

print(f"Indexed: {store.count_documents()} chunks")


# ---------------------------
# Query / retrieval pipeline
# ---------------------------

query_pipeline = Pipeline()

query_pipeline.add_component(
    "text_embedder",
    SentenceTransformersTextEmbedder(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
)

query_pipeline.add_component(
    "retriever",
    InMemoryEmbeddingRetriever(
        document_store=store,
        top_k=3
    )
)

query_pipeline.connect(
    "text_embedder.embedding",
    "retriever.query_embedding"
)


# ---------------------------
# Ask question
# ---------------------------

question = "What are the main topics?"

result = query_pipeline.run({
    "text_embedder": {
        "text": question
    }
})

retrieved_docs = result["retriever"]["documents"]

print("\nRetrieved Chunks:\n")

for doc in retrieved_docs:
    print(f"Source: {doc.meta['source']}")
    print(doc.content)
    print("-" * 50)


# ---------------------------
# Send retrieved context to LLM
# ---------------------------

context = "\n\n".join(
    doc.content for doc in retrieved_docs
)

prompt = f"""
Answer the question only using the context below.

Context:
{context}

Question:
{question}
"""

response = client.responses.create(
    model="openai/gpt-4o-mini",
    input=prompt
)

print("\nAnswer:\n")
print(response.output_text)