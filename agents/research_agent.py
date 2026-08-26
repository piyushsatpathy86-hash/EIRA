# ============================================================
# EIRA — Research Agent (with Web Search)
# ============================================================

import sys
sys.path.append("C:/EIRA")

import ollama
from config.settings import MAIN_MODEL, EIRA_BASE_PERSONALITY
from tools.search_tool import search

RESEARCH_PROMPT = EIRA_BASE_PERSONALITY + """
You are EIRA's Research Agent.

Your job:
- Research any topic deeply using web search results provided
- Compare technologies (React vs Vue, SQL vs NoSQL etc)
- Summarize complex topics simply
- Give recommendations with reasons

Format always:
Overview → Key Points → Pros/Cons → Recommendation

Rules:
- Be objective and factual
- Give practical examples
- Keep it concise but complete
- Always use the web search results provided to give accurate answers
"""


def research(message: str, history: list = []) -> str:
    
    # Web search pehle
    print(f"[EIRA] Searching web for: {message}")
    search_results = search(message, max_results=5)
    
    # Search results ko message mein add karo
    enhanced_message = f"""User question: {message}

Web search results:
{search_results}

Based on these results, give a clear and helpful answer."""

    messages = [{"role": "system", "content": RESEARCH_PROMPT}]
    
    for msg in history[-10:]:
        messages.append(msg)
    
    messages.append({"role": "user", "content": enhanced_message})

    try:
        response = ollama.chat(model=MAIN_MODEL, messages=messages)
        return response["message"]["content"]
    except Exception as e:
        # Fallback — sirf search results return karo
        return f"Here's what I found:\n\n{search_results}"


if __name__ == "__main__":
    print("EIRA Research Agent Test")
    print("-" * 40)
    
    tests = [
        "compare react vs vue for beginners",
        "latest AI models in 2026",
    ]
    
    for q in tests:
        print(f"\nQ: {q}")
        print(f"A: {research(q)[:300]}...")
        print("-" * 40)