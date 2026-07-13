# Unit 01 · Setup & Development Environment

## What I Learned

In this unit, I set up my Python development environment for the course. I installed Python 3.11 and used VSCode as my main editor.

I created a virtual environment using `venv` so that the packages for this project are isolated from other Python projects.

I installed `ipykernel`, which allows me to run Jupyter notebooks directly inside VSCode.

I also learned how to store API keys securely in a `.env` file and load them using `python-dotenv` instead of writing them directly in the source code.

Finally, I initialized a Git repository and connected it to GitHub so I can track changes and store my work online.

---

## Code Example

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found")

print(f"Key loaded: {api_key[:8]}...")
Output
(.venv) (base) PS C:\Users\ismai\OneDrive\Desktop\llmcourse> python secrets_demo.py
Key geladen: sk-or-v1...
Challenges and How I Solved Them

At first, the script could not find my API key. I realized that I misunderstood how os.getenv() works. I initially used the API key itself instead of the variable name OPENAI_API_KEY.

After correcting the code and making sure that the .env file contained the key in the correct format, the script worked successfully.

Reflection

What was new to me was the use of .env files to manage secrets securely. I had not used this approach before.

I still do not fully understand how environment variables behave across different operating systems, especially on Windows.

I used an AI chatbot to help debug the issue. It was useful for identifying the mistake quickly, but I had to test the solution myself to confirm that it worked.


---


# Unit 02 · LLM APIs: From Chat Completions to the Responses API
What I Learned

In this unit, I learned how to send prompts to large language models through an API and receive generated responses.

We first looked at the Chat Completions API to understand the traditional request-response pattern using system and user messages.

We then moved to the Responses API, which is the newer and simpler way to interact with language models.

I also learned how to read token usage and estimate the cost of each API request.

Finally, I gained a basic understanding of Transformer models and how they predict the next token based on the context of previous tokens.

Code Example
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
Output
(.venv) (base) PS C:\Users\ismai\OneDrive\Desktop\llmcourse> python unit02.py
A large language model is an advanced artificial intelligence system designed to understand and generate human-like text by processing vast amounts of language data.
Tokens: 18 in / 27 out
Estimated cost: $0.000019
Challenges and How I Solved Them

At first, I tried to use my OpenRouter API key with the default OpenAI configuration and received authentication errors.

After debugging, I learned that OpenRouter uses a different API endpoint. I fixed the issue by setting base_url="https://openrouter.ai/api/v1" and using the model name openai/gpt-4o-mini.

I also wanted to understand what tokens represent. I learned that they are pieces of text used to measure both the input and the generated output.

Reflection

What was new to me was that every API request has a measurable cost based on token usage. I found it interesting that the example request cost only a tiny fraction of a cent.

I still do not fully understand how text is split into tokens internally or how Transformer attention works in detail.

I used an AI chatbot to understand the difference between the Chat Completions API and the Responses API and to debug the authentication issue. The explanations were helpful, but running the code myself was essential to confirm my understanding.


# Unit 03 · SQLite Logging and Multi-Turn Conversations

## What I Learned

In this unit, I learned how to store API usage data in an SQLite database using Python's built-in `sqlite3` module.

I created a database file called `usage.db` that automatically stores information about every API call, including the timestamp, model name, number of input and output tokens, and the estimated cost.

I also learned that large language models do not have memory by themselves. The model only appears to remember previous messages because the entire conversation history is stored in a `messages` list and sent again with each new request.

Finally, I built a simple console-based chat application where I could ask multiple questions in sequence and receive context-aware responses.

---

## Code Example

```python
messages = [{"role": "system", "content": "You are a precise assistant."}]

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
Output
(.venv) (base) PS C:\Users\ismai\OneDrive\Desktop\llmcourse> python multi_turn.py
You: what is llm
Assistant: LLM typically stands for "Large Language Model."

You: are they interesting
Assistant: Yes, Large Language Models are fascinating because they can understand and generate human-like text and perform many different tasks.

The API calls were also stored in usage.db, which I inspected using DB Browser for SQLite.

Challenges and How I Solved Them

The most important concept for me was understanding that the model does not remember anything automatically. I initially assumed that the conversation history was stored somewhere by the API provider.

After testing the code, I realized that the memory is simulated by appending each message to the messages list and sending the entire list with every request.

I also used DB Browser for SQLite to inspect the contents of the usage.db file and verify that all API calls were being recorded correctly.

| id | ts                         | model              | tokens_in | tokens_out |   cost_usd | note       |
| -- | -------------------------- | ------------------ | --------: | ---------: | ---------: | ---------- |
| 1  | 2026-05-11T14:18:57.422123 | openai/gpt-4o-mini |        21 |        122 | 0.00007635 | multi-turn |
| 2  | 2026-05-11T14:20:05.303834 | openai/gpt-4o-mini |       153 |        258 | 0.00017775 | multi-turn |


Reflection

What was new to me was that conversational memory is not built into the model itself. The model only has access to the information that is included in the current API request.

I also found it very useful to store token usage and costs in a database so that I can monitor my API usage throughout the course.

I still do not fully understand how very long conversations are managed efficiently when the message history becomes large.

I used an AI chatbot to understand how SQLite works and why the model appears to remember previous messages. The explanations were helpful, but running the code and inspecting the database made the concepts much clearer.


# Unit 04 · Regex vs Structured Outputs with Pydantic

## What I Learned

In this unit, I learned that regular expressions are not a reliable way to extract structured information from language model responses.

I first used regex to extract a person's name and age from a text. This worked only because the text followed the exact format expected by the pattern.

When the sentence format changed, the regex no longer worked. This showed me that regex is very fragile and can easily break.

I then used Structured Outputs with Pydantic. I defined a `Person` model with the fields `name`, `age`, `profession`, and `skills`.

The model returned the data in the exact structure I defined, which made the extraction much more reliable.

---

## Code Example

```python
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
Output
python regex_fixed.py
Structured output result:
Maria Müller
34
Software Developer
['Python', 'FastAPI', 'Docker']
Challenges and How I Solved Them

When I ran regex.py, the program successfully extracted the name and age from the text because the sentence matched the expected pattern exactly.

After changing the wording, the regex no longer matched and the extraction failed. This showed me that regular expressions are very sensitive to changes in the text format.

I then ran regex_fixed.py, where I used a Pydantic model to define the fields I wanted to extract. The program returned the name, age, profession, and skills in a structured and reliable way.

Reflection

What was new to me was that instead of manually parsing text with regex, I can define a schema and let the model return the data in that format.

The most interesting part was seeing the difference between the two approaches: regex worked only in a very specific case, while structured outputs returned all fields correctly.

I still do not fully understand how the API guarantees that the response matches the Pydantic model.

I used an AI chatbot to understand the code and to fix the configuration so that regex_fixed.py would run successfully with my OpenRouter setup.


# Unit 05 · Embeddings and Semantic Search

## What I Learned

In this unit, I learned what embeddings are and how they are used to represent the meaning of text as numerical vectors.

I used the `sentence-transformers` library and the model `all-MiniLM-L6-v2`, which runs locally on my computer without requiring a GPU or an API key.

I learned that each sentence is converted into a vector with 384 dimensions. These vectors can then be compared mathematically using cosine similarity.

I also implemented a simple semantic search system. Instead of searching for exact words, the program finds sentences with similar meaning.

In my example, the query "How do you build a web API with Python?" correctly returned the sentence about FastAPI as the most relevant result.

---

## Code Example

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

docs = [
    "Python is an interpreted programming language.",
    "Machine learning requires large amounts of training data.",
    "FastAPI is a modern web framework for Python.",
    "Neural networks learn patterns from examples.",
    "REST APIs communicate over HTTP.",
]

doc_embeddings = model.encode(docs)

print(f"Embedding dimension: {doc_embeddings.shape[1]}")
Output
(.venv) (base) PS C:\Users\ismai\OneDrive\Desktop\llmcourse\unit5> python embeddings.py
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|███████████████████████████████████| 103/103 [00:00<00:00, 2718.71it/s]
Embedding dimension: 384

Semantic Search Results:
[0.666] FastAPI is a modern web framework for Python.
[0.544] Python is an interpreted programming language.
[0.454] REST APIs communicate over HTTP.
Challenges and How I Solved Them

The first time I ran the script, the model was downloaded automatically from Hugging Face. I also received a warning about not having an HF token, but the program still worked correctly.

The most interesting part was seeing that the search returned relevant results even though the query did not use the exact same wording as the documents.

This helped me understand the difference between exact keyword matching and semantic search.

Reflection

What was new to me was that text can be represented as numerical vectors and compared mathematically.

I was surprised that the model ran locally on my CPU and did not require any API calls or payment.

I still do not fully understand what each of the 384 dimensions represents, but I understand that similar meanings produce similar vectors.

I used an AI chatbot to better understand embeddings and cosine similarity. Running the code and seeing the search results made the concept much clearer.


# Unit 06 · RAG Fundamentals: Build It Manually

## What I Learned

In this unit, I built my first Retrieval-Augmented Generation (RAG) system without using any frameworks.

I learned that before a language model can answer questions about a document, the document must first be split into smaller chunks. These chunks are then converted into embeddings so they can be searched semantically.

I also learned that cosine similarity can be used to find the chunks that are most relevant to a user's question.

The most important idea was that the language model does not receive the entire document. Instead, only the most relevant chunks are retrieved and sent to the model together with the question.

This helped me understand how RAG systems can answer questions based on external documents.

---

## Code Example

```python
def retrieve(query, top_k=3):
    q_emb = embed_model.encode([query])[0]

    scores = [
        cosine_similarity(q_emb, c_emb)
        for c_emb in chunk_embeddings
    ]

    top_idx = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]

    return [(scores[i], chunks[i]) for i in top_idx]
Output
Question:
Why is chunking useful in RAG?

Retrieved Chunks:
[0.517] Chunking is important because long documents cannot always fit into the context window of a language model. Splitting text into smaller chunks makes retrieval easier.

[0.488] Overlap helps prevent information loss between chunks. If important information is located at the edge of one chunk, overlap can make sure it also appears in the next chunk.

[0.319] It is fast, easy to use, and supports automatic API documentation. Retrieval-Augmented Generation, also called RAG, combines search with language models.

Answer:
Chunking is useful in RAG because it allows for easier retrieval of information from long documents that may not fit into the context window of a language model. By splitting text into smaller chunks, it enhances the efficiency of the search and retrieval process.
Challenges and How I Solved Them

The first thing I had to understand was why we needed a document file. At first, I did not understand why we created mein_dokument.txt, but I later realized that the RAG system needs a knowledge source to search through.

I also had to understand the retrieval process. After running the code and looking at the similarity scores, I saw that the system retrieved the chunks that were most relevant to the question before sending them to the language model.

Seeing the retrieved chunks helped me understand how RAG works internally.

Reflection

What was new to me was seeing all parts of a RAG system working together without using any framework.

The most interesting part was that the model did not receive the entire document. Instead, the system first searched for the most relevant chunks and only sent those chunks to the model.

I still do not fully understand how to choose the best chunk size and overlap values for different types of documents.

I used an AI chatbot to understand the retrieval process and verify that the retrieved chunks matched the question correctly. Running the code and examining the results made the concept much clearer.


# Unit 07 · Structuring RAG with Haystack

## What I Learned

In this unit, I worked with a RAG pipeline built using Haystack. The goal was to understand how Haystack organizes the same retrieval process that was shown in the previous unit.

I learned that Haystack uses separate components for document splitting, embeddings, document storage, and retrieval. These components can be connected together inside a pipeline.

I also learned that Haystack automatically stores metadata for each document chunk, such as the source file. This can later be used to show where information comes from.

By running the code, I was able to see how a document is split into chunks, embedded, stored, and searched when a question is asked.

---

## Code Example

```python
indexing = Pipeline()

indexing.add_component(
    "splitter",
    DocumentSplitter(
        split_by="sentence",
        split_length=4,
        split_overlap=1
    )
)

indexing.add_component(
    "embedder",
    SentenceTransformersDocumentEmbedder(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
)

indexing.add_component(
    "writer",
    DocumentWriter(document_store=store)
)

indexing.connect("splitter.documents", "embedder.documents")
indexing.connect("embedder.documents", "writer.documents")
Output
Indexed: 3 chunks

Retrieved Chunks:

Source: mein_dokument.txt
Retrieval-Augmented Generation, also called RAG, combines search with language models. First, relevant text chunks are retrieved from documents. Then, the language model answers using only that retrieved context.

Chunking is important because long documents cannot always fit into the context window of a language model.

--------------------------------------------------

Source: mein_dokument.txt
Chunking is important because long documents cannot always fit into the context window of a language model. Splitting text into smaller chunks makes retrieval easier.

Overlap helps prevent information loss between chunks. If important information is located at the edge of one chunk, overlap can make sure it also appears in the next chunk.

--------------------------------------------------

Source: mein_dokument.txt
Python is a popular programming language used for automation, data analysis, machine learning, and web development.

FastAPI is a modern Python web framework for building APIs. It is fast, easy to use, and supports automatic API documentation.

Retrieval-Augmented Generation, also called RAG, combines search with language models.

--------------------------------------------------


The main topics are Retrieval-Augmented Generation (RAG), chunking and its importance in document processing, overlap in chunking, Python as a programming language, and FastAPI as a web framework.
Challenges and How I Solved Them

The indexing part of the Haystack pipeline worked correctly and created three document chunks.

The original example used an OpenAI generator component. Since I have been using OpenRouter in the previous units, I adapted the generation step so that it would work with my API configuration.

After making this change, the retrieval pipeline worked correctly and produced an answer based on the retrieved document chunks.

Reflection

What was new to me was seeing how Haystack organizes a RAG system into separate components and pipelines.

The most interesting part was seeing the retrieved chunks before the final answer was generated. This helped me understand how the retrieval step works.

I still do not fully understand all Haystack components and configuration options, but I understand the general pipeline structure.

I used an AI chatbot to understand the code and adapt the generation step to my OpenRouter setup. Running the code and examining the retrieved chunks helped me understand the process much better.


# Unit 08 · FastAPI Backend for RAG

## What I Learned

In this unit, I learned how to expose a RAG pipeline through a REST API using FastAPI.

The goal was to make the RAG system accessible through HTTP endpoints instead of running it only from the command line. This allows other applications to communicate with the RAG pipeline.

I learned how to create API endpoints using FastAPI and how to define request and response structures using Pydantic models.

The API included three endpoints:

- `/ask` for asking questions to the RAG system
- `/stats` for viewing usage statistics stored in the database
- `/health` for checking whether the API is running

I also learned that FastAPI automatically generates interactive API documentation through Swagger UI.

---

## Code Example

```python
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(req: QuestionRequest):

    answer_text, retrieved = ask(req.question)

    sources = []
    for score, chunk in retrieved:
        sources.append(chunk)

    return AnswerResponse(
        answer=answer_text,
        sources=sources,
        question=req.question
    )
Output
Health Endpoint
{
  "status": "ok"
}
Statistics Endpoint
{
  "total_calls": 2,
  "total_cost_usd": 0.000254
}
API Documentation
http://127.0.0.1:8000/docs
Challenges and How I Solved Them

Initially, the API failed to start because Python could not import the RAG pipeline correctly.

I also encountered an issue where the /ask endpoint returned a 500 Internal Server Error. After debugging, I discovered that the API was returning tuples while the Pydantic response model expected strings.

By adjusting the response format and extracting only the required values, the endpoint worked correctly.

Another issue occurred when I tried to start the application using:

python api.py

I learned that FastAPI applications should be started using Uvicorn:

uvicorn api:app --reload

After making these changes, all endpoints worked successfully.

Reflection

What was new to me was learning how a machine learning application can be exposed as a web API.

The most interesting part was using Swagger UI to test the API directly from the browser.

I also learned that Pydantic validates API responses and can detect data type mismatches automatically.

I used an AI chatbot to help debug the import issues and the response validation errors. Testing the endpoints manually helped me better understand how FastAPI applications work.


This matches the style of Units 1–9: what you learned, what actually happened during execution, the errors you encountered, and how you fixed them.


# Unit 09 · Deployment on Render & Streamlit Frontend

## What I Learned

In this unit, I learned how to separate a RAG application into a backend and a frontend.

The backend was the FastAPI application created in the previous unit. The frontend was built using Streamlit, which allows creating web interfaces using only Python.

I learned that the frontend communicates with the backend by sending HTTP requests to API endpoints. The backend processes the request, runs the RAG pipeline, and returns a response to the frontend.

I also learned the basic deployment workflow using GitHub and Render. Render can automatically deploy a Python application and expose it as a web service.

Another important concept was understanding the architecture of a modern AI application, where the user interface, backend logic, and language model are separated into different layers.

---

## Code Example

```python
resp = requests.post(
    f"{BACKEND_URL}/ask",
    json={
        "question": prompt,
        "top_k": 3
    },
    timeout=90
)

answer = resp.json()["answer"]
Output
Question
Why is chunking useful in RAG?
Response
Chunking is useful in RAG because it allows for the management of long documents that may not fit into the context window of a language model, making retrieval easier.
Challenges and How I Solved Them

Initially, the Streamlit application displayed the following error:

Fehler: Expecting value: line 1 column 1 (char 0)

The issue was caused by the FastAPI /ask endpoint returning an error instead of valid JSON data.

After debugging the API and fixing the response format, the frontend was able to communicate correctly with the backend.

I also learned that FastAPI applications should be started with:

uvicorn api:app --reload

instead of running the Python file directly.

Reflection

What was new to me was seeing a complete application with a frontend and backend working together.

The most interesting part was sending a question from Streamlit and receiving an answer generated through the RAG pipeline.

I still do not fully understand all deployment settings used by Render, especially environment variables and production configuration.

I used an AI chatbot to help debug the communication between Streamlit and FastAPI. The debugging process helped me better understand how API-based applications are structured.


This fits the style of your previous logs: what happened, what you ran, the actual error you got, how you fixed it, and the final working output.


# Unit 10 · Evaluation: Testing the System Systematically

## What I Learned

In this unit, I learned that having a working RAG system does not necessarily mean that the system performs well. It is important to evaluate the quality of the answers instead of simply checking whether the system produces a response.

I learned how to create test cases containing questions, expected keywords, and expected sources. The evaluation script then compares the generated answers against these expectations.

The evaluation focused on three aspects:

- completeness of the answer
- correctness of the answer
- retrieval of the expected source

I also learned that evaluation helps identify weaknesses in the system and provides ideas for future improvements.

---

## Code Example

```python
found = [
    kw for kw in tc.expected_keywords
    if kw.lower() in answer
]

missing = [
    kw for kw in tc.expected_keywords
    if kw.lower() not in answer
]

src_ok = (
    tc.should_retrieve_from.lower() in sources
    if tc.should_retrieve_from
    else True
)
Output
(.venv) (base) PS C:\Users\ismai\OneDrive\Desktop\llmcourse> python eval.py

Antwort: Die Hauptthemen des Dokuments sind die Verwendung von Python für Automatisierung, Datenanalyse, maschinelles Lernen und Webentwicklung sowie die Beschreibung von FastAPI als modernen Python-Webframework für den Aufbau von APIs. Zudem werden Aspekte wie die Wichtigkeit von Überlappung zur Vermeidung von Informationsverlust und das Konzept Retrieval-Augmented Generation (RAG) erwähnt.

Quellen:
['Python is a popular programming language used for automation, data analysis, machine learning, and web development. FastAPI is a modern Python web framework for building APIs.',
'Overlap helps prevent information loss between chunks. If important information is located at the edge of one chunk, overlap can make sure it also appears in the next chunk.',
'It is fast, easy to use, and supports automatic API documentation. Retrieval-Augmented Generation, also called RAG, combines search with language models.']

❌ [35%] Was ist die Hauptthese?
   Fehlende Keywords: ['Argument']

❌ [35%] Welche Methoden werden beschrieben?
   Fehlende Keywords: ['Ansatz']

⚠️ [53%] Telefonnummer des Autors?
   Fehlende Keywords: ['nicht', 'unbekannt']

Durchschnitt: 41%
Challenges and How I Solved Them

The evaluation produced a relatively low average score of 41%. This showed that even though the RAG system was functioning, the answers did not always contain the expected keywords.

The most interesting result was that the system struggled with some evaluation questions because the required information was not actually present in the document. This demonstrated that evaluation depends heavily on the quality of the test cases.

By examining the missing keywords, I was able to identify weaknesses in the retrieval and answer generation process.

Reflection

What was new to me was learning that AI systems should be evaluated systematically instead of relying on the impression that they "seem to work."

The most interesting part was seeing a numerical score for the performance of the RAG system and identifying missing information in the generated answers.

I still do not fully understand how large-scale evaluation frameworks work, but I now understand the importance of testing and benchmarking.

I used an AI chatbot to understand the evaluation script and the scoring mechanism. Running the evaluation myself helped me understand why testing is an important part of AI system development.

# Unit 11 · Document Upload & Re-indexing

## What I Learned

In this unit, I learned how to extend the RAG system so that new documents can be added while the application is running.

Instead of indexing documents only when the backend starts, I added an upload endpoint that accepts a text document, splits it into chunks, and stores information about the document in the database.

I also learned about incremental indexing. Rather than rebuilding the entire index whenever a new document is uploaded, only the new document is processed.

Another important concept was duplicate detection. A SHA-256 hash is generated for every uploaded document. If the same document is uploaded again, the system detects that it already exists and avoids indexing it a second time.

Finally, I learned how metadata can be stored for every indexed document, including the filename, number of chunks, and indexing date.

---

## Code Example

```python
doc_hash = hashlib.sha256(content.encode()).hexdigest()

if conn.execute(
    "SELECT id FROM indexed_docs WHERE doc_hash=?",
    (doc_hash,)
).fetchone():

    return DocumentInfo(
        filename=file.filename,
        chunks_added=0,
        doc_hash=doc_hash,
        already_existed=True
    )
Output
Uploading a New Document
Filename: new_document.txt
Chunks Added: 1
Already Existed: False
Listing Indexed Documents
Filename: new_document.txt
Chunks: 1
Indexed At: 2026-06-03 ...
Uploading the Same Document Again
Filename: new_document.txt
Chunks Added: 0
Already Existed: True


Challenges and How I Solved Them

The main challenge was understanding how to avoid indexing the same document multiple times.

I learned that generating a SHA-256 hash from the document content provides a unique identifier. Before adding a new document, the backend checks whether the hash already exists in the database.

I also extended the SQLite database by creating a new table to store indexed document information. After testing the API through Swagger, I confirmed that uploading new documents and detecting duplicates worked correctly.

Reflection

What was new to me was learning how a RAG system can be extended while it is already running without rebuilding the entire index.

The most interesting part was seeing duplicate detection work automatically using document hashes.

I still do not fully understand how production systems update vector databases incrementally, but I now understand the basic workflow.

I used an AI chatbot to understand incremental indexing and document hashing. Running the upload endpoint and testing duplicate uploads helped me understand how document management works in a RAG application.


# Unit 12 · Multimodal AI with Vision Models

## What I Learned

In this unit, I learned that large language models can process both text and images. Instead of only sending a text prompt, an image can also be included in the API request.

I learned how to convert an image into a Base64 string and include it in the request using the `image_url` field. The model then analyzes the image and answers the accompanying question.

Another important concept was that the image is processed by the model running on the API provider's servers, so no local GPU is required.

Finally, I learned that multimodal models can be used for practical tasks such as explaining screenshots, analyzing error messages, describing diagrams, and extracting information from images.

---

## Code Example

```python
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
    ]
)
```

---

## Output

### Question

```text
What is shown in this image? Explain it briefly.
```

### Response

```text
The image appears to be a promotional graphic for an event hosted by Macromedia University of Applied Sciences, focusing on "Pioneering AI-driven Transformation." It likely takes place at their Berlin campus on June 3rd. The graphic features a modern, stylized individual, possibly symbolizing innovation and technology, which aligns with the theme of AI transformation. There are also several logos from sponsors or partners, indicating collaboration in the event.
```

---

## Challenges and How I Solved Them

At first, I needed to understand how images are sent through the API. I learned that the image must first be encoded into Base64 format before being included in the request.

Since I use OpenRouter instead of the default OpenAI endpoint, I also updated the client configuration by specifying the correct `base_url`. After making these changes, the model successfully analyzed the uploaded image.

---

## Reflection

What was new to me was that the same language model can understand both text and images through a single API request.

The most interesting part was seeing the model correctly describe the event poster and identify its main content.

I still do not fully understand how vision models internally combine image and text information, but I now understand how to use them through the API.

I used an AI chatbot to understand how Base64 image encoding works and how to adapt the code for OpenRouter. Running the example myself helped me understand how multimodal AI applications work.


# Unit 13 · OpenRouter: Provider-Independent Architecture

## What I Learned

In this unit, I learned that OpenRouter provides a single API interface for accessing language models from different providers. Instead of changing the application code, only the `base_url` and model name need to be updated.

I learned that the same program can communicate with models from OpenAI, Anthropic, Meta, and other providers while using the same API structure.

Another important concept was benchmarking. By sending the same question to different models, it is possible to compare response quality, latency, token usage, and cost.

I also learned that OpenRouter makes it easy to experiment with multiple models without rewriting the application.

---

## Code Example

```python
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": question
        }
    ]
)
```

---

## Output

```text
(.venv) (base) PS C:\Users\ismai\OneDrive\Desktop\llmcourse> python benchmark.py

gpt-4o-mini
Latency: 10.07s
Tokens: 16 in / 594 out

Chunking and embeddings are two different concepts commonly used in natural language processing (NLP) and machine learning...
```

While testing additional models, OpenRouter returned the following error:

```text
Error code: 402

This request requires more credits...
```

The benchmark worked successfully with GPT-4o Mini, but additional models could not be tested because the available OpenRouter credits were insufficient.

---

## Challenges and How I Solved Them

The benchmark successfully connected to OpenRouter and generated a response using GPT-4o Mini.

When I attempted to benchmark additional models, OpenRouter returned a **402** error because my account did not have enough credits for the requested response size.

Although I could not compare every model, I successfully verified that changing only the model name allows the same application to work with different providers.

---

## Reflection

What was new to me was that different AI providers can be accessed through the same OpenAI-compatible API.

The most interesting part was seeing that only a few configuration changes are required to switch between models.

I still do not fully understand the pricing differences between all providers, but I now understand how OpenRouter simplifies working with multiple models.

I used an AI chatbot to understand the OpenRouter architecture and to troubleshoot the benchmark script. Running the benchmark myself helped me understand how provider-independent AI applications are built.



# Unit 14 · Personal Knowledge Base with Supabase
What I Learned

In this unit, I built a personal knowledge base using Supabase and PostgreSQL with the pgvector extension. Instead of storing embeddings only in memory, notes are now stored permanently in a database.

I learned how to generate embeddings using sentence-transformers, store them together with the note, and retrieve the most relevant notes using cosine similarity directly inside PostgreSQL.

I also integrated the knowledge base into my existing FastAPI application by creating three endpoints: /notes, /notes/audio, and /search.

Code Example
def add_note(text, source="manual", tags=None):
    embedding = model.encode(text).tolist()

    row = sb.table("notes").insert({
        "content": text,
        "embedding": embedding,
        "source": source,
        "tags": tags or [],
    }).execute()

    return row.data[0]
Output
POST /notes
Status: 200 OK

POST /search
Status: 200 OK

Swagger Endpoints:
/notes
/notes/audio
/search

The notes were successfully stored in Supabase and retrieved using semantic search.

Challenges and How I Solved Them

At first, my search returned no results. After debugging, I discovered that the similarity threshold was too high for my test query. Lowering the threshold and testing with matching notes confirmed that the semantic search was working correctly.

I also mistakenly used the REST endpoint instead of the Supabase project URL. After correcting the URL and using the secret API key, the connection worked successfully.

Reflection

What was new to me was learning how pgvector enables semantic search directly inside PostgreSQL instead of comparing embeddings manually in Python.

The most interesting part was connecting Supabase with FastAPI and testing the API through Swagger.

I used an AI chatbot to understand the Supabase setup, debug the search functionality, and integrate the new endpoints into my existing RAG application.



### Unit 15 – Final Project Part 2: Agent with Knowledge Base Access
Learning Goal

The objective of this unit was to build an intelligent agent capable of interacting with the semantic knowledge base developed in Unit 14. Instead of relying solely on its internal knowledge, the agent can decide when external information is required and automatically retrieve relevant notes from the knowledge base before generating a response.

This unit introduced the concept of tool use (function calling), one of the key features of modern Large Language Models (LLMs). The final system combined an LLM, semantic search with pgvector, a PostgreSQL database hosted on Supabase, and a Streamlit web interface into a complete Retrieval-Augmented Generation (RAG) application.

1. Tool Calling and Function Calling

Modern LLMs are capable of calling external functions when additional information is needed.

Instead of immediately answering a question, the model receives a list of available tools. When a question requires external knowledge, it generates a structured tool call rather than a normal text response.

In this project, the agent had access to one tool:

search_knowledge(query, top_k)

When the user asks a question related to stored knowledge, the model automatically generates a tool call.

Example:

User:
What do I know about FastAPI?

↓

Tool Call

search_knowledge(
    query="FastAPI",
    top_k=4
)

The application executes the tool, retrieves the most relevant notes from Supabase, and sends the results back to the language model. The model then generates a grounded answer based on the retrieved information.

2. Agent Architecture

The complete system consists of several connected components.

User
   │
   ▼
Streamlit UI
   │
   ▼
LLM Agent (GPT-4o-mini)
   │
Tool Calling
   │
   ▼
search_knowledge()
   │
   ▼
Supabase PostgreSQL + pgvector
   │
Retrieved Notes
   │
   ▼
LLM
   │
   ▼
Final Answer

The language model never accesses the database directly. Instead, it requests information through the search tool whenever additional context is required.

3. Multi-turn Agent Loop

The agent was implemented as a multi-turn conversation system.

The conversation history is stored after every interaction and sent back to the model together with the current user question.

The agent loop consists of four steps:

Receive the user's question.
Decide whether a tool is required.
Execute the tool if necessary.
Generate the final answer using the retrieved information.

This architecture allows the model to maintain context across multiple conversation turns while grounding its responses in the user's personal knowledge base.

4. Streamlit User Interface

A Streamlit application was developed to provide an interactive interface for the agent.

The interface contains three main features:

Manual note creation
Audio note upload
Conversational chat with the knowledge base

Users can add notes, upload audio recordings, and ask questions using natural language. The chat interface communicates with the agent, which automatically decides when to query the knowledge base.

5. Semantic Retrieval

The semantic search implementation from Unit 14 was reused.

When a user submits a question:

The query is converted into an embedding using SentenceTransformers.
The embedding is compared with all stored note embeddings using pgvector.
The most similar notes are returned.
The retrieved notes are passed to the language model.
The language model generates the final grounded answer.

Example:

User:
What do I know about FastAPI?

↓

search_knowledge("FastAPI")

↓

Retrieved Note

FastAPI nutzt Pydantic für Request-Validierung.

↓

Assistant

You have saved that FastAPI uses Pydantic for request validation.
6. Debugging Process

During implementation, several issues had to be resolved before the system worked correctly.

The most significant problems included:

Missing environment variables after the .env file was accidentally overwritten.
Duplicate search implementations causing inconsistent retrieval.
The language model initially generated long conversational search queries instead of concise semantic keywords. This was improved by refining the tool description and system prompt.
The pgvector retrieval initially returned no results because an approximate vector index was being used on a very small dataset. Switching to exact vector search resolved the issue.

After debugging, the complete retrieval pipeline functioned correctly and the agent successfully answered questions using the stored notes.

7. Audio Transcription

As part of this project, an audio note feature was implemented in the Streamlit application. The intended workflow was to upload an audio recording, transcribe it using a Whisper speech-to-text model, generate an embedding from the transcription, and store the resulting note in the Supabase knowledge base.

The application successfully handled audio uploads and sent transcription requests to the configured provider (OpenRouter). However, the selected speech-to-text model (openai/whisper-large-v3) required paid API credits. Since no credits were available, the provider rejected the transcription request with a payment-related error.

As a result, the complete audio ingestion pipeline could not be fully demonstrated during testing. Nevertheless, the implementation of the feature was completed, and the application correctly handled the provider's response without crashing. The remaining components of the system—including semantic search, tool calling, the multi-turn agent loop, and the Streamlit interface—were successfully implemented and tested.

In a production environment, this limitation could be resolved by using an OpenAI API key with billing enabled, selecting another speech-to-text provider, or deploying a local transcription solution such as Faster-Whisper.

8. Production Improvements

Although the application is fully functional, several improvements would be necessary before deploying it in production.

Possible enhancements include:

User authentication and authorization
Rate limiting
Persistent conversation history
Improved document chunking strategies
Hybrid retrieval combining keyword and vector search
Model switching through OpenRouter
Monitoring and logging
Local speech-to-text using Faster-Whisper
Automatic source citation for retrieved notes
Reflection

This unit combined all previous work into a complete AI application. The most important concept I learned was function calling, where the language model decides autonomously when external knowledge is needed instead of relying only on its internal parameters. I also gained valuable experience debugging a complete RAG pipeline, including issues related to embeddings, pgvector retrieval, SQL functions, and agent behavior. I used ChatGPT mainly as a debugging and learning assistant to better understand the architecture, identify implementation problems, and discuss possible solutions while building the system myself. Although the speech-to-text functionality could not be fully demonstrated because the selected OpenRouter model required paid credits, the core objectives of the unit—tool calling, semantic retrieval, and the complete agent workflow—were successfully achieved.