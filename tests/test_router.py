import sys
sys.path.append("C:/EIRA")

from core.router import detect_intent

def test_coding_agent():
    result = detect_intent("write a java program")
    assert result["agent"] == "coding"

def test_study_agent():
    result = detect_intent("explain binary tree")
    assert result["agent"] == "study"

def test_notes_agent():
    result = detect_intent("make notes from youtube")
    assert result["agent"] == "notes"

def test_research_agent():
    result = detect_intent("compare react vs vue")
    assert result["agent"] == "research"

def test_planner_agent():
    result = detect_intent("create study plan")
    assert result["agent"] == "planner"

def test_general_fallback():
    result = detect_intent("hey what's up")
    assert result["agent"] == "general"