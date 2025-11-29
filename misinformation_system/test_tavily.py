from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import os

load_dotenv()

def test_tavily():
    print("Testing Tavily Search...")
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        print("ERROR: TAVILY_API_KEY not found in environment.")
        return

    try:
        tool = TavilySearchResults(max_results=3)
        results = tool.invoke({"query": "Test query"})
        print(f"Success! Found {len(results)} results.")
        print(results)
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_tavily()
