"""
Microgravity Combustion Physics & Computational Models.

This module implements pure scientific calculations and physics models for microgravity
combustion phenomena without UI dependencies, including:
- Limiting Oxygen Concentration (LOC) U-curve flammability boundaries.
- Solid and fuel flame spread rates (V_f) under concurrent and opposed forced flows.
- Godsave-Spalding droplet combustion d^2(t) law with abrupt radiative extinction.
- Log-normal smoke aerosol particle size distributions for optical detector simulation.
- Master KPI aggregator for spacecraft environmental fire safety assessments.
"""

import numpy as np

from data.benchmark_data import FLEX_DROPLET_DATA, SAME_AEROSOL_DATA

# ==============================================================================
# Base physical properties and calibration constants
# ==============================================================================
FUEL_PROPERTIES: dict[str, dict[str, float]] = {
    "PMMA": {
        "loc_opt": 16.5,  # Minimum LOC (% O2) at optimal velocity
        "u_opt": 2.0,  # Optimal airflow velocity (cm/s)
        "c_rad": 1.25,  # Radiative heat loss coefficient
        "c_blow": 0.085,  # Convective blowoff coefficient
        "vf0": 0.082,  # Baseline flame spread velocity (mm/s)
        "hrr_coeff": 42.5,  # Heat release conversion factor
        "is_solid": True,
    },
    "SIBAL_Fabric": {
        "loc_opt": 14.5,  # Saffire/BASS standard cellulosic fabric
        "u_opt": 2.0,
        "c_rad": 1.10,
        "c_blow": 0.075,
        "vf0": 0.450,
        "hrr_coeff": 65.0,
        "is_solid": True,
    },
    "Nomex": {
        "loc_opt": 26.0,  # Aromatic polyamide flame-retardant fabric
        "u_opt": 2.0,
        "c_rad": 1.40,
        "c_blow": 0.120,
        "vf0": 0.020,
        "hrr_coeff": 28.0,
        "is_solid": True,
    },
    "Silicone": {
        "loc_opt": 19.5,  # Spacecraft elastomer insulation
        "u_opt": 2.0,
        "c_rad": 1.30,
        "c_blow": 0.090,
        "vf0": 0.120,
        "hrr_coeff": 35.0,
        "is_solid": True,
    },
    "n-Heptane": {
        "loc_opt": 13.5,  # FLEX isolated droplet extinction limit
        "u_opt": 1.5,
        "c_rad": 0.95,
        "c_blow": 0.060,
        "vf0": 0.350,
        "hrr_coeff": 48.0,
        "is_solid": False,
    },
    "Methane": {
        "loc_opt": 12.0,  # ACME gaseous coflow diffusion flame limit
        "u_opt": 2.0,
        "c_rad": 0.85,
        "c_blow": 0.050,
        "vf0": 0.280,
        "hrr_coeff": 52.0,
        "is_solid": False,
    },
    "Ethylene": {
        "loc_opt": 11.0,  # ACME Flame Design soot inception limit
        "u_opt": 2.0,
        "c_rad": 0.80,
        "c_blow": 0.045,
        "vf0": 0.320,
        "hrr_coeff": 55.0,
        "is_solid": False,
    },
}


# ==============================================================================
# Action 1.5: Microgravity Limiting Oxygen Concentration (LOC) U-Curve
# ==============================================================================
def compute_loc(u_inf_cm_s: float, fuel: str) -> float:
    """Computes the Limiting Oxygen Concentration (LOC) in % O2 as a function

    of forced airflow velocity (u_inf) and fuel material.

    Models the characteristic microgravity U-curve:
    - At low velocities (u_inf < u_opt): Radiative heat losses dominate and exceed
      chemical heat release, causing radiative extinction unless O2 is elevated.
    - At optimal velocity (u_inf ~ u_opt): Minimum LOC is observed.
    - At high velocities (u_inf > u_opt): Convective residence time falls below
      chemical kinetic times, driving convective blowoff extinction.
    """
    props = FUEL_PROPERTIES.get(fuel, FUEL_PROPERTIES["PMMA"])
    loc_opt = props["loc_opt"]
    u_opt = props["u_opt"]
    c_rad = props["c_rad"]
    c_blow = props["c_blow"]

    u = max(0.0, float(u_inf_cm_s))

    if u < u_opt:
        # Radiative extinction regime
        delta = c_rad * (1.0 / (u + 0.1) - 1.0 / (u_opt + 0.1))
        loc = loc_opt + delta
    else:
        # Convective blowoff regime
        delta = c_blow * ((u - u_opt) ** 1.5)
        loc = loc_opt + delta

    return float(np.clip(loc, 10.0, 40.0))


# ==============================================================================
# Action 1.6: Solid & Fuel Flame Spread Rate (V_f) Model
# ==============================================================================
def compute_flame_spread_rate(
    u_inf_cm_s: float,
    o2_pct: float,
    fuel: str,
    flow_direction: str = "Concurrent",
) -> float:
    """Computes flame spread rate V_f (mm/s) taking into account oxygen driving force,

    forced flow velocity, and concurrent vs. opposed flow directions.

    Extinguishes (returns 0.0 mm/s) when ambient O2 is below the dynamic LOC.
    For droplet and gaseous fuels, flow direction is physically non-applicable
    (radial diffusion / isotropic flame structure).
    """
    props = FUEL_PROPERTIES.get(fuel, FUEL_PROPERTIES["PMMA"])
    loc = compute_loc(u_inf_cm_s, fuel)

    if o2_pct <= loc:
        return 0.0

    # Effective dimensionless oxygen driving force
    # Scaled relative to standard 21.0% Earth normal reference
    driving_force = max(0.0, (o2_pct - loc) / max(0.5, 21.0 - loc))
    u = max(0.0, float(u_inf_cm_s))
    vf0 = props["vf0"]

    if props["is_solid"]:
        if flow_direction == "Concurrent":
            # Convective preheating enhances flame front advance
            vf = vf0 * (1.0 + 0.45 * u) * (driving_force**1.2)
        else:
            # Opposed flow: heat conduction through boundary layer is thinned by flow
            opp_factor = 0.85 + 0.60 / (1.0 + 0.30 * u)
            vf = vf0 * opp_factor * (driving_force**1.1)
    else:
        # Isotropic radial diffusion / droplet & gaseous envelope
        vf = vf0 * (1.0 + 0.15 * u) * (driving_force**1.15)

    return float(max(0.0, vf))


# ==============================================================================
# Action 1.7: Droplet d^2(t) Regression with Radiative Quenching
# ==============================================================================
def compute_droplet_regression(
    d0_mm: float,
    fuel: str = "n-Heptane",
    o2_pct: float = 21.0,
) -> tuple[np.ndarray, np.ndarray, float]:
    """Models isolated droplet combustion obeying the d^2-law with sudden

    radiative quenching at extinction diameter d_ext.

    Returns:
        (time_array_s, d2_array_mm2, d_ext_mm)
    """
    droplet_info = FLEX_DROPLET_DATA.get(fuel, FLEX_DROPLET_DATA["n-Heptane"])
    k_ref = droplet_info["K"]
    ext_ratio = droplet_info["d_ext_ratio"]

    # Burning rate constant K scales with ambient oxygen concentration
    k = k_ref * ((max(14.0, o2_pct) / 21.0) ** 0.8)

    # Radiative extinction diameter d_ext increases as oxygen decreases
    d_ext = float(d0_mm * ext_ratio * ((21.0 / max(14.0, o2_pct)) ** 0.5))
    d0_sq = float(d0_mm**2)
    dext_sq = float(d_ext**2)

    # Estimated burn duration until radiative extinction
    t_burn = max(0.1, (d0_sq - dext_sq) / max(0.01, k))
    t_total = t_burn * 1.35  # Extended post-extinction plateau window

    time_array = np.linspace(0.0, t_total, 200)
    d2_array = np.maximum(dext_sq, d0_sq - k * time_array)

    return time_array, d2_array, d_ext


# ==============================================================================
# Action 1.8: Aerosol Size Spectrum Log-Normal Distribution
# ==============================================================================
def compute_aerosol_distribution(
    material: str,
    u_inf: float = 2.0,
    o2_pct: float = 21.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Generates particle size distribution spectrum dN/dlog(dp) for smoke precursors.

    Grounded in SAME (PSI-102), SAME-R (PSI-101), and DAFT (PSI-47) flight sensor records,
    incorporating Smoluchowski Brownian coagulation kinetics and ventilation airflow dilution:
    - Lower u_inf prolongs residence time, accelerating Brownian coagulation and shifting
      geometric mean diameter d_pg to larger sizes.
    - Higher u_inf increases convective dilution, reducing peak number concentration N_0.
    - Elevated O2 enhances soot yield and aerosol number density.

    Args:
        material: Target precursor material key.
        u_inf: Cabin forced ventilation airflow velocity in cm/s (nominal 2.0).
        o2_pct: Ambient oxygen concentration in % O2 (nominal 21.0).

    Returns:
        (dp_microns, dN_dlogdp)
    """
    data = SAME_AEROSOL_DATA.get(material, SAME_AEROSOL_DATA["Pyrolyzing_PMMA"])
    d_pg_base = data["d_pg"]
    sigma_g = data["sigma_g"]
    n0_base = data["N_0"]

    # Smoluchowski residence time scaling: tau_res proportional to 1 / (u_inf + 0.5)
    # At nominal u_inf = 2.0 cm/s, factor is 1.0. At u_inf = 0.5, factor > 1 (coagulation growth)
    coagulation_factor = (1.0 + 0.45 * (2.0 / (max(0.1, u_inf) + 0.5) - 0.8)) ** (1.0 / 3.0)
    d_pg = d_pg_base * max(0.7, min(1.8, coagulation_factor))

    # Convective dilution and oxygen soot yield scaling
    dilution_factor = 2.5 / (max(0.1, u_inf) + 0.5)
    o2_factor = (max(14.0, o2_pct) / 21.0) ** 0.6
    n0 = n0_base * max(0.4, min(2.5, dilution_factor * o2_factor))

    # Logarithmic diameter space spanning 0.01 um (10 nm) to 10 um
    dp = np.logspace(-2.0, 1.0, 100)
    ln_sigma_g = np.log(sigma_g)

    # Standard log-normal aerosol density equation
    exponent = -((np.log(dp) - np.log(d_pg)) ** 2) / (2.0 * (ln_sigma_g**2))
    dn_dlogdp = (n0 / (np.sqrt(2.0 * np.pi) * ln_sigma_g)) * np.exp(exponent)

    return dp, dn_dlogdp


# ==============================================================================
# Action 1.9: Master KPI Summary Aggregator
# ==============================================================================
def compute_kpis(
    o2_pct: float,
    u_inf_cm_s: float,
    fuel: str,
    flow_direction: str = "Concurrent",
) -> dict[str, float]:
    """Aggregates the 4 core fire safety metrics in < 1 ms:

    1. loc_margin_pct: Absolute oxygen difference relative to LOC (Delta % O2).
    2. flame_spread_mm_s: Projected flame front propagation speed (mm/s).
    3. peak_hrr_kw: Projected thermal heat release hazard power (kW).
    4. smoke_detection_time_s: Projected time to smoke sensor alarm threshold (s).
    """
    props = FUEL_PROPERTIES.get(fuel, FUEL_PROPERTIES["PMMA"])
    loc = compute_loc(u_inf_cm_s, fuel)
    loc_margin = o2_pct - loc

    spread_rate = compute_flame_spread_rate(u_inf_cm_s, o2_pct, fuel, flow_direction)
    hrr_coeff = props["hrr_coeff"]
    peak_hrr = spread_rate * hrr_coeff * (o2_pct / 21.0)

    # Smoke detection delay accounts for convective transport lag and dilution
    u = max(0.0, float(u_inf_cm_s))
    detection_time = max(8.0, 180.0 / (u + 0.5) * (18.0 / max(10.0, o2_pct)))

    return {
        "loc_margin_pct": round(loc_margin, 2),
        "flame_spread_mm_s": round(spread_rate, 3),
        "peak_hrr_kw": round(peak_hrr, 2),
        "smoke_detection_time_s": round(detection_time, 1),
    }
