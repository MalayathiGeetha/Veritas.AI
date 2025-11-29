import subprocess
import time
import requests
import sys
import os

def test_server():
    print("Starting API server...")
    # Start server in background
    process = subprocess.Popen(
        [sys.executable, "-m", "misinformation_system.api"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Wait for server to start
        print("Waiting for server to initialize...")
        time.sleep(10) 
        
        # Test Health
        print("Testing /health endpoint...")
        try:
            resp = requests.get("http://localhost:8000/health")
            print(f"Health Status: {resp.status_code}")
            print(resp.json())
        except Exception as e:
            print(f"Health check failed: {e}")
            return

        # Test Verify (Mock claim to save time/cost if possible, but we'll use a real one)
        print("Testing /verify endpoint...")
        claim = "The earth is flat."
        try:
            resp = requests.post("http://localhost:8000/verify", json={"claim": claim})
            print(f"Verify Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                print(f"Verdict: {data.get('verdict')}")
                print(f"Confidence: {data.get('confidence')}")
            else:
                print(resp.text)
        except Exception as e:
            print(f"Verify check failed: {e}")

    finally:
        print("Stopping server...")
        process.terminate()
        outs, errs = process.communicate()
        print("Server Output:")
        print(outs.decode('utf-8', errors='ignore'))
        print("Server Errors:")
        print(errs.decode('utf-8', errors='ignore'))

if __name__ == "__main__":
    test_server()
