"""NASA PSI Microgravity Flammability & Fire Safety Dashboard - Modular UI Layout.

Authors: Cesia Burgos (Chief Executive Officer, CEO) & Ethan Bula (Chief Operating Officer, COO).
"""

from __future__ import annotations

import json
import os
from typing import Any

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html

from data.investigation_charts import apply_hud_theme


def load_investigations() -> list[dict[str, Any]]:
    """Load the enriched NASA PSI combustion science flight dataset."""
    json_path = os.path.join(
        os.path.dirname(__file__), "data", "psi_combustion_science.json"
    )
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# ==============================================================================
# Action 5.4: Sticky Top Navbar
# ==============================================================================


def build_navbar() -> dbc.Navbar:
    """Build the sticky top navigation bar with anchors to all 4 sections."""
    return dbc.Navbar(
        dbc.Container(
            [
                html.Div(
                    [
                        html.Span("🚀", className="me-2", style={"fontSize": "1.3rem"}),
                        html.Span(
                            "NASA PSI",
                            className="navbar-brand-title",
                        ),
                        html.Span("FLIGHT HUD", className="navbar-brand-badge"),
                    ],
                    className="d-flex align-items-center",
                ),
                dbc.Nav(
                    [
                        dbc.NavLink(
                            "1. Dashboard",
                            href="#dashboard",
                            className="nav-link-hud",
                            external_link=True,
                        ),
                        dbc.NavLink(
                            "2. Literature",
                            href="#literature",
                            className="nav-link-hud",
                            external_link=True,
                        ),
                        dbc.NavLink(
                            "3. AI Copilot",
                            href="#agent",
                            className="nav-link-hud",
                            external_link=True,
                        ),
                        dbc.NavLink(
                            "4. Project Info",
                            href="#info",
                            className="nav-link-hud",
                            external_link=True,
                        ),
                    ],
                    className="ms-auto d-flex flex-row",
                    navbar=True,
                ),
            ],
            fluid=True,
        ),
        className="sticky-navbar px-3",
        dark=True,
    )


# ==============================================================================
# Action 5.5: Section 1 - Environmental Dashboard (#dashboard)
# ==============================================================================


def _build_kpi_card(
    card_id: str, label: str, default_val: str, unit: str, border_variant: str = ""
) -> dbc.Col:
    """Helper to render an aerospace HUD KPI card."""
    card_class = f"hud-card hud-card-compact kpi-container {border_variant}".strip()
    return dbc.Col(
        html.Div(
            [
                html.Div(label, className="kpi-header"),
                html.Div(
                    [
                        html.Span(default_val, id=card_id, className="kpi-value"),
                        html.Span(f" {unit}", className="kpi-subtext ms-1"),
                    ],
                    className="d-flex align-items-baseline",
                ),
            ],
            className=card_class,
        ),
        xs=12,
        sm=6,
        md=3,
        className="mb-3",
    )


def build_dashboard_section() -> html.Div:
    """Build Section 1: Sliders, reactive flow toggle, 4 KPI cards, and 2x2 grid."""
    empty_fig = apply_hud_theme(go.Figure(), "Awaiting Simulation Telemetry...", "", "")

    return html.Div(
        id="dashboard",
        className="section-dashboard",
        children=[
            dbc.Container(
                [
                    # Section Header
                    html.Div(
                        [
                            html.Div(
                                "SECTION 1 // TELEMETRY & CONTROLS",
                                className="section-heading-eyebrow",
                            ),
                            html.H1(
                                "Microgravity Flammability & Fire Safety Dashboard",
                                className="section-heading-title",
                            ),
                            html.P(
                                "Simulate exploration atmosphere flammability thresholds, flame spread dynamics, "
                                "and cabin smoke detection across validated NASA ISS & Cygnus flight regimes.",
                                className="section-heading-subtitle",
                            ),
                        ]
                    ),
                    # Environmental Control Bar
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    # Oxygen Slider
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "Ambient Oxygen Concentration (% O₂)",
                                                className="hud-label",
                                            ),
                                            dcc.Slider(
                                                id="slider-o2",
                                                min=14.0,
                                                max=30.0,
                                                step=0.5,
                                                value=21.0,
                                                marks={
                                                    15: {
                                                        "label": "15%",
                                                        "style": {"color": "#94a3b8"},
                                                    },
                                                    21: {
                                                        "label": "21% (Earth)",
                                                        "style": {"color": "#0cb64d"},
                                                    },
                                                    30: {
                                                        "label": "30%",
                                                        "style": {"color": "#d91119"},
                                                    },
                                                },
                                                tooltip={
                                                    "placement": "bottom",
                                                    "always_visible": False,
                                                },
                                            ),
                                        ],
                                        xs=12,
                                        md=4,
                                        className="mb-3",
                                    ),
                                    # Airflow Velocity Slider
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "Forced Ventilation Airflow u_inf (cm/s)",
                                                className="hud-label",
                                            ),
                                            dcc.Slider(
                                                id="slider-velocity",
                                                min=0.0,
                                                max=15.0,
                                                step=0.5,
                                                value=2.0,
                                                marks={
                                                    0: {
                                                        "label": "0",
                                                        "style": {"color": "#94a3b8"},
                                                    },
                                                    2: {
                                                        "label": "2 (ISS Nom)",
                                                        "style": {"color": "#0cb64d"},
                                                    },
                                                    10: {
                                                        "label": "10",
                                                        "style": {"color": "#fbdc08"},
                                                    },
                                                    15: {
                                                        "label": "15 cm/s",
                                                        "style": {"color": "#d91119"},
                                                    },
                                                },
                                                tooltip={
                                                    "placement": "bottom",
                                                    "always_visible": False,
                                                },
                                            ),
                                        ],
                                        xs=12,
                                        md=4,
                                        className="mb-3",
                                    ),
                                    # Fuel Selection & Flow Direction
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "Fuel Material / Reactant",
                                                className="hud-label",
                                            ),
                                            dcc.Dropdown(
                                                id="dropdown-fuel",
                                                options=[
                                                    {
                                                        "label": "PMMA (Acrylic Slab)",
                                                        "value": "PMMA",
                                                    },
                                                    {
                                                        "label": "SIBAL Fabric (Cotton/Fiberglass)",
                                                        "value": "SIBAL_Fabric",
                                                    },
                                                    {
                                                        "label": "Nomex (Aromatic Polyamide)",
                                                        "value": "Nomex",
                                                    },
                                                    {
                                                        "label": "Silicone Rubber",
                                                        "value": "Silicone",
                                                    },
                                                    {
                                                        "label": "n-Heptane Droplets",
                                                        "value": "n-Heptane",
                                                    },
                                                    {
                                                        "label": "Methane Gas (CH4)",
                                                        "value": "Methane",
                                                    },
                                                    {
                                                        "label": "Ethylene Gas (C2H4)",
                                                        "value": "Ethylene",
                                                    },
                                                ],
                                                value="PMMA",
                                                clearable=False,
                                                className="mb-2",
                                            ),
                                            html.Label(
                                                "Flow Direction",
                                                className="hud-label mt-1",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.RadioItems(
                                                        id="toggle-flow-direction",
                                                        options=[
                                                            {
                                                                "label": "Concurrent (Downwind)",
                                                                "value": "Concurrent",
                                                            },
                                                            {
                                                                "label": "Opposed (Upwind)",
                                                                "value": "Opposed",
                                                            },
                                                        ],
                                                        value="Concurrent",
                                                        inline=True,
                                                        className="flow-toggle-enabled",
                                                    ),
                                                    dbc.Tooltip(
                                                        "Not applicable (Spherical symmetry and radial diffusion in microgravity)",
                                                        id="tooltip-flow-direction",
                                                        target="toggle-flow-direction",
                                                        placement="top",
                                                    ),
                                                ]
                                            ),
                                        ],
                                        xs=12,
                                        md=4,
                                        className="mb-3",
                                    ),
                                ]
                            )
                        ],
                        className="hud-card hud-controls-card hud-card-red",
                    ),
                    # 4 KPI Risk Metric Cards
                    dbc.Row(
                        [
                            _build_kpi_card(
                                "kpi-margin",
                                "LOC Flammability Margin",
                                "+4.5",
                                "% O2",
                                "hud-card-green",
                            ),
                            _build_kpi_card(
                                "kpi-spread",
                                "Flame Spread Rate",
                                "0.125",
                                "mm/s",
                                "hud-card-yellow",
                            ),
                            _build_kpi_card(
                                "kpi-hrr",
                                "Peak Heat Release Rate",
                                "0.85",
                                "kW",
                                "hud-card-red",
                            ),
                            _build_kpi_card(
                                "kpi-detection",
                                "Aerosol Detection Window",
                                "18.4",
                                "s",
                                "hud-card-green",
                            ),
                        ],
                        className="mb-2",
                    ),
                    # 2x2 Plotly Microgravity Flammability Grid
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="graph-g1-loc",
                                        figure=empty_fig,
                                        config={
                                            "responsive": True,
                                            "displayModeBar": False,
                                        },
                                        style={"height": "340px"},
                                    ),
                                    className="hud-card hud-card-red",
                                ),
                                xs=12,
                                lg=6,
                            ),
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="graph-g2-spread",
                                        figure=empty_fig,
                                        config={
                                            "responsive": True,
                                            "displayModeBar": False,
                                        },
                                        style={"height": "340px"},
                                    ),
                                    className="hud-card hud-card-yellow",
                                ),
                                xs=12,
                                lg=6,
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="graph-g3-saffire",
                                        figure=empty_fig,
                                        config={
                                            "responsive": True,
                                            "displayModeBar": False,
                                        },
                                        style={"height": "340px"},
                                    ),
                                    className="hud-card hud-card-red",
                                ),
                                xs=12,
                                lg=6,
                            ),
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="graph-g4-aerosol",
                                        figure=empty_fig,
                                        config={
                                            "responsive": True,
                                            "displayModeBar": False,
                                        },
                                        style={"height": "340px"},
                                    ),
                                    className="hud-card hud-card-green",
                                ),
                                xs=12,
                                lg=6,
                            ),
                        ]
                    ),
                ],
                fluid=True,
                className="px-4",
            )
        ],
    )


# ==============================================================================
# Action 5.6: Section 2 - Literature Explorer (#literature)
# ==============================================================================


def build_literature_section(
    investigations: list[dict[str, Any]] | None = None,
) -> html.Div:
    """Build Section 2: 3-Column Master-Detail Literature Explorer & Dedicated Charts."""
    if investigations is None:
        investigations = load_investigations()

    total_count = len(investigations)

    # Empty initial figure for dedicated investigation chart
    initial_chart = apply_hud_theme(
        go.Figure(),
        title="Dedicated Flight Experiment Telemetry",
        x_title="Parameter",
        y_title="Measurement",
    )

    return html.Div(
        id="literature",
        className="section-literature",
        children=[
            dbc.Container(
                [
                    # Section Header
                    html.Div(
                        [
                            html.Div(
                                "SECTION 2 // PSI FLIGHT ARCHIVE",
                                className="section-heading-eyebrow",
                            ),
                            html.H1(
                                "Physical Sciences Informatics Literature Explorer",
                                className="section-heading-title",
                            ),
                            html.P(
                                "Explore all 24 flight investigations, peer-reviewed publications, and dedicated "
                                "experimental datasets across ISS and Cygnus microgravity combustion campaigns.",
                                className="section-heading-subtitle",
                            ),
                        ]
                    ),
                    # Row 1: Search & Filters (Col 1, Width 4) + Scientific Detail Card (Col 2, Width 8)
                    dbc.Row(
                        [
                            # Top-Left: Filters (Yellow Border)
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H5(
                                            "Search & Filters",
                                            className="hud-label mb-3",
                                        ),
                                        html.Label(
                                            "Keyword Search", className="hud-label"
                                        ),
                                        dbc.Input(
                                            id="input-search",
                                            placeholder="Search title, acronym, accession...",
                                            type="text",
                                            className="mb-3",
                                        ),
                                        html.Label(
                                            "Combustion Category", className="hud-label"
                                        ),
                                        dcc.Dropdown(
                                            id="dropdown-category",
                                            options=[
                                                {
                                                    "label": "All Categories",
                                                    "value": "ALL",
                                                },
                                                {
                                                    "label": "Spacecraft Fire Safety",
                                                    "value": "Spacecraft Fire Safety",
                                                },
                                                {
                                                    "label": "Droplet Combustion",
                                                    "value": "Droplet Combustion",
                                                },
                                                {
                                                    "label": "Gaseous Combustion",
                                                    "value": "Gaseous Combustion",
                                                },
                                            ],
                                            value="ALL",
                                            clearable=False,
                                            className="mb-3",
                                        ),
                                        html.Label(
                                            "Flight Platform", className="hud-label"
                                        ),
                                        dcc.Dropdown(
                                            id="dropdown-platform",
                                            options=[
                                                {
                                                    "label": "All Platforms",
                                                    "value": "ALL",
                                                },
                                                {
                                                    "label": "International Space Station (ISS)",
                                                    "value": "International Space Station (ISS)",
                                                },
                                                {
                                                    "label": "Cygnus Spacecraft",
                                                    "value": "Cygnus Spacecraft",
                                                },
                                                {
                                                    "label": "Not Applicable",
                                                    "value": "Not Applicable",
                                                },
                                            ],
                                            value="ALL",
                                            clearable=False,
                                            className="mb-2",
                                        ),
                                    ],
                                    className="hud-card hud-card-yellow hud-filters-card h-100 mb-0",
                                ),
                                xs=12,
                                lg=4,
                                className="mb-3",
                            ),
                            # Top-Right: Scientific Detail Card (Green Border)
                            dbc.Col(
                                html.Div(
                                    id="container-investigation-detail",
                                    children=[
                                        html.Div(
                                            [
                                                html.Span(
                                                    "🔬",
                                                    style={"fontSize": "2rem"},
                                                    className="d-block mb-2",
                                                ),
                                                html.H6(
                                                    "Select an investigation from the list below",
                                                    className="text-white mb-2",
                                                ),
                                                html.P(
                                                    "Explore its flight research objectives, scientific hypothesis, experimental approach, "
                                                    "earth/space fire safety impacts, peer-reviewed DOIs, and dedicated experimental data.",
                                                    className="text-muted small mb-0",
                                                ),
                                            ],
                                            className="empty-state-prompt text-center py-4",
                                        )
                                    ],
                                    className="hud-card hud-card-green h-100 mb-0",
                                ),
                                xs=12,
                                lg=8,
                                className="mb-3",
                            ),
                        ],
                        className="mb-3 hud-literature-row-top",
                    ),
                    # Row 2: Flight Investigations List (Red Border) + Dedicated Chart (Yellow Border)
                    dbc.Row(
                        [
                            # Bottom-Left: Flight Investigations List (Dynamic Width: col-lg-6 <-> col-lg-3)
                            html.Div(
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H5(
                                                    "Flight Investigations",
                                                    className="hud-label mb-0",
                                                ),
                                                html.Span(
                                                    f"{total_count} Available",
                                                    id="badge-investigation-count",
                                                    className="badge-accession ms-2",
                                                ),
                                                dbc.Button(
                                                    [
                                                        html.Span("⇲", id="icon-toggle-list-size", className="me-1"),
                                                        html.Span("Focus Chart", id="text-toggle-list-size"),
                                                    ],
                                                    id="btn-toggle-list-size",
                                                    size="sm",
                                                    color="outline-warning",
                                                    className="btn-hud-toggle-sm ms-auto",
                                                    title="Toggle list width (Compress / Expand)",
                                                ),
                                            ],
                                            className="d-flex align-items-center mb-3",
                                        ),
                                        html.Div(
                                            id="container-investigation-list",
                                            className="investigation-list-scroll",
                                        ),
                                    ],
                                    className="hud-card hud-card-red h-100 mb-0",
                                ),
                                id="col-investigations-list",
                                className="col-12 col-lg-6 mb-3 layout-col-transition",
                            ),
                            # Bottom-Right: Dedicated Chart (Dynamic Width: col-lg-6 <-> col-lg-9)
                            html.Div(
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H5(
                                                    "Dedicated Flight Experiment Telemetry",
                                                    className="hud-label mb-0",
                                                ),
                                                html.Span(
                                                    "Interactive Data",
                                                    className="badge-platform ms-auto",
                                                ),
                                            ],
                                            className="d-flex align-items-center mb-3",
                                        ),
                                        dcc.Graph(
                                            id="graph-investigation-detail",
                                            figure=initial_chart,
                                            config={
                                                "responsive": True,
                                                "displayModeBar": False,
                                            },
                                            style={"height": "430px"},
                                        ),
                                    ],
                                    className="hud-card hud-card-yellow h-100 mb-0",
                                ),
                                id="col-investigations-chart",
                                className="col-12 col-lg-6 mb-3 layout-col-transition",
                            ),
                        ],
                        className="hud-literature-row-bottom",
                    ),
                ],
                fluid=True,
                className="px-4",
            )
        ],
    )


# ==============================================================================
# Action 5.7: Section 3 - AI Copilot (#agent)
# ==============================================================================


def build_agent_section() -> html.Div:
    """Build Section 3: Aerospace Conversational AI Copilot Console."""
    return html.Div(
        id="agent",
        className="section-agent",
        children=[
            dbc.Container(
                [
                    # Section Header
                    html.Div(
                        [
                            html.Div(
                                "SECTION 3 // LANGGRAPH INTELLIGENCE",
                                className="section-heading-eyebrow",
                            ),
                            html.H1(
                                "Autonomous Combustion Science AI Copilot",
                                className="section-heading-title",
                            ),
                            html.P(
                                "Conversational intelligence grounded in real-time telemetry, active scenario states, "
                                "and the 24 NASA PSI flight investigations. Powered by Google Gemini.",
                                className="section-heading-subtitle",
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [
                                        # Suggestion Pills
                                        html.Div(
                                            id="pills-container",
                                            children=[
                                                dbc.Button(
                                                    "Explain current scenario",
                                                    id="pill-1",
                                                    size="sm",
                                                    className="pill-suggestion-btn me-2 mb-2",
                                                ),
                                                dbc.Button(
                                                    "Synthesize active investigation",
                                                    id="pill-2",
                                                    size="sm",
                                                    className="pill-suggestion-btn me-2 mb-2",
                                                ),
                                                dbc.Button(
                                                    "Why does CO surge in microgravity?",
                                                    id="pill-3",
                                                    size="sm",
                                                    className="pill-suggestion-btn mb-2",
                                                ),
                                            ],
                                            className="d-flex flex-wrap mb-3",
                                        ),
                                        # Chat Feed Container
                                        html.Div(
                                            id="chat-feed-container",
                                            className="chat-feed-scroll",
                                            children=[
                                                html.Div(
                                                    [
                                                        html.Strong(
                                                            "NASA PSI Copilot // Online",
                                                            className="d-block mb-1 small",
                                                            style={"color": "#fbdc08"},
                                                        ),
                                                        (
                                                            "Welcome to the NASA Microgravity Flammability Copilot. "
                                                            "I am grounded in the 24 PSI flight combustion experiments. "
                                                            "Ask about current flammability margins, flame spread kinetics, "
                                                            "or select any investigation to inspect its findings."
                                                        ),
                                                    ],
                                                    className="chat-bubble chat-bubble-agent",
                                                )
                                            ],
                                        ),
                                        # Loading Spinner Indicator
                                        dcc.Loading(
                                            id="loading-agent",
                                            type="circle",
                                            color="#d91119",
                                            children=html.Div(
                                                id="agent-loading-output"
                                            ),
                                        ),
                                        # Input & Transmission Form
                                        dbc.InputGroup(
                                            [
                                                dbc.Input(
                                                    id="chat-input",
                                                    placeholder="Transmit query to NASA PSI AI Copilot...",
                                                    type="text",
                                                ),
                                                dbc.Button(
                                                    "Transmit",
                                                    id="chat-send-btn",
                                                    color="danger",
                                                    className="px-4",
                                                ),
                                            ],
                                            className="mt-3",
                                        ),
                                    ],
                                    className="hud-card chat-console-card hud-card-green",
                                ),
                                xs=12,
                                lg=10,
                                className="mx-auto",
                            )
                        ]
                    ),
                ],
                fluid=True,
                className="px-4",
            )
        ],
    )


# ==============================================================================
# Action 5.8: Section 4 - Project Info & Stack (#info)
# ==============================================================================


def build_info_section() -> html.Div:
    """Build Section 4: Data provenance, author credits, tech stack, and JSON export."""
    return html.Div(
        id="info",
        className="section-info",
        children=[
            dbc.Container(
                [
                    # Section Header
                    html.Div(
                        [
                            html.Div(
                                "SECTION 4 // PROVENANCE & CREDITS",
                                className="section-heading-eyebrow",
                            ),
                            html.H1(
                                "System Architecture & Engineering Provenance",
                                className="section-heading-title",
                            ),
                            html.P(
                                "Open-source mission analytics interface developed for NASA Physical Sciences Informatics.",
                                className="section-heading-subtitle",
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            # Provenance Card
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H5(
                                            "NASA PSI Provenance", className="hud-label"
                                        ),
                                        html.P(
                                            "Derived from the NASA Physical Sciences Informatics (PSI) repository. "
                                            "Encompasses 24 microgravity combustion science flight investigations, "
                                            "347 peer-reviewed publications, and curated flight benchmarks.",
                                            className="text-muted small",
                                        ),
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Download PSI Dataset (JSON)",
                                                    id="btn-download-json",
                                                    color="danger",
                                                    size="sm",
                                                    className="me-2 mt-2",
                                                ),
                                                dcc.Download(id="download-json"),
                                            ]
                                        ),
                                    ],
                                    className="hud-card h-100 hud-card-green",
                                ),
                                xs=12,
                                md=4,
                                className="mb-3",
                            ),
                            # Engineering Team Card
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H5(
                                            "Project Leadership", className="hud-label"
                                        ),
                                        html.Ul(
                                            [
                                                html.Li(
                                                    [
                                                        html.Strong("Cesia Burgos: "),
                                                        "Chief Executive Officer (CEO)",
                                                    ],
                                                    className="mb-2 text-white small",
                                                ),
                                                html.Li(
                                                    [
                                                        html.Strong("Ethan Bula: "),
                                                        "Chief Operating Officer (COO)",
                                                    ],
                                                    className="text-white small",
                                                ),
                                            ],
                                            className="list-unstyled mb-0",
                                        ),
                                    ],
                                    className="hud-card h-100 hud-card-yellow",
                                ),
                                xs=12,
                                md=4,
                                className="mb-3",
                            ),
                            # Technology Stack Badges
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H5(
                                            "Technology Stack", className="hud-label"
                                        ),
                                        html.Div(
                                            [
                                                html.Span(
                                                    "Python 3.12",
                                                    className="badge-platform me-2 mb-2",
                                                ),
                                                html.Span(
                                                    "Plotly Dash 4.x",
                                                    className="badge-platform me-2 mb-2",
                                                ),
                                                html.Span(
                                                    "LangGraph",
                                                    className="badge-platform me-2 mb-2",
                                                ),
                                                html.Span(
                                                    "Google Gemini",
                                                    className="badge-platform me-2 mb-2",
                                                ),
                                                html.Span(
                                                    "Bootstrap 5 Darkly",
                                                    className="badge-platform me-2 mb-2",
                                                ),
                                                html.Span(
                                                    "Docker",
                                                    className="badge-platform me-2 mb-2",
                                                ),
                                                html.Span(
                                                    "Hugging Face Spaces",
                                                    className="badge-platform mb-2",
                                                ),
                                            ],
                                            className="d-flex flex-wrap",
                                        ),
                                    ],
                                    className="hud-card h-100 hud-card-red",
                                ),
                                xs=12,
                                md=4,
                                className="mb-3",
                            ),
                        ]
                    ),
                ],
                fluid=True,
                className="px-4",
            )
        ],
    )


# ==============================================================================
# Action 5.9: Master Layout Assembler
# ==============================================================================


def create_layout() -> html.Div:
    """Assemble the complete NASA PSI Single-Page Application Layout."""
    investigations = load_investigations()

    return html.Div(
        [
            # Application State Stores
            dcc.Store(id="store-scenario", data={}),
            dcc.Store(id="store-selected-investigation", data={}),
            dcc.Store(id="store-literature-layout", data={"mode": "expanded"}),
            html.Div(id="dummy-resize-output", style={"display": "none"}),
            # Sticky Navbar
            build_navbar(),
            # Section 1: Environmental Dashboard
            build_dashboard_section(),
            # Section 2: Literature Explorer
            build_literature_section(investigations),
            # Section 3: AI Copilot
            build_agent_section(),
            # Section 4: Architecture & Provenance
            build_info_section(),
        ]
    )
