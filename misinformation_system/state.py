from typing import List, Dict, Optional, TypedDict, Any
import operator
from typing_extensions import Annotated

class AgentState(TypedDict):
    """
    Represents the state of the misinformation verification pipeline.
    """
    claim: str
    sources: List[Dict[str, Any]]
    chunks: List[str]
    retrieved_passages: List[str]
    evidence: List[Dict[str, Any]]
    verdict: str
    confidence: float
    explanation: str
    adjusted_confidence: float
    credibility_report: Dict[str, Any]
    record_id: str
