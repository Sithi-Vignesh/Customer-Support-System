from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def sales_agent(state) -> dict:
    query = state["query"]
    context = state.get("retrieved_context", "")
    customer_name = state.get("customer_name", "Customer")

    prompt = f"""You are a Sales Support agent at ABC Technologies.
        Help the customer with product information, pricing, and subscription plans.

        Retrieved Context:
        {context}

        Customer Name: {customer_name}
        Customer Query: {query}

        Provide a helpful, professional response."""

    response = llm.invoke(prompt).content.strip()
    return {"agent_response": response}