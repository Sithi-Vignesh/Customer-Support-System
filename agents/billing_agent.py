from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def billing_agent(state) -> dict:
    query = state["query"]
    context = state.get("retrieved_context", "")
    customer_name = state.get("customer_name", "Customer")

    prompt = f"""You are a Billing Support agent at ABC Technologies.
        Help the customer with invoices, payments, and refund requests.

        Retrieved Context:
        {context}

        Customer Name: {customer_name}
        Customer Query: {query}

        Provide a helpful response. For refund requests, inform the customer their request will be reviewed."""

    response = llm.invoke(prompt).content.strip()
    return {"agent_response": response}