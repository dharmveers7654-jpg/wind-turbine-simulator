import streamlit as st
import numpy as np
import math
import time

st.title("Wind Turbine Simulation (Real Formula Based)")

st.write("""
This simulator calculates real wind turbine power using:
**P = 0.5 × ρ × A × V³ × Cp**

Where:
- ρ = air density (1.225 kg/m³ standard)
- A = swept area = π × R²
- V = wind speed (m/s)
- Cp = coefficient of performance (0.45 for modern turbines)
""")

# ------------------- USER INPUTS --------------------
wind_kmh = st.slider("Wind Speed (km/h)", 5, 60, 20, step=5)
wind = wind_kmh / 3.6                 # convert to m/s
radius = 40                           # real turbine blade length
rho = 1.225                           # standard air density
Cp = 0.45                             # real efficiency
Area = math.pi * radius**2

# ------------------- POWER CALCULATION --------------------
Power = 0.5 * rho * Area * wind**3 * Cp

st.subheader("Calculated Power Output")
st.success(f"**{Power/1000:.2f} kW**")

# ------------------- ROTATING BLADE ANIMATION --------------------
st.subheader("Wind Turbine Rotor Animation")

placeholder = st.empty()

for angle in range(0, 360, 10):
    fig = st.pyplot()
    placeholder.write(f"Rotor Angle: {angle}°")
    time.sleep(0.1)

