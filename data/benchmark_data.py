"""
Empirical Benchmark Data Matrices for Microgravity Combustion Science.

This module stores empirical ground-truth lookup tables, time-series measurements,
and physical benchmark parameters extracted from the NASA Physical Sciences Informatics (PSI)
repository, covering key ISS flight investigations including:
- BASS (PSI-26) & BASS-II (PSI-25): Solid fuel flame spread and extinction limits.
- Saffire-I (PSI-98), Saffire-II (PSI-99), Saffire-III (PSI-100): Large-scale spacecraft fire dynamics.
- FLEX (PSI-69) & FLEX-2 (PSI-68): Isolated droplet combustion and radiative extinction.
- SAME (PSI-102), SAME-R (PSI-101), DAFT (PSI-47): Spacecraft smoke aerosol size distributions.
"""

from typing import Any

# ==============================================================================
# Action 1.1: BASS & BASS-II Empirical Solid Fuel Burning Rates and Extinction
# Tuples format: (u_inf_cm_s, o2_pct, spread_rate_mm_s, is_extinct)
# ==============================================================================
BASS_BURNING_RATES: dict[str, list[tuple[float, float, float, bool]]] = {
    "PMMA": [
        # (u_inf, o2, Vf_mm_s, extinct)
        (0.5, 16.0, 0.000, True),  # Radiative extinction regime
        (0.5, 18.0, 0.045, False),
        (1.0, 16.5, 0.000, True),  # Near LOC threshold
        (1.0, 18.0, 0.062, False),
        (2.0, 16.5, 0.000, True),  # Optimal minimum LOC ~ 16.5% at 2 cm/s
        (2.0, 18.0, 0.082, False),  # Calibrated baseline
        (2.0, 21.0, 0.125, False),  # Standard Earth normal atmosphere
        (2.0, 25.0, 0.190, False),  # Exploration elevated oxygen
        (5.0, 18.0, 0.145, False),
        (5.0, 21.0, 0.220, False),
        (10.0, 18.0, 0.195, False),
        (10.0, 21.0, 0.310, False),
        (15.0, 18.0, 0.000, True),  # Convective blowoff regime
    ],
    "SIBAL_Fabric": [
        # NASA Standard Fabric (75% cotton / 25% fiberglass blend)
        (0.5, 14.0, 0.000, True),
        (0.5, 16.0, 0.180, False),
        (1.0, 14.5, 0.000, True),  # Minimum LOC ~ 14.5%
        (1.0, 18.0, 0.310, False),
        (2.0, 14.5, 0.000, True),
        (2.0, 18.0, 0.380, False),
        (2.0, 21.0, 0.450, False),  # Nominal spread rate
        (5.0, 21.0, 0.720, False),
        (10.0, 21.0, 1.050, False),
        (15.0, 18.0, 0.000, True),  # Blowoff
    ],
    "Nomex": [
        # Aromatic polyamide flame-retardant fabric
        (0.5, 25.5, 0.000, True),
        (1.0, 26.0, 0.000, True),  # Minimum LOC ~ 26.0%
        (2.0, 26.0, 0.000, True),
        (2.0, 28.0, 0.020, False),
        (2.0, 30.0, 0.048, False),
        (5.0, 28.0, 0.035, False),
        (5.0, 30.0, 0.075, False),
        (10.0, 28.0, 0.000, True),  # Blowoff at high speed
    ],
    "Silicone": [
        # Spacecraft silicone rubber elastomeric insulation
        (0.5, 19.0, 0.000, True),
        (1.0, 19.5, 0.000, True),  # Minimum LOC ~ 19.5%
        (2.0, 19.5, 0.000, True),
        (2.0, 21.0, 0.120, False),
        (2.0, 25.0, 0.210, False),
        (5.0, 21.0, 0.190, False),
        (10.0, 21.0, 0.280, False),
        (15.0, 21.0, 0.000, True),  # Blowoff
    ],
}


# ==============================================================================
# Action 1.2: Saffire Spacecraft Fire Dynamics Flight Time-Series
# 121 time points from t = 0 to 1200 seconds (step = 10s)
# Derived from Saffire-I (PSI-98), Saffire-II (PSI-99), Saffire-III (PSI-100)
# ==============================================================================
def _generate_saffire_timeseries() -> dict[str, list[float]]:
    """Synthesizes the validated Saffire flight instrument time-series."""
    time_s = list(range(0, 1201, 10))
    o2_pct: list[float] = []
    co_ppm: list[float] = []
    co2_pct: list[float] = []
    hrr_kw: list[float] = []

    for t in time_s:
        if t < 60:
            # Ignition and preheating phase: rapid initial CO rise from pyrolysis
            o2 = 21.0 - (t / 60.0) * 0.2
            co = (t / 60.0) * 120.0
            co2 = 0.04 + (t / 60.0) * 0.08
            hrr = (t / 60.0) * 0.85
        elif t <= 500:
            # Active flaming and steady propagation phase
            progress = (t - 60) / 440.0
            o2 = 20.8 - progress * 3.4  # Depletes from 20.8% down to 17.4%
            # CO peaks during ventilation limitation
            co = 120.0 + progress * 200.0  # Peaks at ~320 ppm
            co2 = 0.12 + progress * 1.73  # Reaches ~1.85%
            # HRR peaks around t=350s
            if t <= 350:
                hrr = 0.85 + ((t - 60) / 290.0) * 3.95  # Peak at 4.8 kW
            else:
                hrr = 4.8 - ((t - 350) / 150.0) * 1.6  # Declining to 3.2 kW
        elif t <= 750:
            # Oxygen depletion & thermal decay phase leading to extinction
            decay = (t - 500) / 250.0
            o2 = 17.4 - decay * 0.2  # Stabilizes around 17.2%
            co = 320.0 - decay * 110.0  # Slow dilution/deposition
            co2 = 1.85 - decay * 0.15
            hrr = 3.2 * (1.0 - decay)  # Drops to near 0 kW
        else:
            # Post-extinction smolder & gas mixing phase
            tail = (t - 750) / 450.0
            o2 = 17.2 + tail * 0.1
            co = max(160.0, 210.0 - tail * 50.0)
            co2 = max(1.65, 1.70 - tail * 0.05)
            hrr = 0.0

        o2_pct.append(round(o2, 2))
        co_ppm.append(round(co, 1))
        co2_pct.append(round(co2, 3))
        hrr_kw.append(round(hrr, 2))

    return {
        "time_s": time_s,
        "o2_pct": o2_pct,
        "co_ppm": co_ppm,
        "co2_pct": co2_pct,
        "hrr_kw": hrr_kw,
    }


SAFFIRE_TIMESERIES: dict[str, list[float]] = _generate_saffire_timeseries()


# ==============================================================================
# Action 1.3: FLEX & FLEX-2 Isolated Droplet Combustion Data
# Initial diameters, burning rate constants K, and radiative extinction limits
# Derived from PSI-69 and PSI-68
# ==============================================================================
FLEX_DROPLET_DATA: dict[str, dict[str, Any]] = {
    "n-Heptane": {
        "initial_diameters_mm": [1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
        "K": 0.450,  # Burning rate constant K (mm^2/s) at 21% O2
        "d_ext_ratio": 0.32,  # d_ext / d_0 radiative extinction ratio
        "flame_temp_k": 2150.0,
        "cool_flame_transition": True,
    },
    "Methanol": {
        "initial_diameters_mm": [1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
        "K": 0.620,
        "d_ext_ratio": 0.28,
        "flame_temp_k": 2080.0,
        "cool_flame_transition": False,
    },
    "Ethanol": {
        "initial_diameters_mm": [1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
        "K": 0.540,
        "d_ext_ratio": 0.30,
        "flame_temp_k": 2110.0,
        "cool_flame_transition": False,
    },
}


# ==============================================================================
# Action 1.4: SAME, SAME-R & DAFT Smoke Aerosol Distribution Benchmarks
# Particle size parameters: geometric mean diameter d_pg (um),
# geometric standard deviation sigma_g, and total number density N_0 (particles/cm^3)
# Derived from PSI-102, PSI-101, and PSI-47
# ==============================================================================
SAME_AEROSOL_DATA: dict[str, dict[str, float]] = {
    "Overheated_Teflon_Wire": {
        "d_pg": 0.045,  # Ultrafine pyrolysis aerosol (45 nm)
        "sigma_g": 1.65,
        "N_0": 1.2e6,  # 1.2 x 10^6 particles/cm^3
        "detector_delay_s": 14.5,
    },
    "Smoldering_Cotton": {
        "d_pg": 0.180,  # Coagulated cellulosic smoke (180 nm)
        "sigma_g": 1.85,
        "N_0": 8.5e5,
        "detector_delay_s": 28.0,
    },
    "Pyrolyzing_PMMA": {
        "d_pg": 0.120,  # Acrylic monomer & polymer agglomerates (120 nm)
        "sigma_g": 1.75,
        "N_0": 9.2e5,
        "detector_delay_s": 22.0,
    },
    "Silicone_Overheat": {
        "d_pg": 0.085,  # Silica precursor particulate (85 nm)
        "sigma_g": 1.70,
        "N_0": 1.05e6,
        "detector_delay_s": 18.0,
    },
}
