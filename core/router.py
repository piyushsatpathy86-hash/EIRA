# ============================================================
# EIRA — Router (Intent Detection)
# ============================================================
# Jo bhi tu type kare → decide karta hai kaunsa agent handle karega

import sys
sys.path.append("C:/EIRA")
from config.settings import MAIN_MODEL, CODER_MODEL, FAST_MODEL

# --- Keyword map ---
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
        "best way", "options", "alternatives", "recommend"
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


def detect_intent(message: str) -> dict:
    message_lower = message.lower()
    scores = {agent: 0 for agent in AGENT_KEYWORDS}

    for agent, keywords in AGENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                scores[agent] += len(keyword.split())

    best_agent = max(scores, key=scores.get)
    best_score = scores[best_agent]

    if best_score == 0:
        best_agent = "general"

    return {
        "agent":      best_agent,
        "model":      AGENT_MODELS.get(best_agent, MAIN_MODEL),
        "confidence": best_score
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
    ]
    print("=" * 50)
    print("EIRA ROUTER — Test")
    print("=" * 50)
    for msg in tests:
        result = detect_intent(msg)
        print(f"Input : {msg[:40]}")
        print(f"Agent : {result['agent'].upper()} | Model: {result['model']}")
        print("-" * 50)