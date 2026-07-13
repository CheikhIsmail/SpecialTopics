import json

from agent import client, TOOLS, SYSTEM_PROMPT, MODEL
from kb_core import search_knowledge


def run_agent(user_question: str, history: list[dict] | None = None):
    if history is None:
        history = []

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        *history,
        {
            "role": "user",
            "content": user_question
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message

    if assistant_message.tool_calls:
        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:
            if tool_call.function.name != "search_knowledge":
                continue

            try:
                arguments = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    "The model returned invalid search tool arguments."
                ) from exc

            query = arguments.get("query", "").strip()
            top_k = arguments.get("top_k", 4)

            if not query:
                results = []
            else:
                results = search_knowledge(
                    query=query,
                    top_k=top_k
                )

            print(
                f"\nTool called: search_knowledge({query!r}, top_k={top_k})"
            )
            print("\nTool results:")
            print(
                json.dumps(
                    results,
                    indent=2,
                    ensure_ascii=False,
                    default=str
                )
            )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    results,
                    ensure_ascii=False,
                    default=str
                )
            })

        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        answer = final_response.choices[0].message.content
    else:
        answer = assistant_message.content

    updated_history = [
        *history,
        {
            "role": "user",
            "content": user_question
        },
        {
            "role": "assistant",
            "content": answer
        }
    ]

    return answer, updated_history


if __name__ == "__main__":
    answer, conversation_history = run_agent(
        "What have I saved about FastAPI?"
    )

    print("\nAnswer:")
    print(answer)