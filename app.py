import streamlit as st
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="Wind Turbine Simulator", page_icon="💨")

st.title("🌬️ Wind Turbine Simulation")

# --- Input wind speed ---
wind_speed = st.slider("Wind Speed (km/h)", 0, 200, 20, step=5)

# --- Determine rotation stage ---
if wind_speed > 150:
    stage = 0  # STOP
elif wind_speed <= 20:
    stage = 1
elif wind_speed <= 40:
    stage = 2
elif wind_speed <= 70:
    stage = 3
else:
    stage = 4

st.subheader("Turbine Rotation Stage:")
stage_names = ["STOP", "Very Slow", "Slow", "Medium", "Fast"]
st.write(stage_names[stage])

# --- Load turbine images based on stage ---
image_paths = {
    0: "images/blade_1.png",
    1: "images/blade_2.png",
    2: "images/blade_3.png",
    3: "images/blade_4.png",
    4: "images/blade_5.png"
}

st.image(image_paths[stage], width=350)

# --- Instant Power Calculation (Simple Real Formula) ---
air_density = 1.225
area = 80        # m2 — small real turbine
cp = 0.45        # efficiency value

wind_speed_m_s = wind_speed / 3.6
power_watts = 0.5 * air_density * area * cp * (wind_speed_m_s ** 3)

if stage == 0:
    power_watts = 0

power_kW = power_watts / 1000
st.subheader("Instantaneous Power Output:")
st.write(f"⚡ {power_kW:.2f} kW")

# --- REAL-TIME ENERGY GRAPH ---
st.subheader("Energy Generation Over Time")

duration = st.slider("Simulation Duration (seconds)", 1, 30, 10)
energy_values = []
time_axis = []

placeholder = st.empty()

for t in range(duration):
    energy_values.append(power_kW)
    time_axis.append(t)

    fig, ax = plt.subplots()
    ax.plot(time_axis, energy_values)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Energy (kW)")
    ax.set_title("Instant Energy vs Time")
    placeholder.pyplot(fig)

    time.sleep(0.4)

