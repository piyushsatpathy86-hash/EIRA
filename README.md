# ✦ EIRA — Enhanced Intelligent Reasoning Assistant

> A local AI Operating System with multi-agent architecture, persistent memory, and real-time web search.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![Groq](https://img.shields.io/badge/Groq-API-orange)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## What is EIRA?

EIRA is a personal AI operating system built for students and developers. She routes your requests to specialized AI agents, remembers past conversations, and searches the web in real time — all running locally on your machine.

---

## Features

- **Multi-Agent System** — 5 specialized agents (Study, Coding, Research, Notes, Planner)
- **Persistent Memory** — ChromaDB vector database remembers past conversations
- **Real-time Web Search** — DuckDuckGo + Tavily integration
- **Session Management** — Full conversation history like ChatGPT
- **4 Themes** — Dark, Light, Teal, Amber
- **Groq + Ollama** — Cloud speed with local fallback
- **FastAPI Backend** — Production-grade REST API
- **Privacy First** — Runs 100% locally

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, Uvicorn |
| AI Models | Groq API, Ollama, Qwen2.5, DeepSeek-Coder |
| Memory | ChromaDB, Sentence-Transformers |
| Search | DuckDuckGo, Tavily |
| Database | SQLite (sessions) |
| Frontend | HTML, CSS, JavaScript |

---

## Agents

| Agent | Capabilities |
|-------|-------------|
| Study | Notes, quizzes, concept explanations — DSA, Java, GATE |
| Coding | Write, debug, review code in any language |
| Research | Web search, summarize, compare technologies |
| Notes | YouTube transcripts to notes, revision sheets |
| Planner | Study plans, project plans, goal tracking |

---

## Project Structure

```
EIRA/
├── agents/
│   ├── coding_agent.py
│   ├── notes_agent.py
│   ├── planner_agent.py
│   ├── research_agent.py
│   └── study_agent.py
├── api/
│   └── main.py
├── config/
│   └── settings.py        # gitignored — add your keys here
├── core/
│   ├── eira.py
│   └── router.py
├── dashboard/
│   └── index.html
├── data/                  # gitignored — memory, sessions, notes
├── tools/
│   ├── desktop_control.py
│   ├── memory_tool.py
│   ├── search_tool.py
│   ├── session_tool.py
│   └── system_control.py
└── README.md
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/piyushsatpathy86-hash/EIRA.git
cd EIRA
```

### 2. Install dependencies
```bash
pip install fastapi uvicorn groq chromadb sentence-transformers ddgs tavily-python
```

### 3. Configure settings
Create `config/settings.py`:
```python
GROQ_API_KEY   = "your_groq_api_key"
TAVILY_API_KEY = "your_tavily_api_key"
GROQ_MODEL     = "openai/gpt-oss-20b"
USE_GROQ       = True
USE_TAVILY     = True
OLLAMA_HOST    = "http://localhost:11434"
API_HOST       = "0.0.0.0"
API_PORT       = 8001
DATA_DIR       = "C:/EIRA/data"
MEMORY_DIR     = "C:/EIRA/data/memory"
```

### 4. Get free API keys
- **Groq** — [console.groq.com](https://console.groq.com) — free, no credit card
- **Tavily** — [tavily.com](https://tavily.com) — free 1000 searches/month

### 5. Run EIRA
```bash
python api/main.py
```

### 6. Open dashboard
Open `dashboard/index.html` in your browser.

---

## How it works

```
You type a message
        ↓
Router detects intent (Study / Coding / Research / Notes / Planner)
        ↓
Memory fetches relevant past context (ChromaDB)
        ↓
Research agent searches web if needed (DuckDuckGo / Tavily)
        ↓
Groq API generates response (Ollama as fallback)
        ↓
Response saved to memory + session (SQLite)
        ↓
EIRA replies
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /chat | Send message to EIRA |
| GET | /sessions | Get all sessions |
| GET | /sessions/{id}/messages | Get session messages |
| POST | /sessions | Create new session |
| DELETE | /sessions/{id} | Delete session |
| GET | / | Health check |

---

## Roadmap

- [x] Multi-agent architecture
- [x] Persistent memory (ChromaDB)
- [x] Web search integration
- [x] Session management
- [x] Custom Web UI with themes
- [ ] Voice input (Whisper)
- [ ] Text-to-speech (Coqui TTS)
- [ ] User authentication
- [ ] Cloud deployment
- [ ] LangChain integration

---

## Built By

**Piyush Satpathy** — 2nd year CSE student
GITA Autonomous College, Bhubaneswar
GitHub: [@piyushsatpathy86-hash](https://github.com/piyushsatpathy86-hash)

---

## License

MIT License — feel free to use and build on this project.