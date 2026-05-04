from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.document_processing.pdf_loader import load_pdf
from backend.document_processing.chunking import chunk_text
from backend.embeddings.embeddings import generate_embeddings
from backend.vector_store.chroma_store import store_chunks
from backend.rag.retriever import retrieve
from backend.rag.generator import generate_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure uploads folder exists
os.makedirs("uploads", exist_ok=True)


# ✅ UPLOAD PDF API
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    print("Loading PDF...")
    text = load_pdf(file_path)

    print("Chunking...")
    chunks = chunk_text(text)

    print("Generating embeddings...")
    embeddings = generate_embeddings(chunks)

    print("Storing in DB...")
    store_chunks(chunks, embeddings)

    return {"message": "PDF uploaded and processed successfully"}


# ✅ ASK QUESTION API
@app.post("/ask")
async def ask_question(question: str):
    query_embedding = generate_embeddings([question])[0]
    retrieved_docs = retrieve(query_embedding)
    answer = generate_answer(retrieved_docs, question)

    return {
        "answer": answer,
        "sources": retrieved_docs
    }