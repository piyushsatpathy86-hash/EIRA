# ============================================================
# EIRA — Coding Agent
# ============================================================

import sys
sys.path.append("C:/EIRA")

import ollama
from config.settings import CODER_MODEL, EIRA_BASE_PERSONALITY

CODING_PROMPT = EIRA_BASE_PERSONALITY + """
You are EIRA's Coding Agent.

Your job:
- Write clean, working code with comments
- Debug errors — explain WHY error happened
- Review code — give improvements
- Explain code line by line if asked
- Prefer Java and Python unless specified

Rules:
- Always give complete working code
- Add comments explaining logic
- If bug found → show fixed code + explain the fix
- For DSA problems → give brute force first, then optimal
"""


def code(message: str, history: list = []) -> str:
    messages = [{"role": "system", "content": CODING_PROMPT}]
    
    for msg in history[-10:]:
        messages.append(msg)
    
    messages.append({"role": "user", "content": message})

    try:
        response = ollama.chat(model=CODER_MODEL, messages=messages)
        return response["message"]["content"]
    except Exception as e:
        return f"Coding Agent error: {str(e)}"


if __name__ == "__main__":
    print("EIRA Coding Agent Test")
    print("-" * 40)
    
    tests = [
        "write a java program to reverse a linked list",
        "debug this: for i in range(10) print(i)",
    ]
    
    for q in tests:
        print(f"\nQ: {q}")
        print(f"A: {code(q)[:300]}...")
        print("-" * 40)