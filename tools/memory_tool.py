# ============================================================
# EIRA — Memory Tool (ChromaDB)
# ============================================================

import sys
import os
import chromadb
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import MEMORY_DIR

# Ensure memory directory exists
os.makedirs(MEMORY_DIR, exist_ok=True)

# ChromaDB client
client = chromadb.PersistentClient(path=MEMORY_DIR)
collection = client.get_or_create_collection(name="eira_memory")

def save_memory(user_msg: str, eira_response: str, agent: str = "general"):
    """Conversation save karo memory mein"""
    try:
        doc_id = f"mem_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        collection.add(
            documents=[f"User: {user_msg}\nEIRA: {eira_response}"],
            metadatas=[{
                "agent": agent,
                "timestamp": datetime.now().isoformat(),
                "user_msg": user_msg[:200]
            }],
            ids=[doc_id]
        )
        return True
    except Exception as e:
        print(f"Memory save error: {e}")
        return False

def get_relevant_memory(query: str, n_results: int = 3) -> str:
    """Query se related purani conversations dhundho"""
    try:
        count = collection.count()
        if count == 0:
            return ""

        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, count)
        )

        if not results["documents"][0]:
            return ""

        memory_text = "📚 Relevant past context:\n"
        for doc in results["documents"][0]:
            memory_text += f"- {doc[:200]}\n"
        return memory_text
    except Exception as e:
        print(f"Memory fetch error: {e}")
        return ""

def clear_memory():
    """Sari memory clear karo"""
    try:
        global collection
        client.delete_collection("eira_memory")
        collection = client.get_or_create_collection(name="eira_memory")
        return "Memory clear ho gayi! ✅"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Test
    print("Testing EIRA Memory...")
    save_memory("what is binary search?",
                "Binary search is a search algorithm...",
                "study")
    save_memory("write a java hello world",
                "public class Hello { ... }",
                "coding")

    result = get_relevant_memory("binary search algorithm")
    print(f"Memory found:\n{result}")
    print("Memory test complete! ✅")