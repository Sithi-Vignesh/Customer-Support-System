"""
main.py
Entry point for the ABC Technologies Customer Support Automation System.
Builds the LangGraph workflow, connects all nodes and edges,
and runs the five demonstration queries from the assignment spec.
"""
from langgraph.graph import StateGraph, END
from graph.state import SupportState
from graph.nodes import classify_intent, memory_node, hitl_node, supervisor_node
from graph.router import route_by_intent, route_after_hitl
from agents.sales_agent import sales_agent
from agents.technical_agent import technical_agent
from agents.billing_agent import billing_agent
from agents.account_agent import account_agent
from rag.retriever import ingest_documents, retrieve_context
from memory.memory_manager import init_db, save_conversation


def rag_node(state: SupportState) -> dict:
    """
    RAG node that retrieves relevant context from ChromaDB
    based on the customer query before passing to specialized agents.
    """
    query = state["query"]
    context = retrieve_context(query)
    return {"retrieved_context": context}


def build_graph():
    """
    Constructs and compiles the full LangGraph state machine.
    Defines all nodes, edges, and conditional routing logic.
    Returns a compiled LangGraph app ready for invocation.
    """
    graph = StateGraph(SupportState)

    # Register all nodes
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("rag_node", rag_node)
    graph.add_node("sales_node", sales_agent)
    graph.add_node("technical_node", technical_agent)
    graph.add_node("billing_node", billing_agent)
    graph.add_node("account_node", account_agent)
    graph.add_node("memory_node", memory_node)
    graph.add_node("hitl_node", hitl_node)
    graph.add_node("supervisor_node", supervisor_node)

    # Entry point
    graph.set_entry_point("classify_intent")

    # After classification: memory goes direct, others go through RAG first
    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "sales_node": "rag_node",
            "technical_node": "rag_node",
            "billing_node": "rag_node",
            "account_node": "rag_node",
            "memory_node": "memory_node"
        }
    )

    # After RAG: route to correct specialized agent
    graph.add_conditional_edges(
        "rag_node",
        route_by_intent,
        {
            "sales_node": "sales_node",
            "technical_node": "technical_node",
            "billing_node": "billing_node",
            "account_node": "account_node",
            "memory_node": "memory_node"
        }
    )

    # All agents feed into HITL check
    graph.add_edge("sales_node", "hitl_node")
    graph.add_edge("technical_node", "hitl_node")
    graph.add_edge("billing_node", "hitl_node")
    graph.add_edge("account_node", "hitl_node")

    # After HITL: always go to supervisor regardless of approval outcome
    graph.add_conditional_edges(
        "hitl_node",
        route_after_hitl,
        {
            "supervisor_node": "supervisor_node"
        }
    )

    # Terminal edges
    graph.add_edge("supervisor_node", END)
    graph.add_edge("memory_node", END)

    return graph.compile()


def run_query(app, customer_id: str, query: str, customer_name: str = "Customer"):
    """
    Runs a single customer query through the compiled LangGraph app.
    Prints intent and final response, then saves interaction to SQLite memory.
    """
    print("\n" + "="*60)
    print(f"Customer: {customer_name} | ID: {customer_id}")
    print(f"Query: {query}")
    print("="*60)

    initial_state = {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "query": query,
    }

    result = app.invoke(initial_state)

    final_response = result.get("final_response", "No response generated.")
    intent = result.get("intent", "Unknown")

    print(f"\nIntent: {intent}")
    print(f"Final Response: {final_response}")

    # Persist interaction to SQLite for future memory recall
    save_conversation(customer_id, query, final_response)

    return result


if __name__ == "__main__":
    # Initialize SQLite memory and ingest KB documents into ChromaDB
    init_db()
    ingest_documents()

    # Build and compile the LangGraph workflow
    app = build_graph()

    print("\n--ABC Technologies Customer Support System--\n")

    # Query 1 - Sales routing
    run_query(app, "C001", "What are the pricing plans available for your software?", "Sithi")

    # Query 2 - Account routing
    run_query(app, "C002", "I forgot my account password.", "Nithin")

    # Query 3 - Technical routing
    run_query(app, "C003", "My application crashes whenever I upload a file.", "Nikhil")

    # Query 4 - Billing routing with HITL approval
    run_query(app, "C004", "I need a refund for my annual subscription.", "Logith")

    # Query 5 - Memory recall (same customer as Query 4)
    run_query(app, "C004", "What was my previous support issue?", "Logith")