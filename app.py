import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

st.set_page_config(page_title="Wind Turbine Simulator", layout="centered")

st.title("🌬️ Wind Turbine Simulator")
st.write("Realistic simulation based on standard wind turbine values.")

# -----------------------------
# INPUT: WIND SPEED
# -----------------------------
wind_speed = st.slider("Wind Speed (km/h)", 0, 200, 10, step=5)

# Convert to m/s
v = wind_speed / 3.6

# -----------------------------
# DETERMINE ROTATION STAGE
# -----------------------------
if wind_speed == 0:
    stage = "STOPPED"
    rpm = 0
elif 0 < wind_speed <= 30:
    stage = "VERY SLOW"
    rpm = 5
elif 30 < wind_speed <= 50:
    stage = "SLOW"
    rpm = 10
elif 50 < wind_speed <= 100:
    stage = "MEDIUM"
    rpm = 20
elif 100 < wind_speed <= 150:
    stage = "FAST"
    rpm = 35
else:
    stage = "CUT-OFF (Safety Shutdown)"
    rpm = 0

# -----------------------------
# TURBINE ANIMATION (NO IMAGES)
# -----------------------------
# -----------------------------
# TURBINE ANIMATION (NO IMAGES)
# -----------------------------
# -----------------------------
# TURBINE ANIMATION (SVG, smooth, non-blocking)
# -----------------------------
st.subheader("Turbine Animation (SVG)")

# If turbine is stopped, don't animate
if stage == "CUT-OFF (Safety Shutdown)" or rpm == 0:
    st.markdown("<h3 style='text-align:center;'>🛑 Turbine Stopped (Safety Shutdown)</h3>", unsafe_allow_html=True)
else:
    # convert RPM to seconds per full rotation (period)
    # rpm = rotations per minute -> period_sec = 60 / rpm
    period_sec = max(0.15, 60.0 / float(rpm))  # clamp to avoid too-fast animation

    # SVG with CSS animation-duration set by period_sec
    svg = f"""
    <div style="display:flex;justify-content:center;align-items:center;">
    <style>
      .rot{{ transform-origin: 100px 100px; animation: spin {period_sec}s linear infinite; }}
      @keyframes spin {{
        from {{ transform: rotate(0deg); }}
        to   {{ transform: rotate(360deg); }}
      }}
      .turbine-container {{ width: 320px; height: 320px; }}
      .hub {{ fill: #666; }}
      .blade {{ fill: #444; rx: 2; ry: 2; }}
      .tower {{ fill: #888; }}
    </style>

    <svg class="turbine-container" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Rotating wind turbine">
      <!-- hub -->
      <circle cx="100" cy="100" r="6" class="hub"/>
      <!-- rotating blades group -->
      <g class="rot">
        <rect x="98" y="20" width="4" height="70" class="blade" />
        <rect x="98" y="20" width="4" height="70" class="blade" transform="rotate(120 100 100)"/>
        <rect x="98" y="20" width="4" height="70" class="blade" transform="rotate(240 100 100)"/>
      </g>
      <!-- tower -->
      <rect x="95" y="100" width="10" height="80" class="tower"/>
    </svg>
    </div>

    <div style="text-align:center;margin-top:6px;">
      <strong>Stage:</strong> {stage} &nbsp; • &nbsp; <strong>RPM:</strong> {rpm}
    </div>
    """

    st.markdown(svg, unsafe_allow_html=True)


# -----------------------------
# INSTANTANEOUS POWER (kW)
# Formula: P = 0.5 * ρ * A * Cp * v³
# -----------------------------
rho = 1.225           # air density
r = 40                # blade radius (m)
A = np.pi * r * r     # swept area
Cp = 0.45             # typical efficiency

if stage == "CUT-OFF (Safety Shutdown)":
    power_kw = 0
else:
    power = 0.5 * rho * A * Cp * (v ** 3)    # watts
    power_kw = round(power / 1000, 2)

st.subheader("Instantaneous Energy Output")
st.write(f"**Power Generated:** {power_kw} kW")

# -----------------------------
# POWER CURVE GRAPH (EXTENDED RANGE)
# -----------------------------
st.subheader("Wind Turbine Power Curve")

wind_speeds = np.linspace(0, 40, 100)
power_output = []

# -----------------------------
# REAL POWER CURVE USING ALL SPEEDS UP TO CURRENT VALUE
# -----------------------------
st.subheader("Wind Turbine Power Curve (Dynamic)")

rho = 1.225
r = 40
A = np.pi * r * r
Cp = 0.45
rated_power_kw = 3000  # 3 MW
cut_in = 3
rated_speed = 15
cut_out = 25

# create speeds from 0 → current wind speed (v)
wind_speeds = np.linspace(0, v, 200)
power_output = []

for vs in wind_speeds:
    if vs < cut_in:
        P = 0
    elif cut_in <= vs < rated_speed:
        P = 0.5 * rho * A * Cp * (vs ** 3)
        P = min(P / 1000, rated_power_kw)
    elif rated_speed <= vs < cut_out:
        P = rated_power_kw
    else:
        P = 0
    power_output.append(P)

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(wind_speeds, power_output, linewidth=2)
ax.set_xlabel("Wind Speed (m/s)", fontsize=12)
ax.set_ylabel("Power Output (kW)", fontsize=12)
ax.set_title("Wind Turbine Power Curve (Up to Current Wind Speed)", fontsize=14)
ax.grid(True)

st.pyplot(fig)
