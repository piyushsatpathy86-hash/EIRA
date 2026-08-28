# ============================================================
# EIRA — Router (ML-based Semantic Intent Detection)
# ============================================================
# Uses sentence embeddings for semantic routing + keyword fallback
# Safe version: CPU device, graceful fallback

import sys
import os
sys.path.append("C:/EIRA")
from config.settings import MAIN_MODEL, CODER_MODEL, FAST_MODEL

# --- Keyword map (fallback) ---
AGENT_KEYWORDS = {
    "coding": [
        "code", "debug", "error", "function", "class", "write",
        "fix", "review", "implement", "program", "syntax", "compile",
        "output", "exception", "traceback", "method", "loop", "array",
        "recursion", "algorithm", "leetcode", "java", "python",
        "javascript", "html", "css", "sql", "bug", "crash", "run",
        "execute", "return", "variable", "object", "inheritance",
        "interface", "lambda", "api", "endpoint", "json", "parse"
    ],
    "study": [
        "explain", "teach", "concept", "understand", "what is",
        "how does", "dsa", "data structure", "linked list", "tree",
        "graph", "heap", "sorting", "searching", "bfs", "dfs",
        "dynamic programming", "os", "operating system", "dbms",
        "database", "network", "discrete", "mathematics",
        "gate", "quiz", "test me", "question", "practice", "revise",
        "doubt", "samjhao", "batao", "kya hai", "kaise kaam",
        "college", "semester", "subject", "exam", "syllabus"
    ],
    "notes": [
        "notes", "summarize", "summary", "youtube", "yt", "video",
        "transcript", "revision", "sheet", "key points", "important",
        "bullet", "highlight", "extract", "convert", "make notes",
        "note banao", "summarise", "brief", "tldr", "short"
    ],
    "research": [
        "research", "compare", "difference", "vs", "versus",
        "which is better", "pros cons", "technology", "framework",
        "library", "search", "find", "look up", "information",
        "tell me about", "what are", "latest", "trend",
        "best way", "options", "alternatives", "recommend",
        "link", "playlist", "resource", "resources", "course", "course link"
    ],
    "planner": [
        "plan", "schedule", "goal", "week", "sprint", "track",
        "roadmap", "deadline", "timeline", "study plan", "project plan",
        "task", "todo", "remind", "reminder", "organize", "manage",
        "priority", "milestone", "target", "daily", "monthly",
        "sih", "hackathon", "internship", "preparation",
        "kal karna", "aaj karna", "next week"
    ],
    "desktop": [
        "wallpaper", "download", "open", "launch", "start",
        "screenshot", "file", "folder", "create file",
        "delete", "move", "copy", "rename", "remind me",
        "set reminder", "timer", "alarm", "search web"
    ],
    "camera": [
        "camera", "see me", "dekh", "look at me", "mood",
        "face", "posture", "photo le", "capture",
        "snapshot", "webcam", "kaisa dikh"
    ]
}

# --- Which model handles which agent ---
AGENT_MODELS = {
    "coding":   CODER_MODEL,
    "study":    MAIN_MODEL,
    "notes":    FAST_MODEL,
    "research": MAIN_MODEL,
    "planner":  MAIN_MODEL,
    "desktop":  FAST_MODEL,
    "camera":   MAIN_MODEL,
    "general":  MAIN_MODEL,
}

# --- Agent descriptions for semantic matching ---
AGENT_DESCRIPTIONS = {
    "coding": "Write code, debug errors, fix programs, implement functions, review code, solve programming problems",
    "study": "Explain concepts, teach topics, prepare for exams, understand data structures, learn DSA, answer academic questions",
    "notes": "Create notes, summarize content, extract key points from YouTube videos, make revision sheets",
    "research": "Compare technologies, find information, research topics, search for resources, latest trends",
    "planner": "Create study plans, schedule tasks, set goals, make roadmaps, organize daily routine, plan projects",
    "desktop": "Control desktop, open apps, manage files, set reminders, take screenshots",
    "camera": "Use camera, see user, detect mood, analyze face, check posture",
}

# --- Lazy-load sentence transformer (only when needed) ---
_embedder = None
_agent_embeddings = None
_embedder_failed = False

def _get_embedder():
    global _embedder, _embedder_failed
    if _embedder is not None or _embedder_failed:
        return _embedder
    try:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        print("✅ Semantic router loaded (all-MiniLM-L6-v2)")
    except Exception as e:
        print(f"⚠️  Semantic router unavailable, using keyword fallback: {e}")
        _embedder = False
        _embedder_failed = True
    return _embedder

def _get_agent_embeddings():
    global _agent_embeddings
    if _agent_embeddings is not None:
        return _agent_embeddings
    embedder = _get_embedder()
    if embedder:
        try:
            descriptions = list(AGENT_DESCRIPTIONS.values())
            _agent_embeddings = embedder.encode(descriptions, convert_to_numpy=True)
        except Exception as e:
            print(f"⚠️  Embedding generation failed: {e}")
            _agent_embeddings = False
    else:
        _agent_embeddings = False
    return _agent_embeddings


def _semantic_route(message: str) -> tuple:
    """Returns (agent, confidence) using sentence embeddings"""
    embedder = _get_embedder()
    agent_embeddings = _get_agent_embeddings()
    
    if not embedder or agent_embeddings is False:
        return None, 0
    
    try:
        from sentence_transformers import util
        msg_embedding = embedder.encode([message], convert_to_numpy=True)
        similarities = util.cos_sim(msg_embedding, agent_embeddings)[0]
        
        best_idx = int(similarities.argmax())
        best_score = float(similarities[best_idx])
        best_agent = list(AGENT_DESCRIPTIONS.keys())[best_idx]
        
        return best_agent, best_score
    except Exception as e:
        print(f"Semantic routing error: {e}")
        return None, 0


def _keyword_route(message: str) -> tuple:
    """Returns (agent, confidence) using keyword matching (fallback)"""
    message_lower = message.lower()
    scores = {agent: 0 for agent in AGENT_KEYWORDS}

    for agent, keywords in AGENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                scores[agent] += len(keyword.split())

    best_agent = max(scores, key=scores.get)
    best_score = scores[best_agent]
    
    if best_score == 0:
        return "general", 0
    
    return best_agent, best_score


def detect_intent(message: str) -> dict:
    """
    Route message to the most appropriate agent.
    Uses semantic embeddings first, falls back to keywords.
    """
    # Try semantic routing first (graceful fallback)
    try:
        agent, confidence = _semantic_route(message)
        if agent and confidence > 0.35:
            return {
                "agent":      agent,
                "model":      AGENT_MODELS.get(agent, MAIN_MODEL),
                "confidence": round(confidence, 3),
                "method":     "semantic"
            }
    except Exception as e:
        print(f"Semantic routing failed: {e}")

    # Fallback to keyword routing
    agent, confidence = _keyword_route(message)
    return {
        "agent":      agent,
        "model":      AGENT_MODELS.get(agent, MAIN_MODEL),
        "confidence": confidence,
        "method":     "keyword"
    }


# --- Test karne ke liye ---
if __name__ == "__main__":
    tests = [
        "explain binary search tree",
        "write a java program to reverse a string",
        "make notes from this youtube video",
        "compare react vs vue",
        "create a study plan for gate 2028",
        "change my wallpaper",
        "dekh main kya kar raha hoon",
        "hey what's up",
        "mujhe DSA padhna hai",
        "mera code crash ho raha hai",
    ]
    print("=" * 60)
    print("EIRA ROUTER — Test (Semantic + Keyword Fallback)")
    print("=" * 60)
    for msg in tests:
        result = detect_intent(msg)
        method = result.get('method', 'keyword')
        print(f"Input    : {msg}")
        print(f"Agent    : {result['agent'].upper()} | Model: {result['model']}")
        print(f"Method   : {method} | Confidence: {result['confidence']}")
        print("-" * 60)