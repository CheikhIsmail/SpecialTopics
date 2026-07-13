import re

def chunk_by_chars(text, size=300, overlap=50):
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start+size])
        start += size - overlap
    return chunks

def chunk_by_sentences(text, max_sentences=3):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [
        " ".join(sentences[i:i+max_sentences])
        for i in range(0, len(sentences), max_sentences)
    ]

def chunk_by_paragraphs(text):
    return [p.strip() for p in text.split("\n\n") if p.strip()]