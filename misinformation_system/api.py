from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from misinformation_system.graph import create_graph

app = FastAPI(title="Misinformation Verification API")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class VerifyRequest(BaseModel):
    claim: str
    url: Optional[str] = None

class VerifyResponse(BaseModel):
    verdict: str
    confidence: float
    explanation: str
    evidence: list
    credibility_report: list

# Initialize graph once
print("Initializing Graph...")
graph_app = create_graph()
print("Graph Initialized.")

@app.post("/verify", response_model=VerifyResponse)
async def verify_claim(request: VerifyRequest):
    print(f"Received claim: {request.claim}")
    
    try:
        initial_state = {"claim": request.claim}
        final_state = None
        
        # Run graph
        # Note: In a real async app, we might want to run this in a threadpool if it's blocking
        for output in graph_app.stream(initial_state):
            for key, value in output.items():
                print(f"Finished step: {key}")
                if key == "ledger_agent":
                    final_state = value
        
        if not final_state:
            # Fallback if ledger_agent output isn't captured directly in stream loop
            # (depending on how stream yields)
            # But usually the last yield is the final state update
            # Let's try to get the final state from the last output or assume the last step was ledger
            pass

        # Since stream yields partial updates, we need to ensure we have the final data.
        # A better way with LangGraph is to invoke() if we don't need streaming updates, 
        # but invoke() might be synchronous blocking.
        # Let's use invoke for simplicity in the API for now.
        
        result = graph_app.invoke(initial_state)
        
        return VerifyResponse(
            verdict=result.get("verdict", "UNKNOWN"),
            confidence=result.get("confidence", 0.0),
            explanation=result.get("explanation", "No explanation provided."),
            evidence=result.get("evidence", []),
            credibility_report=result.get("credibility_report", {})
        )

    except Exception as e:
        print(f"Error processing claim: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
