HIGH_RISK_KEYWORDS = [
    "refund",
    "cancel",
    "cancellation",
    "close account",
    "account closure",
    "compensation",
    "escalate",
    "escalation",
    "speak to manager",
    "talk to manager"
]

def check_requires_approval(query: str) -> bool:
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in HIGH_RISK_KEYWORDS)


def request_human_approval(state) -> tuple:
    query = state["query"]
    agent_response = state.get("agent_response", "")
    customer_id = state["customer_id"]

    print("\n" + "="*60)
    print("HUMAN APPROVAL REQUIRED")
    print("="*60)
    print(f"Customer ID: {customer_id}")
    print(f"Customer Query: {query}")
    print(f"Agent Response: {agent_response}")
    print("="*60)

    escalation_reason = f"High-risk request detected: {query}"

    while True:
        decision = input("\nApprove this request? (yes/no): ").strip().lower()
        if decision in ["yes", "no"]:
            break
        print("Please enter 'yes' or 'no'")

    if decision == "yes":
        return "approved", escalation_reason
    else:
        return "rejected", escalation_reason