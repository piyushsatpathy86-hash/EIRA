# ============================================================
# EIRA — FastAPI Server (with Sessions)
# ============================================================

import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.eira import chat_with_eira
from core.router import detect_intent
from tools.session_tool import (
    create_session, save_message, get_sessions,
    get_messages, update_session_title, delete_session
)

app = FastAPI(title="EIRA API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
class ChatRequest(BaseModel):
    message: str
    history: list = []
    session_id: str = ""

class ChatResponse(BaseModel):
    response: str
    agent: str
    model: str
    session_id: str

class SessionRequest(BaseModel):
    title: str = "New Chat"

# --- Health check ---
@app.get("/")
async def root():
    return {"status": "EIRA is online! 🔥"}

# --- Main chat ---
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Session handle karo
    session_id = request.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
        create_session(session_id, "New Chat")

    routing = detect_intent(request.message)
    response = chat_with_eira(request.message, request.history)

    # Messages save karo
    save_message(session_id, "user", request.message,
                 routing["agent"], routing["model"])
    save_message(session_id, "assistant", response,
                 routing["agent"], routing["model"])

    # Title update karo — pehle message se
    sessions = get_sessions()
    for s in sessions:
        if s["id"] == session_id and s["title"] == "New Chat":
            title = request.message[:40]
            update_session_title(session_id, title)
            break

    return ChatResponse(
        response=response,
        agent=routing["agent"],
        model=routing["model"],
        session_id=session_id
    )

# --- Session endpoints ---
@app.get("/sessions")
async def list_sessions():
    return get_sessions()

@app.get("/sessions/{session_id}/messages")
async def session_messages(session_id: str):
    return get_messages(session_id)

@app.post("/sessions")
async def new_session(req: SessionRequest):
    session_id = str(uuid.uuid4())
    create_session(session_id, req.title)
    return {"session_id": session_id, "title": req.title}

@app.delete("/sessions/{session_id}")
async def remove_session(session_id: str):
    delete_session(session_id)
    return {"status": "deleted"}


# ============================================================
# --- Server startup (TOP LEVEL — koi function ke andar nahi) ---
# ============================================================
if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    print("=" * 40)
    print("EIRA API Server starting...")
    print(f"Open: http://localhost:{port}")
    print(f"Docs: http://localhost:{port}/docs")
    print("=" * 40)
    uvicorn.run(app, host="0.0.0.0", port=port)