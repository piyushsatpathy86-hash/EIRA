import sys
sys.path.append("C:/EIRA")

from tools.memory_tool import save_memory, get_relevant_memory, clear_memory

def test_save_and_retrieve_memory():
    clear_memory()
    save_memory("what is binary search?", "Binary search is a search algorithm.", "study")
    result = get_relevant_memory("binary search algorithm")
    assert "Binary search" in result or "binary" in result.lower()

def test_no_memory_returns_empty():
    clear_memory()
    result = get_relevant_memory("anything random")
    assert result == ""

def test_memory_persistence():
    clear_memory()
    save_memory("I love Java", "Java is great for OOP.", "coding")
    result = get_relevant_memory("Java programming")
    assert "Java" in result

    clear_memory()