"""
Unit Tests for Microgravity Combustion Physical and Computational Models.

Validates that:
- Limiting Oxygen Concentration (LOC) for PMMA at 2 cm/s matches BASS flight benchmarks (~16.5% O2).
- The non-monotonic U-curve flammability boundary exhibits both radiative extinction and convective blowoff.
- Solid flame spread rate V_f reflects concurrent enhancement over opposed conduction limitations.
- Droplet d^2(t) regression adheres to the Godsave-Spalding law with sudden radiative quenching.
- Smoke aerosol particle distributions produce physical geometric mean diameter peaks matching SAME data.
"""

import numpy as np

from data.microgravity_models import (
    compute_aerosol_distribution,
    compute_droplet_regression,
    compute_flame_spread_rate,
    compute_kpis,
    compute_loc,
)


def test_pmma_loc_matches_bass_flight_data() -> None:
    """Action 2.4: Validate that PMMA LOC at u_inf = 2.0 cm/s matches BASS flight data (16.5% +- 0.5%)."""
    loc_pmma = compute_loc(2.0, "PMMA")
    assert 16.0 <= loc_pmma <= 17.0, (
        f"PMMA LOC {loc_pmma}% O2 outside BASS flight tolerance [16.0%, 17.0%]"
    )


def test_loc_u_curve_behavior() -> None:
    """Action 2.5: Verify non-monotonic microgravity U-curve flammability boundaries."""
    loc_optimal = compute_loc(2.0, "PMMA")
    loc_quenched = compute_loc(0.2, "PMMA")
    loc_blown_off = compute_loc(15.0, "PMMA")

    # Low velocity radiative quenching demands higher oxygen concentration
    assert loc_quenched > loc_optimal, (
        f"Low velocity LOC ({loc_quenched}%) should exceed optimal LOC ({loc_optimal}%) due to radiative loss"
    )

    # High velocity convective blowoff also demands higher oxygen concentration
    assert loc_blown_off > loc_optimal, (
        f"High velocity LOC ({loc_blown_off}%) should exceed optimal LOC ({loc_optimal}%) due to flow residence time"
    )


def test_flame_spread_rate_trends() -> None:
    """Action 2.6: Validate that concurrent flow spreads faster than opposed flow."""
    v_conc = compute_flame_spread_rate(4.0, 21.0, "PMMA", "Concurrent")
    v_opp = compute_flame_spread_rate(4.0, 21.0, "PMMA", "Opposed")

    # Convective preheating in concurrent flow accelerates flame front relative to opposed
    assert v_conc > v_opp > 0.0, (
        f"Concurrent spread rate ({v_conc} mm/s) must exceed opposed spread rate ({v_opp} mm/s)"
    )

    # Sub-LOC environmental conditions must yield immediate flame extinction (0.0 mm/s)
    v_sub_loc = compute_flame_spread_rate(4.0, 15.0, "PMMA", "Concurrent")
    assert v_sub_loc == 0.0, (
        f"Flame spread below LOC threshold must be 0.0 mm/s, got {v_sub_loc}"
    )


def test_droplet_d2_law_monotonic_decay() -> None:
    """Action 2.7: Verify monotonic d^2(t) decay and finite positive radiative extinction limit."""
    _time_array, d2_array, d_ext = compute_droplet_regression(2.0, "n-Heptane", 21.0)

    # Initial droplet diameter squared must equal (2.0 mm)^2 = 4.0 mm^2
    assert d2_array[0] == 4.0, f"Initial d2 should be 4.0 mm^2, got {d2_array[0]}"

    # d^2(t) must be monotonically non-increasing across all time steps
    diffs = np.diff(d2_array)
    assert np.all(diffs <= 1e-9), "d^2(t) array contains non-physical increasing values"

    # Radiative extinction diameter must be positive and match the terminal plateau
    assert d_ext > 0.0, f"Extinction diameter must be positive, got {d_ext}"
    assert np.isclose(d2_array[-1], d_ext**2), (
        f"Terminal d2 value ({d2_array[-1]}) must equal d_ext^2 ({d_ext**2})"
    )


def test_aerosol_distribution_peak() -> None:
    """Action 2.8: Verify log-normal aerosol distribution exhibits physical peak matching SAME records."""
    dp, dist = compute_aerosol_distribution("Pyrolyzing_PMMA")

    assert len(dp) == 100, f"Expected 100 particle size bins, got {len(dp)}"
    peak_idx = int(np.argmax(dist))
    peak_dp = dp[peak_idx]

    # SAME flight sensors observe peak pyrolysis aerosol diameter between 0.05 and 0.30 um
    assert 0.05 <= peak_dp <= 0.30, (
        f"Pyrolysis aerosol peak diameter {peak_dp} um outside SAME sensor range [0.05, 0.30] um"
    )

    # Total concentration under curve must be positive
    assert np.max(dist) > 1e4, (
        f"Aerosol concentration peak ({np.max(dist)}) is non-physical"
    )


def test_kpi_aggregator_values() -> None:
    """Action 2.8b: Verify master KPI aggregator values match standard definitions."""
    kpis = compute_kpis(21.0, 2.0, "PMMA", "Concurrent")
    assert "loc_margin_pct" in kpis
    assert "flame_spread_mm_s" in kpis
    assert "peak_hrr_kw" in kpis
    assert "smoke_detection_time_s" in kpis

    # At 21% O2 and 2 cm/s for PMMA (LOC ~16.5%), margin must be +4.5% O2
    assert np.isclose(kpis["loc_margin_pct"], 4.5, atol=0.1)
    assert kpis["flame_spread_mm_s"] > 0.0
    assert kpis["peak_hrr_kw"] > 0.0
    assert kpis["smoke_detection_time_s"] > 0.0
