# uvicorn api:app --reload --port 8000
# → http://localhost:8000/docs

# client.py
import requests

BASE = "http://localhost:8000"

def ask_rag(question, top_k=3):
    resp = requests.post(f"{BASE}/ask", json={"question": question, "top_k": top_k})
    resp.raise_for_status()
    return resp.json()

result = ask_rag("Was sind die Hauptthemen des Dokuments?")
print("Antwort:", result["answer"])
print("Quellen:", result["sources"])