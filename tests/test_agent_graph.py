"""Unit tests for the NASA PSI LangGraph AI Copilot engine.

Validates graph compilation, topology, scenario context handling,
and graceful unauthenticated error propagation.

Authors: Cesia Burgos (Chief Executive Officer, CEO) & Ethan Bula (Chief Operating Officer, COO).
"""

from __future__ import annotations

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from agent.graph import app_graph
from agent.state import CombustionAgentState


def test_graph_structure() -> None:
    """Verify that the StateGraph compiles with the required agent node and entry point."""
    assert app_graph is not None
    assert "agent" in app_graph.nodes
    # Verify StateGraph schema attributes
    assert hasattr(app_graph, "invoke")


def test_unauthenticated_clean_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that invoking the graph without an API key produces an explicit auth notice."""
    # Ensure neither GEMINI_API_KEY nor GOOGLE_API_KEY is available
    monkeypatch.setenv("GEMINI_API_KEY", "")
    monkeypatch.setenv("GOOGLE_API_KEY", "")

    state_input: CombustionAgentState = {
        "messages": [
            HumanMessage(content="What is the microgravity LOC for PMMA in BASS?")
        ],
        "current_scenario": {
            "o2_pct": 18.0,
            "u_inf_cm_s": 2.0,
            "fuel": "PMMA (Acrylic Slab)",
            "flow_direction": "Concurrent",
            "loc_margin_pct": 1.5,
            "flame_spread_cm_s": 0.08,
        },
        "selected_investigation": {
            "accession": "PSI-26",
            "title": "Burning and Suppression of Solids (BASS)",
            "category": "Spacecraft Fire Safety",
            "platform": "International Space Station (ISS)",
            "hardware": "Microgravity Science Glovebox (MSG)",
        },
        "error": None,
    }

    result = app_graph.invoke(state_input)

    assert "messages" in result
    assert len(result["messages"]) >= 2  # HumanMessage + AIMessage

    response_msg = result["messages"][-1]
    assert isinstance(response_msg, AIMessage)
    assert "Authentication Notice" in response_msg.content
    assert "GEMINI_API_KEY" in response_msg.content
    assert result.get("error") is not None
