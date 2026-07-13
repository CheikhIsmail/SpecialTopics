from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

response = client.responses.create(
    model="openai/gpt-4o-mini",
    input="Explain in one sentence what a large language model is."
)

print(response.output_text)

usage = response.usage
PRICE_IN = 0.00015 / 1000
PRICE_OUT = 0.00060 / 1000

cost = usage.input_tokens * PRICE_IN + usage.output_tokens * PRICE_OUT

print(f"Tokens: {usage.input_tokens} in / {usage.output_tokens} out")
print(f"Estimated cost: ${cost:.6f}")