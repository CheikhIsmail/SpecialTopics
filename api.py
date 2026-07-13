from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from rag_pipeline import ask
from db import UsageDB
import sqlite3
import hashlib
from datetime import datetime
import tempfile
import os
from kb_core import add_note, add_note_from_audio, search_knowledge

app = FastAPI(title="RAG API", version="1.0")
db = UsageDB()


class NoteRequest(BaseModel):
    text: str
    tags: list[str] = []


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    threshold: float = 0.0


class QuestionRequest(BaseModel):
    question: str
    top_k: Optional[int] = 3


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]
    question: str


class DocumentInfo(BaseModel):
    filename: str
    chunks_added: int
    doc_hash: str
    already_existed: bool


def ensure_indexed_docs_table():
    conn = sqlite3.connect("usage.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS indexed_docs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            doc_hash TEXT UNIQUE NOT NULL,
            chunks INTEGER NOT NULL,
            indexed_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(req: QuestionRequest):
    try:
        answer_text, retrieved = ask(req.question)

        sources = []
        for score, chunk in retrieved:
            sources.append(chunk)

        return AnswerResponse(
            answer=answer_text,
            sources=sources,
            question=req.question
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload", response_model=DocumentInfo)
async def upload_document(file: UploadFile = File(...)):
    try:
        ensure_indexed_docs_table()

        content = (await file.read()).decode("utf-8", errors="ignore")
        doc_hash = hashlib.sha256(content.encode()).hexdigest()

        conn = sqlite3.connect("usage.db")

        existing = conn.execute(
            "SELECT id FROM indexed_docs WHERE doc_hash=?",
            (doc_hash,)
        ).fetchone()

        if existing:
            conn.close()
            return DocumentInfo(
                filename=file.filename,
                chunks_added=0,
                doc_hash=doc_hash,
                already_existed=True
            )

        from chunking import chunk_by_sentences
        chunks = chunk_by_sentences(content, max_sentences=4)

        conn.execute(
            """
            INSERT INTO indexed_docs
            (filename, doc_hash, chunks, indexed_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                file.filename,
                doc_hash,
                len(chunks),
                datetime.utcnow().isoformat()
            )
        )

        conn.commit()
        conn.close()

        return DocumentInfo(
            filename=file.filename,
            chunks_added=len(chunks),
            doc_hash=doc_hash,
            already_existed=False
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents")
async def list_documents():
    try:
        ensure_indexed_docs_table()

        conn = sqlite3.connect("usage.db")
        rows = conn.execute(
            """
            SELECT filename, chunks, indexed_at
            FROM indexed_docs
            ORDER BY indexed_at DESC
            """
        ).fetchall()
        conn.close()

        return [
            {
                "filename": r[0],
                "chunks": r[1],
                "indexed_at": r[2]
            }
            for r in rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_stats():
    try:
        conn = sqlite3.connect("usage.db")
        row = conn.execute(
            "SELECT COUNT(*), ROUND(SUM(cost_usd),6) FROM api_calls"
        ).fetchone()
        conn.close()

        return {
            "total_calls": row[0] or 0,
            "total_cost_usd": row[1] or 0.0
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/notes")
async def create_note(note: NoteRequest):
    try:
        return add_note(note.text, tags=note.tags)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/notes/audio")
async def create_note_from_audio(file: UploadFile = File(...), tags: str = ""):
    try:
        suffix = os.path.splitext(file.filename)[-1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        parsed_tags = [t.strip() for t in tags.split(",") if t.strip()]

        return add_note_from_audio(tmp_path, tags=parsed_tags)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
async def search_notes(req: SearchRequest):
    try:
        results = search_knowledge(
            query=req.query,
            top_k=req.top_k,
            threshold=req.threshold
        )

        return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))