from typing import Dict, Any
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from ..state import AgentState
from dotenv import load_dotenv

load_dotenv()

def judge_agent(state: AgentState) -> Dict[str, Any]:
    """
    JudgeAgent: Produces a final verdict based on the evidence using Gemini.
    """
    print("---JudgeAgent---")
    claim = state["claim"]
    evidence = state.get("evidence", [])
    
    print(f"Judging claim '{claim}' based on {len(evidence)} pieces of evidence.")
    
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)
        
        prompt_text = """
        You are an impartial judge.
        Given the following claim and the extracted evidence, determine if the claim is TRUE, FALSE, or UNCLEAR.
        Provide a confidence score (0.0-1.0) and a brief explanation.
        
        Claim: {claim}
        
        Evidence:
        {evidence}
        
        Return the output as a JSON object with keys: "verdict", "confidence", "explanation".
        """
        
        prompt = ChatPromptTemplate.from_template(prompt_text)
        chain = prompt | llm | JsonOutputParser()
        
        # Format evidence for prompt
        evidence_text = "\n".join([f"- {e['label']} ({e['score']}): {e['sentence']}" for e in evidence])
        
        result = chain.invoke({"claim": claim, "evidence": evidence_text})
        
        return {
            "verdict": result.get("verdict", "UNCLEAR"),
            "confidence": result.get("confidence", 0.0),
            "explanation": result.get("explanation", "No explanation provided.")
        }
        
    except Exception as e:
        print(f"Error in JudgeAgent: {e}")
        return {
            "verdict": "UNCLEAR",
            "confidence": 0.0,
            "explanation": f"Error during judgment: {e}"
        }

