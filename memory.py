# llm.py
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os

def build_llm(model: str = "llama-3.1-8b-instant"):
    """
    Build a coding assistant using Groq LLM + LangChain.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment.")

    llm = ChatGroq(
        api_key=api_key,
        model_name=model,
        temperature=0.2,  # lower temp = more precise, less "chatty"
    )

    memory = ConversationBufferMemory(return_messages=True)

    # Custom system prompt for coding
    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template="""
You are CodeMate, an expert coding assistant. 
You help with:
- Writing clean and correct code
- Debugging errors
- Explaining code step by step
- Suggesting best practices

Always provide code inside ```python (or other language) fenced blocks.

Conversation history:
{history}

User: {input}
Assistant:"""
    )

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=True
    )

    return conversation
