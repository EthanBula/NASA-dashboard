"""NASA PSI Microgravity Flammability & Fire Safety Dashboard - Main Application Entrypoint.

Authors: Cesia Burgos (Chief Executive Officer, CEO) & Ethan Bula (Chief Operating Officer, COO).
"""

from __future__ import annotations

import dash
import dash_bootstrap_components as dbc

from callbacks import register_callbacks
from layout import create_layout

# Initialize Dash application with Darkly theme and responsive viewport
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

# Underlying Flask WSGI server instance for Hugging Face Spaces & Gunicorn
server = app.server

# Application metadata & layout
app.title = "NASA PSI Microgravity Flammability & Fire Safety Dashboard"
app.layout = create_layout()

# Wire callback triggers
register_callbacks(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=False)
