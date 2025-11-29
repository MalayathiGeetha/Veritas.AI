from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def test_gemini():
    print("Testing Gemini API...")
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        print("ERROR: GOOGLE_API_KEY not found in environment.")
        return

    try:
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
        result = llm.invoke("Hello, are you working?")
        print("Success! Response:")
        print(result.content)
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_gemini()
