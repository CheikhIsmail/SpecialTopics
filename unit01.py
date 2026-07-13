from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY nicht gefunden – .env vorhanden?")

print(f"Key geladen: {api_key[:8]}...")