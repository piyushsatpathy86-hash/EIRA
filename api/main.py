# ============================================================
# EIRA — FastAPI Server (with Firebase Auth + Per-User Sessions)
# ============================================================

import sys
sys.path.append("C:/EIRA")

import os
import uuid
import tempfile
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.eira import chat_with_eira
from core.router import detect_intent
from tools.session_tool import (
    create_session, save_message, get_sessions,
    get_messages, update_session_title, delete_session
)
from tools.file_tool import process_uploaded_file

app = FastAPI(title="EIRA API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


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

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Accepts a file, extracts its content (text or vision description),
    and returns it. The frontend attaches this content to the next
    chat message it sends — the file itself is never stored long-term.
    """
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        return {"error": "File too large. Max size is 10MB."}

    suffix = os.path.splitext(file.filename)[1]
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        result = process_uploaded_file(tmp_path, file.filename)

    except Exception as e:
        return {"error": f"Could not process file: {str(e)}"}
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    if result["type"] == "unsupported":
        return {"error": "That file type isn't supported yet."}
    if result["type"] == "error":
        return {"error": f"Could not read file: {result['content']}"}

    return {
        "filename": file.filename,
        "type": result["type"],
        "content": result["content"][:8000]  # cap to keep prompts reasonable
    }

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