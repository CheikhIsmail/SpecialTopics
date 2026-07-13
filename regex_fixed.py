from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

class Person(BaseModel):
    name: str
    age: int
    profession: str
    skills: list[str]

response = client.responses.parse(
    model="openai/gpt-4o-mini",
    input=[
        {
            "role": "system",
            "content": "Extract the following information exactly as structured data."
        },
        {
            "role": "user",
            "content": (
                "Maria Müller (34) is a software developer. "
                "She knows Python, FastAPI and Docker."
            )
        }
    ],
    text_format=Person,
)

person = response.output_parsed

print("Structured output result:")
print(person.name)
print(person.age)
print(person.profession)
print(person.skills)