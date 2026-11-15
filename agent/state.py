"""State schema for the NASA PSI Combustion Science LangGraph AI Copilot.

Authors: Cesia Burgos (Chief Executive Officer, CEO) & Ethan Bula (Chief Operating Officer, COO).
"""

from __future__ import annotations

from typing import Annotated, Any

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class CombustionAgentState(TypedDict):
    """LangGraph state representation for the conversational AI Copilot.

    Attributes:
        messages: Append-only sequence of conversation messages between the user and Copilot.
        current_scenario: Real-time dashboard parameters (e.g., o2_pct, u_inf_cm_s, fuel, flow_direction).
        selected_investigation: Active NASA PSI flight investigation metadata selected in Section 2.
        error: Optional error message string if an execution failure occurs.
    """

    messages: Annotated[list[BaseMessage], add_messages]
    current_scenario: dict[str, Any]
    selected_investigation: dict[str, Any]
    error: str | None
