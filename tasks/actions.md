# Step-by-Step Fundamental Actions: NASA PSI Microgravity Dashboard

**Specification Reference:** [`SPEC.md` V1.3](file:///d:/NASA/SPEC.md)  
**Implementation Plan Reference:** [`tasks/plan.md`](file:///d:/NASA/tasks/plan.md)  
**Authors:** Cesia Burgos (Chief Executive Officer, CEO) & Ethan Bula (Chief Operating Officer, COO)  
**Target Platform:** Hugging Face Spaces (Port 7860, Docker, Non-Root UID 1000)  
**Execution Strategy:** Strictly Sequential (Slice 1 $\rightarrow$ Slice 8)  
**Language Standard:** 100% English across all modules, tests, UI labels, and documentation.

---

## Slice 1: Empirical Data Matrices & Microgravity Physical Models

### File: `data/benchmark_data.py`

#### Action 1.1: Empirical BASS & BASS-II Solid Fuel Regression Rates
- **Objective:** Establish the ground-truth empirical burning rate matrices and limiting oxygen concentrations (LOC) measured during the BASS (PSI-26) and BASS-II (PSI-25) flight experiments aboard the ISS.
- **Detailed Step:** Define dictionary `BASS_BURNING_RATES` with keys:
  * `"PMMA"`: Data tuples $(u_\infty\text{ [cm/s]}, \text{O}_2\text{ [\%]}, V_f\text{ [mm/s]}, \text{extinct [bool]})$ covering flow velocities from $0.5$ to $10.0\text{ cm/s}$ and oxygen concentrations from $15.0$ to $25.0\%$. Calibrated baseline: at $u_\infty = 2.0\text{ cm/s}$ and $\text{O}_2 = 18.0\%$, $V_f \approx 0.082\text{ mm/s}$; extinction occurs at $\le 16.5\% \text{ O}_2$.
  * `"SIBAL_Fabric"`: NASA standard fabric (75% cotton / 25% fiberglass blend) benchmarked in Saffire and BASS ($V_f \approx 0.45\text{ mm/s}$ at $u_\infty = 2.0\text{ cm/s}$, $\text{O}_2 = 21.0\%$; LOC $\approx 14.5\%$).
  * `"Nomex"`: High-performance aromatic polyamide ($V_f \approx 0.02\text{ mm/s}$ at $u_\infty = 2.0\text{ cm/s}$, $\text{O}_2 = 28.0\%$; LOC $\approx 26.0\%$).
  * `"Silicone"`: Elastomer benchmark ($V_f \approx 0.12\text{ mm/s}$ at $u_\infty = 2.0\text{ cm/s}$, $\text{O}_2 = 21.0\%$; LOC $\approx 19.5\%$).
- **Verification:** Execute `python -c "import data.benchmark_data as bd; assert 'PMMA' in bd.BASS_BURNING_RATES; assert len(bd.BASS_BURNING_RATES['PMMA']) >= 6; print('Action 1.1 Verified')"`

#### Action 1.2: Saffire Large-Scale Spacecraft Fire Dynamics Time-Series
- **Objective:** Store real-scale fire progression curves derived from Saffire-I (PSI-98), Saffire-II (PSI-99), and Saffire-III (PSI-100) tests on Cygnus cargo resupply vehicles.
- **Detailed Step:** Define dictionary `SAFFIRE_TIMESERIES` with 120 time points ($t = 0$ to $1200\text{ s}$ in steps of $10\text{ s}$):
  * `"time_s"`: NumPy array or list of integers $[0, 10, 20, \dots, 1200]$.
  * `"o2_pct"`: Initial $21.0\%$, decaying monotonically to $17.2\%$ during active flame phase ($t = 60\text{ s}$ to $600\text{ s}$), stabilizing post-extinction.
  * `"co_ppm"`: Initial $0\text{ ppm}$, surging during pre-flame smoldering ($t = 30\text{ s}$ to $90\text{ s}$) up to $185\text{ ppm}$, peaking at $320\text{ ppm}$ at $t = 450\text{ s}$.
  * `"co2_pct"`: Initial $0.04\%$, rising to peak of $1.85\%$ at $t = 500\text{ s}$.
  * `"hrr_kw"`: Peak heat release rate reaching $4.8\text{ kW}$ at $t = 350\text{ s}$.
- **Verification:** Execute `python -c "import data.benchmark_data as bd; assert len(bd.SAFFIRE_TIMESERIES['time_s']) == 121; assert max(bd.SAFFIRE_TIMESERIES['co_ppm']) > 300; print('Action 1.2 Verified')"`

#### Action 1.3: FLEX & FLEX-2 Isolated Droplet Extinction Data
- **Objective:** Curate droplet diameter regression and radiative extinction limits from PSI-69 and PSI-68.
- **Detailed Step:** Define dictionary `FLEX_DROPLET_DATA`:
  * Fuels: `"n-Heptane"`, `"Methanol"`, `"Ethanol"`.
  * For each fuel, specify: initial diameter $d_0 = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]\text{ mm}$, burning rate constant $K$ ($0.45\text{ mm}^2/\text{s}$ for n-Heptane, $0.62\text{ mm}^2/\text{s}$ for Methanol), and radiative extinction diameter $d_{ext}$ ($0.75\text{ mm}$ for n-Heptane).
- **Verification:** Execute `python -c "import data.benchmark_data as bd; assert bd.FLEX_DROPLET_DATA['n-Heptane']['K'] > 0; print('Action 1.3 Verified')"`

#### Action 1.4: SAME & DAFT Pyrolysis Smoke Aerosol Distributions
- **Objective:** Store smoke aerosol particle size parameters from SAME (PSI-102), SAME-R (PSI-101), and DAFT (PSI-47).
- **Detailed Step:** Define dictionary `SAME_AEROSOL_DATA` containing geometric mean diameters ($d_{pg}$ in $\mu\text{m}$), geometric standard deviations ($\sigma_g$), and total particle number densities ($N_0$ in particles/$\text{cm}^3$) for:
  * `"Overheated_Teflon_Wire"`: $d_{pg} = 0.045\ \mu\text{m}$, $\sigma_g = 1.65$, $N_0 = 1.2 \times 10^6$.
  * `"Smoldering_Cotton"`: $d_{pg} = 0.180\ \mu\text{m}$, $\sigma_g = 1.85$, $N_0 = 8.5 \times 10^5$.
  * `"Pyrolyzing_PMMA"`: $d_{pg} = 0.120\ \mu\text{m}$, $\sigma_g = 1.75$, $N_0 = 9.2 \times 10^5$.
- **Verification:** Execute `python -c "import data.benchmark_data as bd; assert bd.SAME_AEROSOL_DATA['Pyrolyzing_PMMA']['d_pg'] > 0; print('Action 1.4 Verified')"`

---

### File: `data/microgravity_models.py`

#### Action 1.5: Microgravity Limiting Oxygen Concentration (LOC) U-Curve Formula
- **Objective:** Model the non-monotonic microgravity flammability boundary curve as a function of forced flow speed ($u_\infty$).
- **Detailed Step:** Implement `compute_loc(u_inf_cm_s: float, fuel: str) -> float`:
  * Base LOC values at optimal velocity ($u_{opt} = 2.0\text{ cm/s}$): PMMA $\approx 16.5\%$, SIBAL Fabric $\approx 14.5\%$, Nomex $\approx 26.0\%$, Silicone $\approx 19.5\%$, n-Heptane $\approx 13.5\%$, Methane $\approx 12.0\%$, Ethylene $\approx 11.0\%$.
  * For $u_\infty < u_{opt}$: Radiative extinction regime where radiative heat loss exceeds combustion heat release:
    $$\text{LOC}(u_\infty) = \text{LOC}_{opt} + C_{rad} \left(\frac{1}{u_\infty + 0.1} - \frac{1}{u_{opt} + 0.1}\right)$$
  * For $u_\infty \ge u_{opt}$: Convective blowoff regime where flow residence time falls below chemical reaction time:
    $$\text{LOC}(u_\infty) = \text{LOC}_{opt} + C_{blow} (u_\infty - u_{opt})^{1.5}$$
  * Clamp returned LOC between $10.0\%$ and $40.0\%$.
- **Verification:** Execute `python -c "import data.microgravity_models as mm; loc_min = mm.compute_loc(2.0, 'PMMA'); loc_low = mm.compute_loc(0.2, 'PMMA'); loc_high = mm.compute_loc(15.0, 'PMMA'); assert loc_low > loc_min and loc_high > loc_min; print('Action 1.5 Verified')"`

#### Action 1.6: Solid & Fuel Flame Spread Rate ($V_f$) Model
- **Objective:** Compute flame spread velocity considering fuel type, oxygen concentration, forced airflow speed, and flow direction.
- **Detailed Step:** Implement `compute_flame_spread_rate(u_inf_cm_s: float, o2_pct: float, fuel: str, flow_direction: str = "Concurrent") -> float`:
  * If $\text{O}_2 \le \text{compute\_loc}(u_\infty, fuel)$, return $0.0\text{ mm/s}$ (extinction).
  * Effective oxygen driving force: $\Delta Y = \max(0.0, \frac{\text{O}_2 - \text{LOC}}{21.0 - \text{LOC}})$.
  * Concurrent Flow ($\text{flow\_direction} == \text{"Concurrent"}$): Flame propagates in the direction of the airflow, preheating unburned fuel ahead via convection:
    $$V_f = V_{f0} \cdot (1 + 0.45 \cdot u_\infty) \cdot (\Delta Y)^{1.2}$$
  * Opposed Flow ($\text{flow\_direction} == \text{"Opposed"}$): Flame propagates against airflow; conduction limited by boundary layer thickness:
    $$V_f = V_{f0} \cdot \left(0.85 + \frac{0.6}{1.0 + 0.3 \cdot u_\infty}\right) \cdot (\Delta Y)^{1.1}$$
- **Verification:** Execute `python -c "import data.microgravity_models as mm; v_conc = mm.compute_flame_spread_rate(4.0, 21.0, 'PMMA', 'Concurrent'); v_opp = mm.compute_flame_spread_rate(4.0, 21.0, 'PMMA', 'Opposed'); assert v_conc > v_opp > 0; print('Action 1.6 Verified')"`

#### Action 1.7: Droplet $d^2(t)$ Regression with Radiative Quenching
- **Objective:** Model isolated droplet regression adhering to Godsave-Spalding law with abrupt radiative quenching at $d_{ext}$.
- **Detailed Step:** Implement `compute_droplet_regression(d0_mm: float, fuel: str, o2_pct: float) -> tuple[np.ndarray, np.ndarray, float]`:
  * Time array $t = \text{np.linspace}(0, t_{burn}, 200)$.
  * Burning rate constant $K = K_{ref} \cdot (\text{O}_2 / 21.0)^{0.8}$.
  * Radiative extinction diameter $d_{ext} = d_0 \cdot 0.32 \cdot (21.0 / \text{O}_2)^{0.5}$.
  * For each time step, $d^2(t) = \max(d_{ext}^2, d_0^2 - K \cdot t)$.
  * Return tuple `(time_array, d2_array, d_ext)`.
- **Verification:** Execute `python -c "import data.microgravity_models as mm; t, d2, dext = mm.compute_droplet_regression(2.0, 'n-Heptane', 21.0); assert d2[0] == 4.0; assert d2[-1] == dext**2; print('Action 1.7 Verified')"`

#### Action 1.8: Aerosol Size Spectrum Log-Normal Function
- **Objective:** Generate particle size distribution curves for optical smoke detector simulation.
- **Detailed Step:** Implement `compute_aerosol_distribution(material: str) -> tuple[np.ndarray, np.ndarray]`:
  * Diameter array: $d_p = \text{np.logspace}(-2, 1, 100)$ (from $0.01\ \mu\text{m}$ to $10.0\ \mu\text{m}$).
  * Retrieve $d_{pg}$, $\sigma_g$, and $N_0$ from `data.benchmark_data.SAME_AEROSOL_DATA`.
  * Log-normal equation:
    $$\frac{dN}{d\log d_p} = \frac{N_0}{\sqrt{2\pi}\ln\sigma_g} \exp\left(-\frac{(\ln d_p - \ln d_{pg})^2}{2 (\ln\sigma_g)^2}\right)$$
  * Return `(d_p, dN_dlogdp)`.
- **Verification:** Execute `python -c "import data.microgravity_models as mm; dp, dist = mm.compute_aerosol_distribution('Pyrolyzing_PMMA'); assert len(dp) == 100; assert np.max(dist) > 0; print('Action 1.8 Verified')"`

#### Action 1.9: Master KPI Summary Aggregator
- **Objective:** Provide a fast, unified function that computes the 4 primary dashboard metrics simultaneously using standard NASA fire safety metrics.
- **Detailed Step:** Implement `compute_kpis(o2_pct: float, u_inf_cm_s: float, fuel: str, flow_direction: str) -> dict[str, float]`:
  * Calculate `loc = compute_loc(u_inf_cm_s, fuel)`.
  * Calculate `loc_margin = o2_pct - loc` ($\Delta \% \text{O}_2$, absolute percentage points difference above extinction).
  * Calculate `spread_rate = compute_flame_spread_rate(u_inf_cm_s, o2_pct, fuel, flow_direction)`.
  * Calculate `peak_hrr = spread_rate * 42.5 * (o2_pct / 21.0)` (in kW).
  * Calculate `detection_time = max(8.0, 180.0 / (u_inf_cm_s + 0.5) * (18.0 / o2_pct))` (in seconds).
  * Return dictionary: `{"loc_margin_pct": round(loc_margin, 2), "flame_spread_mm_s": round(spread_rate, 3), "peak_hrr_kw": round(peak_hrr, 2), "smoke_detection_time_s": round(detection_time, 1)}`.
- **Verification:** Execute `python -c "import data.microgravity_models as mm; kpis = mm.compute_kpis(21.0, 2.0, 'PMMA', 'Concurrent'); assert 'loc_margin_pct' in kpis; print('Action 1.9 Verified')"`

---

## Slice 2: Backend Unit Tests & Data Integrity Verification (TDD)

### File: `tests/test_data_integrity.py`

#### Action 2.1: Test JSON Existence & Enriched Size
- **Objective:** Enforce that the primary NASA dataset exists and matches the enriched flight payload size (~285 KB).
- **Detailed Step:** Implement `test_json_file_exists_and_size()`:
  * Path: `data/psi_combustion_science.json`.
  * Verify `os.path.exists(path) is True`.
  * Verify `280000 <= os.path.getsize(path) <= 305000`.
- **Verification:** Execute `pytest tests/test_data_integrity.py::test_json_file_exists_and_size -v`.

#### Action 2.2: Test Investigations Schema, Categories & Flight Metadata
- **Objective:** Guarantee all 24 investigations load as a list with complete scientific flight metadata and single normalized category.
- **Detailed Step:** Implement `test_investigations_count_and_keys()`:
  * Parse JSON file (`with open(...) as f: data = json.load(f)`).
  * Assert `isinstance(data, list) and len(data) == 24`.
  * For each investigation, assert presence and non-emptiness of: `"accession"`, `"title"`, `"category"`, `"platform"`, `"objectives"`, `"hypothesis"`, `"approach"`, `"publications"`.
  * Assert `item["category"] in ["Spacecraft Fire Safety", "Droplet Combustion", "Gaseous Combustion"]`.
- **Verification:** Execute `pytest tests/test_data_integrity.py::test_investigations_count_and_keys -v`.

#### Action 2.3: Test 347 Publications & Valid DOIs Where Present
- **Objective:** Verify every single scientific article across all investigations has a valid title, and for all publications with existing DOIs, verify valid standard DOI syntax.
- **Detailed Step:** Implement `test_publications_total_and_dois()`:
  * Iterate through all investigations and count publications.
  * Assert `total_publications == 347`.
  * For every publication, assert `len(item["title"].strip()) > 0`.
  * For publications that contain a non-empty DOI (`if item.get("doi"):`), assert `item["doi"].startswith("10.")`.
- **Verification:** Execute `pytest tests/test_data_integrity.py::test_publications_total_and_dois -v`.

---

### File: `tests/test_physics_models.py`

#### Action 2.4: Test PMMA LOC Flight Benchmark
- **Objective:** Confirm BASS flight record alignment for PMMA ($16.5\% \text{ O}_2 \pm 0.5\%$).
- **Detailed Step:** Implement `test_pmma_loc_matches_bass_flight_data()`:
  * Call `compute_loc(2.0, "PMMA")`.
  * Assert `16.0 <= loc <= 17.0`.
- **Verification:** Execute `pytest tests/test_physics_models.py::test_pmma_loc_matches_bass_flight_data -v`.

#### Action 2.5: Test U-Curve Non-Monotonic Extinction
- **Objective:** Confirm the U-curve shape has higher extinction boundaries at both low and high speeds.
- **Detailed Step:** Implement `test_loc_u_curve_behavior()`:
  * Assert `compute_loc(0.2, "PMMA") > compute_loc(2.0, "PMMA")` (radiative quenching).
  * Assert `compute_loc(15.0, "PMMA") > compute_loc(2.0, "PMMA")` (convective blowoff).
- **Verification:** Execute `pytest tests/test_physics_models.py::test_loc_u_curve_behavior -v`.

#### Action 2.6: Test Concurrent vs. Opposed Flame Spread
- **Objective:** Validate that concurrent flow spreads faster than opposed flow.
- **Detailed Step:** Implement `test_flame_spread_rate_trends()`:
  * Compute `v_conc = compute_flame_spread_rate(4.0, 21.0, "PMMA", "Concurrent")`.
  * Compute `v_opp = compute_flame_spread_rate(4.0, 21.0, "PMMA", "Opposed")`.
  * Assert `v_conc > v_opp > 0.0`.
  * Assert `compute_flame_spread_rate(4.0, 15.0, "PMMA", "Concurrent") == 0.0` (below LOC).
- **Verification:** Execute `pytest tests/test_physics_models.py::test_flame_spread_rate_trends -v`.

#### Action 2.7: Test Droplet $d^2(t)$ Monotonic Decay & Radiative Extinction
- **Objective:** Verify monotonic decrease and positive extinction diameter.
- **Detailed Step:** Implement `test_droplet_d2_law_monotonic_decay()`:
  * Call `t, d2, dext = compute_droplet_regression(2.0, "n-Heptane", 21.0)`.
  * Assert `np.all(np.diff(d2) <= 1e-9)` (monotonically non-increasing).
  * Assert `dext > 0.0` and `d2[-1] == dext**2`.
- **Verification:** Execute `pytest tests/test_physics_models.py::test_droplet_d2_law_monotonic_decay -v`.

#### Action 2.8: Test Aerosol Size Spectrum Peak
- **Objective:** Verify log-normal aerosol distribution exhibits physical peak.
- **Detailed Step:** Implement `test_aerosol_distribution_peak()`:
  * Call `dp, dist = compute_aerosol_distribution("Pyrolyzing_PMMA")`.
  * Peak diameter index `idx = np.argmax(dist)`.
  * Assert `0.05 <= dp[idx] <= 0.30` (matching SAME flight sensor ranges).
- **Verification:** Execute `pytest tests/test_physics_models.py::test_aerosol_distribution_peak -v`.

#### Action 2.9: Full Pytest Slice 2 Gate Pass
- **Objective:** Run both test files and confirm 100% green pass.
- **Detailed Step:** Run `pytest tests/test_data_integrity.py tests/test_physics_models.py -v`.
- **Verification:** Check console output: `passed` on all test cases with zero warnings or errors.

---

## Slice 3: Design System, Scrollytelling & CSS Tokens

### File: `assets/custom.css`

#### Action 3.1: Define CSS Variables & NASA HUD Design Tokens
- **Objective:** Establish the glassmorphic dark aerospace palette.
- **Detailed Step:** Define `:root` with:
  * `--bg-dark: #0b0f19;`
  * `--card-bg: rgba(19, 24, 38, 0.85);`
  * `--bg-card: var(--card-bg);`
  * `--border-cyan: rgba(56, 189, 248, 0.25);`
  * `--border-glow: 0 0 12px rgba(56, 189, 248, 0.35);`
  * `--accent-cyan: #38bdf8;`
  * `--accent-orange: #f97316;`
  * `--accent-red: #ef4444;`
  * `--text-main: #f8fafc;`
  * `--text-muted: #94a3b8;`
  * `--navbar-height: 64px;`
- **Verification:** Syntax check and confirm all variables exist in `:root`.

#### Action 3.2: Implement 4 Scrollytelling Wallpaper Sections
- **Objective:** Map each vertical section anchor to its dedicated wallpaper with dark contrast overlays.
- **Detailed Step:** Implement CSS classes:
  * `.section-dashboard`: `background: linear-gradient(180deg, rgba(11, 15, 25, 0.86), rgba(11, 15, 25, 0.94)), url('/assets/wallpapers/wallpaper1.png') center/cover no-repeat fixed; min-height: 100vh; padding: 40px 0;`
  * `.section-literature`: `background: linear-gradient(180deg, rgba(11, 15, 25, 0.88), rgba(11, 15, 25, 0.95)), url('/assets/wallpapers/wallpaper2.png') center/cover no-repeat fixed; min-height: 100vh; padding: 40px 0;`
  * `.section-agent`: `background: linear-gradient(180deg, rgba(11, 15, 25, 0.84), rgba(11, 15, 25, 0.92)), url('/assets/wallpapers/wallpaper3.png') center/cover no-repeat fixed; min-height: 90vh; padding: 40px 0;`
  * `.section-info`: `background: linear-gradient(180deg, rgba(11, 15, 25, 0.90), rgba(11, 15, 25, 0.98)), url('/assets/wallpapers/wallpaper4.png') center/cover no-repeat fixed; min-height: 60vh; padding: 40px 0;`
- **Verification:** Verify that all 4 wallpaper files exist in `assets/wallpapers/` and match paths.

#### Action 3.3: Implement Glassmorphic Card Styling (`.hud-card`)
- **Objective:** Render high-contrast aerospace HUD cards with subtle cyan glow.
- **Detailed Step:** Define `.hud-card`:
  * `background: var(--bg-card);`
  * `backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);`
  * `border: 1px solid var(--border-cyan);`
  * `border-radius: 12px;`
  * `box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);`
  * `.hud-card:hover { border-color: rgba(56, 189, 248, 0.5); box-shadow: var(--border-glow); }`
- **Verification:** Inspect CSS properties and pseudo-states.

#### Action 3.4: Implement Sticky Top Navbar & Smooth Scroll
- **Objective:** Build sticky navigation with smooth scrolling to `#section` targets.
- **Detailed Step:** Add rules:
  * `html { scroll-behavior: smooth; }`
  * `.sticky-navbar`: `position: sticky; top: 0; z-index: 1050; background: rgba(11, 15, 25, 0.92); backdrop-filter: blur(10px); border-bottom: 1px solid var(--border-cyan); height: var(--navbar-height);`
  * Nav link active and hover states with cyan glow indicator.
- **Verification:** Verify smooth scroll behavior and z-index hierarchy.

#### Action 3.5: Implement Fixed-Height Scrollable Literature Container
- **Objective:** Prevent vertical layout explosion on mobile and desktop by constraining the 24-item list.
- **Detailed Step:** Define `.investigation-list-scroll`:
  * `max-height: 420px;`
  * `overflow-y: auto;`
  * `overflow-x: hidden;`
  * `scrollbar-width: thin; scrollbar-color: var(--accent-cyan) var(--bg-dark);`
  * `&::-webkit-scrollbar { width: 6px; }`
  * `&::-webkit-scrollbar-thumb { background: var(--accent-cyan); border-radius: 3px; }`
- **Verification:** Inspect scrollbar styles and max-height bounds.

#### Action 3.6: Mobile Media Queries & Touch Target Enforcement
- **Objective:** Guarantee flawless responsiveness on mobile (e.g. 390px iPhone viewport).
- **Detailed Step:** Add media queries `@media (max-width: 768px)`:
  * `html, body { overflow-x: hidden !important; width: 100vw; }`
  * `button, .form-control, .form-select, .rc-slider-handle { min-height: 44px; min-width: 44px; }`
  * `.section-dashboard, .section-literature, .section-agent, .section-info { background-attachment: scroll; }` (for smooth mobile GPU rendering).
- **Verification:** Verify touch target dimensions and zero horizontal overflow constraints.

---

## Slice 4: LangGraph AI Copilot Engine

### File: `agent/state.py`

#### Action 4.1: Define LangGraph State Schema
- **Objective:** Establish the typed dictionary governing conversation history and live dashboard state.
- **Detailed Step:** Implement `CombustionAgentState(TypedDict)`:
  * `messages: Annotated[list[BaseMessage], add_messages]`
  * `current_scenario: dict[str, Any]` (holding `o2_pct`, `u_inf_cm_s`, `fuel`, `flow_direction`)
  * `selected_investigation: dict[str, Any]` (holding `accession`, `title`, `abstract`, `hardware`)
  * `error: Optional[str]`
- **Verification:** Execute `python -c "from agent.state import CombustionAgentState; print('Action 4.1 Verified')"`

---

### File: `agent/prompts.py`

#### Action 4.2: Define NASA Combustion Science Grounding Prompt
- **Objective:** Enforce scientific rigor, live dashboard awareness, and DOI citation.
- **Detailed Step:** Define `SYSTEM_PROMPT = """..."""`:
  * Explicit role: Autonomous AI Copilot for the NASA Physical Sciences Informatics (PSI) Microgravity Combustion Dashboard.
  * Authors acknowledgment: Cesia Burgos (Chief Executive Officer, CEO) and Ethan Bula (Chief Operating Officer, COO).
  * Knowledge boundary: Restrict claims strictly to the 24 NASA PSI Combustion investigations.
  * Live scenario instructions: Cite the active oxygen level, airflow velocity, fuel, and calculated flammability margin when answering.
  * Citation mandate: When describing an experimental effect, include the paper's title, authors, and DOI string (`https://doi.org/...`).
  * Anti-hallucination constraint: If asked about conditions not studied in PSI, state explicitly: "This condition falls outside the flight-verified NASA PSI microgravity dataset."
- **Verification:** Execute `python -c "from agent.prompts import SYSTEM_PROMPT; assert 'Cesia Burgos' in SYSTEM_PROMPT; assert 'Ethan Bula' in SYSTEM_PROMPT; print('Action 4.2 Verified')"`

---

### File: `agent/graph.py`

#### Action 4.3: Implement StateGraph with Model Router & Fallback
- **Objective:** Compile the LangGraph engine with `gemini-3.8-flash` primary model, `gemini-3.6-flash` fallback, 10s timeout, and unauthenticated error message.
- **Detailed Step:** Implement `agent/graph.py`:
  * Initialize `primary_llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0.2, timeout=10.0)`.
  * Initialize `fallback_llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.2, timeout=10.0)`.
  * Bind fallback: `llm = primary_llm.with_fallbacks([fallback_llm])`.
  * Implement node `def call_model(state: CombustionAgentState) -> dict`:
    * Check if `"GEMINI_API_KEY"` in `os.environ` and not empty.
    * If missing, return `{"messages": [AIMessage(content="**Authentication Notice:** A valid `GEMINI_API_KEY` is required to communicate with the NASA PSI AI Copilot. Please set your key in the environment to activate full conversational reasoning.")]}`.
    * Build context string from `state["current_scenario"]` and `state["selected_investigation"]`.
    * Invoke `llm.invoke([SystemMessage(content=SYSTEM_PROMPT + context_str)] + state["messages"])`.
    * Wrap in `try...except` block catching timeout (>10s) or connection errors, returning an informative error message.
  * Assemble graph:
    * `builder = StateGraph(CombustionAgentState)`
    * `builder.add_node("agent", call_model)`
    * `builder.set_entry_point("agent")`
    * `builder.add_edge("agent", END)`
    * `app_graph = builder.compile()`
- **Verification:** Execute `python -c "from agent.graph import app_graph; assert app_graph is not None; print('Action 4.3 Verified')"`

---

### File: `tests/test_agent_graph.py`

#### Action 4.4: Verify Graph Compilation & Execution
- **Objective:** Automated test ensuring the StateGraph instantiates and routes correctly.
- **Detailed Step:** Implement:
  * `test_graph_structure()`: Verifies node "agent" exists and compiles.
  * `test_unauthenticated_clean_error()`: Monkeypeach `GEMINI_API_KEY` to `""`, invokes `app_graph.invoke(...)`, asserts the response message is an `AIMessage` containing "Authentication Notice" or "GEMINI_API_KEY is required".
- **Verification:** Execute `pytest tests/test_agent_graph.py -v`.

---

## Slice 5: Dash UI Layout & Scrollytelling Assembly (`layout.py`, `app.py` & `data/investigation_charts.py`)

### File: `data/investigation_charts.py`

#### Action 5.1: Implement Shared HUD Plotly Theming Helper
- **Objective:** Ensure every chart follows a consistent dark NASA aerospace HUD visual language.
- **Detailed Step:** Implement `apply_hud_theme(fig: go.Figure, title: str, x_title: str, y_title: str) -> go.Figure`:
  * `paper_bgcolor: 'rgba(0,0,0,0)'`, `plot_bgcolor: 'rgba(15, 23, 42, 0.6)'`.
  * Font family: `Inter, -apple-system, sans-serif`, color: `#f8fafc`.
  * Grid lines: color `rgba(56, 189, 248, 0.12)`.
  * Zero line: color `rgba(56, 189, 248, 0.3)`.
  * Margin: `l=50, r=20, t=50, b=50`.
  * Hovermode: `"x unified"`.
- **Verification:** Execute `python -c "import plotly.graph_objects as go; from data.investigation_charts import apply_hud_theme; fig = apply_hud_theme(go.Figure(), 'Test', 'X', 'Y'); assert fig.layout.font.color == '#f8fafc'; print('Action 5.1 Verified')"`

#### Action 5.2: Implement 24 Dedicated Investigation Plotly Figures
- **Objective:** Create distinct, scientifically grounded interactive charts for each of the 24 PSI investigations.
- **Detailed Step:** Implement individual functions returning `go.Figure`:
  1. `chart_psi_69_flex()`: Droplet $d^2(t)$ regression curve and radiative extinction diameter.
  2. `chart_psi_68_flex_2()`: Burning rate constant $K$ vs. initial droplet diameter.
  3. `chart_psi_23_acme_sflame()`: Spherical flame diameter vs. stretch rate.
  4. `chart_psi_10_acme_flame_design()`: Radial soot volume fraction $f_v(r)$.
  5. `chart_psi_22_acme_efield()`: Liftoff height vs. applied electric field voltage.
  6. `chart_psi_21_acme_cld_flame()`: Coflow laminar diffusion flame length vs. fuel velocity.
  7. `chart_psi_25_bass_ii()`: Solid fuel regression rate vs. forced flow speed.
  8. `chart_psi_20_acme_bre()`: Porous burner heat feedback vs. mass burning rate.
  9. `chart_psi_102_same()`: Smoke aerosol size distribution $dN/d\log d_p$.
  10. `chart_psi_142_cool_flame()`: Cool flame extinction limit vs. strain rate.
  11. `chart_psi_26_bass()`: PMMA LOC U-curve boundary.
  12. `chart_psi_117_cfd()`: Cool flame oscillation frequency vs. Damköhler number.
  13. `chart_psi_107_spice()`: Smoke point fuel flow rate vs. microgravity coflow velocity.
  14. `chart_psi_39_cfi()`: Droplet cool flame transition temperature vs. pressure.
  15. `chart_psi_99_saffire_ii()`: Material flammability limit vs. cabin pressure.
  16. `chart_psi_98_saffire_i()`: Fabric flame spread rate and heat release rate.
  17. `chart_psi_101_same_r()`: Particle agglomeration count decay over time.
  18. `chart_psi_62_fgm()`: 2D flamelet temperature profile vs. BASS experimental data.
  19. `chart_psi_100_saffire_iii()`: Thick PMMA flame spread rate vs. airflow.
  20. `chart_psi_47_daft()`: Dust vs. smoke aerosol light scattering ratio.
  21. `chart_psi_159_acme_cfig()`: Gaseous cool flame burning rate vs. $CO_2/He$ dilution.
  22. `chart_psi_60_spice_reanalysis()`: Soot yield fraction vs. time.
  23. `chart_psi_106_slice()`: Gaseous diffusion flame liftoff velocity vs. air speed.
  24. `chart_psi_115_same_modeling()`: CFD simulation vs. flight particle coagulation kinetics.
- **Verification:** Execute `python -c "import data.investigation_charts as ic; assert all(hasattr(ic, f'chart_psi_{num}') for num in ['69_flex', '26_bass', '98_saffire_i', '102_same']); print('Action 5.2 Verified')"`

#### Action 5.3: Implement Investigation Chart Dispatcher
- **Objective:** Provide a single dispatch function `get_investigation_chart(accession: str) -> go.Figure`.
- **Detailed Step:** Map accession strings (`"PSI-69"`, `"PSI-26"`, etc.) to their respective chart builder functions, falling back to a clean placeholder figure if unknown.
- **Verification:** Execute `python -c "from data.investigation_charts import get_investigation_chart; fig = get_investigation_chart('PSI-26'); assert fig is not None; print('Action 5.3 Verified')"`

---

### File: `layout.py`

#### Action 5.4: Implement Sticky Top Navbar Component
- **Objective:** Build the fixed top navigation bar with anchor links.
- **Detailed Step:** Implement `build_navbar() -> dbc.Navbar`:
  * Logo: NASA meatball / PSI badge.
  * Brand: "NASA PSI | Microgravity Flammability & Fire Safety Dashboard".
  * Nav links: `[{"label": "Dashboard", "href": "#dashboard"}, {"label": "Literature", "href": "#literature"}, {"label": "AI Copilot", "href": "#agent"}, {"label": "Project Info", "href": "#info"}]`.
  * Class: `sticky-navbar px-4`.
- **Verification:** Execute `python -c "from layout import build_navbar; nb = build_navbar(); assert nb is not None; print('Action 5.4 Verified')"`

#### Action 5.5: Implement Section 1: Dashboard (`#dashboard`)
- **Objective:** Build control sliders, reactive flow toggle, 4 KPI cards, and 2x2 Plotly grid.
- **Detailed Step:** Implement `build_dashboard_section() -> html.Div`:
  * Outer div: `id="dashboard"`, `className="section-dashboard"`.
  * Control bar card:
    * Oxygen slider: `dcc.Slider(id="slider-o2", min=14.0, max=30.0, step=0.5, value=21.0, marks={15: '15%', 21: '21% (Earth)', 30: '30%'})`.
    * Forced velocity slider: `dcc.Slider(id="slider-velocity", min=0.0, max=15.0, step=0.5, value=2.0, marks={0: '0', 2: '2 cm/s (ISS)', 10: '10', 15: '15 cm/s'})`.
    * Fuel dropdown (Standardized across PSI Flight Databases): `dcc.Dropdown(id="dropdown-fuel", options=[{"label": "PMMA (Acrylic Slab)", "value": "PMMA"}, {"label": "SIBAL Fabric (Cotton/Fiberglass)", "value": "SIBAL_Fabric"}, {"label": "Nomex (Aromatic Polyamide)", "value": "Nomex"}, {"label": "Silicone Rubber", "value": "Silicone"}, {"label": "n-Heptane Droplets", "value": "n-Heptane"}, {"label": "Methane Gas (CH4)", "value": "Methane"}, {"label": "Ethylene Gas (C2H4)", "value": "Ethylene"}], value="PMMA")`.
    * Flow direction toggle: `dbc.RadioItems(id="toggle-flow-direction", options=[{"label": "Concurrent (Downwind)", "value": "Concurrent"}, {"label": "Opposed (Upwind)", "value": "Opposed"}], value="Concurrent", inline=True)`.
  * KPI row: 4 glassmorphic cards (`id="kpi-margin"`, `id="kpi-spread"`, `id="kpi-hrr"`, `id="kpi-detection"`).
  * 2x2 Plotly grid:
    * `dcc.Graph(id="graph-g1-loc", config={"responsive": True, "displayModeBar": False})`
    * `dcc.Graph(id="graph-g2-spread", config={"responsive": True, "displayModeBar": False})`
    * `dcc.Graph(id="graph-g3-saffire", config={"responsive": True, "displayModeBar": False})`
    * `dcc.Graph(id="graph-g4-aerosol", config={"responsive": True, "displayModeBar": False})`
- **Verification:** Execute `python -c "from layout import build_dashboard_section; sec1 = build_dashboard_section(); assert sec1 is not None; print('Action 5.5 Verified')"`

#### Action 5.6: Implement Section 2: Literature Explorer (`#literature`)
- **Objective:** Build the 3-column Master-Detail explorer with normalized category filters, constrained scrollable list, empty initial state, and dedicated graph container.
- **Detailed Step:** Implement `build_literature_section(investigations: list) -> html.Div`:
  * Outer div: `id="literature"`, `className="section-literature"`.
  * Column 1 (Filters, width 3): Search input (`id="input-search"`), Category filter (`dcc.Dropdown(id="dropdown-category", options=[{"label": "All Categories", "value": "ALL"}, {"label": "Spacecraft Fire Safety", "value": "Spacecraft Fire Safety"}, {"label": "Droplet Combustion", "value": "Droplet Combustion"}, {"label": "Gaseous Combustion", "value": "Gaseous Combustion"}], value="ALL")`), Platform filter (`dcc.Dropdown(id="dropdown-platform", options=[{"label": "All Platforms", "value": "ALL"}, {"label": "International Space Station (ISS)", "value": "International Space Station (ISS)"}, {"label": "Cygnus Spacecraft", "value": "Cygnus Spacecraft"}, {"label": "Not Applicable", "value": "Not Applicable"}], value="ALL")`).
  * Column 2 (List, width 4): Header with count badge (`id="badge-investigation-count"`), scroll container `html.Div(id="container-investigation-list", className="investigation-list-scroll")` rendering accession, acronym, title, and category badge.
  * Column 3 (Detail, width 5):
    * Top detail card `html.Div(id="container-investigation-detail")`: Initially empty, displaying prompt *"Select an investigation from the list to view its flight research objectives, hypothesis, approach, space/earth impacts, and dedicated experimental data."* When an investigation is selected, displays PI (`principal_investigator`), Center (`monitoring_center`), hardware (`experiment_hardware`), tabbed scientific summary (`Objectives`, `Hypothesis`, `Approach`, `Research Impacts / Earth Benefits`), and publications table (existing DOIs render clickable `https://doi.org/{doi}`; empty DOIs render formatted citation text without hyperlink).
    * Bottom chart container `dcc.Graph(id="graph-investigation-detail", config={"responsive": True})`: Initially empty figure (`go.Figure()`) until user selects an investigation.
- **Verification:** Execute `python -c "from layout import build_literature_section; sec2 = build_literature_section([]); assert sec2 is not None; print('Action 5.6 Verified')"`

#### Action 5.7: Implement Section 3: AI Copilot (`#agent`)
- **Objective:** Build the dark aerospace console chat feed with suggestion pills and radar loader.
- **Detailed Step:** Implement `build_agent_section() -> html.Div`:
  * Outer div: `id="agent"`, `className="section-agent"`.
  * Suggestion pills row: `html.Div(id="pills-container", children=[dbc.Button("Explain current scenario", id="pill-1", size="sm", className="me-2 pill-btn"), dbc.Button("Synthesize active investigation", id="pill-2", size="sm", className="me-2 pill-btn"), dbc.Button("Why does CO surge in microgravity?", id="pill-3", size="sm", className="pill-btn")])`.
  * Chat scroll container: `html.Div(id="chat-feed-container", style={"height": "400px", "overflowY": "auto"})`.
  * Input row: `dbc.Input(id="chat-input", placeholder="Ask the NASA PSI Copilot about microgravity combustion...", type="text")`, `dbc.Button("Transmit", id="chat-send-btn", color="primary", className="ms-2")`.
  * Loading indicator: `dcc.Loading(id="loading-agent", type="circle", children=html.Div(id="agent-loading-output"))`.
- **Verification:** Execute `python -c "from layout import build_agent_section; sec3 = build_agent_section(); assert sec3 is not None; print('Action 5.7 Verified')"`

#### Action 5.8: Implement Section 4: Project Info & Stack (`#info`)
- **Objective:** Build metadata cards, author attribution, and JSON download button.
- **Detailed Step:** Implement `build_info_section() -> html.Div`:
  * Outer div: `id="info"`, `className="section-info"`.
  * Provenance card: NASA PSI Physical Sciences Informatics, 24 investigations, 347 articles (~285 KB enriched JSON from 12.21 TB payload).
  * Engineering credits card: Cesia Burgos (Chief Executive Officer, CEO) and Ethan Bula (Chief Operating Officer, COO).
  * Tech stack badges: Python 3.12, Dash, Plotly, LangGraph, Google Gemini, Docker, Hugging Face Spaces.
  * Export button: `dbc.Button("Download PSI Dataset (JSON)", id="btn-download-json", color="info")`, `dcc.Download(id="download-json")`.
- **Verification:** Execute `python -c "from layout import build_info_section; sec4 = build_info_section(); assert sec4 is not None; print('Action 5.8 Verified')"`

#### Action 5.9: Implement Master Layout Assembler (`create_layout()`)
- **Objective:** Combine all sections, navigation bar, and state stores into a single layout tree.
- **Detailed Step:** Implement `create_layout() -> html.Div`:
  * Include `dcc.Store(id="store-scenario")` and `dcc.Store(id="store-selected-investigation")`.
  * Include `build_navbar()`.
  * Include `build_dashboard_section()`.
  * Include `build_literature_section(investigations)`.
  * Include `build_agent_section()`.
  * Include `build_info_section()`.
- **Verification:** Execute `python -c "from layout import create_layout; layout = create_layout(); assert layout is not None; print('Action 5.9 Verified')"`

---

### File: `app.py`

#### Action 5.10: Assemble Main Dash Application Entrypoint
- **Objective:** Initialize the Dash app, mount `layout.py`, register callbacks, and configure the WSGI server for Hugging Face Spaces.
- **Detailed Step:** Implement `app.py`:
  * Import `dash`, `dash_bootstrap_components as dbc`.
  * Import `create_layout` from `layout`.
  * Import `register_callbacks` from `callbacks`.
  * Configure: `app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])`.
  * Set `server = app.server`.
  * Set `app.title = "NASA PSI Microgravity Flammability & Fire Safety Dashboard"`.
  * Set `app.layout = create_layout()`.
  * Call `register_callbacks(app)`.
  * Add main runner: `if __name__ == "__main__": app.run_server(host="0.0.0.0", port=7860, debug=False)`.
- **Verification:** Execute `python -c "import app; assert app.server is not None; print('Action 5.10 Verified')"`

---

### File: `tests/test_layout_rendering.py`

#### Action 5.11: Automated Layout Smoke Tests
- **Objective:** Verify layout instantiation and component existence without running the full server.
- **Detailed Step:** Implement:
  * `test_layout_exists()`: Confirms `create_layout()` returns a non-null object.
  * `test_required_component_ids()`: Traverses the layout tree and asserts presence of: `"slider-o2"`, `"slider-velocity"`, `"dropdown-fuel"`, `"toggle-flow-direction"`, `"tooltip-flow-direction"`, `"kpi-margin"`, `"kpi-spread"`, `"kpi-hrr"`, `"kpi-detection"`, `"graph-g1-loc"`, `"graph-g2-spread"`, `"graph-g3-saffire"`, `"graph-g4-aerosol"`, `"input-search"`, `"dropdown-category"`, `"dropdown-platform"`, `"container-investigation-list"`, `"graph-investigation-detail"`, `"chat-input"`, `"chat-send-btn"`, `"chat-feed-container"`, `"btn-download-json"`.
- **Verification:** Execute `pytest tests/test_layout_rendering.py -v`.

---

## Slice 6: Reactive Callbacks Engine (`callbacks.py`)

### File: `callbacks.py`

#### Action 6.1: Fuel Selection & Flow Direction Reactive Lockout Callback
- **Objective:** Enable flow direction toggle for solid materials; disable it with an informative tooltip for droplets or gases without mutating internal component state (Option 1).
- **Detailed Step:** Register callback:
  * `@app.callback([Output("toggle-flow-direction", "options"), Output("toggle-flow-direction", "className"), Output("tooltip-flow-direction", "children")], [Input("dropdown-fuel", "value")])`
  * If fuel in `["PMMA", "SIBAL_Fabric", "Nomex", "Silicone"]`:
    * Set options: `[{"label": "Concurrent (Downwind)", "value": "Concurrent", "disabled": False}, {"label": "Opposed (Upwind)", "value": "Opposed", "disabled": False}]`
    * Set className: `"flow-toggle-enabled"`
    * Set tooltip: `"Forced airflow orientation relative to solid flame propagation front."`
  * If fuel in `["n-Heptane", "Methane", "Ethylene"]`:
    * Set options: `[{"label": "Concurrent (Downwind)", "value": "Concurrent", "disabled": True}, {"label": "Opposed (Upwind)", "value": "Opposed", "disabled": True}]`
    * Set className: `"flow-toggle-disabled opacity-50"`
    * Set tooltip: `"Not applicable (Spherical symmetry and radial diffusion in microgravity)"`
  * Note: The internal `value` of `toggle-flow-direction` is preserved (not mutated to an invalid string), and the underlying computational model in `data/microgravity_models.py` mathematically ignores flow direction for droplets and gases.
- **Verification:** Unit test callback function with mock inputs verifying that `options[0]["disabled"] is True` for `"n-Heptane"` and `False` for `"SIBAL_Fabric"`.

#### Action 6.2: Section 1 Environmental Sliders & Dashboard Reactivity Callback
- **Objective:** Update 4 KPIs and 4 Section 1 charts in $<100\text{ ms}$ upon slider or dropdown adjustment.
- **Detailed Step:** Register callback:
  * Inputs: `slider-o2.value`, `slider-velocity.value`, `dropdown-fuel.value`, `toggle-flow-direction.value`.
  * Outputs: `kpi-margin.children`, `kpi-spread.children`, `kpi-hrr.children`, `kpi-detection.children`, `graph-g1-loc.figure`, `graph-g2-spread.figure`, `graph-g3-saffire.figure`, `graph-g4-aerosol.figure`, `store-scenario.data`.
  * Compute KPIs with `compute_kpis(...)`.
  * Generate G1 (LOC U-curve with current operating point marker).
  * Generate G2 (Flame spread rate vs. forced flow speed curve).
  * Generate G3 (Saffire spacecraft fire dynamic concentration traces).
  * Generate G4 (SAME smoke aerosol size distribution).
  * Return all formatted values and figures.
- **Verification:** Verify that the callback executes in $< 100\text{ ms}$ using Python's `time.perf_counter()`.

#### Action 6.3: Section 2 Literature Search & Filtering Callback
- **Objective:** Filter all 24 investigations in real time by keyword, normalized category, and platform.
- **Detailed Step:** Register callback:
  * Inputs: `input-search.value`, `dropdown-category.value`, `dropdown-platform.value`.
  * Outputs: `container-investigation-list.children`, `badge-investigation-count.children`.
  * Filter logic: Case-insensitive search matching title, abstract, PI, and keywords; match normalized `category` (`Spacecraft Fire Safety`, `Droplet Combustion`, `Gaseous Combustion`); match normalized `platform` (`International Space Station (ISS)`, `Cygnus Spacecraft`, `Not Applicable`).
  * Render updated list of clickable cards.
- **Verification:** Unit test filter callback with keyword `"Saffire"` and category `"Spacecraft Fire Safety"` and assert matching cards returned.

#### Action 6.4: Section 2 Investigation Detail & 24 Dedicated Charts Callback
- **Objective:** Clicking an investigation renders its scientific flight summary, valid clickable DOIs, and calls `data/investigation_charts.py` for its exact dedicated chart.
- **Detailed Step:** Register callback:
  * Inputs: `{"type": "investigation-card", "index": ALL}.n_clicks`.
  * Outputs: `container-investigation-detail.children`, `graph-investigation-detail.figure`, `store-selected-investigation.data`.
  * Retrieve selected investigation object from JSON.
  * Build tabbed detail summary (PI, Center, Hardware, Objectives, Hypothesis, Approach, Research Impacts / Earth Benefits).
  * Build publications table: for articles with an existing DOI, render clickable link `https://doi.org/{doi}`; for articles without a DOI, render formatted citation text without hyperlink.
  * Call `get_investigation_chart(accession)` to produce the exact dedicated figure.
- **Verification:** Unit test callback with accession `"PSI-98"` and assert Saffire-I chart is produced.
  * Inputs: `{"type": "investigation-card", "index": ALL}.n_clicks`.
  * Outputs: `container-investigation-detail.children`, `graph-investigation-detail.figure`, `store-selected-investigation.data`.
  * Retrieve selected investigation object from JSON.
  * Build tabbed detail summary (Objectives, Hypothesis, Approach, Space/Earth Impact).
  * Build DOI links table (`https://doi.org/{doi}`).
  * Call `get_investigation_chart(accession)` to produce the exact dedicated figure.
- **Verification:** Unit test callback with accession `"PSI-98"` and assert Saffire-I chart is produced.

#### Action 6.5: Section 3 AI Copilot Chat Synchronous Execution Callback
- **Objective:** Process user prompt, inject live `dcc.Store` scenario and investigation context, invoke LangGraph, and render Markdown response.
- **Detailed Step:** Register callback:
  * Inputs: `chat-send-btn.n_clicks`, `chat-input.n_submit`, `pill-1.n_clicks`, `pill-2.n_clicks`, `pill-3.n_clicks`.
  * States: `chat-input.value`, `store-scenario.data`, `store-selected-investigation.data`, `chat-feed-container.children`.
  * Outputs: `chat-feed-container.children`, `chat-input.value`.
  * Check trigger source. If a pill was clicked, use the pill's predefined text.
  * Format prompt and invoke `app_graph.invoke({"messages": [HumanMessage(content=prompt)], "current_scenario": scenario, "selected_investigation": investigation})`.
  * Append user message and AI response bubble to chat feed.
- **Verification:** Execute callback with mock unauthenticated state and verify error bubble returned.

#### Action 6.6: Section 4 Dataset Download Callback
- **Objective:** Send `psi_combustion_science.json` to the user's browser upon button click.
- **Detailed Step:** Register callback:
  * Inputs: `btn-download-json.n_clicks`.
  * Outputs: `download-json.data`.
  * Send file using `dcc.send_file("data/psi_combustion_science.json")`.
- **Verification:** Verify callback returns valid `dcc.send_file` dict.

---

## Slice 7: Autonomous Testing & Mobile Viewport Audit

#### Action 7.1: Execute Full Pytest Test Suite
- **Objective:** Ensure 100% test pass across all backend, data, agent, and layout test modules.
- **Detailed Step:** Run `pytest tests/ -v --tb=short`.
- **Verification:** Verify output: `12 passed in X.XXs` with 0 failures and 0 errors.

#### Action 7.2: Launch Local Testing Server
- **Objective:** Run the Dash application locally on port 7860.
- **Detailed Step:** Execute `python app.py` as a background process; verify HTTP 200 on `http://127.0.0.1:7860`.
- **Verification:** Curl or test request returns HTTP 200.

#### Action 7.3: Deploy Autonomous DevTools Desktop Audit (1920x1080)
- **Objective:** Verify layout rendering, slider reactivity, and chart switching in Chrome DevTools.
- **Detailed Step:** Deploy autonomous `browser` subagent:
  * Navigate to `http://127.0.0.1:7860`.
  * Verify top navbar anchors smoothly scroll to `#dashboard`, `#literature`, `#agent`, `#info`.
  * Move oxygen slider from 21% to 25%; verify KPI margin updates.
  * Click on `"PSI-98 (SAFFIRE-I)"` in literature list; verify `#graph-investigation-detail` updates with Saffire-I chart.
  * Transmit prompt `"Explain current scenario"`; verify message bubble appears.
  * Check DevTools console for uncaught exceptions (0 errors required).
- **Verification:** DevTools subagent reports all tests green with 0 console errors.

#### Action 7.4: Deploy Autonomous DevTools Mobile Audit (390x844 Viewport)
- **Objective:** Verify mobile UX, touch target compliance, and zero horizontal scroll.
- **Detailed Step:** Deploy autonomous `browser` subagent with viewport 390x844:
  * Execute JavaScript: `return window.innerWidth === document.documentElement.scrollWidth;` (must return `true`).
  * Check `.investigation-list-scroll`: verify internal vertical scrolling works and max-height is $\le 420\text{px}$.
  * Check touch targets on sliders and buttons: verify bounding boxes $\ge 44\text{px} \times 44\text{px}$.
- **Verification:** DevTools subagent confirms zero horizontal overflow and full touch-target compliance.

#### Action 7.5: Clean Server Shutdown
- **Objective:** Terminate the local testing server process cleanly.
- **Detailed Step:** Stop background process.
- **Verification:** Confirm port 7860 is released.

---

## Slice 8: Containerization & Hugging Face Spaces Deployment

### File: `Dockerfile`

#### Action 8.1: Write Production Dockerfile (UID 1000)
- **Objective:** Configure standard Hugging Face Spaces container environment.
- **Detailed Step:** Write `Dockerfile`:
  ```dockerfile
  FROM python:3.12-slim

  RUN useradd -m -u 1000 user
  USER user
  ENV HOME=/home/user \
      PATH=/home/user/.local/bin:$PATH \
      PYTHONUNBUFFERED=1

  WORKDIR $HOME/app

  COPY --chown=user requirements.txt .
  RUN pip install --no-cache-dir --user -r requirements.txt

  COPY --chown=user . $HOME/app

  EXPOSE 7860

  CMD ["gunicorn", "app:server", "--workers", "2", "--threads", "4", "--timeout", "120", "--bind", "0.0.0.0:7860"]
  ```
- **Verification:** Verify Dockerfile syntax and non-root UID 1000 user permissions.

---

### File: `README.md`

#### Action 8.2: Create Hugging Face Spaces Metadata & Documentation
- **Objective:** Create Spaces README with YAML frontmatter.
- **Detailed Step:** Write `README.md`:
  * YAML Frontmatter:
    ```yaml
    ---
    title: NASA PSI Microgravity Flammability & Fire Safety Dashboard
    emoji: 🚀
    colorFrom: blue
    colorTo: cyan
    sdk: docker
    app_port: 7860
    ---
    ```
  * Documentation sections: Project Overview, Scientific Dataset Provenance (NASA PSI, ~285 KB enriched JSON from 12.21 TB archive), Engineering Team Credits (Cesia Burgos, CEO & Ethan Bula, COO), Architecture Summary, and Local Execution Guide.
- **Verification:** Check YAML frontmatter syntax and verify documentation sections.

#### Action 8.3: Deployment Readiness Verification
- **Objective:** Final verification pass ensuring all files match Hugging Face Spaces requirements.
- **Detailed Step:** Confirm `Dockerfile`, `README.md`, `requirements.txt`, `app.py`, `layout.py`, `callbacks.py`, `data/`, `agent/`, `assets/`, and `tests/` are present and ready for deployment.
- **Verification:** All checks pass.

