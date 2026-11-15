# Specification: NASA PSI Microgravity Flammability & Fire Safety Dashboard — V1.3

## 1. Project Overview & Objectives

### 1.1 Objective
Build an interactive, production-grade scientific dashboard, literature explorer, and conversational AI copilot that assists aerospace engineers, researchers, and mission safety officers in **predictive modeling of material flammability, flame spread, and fire precursors in microgravity spaceflight environments**.

All data, empirical benchmarks, and citations are strictly derived from the **24 Combustion Science investigations and 347 peer-reviewed articles** archived in the NASA Physical Sciences Informatics (PSI) repository (`data/psi_combustion_science.json`, enriched scientific flight dataset size: **~285 KB** / 292,483 bytes).

### 1.2 Language Standard
All project components—source code, comments, docstrings, UI labels, visualizations, error messages, and documentation—**MUST be entirely in English**.

### 1.3 Project Authors & Roles
* **Cesia Burgos** — Chief Executive Officer (CEO)
* **Ethan Bula** — Chief Operating Officer (COO)

---

## 2. Architecture & Vertical Flow Layout

The application is engineered as a **Single-Page Application (SPA)** with continuous smooth vertical scrolling across four thematic sections, each styled with its dedicated atmospheric background from `assets/wallpapers/`:

```
┌────────────────────────────────────────────────────────────────────────┐
│  STICKY TOP NAVBAR: [ Dashboard ] [ Literature ] [ AI Agent ] [ Info ] │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Section 1: Flammability Modeling Dashboard (`#dashboard` | `.section-dashboard` | Background: `wallpaper1.png`)
* **Environmental Controls Bar:**
  * Oxygen Concentration Slider: $14.0\% - 30.0\% \text{ O}_2$ (step $0.5\%$, default $21.0\%$).
  * Forced Flow Velocity Slider: $u_\infty: 0.0 - 15.0\text{ cm/s}$ (step $0.5\text{ cm/s}$, default $2.0\text{ cm/s}$).
  * Fuel / Material Selector (Standardized across PSI Flight Databases):
    * *Solids:* `PMMA (Acrylic Slab)`, `SIBAL Fabric (Cotton/Fiberglass)`, `Nomex (Aromatic Polyamide)`, `Silicone Rubber`.
    * *Droplets:* `n-Heptane Droplets`.
    * *Gaseous:* `Methane Gas (CH4)`, `Ethylene Gas (C2H4)`.
  * **Flow Direction Toggle (Concurrent vs. Opposed):**
    * *Behavior:* **Reactively Enabled** for solid fuels (`PMMA`, `SIBAL`, `Nomex`, `Silicone`).
    * **Reactively Disabled & Dimmed** for liquid droplets (`n-Heptane`) and gases (`Methane`, `Ethylene`) with tooltip: *"Not applicable (Spherical symmetry and radial diffusion in microgravity)"*.
* **4 Reactive KPI Cards:**
  1. *LOC Margin ($\Delta \% \text{O}_2$):* Absolute difference relative to the Limiting Oxygen Concentration extinction threshold ($\Delta \% \text{O}_2 = \text{O}_{2,\text{operating}} - \text{LOC}$).
  2. *Peak Spread Rate ($V_{f,\max}$):* Estimated flame advance speed ($\text{mm/s}$).
  3. *Peak Heat Release Rate ($HRR$):* Projected thermal hazard power ($\text{kW}$).
  4. *Smoke Detection Time:* Estimated time until pyrolysis aerosols reach optical detector threshold ($s$).
* **2x2 Plotly Chart Grid:**
  * *G1 (Top-Left):* Microgravity Flammability Phase Boundary (U-Curve: $u_\infty$ vs. $\% \text{O}_2$) showing the dynamic operating point.
  * *G2 (Top-Right):* Flame Spread Rate ($V_f$) by material, thickness, and flow direction (BASS / Saffire benchmarks).
  * *G3 (Bottom-Left):* Real-Scale Spacecraft Fire Dynamics Time-Series ($O_2$ depletion, $CO$ and $CO_2$ generation, and radiant heat from Saffire / ACME BRE).
  * *G4 (Bottom-Right):* Precursor Smoke Aerosol Particle Size Distribution ($d_p$ vs. particle concentration from SAME / SAME-R).

### 2.2 Section 2: Literature & Investigation Explorer (`#literature` | `.section-literature` | Background: `wallpaper2.png`)
* **3-Column Master-Detail Layout:**
  * *Column 1 (Filters, width 3 desktop / 12 mobile):* Instant keyword search (titles, authors, keywords) + Category filter (`Spacecraft Fire Safety`, `Gaseous Combustion`, `Droplet Combustion`) + Platform filter (`International Space Station (ISS)`, `Cygnus Spacecraft`, `Not Applicable`).
  * *Column 2 (Results List, width 4 desktop / 12 mobile):*
    * **Scrollable Container with Fixed Max-Height:** Styled with `max-height: 420px; overflow-y: auto;` to prevent pushing the detail view offscreen on mobile devices while allowing smooth navigation across all 24 items.
    * Interactive card list displaying accession badges (`PSI-98`), acronyms (`SAFFIRE-I`), category badges, and publication counters.
  * *Column 3 (Detail & Dynamic Graph, width 5 desktop / 12 mobile):*
    * *Initial State:* Clean empty state placeholder prompting user: *"Select an investigation from the list to inspect its flight research objectives, hypothesis, approach, space/earth impacts, and dedicated experimental data."*
    * *Top Card:* Investigation header (PI `principal_investigator`, NASA Center `monitoring_center`, hardware `experiment_hardware`), tabbed scientific summary (`Objectives`, `Hypothesis`, `Approach`, `Research Impacts / Earth Benefits`), and peer-reviewed articles table. Articles with existing DOIs provide clickable hyperlinks (`https://doi.org/{doi}`); articles without DOIs are displayed cleanly as formatted citations without broken links.
    * *Bottom Card:* **Contextual Experimental Chart (All 24 Investigations Dedicated):** Generated dynamically by `data/investigation_charts.py` using physical and mathematical outputs from `data/microgravity_models.py`:
      1. **PSI-69 (FLEX):** Droplet $d^2(t)$ regression & radiative extinction diameter curve.
      2. **PSI-68 (FLEX-2):** Binary alkane burning rate constant $K$ vs. initial droplet diameter.
      3. **PSI-23 (ACME s-Flame):** Spherical diffusion flame diameter & extinction stretch rate.
      4. **PSI-10 (ACME Flame Design):** Radial soot volume fraction $f_v(r)$ & temperature profile.
      5. **PSI-22 (ACME E-FIELD):** Flame liftoff height vs. applied electric field voltage.
      6. **PSI-21 (ACME CLD Flame):** Coflow laminar diffusion flame length vs. fuel flow velocity.
      7. **PSI-25 (BASS-II):** Solid fuel regression rate vs. forced flow speed.
      8. **PSI-20 (ACME BRE):** Porous burner heat feedback vs. fuel mass burning rate.
      9. **PSI-102 (SAME):** Smoke aerosol particle size distribution ($dN/d\log d_p$).
      10. **PSI-142 (Cool Flame Counterflow):** Cool flame extinction limit vs. strain rate & oxygen index.
      11. **PSI-26 (BASS):** Solid fuel limiting oxygen concentration (LOC) boundary curve.
      12. **PSI-117 (Thermo-Convective CFD):** Cool flame oscillation frequency vs. Damköhler number.
      13. **PSI-107 (SPICE):** Smoke point fuel flow rate vs. microgravity coflow velocity.
      14. **PSI-39 (CFI):** Droplet cool flame transition temperature vs. ambient pressure.
      15. **PSI-99 (SAFFIRE-II):** Material flammability limit vs. cabin pressure ($0.7 - 1.0\text{ atm}$).
      16. **PSI-98 (SAFFIRE-I):** Large-scale fabric flame spread rate & heat release rate ($HRR$).
      17. **PSI-101 (SAME-R):** Smoke agglomeration rate & particle count decay over time.
      18. **PSI-62 (FGM Modeling vs. BASS):** 2D flamelet temperature profile vs. BASS experimental data.
      19. **PSI-100 (SAFFIRE-III):** Thick PMMA slab flame front propagation speed vs. airflow.
      20. **PSI-47 (DAFT / DAFT-2):** Dust vs. smoke aerosol light scattering ratio (sensor discriminator).
      21. **PSI-159 (ACME CFI-G):** Gaseous cool flame burning rate vs. reactant dilution ($CO_2/He$).
      22. **PSI-60 (SPICE Re-Analysis):** Soot yield fraction & optical pyrometry color-ratio vs. time.
      23. **PSI-106 (SLICE):** Gaseous diffusion flame liftoff velocity vs. coflow air speed.
      24. **PSI-115 (SAME Modeling):** CFD simulation vs. flight particle coagulation kinetics.

### 2.3 Section 3: LangGraph AI Copilot (`#agent` | `.section-agent` | Background: `wallpaper3.png`)
* **LangGraph StateGraph Engine:** Grounded conversational agent with live awareness of user state (`dcc.Store` holding current dashboard parameters and selected investigation).
* **Model Hierarchy & Fallback:**
  * **Primary Model:** Google Gemini `gemini-3.8-flash` via `langchain-google-genai`.
  * **Automatic Fallback:** `gemini-3.6-flash` triggered upon rate limits, 5xx responses, or connection timeouts.
  * **Strict API Key Requirement:** Valid `GEMINI_API_KEY` is strictly required. If the key is missing or both models fail/timeout after 10s, the agent delivers an explicit authentication/network error message in the chat console rather than an offline simulated response.
* **Execution & Latency Strategy (Option A):**
  * **Synchronous Callback with NASA HUD Loading Indicator:** Displays a pulsating radar loader (`dcc.Loading(type="circle")`).
  * **Strict 10-Second Timeout:** If Gemini does not respond within 10 seconds, the fallback node returns immediately to preserve UI responsiveness.
* **UI Interface:** Dark aerospace console with Markdown rendering, LaTeX math support, prompt suggestion pills (*"Explain current dashboard scenario"*, *"Synthesize active investigation"*, *"Why does CO surge prior to flaming combustion in microgravity?"*), and responsive input field.

### 2.4 Section 4: Project Info & Stack (`#info` | `.section-info` | Background: `wallpaper4.png`)
* **Modular Cards:**
  * *Dataset Provenance:* NASA Physical Sciences Informatics (PSI), 24 investigations, 12.21 TB CIR payload data archive (**~285 KB** enriched dataset including objectives, hypotheses, approach, and publications).
  * *Engineering Team:* Cesia Burgos (Chief Executive Officer, CEO) & Ethan Bula (Chief Operating Officer, COO).
  * *Tech Stack Badges:* Python, Dash, Plotly, LangGraph, Google Gemini, Docker, Hugging Face Spaces.
  * *Data Export:* One-click download button for `psi_combustion_science.json`.

---

## 3. Tech Stack & Environment

* **Runtime:** Python 3.12+ (CPython 3.12 / 3.13)
* **Core Analytics:** `pandas>=2.2.0`, `numpy>=1.26.0`
* **Web Framework:** `dash>=2.16.0`, `dash-bootstrap-components>=1.6.0`, `plotly>=5.20.0`
* **Agentic AI:** `langgraph>=0.2.0`, `langchain-core>=0.3.0`, `langchain-google-genai>=2.0.0`
* **Production Server:** `gunicorn>=22.0.0` running strictly on port **`7860`**
* **Container & Hosting Platform:** Hugging Face Spaces (SDK: `docker`, 16 GB RAM, 2 vCPUs, port `7860`)
* **Frontend Design Skills:** `scrollytelling` (smooth scroll snapping & section transitions), `design-system` (3-tier CSS tokens & glassmorphic HUD), `ui-ux-pro-max` (responsive layout & touch UX)
* **Testing & Quality:** `pytest>=8.0.0`, `ruff>=0.4.0`

---

## 4. Commands

* **Local Environment Setup & Activation:**
  ```bash
  uv venv .venv
  .\.venv\Scripts\activate
  uv pip install -r requirements.txt
  ```
* **Local Development Server (Strictly Port 7860):**
  ```bash
  .\.venv\Scripts\python app.py
  # Serves locally at http://127.0.0.1:7860
  ```
* **Execute Test Suite:**
  ```bash
  .\.venv\Scripts\pytest tests/ -v --tb=short
  ```
* **Code Linting & Formatting:**
  ```bash
  .\.venv\Scripts\ruff check .
  .\.venv\Scripts\ruff format --check .
  ```
* **Hugging Face Spaces Production Launch (Container):**
  ```bash
  gunicorn app:server --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:7860
  ```

---

## 5. Production Dockerfile Specification (Hugging Face Spaces UID 1000 — Option A)

```dockerfile
FROM python:3.12-slim

# Create unprivileged user with UID 1000 per Hugging Face Spaces specification
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

WORKDIR $HOME/app

# Install dependencies into user space
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application source code
COPY --chown=user . $HOME/app

EXPOSE 7860

CMD ["gunicorn", "app:server", "--workers", "2", "--threads", "4", "--timeout", "120", "--bind", "0.0.0.0:7860"]
```

---

## 6. Project Directory Structure

```text
d:\NASA\
├── SPEC.md                           # Single source of truth (this specification)
├── README.md                         # Hugging Face Spaces metadata & deployment documentation
├── Dockerfile                        # Production Docker container definition (UID 1000)
├── requirements.txt                  # Pinned Python package dependencies (78 packages)
├── skills-lock.json                  # Lockfile for agent skills from skills.sh
├── .env.example                      # Template for environment variables (GEMINI_API_KEY)
├── .env                              # Local private environment variables (git-ignored)
├── .gitignore                        # Git ignore patterns (.env, .venv, __pycache__, etc.)
├── app.py                            # Main Dash application entrypoint (serves port 7860)
├── layout.py                         # Modular UI component layout tree for Sections 1-4 & sticky navbar
├── callbacks.py                      # Dash reactive callbacks registry (KPIs, graphs, filters, chat)
│
├── .agents/                          # Installed Agent Skills from skills.sh
│   └── skills/                       # spec-driven-dev, scrollytelling, design-system, etc.
│
├── .venv/                            # Virtual environment created via uv (git-ignored)
│   ├── Scripts/                      # Python executable, pytest, ruff, activate
│   └── Lib/site-packages/            # Installed libraries (Dash, Plotly, LangGraph, etc.)
│
├── data/
│   ├── psi_combustion_science.json   # 24 investigations + 347 papers enriched metadata (~285 KB)
│   ├── microgravity_models.py        # Physical equations (LOC U-curve, Vf, d^2 law, SAME aerosols)
│   ├── benchmark_data.py             # Empirical data tables from BASS, Saffire, FLEX, SAME
│   └── investigation_charts.py       # Plotly figure generation routines for all 24 investigations
│
├── agent/
│   ├── __init__.py                   # Package marker
│   ├── state.py                      # TypedDict state schema for LangGraph
│   ├── graph.py                      # StateGraph nodes, edges, Gemini 3.8/3.6 fallback
│   └── prompts.py                    # Domain grounding system prompts & citation enforcement
│
├── assets/
│   ├── custom.css                    # Glassmorphic HUD styles, sticky navbar, mobile breakpoints
│   ├── wallpapers/                   # Atmospheric section backgrounds
│   │   ├── wallpaper1.png            # Section 1: Dashboard
│   │   ├── wallpaper2.png            # Section 2: Literature
│   │   ├── wallpaper3.png            # Section 3: AI Copilot
│   │   └── wallpaper4.png            # Section 4: Project Info & Credits
│   └── favicon.ico
│
└── tests/
    ├── __init__.py                   # Test package marker
    ├── test_physics_models.py        # Unit tests for LOC, flame spread rates, and droplet extinction
    ├── test_data_integrity.py        # Validates JSON schema, DOIs, accessions, and publications
    ├── test_agent_graph.py           # Validates LangGraph state transitions, router, and fallbacks
    └── test_layout_rendering.py      # Dash layout smoke test and callback registry verification
```

---

## 7. Styling, Theming & Wallpaper Implementation

### 7.1 Section Wallpapers in `assets/custom.css`
Dash automatically serves all assets in `assets/` under `/assets/`. Each section applies its corresponding wallpaper with semi-transparent dark HUD overlays to guarantee WCAG AAA text readability:

```css
/* Glassmorphic NASA HUD Theme & Design Tokens */
:root {
  --bg-dark: #0b0f19;
  --card-bg: rgba(19, 24, 38, 0.85);
  --bg-card: var(--card-bg);
  --border-cyan: rgba(56, 189, 248, 0.25);
  --accent-cyan: #38bdf8;
  --accent-orange: #f97316;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
}

/* Vertical Sections with Wallpaper Backdrops */
.section-dashboard {
  background: linear-gradient(180deg, rgba(11, 15, 25, 0.86), rgba(11, 15, 25, 0.94)),
              url('/assets/wallpapers/wallpaper1.png') center/cover no-repeat fixed;
  min-height: 100vh;
}

.section-literature {
  background: linear-gradient(180deg, rgba(11, 15, 25, 0.88), rgba(11, 15, 25, 0.95)),
              url('/assets/wallpapers/wallpaper2.png') center/cover no-repeat fixed;
  min-height: 100vh;
}

.section-agent {
  background: linear-gradient(180deg, rgba(11, 15, 25, 0.84), rgba(11, 15, 25, 0.92)),
              url('/assets/wallpapers/wallpaper3.png') center/cover no-repeat fixed;
  min-height: 90vh;
}

.section-info {
  background: linear-gradient(180deg, rgba(11, 15, 25, 0.90), rgba(11, 15, 25, 0.98)),
              url('/assets/wallpapers/wallpaper4.png') center/cover no-repeat fixed;
  min-height: 60vh;
}

/* Glassmorphic Cards */
.hud-card {
  background: var(--card-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--border-cyan);
  border-radius: 12px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

/* Scrollable Investigation List for Literature Section */
.investigation-list-scroll {
  max-height: 420px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--accent-cyan) var(--bg-dark);
}
```

---

## 8. Mobile-First Responsive Design Standards

* **Grid Breakpoints:**
  * Desktop ($\ge 992\text{px}$): 2x2 grid for Section 1 (`col-lg-6`); 3-column layout for Section 2 (`col-lg-3`, `col-lg-4`, `col-lg-5`).
  * Mobile ($< 768\text{px}$): Columns stack cleanly to `col-12` with comfortable padding.
* **Literature List Mobile Compactness:** The `investigation-list-scroll` container maintains its max-height of 420px with smooth internal scrolling, preventing mobile users from having to scroll past 24 uncollapsed cards to view the detail card.
* **Touch-Friendly Constraints:** All sliders, dropdowns, and action buttons have touch targets $\ge 44\text{px}$.
* **Zero Horizontal Overflow:** Strict `overflow-x: hidden` on viewport.
* **Plotly Responsiveness:** Every chart initializes with `config={"responsive": True, "displayModeBar": False}` to dynamically adapt to narrow mobile screens.

---

## 9. Autonomous Testing & Verification Protocols

### 9.1 Backend Unit Tests (`pytest`)
* **`test_physics_models.py`:**
  * Validate that PMMA LOC at $u_\infty = 2\text{ cm/s}$ matches BASS experimental data ($\approx 16.5\% \text{ O}_2$).
  * Validate that the $d^2(t)$ droplet law monotonically regresses to extinction.
  * Validate that smoke aerosol geometric mean diameter $d_p$ matches SAME flight records.
* **`test_data_integrity.py`:**
  * Ensure all 24 investigations load with non-empty titles, accessions, single assigned `category`, `platform`, `objectives`, `hypothesis`, and `approach`.
  * Ensure exactly 347 publications exist, all with non-empty titles, and for those with non-empty DOIs, verify standard syntax (`10.xxxx/...`).
* **`test_agent_graph.py`:**
  * Validate LangGraph compilation and conditional routing logic (Gemini 3.8 Flash to 3.6 Flash fallback).
  * Verify explicit error propagation when `GEMINI_API_KEY` is unset or invalid.
* **`test_layout_rendering.py`:**
  * Smoke test verifying full Dash layout tree rendering, component IDs integrity, and callback registry without exceptions.

### 9.2 Autonomous Frontend Verification (`browser-testing-with-devtools`)
* Automated execution via the autonomous `browser` subagent driving Chrome DevTools:
  1. **Desktop Verification (1920x1080):** Verify 2x2 grid layout, live slider reactivity, smooth scrolling to `#section` anchors, and list selection.
  2. **Mobile Responsive Audit (390x844 viewport):** Verify zero horizontal scrollbar, 100% chart width fitting, touch-target sizing, and clean vertical stacking.

---

## 10. Boundaries & Operating Rules

* **Always:**
  * Restrict all scientific figures and literature claims strictly to the 24 NASA PSI investigations.
  * Ensure all code, docstrings, variable names, and UI elements are written in English.
  * Keep memory footprint optimized for high concurrency on Hugging Face Spaces (16 GB limit).
* **Ask First:**
  * Modifying the core vertical layout or reordering sections.
  * Adding heavyweight dependencies beyond the approved stack.
* **Never:**
  * Commit `.env` or plaintext API keys to GitHub or Hugging Face.
  * Attempt to download raw multi-gigabyte video or TIFF payload files (the 12 TB).
  * Allow the AI agent to invent or hallucinate non-existent DOIs or scientific citations.

---

## 11. Success Criteria (Definition of Done)

1. **Unit Tests Passing:** 100% of tests in `tests/` pass with zero failures.
2. **Data Completeness:** All 24 investigations and 347 articles accessible in the literature explorer.
3. **24 Dedicated Experimental Charts:** Each investigation selected renders its corresponding distinct scientific graph.
4. **Wallpaper Integration:** All 4 sections render their designated background wallpaper with high-contrast text and charts.
5. **Interactive Dashboard:** Slider modifications update all 4 KPIs and 4 charts in $< 100\text{ ms}$.
6. **AI Copilot Functional:** LangGraph agent responds contextually using Gemini 3.8 Flash (with 3.6 Flash fallback and 10s timeout).
7. **Mobile Audit Approved:** Autonomous browser audit confirms flawless mobile responsiveness at 390px width.
8. **Production Ready:** Docker container starts cleanly on `0.0.0.0:7860` as UID 1000 and serves HTTP 200 OK.
