"""Layout smoke tests for the NASA PSI Microgravity Dashboard.

Validates that the complete Dash layout tree instantiates and all required
component identifiers for callbacks and testing exist.

Authors: Cesia Burgos (Chief Executive Officer, CEO) & Ethan Bula (Chief Operating Officer, COO).
"""

from __future__ import annotations

from typing import Any

from layout import create_layout


def _extract_component_ids(component: Any, id_set: set[str] | None = None) -> set[str]:
    """Recursively collect all component IDs within a Dash layout tree."""
    if id_set is None:
        id_set = set()

    if component is None:
        return id_set

    # Check for direct 'id' attribute
    if hasattr(component, "id") and component.id:
        if isinstance(component.id, str):
            id_set.add(component.id)
        elif isinstance(component.id, dict):
            # Pattern-matching callbacks ID dict
            id_set.add(str(component.id))

    # Recurse through children
    if hasattr(component, "children"):
        children = component.children
        if isinstance(children, list):
            for child in children:
                _extract_component_ids(child, id_set)
        else:
            _extract_component_ids(children, id_set)

    return id_set


def test_layout_rendering_and_component_ids() -> None:
    """Verify layout instantiation and assert presence of all critical component IDs."""
    layout = create_layout()
    assert layout is not None, "create_layout() returned None"

    all_ids = _extract_component_ids(layout)

    required_ids = [
        # Environmental Controls
        "slider-o2",
        "slider-velocity",
        "dropdown-fuel",
        "toggle-flow-direction",
        "tooltip-flow-direction",
        # KPI Risk Metrics
        "kpi-margin",
        "kpi-spread",
        "kpi-hrr",
        "kpi-detection",
        # Section 1 Graphs
        "graph-g1-loc",
        "graph-g2-spread",
        "graph-g3-saffire",
        "graph-g4-aerosol",
        # Section 2 Literature Explorer
        "input-search",
        "dropdown-category",
        "dropdown-platform",
        "container-investigation-list",
        "container-investigation-detail",
        "graph-investigation-detail",
        "col-investigations-list",
        "col-investigations-chart",
        "btn-toggle-list-size",
        # Section 3 AI Copilot
        "pills-container",
        "chat-feed-container",
        "chat-input",
        "chat-send-btn",
        # Section 4 Info & Provenance
        "btn-download-json",
        "download-json",
        # Stores
        "store-scenario",
        "store-selected-investigation",
        "store-literature-layout",
    ]

    missing_ids = [cid for cid in required_ids if cid not in all_ids]
    assert not missing_ids, f"Layout missing required component IDs: {missing_ids}"
