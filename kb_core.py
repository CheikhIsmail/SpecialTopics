import base64
import os
from typing import Any

import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from supabase import Client, create_client


load_dotenv()

# Prefer the clearer variable name, but keep the old name as a fallback
# so the rest of the course project does not break.
OPENROUTER_API_KEY = (
    os.getenv("OPENROUTER_API_KEY")
    or os.getenv("OPENAI_API_KEY")
)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

DEFAULT_SEARCH_THRESHOLD = float(
    os.getenv("SEARCH_THRESHOLD", "0.0")
)
EMBEDDING_MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL_NAME",
    "all-MiniLM-L6-v2",
)
OPENROUTER_STT_MODEL = os.getenv(
    "OPENROUTER_STT_MODEL",
    "openai/whisper-large-v3",
)

if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY is missing from .env "
        "(OPENAI_API_KEY is also accepted as a fallback)"
    )

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is missing from .env")

if not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_KEY is missing from .env")


sb: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
model = SentenceTransformer(EMBEDDING_MODEL_NAME)


def _to_pgvector(values: Any) -> str:
    """Convert an embedding to PostgreSQL pgvector text format."""
    return "[" + ",".join(str(float(value)) for value in values) + "]"


def _audio_format(audio_path: str) -> str:
    """Map a file extension to an OpenRouter-supported audio format."""
    extension = os.path.splitext(audio_path)[1].lower().lstrip(".")

    if extension == "m4a":
        return "mp4"

    if extension in {"wav", "mp3", "mp4", "mpeg", "mpga", "webm"}:
        return extension

    raise ValueError(
        f"Unsupported audio format: .{extension or 'unknown'}. "
        "Use WAV, MP3, M4A, MP4, MPEG, MPGA, or WEBM."
    )


def add_note(
    text: str,
    source: str = "manual",
    tags: list[str] | None = None,
) -> dict:
    cleaned_text = text.strip()

    if not cleaned_text:
        raise ValueError("Note text cannot be empty")

    embedding = model.encode(cleaned_text).tolist()

    response = (
        sb.table("notes")
        .insert(
            {
                "content": cleaned_text,
                "embedding": embedding,
                "source": source,
                "tags": tags or [],
            }
        )
        .execute()
    )

    if not response.data:
        raise RuntimeError("Supabase did not return the inserted note")

    return response.data[0]


def transcribe_audio(
    audio_path: str,
    language: str | None = "de",
) -> str:
    """Transcribe an audio file through OpenRouter's STT endpoint."""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    with open(audio_path, "rb") as audio_file:
        encoded_audio = base64.b64encode(
            audio_file.read()
        ).decode("utf-8")

    payload: dict[str, Any] = {
        "model": OPENROUTER_STT_MODEL,
        "input_audio": {
            "data": encoded_audio,
            "format": _audio_format(audio_path),
        },
    }

    if language:
        payload["language"] = language

    response = requests.post(
        "https://openrouter.ai/api/v1/audio/transcriptions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Personal Knowledge Agent",
        },
        json=payload,
        timeout=180,
    )

    if response.status_code == 402:
        raise RuntimeError(
            "OpenRouter requires credits for the selected speech-to-text "
            f"model ({OPENROUTER_STT_MODEL}). Choose an available model "
            "or use local Whisper."
        )

    if not response.ok:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text

        raise RuntimeError(
            "OpenRouter transcription failed "
            f"({response.status_code}): {detail}"
        )

    data = response.json()
    transcription = str(data.get("text", "")).strip()

    if not transcription:
        raise RuntimeError(
            "OpenRouter returned no transcription text"
        )

    return transcription


def add_note_from_audio(
    audio_path: str,
    tags: list[str] | None = None,
    language: str | None = "de",
) -> dict:
    text = transcribe_audio(
        audio_path=audio_path,
        language=language,
    )

    return add_note(
        text=text,
        source="audio",
        tags=tags or [],
    )


def search_knowledge(
    query: str,
    top_k: int = 5,
    threshold: float | None = None,
) -> list[dict]:
    cleaned_query = query.strip()

    if not cleaned_query:
        return []

    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    if threshold is None:
        threshold = DEFAULT_SEARCH_THRESHOLD

    embedding = model.encode(cleaned_query)
    query_embedding = _to_pgvector(embedding)

    response = sb.rpc(
        "search_notes_raw",
        {
            "p_query_embedding": query_embedding,
            "p_match_count": int(top_k),
        },
    ).execute()

    results = response.data or []

    return [
        result
        for result in results
        if float(result.get("similarity", -1.0))
        >= float(threshold)
    ]