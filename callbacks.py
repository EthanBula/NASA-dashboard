"""Reactive callbacks engine for the NASA PSI Microgravity Flammability & Fire Safety Dashboard.

Handles:
- Action 6.1: Fuel selection & reactive flow direction lockout.
- Action 6.2: Section 1 environmental sliders & real-time dashboard reactivity.
- Action 6.3: Section 2 literature search, category, and platform filtering.
- Action 6.4: Section 2 master-detail scientific viewer & 24 dedicated charts.
- Action 6.5: Section 3 AI Copilot chat transmission & LangGraph execution.
- Action 6.6: Section 4 NASA PSI dataset JSON download.

Authors: Cesia Burgos (Chief Executive Officer, CEO) & Ethan Bula (Chief Operating Officer, COO).
"""

from __future__ import annotations

import json
import os
from typing import Any

import dash_bootstrap_components as dbc
import numpy as np
from dash import ALL, Input, Output, State, ctx, dcc, html
from dash.exceptions import PreventUpdate
from langchain_core.messages import HumanMessage

from agent.graph import app_graph
from agent.state import CombustionAgentState
from data.benchmark_data import SAFFIRE_TIMESERIES
from data.investigation_charts import get_investigation_chart
from data.microgravity_models import (
    compute_aerosol_distribution,
    compute_flame_spread_rate,
    compute_kpis,
    compute_loc,
)

# Load dataset into memory for fast lookup
_DATA_PATH = os.path.join(
    os.path.dirname(__file__), "data", "psi_combustion_science.json"
)
_INVESTIGATIONS: list[dict[str, Any]] = []
if os.path.exists(_DATA_PATH):
    with open(_DATA_PATH, "r", encoding="utf-8") as _f:
        _INVESTIGATIONS = json.load(_f)

_INVESTIGATIONS_BY_ACCESSION: dict[str, dict[str, Any]] = {
    inv["accession"]: inv for inv in _INVESTIGATIONS
}

SOLID_FUELS = {"PMMA", "SIBAL_Fabric", "Nomex", "Silicone"}

HUD_LAYOUT_BASE: dict[str, Any] = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(15, 23, 42, 0.6)",
    "height": 340,
    "font": {
        "family": "Inter, -apple-system, sans-serif",
        "color": "#f8fafc",
        "size": 11,
    },
    "margin": {"l": 65, "r": 65, "t": 48, "b": 48},
    "hovermode": "x unified",
    "hoverlabel": {
        "bgcolor": "#0b1329",
        "bordercolor": "#d91119",
        "font": {
            "family": "Inter, -apple-system, sans-serif",
            "color": "#f8fafc",
            "size": 11,
        },
    },
    "xaxis": {
        "gridcolor": "rgba(255, 255, 255, 0.08)",
        "zerolinecolor": "rgba(217, 17, 25, 0.3)",
        "showgrid": True,
        "zeroline": True,
        "tickfont": {"size": 10, "color": "#94a3b8"},
        "title": {"standoff": 10},
    },
    "yaxis": {
        "gridcolor": "rgba(255, 255, 255, 0.08)",
        "zerolinecolor": "rgba(217, 17, 25, 0.3)",
        "showgrid": True,
        "zeroline": True,
        "tickfont": {"size": 10, "color": "#94a3b8"},
        "title": {"standoff": 10},
    },
}


# ==============================================================================
# Pure Computational Helpers for Callbacks & Verification Testing
# ==============================================================================


def compute_fuel_lockout(
    fuel: str,
) -> tuple[list[dict[str, Any]], str, str]:
    """Action 6.1 helper: Compute options, CSS class, and tooltip text for fuel direction."""
    if fuel in SOLID_FUELS:
        options = [
            {
                "label": "Concurrent (Downwind)",
                "value": "Concurrent",
                "disabled": False,
            },
            {"label": "Opposed (Upwind)", "value": "Opposed", "disabled": False},
        ]
        class_name = "flow-toggle-enabled"
        tooltip_text = (
            "Forced airflow orientation relative to solid flame propagation front."
        )
    else:
        options = [
            {"label": "Concurrent (Downwind)", "value": "Concurrent", "disabled": True},
            {"label": "Opposed (Upwind)", "value": "Opposed", "disabled": True},
        ]
        class_name = "flow-toggle-disabled opacity-50"
        tooltip_text = (
            "Not applicable (Spherical symmetry and radial diffusion in microgravity)"
        )
    return options, class_name, tooltip_text


def compute_dashboard_telemetry(
    o2_pct: float,
    u_inf_cm_s: float,
    fuel: str,
    flow_direction: str,
) -> tuple[
    str,
    str,
    str,
    str,
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    """Action 6.2 helper: Compute KPIs and build 4 fast dict-based figures (< 100 ms)."""
    kpis = compute_kpis(o2_pct, u_inf_cm_s, fuel, flow_direction)

    margin_val = kpis["loc_margin_pct"]
    margin_str = f"{margin_val:+.1f}"
    spread_str = f"{kpis['flame_spread_mm_s']:.3f}"
    hrr_str = f"{kpis['peak_hrr_kw']:.2f}"
    detect_str = f"{kpis['smoke_detection_time_s']:.1f}"

    # G1: LOC U-Curve & Operating Point
    u_vals = np.linspace(0.2, 15.0, 30).tolist()
    loc_vals = [compute_loc(u, fuel) for u in u_vals]
    curr_loc = compute_loc(u_inf_cm_s, fuel)
    pt_color = "#d91119" if o2_pct >= curr_loc else "#0cb64d"
    pt_status = "Flammable" if o2_pct >= curr_loc else "Below LOC"

    g1_fig = {
        "data": [
            {
                "type": "scatter",
                "x": u_vals,
                "y": loc_vals,
                "mode": "lines",
                "name": "LOC Boundary",
                "line": {"color": "#d91119", "width": 2},
            },
            {
                "type": "scatter",
                "x": [u_inf_cm_s],
                "y": [o2_pct],
                "mode": "markers",
                "name": f"Operating Point ({pt_status})",
                "marker": {"size": 11, "color": pt_color},
            },
        ],
        "layout": {
            **HUD_LAYOUT_BASE,
            "title": {
                "text": f"G1: Flammability Boundary & LOC ({fuel})",
                "font": {"size": 13, "color": "#fbdc08"},
            },
            "xaxis": {
                **HUD_LAYOUT_BASE["xaxis"],
                "title": {"text": "Forced Airflow u_inf (cm/s)"},
            },
            "yaxis": {
                **HUD_LAYOUT_BASE["yaxis"],
                "title": {"text": "Oxygen Concentration (% O₂)"},
            },
        },
    }

    # G2: Projected Flame Spread Rate
    vf_vals = [
        compute_flame_spread_rate(u, o2_pct, fuel, flow_direction) for u in u_vals
    ]
    g2_fig = {
        "data": [
            {
                "type": "scatter",
                "x": u_vals,
                "y": vf_vals,
                "mode": "lines",
                "name": "Spread Rate",
                "line": {"color": "#fbdc08", "width": 2},
            },
            {
                "type": "scatter",
                "x": [u_inf_cm_s],
                "y": [kpis["flame_spread_mm_s"]],
                "mode": "markers",
                "name": "Current Vf",
                "marker": {"size": 10, "color": "#fbdc08"},
            },
        ],
        "layout": {
            **HUD_LAYOUT_BASE,
            "title": {
                "text": f"G2: Flame Spread Rate vs Forced Flow ({fuel})",
                "font": {"size": 13, "color": "#fbdc08"},
            },
            "xaxis": {
                **HUD_LAYOUT_BASE["xaxis"],
                "title": {"text": "Forced Airflow u_inf (cm/s)"},
            },
            "yaxis": {
                **HUD_LAYOUT_BASE["yaxis"],
                "title": {"text": "Spread Rate (mm/s)"},
            },
        },
    }

    # G3: Spacecraft Cabin Fire Dynamics (Scaled by Thornton-Huggett Principle & O2 flux)
    fuel_multipliers = {
        "PMMA": 1.25,
        "SIBAL_Fabric": 1.0,
        "Nomex": 0.65,
        "Silicone": 0.85,
        "n-Heptane": 1.40,
        "Methane": 1.30,
        "Ethylene": 1.45,
    }
    f_fuel = fuel_multipliers.get(fuel, 1.0)

    # HRR scaling with oxidizer concentration and convective mass flux
    hrr_scale = ((o2_pct / 21.0) ** 1.25) * (1.0 + 0.06 * (u_inf_cm_s - 2.0)) * f_fuel
    hrr_vals = [round(max(0.0, val * hrr_scale), 2) for val in SAFFIRE_TIMESERIES["hrr_kw"]]

    # CO generation surges under incomplete combustion (lower O2, low u_inf)
    # Freezing of CO + OH -> CO2 + H at lower microgravity flame temperatures
    o2_deficit = max(0.0, 21.0 - o2_pct)
    flow_deficit = max(0.0, 2.0 - u_inf_cm_s)
    co_scale = (1.0 + 0.14 * o2_deficit + 0.08 * flow_deficit) * f_fuel
    co_vals = [round(max(0.0, val * co_scale), 1) for val in SAFFIRE_TIMESERIES["co_ppm"]]

    g3_fig = {
        "data": [
            {
                "type": "scatter",
                "x": SAFFIRE_TIMESERIES["time_s"],
                "y": hrr_vals,
                "mode": "lines",
                "name": "HRR (kW)",
                "line": {"color": "#d91119", "width": 2},
            },
            {
                "type": "scatter",
                "x": SAFFIRE_TIMESERIES["time_s"],
                "y": co_vals,
                "mode": "lines",
                "name": "CO Concentration (ppm)",
                "yaxis": "y2",
                "line": {"color": "#0cb64d", "width": 1.5, "dash": "dash"},
            },
        ],
        "layout": {
            **HUD_LAYOUT_BASE,
            "title": {
                "text": f"G3: Spacecraft Cabin Fire Dynamics ({fuel})",
                "font": {"size": 13, "color": "#fbdc08"},
            },
            "xaxis": {**HUD_LAYOUT_BASE["xaxis"], "title": {"text": "Flight Time (s)"}},
            "yaxis": {
                **HUD_LAYOUT_BASE["yaxis"],
                "title": {"text": "Heat Release Rate (kW)"},
            },
            "yaxis2": {
                "title": {"text": "CO (ppm)", "font": {"color": "#0cb64d"}},
                "overlaying": "y",
                "side": "right",
                "showgrid": False,
                "tickfont": {"color": "#0cb64d"},
            },
        },
    }

    # G4: Aerosol Distribution (Scaled by SAME / Smoluchowski coagulation & dilution)
    mat = (
        "Pyrolyzing_PMMA"
        if fuel == "PMMA"
        else (
            "Silicone_Overheat"
            if fuel == "Silicone"
            else ("Overheated_Teflon_Wire" if fuel == "Nomex" else "Smoldering_Cotton")
        )
    )
    dp, dist = compute_aerosol_distribution(mat, u_inf=u_inf_cm_s, o2_pct=o2_pct)
    g4_fig = {
        "data": [
            {
                "type": "scatter",
                "x": dp.tolist(),
                "y": dist.tolist(),
                "mode": "lines",
                "name": "Aerosol Density",
                "line": {"color": "#0cb64d", "width": 2},
            }
        ],
        "layout": {
            **HUD_LAYOUT_BASE,
            "title": {
                "text": f"G4: Smoke Aerosol Size Distribution ({mat})",
                "font": {"size": 13, "color": "#fbdc08"},
            },
            "xaxis": {
                **HUD_LAYOUT_BASE["xaxis"],
                "type": "log",
                "title": {"text": "Particle Diameter d_p (µm, Log)"},
            },
            "yaxis": {
                **HUD_LAYOUT_BASE["yaxis"],
                "title": {"text": "Concentration dN/dlog(d_p) (#/cm³)"},
            },
        },
    }

    scenario_state = {
        "o2_pct": o2_pct,
        "u_inf_cm_s": u_inf_cm_s,
        "fuel": fuel,
        "flow_direction": flow_direction,
        "loc_margin_pct": margin_val,
        "flame_spread_cm_s": round(kpis["flame_spread_mm_s"] / 10.0, 4),
    }

    return (
        margin_str,
        spread_str,
        hrr_str,
        detect_str,
        g1_fig,
        g2_fig,
        g3_fig,
        g4_fig,
        scenario_state,
    )


def filter_investigation_records(
    search_query: str | None,
    category: str | None,
    platform: str | None,
) -> list[dict[str, Any]]:
    """Action 6.3 helper: Filter investigation records based on search criteria."""
    query = (search_query or "").strip().lower()
    cat = category or "ALL"
    plat = platform or "ALL"

    results: list[dict[str, Any]] = []
    for inv in _INVESTIGATIONS:
        if cat != "ALL" and inv.get("category") != cat:
            continue
        if plat != "ALL" and inv.get("platform") != plat:
            continue
        if query:
            searchable = " ".join(
                [
                    inv.get("title", ""),
                    inv.get("acronym", ""),
                    inv.get("accession", ""),
                    inv.get("principal_investigator", ""),
                    inv.get("experiment_hardware", ""),
                    inv.get("category", ""),
                    inv.get("platform", ""),
                    inv.get("objectives", ""),
                ]
            ).lower()
            if query not in searchable:
                continue
        results.append(inv)
    return results


def build_investigation_detail_component(inv: dict[str, Any]) -> html.Div:
    """Action 6.4 helper: Render structured scientific tabs and publications table."""
    pubs = inv.get("publications", [])

    # Format publications rows
    pub_rows = []
    for pub in pubs:
        doi = (pub.get("doi") or "").strip()
        doi_elem = (
            html.A(
                f"https://doi.org/{doi}",
                href=f"https://doi.org/{doi}",
                target="_blank",
                className="doi-link small",
            )
            if doi
            else html.Span(
                "No DOI available (NASA Technical Report / Archival Paper)",
                className="text-muted small fst-italic",
            )
        )
        author_str = pub.get("authorList") or pub.get("authors") or "N/A"
        pub_rows.append(
            html.Div(
                [
                    html.Div(
                        pub.get("title", "Untitled Article"),
                        className="fw-semibold text-white small",
                    ),
                    html.Div(
                        f"Authors: {author_str}",
                        className="text-muted small mb-1",
                    ),
                    doi_elem,
                ],
                className="mb-3 pb-2 border-bottom border-secondary",
            )
        )

    if not pub_rows:
        pub_rows.append(
            html.Div(
                "No peer-reviewed publications indexed for this accession.",
                className="text-muted small",
            )
        )

    return html.Div(
        [
            # Header
            html.Div(
                [
                    html.Span(inv["accession"], className="badge-accession me-2"),
                    html.Span(inv.get("category", ""), className="badge-category me-2"),
                    html.Span(
                        inv.get("platform", ""), className="badge-platform ms-auto"
                    ),
                ],
                className="d-flex align-items-center mb-2",
            ),
            html.H5(inv.get("title", "Untitled"), className="text-white fw-bold mb-2"),
            # Metadata Grid
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Span(
                                "Principal Investigator: ", className="text-muted small"
                            ),
                            html.Span(
                                inv.get("principal_investigator", "N/A"),
                                className="text-info small fw-semibold",
                            ),
                        ],
                        xs=12,
                        md=6,
                        className="mb-1",
                    ),
                    dbc.Col(
                        [
                            html.Span("NASA Center: ", className="text-muted small"),
                            html.Span(
                                inv.get("monitoring_center", "N/A"),
                                className="text-white small",
                            ),
                        ],
                        xs=12,
                        md=6,
                        className="mb-1",
                    ),
                    dbc.Col(
                        [
                            html.Span(
                                "Experiment Hardware: ", className="text-muted small"
                            ),
                            html.Span(
                                inv.get("experiment_hardware", "N/A"),
                                className="text-white small",
                            ),
                        ],
                        xs=12,
                        className="mb-3",
                    ),
                ]
            ),
            # Scientific Tabs
            dbc.Tabs(
                [
                    dbc.Tab(
                        html.Div(
                            inv.get(
                                "objectives", "No explicit flight objectives specified."
                            ),
                            className="scientific-tab-content",
                        ),
                        label="Objectives",
                        tab_id="tab-objectives",
                    ),
                    dbc.Tab(
                        html.Div(
                            inv.get(
                                "hypothesis",
                                "No explicit scientific hypothesis specified.",
                            ),
                            className="scientific-tab-content",
                        ),
                        label="Hypothesis",
                        tab_id="tab-hypothesis",
                    ),
                    dbc.Tab(
                        html.Div(
                            inv.get(
                                "approach",
                                "No explicit experimental approach documented.",
                            ),
                            className="scientific-tab-content",
                        ),
                        label="Approach",
                        tab_id="tab-approach",
                    ),
                    dbc.Tab(
                        html.Div(
                            inv.get(
                                "research_impacts",
                                "No explicit research impacts or Earth benefits documented.",
                            ),
                            className="scientific-tab-content",
                        ),
                        label="Earth / Space Impacts",
                        tab_id="tab-impacts",
                    ),
                    dbc.Tab(
                        html.Div(
                            pub_rows,
                            className="scientific-tab-content doi-table-container",
                        ),
                        label=f"Publications ({len(pubs)})",
                        tab_id="tab-publications",
                    ),
                ],
                active_tab="tab-objectives",
            ),
        ]
    )


# ==============================================================================
# Master Callback Registration
# ==============================================================================


def register_callbacks(app: Any) -> None:
    """Wire all 6 reactive callbacks into the Dash application instance."""

    # --------------------------------------------------------------------------
    # Action 6.1: Flow Direction Reactive Lockout
    # --------------------------------------------------------------------------
    @app.callback(
        Output("toggle-flow-direction", "options"),
        Output("toggle-flow-direction", "className"),
        Output("tooltip-flow-direction", "children"),
        Input("dropdown-fuel", "value"),
    )
    def handle_fuel_selection_lockout(
        fuel: str,
    ) -> tuple[list[dict[str, Any]], str, str]:
        return compute_fuel_lockout(fuel)

    # --------------------------------------------------------------------------
    # Action 6.2: Section 1 Sliders & Dashboard Reactivity
    # --------------------------------------------------------------------------
    @app.callback(
        Output("kpi-margin", "children"),
        Output("kpi-spread", "children"),
        Output("kpi-hrr", "children"),
        Output("kpi-detection", "children"),
        Output("graph-g1-loc", "figure"),
        Output("graph-g2-spread", "figure"),
        Output("graph-g3-saffire", "figure"),
        Output("graph-g4-aerosol", "figure"),
        Output("store-scenario", "data"),
        Input("slider-o2", "value"),
        Input("slider-velocity", "value"),
        Input("dropdown-fuel", "value"),
        Input("toggle-flow-direction", "value"),
    )
    def handle_dashboard_updates(
        o2_pct: float,
        u_inf: float,
        fuel: str,
        flow_dir: str,
    ) -> tuple[
        str,
        str,
        str,
        str,
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
    ]:
        return compute_dashboard_telemetry(
            float(o2_pct or 21.0),
            float(u_inf or 2.0),
            fuel or "PMMA",
            flow_dir or "Concurrent",
        )

    # --------------------------------------------------------------------------
    # Action 6.3: Section 2 Literature Search & Filtering
    # --------------------------------------------------------------------------
    @app.callback(
        Output("container-investigation-list", "children"),
        Output("badge-investigation-count", "children"),
        Input("input-search", "value"),
        Input("dropdown-category", "value"),
        Input("dropdown-platform", "value"),
    )
    def handle_literature_filter(
        search_val: str | None,
        category_val: str | None,
        platform_val: str | None,
    ) -> tuple[list[html.Div], str]:
        filtered_invs = filter_investigation_records(
            search_val, category_val, platform_val
        )
        count_str = f"{len(filtered_invs)} / {len(_INVESTIGATIONS)} Listed"

        card_elements = []
        for inv in filtered_invs:
            acc = inv["accession"]
            card_elements.append(
                html.Div(
                    id={"type": "investigation-card", "index": acc},
                    n_clicks=0,
                    className="investigation-card-item",
                    children=[
                        html.Div(
                            [
                                html.Span(acc, className="badge-accession"),
                                html.Span(
                                    inv.get("category", ""), className="badge-category"
                                ),
                            ],
                            className="mb-1 d-flex align-items-center",
                        ),
                        html.Div(
                            inv.get("title", "Untitled"),
                            className="text-white fw-bold small mb-1",
                        ),
                        html.Div(
                            [
                                html.Span(
                                    f"PI: {inv.get('principal_investigator', 'N/A')}",
                                    className="text-muted small me-2",
                                ),
                                html.Span(
                                    inv.get("platform", ""),
                                    className="badge-platform ms-auto",
                                ),
                            ],
                            className="d-flex align-items-center text-muted small",
                        ),
                    ],
                )
            )

        if not card_elements:
            card_elements.append(
                html.Div(
                    "No flight investigations match the selected filters.",
                    className="text-muted text-center p-3 small",
                )
            )

        return card_elements, count_str

    # --------------------------------------------------------------------------
    # Action 6.4: Section 2 Master-Detail Selection & Dedicated Charts
    # --------------------------------------------------------------------------
    @app.callback(
        Output("container-investigation-detail", "children"),
        Output("graph-investigation-detail", "figure"),
        Output("store-selected-investigation", "data"),
        Input({"type": "investigation-card", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def handle_investigation_selection(
        n_clicks_list: list[int | None],
    ) -> tuple[Any, Any, Any]:
        # Handle initial empty edge case
        if not ctx.triggered_id or not any(n_clicks_list):
            raise PreventUpdate

        # Extract selected accession from triggered pattern dict
        if isinstance(ctx.triggered_id, dict):
            selected_accession = ctx.triggered_id.get("index")
        else:
            raise PreventUpdate

        inv = _INVESTIGATIONS_BY_ACCESSION.get(selected_accession)
        if not inv:
            raise PreventUpdate

        detail_component = build_investigation_detail_component(inv)
        dedicated_chart = get_investigation_chart(selected_accession)

        selected_store_data = {
            "accession": inv.get("accession"),
            "title": inv.get("title"),
            "category": inv.get("category"),
            "platform": inv.get("platform"),
            "hardware": inv.get("experiment_hardware"),
            "objectives": inv.get("objectives"),
            "hypothesis": inv.get("hypothesis"),
        }

        return detail_component, dedicated_chart, selected_store_data

    # --------------------------------------------------------------------------
    # Action 6.5: Section 3 AI Copilot Synchronous Chat Execution
    # --------------------------------------------------------------------------
    @app.callback(
        Output("chat-feed-container", "children"),
        Output("chat-input", "value"),
        Output("agent-loading-output", "children"),
        Input("chat-send-btn", "n_clicks"),
        Input("chat-input", "n_submit"),
        Input("pill-1", "n_clicks"),
        Input("pill-2", "n_clicks"),
        Input("pill-3", "n_clicks"),
        State("chat-input", "value"),
        State("store-scenario", "data"),
        State("store-selected-investigation", "data"),
        State("chat-feed-container", "children"),
        prevent_initial_call=True,
    )
    def handle_copilot_chat(
        _btn_clicks: int | None,
        _submit_n: int | None,
        _pill1_clicks: int | None,
        _pill2_clicks: int | None,
        _pill3_clicks: int | None,
        chat_val: str | None,
        scenario_data: dict[str, Any] | None,
        investigation_data: dict[str, Any] | None,
        current_feed: list[Any] | None,
    ) -> tuple[list[Any], str, str]:
        trigger = ctx.triggered_id
        if not trigger:
            raise PreventUpdate

        # Determine prompt based on trigger source
        if trigger == "pill-1":
            prompt = "Explain the flammability risk and margin for the current active scenario."
        elif trigger == "pill-2":
            prompt = (
                "Synthesize the objectives, hypothesis, and key findings of the currently "
                "selected PSI flight investigation."
            )
        elif trigger == "pill-3":
            prompt = (
                "Why does carbon monoxide (CO) surge during microgravity smoldering and flame spread "
                "compared to Earth gravity?"
            )
        else:
            prompt = (chat_val or "").strip()
            if not prompt:
                raise PreventUpdate

        # Render user message bubble
        user_bubble = html.Div(prompt, className="chat-bubble chat-bubble-user")

        # Invoke LangGraph engine
        graph_input: CombustionAgentState = {
            "messages": [HumanMessage(content=prompt)],
            "current_scenario": scenario_data or {},
            "selected_investigation": investigation_data or {},
            "error": None,
        }

        agent_result = app_graph.invoke(graph_input)
        response_msg = agent_result["messages"][-1]
        agent_reply_text = (
            response_msg.content
            if hasattr(response_msg, "content")
            else str(response_msg)
        )

        agent_bubble = html.Div(
            [
                html.Strong(
                    "NASA PSI AI Copilot",
                    className="d-block mb-1 small",
                    style={"color": "#fbdc08"},
                ),
                dcc.Markdown(agent_reply_text, mathjax=True),
            ],
            className="chat-bubble chat-bubble-agent",
        )

        feed_list = list(current_feed or [])
        feed_list.append(user_bubble)
        feed_list.append(agent_bubble)

        return feed_list, "", ""

    # --------------------------------------------------------------------------
    # Action 6.6: Section 4 Dataset Download
    # --------------------------------------------------------------------------
    @app.callback(
        Output("download-json", "data"),
        Input("btn-download-json", "n_clicks"),
        prevent_initial_call=True,
    )
    def handle_dataset_download(n_clicks: int | None) -> Any:
        if not n_clicks:
            raise PreventUpdate
        return dcc.send_file(_DATA_PATH)
