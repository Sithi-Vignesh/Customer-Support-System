"""
state.py
Defines the shared state structure (SupportState) used across all LangGraph nodes.
Each field represents a piece of information that flows through the graph.
"""
from typing import TypedDict, Optional, List

class SupportState(TypedDict, total=False):
    """Central state object passed between all nodes in the LangGraph workflow."""
    customer_id: str                          # Unique customer identifier
    query: str                                # Customer's input query
    customer_name: Optional[str]              # Customer's name (if provided)
    intent: Optional[str]                     # Classified intent: Sales/Technical/Billing/Account/Memory
    retrieved_context: Optional[str]          # RAG retrieved content from knowledge base
    agent_response: Optional[str]             # Draft response from specialized agent
    requires_approval: bool                   # Flag for HITL approval requirement
    approval_status: Optional[str]            # approved / rejected / pending
    final_response: Optional[str]             # Supervisor validated final response
    conversation_history: Optional[List[dict]] # Customer's past interactions
    escalation_reason: Optional[str]          # Reason for HITL escalation