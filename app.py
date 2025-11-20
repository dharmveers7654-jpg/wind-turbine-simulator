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
elif 0 < wind_speed <= 20:
    stage = "VERY SLOW"
    rpm = 5
elif 20 < wind_speed <= 40:
    stage = "SLOW"
    rpm = 10
elif 40 < wind_speed <= 80:
    stage = "MEDIUM"
    rpm = 20
elif 80 < wind_speed <= 150:
    stage = "FAST"
    rpm = 35
else:
    stage = "CUT-OFF (Safety Shutdown)"
    rpm = 0

# -----------------------------
# TURBINE ANIMATION (NO IMAGES)
# -----------------------------
frames = ["🌪️", "🌀", "💨", "🔄"]  # animation frames

st.subheader("Turbine Animation")
placeholder = st.empty()

if stage == "CUT-OFF (Safety Shutdown)" or rpm == 0:
    placeholder.write("🛑 Turbine Stopped (Safety Shutdown)")
else:
    # Faster wind = faster animation
    speed = max(0.05, 0.5 - (rpm / 100))

    for i in range(15):
        placeholder.write(
            f"### {frames[i % 4]}\n**Stage:** {stage} — **RPM:** {rpm}"
        )
        time.sleep(speed)

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

for vs in wind_speeds:
    if vs < 3:
        power_output.append(0)
    elif 3 <= vs <= 15:
        power_output.append((vs - 3) ** 2)
    elif 15 < vs <= 25:
        power_output.append(150)
    else:
        power_output.append(0)

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(wind_speeds, power_output, linewidth=2)
ax.set_xlabel("Wind Speed (m/s)", fontsize=12)
ax.set_ylabel("Power Output (kW)", fontsize=12)
ax.set_title("Wind Turbine Power Curve", fontsize=14)
ax.grid(True)

st.pyplot(fig)
