from haystack import Document, Pipeline
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore

store = InMemoryDocumentStore(embedding_similarity_function="cosine")

with open("mein_dokument.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

docs = [
    Document(
        content=raw_text,
        meta={"source": "mein_dokument.txt"}
    )
]

indexing = Pipeline()

indexing.add_component(
    "splitter",
    DocumentSplitter(split_by="sentence", split_length=4, split_overlap=1)
)

indexing.add_component(
    "embedder",
    SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
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