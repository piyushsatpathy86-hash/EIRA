# ============================================================
# EIRA — Notes Agent (Permission-Based PDF + Doodles)
# ============================================================

import sys
sys.path.append("C:/EIRA")

import ollama
import os
from config.settings import FAST_MODEL, NOTES_DIR, EIRA_BASE_PERSONALITY

NOTES_PROMPT = EIRA_BASE_PERSONALITY + """
You are EIRA's Notes Agent.

Convert any topic into clean structured notes.

ALWAYS format like this:
# Topic Name
## Key Concepts
- Point 1
- Point 2
## Important Terms
- Term: Definition
## Quick Summary
2-3 lines only
## Revision Questions
1. Question?
2. Question?

Keep it clean, concise, student-friendly.
"""


def make_notes(message: str,
               save: bool = False,
               make_pdf: bool = False,
               make_doodle: bool = False,
               history: list = []) -> str:
    """
    save       = True only when user says 'save'
    make_pdf   = True only when user says 'make pdf' or 'save as pdf'
    make_doodle= True only when user says 'draw' or 'make doodle'
    """

    messages = [{"role": "system", "content": NOTES_PROMPT}]
    for msg in history[-6:]:
        messages.append(msg)
    messages.append({"role": "user", "content": message})

    try:
        # Groq first (fast)
        try:
            from groq import Groq
            from config.settings import GROQ_API_KEY, GROQ_MODEL
            client = Groq(api_key=GROQ_API_KEY)
            res    = client.chat.completions.create(
                model=GROQ_MODEL, messages=messages, max_tokens=2048)
            notes  = res.choices[0].message.content
        except Exception:
            res   = ollama.chat(model=FAST_MODEL, messages=messages)
            notes = res["message"]["content"]

        result = notes

        # Save markdown ONLY if user said so
        if save:
            os.makedirs(NOTES_DIR, exist_ok=True)
            topic   = message[:40].replace(" ","_").replace("/","-")
            md_path = f"{NOTES_DIR}/{topic}.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(notes)
            result += f"\n\n✅ Notes saved: {md_path}"

        # PDF ONLY if user gave permission
        if make_pdf:
            try:
                from tools.pdf_maker import notes_to_pdf
                pdf_path = notes_to_pdf(message[:40], notes)
                result  += f"\n✅ PDF saved: {pdf_path}"
                import subprocess
                subprocess.Popen(["start", pdf_path], shell=True)
            except Exception as e:
                result += f"\n⚠️ PDF error: {e}"

        # Doodle ONLY if user asked
        if make_doodle:
            try:
                from tools.doodle_maker import (
                    make_concept_cartoon, open_svg)
                svg = make_concept_cartoon(
                    message[:40],
                    notes[:120]
                )
                result += f"\n✅ Doodle saved: {svg}"
                open_svg(svg)
            except Exception as e:
                result += f"\n⚠️ Doodle error: {e}"

        return result

    except Exception as e:
        return f"Notes Agent error: {str(e)}"


if __name__ == "__main__":
    # Test — no auto save
    result = make_notes("binary search tree")
    print(result)
    print("\n--- Now with PDF permission ---")
    result2 = make_notes("quicksort", make_pdf=True)
    print(result2[:300])