from langgraph.graph import StateGraph, END
from .state import AgentState
from .agents.source_agent import source_agent
from .agents.fetch_agent import fetch_agent
from .agents.retriever_agent import retriever_agent
from .agents.evidence_agent import evidence_agent
from .agents.judge_agent import judge_agent
from .agents.reputation_agent import reputation_agent
from .agents.ledger_agent import ledger_agent

def create_graph():
    """
    Constructs the LangGraph for the misinformation verification pipeline.
    """
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("source_agent", source_agent)
    workflow.add_node("fetch_agent", fetch_agent)
    workflow.add_node("retriever_agent", retriever_agent)
    workflow.add_node("evidence_agent", evidence_agent)
    workflow.add_node("judge_agent", judge_agent)
    workflow.add_node("reputation_agent", reputation_agent)
    workflow.add_node("ledger_agent", ledger_agent)

    # Define Edges
    workflow.set_entry_point("source_agent")
    
    workflow.add_edge("source_agent", "fetch_agent")
    workflow.add_edge("fetch_agent", "retriever_agent")
    workflow.add_edge("retriever_agent", "evidence_agent")
    workflow.add_edge("evidence_agent", "judge_agent")
    workflow.add_edge("judge_agent", "reputation_agent")
    workflow.add_edge("reputation_agent", "ledger_agent")
    workflow.add_edge("ledger_agent", END)

    # Compile
    app = workflow.compile()
    return app
