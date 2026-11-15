"""LangGraph orchestration engine for the NASA PSI AI Copilot.

Compiles a stateful graph integrating Google Gemini models with automatic fallback,
scenario context injection, and strict authentication enforcement.

Authors: Cesia Burgos (Chief Executive Officer, CEO) & Ethan Bula (Chief Operating Officer, COO).
"""

from __future__ import annotations

import os
import re
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph

from agent.prompts import SYSTEM_PROMPT
from agent.state import CombustionAgentState

load_dotenv()


def format_runtime_context(
    current_scenario: dict[str, Any] | None,
    selected_investigation: dict[str, Any] | None,
) -> str:
    """Format live dashboard scenario and literature metadata into prompt context.

    Args:
        current_scenario: Active environmental parameters from Section 1 sliders.
        selected_investigation: Active flight investigation metadata from Section 2.

    Returns:
        Formatted multi-line context string to append to the system prompt.
    """
    parts = ["\n\n--- ACTIVE DASHBOARD RUNTIME CONTEXT ---"]

    if current_scenario:
        parts.append(
            "Current Environmental Scenario:\n"
            f"- Ambient Oxygen Concentration: {current_scenario.get('o2_pct', 'N/A')}% O2\n"
            f"- Forced Airflow Velocity: {current_scenario.get('u_inf_cm_s', 'N/A')} cm/s\n"
            f"- Fuel Material: {current_scenario.get('fuel', 'N/A')}\n"
            f"- Flow Direction: {current_scenario.get('flow_direction', 'N/A')}\n"
            f"- Flammability Margin (Δ% O2): {current_scenario.get('loc_margin_pct', 'N/A')}%\n"
            f"- Predicted Spread Rate: {current_scenario.get('flame_spread_cm_s', 'N/A')} cm/s"
        )
    else:
        parts.append("Current Environmental Scenario: Not initialized.")

    if selected_investigation:
        parts.append(
            "Selected PSI Flight Investigation:\n"
            f"- Accession: {selected_investigation.get('accession', 'N/A')}\n"
            f"- Title: {selected_investigation.get('title', 'N/A')}\n"
            f"- Category: {selected_investigation.get('category', 'N/A')}\n"
            f"- Platform: {selected_investigation.get('platform', 'N/A')}\n"
            f"- Hardware: {selected_investigation.get('hardware', 'N/A')}\n"
            f"- Objectives: {selected_investigation.get('objectives', 'N/A')}\n"
            f"- Hypothesis: {selected_investigation.get('hypothesis', 'N/A')}"
        )
    else:
        parts.append("Selected PSI Flight Investigation: None currently selected.")

    parts.append("--- END RUNTIME CONTEXT ---\n")
    return "\n\n".join(parts)


def get_llm(api_key: str | None = None) -> Any:
    """Initialize Gemini model chain with 4-level priority fallback.

    Priority order:
    1. gemini-3.8-flash (Primary)
    2. gemini-3.6-flash (Secondary fallback)
    3. gemini-3.5-flash-lite (Tertiary fallback)
    4. gemini-3.1-flash-lite (Quaternary fallback)

    All models configured with max_retries=0 to prevent tenacity loops burning quota.

    Args:
        api_key: Optional Gemini API key string.

    Returns:
        Runnable model with chained fallback bindings.
    """
    llm_38 = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0.2,
        timeout=10.0,
        max_retries=0,
        google_api_key=api_key,
    )
    llm_36 = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.2,
        timeout=10.0,
        max_retries=0,
        google_api_key=api_key,
    )
    llm_35_lite = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0.2,
        timeout=10.0,
        max_retries=0,
        google_api_key=api_key,
    )
    llm_31_lite = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0.2,
        timeout=10.0,
        max_retries=0,
        google_api_key=api_key,
    )
    return llm_38.with_fallbacks([llm_36, llm_35_lite, llm_31_lite])


def _extract_content_text(content: Any) -> str:
    """Extract plain text string from model content whether string or list of dicts."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
        return "\n".join(parts)
    return str(content)


def _clean_latex_syntax(text: str) -> str:
    """Clean raw LaTeX math delimiters into standard Unicode scientific notation."""
    if not text:
        return ""
    s = text
    s = re.sub(r"\$(?:O_\{?2\}?|O_\{2,\s*\\text\{ambient\}\})\$", "O₂", s)
    s = re.sub(r"\$(?:CO_\{?2\}?)\$", "CO₂", s)
    s = re.sub(r"\$(?:u_\\infty|u_\{?\\infty\}?)\$", "u_inf", s)
    s = re.sub(r"\$\\Delta\s*\\?%\s*O_\{?2\}?\$", "Δ% O₂", s)
    s = re.sub(r"\$\\Delta\s*O_\{?2\}?\$", "Δ% O₂", s)
    # Generic dollar stripper for simple single-variable math delimiters like $O_2$ or $V_f$
    s = re.sub(
        r"\$([^$\n]+)\$",
        lambda m: (
            m.group(1)
            .replace(r"\text{ambient}", "ambient")
            .replace(r"\text", "")
            .replace(r"\infty", "∞")
            .replace(r"\Delta", "Δ")
            .replace("{", "")
            .replace("}", "")
            .replace("_", "")
            .strip()
        ),
        s,
    )
    return s


def call_model(state: CombustionAgentState) -> dict[str, Any]:
    """Execute model reasoning node or return explicit authentication notice.

    Args:
        state: Current LangGraph conversation and scenario state.

    Returns:
        Partial state dictionary with appended AIMessage response.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return {
            "messages": [
                AIMessage(
                    content=(
                        "**Authentication Notice:** A valid `GEMINI_API_KEY` is required to communicate "
                        "with the NASA PSI AI Copilot. Please set your key in the environment to activate "
                        "full conversational reasoning."
                    )
                )
            ],
            "error": "Authentication error: Missing GEMINI_API_KEY",
        }

    try:
        llm = get_llm(api_key=api_key)
        context_str = format_runtime_context(
            state.get("current_scenario"),
            state.get("selected_investigation"),
        )
        system_instruction = SystemMessage(content=SYSTEM_PROMPT + context_str)
        messages = [system_instruction] + list(state.get("messages", []))

        response = llm.invoke(messages)
        raw_text = _extract_content_text(response.content)
        content_text = _clean_latex_syntax(raw_text)
        return {"messages": [AIMessage(content=content_text)], "error": None}
    except Exception as exc:  # noqa: BLE001 - Catch all network, timeout, and API failures gracefully
        err_msg = str(exc)
        if "429" in err_msg or "resource_exhausted" in err_msg.lower() or "quota" in err_msg.lower():
            content = (
                "**Quota / Rate Limit Alert:** The daily request quota for Google Gemini API models has been reached. "
                "Please check your Google AI Studio plan or retry when your quota resets."
            )
        elif "timeout" in err_msg.lower() or "deadline" in err_msg.lower():
            content = (
                "**Timeout Alert:** The reasoning request exceeded the 10-second limit. "
                "Microgravity physics computation and network latency caused a timeout. "
                "Please retry with a more specific query."
            )
        else:
            content = (
                f"**Service Notice:** Unable to reach Google Gemini API ({exc.__class__.__name__}). "
                "Please check your API key, quotas, or network connection."
            )
        return {
            "messages": [AIMessage(content=content)],
            "error": err_msg,
        }


# Assemble and compile the LangGraph workflow
builder = StateGraph(CombustionAgentState)
builder.add_node("agent", call_model)
builder.set_entry_point("agent")
builder.add_edge("agent", END)
app_graph = builder.compile()
