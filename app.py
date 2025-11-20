


           import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Wind Turbine Simulator", layout="centered")

st.title("🌬️ Wind Turbine Simulator")
st.write("Realistic simulation based on standard wind turbine values.")

# --- Define Physics and Speed Constants ---
rho = 1.225            # air density (kg/m³)
r = 30                 # blade radius (m)
A = np.pi * r * r      # swept area (m²)
Cp = 0.45              # typical efficiency

# Define limits in KM/H (for the user/slider input and RPM logic)
CUT_IN_KMH = 15        # Minimum wind speed for rotation (15 km/h)
CUT_OFF_KMH = 90       # Maximum wind speed for operation (90 km/h)

# Convert limits to M/S (REQUIRED for the power formula: P = 0.5 * rho * A * Cp * v³)
CUT_IN_MS = CUT_IN_KMH / 3.6    # ~4.17 m/s
CUT_OFF_MS = CUT_OFF_KMH / 3.6  # ~25.0 m/s
# ------------------------------------------

# -----------------------------
# INPUT & CONVERSION
# -----------------------------
wind_speed_kmh = st.slider("Wind Speed (km/h)", 0, 100, 15, step=5)

# Convert to m/s (REQUIRED for the power formula)
v_ms = wind_speed_kmh / 3.6

# -----------------------------
# DETERMINE ROTATION STAGE
# -----------------------------
if wind_speed_kmh < CUT_IN_KMH: # If less than 15 km/h
    stage = "LOW WIND (No Rotation)"
    rpm = 0
elif wind_speed_kmh >= CUT_OFF_KMH: # If 90 km/h or more
    stage = "CUT-OFF (Safety Shutdown)"
    rpm = 0
elif CUT_IN_KMH <= wind_speed_kmh <= 20:
    stage = "VERY SLOW"
    rpm = 5
elif 20 < wind_speed_kmh <= 30:
    stage = "SLOW"
    rpm = 10
elif 30 < wind_speed_kmh <= 45:
    stage = "MEDIUM"
    rpm = 20
elif 45 < wind_speed_kmh <= 60:
    stage = "FAST"
    rpm = 25
elif 60 < wind_speed_kmh < CUT_OFF_KMH: # Up to 90 km/h
    stage = "VERYFAST"
    rpm = 35

# -----------------------------
# TURBINE ANIMATION (SVG, smooth, non-blocking)
# -----------------------------
st.subheader("Turbine Animation (SVG)")

# If turbine is stopped, don't animate
if rpm == 0:
    st.markdown("<h3 style='text-align:center;'>🛑 Turbine Stopped</h3>", unsafe_allow_html=True)
else:
    # convert RPM to seconds per full rotation (period)
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
      <circle cx="100" cy="100" r="6" class="hub"/>
      <g class="rot">
        <rect x="98" y="20" width="4" height="70" class="blade" />
        <rect x="98" y="20" width="4" height="70" class="blade" transform="rotate(120 100 100)"/>
        <rect x="98" y="20" width="4" height="70" class="blade" transform="rotate(240 100 100)"/>
      </g>
      <rect x="95" y="100" width="10" height="80" class="tower"/>
    </svg>
    </div>

    <div style="text-align:center;margin-top:6px;">
      <strong>Stage:</strong> {stage} &nbsp; • &nbsp; <strong>RPM:</strong> {rpm}
    </div>
    """

    st.markdown(svg, unsafe_allow_html=True)

# -----------------------------
# INSTANTANEOUS POWER (kW) - CORRECTED
# -----------------------------
power_kw = 0 # Initialize power to zero

# Logic uses the M/S variables for the check against the M/S wind speed (v_ms)
if v_ms < CUT_IN_MS:
    power_kw = 0
elif v_ms >= CUT_OFF_MS:
    power_kw = 0
else:
    # Calculation performed using v_ms (correct units for the power formula)
    power = 0.5 * rho * A * Cp * (v_ms ** 3)    # watts
    power_kw = round(power / 1000, 2)

st.subheader("Instantaneous Energy Output")
st.write(f"**Power Generated:** **{power_kw} kW**")

# -----------------------------
# REAL POWER CURVE GRAPH - CORRECTED
# -----------------------------
st.subheader("Wind Turbine Power Curve")

# Generate wind speeds in m/s for the graph x-axis
wind_speeds_ms = np.linspace(0, 30, 300) # Range up to 30 m/s (~108 km/h)
power_output = []

for v_plot in wind_speeds_ms:
    # Implemented Cut-In/Cut-Off logic inside the loop
    if v_plot < CUT_IN_MS or v_plot >= CUT_OFF_MS:
        P_kw = 0 # Power is zero outside the operating range
    else:
        # Calculate power
        P = 0.5 * rho * A * Cp * (v_plot ** 3) # watts
        P_kw = P / 1000                        # convert to kW
    
    power_output.append(P_kw)
    
# Plot graph
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(wind_speeds_ms, power_output, linewidth=2, label='Theoretical Power Curve')

# Plot the current operating point
current_power_kw = power_kw
ax.plot(v_ms, current_power_kw, 'o', color='red', label='Current Speed')
ax.vlines(v_ms, 0, current_power_kw, colors='r', linestyles='--', linewidth=1)
ax.legend()


ax.set_xlabel("Wind Speed (m/s)", fontsize=12)
ax.set_ylabel("Power Output (kW)", fontsize=12)
ax.set_title("Wind Turbine Power Curve (R = 30m, $\text{C}_p = 0.45$)", fontsize=14)

ax.set_ylim(0, max(power_output) * 1.1)
ax.grid(True)

st.pyplot(fig)  
