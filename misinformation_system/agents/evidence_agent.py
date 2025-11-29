from typing import Dict, Any
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from ..state import AgentState
from dotenv import load_dotenv

load_dotenv()

def evidence_agent(state: AgentState) -> Dict[str, Any]:
    """
    EvidenceAgent: Extracts supporting and refuting sentences using Gemini.
    """
    print("---EvidenceAgent---")
    claim = state["claim"]
    passages = state.get("retrieved_passages", [])
    
    if not passages:
        print("No passages to analyze.")
        return {"evidence": []}
    
    print(f"Analyzing {len(passages)} passages for evidence...")
    
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)
        
        prompt_text = """
        You are an expert fact-checker. 
        Given the following claim and a list of retrieved passages, extract sentences that either SUPPORT or REFUTE the claim.
        For each sentence, assign a label (SUPPORT/REFUTE) and a confidence score (0.0-1.0).
        
        Claim: {claim}
        
        Passages:
        {passages}
        
        Return the output as a JSON object with a key "evidence" containing a list of objects.
        Each object should have: "sentence", "label", "score".
        """
        
        prompt = ChatPromptTemplate.from_template(prompt_text)
        chain = prompt | llm | JsonOutputParser()
        
        # Combine passages for context
        context = "\n\n".join(passages)
        
        result = chain.invoke({"claim": claim, "passages": context})
        
        evidence = result.get("evidence", [])
        print(f"Extracted {len(evidence)} pieces of evidence.")
        
        return {"evidence": evidence}
        
    except Exception as e:
        print(f"Error in EvidenceAgent: {e}")
        return {"evidence": []}

