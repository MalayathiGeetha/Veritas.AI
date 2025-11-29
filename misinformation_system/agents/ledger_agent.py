import json
import uuid
from typing import Dict, Any
from ..state import AgentState

def ledger_agent(state: AgentState) -> Dict[str, Any]:
    """
    LedgerAgent: Writes the final record to a database.
    """
    print("---LedgerAgent---")
    
    record = {
        "id": str(uuid.uuid4()),
        "claim": state["claim"],
        "verdict": state.get("verdict"),
        "confidence": state.get("adjusted_confidence"),
        "explanation": state.get("explanation"),
        "evidence": state.get("evidence"),
        "credibility_report": state.get("credibility_report")
    }
    
    # Mock DB Write
    print("Writing record to DB:")
    print(json.dumps(record, indent=2))
    
    return {"record_id": record["id"]}
