from typing import Dict, Any
import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..state import AgentState

def fetch_agent(state: AgentState) -> Dict[str, Any]:
    """
    FetchAgent: Fetches content from URLs and splits it into chunks.
    """
    print("---FetchAgent---")
    sources = state.get("sources", [])
    
    chunks = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    for source in sources:
        url = source.get("url")
        if not url:
            continue
            
        print(f"Fetching: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                    
                text = soup.get_text()
                
                # Clean text
                lines = (line.strip() for line in text.splitlines())
                chunks_text = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks_text if chunk)
                
                # Split into chunks
                source_chunks = text_splitter.split_text(text)
                
                # Limit chunks per source to avoid context overflow
                chunks.extend(source_chunks[:5]) 
                
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            continue
        
    return {"chunks": chunks}

