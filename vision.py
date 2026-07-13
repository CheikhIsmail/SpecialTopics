import base64
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_image(image_path, question):
    b64 = encode_image(image_path)

    ext = image_path.rsplit(".", 1)[-1].lower()
    media_type = (
        f"image/{ext}"
        if ext in ("png", "jpg", "jpeg", "webp")
        else "image/jpeg"
    )

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{b64}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000,
    )

    return response.choices[0].message.content

answer = analyze_image(
    "screenshot_error.png",
    "What is shown in this image? Explain it briefly."
)

print(answer)