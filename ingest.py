import os
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from supabase import create_client

load_dotenv()

oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
model = SentenceTransformer("all-MiniLM-L6-v2")


def add_note(text, source="manual", tags=None):
    if tags is None:
        tags = []

    embedding = model.encode(text).tolist()

    row = sb.table("notes").insert({
        "content": text,
        "embedding": embedding,
        "source": source,
        "tags": tags,
    }).execute()

    print(f"Gespeichert: '{text[:60]}...'")
    return row.data[0]


add_note("FastAPI nutzt Pydantic für Request-Validierung.", tags=["python"])
add_note("pgvector speichert Embeddings nativ in PostgreSQL.", tags=["database"])