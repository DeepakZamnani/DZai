# llm.py
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
def build_llm(model: str = "llama-3.1-8b-instant"):
    """
    Initialize the Groq LLM chat model.
    Requires GROQ_API_KEY to be set in environment.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment.")

    return ChatGroq(
        api_key=api_key,
        model_name=model,
        temperature=0.7
    )
