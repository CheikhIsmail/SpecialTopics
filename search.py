import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing in .env")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is missing in .env")

sb = create_client(SUPABASE_URL, SUPABASE_KEY)
model = SentenceTransformer("all-MiniLM-L6-v2")


def search_knowledge(query, top_k=5, threshold=0.0):
    query_embedding = model.encode(query).tolist()

    result = sb.rpc(
        "search_notes",
        {
            "query_embedding": query_embedding,
            "match_count": top_k,
            "similarity_threshold": threshold,
        },
    ).execute()

    return result.data


if __name__ == "__main__":
    query = "Pydantic Validation in FastAPI"

    print("Encoding query...")
    results = search_knowledge(query, top_k=5, threshold=0.0)
    print("Search finished.")

    if not results:
        print("No results found.")
    else:
        for note in results:
            print("-" * 50)
            print(f"Similarity : {note['similarity']:.3f}")
            print(f"Content    : {note['content']}")