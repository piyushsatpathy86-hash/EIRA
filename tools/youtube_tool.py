# ============================================================
# EIRA — YouTube to Notes Tool
# ============================================================

import sys
sys.path.append("C:/EIRA")

from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url: str) -> str:
    patterns = [
        r'v=([a-zA-Z0-9_-]{11})',
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
        r'embed/([a-zA-Z0-9_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript(url: str) -> str:
    video_id = get_video_id(url)
    if not video_id:
        return None, "Invalid YouTube URL"
    
    try:
        ytt = YouTubeTranscriptApi()
        transcript = ytt.fetch(video_id, languages=['en-IN', 'en', 'hi'])
        full_text = " ".join([t.text for t in transcript])
        return full_text, None
    except Exception as e:
        return None, f"Transcript nahi mila: {str(e)}"

def youtube_to_notes(url: str, client, model: str) -> str:
    transcript, error = get_transcript(url)
    if error:
        return f"Error: {error}"
    
    max_chars = 8000
    if len(transcript) > max_chars:
        transcript = transcript[:max_chars] + "..."
    
    prompt = f"""Convert this YouTube video transcript into clean, structured study notes.

Transcript:
{transcript}

Format the notes as:
# Topic Name

## Overview
(2-3 lines summary)

## Key Concepts
(bullet points of main ideas)

## Detailed Notes
(organized sections with explanations)

## Important Points
(things to remember)

## Revision Questions
(5 questions to test understanding)

Make the notes clear, concise, and student-friendly."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Notes generation error: {e}"


if __name__ == "__main__":
    from groq import Groq
    from config.settings import GROQ_API_KEY, GROQ_MODEL
    
    client = Groq(api_key=GROQ_API_KEY)
    url = input("YouTube URL dalo: ")
    print("\nNotes bana rahi hoon...\n")
    notes = youtube_to_notes(url, client, GROQ_MODEL)
    print(notes)