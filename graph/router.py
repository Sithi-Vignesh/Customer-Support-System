from graph.state import SupportState

def route_by_intent(state: SupportState) -> str:
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
    approval_status = state.get("approval_status", "approved")
    
    if approval_status in ["approved", "auto_approved"]:
        return "supervisor_node"
    elif approval_status == "rejected":
        return "supervisor_node"
    else:
        return "supervisor_node"