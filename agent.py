import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

OPENROUTER_API_KEY = (
    os.getenv("OPENROUTER_API_KEY")
    or os.getenv("OPENAI_API_KEY")
)

if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY is missing from .env "
        "(OPENAI_API_KEY is also accepted as a fallback)"
    )

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

MODEL = os.getenv(
    "OPENROUTER_CHAT_MODEL",
    "openai/gpt-4o-mini",
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": (
                "Search the personal knowledge base semantically. "
                "Use a concise query containing the main topic and "
                "important keywords. Remove conversational filler."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "A concise semantic search query containing "
                            "the main topic and important technical terms."
                        ),
                    },
                    "top_k": {
                        "type": "integer",
                        "description": (
                            "Maximum number of stored notes to retrieve."
                        ),
                        "default": 4,
                        "minimum": 1,
                        "maximum": 10,
                    },
                },
                "required": ["query"],
            },
        },
    }
]

SYSTEM_PROMPT = """
You are a personal knowledge assistant.

Use the search_knowledge tool before answering questions about information
stored in the user's personal knowledge base.

When searching, use a concise query containing the main topic and important
technical terms. Do not include conversational filler.

Base your answer on the retrieved notes. If the search returns no relevant
notes, clearly state that nothing relevant was found.
"""