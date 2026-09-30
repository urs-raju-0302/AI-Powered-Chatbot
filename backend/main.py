from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

from backend.chatbot import get_response
from backend.database import init_db, save_chat, get_recent_chats

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="AI-Powered Chatbot",
    description="FAQ/customer-support chatbot with NLP, SQLite logging, and a web UI.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/chats")
def chats():
    return {"chats": get_recent_chats(50)}


@app.post("/api/chat")
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    result = get_response(message)
    save_chat(message, result["intent"], result["confidence"], result["response"])

    return {
        "user_message": message,
        **result
    }


# Serve the frontend
app.mount("/", StaticFiles(directory=str(BASE_DIR / "frontend"), html=True), name="frontend")
