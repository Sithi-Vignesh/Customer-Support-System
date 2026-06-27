"""
router.py
Contains conditional edge functions used by LangGraph to route
the state to the correct next node based on intent or approval status.
"""
from graph.state import SupportState

def route_by_intent(state: SupportState) -> str:
    """
    Routes the query to the appropriate agent node based on classified intent.
    Returns the node name as a string for LangGraph conditional edges.
    """
    intent = state.get("intent", "").strip()
    
    routes = {
        "Sales": "sales_node",
        "Technical": "technical_node",
        "Billing": "billing_node",
        "Account": "account_node",
        "Memory": "memory_node"
    }
    
    return routes.get(intent, "account_node")


def route_after_hitl(state: SupportState) -> str:
    """
    Routes to supervisor_node after HITL review regardless of approval outcome.
    Supervisor handles both approved and rejected responses differently.
    """
    return "supervisor_node"