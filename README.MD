# Final Project – Special Topics in Digital Technologies & Coding

This project implements a **Retrieval-Augmented Generation (RAG)** system that enables an AI agent to retrieve information from a personal knowledge base before answering user questions. The application combines semantic search, vector embeddings, PostgreSQL with pgvector, tool calling, and a Streamlit interface into a complete AI application.

---

# Features

- 🧠 Personal Knowledge Base
- 🔎 Semantic Search using Sentence Transformers
- 🗄️ PostgreSQL + pgvector (Supabase)
- 🚀 FastAPI REST API
- 🤖 AI Agent with Tool Calling (Function Calling)
- 💬 Multi-turn Conversation
- 🎨 Streamlit Chat Interface
- 🎤 Audio Note Upload (Speech-to-Text pipeline implemented)

---

# Project Structure

```text
.
├── agent.py
├── agent_loop.py
├── api.py
├── kb_core.py
├── ingest.py
├── streamlit_agent.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Technologies

- Python
- FastAPI
- Streamlit
- Supabase
- PostgreSQL
- pgvector
- Sentence Transformers
- OpenRouter
- OpenAI SDK
- Pydantic

---

# Installation

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Install the required packages

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
OPENROUTER_API_KEY=your_openrouter_api_key

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key

EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
SEARCH_THRESHOLD=0.0

OPENROUTER_CHAT_MODEL=openai/gpt-4o-mini
OPENROUTER_STT_MODEL=openai/whisper-large-v3
```

---

# Running the Project

## Start the FastAPI API

```bash
uvicorn api:app --reload
```

Swagger documentation

```
http://127.0.0.1:8000/docs
```

---

## Start the Streamlit Application

```bash
streamlit run streamlit_agent.py
```

---

## Run the Agent from the Terminal

```bash
python agent_loop.py
```

Example:

```
User:
What do I know about FastAPI?

↓

Tool:
search_knowledge("FastAPI")

↓

Assistant:
You have saved that FastAPI uses Pydantic for request validation.
```

---

# System Architecture

```text
                User
                  │
                  ▼
         Streamlit Interface
                  │
                  ▼
          AI Agent (GPT-4o-mini)
                  │
          Tool Calling
                  │
                  ▼
        search_knowledge()
                  │
                  ▼
     Supabase PostgreSQL + pgvector
                  │
                  ▼
        Semantic Retrieval
                  │
                  ▼
         Retrieved Notes
                  │
                  ▼
        Grounded AI Response
```

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/notes` | Add a text note |
| POST | `/notes/audio` | Upload an audio note |
| POST | `/search` | Semantic search |

---

# Audio Transcription

The project includes an audio note workflow.

```
Audio
   │
   ▼
Speech-to-Text
   │
   ▼
Embedding
   │
   ▼
Supabase
```

During testing, transcription requests successfully reached the configured speech-to-text provider (OpenRouter). However, the selected Whisper model required API credits, preventing complete end-to-end transcription with the available account.

The implementation is complete, and the application correctly handles transcription requests and provider responses. In a production deployment, this limitation could be resolved by using a speech-to-text provider with available credits or by running a local solution such as Faster-Whisper.

---

# Future Improvements

- User Authentication
- Persistent Conversation History
- Hybrid Search (Keyword + Vector Search)
- Improved Document Chunking
- Local Speech-to-Text
- Automatic Source Citations
- Monitoring & Logging
- Multiple Knowledge Bases

---

# Learning Outcomes

This project demonstrates practical experience with:

- Retrieval-Augmented Generation (RAG)
- Tool Calling / Function Calling
- AI Agents
- Semantic Search
- Vector Databases
- FastAPI
- Streamlit
- PostgreSQL + pgvector
- Supabase Integration
- OpenRouter Integration

---

# Course Information

This project was developed as the final project for the course:

**Special Topics in Digital Technologies & Coding**

Macromedia University of Applied Sciences