from typing import Dict, Any
from ..state import AgentState

def reputation_agent(state: AgentState) -> Dict[str, Any]:
    """
    ReputationAgent: Adjusts confidence based on source credibility.
    """
    print("---ReputationAgent---")
    sources = state.get("sources", [])
    confidence = state.get("confidence", 0.5)
    
    # Simple Allowlist/Blocklist
    trusted_domains = ["science-journal.org", "reuters.com", "bbc.com"]
    questionable_domains = ["conspiracy-news.net", "clickbait.com"]
    
    score_adjustment = 0.0
    credibility_report = []
    
    for source in sources:
        url = source.get("url", "")
        if not url:
            continue
            
        domain = url.split("//")[-1].split("/")[0]
        status = "Neutral"
        
        if any(trusted in domain for trusted in trusted_domains):
            score_adjustment += 0.1
            status = "Trusted"
        elif any(questionable in domain for questionable in questionable_domains):
            score_adjustment -= 0.2
            status = "Questionable"
            
        credibility_report.append({
            "domain": domain,
            "url": url,
            "status": status
        })
            
    adjusted_confidence = min(max(confidence + score_adjustment, 0.0), 1.0)
    
    print(f"Confidence adjusted from {confidence} to {adjusted_confidence}")
    
    return {
        "adjusted_confidence": adjusted_confidence,
        "credibility_report": credibility_report
    }
