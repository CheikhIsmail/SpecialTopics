import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")   # or OPENROUTER_API_KEY if that's what you use
)

MODELS = {
    "gpt-4o-mini": "openai/gpt-4o-mini",
    "claude-haiku": "anthropic/claude-haiku-4.5",
    "llama-3-8b": "meta-llama/llama-3-8b-instruct:free",
}

question = "Explain the difference between chunking and embeddings."

for name, model in MODELS.items():

    start = time.time()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        extra_headers={
            "X-Title": "LLM Course"
        }
    )

    latency = round(time.time() - start, 2)

    print(f"\n{name}")
    print(f"Latency: {latency}s")
    print(
        f"Tokens: {response.usage.prompt_tokens} in / "
        f"{response.usage.completion_tokens} out"
    )
    print(response.choices[0].message.content)