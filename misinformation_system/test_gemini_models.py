from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def test_model(model_name):
    print(f"Testing model: {model_name}")
    try:
        llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
        result = llm.invoke("Hello")
        print(f"SUCCESS: {model_name}")
        return True
    except Exception as e:
        print(f"FAILED: {model_name} - {e}")
        return False

if __name__ == "__main__":
    models_to_test = ["gemini-pro", "gemini-1.5-flash", "models/gemini-pro", "gemini-1.5-flash-001"]
    
    for model in models_to_test:
        if test_model(model):
            break
