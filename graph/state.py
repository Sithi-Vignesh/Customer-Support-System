from typing import TypedDict, Optional, List

class SupportState(TypedDict, total=False):
    customer_id: str
    query: str
    customer_name: Optional[str]
    intent: Optional[str]
    retrieved_context: Optional[str]
    agent_response: Optional[str]
    requires_approval: bool
    approval_status: Optional[str]
    final_response: Optional[str]
    conversation_history: Optional[List[dict]]
    escalation_reason: Optional[str]