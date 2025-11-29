import sys
import os

print("DEBUG: main.py started", flush=True)

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from misinformation_system.graph import create_graph

def main():
    print("DEBUG: Entering main()", flush=True)
    print("Initializing Misinformation Verification System...", flush=True)
    
    print("DEBUG: Calling create_graph()", flush=True)
    app = create_graph()
    print("DEBUG: Graph created", flush=True)
    
    claim = "Drinking bleach cures COVID-19."
    print(f"\nProcessing Claim: '{claim}'\n")
    
    initial_state = {"claim": claim}
    
    # Run the graph
    print("Starting graph execution...")
    try:
        for output in app.stream(initial_state):
            for key, value in output.items():
                print(f"Finished: {key}")
    except Exception as e:
        print(f"Graph execution failed: {e}")
            
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    main()
