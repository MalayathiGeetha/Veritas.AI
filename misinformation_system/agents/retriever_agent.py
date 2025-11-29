from typing import Dict, Any
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from ..state import AgentState
from dotenv import load_dotenv

load_dotenv()

def retriever_agent(state: AgentState) -> Dict[str, Any]:
    """
    RetrieverAgent: Queries a vector store for relevant passages using Gemini Embeddings and FAISS.
    """
    print("---RetrieverAgent---")
    claim = state["claim"]
    chunks = state.get("chunks", [])
    
    if not chunks:
        print("No chunks to retrieve from.")
        return {"retrieved_passages": []}
        
    print(f"Indexing {len(chunks)} chunks...")
    
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        
        # Create documents
        docs = [Document(page_content=chunk) for chunk in chunks]
        
        print("Creating vector store (FAISS)...")
        # Create temporary vector store
        vectorstore = FAISS.from_documents(
            documents=docs,
            embedding=embeddings
        )
        print("Vector store created.")
        
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        print("Invoking retriever...")
        results = retriever.invoke(claim)
        print("Retriever invoked.")
        
        retrieved_passages = [doc.page_content for doc in results]
        print(f"Retrieved {len(retrieved_passages)} relevant passages.")
        
        return {"retrieved_passages": retrieved_passages}
        
    except Exception as e:
        print(f"Error in RetrieverAgent: {e}")
        return {"retrieved_passages": []}

