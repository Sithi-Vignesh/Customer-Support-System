"""
technical_agent.py
Specialized agent for handling Technical Support queries including
application errors, installation issues, login problems, and configuration.
Uses RAG context retrieved from the technical manual.
"""
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def technical_agent(state) -> dict:
    """
    Generates a technical support response using RAG context and Groq LLM.
    Handles errors, crashes, installation, and configuration issues.
    """
    query = state["query"]
    context = state.get("retrieved_context", "")
    customer_name = state.get("customer_name", "Customer")

    prompt = f"""You are a Technical Support agent at ABC Technologies.
Help the customer with application errors, installation issues, login problems, and configuration.

Retrieved Context:
{context}

Customer Name: {customer_name}
Customer Query: {query}

Provide a clear, step-by-step technical response."""

    response = llm.invoke(prompt).content.strip()
    return {"agent_response": response}