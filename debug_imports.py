import sys
import os

print("Starting import debug...")

try:
    print("Importing state...")
    from misinformation_system.state import AgentState
    print("State imported.")

    print("Importing source_agent...")
    from misinformation_system.agents.source_agent import source_agent
    print("SourceAgent imported.")

    print("Importing fetch_agent...")
    from misinformation_system.agents.fetch_agent import fetch_agent
    print("FetchAgent imported.")

    print("Importing retriever_agent...")
    from misinformation_system.agents.retriever_agent import retriever_agent
    print("RetrieverAgent imported.")

    print("Importing evidence_agent...")
    from misinformation_system.agents.evidence_agent import evidence_agent
    print("EvidenceAgent imported.")

    print("Importing judge_agent...")
    from misinformation_system.agents.judge_agent import judge_agent
    print("JudgeAgent imported.")

    print("Importing reputation_agent...")
    from misinformation_system.agents.reputation_agent import reputation_agent
    print("ReputationAgent imported.")

    print("Importing ledger_agent...")
    from misinformation_system.agents.ledger_agent import ledger_agent
    print("LedgerAgent imported.")

    print("Importing graph...")
    from misinformation_system.graph import create_graph
    print("Graph imported.")

except Exception as e:
    print(f"IMPORT ERROR: {e}")
    import traceback
    traceback.print_exc()

print("Debug complete.")
