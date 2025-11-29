from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def test_gemini_3():
    print("Testing Gemini 3 Pro...")
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-3-pro-preview", temperature=0)
        result = llm.invoke("Hello")
        print("Success! Response:")
        print(result.content)
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_gemini_3()
