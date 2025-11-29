from typing import Dict, Any
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from ..state import AgentState
from dotenv import load_dotenv

load_dotenv()

def source_agent(state: AgentState) -> Dict[str, Any]:
    """
    SourceAgent: Performs SERP search to find relevant URLs using Tavily.
    """
    print("---SourceAgent---")
    claim = state["claim"]
    
    print(f"Searching for: {claim}")
    
    try:
        tool = TavilySearchResults(max_results=5)
        results = tool.invoke({"query": claim})
        
        # Tavily returns a list of dicts with 'url' and 'content'
        sources = []
        for res in results:
            sources.append({
                "url": res["url"],
                "title": res.get("title", "No Title"), # Tavily might not always return title in basic mode
                "snippet": res.get("content", ""),
                "date": "" # Tavily doesn't always provide date
            })
            
        return {"sources": sources}
        
    except Exception as e:
        print(f"Error in SourceAgent: {e}")
        return {"sources": []}

