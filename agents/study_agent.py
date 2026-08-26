# ============================================================
# EIRA — Study Agent
# ============================================================

import sys
sys.path.append("C:/EIRA")

import ollama
from config.settings import MAIN_MODEL, EIRA_BASE_PERSONALITY

STUDY_PROMPT = EIRA_BASE_PERSONALITY + """
You are EIRA's Study Agent.

Your job:
- Explain DSA concepts simply (arrays, trees, graphs, sorting, DP, etc.)
- Help with Java and Python code concepts
- Explain OS, DBMS, CN, Discrete Math topics
- Create quizzes (5 MCQs with answers at end)
- Help with GATE 2028 preparation
- Make revision notes on any topic
- Make him understand everything he asks
- Remind him to study regularly and revise old topics
- Make him confident
- make his study session effective and fun
- make his study plan and schedule

Rules:
- Use simple language + real life analogies
- Always give examples
- Connect to GATE/interview wherever possible
- If quiz requested → give 5 MCQs → answers at end
"""


def study(message: str, history: list = []) -> str:
    messages = [{"role": "system", "content": STUDY_PROMPT}]
    
    for msg in history[-10:]:
        messages.append(msg)
    
    messages.append({"role": "user", "content": message})

    try:
        response = ollama.chat(model=MAIN_MODEL, messages=messages)
        return response["message"]["content"]
    except Exception as e:
        return f"Study Agent error: {str(e)}"


if __name__ == "__main__":
    print("EIRA Study Agent Test")
    print("-" * 40)
    
    tests = [
        "explain binary search tree simply",
        "quiz me on sorting algorithms",
        "what is deadlock in OS"
    ]
    
    for q in tests:
        print(f"\nQ: {q}")
        print(f"A: {study(q)[:300]}...")
        print("-" * 40)