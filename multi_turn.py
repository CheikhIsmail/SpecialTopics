from openai import OpenAI
from dotenv import load_dotenv
import os
from db import UsageDB

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

db = UsageDB()

messages = [
    {"role": "system", "content": "You are a precise assistant."}
]

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ("exit", "quit"):
        break

    messages.append({"role": "user", "content": user_input})

    resp = client.responses.create(
        model="openai/gpt-4o-mini",
        input=messages
    )

    reply = resp.output_text
    messages.append({"role": "assistant", "content": reply})

    print(f"Assistant: {reply}\n")

    usage = resp.usage
    cost = (
        usage.input_tokens * 0.00000015
        + usage.output_tokens * 0.00000060
    )

    db.log(
        "openai/gpt-4o-mini",
        usage.input_tokens,
        usage.output_tokens,
        cost,
        note="multi-turn"
    )

print("\n--- Statistics ---")
db.stats()