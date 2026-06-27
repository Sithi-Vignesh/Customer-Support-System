"""
nodes.py
Defines all core LangGraph nodes:
- classify_intent: Categorizes customer query using LLM
- memory_node: Handles memory recall queries using SQLite history
- hitl_node: Checks if human approval is required and requests it
- supervisor_node: Validates and improves agent responses before final delivery
"""
from graph.state import SupportState
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Groq LLM with LLaMA 3.3 70B model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def classify_intent(state: SupportState) -> dict:
    """
    Classifies the customer query into one of five categories:
    Sales, Technical, Billing, Account, or Memory.
    Uses a strict LLM prompt to return only the category name.
    """
    query = state["query"]
    
    prompt = f"""You are an intent classifier for a customer support system.
Classify the following customer query into exactly one of these categories:
Sales, Technical, Billing, Account, Memory

Rules:
- Sales: pricing, plans, product information
- Technical: errors, crashes, installation, login issues
- Billing: invoices, payments, refunds
- Account: password reset, profile updates, account activation
- Memory: customer asking about previous interactions

Query: {query}

Respond with only the category name. Nothing else."""

    response = llm.invoke(prompt)
    intent = response.content.strip()
    return {"intent": intent}


def memory_node(state: SupportState) -> dict:
    """
    Handles memory recall queries by fetching conversation history
    from SQLite and using LLM to generate a context-aware response.
    Bypasses all agent routing — goes directly to END.
    """
    from memory.memory_manager import get_conversation_history
    customer_id = state["customer_id"]
    history = get_conversation_history(customer_id)
    
    if not history:
        response = "I don't have any previous interactions recorded for you."
    else:
        history_text = "\n".join([f"Q: {h['query']} A: {h['response']}" for h in history])
        prompt = f"""Based on this conversation history, answer the customer's question.
        
History:
{history_text}

Customer question: {state["query"]}"""
        response = llm.invoke(prompt).content.strip()
    
    return {"final_response": response, "intent": "Memory"}


def hitl_node(state: SupportState) -> dict:
    """
    Checks if the customer query requires human approval.
    If yes, pauses and prompts the supervisor for a decision via terminal input.
    High-risk requests: refunds, cancellations, account closure, compensation, escalation.
    """
    from hitl.approval import check_requires_approval, request_human_approval
    
    query = state["query"]
    requires_approval = check_requires_approval(query)
    
    if requires_approval:
        approval_status, escalation_reason = request_human_approval(state)
        return {
            "requires_approval": True,
            "approval_status": approval_status,
            "escalation_reason": escalation_reason
        }
    
    return {"requires_approval": False, "approval_status": "approved"}


def supervisor_node(state: SupportState) -> dict:
    """
    Supervisor agent that reviews and improves the specialized agent's draft response.
    If the request was rejected by HITL, returns a standard rejection message.
    Otherwise, uses LLM to produce a polished, professional final response.
    """
    agent_response = state.get("agent_response", "")
    query = state["query"]
    approval_status = state.get("approval_status", "approved")
    
    if approval_status == "rejected":
        return {"final_response": "Your request has been reviewed and unfortunately cannot be processed at this time. Please contact our support team for further assistance."}
    
    prompt = f"""You are a customer support supervisor at ABC Technologies.
Review and improve the following agent response for professionalism, accuracy, and completeness.

Customer Query: {query}
Agent Response: {agent_response}

Provide an improved, professional final response. Be concise and helpful.
Return only one final response. Do not provide alternatives or multiple versions."""

    final = llm.invoke(prompt).content.strip()
    return {"final_response": final}