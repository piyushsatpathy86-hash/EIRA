# ============================================================
# EIRA — Main Brain (Orchestrator)
# ============================================================

import sys
sys.path.append("C:/EIRA")

from core.router import detect_intent
from config.settings import EIRA_BASE_PERSONALITY, MAIN_MODEL
from tools.memory_tool import save_memory, get_relevant_memory

def handle_desktop_action(user_message: str):
    """Desktop actions — direct, no AI needed"""
    msg = user_message.lower()

    if any(w in msg for w in ["open", "search", "play", "kholo"]):
        if any(w in msg for w in ["youtube", "yt", "video"]):
            from tools.system_control import open_youtube_video
            import re
            url = re.search(r'https?://\S+', user_message)
            if url:
                open_youtube_video(url.group())
                return "Video khul gaya! ✅"
            else:
                skip = ["open","search","play","on","youtube",
                        "yt","eira","video","kholo","please","kar"]
                words = [w for w in user_message.split()
                         if w.lower() not in skip]
                query = " ".join(words)
                open_youtube_video(query)
                return f"YouTube pe search ho gaya: '{query}' ✅"

    if any(w in msg for w in ["open", "kholo", "jaao"]):
        sites = ["google","github","leetcode",
                 "gmail","linkedin","netflix","spotify"]
        for site in sites:
            if site in msg:
                from tools.system_control import open_website
                open_website(site)
                return f"{site.capitalize()} khul gaya! ✅"

    if any(w in msg for w in ["wallpaper", "background"]):
        from tools.desktop_control import download_and_set_wallpaper
        skip = ["wallpaper","background","change","set",
                "eira","please","karo","kar","mera","meri"]
        words = [w for w in user_message.split()
                 if w.lower() not in skip]
        query = " ".join(words) if words else "nature dark aesthetic"
        return download_and_set_wallpaper(query)

    if any(w in msg for w in ["screenshot", "ss le", "screen capture"]):
        from tools.desktop_control import take_screenshot
        return take_screenshot()

    if any(w in msg for w in ["battery", "charge", "kitni battery"]):
        from tools.system_control import get_battery
        return get_battery()

    if any(w in msg for w in ["open", "kholo", "launch"]):
        from tools.system_control import open_app
        skip = ["open","kholo","launch","eira","please","kar","karo"]
        words = [w for w in user_message.split()
                 if w.lower() not in skip]
        app = " ".join(words)
        if app:
            return open_app(app)

    return None


def chat_with_eira(user_message: str, history: list = []) -> str:

    # Step 1 — Desktop action check
    action_result = handle_desktop_action(user_message)
    if action_result:
        return action_result

    # Step 2 — Kaunsa agent?
    routing = detect_intent(user_message)
    agent   = routing["agent"]
    model   = routing["model"]
    print(f"\n[EIRA] Agent: {agent.upper()} | ", end="")

    # Step 3 — Agent prompts
    agent_prompts = {
        "coding": """
You are EIRA's Coding Agent.
Help write, debug, review, and explain code.
Always give working code with clear comments.
Explain WHY errors happen, not just how to fix.
Prefer Java and Python unless specified.
""",
        "study": """
You are EIRA's Study Agent.
Help with DSA, Java, OS, DBMS, Discrete Math, GATE prep.
Use simple language, real life analogies, examples.
Quiz format: 5 MCQs with answers at end.
""",
        "notes": """
You are EIRA's Notes Agent.
Convert content into clean structured notes.
Format: Topic -> Key Points -> Summary -> Revision Questions.
""",
        "research": """
You are EIRA's Research Agent.
You have access to real web search results — use them.
Format: Overview -> Key Points -> Pros/Cons -> Recommendation.
Always cite sources where relevant.
Be objective, factual, and helpful.
""",
        "planner": """
You are EIRA's Planner Agent.
Give realistic week-wise or day-wise plans.
Goals to keep in mind: SIH 2026, internship, GATE 2028.
""",
        "general": """
You are EIRA — a warm, witty, and helpful AI assistant.
Be friendly and supportive. Talk like a smart friend.
"""
    }

    system_prompt = (EIRA_BASE_PERSONALITY + "\n"
                     + agent_prompts.get(agent, agent_prompts["general"]))

    # Step 3.5 — Memory fetch karo
    try:
        relevant_memory = get_relevant_memory(user_message)
        if relevant_memory:
            system_prompt += f"\n\n{relevant_memory}"
            print(f"[EIRA] Memory loaded ✓ | ", end="")
    except Exception as e:
        print(f"[EIRA] Memory error: {e} | ", end="")

    # Step 3.6 — Research agent ke liye web search
    if agent == "research":
        try:
            from tools.search_tool import search
            print(f"[EIRA] Web search chal rahi hai...")
            search_results = search(user_message, max_results=5)
            user_message = f"""User question: {user_message}

Web search results:
{search_results}

Based on these results, give a clear, helpful, and well-structured answer."""
        except Exception as e:
            print(f"Search error: {e}")

    messages = [{"role": "system", "content": system_prompt}]
    for msg in history[-4:]:
        messages.append(msg)
    messages.append({"role": "user", "content": user_message})

    # Step 4 — Groq ya Ollama fallback
    final_response = ""
    try:
        from groq import Groq
        from config.settings import GROQ_API_KEY, GROQ_MODEL
        client   = Groq(api_key=GROQ_API_KEY)
        print(f"Groq | Model: {GROQ_MODEL}")
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=1024
        )
        final_response = response.choices[0].message.content

    except Exception as e:
        print(f"Groq error: {e} — falling back to Ollama")
        try:
            import ollama
            print(f"Ollama | Model: {model}")
            response = ollama.chat(model=model, messages=messages)
            final_response = response["message"]["content"]
        except Exception as e2:
            return f"EIRA error: {str(e2)}"

    # Step 5 — Memory mein save karo
    try:
        save_memory(user_message, final_response, agent)
    except Exception as e:
        print(f"Memory save error: {e}")

    return final_response


def run_terminal_chat():
    print("=" * 50)
    print("  EIRA — Online aur ready!")
    print("  'quit' likhke band karo")
    print("=" * 50)

    history = []

    while True:
        try:
            user_input = input("\nTum: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["quit","exit","bye","band kar"]:
                print("\nEIRA: Chal phir milte hain! 👋")
                break

            response = chat_with_eira(user_input, history)
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})
            print(f"\nEIRA: {response}")

        except KeyboardInterrupt:
            print("\n\nEIRA: Bye! 👋")
            break


if __name__ == "__main__":
    run_terminal_chat()