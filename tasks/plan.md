# Technical Implementation Plan: NASA PSI Microgravity Flammability & Fire Safety Dashboard

**Specification Reference:** [`SPEC.md` V1.3](file:///d:/NASA/SPEC.md)  
**Authors:** Cesia Burgos (Chief Executive Officer, CEO) & Ethan Bula (Chief Operating Officer, COO)  
**Target Platform:** Hugging Face Spaces (Docker, 16 GB RAM, 2 vCPUs, Port 7860)  
**Execution Strategy:** Strictly Sequential (Slice 1 through Slice 8)  
**Language Standard:** 100% English across all modules, tests, UI labels, and documentation.

---

## 1. Component Dependency Graph & Architecture

```text
                         ┌────────────────────────────────────────────────────────┐
                         │ .agents/skills/ (Design, Scrolly, LangGraph, Testing)  │
                         └───────────┬───────────────────────────────┬────────────┘
                                     │                               │
                                     ▼                               ▼
                         ┌─────────────────────────────┐   ┌──────────────────────┐
                         │data/psi_combustion_science  │   │  assets/wallpapers/  │
                         │(Enriched: ~285 KB JSON)     │   │  (wallpaper1..4.png) │
                         └───────────┬─────────────────┘   └──────────┬───────────┘
                                     │                                │
            ┌────────────────────────┴────────────────┐               │
            ▼                                         ▼               ▼
┌─────────────────────────┐               ┌─────────────────────────────────────┐
│ data/benchmark_data.py  │               │ assets/custom.css                   │
│ (BASS, Saffire, FLEX)   │               │ (NASA HUD Tokens, Glassmorphism,    │
└───────────┬─────────────┘               │  Wallpapers, Scrollytelling, Mobile)│
            │                             └───────────────────┬─────────────────┘
            ▼                                                 │
┌─────────────────────────┐                                   │
│data/microgravity_models │                                   │
│(LOC, Vf, d^2, SAME)     │                                   │
└───────────┬─────────────┘                                   │
            ├─────────────────────────────┐                   │
            ▼                             ▼                   │
┌─────────────────────────┐  ┌─────────────────────────────┐  │
│ tests/test_physics_*.py │  │data/investigation_charts.py │  │
│ tests/test_data_*.py    │  │(24 Dedicated Plotly Figures)│  │
└─────────────────────────┘  └────────────┬────────────────┘  │
                                          │                   │
            ┌─────────────────────────────┘                   │
            │                                                 │
            ▼                                                 ▼
┌─────────────────────────┐               ┌─────────────────────────────────────┐
│ agent/ (LangGraph:      │               │ app.py                              │
│ state, prompts, graph   │──────────────►│ (Dash Layout, 4 Sections, Callbacks,│
│ Gemini 3.8/3.6 Fallback)│               │  Sticky Navbar, dcc.Store)          │
└───────────┬─────────────┘               └───────────────────┬─────────────────┘
            │                                                 │
            ▼                                                 ▼
┌─────────────────────────┐               ┌─────────────────────────────────────┐
│ tests/test_agent_*.py   │               │ tests/test_layout_rendering.py      │
└───────────┬─────────────┘               │ Browser DevTools Audits (Slice 7)   │
            │                             └───────────────────┬─────────────────┘
            └──────────────────────────────┬──────────────────┘
                                           ▼
                            ┌─────────────────────────────┐
                            │ Dockerfile & README.md      │
                            │ (Hugging Face Spaces Deploy)│
                            └─────────────────────────────┘
```

---

## 2. Implementation Order & Vertical Slices

The build follows an incremental, test-driven path where **all slices execute strictly sequentially**. Each slice must be fully built and pass its associated checkpoint before work on the next slice begins.

### Slice 1: Empirical Data Matrices & Microgravity Physical Models
* **Objective:** Establish physical formulas and empirical lookup tables from the 24 investigations.
* **Deliverables:**
  * `data/benchmark_data.py`: Curated data points for BASS/BASS-II solid burning rates, Saffire gas concentrations ($O_2, CO, CO_2$), FLEX droplet extinction boundaries, and SAME aerosol size spectra.
  * `data/microgravity_models.py`: Pure computational engines for:
    * Microgravity U-curve LOC limit: $f(u_\infty, \text{fuel})$.
    * Solid flame spread rate ($V_f$) under concurrent vs. opposed flows.
    * Godsave-Spalding droplet $d^2(t)$ regression with radiative quenching.
    * Pyrolysis smoke aerosol size distributions ($dN/d\log d_p$).
* **Dependencies:** `data/psi_combustion_science.json`.
* **Execution:** Strictly sequential (Step 1 of 8).

### Slice 2: Backend Unit Tests & Data Integrity Verification (TDD)
* **Objective:** Prove model accuracy and dataset completeness with `pytest` before touching the UI.
* **Deliverables:**
  * `tests/test_physics_models.py`: Validates that PMMA LOC matches BASS flight records ($\sim 16.5\% \text{ O}_2$ at $2\text{ cm/s}$), $d^2(t)$ decays monotonically, and aerosol size distributions match SAME flight data.
  * `tests/test_data_integrity.py`: Validates that all 24 investigations load as a list with non-empty titles, accessions, single assigned `category`, `platform`, `objectives`, and `hypothesis`, and that exactly 347 publications exist with valid titles and valid DOIs where present.
* **Dependencies:** Slice 1.
* **Execution:** Strictly sequential (Step 2 of 8). Gate requirement: 100% green pass.

### Slice 3: Design System, Scrollytelling & CSS Tokens
* **Objective:** Establish the visual styling, glassmorphic HUD theme, and section backgrounds using `.agents/skills/design-system` and `.agents/skills/scrollytelling`.
* **Deliverables:**
  * `assets/custom.css`:
    * CSS variables for dark HUD palette (`--bg-dark`, `--accent-cyan: #38bdf8`, `--accent-orange: #f97316`).
    * Section background classes (`.section-dashboard`, `.section-literature`, `.section-agent`, `.section-info`) using `assets/wallpapers/wallpaper1.png` through `wallpaper4.png` with high-contrast linear gradient overlays.
    * Glassmorphic HUD cards (`.hud-card`) with `backdrop-filter: blur(12px)`.
    * Sticky top navigation bar styling with smooth scroll snapping (`scroll-behavior: smooth`).
    * Scrollable literature container (`.investigation-list-scroll`) with fixed `max-height: 420px; overflow-y: auto;`.
    * Mobile media queries (`@media (max-width: 768px)`) enforcing touch targets $\ge 44\text{px}$ and zero horizontal overflow (`overflow-x: hidden`).
* **Dependencies:** `assets/wallpapers/`, Slice 2.
* **Execution:** Strictly sequential (Step 3 of 8).

### Slice 4: LangGraph AI Copilot Engine
* **Objective:** Build the conversational AI agent grounded in live dashboard state and literature metadata using `.agents/skills/langgraph-fundamentals`.
* **Deliverables:**
  * `agent/state.py`: TypedDict `CombustionAgentState` holding conversation messages, `current_scenario` parameters, and `selected_investigation` data.
  * `agent/prompts.py`: NASA combustion science domain prompt enforcing rigorous physics grounding, citation of actual PSI papers/DOIs, and zero hallucination.
  * `agent/graph.py`: StateGraph orchestration:
    * Primary model `gemini-3.8-flash` via `langchain-google-genai`.
    * Automatic fallback to `gemini-3.6-flash` upon rate limit or service errors.
    * Strict 10-second timeout.
    * Explicit error message propagation if `GEMINI_API_KEY` is missing or unauthenticated (no fake offline simulation node).
  * `tests/test_agent_graph.py`: Validates StateGraph compilation, scenario-aware answering, and clean error reporting on authentication/network failure.
* **Dependencies:** Slice 3, `.env` with `GEMINI_API_KEY`.
* **Execution:** Strictly sequential (Step 4 of 8).

### Slice 5: Dash UI Layout & Scrollytelling Assembly (`app.py` & `data/investigation_charts.py`)
* **Objective:** Assemble the complete visual single-page application structure with decoupled figure builders and smoke tests.
* **Deliverables:**
  * `data/investigation_charts.py`: Specialized routines to build Plotly `go.Figure` instances for each of the 24 investigations, styled in dark NASA HUD theme.
  * `app.py`:
    * Dash instance configured with `dbc.themes.DARKLY`, `suppress_callback_exceptions=True`, and asset autoloading.
    * Sticky navigation bar (`#dashboard`, `#literature`, `#agent`, `#info`).
    * **Section 1 Layout:** Control bar (sliders, reactive flow direction toggle), 4 KPI cards, and 2x2 Plotly initial graph placeholders.
    * **Section 2 Layout:** 3-Column Master-Detail explorer (Filter inputs $\rightarrow$ Scrollable investigation list $\rightarrow$ Scientific summary card + dynamic graph container).
    * **Section 3 Layout:** Aerospace console chat container with message feed, suggestion pills, input field, and `dcc.Loading` HUD spinner.
    * **Section 4 Layout:** Project provenance, author credits (Cesia Burgos, CEO & Ethan Bula, COO), tech stack badges, and data export button.
  * `tests/test_layout_rendering.py`: Verifies that the Dash layout tree instantiates completely, all component IDs match, and default figures render without exceptions.
* **Dependencies:** Slice 1, Slice 3, Slice 4.
* **Execution:** Strictly sequential (Step 5 of 8).

### Slice 6: Reactive Callbacks Engine
* **Objective:** Wire full inter-section reactivity, real-time dashboard calculations, and literature/chat interactions.
* **Deliverables:**
  * Environmental control callbacks: Sliders and fuel selectors update all 4 KPIs and 4 charts in $<100\text{ ms}$.
  * Flow direction toggle logic: Automatically enabled for solids; disabled with an informative tooltip for droplets/gases.
  * Literature master-detail callback: Real-time search/filter updates the scrollable list; clicking an item updates the detail summary, DOI table, and calls `data/investigation_charts.py` to render the exact corresponding experimental chart (1 of 24).
  * Agent callback: Synchronous execution with `dcc.Loading` and 10s strict timeout, feeding live `current_scenario` and `selected_investigation` into the LangGraph state.
* **Dependencies:** Slice 5.
* **Execution:** Strictly sequential (Step 6 of 8).

### Slice 7: Autonomous Testing & Mobile Viewport Audit
* **Objective:** Verify functionality and visual responsiveness before containerization using `.agents/skills/browser-testing-with-devtools`.
* **Deliverables:**
  * Full test suite execution: `pytest tests/ -v` (100% green pass).
  * Launch local server on `http://127.0.0.1:7860`.
  * Deploy autonomous `browser` subagent driving Chrome DevTools:
    * Desktop audit (1920x1080): Test slider reactivity, smooth scrolling to `#section` anchors, and list selection.
    * Mobile audit (390x844 viewport): Verify zero horizontal scroll (`overflow-x: hidden`), touch targets $\ge 44\text{px}$, and `max-height: 420px` internal scrolling in the literature list.
* **Dependencies:** Slice 6.
* **Execution:** Strictly sequential (Step 7 of 8). Verification gate.

### Slice 8: Containerization & Hugging Face Spaces Deployment
* **Objective:** Package the application for production hosting.
* **Deliverables:**
  * `Dockerfile`: Canonical Hugging Face Spaces configuration with `useradd -m -u 1000 user`, `COPY --chown=user`, exposing port `7860`, running Gunicorn (`--workers 2 --threads 4`).
  * `README.md`: Space metadata YAML frontmatter (`title`, `emoji: 🚀`, `sdk: docker`, `app_port: 7860`).
* **Dependencies:** Slice 7.
* **Execution:** Strictly sequential (Step 8 of 8). Final delivery.

---

## 3. Risks & Mitigation Matrix

| Risk / Failure Mode | Impact | Mitigation Strategy |
| :--- | :---: | :--- |
| **Plotly Graph Memory Overhead** | Medium | Reuse graph template dictionaries (`fig.update_layout`); avoid storing large figure states in `dcc.Store`. |
| **Gemini API Timeout or Rate Limit** | Medium | Enforce a strict 10s timeout in LangGraph; automatically fall back from `gemini-3.8-flash` to `gemini-3.6-flash`; display clean authentication/network error message if key is missing or invalid. |
| **Mobile Layout Overflow on 390px** | High | Use `max-height: 420px; overflow-y: auto;` on the investigation list; enforce `overflow-x: hidden` in CSS; run autonomous DevTools audit. |
| **Docker Permission Denied on HF Spaces** | High | Use canonical UID 1000 non-root user (`useradd -m -u 1000 user`) with full ownership of `/home/user/app`. |
| **Port Misconfiguration** | High | Hardcode port `7860` across local dev, `app.py`, Dockerfile, and Gunicorn command. |

---

## 4. Verification Checkpoints

* **[Checkpoint 1 - Slice 1]:** Backend models and empirical data tables load and output values within expected physical ranges.
* **[Checkpoint 2 - Slice 2]:** Backend physics and JSON integrity tests pass (`pytest tests/test_physics_models.py tests/test_data_integrity.py`).
* **[Checkpoint 3 - Slice 3]:** CSS stylesheet passes visual inspection; wallpapers, tokens, glassmorphism, and responsive rules are verified.
* **[Checkpoint 4 - Slice 4]:** LangGraph agent graph compiles and executes successfully (`pytest tests/test_agent_graph.py`), correctly handling Gemini 3.8/3.6 routing and propagating authentication errors.
* **[Checkpoint 5 - Slice 5]:** Dash layout instantiates cleanly and smoke tests confirm all components and default figures exist (`pytest tests/test_layout_rendering.py`).
* **[Checkpoint 6 - Slice 6]:** Local server runs on `http://127.0.0.1:7860`; environmental sliders update KPIs in $<100\text{ ms}$, literature selection switches among all 24 dedicated graphs, and chat updates `dcc.Store`.
* **[Checkpoint 7 - Slice 7]:** Full test suite passes (`pytest tests/ -v`) and autonomous Chrome DevTools audit confirms desktop (1920x1080) and mobile (390x844 px) responsiveness with zero horizontal overflow. [COMPLETED - 12/12 tests green]
* **[Checkpoint 8 - Slice 8]:** Docker container configuration verified with non-root UID 1000 user, `app.py` on port 7860, and Hugging Face Spaces `README.md` metadata frontmatter. [COMPLETED]

---

## 5. Execution Summary

* **Project Leadership:**
  * **Cesia Burgos:** Chief Executive Officer (CEO)
  * **Ethan Bula:** Chief Operating Officer (COO)
* **Status:** 100% Complete, Production-Ready for Hugging Face Spaces deployment.
* **Test Suite:** 12/12 passing (`1.63s`).
* **Code Quality:** Ruff lint clean across all application modules.
