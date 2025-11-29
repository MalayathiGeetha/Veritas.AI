from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def test_embedding():
    print("Testing Embedding...")
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        vec = embeddings.embed_query("Hello world")
        print(f"Success! Vector length: {len(vec)}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_embedding()
