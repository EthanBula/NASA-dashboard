---
title: NASA PSI Microgravity Flammability & Fire Safety Dashboard
emoji: 🚀
colorFrom: blue
colorTo: cyan
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# NASA PSI Microgravity Flammability & Fire Safety Dashboard

An aerospace-grade, scrollytelling web application and interactive telemetry HUD designed for space exploration fire safety analysis, grounded in 24 NASA flight experiments from the **Physical Sciences Informatics (PSI)** repository.

---

## 👥 Project Leadership & Authors

* **Cesia Burgos** — Chief Executive Officer (CEO)
* **Ethan Bula** — Chief Operating Officer (COO)

---

## 🛰️ Overview & Scientific Scope

Spacecraft fire safety presents unique challenges due to the absence of buoyant natural convection in microgravity ($10^{-4}$ to $10^{-6}\text{ g}$). Under microgravity conditions, transport is governed strictly by forced ventilation ($u_\infty$) and molecular diffusion.

This dashboard integrates empirical datasets and validated physical models from seminal NASA missions, including:
* **BASS (Burning and Suppression of Solids):** Concurrent and opposed flame spread rates across PMMA slabs and SIBAL fabrics.
* **Saffire I–VI (Spacecraft Fire Safety Demonstration):** Large-scale fabric combustion, heat release rates (HRR), and carbon monoxide (CO) emission surges during cargo resupply vehicle deorbit.
* **FLEX / FLEX-2 (Flame Extinction Experiment):** Spherically symmetric droplet combustion, $d^2$-law regression rates ($K$), and radiative extinction thresholds ($d_{ext}$).
* **SAME (Smoke Aerosol Measurement Experiment):** Particle size distribution shifts ($d_{pg}$, $\sigma_g$) and early smoke detector alarm windows.
* **ACME (Advanced Combustion via Microgravity Experiments):** Soot inception, cool flame transitions, and electrical field flame control.

---

## 🏛️ Application Architecture

The application is structured into four interconnected vertical sections with an aerospace glassmorphic dark HUD theme (WCAG 2.1 AAA contrast):

1. **Section 1: Environmental Dashboard (`#dashboard`)**
   * Real-time sliders for ambient oxygen ($O_2: 15\%\text{--}30\%$) and forced airflow ($u_\infty: 0\text{--}15\text{ cm/s}$).
   * Reactive fuel selection across solid slabs, fabrics, droplets, and gaseous diffusion flames.
   * Four live KPI readouts: Limiting Oxygen Concentration (LOC) Margin, Flame Spread Rate ($V_f$), Peak Heat Release Rate (HRR), and Aerosol Detection Window ($t_{det}$).
   * 4-panel interactive HUD telemetry charts:
     * **G1:** Flammability Boundary & LOC ($u$-shaped quenching curve).
     * **G2:** Flame Spread Rate vs Forced Flow (blowoff and radiation extinction regimes).
     * **G3:** Spacecraft Cabin Fire Dynamics (Thornton-Huggett scaled HRR and low-temperature incomplete combustion CO kinetics).
     * **G4:** Smoke Aerosol Size Distribution (Smoluchowski Brownian coagulation and convective dilution).

2. **Section 2: Literature & Flight Archive (`#literature`)**
   * Three-column interactive master-detail explorer for the 24 NASA PSI flight investigations.
   * Full-text keyword search and multi-select filtering by combustion category and flight platform (ISS CIR, Cygnus Saffire, Shuttle).
   * Detailed scientific dossier: Principal Investigators, NASA Research Centers, Flight Hardware, Research Objectives, Hypotheses, Approach, and Terrestrial/Space Impacts.
   * 24 dedicated Plotly scientific figures rendering domain-specific telemetry for each experiment.

3. **Section 3: Autonomous Combustion Science AI Copilot (`#copilot`)**
   * LangGraph StateGraph engine integrated with Google Gemini.
   * Grounded strictly in the 24 NASA PSI investigations and real-time dashboard telemetry.
   * 4-tier model fallback: `gemini-3.8-flash` $\rightarrow$ `gemini-3.6-flash` $\rightarrow$ `gemini-3.5-flash-lite` $\rightarrow$ `gemini-3.1-flash-lite`.
   * Complete mathematical rendering via clean Unicode formatting.

4. **Section 4: Architecture & Engineering Provenance (`#info`)**
   * Provenance summary: 24 flight investigations, 347 peer-reviewed publications, and flight benchmarks.
   * Project leadership attribution: Cesia Burgos (CEO) & Ethan Bula (COO).
   * One-click dataset export (`psi_combustion_science.json`).

---

## 🛠️ Technology Stack

* **Framework:** [Plotly Dash 4.x](https://dash.plotly.com/) & [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
* **Visualization:** [Plotly Graph Objects](https://plotly.com/python/)
* **Agentic AI:** [LangGraph](https://langchain-ai.github.io/langgraph/) & [Google Gemini](https://ai.google.dev/)
* **Styling:** Custom Aerospace Glassmorphic HUD CSS (`assets/custom.css`)
* **Containerization:** Docker (`python:3.12-slim`), non-root user UID 1000
* **Testing:** Pytest & Playwright Browser Automation

---

## 🚀 Local Execution

### Prerequisites
* Python 3.12+
* (Optional) Google Gemini API key (`GEMINI_API_KEY`) for AI Copilot queries

### Installation & Launch

```bash
# 1. Clone repository
git clone https://github.com/your-username/nasa-psi-dashboard.git
cd nasa-psi-dashboard

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variable (optional)
cp .env.example .env
# Edit .env and enter your GEMINI_API_KEY

# 5. Run the application
python app.py
```

The application will be live at `http://127.0.0.1:7860`.

---

## 🧪 Testing

Run the automated verification suite:

```bash
pytest tests/ -v
```

