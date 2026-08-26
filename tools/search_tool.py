import sys
sys.path.append("C:/EIRA")

import ssl
import certifi
from config.settings import TAVILY_API_KEY, USE_TAVILY

def search(query: str, max_results: int = 5) -> str:
    """Tavily pehle, fail hua toh DuckDuckGo"""

    if USE_TAVILY:
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=TAVILY_API_KEY)
            results = client.search(query, max_results=max_results)
            output = f"🔍 Search: {query}\n\n"
            for i, r in enumerate(results['results'], 1):
                output += f"{i}. **{r['title']}**\n"
                output += f"   {r['content'][:200]}...\n"
                output += f"   Source: {r['url']}\n\n"
            return output
        except Exception as e:
            print(f"Tavily failed: {e} — trying DuckDuckGo")

    return _ddg_search(query, max_results)

def _ddg_search(query: str, max_results: int = 5) -> str:
    try:
        from ddgs import DDGS
        output = f"🔍 Search: {query}\n\n"
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        for i, r in enumerate(results, 1):
            output += f"{i}. **{r['title']}**\n"
            output += f"   {r['body'][:200]}...\n"
            output += f"   Source: {r['href']}\n\n"
        return output if results else "Koi result nahi mila."
    except Exception as e:
        return f"Search fail ho gaya: {e}"

if __name__ == "__main__":
    print(search("latest AI models 2026"))