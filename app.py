import streamlit as st
import math
import time
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Wind Turbine Simulator", layout="wide")

st.title("🌬️ Wind Turbine Simulation (SVG Rotating Blades)")

# --- Constants ---
RADIUS = 40                  # meters, turbine rotor radius (used for power)
AIR_DENSITY = 1.225          # kg/m^3
CP = 0.45                    # power coefficient (efficiency)
CUT_OFF_KMH = 150            # stop above this

# --- Inputs ---
wind_kmh = st.slider("Wind Speed (km/h) — use multiples of 5", 0, 200, 20, step=5)
duration = st.number_input("Simulation duration (seconds for graph)", min_value=5, max_value=120, value=15, step=5)

# --- Convert & compute power ---
wind_mps = wind_kmh / 3.6
area = math.pi * (RADIUS**2)
if wind_kmh >= CUT_OFF_KMH or wind_kmh < 10:
    power_kw = 0.0
else:
    power_w = 0.5 * AIR_DENSITY * area * (wind_mps**3) * CP
    power_kw = power_w / 1000.0

# --- Determine stage & animation speed (seconds per full rotation) ---
if wind_kmh >= CUT_OFF_KMH:
    stage_name = "Cut-off (Stopped)"
    rot_period = None
elif wind_kmh == 0:
    stage_name = "Stopped"
    rot_period = None
elif wind_kmh <= 10:
    stage_name = "Very Slow"
    rot_period = 6.0
elif wind_kmh <= 30:
    stage_name = "Slow"
    rot_period = 3.5
elif wind_kmh <= 60:
    stage_name = "Medium"
    rot_period = 1.5
else:
    stage_name = "Fast"
    rot_period = 0.8

# --- Display status ---
st.subheader(f"Turbine Stage: {stage_name}")
st.metric("Instant Power", f"{power_kw:.2f} kW")

# --- SVG turbine with CSS rotation: rotation speed controlled by CSS animation-duration ---
if rot_period is None:
    # show a stopped SVG (no animation)
    svg = f"""
    <svg width="320" height="320" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
      <circle cx="100" cy="100" r="6" fill="#666"/>
      <g transform="rotate(0 100 100)">
        <rect x="98" y="20" width="4" height="70" rx="2" ry="2" fill="#444"/>
        <rect x="98" y="20" width="4" height="70" rx="2" ry="2" fill="#444" transform="rotate(120 100 100)"/>
        <rect x="98" y="20" width="4" height="70" rx="2" ry="2" fill="#444" transform="rotate(240 100 100)"/>
      </g>
      <rect x="95" y="100" width="10" height="70" fill="#888"/>
    </svg>
    """
else:
    # animated SVG: animation-duration equals rot_period seconds per full rotation
    svg = f"""
    <style>
    .rot{{ transform-origin: 100px 100px; animation: spin {rot_period}s linear infinite; }}
    @keyframes spin {{
      from {{ transform: rotate(0deg); }}
      to   {{ transform: rotate(360deg); }}
    }}
    </style>
    <svg width="320" height="320" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
      <circle cx="100" cy="100" r="6" fill="#666"/>
      <g class="rot">
        <rect x="98" y="20" width="4" height="70" rx="2" ry="2" fill="#444"/>
        <rect x="98" y="20" width="4" height="70" rx="2" ry="2" fill="#444" transform="rotate(120 100 100)"/>
        <rect x="98" y="20" width="4" height="70" rx="2" ry="2" fill="#444" transform="rotate(240 100 100)"/>
      </g>
      <rect x="95" y="100" width="10" height="70" fill="#888"/>
    </svg>
    """

st.markdown(svg, unsafe_allow_html=True)

# --- Simulate instantaneous energy (kWh) over time and plot ---
st.subheader("Instantaneous Energy (kWh) vs Time")

times = np.arange(1, duration + 1)
# energy produced each second (kWh) = power_kw * (1/3600)
energy_each_sec = np.full_like(times, power_kw / 3600.0, dtype=float)
energy_cumulative = np.cumsum(energy_each_sec)

fig, ax = plt.subplots()
ax.plot(times, energy_cumulative, marker='o')
ax.set_xlabel("Time (s)")
ax.set_ylabel("Energy (kWh)")
ax.set_title("Cumulative Energy Generated")
ax.grid(True)
st.pyplot(fig)

