"""Specialized Plotly figure generators for the 24 NASA PSI Combustion Science investigations.

Authors: Cesia Burgos (Chief Executive Officer, CEO) & Ethan Bula (Chief Operating Officer, COO).
"""

from __future__ import annotations

from typing import Any

import numpy as np
import plotly.graph_objects as go

from data.benchmark_data import (
    BASS_BURNING_RATES,
    SAFFIRE_TIMESERIES,
)
from data.microgravity_models import (
    compute_aerosol_distribution,
    compute_droplet_regression,
    compute_loc,
)


def apply_hud_theme(
    fig: go.Figure,
    title: str = "",
    x_title: str = "",
    y_title: str = "",
) -> go.Figure:
    """Apply the NASA aerospace dark HUD visual theme to a Plotly figure."""
    fig.update_layout(
        title={
            "text": title,
            "x": 0.04,
            "xanchor": "left",
            "font": {"size": 13, "color": "#fbdc08", "family": "'Courier New', Courier, monospace"},
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        font={
            "family": "'Courier New', Courier, monospace",
            "color": "#f8fafc",
            "size": 12,
        },
        margin={"l": 58, "r": 20, "t": 38, "b": 36},
        title_x=0.5,
        title_xanchor="center",
        autosize=True,
        hovermode="x unified",
        hoverlabel={
            "bgcolor": "#0b1329",
            "bordercolor": "rgba(255, 255, 255, 0.4)",
            "font": {
                "family": "'Courier New', Courier, monospace",
                "color": "#f8fafc",
                "size": 12,
            },
        },
        xaxis={
            "title": {"text": x_title, "font": {"size": 11, "color": "#94a3b8"}},
            "gridcolor": "rgba(255, 255, 255, 0.08)",
            "zerolinecolor": "rgba(217, 17, 25, 0.3)",
            "showgrid": True,
            "zeroline": True,
            "tickfont": {"size": 10, "color": "#94a3b8"},
        },
        yaxis={
            "title": {"text": y_title, "font": {"size": 11, "color": "#94a3b8"}},
            "gridcolor": "rgba(255, 255, 255, 0.08)",
            "zerolinecolor": "rgba(217, 17, 25, 0.3)",
            "showgrid": True,
            "zeroline": True,
            "tickfont": {"size": 10, "color": "#94a3b8"},
        },
        legend={
            "bgcolor": "rgba(11, 15, 25, 0.7)",
            "bordercolor": "rgba(217, 17, 25, 0.35)",
            "borderwidth": 1,
            "font": {"size": 10, "color": "#f8fafc"},
        },
    )
    return fig


# ==============================================================================
# 24 Dedicated Investigation Plotly Figures
# ==============================================================================


def chart_psi_69_flex() -> go.Figure:
    """PSI-69: FLEX - Droplet d2(t) regression & radiative extinction."""
    time_pts, d2_pts, dext = compute_droplet_regression(
        d0_mm=2.5, fuel="n-Heptane", o2_pct=21.0
    )
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=time_pts,
            y=d2_pts,
            mode="lines",
            name="d²(t) Flight Data",
            line={"color": "#0cb64d", "width": 2.5},
        )
    )
    fig.add_hline(
        y=dext**2,
        line_dash="dash",
        line_color="#d91119",
        annotation_text=f"Radiative Extinction (d_ext={dext:.2f} mm)",
        annotation_position="bottom right",
    )
    return apply_hud_theme(
        fig,
        "PSI-69: FLEX Droplet Combustion d²-Law & Extinction",
        "Combustion Time (s)",
        "Droplet Diameter Squared (mm²)",
    )


def chart_psi_68_flex_2() -> go.Figure:
    """PSI-68: FLEX-2 - Burning rate constant K vs initial droplet diameter."""
    d0_range = np.linspace(1.5, 4.0, 25)
    # FLEX-2 showed K increases slightly with d0 due to radiative feedback
    k_pure = 0.78 + 0.04 * (d0_range - 1.5)
    k_diluted = 0.58 + 0.03 * (d0_range - 1.5)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=d0_range,
            y=k_pure,
            mode="lines+markers",
            name="Pure n-Heptane",
            line={"color": "#0cb64d", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=d0_range,
            y=k_diluted,
            mode="lines+markers",
            name="CO₂ Diluted",
            line={"color": "#fbdc08", "width": 2},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-68: FLEX-2 Burning Rate Constant vs Droplet Size",
        "Initial Droplet Diameter d₀ (mm)",
        "Burning Rate Constant K (mm²/s)",
    )


def chart_psi_23_acme_sflame() -> go.Figure:
    """PSI-23: ACME s-Flame - Spherical flame diameter vs stretch rate."""
    stretch = np.linspace(5, 50, 30)
    # As stretch rate increases, spherical flame diameter contracts
    d_flame_ch4 = 28.0 * np.exp(-0.035 * stretch) + 8.0
    d_flame_c2h4 = 34.0 * np.exp(-0.028 * stretch) + 10.0

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=stretch,
            y=d_flame_ch4,
            mode="lines",
            name="CH₄ / O₂ / N₂",
            line={"color": "#0cb64d", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=stretch,
            y=d_flame_c2h4,
            mode="lines",
            name="C₂H₄ / O₂ / N₂",
            line={"color": "#fbdc08", "width": 2},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-23: ACME s-Flame Diameter vs Stretch Rate",
        "Stretch Rate a_s (1/s)",
        "Spherical Flame Diameter (mm)",
    )


def chart_psi_10_acme_flame_design() -> go.Figure:
    """PSI-10: ACME Flame Design - Radial soot volume fraction f_v(r)."""
    radius = np.linspace(0, 15, 60)
    # Peak soot occurs in the annular reaction sheet
    fv = 3.5 * np.exp(-((radius - 6.2) ** 2) / 3.2)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=radius,
            y=fv,
            mode="lines",
            fill="tozeroy",
            name="Soot Fraction",
            line={"color": "#0cb64d", "width": 2.5},
            fillcolor="rgba(6, 136, 57, 0.2)",
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-10: ACME Flame Design Soot Volume Fraction Profile",
        "Radial Distance r (mm)",
        "Soot Volume Fraction f_v (ppm)",
    )


def chart_psi_22_acme_efield() -> go.Figure:
    """PSI-22: ACME E-FIELD Flames - Liftoff height vs electric field voltage."""
    voltage = np.linspace(-5.0, 5.0, 21)
    # Positive voltage repels ionic wind, shifting flame attachment
    liftoff = 12.0 - 1.8 * voltage + 0.15 * (voltage**2)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=voltage,
            y=liftoff,
            mode="lines+markers",
            name="Ionic Response",
            line={"color": "#fbdc08", "width": 2},
            marker={"size": 6, "color": "#fbdc08"},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-22: ACME E-FIELD Flame Liftoff vs Applied Potential",
        "Applied Electrode Voltage (kV)",
        "Flame Liftoff Height (mm)",
    )


def chart_psi_21_acme_cld_flame() -> go.Figure:
    """PSI-21: ACME CLD Flame - Coflow laminar flame length vs fuel velocity."""
    v_fuel = np.linspace(5, 50, 25)
    l_flame_iss = 1.4 * v_fuel + 4.0
    l_flame_1g = 0.85 * v_fuel + 6.0

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=v_fuel,
            y=l_flame_iss,
            mode="lines",
            name="Microgravity μg",
            line={"color": "#fbdc08", "width": 2.5},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=v_fuel,
            y=l_flame_1g,
            mode="lines",
            name="Normal 1-g",
            line={"color": "#94a3b8", "dash": "dot"},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-21: ACME CLD Coflow Flame Length Scaling",
        "Fuel Jet Velocity (cm/s)",
        "Laminar Flame Length (mm)",
    )


def chart_psi_25_bass_ii() -> go.Figure:
    """PSI-25: BASS-II - Solid fuel regression rate vs forced flow speed."""
    data = BASS_BURNING_RATES["PMMA"]
    u_vals = [d[0] for d in data if d[1] == 21.0]
    r_vals = [d[2] for d in data if d[1] == 21.0]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=u_vals,
            y=r_vals,
            mode="lines+markers",
            name="Thick PMMA (21% O₂)",
            line={"color": "#fbdc08", "width": 2},
            marker={"size": 7, "color": "#fbdc08"},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-25: BASS-II Solid Fuel Burning Rate vs Forced Airflow",
        "Forced Airflow Velocity u_inf (cm/s)",
        "Spread Rate (mm/s)",
    )


def chart_psi_20_acme_bre() -> go.Figure:
    """PSI-20: ACME BRE - Porous burner heat feedback vs mass burning rate."""
    m_dot = np.linspace(0.01, 0.12, 20)
    q_feedback = 18.0 * (1.0 - np.exp(-15.0 * m_dot))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=m_dot,
            y=q_feedback,
            mode="lines",
            name="Net Heat Flux",
            line={"color": "#d91119", "width": 2.5},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-20: ACME BRE Porous Burner Surface Heat Feedback",
        "Mass Blowing Rate (g/s·cm²)",
        "Heat Flux to Burner (kW/m²)",
    )


def chart_psi_102_same() -> go.Figure:
    """PSI-102: SAME - Smoke aerosol size distribution dN/dlog(dp)."""
    dp_pmma, dist_pmma = compute_aerosol_distribution("Pyrolyzing_PMMA")
    dp_tef, dist_tef = compute_aerosol_distribution("Teflon")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dp_pmma,
            y=dist_pmma,
            mode="lines",
            name="PMMA Smoke",
            line={"color": "#0cb64d", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dp_tef,
            y=dist_tef,
            mode="lines",
            name="Teflon Smoke",
            line={"color": "#fbdc08", "width": 2},
        )
    )
    fig.update_xaxes(type="log")
    return apply_hud_theme(
        fig,
        "PSI-102: SAME Flight Smoke Particle Size Spectrum",
        "Particle Diameter d_p (µm, Log Scale)",
        "Concentration dN/dlog(d_p) (particles/cm³)",
    )


def chart_psi_142_cool_flame() -> go.Figure:
    """PSI-142: Cool Flame Transition - Extinction limit vs strain rate."""
    strain = np.linspace(2, 40, 25)
    t_cool = 680 - 4.5 * strain + 0.05 * (strain**2)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=strain,
            y=t_cool,
            mode="lines",
            name="Cool Extinction",
            line={"color": "#d91119", "width": 2.5},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-142: Cool Flame Transition Temperature vs Strain Rate",
        "Local Strain Rate (1/s)",
        "Cool Flame Peak Temperature (K)",
    )


def chart_psi_26_bass() -> go.Figure:
    """PSI-26: BASS - PMMA flammability U-curve boundary."""
    u_vals = np.linspace(0.2, 15.0, 50)
    loc_vals = [compute_loc(u, "PMMA") for u in u_vals]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=u_vals,
            y=loc_vals,
            mode="lines",
            name="LOC Limit",
            line={"color": "#d91119", "width": 2.5},
        )
    )
    fig.add_annotation(
        x=2.0,
        y=16.5,
        text="Optimal Minimum LOC (16.5% at 2 cm/s)",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#fbdc08",
        font={"color": "#fbdc08"},
    )
    return apply_hud_theme(
        fig,
        "PSI-26: BASS PMMA Microgravity Flammability Boundary (LOC)",
        "Forced Airflow Velocity u_inf (cm/s)",
        "Limiting Oxygen Concentration (% O₂)",
    )


def chart_psi_117_cfd() -> go.Figure:
    """PSI-117: CFD Droplet Flames - Oscillation frequency vs Damköhler number."""
    da = np.linspace(1.2, 8.0, 30)
    freq = 2.4 * np.sqrt(np.maximum(0, da - 1.2)) * np.exp(-0.15 * da)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=da,
            y=freq,
            mode="lines",
            name="Instability Limit",
            line={"color": "#fbdc08", "width": 2},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-117: Droplet Flame Oscillation vs Damköhler Number",
        "Damköhler Number (Da)",
        "Oscillation Frequency f (Hz)",
    )


def chart_psi_107_spice() -> go.Figure:
    """PSI-107: SPICE - Smoke point fuel flow rate vs coflow air speed."""
    u_coflow = np.linspace(2, 20, 25)
    # In microgravity, higher coflow delays soot residence time, raising smoke point
    q_smoke = 12.0 + 1.15 * u_coflow

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=u_coflow,
            y=q_smoke,
            mode="lines+markers",
            name="Smoke Point Limit",
            line={"color": "#0cb64d", "width": 2},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-107: SPICE Critical Smoke Point vs Coflow Airflow",
        "Coflow Air Velocity (cm/s)",
        "Critical Fuel Flow Rate (sccm)",
    )


def chart_psi_39_cfi() -> go.Figure:
    """PSI-39: CFI - Cool Flames Investigation droplet extinction diameter vs pressure."""
    p_atm = np.linspace(0.5, 2.0, 20)
    d_ext = 0.95 * (p_atm**-0.25)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=p_atm,
            y=d_ext,
            mode="lines+markers",
            name="n-Alkane Droplets",
            line={"color": "#0cb64d", "width": 2},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-39: CFI Extinction Diameter vs Chamber Pressure",
        "Chamber Pressure (atm)",
        "Radiative Extinction Diameter d_ext (mm)",
    )


def chart_psi_99_saffire_ii() -> go.Figure:
    """PSI-99: Saffire-II - Material flammability limit vs cabin pressure."""
    p_psia = np.linspace(8.0, 14.7, 25)
    # Exploration atmosphere (8.2 psia, 34% O2) vs Sea Level (14.7 psia, 21% O2)
    loc_sibal = 13.0 + 0.15 * (14.7 - p_psia)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=p_psia,
            y=loc_sibal,
            mode="lines",
            name="SIBAL Limit",
            line={"color": "#d91119", "width": 2.5},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-99: Saffire-II Flammability Boundary vs Cabin Pressure",
        "Spacecraft Cabin Pressure (psia)",
        "Threshold Oxygen Concentration (% O₂)",
    )


def chart_psi_98_saffire_i() -> go.Figure:
    """PSI-98: Saffire-I - Fabric flame spread & heat release rate."""
    ts = SAFFIRE_TIMESERIES
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=ts["time_s"],
            y=ts["hrr_kw"],
            mode="lines",
            name="HRR (kW)",
            line={"color": "#d91119", "width": 2.5},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=ts["time_s"],
            y=ts["co_ppm"],
            mode="lines",
            name="CO (ppm)",
            yaxis="y2",
            line={"color": "#0cb64d", "width": 1.5, "dash": "dash"},
        )
    )
    fig.update_layout(
        yaxis2={
            "title": {"text": "CO Concentration (ppm)", "font": {"color": "#0cb64d"}},
            "overlaying": "y",
            "side": "right",
            "gridcolor": "rgba(0,0,0,0)",
            "tickfont": {"color": "#0cb64d"},
        }
    )
    return apply_hud_theme(
        fig,
        "PSI-98: Saffire-I Large-Scale Fire Dynamics",
        "Flight Experiment Time (s)",
        "Heat Release Rate HRR (kW)",
    )


def chart_psi_101_same_r() -> go.Figure:
    """PSI-101: SAME-R - Particle agglomeration count decay over time."""
    time_min = np.linspace(0, 60, 40)
    count_t = 12000.0 / (1.0 + 0.08 * time_min)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=time_min,
            y=count_t,
            mode="lines",
            name="Aerosol N(t)",
            line={"color": "#0cb64d", "width": 2},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-101: SAME-R Smoke Agglomeration Kinetics in Microgravity",
        "Aging Time (min)",
        "Total Aerosol Number Density (#/cm³)",
    )


def chart_psi_62_fgm() -> go.Figure:
    """PSI-62: FGM - Concurrent flame spread temperature profile."""
    x_pos = np.linspace(-5, 25, 60)
    # Temperature profile around flame base (x=0)
    temp_k = 300.0 + 1150.0 * np.exp(-((x_pos - 4.0) ** 2) / 18.0)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_pos,
            y=temp_k,
            mode="lines",
            name="Flamelet Model",
            line={"color": "#d91119", "width": 2.5},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-62: FGM Flamelet Surface Temperature Profile",
        "Axial Position from Flame Base (mm)",
        "Surface Temperature T (K)",
    )


def chart_psi_100_saffire_iii() -> go.Figure:
    """PSI-100: Saffire-III - Thick PMMA flame spread rate vs high airflow."""
    u_vals = np.linspace(1.0, 20.0, 25)
    v_spread = 0.045 * (u_vals**0.62)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=u_vals,
            y=v_spread,
            mode="lines+markers",
            name="Thick PMMA",
            line={"color": "#fbdc08", "width": 2},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-100: Saffire-III Thick Solid Flame Spread vs High Forced Airflow",
        "Forced Airflow Velocity (cm/s)",
        "Flame Spread Rate (mm/s)",
    )


def chart_psi_47_daft() -> go.Figure:
    """PSI-47: DAFT - Dust vs smoke aerosol light scattering ratio."""
    angle = np.linspace(15, 165, 40)
    scatter_smoke = np.cos(np.radians(angle)) ** 2 + 0.2
    scatter_dust = 3.5 * np.exp(-angle / 25.0) + 0.4

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=angle,
            y=scatter_smoke,
            mode="lines",
            name="Smoke (<1 μm)",
            line={"color": "#0cb64d", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=angle,
            y=scatter_dust,
            mode="lines",
            name="Dust (>1 μm)",
            line={"color": "#fbdc08", "width": 2},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-47: DAFT Light Scattering Phase Function",
        "Scattering Angle θ (deg)",
        "Differential Scattering Cross-Section (a.u.)",
    )


def chart_psi_159_acme_cfig() -> go.Figure:
    """PSI-159: ACME CFI-G - Gaseous cool flame burning rate vs dilution."""
    dilution = np.linspace(0.1, 0.7, 25)
    burning_rate = 14.5 * (1.0 - dilution) ** 1.3

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dilution * 100,
            y=burning_rate,
            mode="lines",
            name="DME / CO₂ Dilution",
            line={"color": "#fbdc08", "width": 2},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-159: ACME CFI-G Cool Flame Burning Rate vs Dilution",
        "CO₂ Inert Dilution Fraction (%)",
        "Laminar Burning Velocity (cm/s)",
    )


def chart_psi_60_spice_reanalysis() -> go.Figure:
    """PSI-60: SPICE Reanalysis - Soot yield fraction vs time."""
    time_pts = np.linspace(0, 10, 30)
    yield_soot = 0.082 * (1.0 - np.exp(-0.45 * time_pts))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=time_pts,
            y=yield_soot * 100,
            mode="lines",
            name="Soot Yield",
            line={"color": "#0cb64d", "width": 2},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-60: SPICE Reanalysis Soot Conversion Yield",
        "Residence Time (s)",
        "Soot Conversion Yield (% Carbon)",
    )


def chart_psi_106_slice() -> go.Figure:
    """PSI-106: SLICE - Gaseous diffusion flame liftoff velocity."""
    re_nozzle = np.linspace(400, 2400, 25)
    v_liftoff = 0.015 * re_nozzle - 2.5

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=re_nozzle,
            y=v_liftoff,
            mode="lines+markers",
            name="Methane Jet",
            line={"color": "#fbdc08", "width": 2},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-106: SLICE Flame Liftoff vs Jet Reynolds Number",
        "Nozzle Reynolds Number (Re)",
        "Liftoff Height (mm)",
    )


def chart_psi_115_same_modeling() -> go.Figure:
    """PSI-115: SAME Modeling - CFD simulation vs flight coagulation kinetics."""
    time_s = np.linspace(0, 300, 35)
    cfd_sim = 1.0 - 0.75 * (1.0 - np.exp(-time_s / 80.0))
    flight_sensor = cfd_sim + np.random.default_rng(42).normal(0, 0.02, len(time_s))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=time_s,
            y=cfd_sim,
            mode="lines",
            name="CFD Model",
            line={"color": "#0cb64d", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=time_s,
            y=flight_sensor,
            mode="markers",
            name="Flight Sensor",
            marker={"size": 5, "color": "#fbdc08"},
        )
    )
    return apply_hud_theme(
        fig,
        "PSI-115: SAME Modeling CFD vs Flight Sensor Kinetics",
        "Chamber Elapsed Time (s)",
        "Normalized Aerosol Concentration (C/C₀)",
    )


# ==============================================================================
# Action 5.3: Investigation Chart Dispatcher
# ==============================================================================

_DISPATCHER: dict[str, Any] = {
    "PSI-69": chart_psi_69_flex,
    "PSI-68": chart_psi_68_flex_2,
    "PSI-23": chart_psi_23_acme_sflame,
    "PSI-10": chart_psi_10_acme_flame_design,
    "PSI-22": chart_psi_22_acme_efield,
    "PSI-21": chart_psi_21_acme_cld_flame,
    "PSI-25": chart_psi_25_bass_ii,
    "PSI-20": chart_psi_20_acme_bre,
    "PSI-102": chart_psi_102_same,
    "PSI-142": chart_psi_142_cool_flame,
    "PSI-26": chart_psi_26_bass,
    "PSI-117": chart_psi_117_cfd,
    "PSI-107": chart_psi_107_spice,
    "PSI-39": chart_psi_39_cfi,
    "PSI-99": chart_psi_99_saffire_ii,
    "PSI-98": chart_psi_98_saffire_i,
    "PSI-101": chart_psi_101_same_r,
    "PSI-62": chart_psi_62_fgm,
    "PSI-100": chart_psi_100_saffire_iii,
    "PSI-47": chart_psi_47_daft,
    "PSI-159": chart_psi_159_acme_cfig,
    "PSI-60": chart_psi_60_spice_reanalysis,
    "PSI-106": chart_psi_106_slice,
    "PSI-115": chart_psi_115_same_modeling,
}


def get_investigation_chart(accession: str) -> go.Figure:
    """Retrieve dedicated Plotly figure for any of the 24 PSI investigations.

    Args:
        accession: PSI accession identifier (e.g. 'PSI-26', 'PSI-98').

    Returns:
        Themed Plotly go.Figure instance.
    """
    builder_fn = _DISPATCHER.get(accession.strip().upper())
    if builder_fn:
        return builder_fn()

    # Empty placeholder figure if not selected or unknown
    fig = go.Figure()
    return apply_hud_theme(
        fig,
        title="No Investigation Selected",
        x_title="Parameter",
        y_title="Measurement",
    )
