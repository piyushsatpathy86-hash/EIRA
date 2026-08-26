# ============================================================
# EIRA — FastAPI Server (with Firebase Auth + Per-User Sessions)
# ============================================================

import sys
sys.path.append("C:/EIRA")

import os
import uuid
from fastapi import FastAPI, Request
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

async def get_user_id(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return "anonymous"
    token = auth.split("Bearer ")[1]
    try:
        import firebase_admin
        from firebase_admin import auth as fb_auth, credentials
        if not firebase_admin._apps:
            cred_json = os.getenv("FIREBASE_CREDENTIALS")
            if cred_json:
                import json
                cred = credentials.Certificate(json.loads(cred_json))
                firebase_admin.initialize_app(cred)
            else:
                return "anonymous"
        decoded = fb_auth.verify_id_token(token)
        return decoded["uid"]
    except Exception as e:
        print(f"Auth error: {e}")
        return "anonymous"

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

@app.get("/")
async def root():
    return {"status": "EIRA is online! 🔥"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest):
    user_id = await get_user_id(request)
    session_id = body.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
        create_session(session_id, "New Chat", user_id)

    routing = detect_intent(body.message)
    response = chat_with_eira(body.message, body.history)

    save_message(session_id, "user", body.message,
                 routing["agent"], routing["model"])
    save_message(session_id, "assistant", response,
                 routing["agent"], routing["model"])

    sessions = get_sessions(user_id)
    for s in sessions:
        if s["id"] == session_id and s["title"] == "New Chat":
            update_session_title(session_id, body.message[:40])
            break

    return ChatResponse(
        response=response,
        agent=routing["agent"],
        model=routing["model"],
        session_id=session_id
    )

@app.get("/sessions")
async def list_sessions(request: Request):
    user_id = await get_user_id(request)
    return get_sessions(user_id)

@app.get("/sessions/{session_id}/messages")
async def session_messages(session_id: str):
    return get_messages(session_id)

@app.post("/sessions")
async def new_session(request: Request, req: SessionRequest):
    user_id = await get_user_id(request)
    session_id = str(uuid.uuid4())
    create_session(session_id, req.title, user_id)
    return {"session_id": session_id, "title": req.title}

@app.delete("/sessions/{session_id}")
async def remove_session(session_id: str, request: Request):
    user_id = await get_user_id(request)
    delete_session(session_id, user_id)
    return {"status": "deleted"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    print("=" * 40)
    print("EIRA API Server starting...")
    print(f"Open: http://localhost:{port}")
    print(f"Docs: http://localhost:{port}/docs")
    print("=" * 40)
    uvicorn.run(app, host="0.0.0.0", port=port)