# ============================================================
# EIRA — Planner Agent
# ============================================================

import sys
sys.path.append("C:/EIRA")

import ollama
import os
from datetime import datetime
from config.settings import MAIN_MODEL, PLANS_DIR, EIRA_BASE_PERSONALITY

PLANNER_PROMPT = EIRA_BASE_PERSONALITY + """
You are EIRA's Planner Agent.

You know about Piyush:
- 2nd year B.Tech CS student
- Goals: SIH 2026 hackathon, internship by 3rd year, GATE 2028
- Team Lead of Team Rocket (SIH project)
- Learning: Java, DSA, Web Development
- Limited time — college + projects + self study

Your job:
- Create realistic study plans
- Create project/sprint plans
- Set weekly goals
- Track progress

Format plans like:
## Goal
## Week-wise Plan
### Week 1
- Day 1-2: Task
- Day 3-4: Task
## Daily Schedule (if asked)
## Tips
"""


def plan(message: str, save: bool = True, history: list = []) -> str:
    messages = [{"role": "system", "content": PLANNER_PROMPT}]
    
    for msg in history[-6:]:
        messages.append(msg)
    
    messages.append({"role": "user", "content": message})

    try:
        response = ollama.chat(model=MAIN_MODEL, messages=messages)
        result = response["message"]["content"]

        # Auto save plan
        if save:
            os.makedirs(PLANS_DIR, exist_ok=True)
            date = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"{PLANS_DIR}/plan_{date}.md"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result)
            
            result += f"\n\n✅ Plan saved: {filename}"

        return result

    except Exception as e:
        return f"Planner Agent error: {str(e)}"


if __name__ == "__main__":
    print("EIRA Planner Agent Test")
    print("-" * 40)
    
    result = plan("create a 4 week DSA study plan for GATE preparation")
    print(result[:500])