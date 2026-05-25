import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
import random

def simulate(thrust, wind_speed):
    weight = dry_mass * 9.81
    dt = 0.01
    velocity = 0
    altitude = 0
    time = 0
    peak_altitude = 0
    altitudes = []
    times = []
    velocities = []
    machs = []
    cds = []
    mach_table = [0.0, 0.8, 1.0, 1.5, 2.0, 3.0]
    cd_table =   [0.40, 0.45, 0.80, 0.55, 0.45, 0.40]

    while time < burn_time:
        temperature = 288.15 -0.0065 * altitude
        speed_of_sound = math.sqrt(1.4 * 287.05 * temperature)
        mach = velocity / speed_of_sound
        air_density = 1.225 * (temperature / 288.15) ** 5.2561
        current_mass = dry_mass + propellant_mass * (1 - time / burn_time)
        current_weight = current_mass * 9.81
        cd = np.interp(mach, mach_table, cd_table)
        k1_drag = 0.5 * cd * air_density * area * velocity ** 2
        k1 = (thrust - k1_drag - current_weight) / current_mass
        k2_drag = 0.5 * cd * air_density * area * (velocity + dt/2 * k1) ** 2
        k2 = (thrust - k2_drag - current_weight) / current_mass
        k3_drag = 0.5 * cd * air_density * area * (velocity + dt/2 * k2) ** 2
        k3 = (thrust - k3_drag - current_weight) / current_mass
        k4_drag = 0.5 * cd * air_density * area * (velocity + dt * k3) ** 2
        k4 = (thrust - k4_drag - current_weight) / current_mass  
        velocity = velocity + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)
        altitude = altitude + velocity * dt
        time = time + dt
        altitudes.append(altitude)
        times.append(time)
        velocities.append(velocity)
        machs.append(mach)
        cds.append(cd)

    parachute_area = math.pi * (parachute_diameter/2) ** 2
    cd_parachute = 0.75

    while altitude > 0:
        temperature = 288.15 -0.0065 * altitude
        air_density = 1.225 * (temperature / 288.15) ** 5.2561
        speed_of_sound = math.sqrt(1.4 * 287.05 * temperature)
        mach = velocity / speed_of_sound
        if altitude > peak_altitude:
            peak_altitude = altitude
        if altitude < deployment_altitude:
            effective_cd = cd_parachute
            effective_area = parachute_area
        else:
            effective_cd = np.interp(mach, mach_table, cd_table)
            effective_area = area
        drag = 0.5 * effective_cd * air_density * effective_area * velocity ** 2
        acceleration = (-weight - drag * math.copysign(1, velocity)) / dry_mass
        velocity = velocity + acceleration * dt
        altitude = altitude + velocity * dt 
        time = time + dt
        altitudes.append(altitude)
        times.append(time)
        velocities.append(velocity) 
        machs.append(mach)
        cds.append(cd)

    return peak_altitude, velocity, altitudes, times, machs, cds, velocities

st.title("Rocket Flight Simulation")
st.sidebar.header("Rocket Parameters")
name = st.sidebar.text_input("Rocket Name", "Falcon")
thrust= st.sidebar.slider("Thrust (N)", min_value=1.0, max_value=100.0, value=29.0, step=0.5)
dry_mass = st.sidebar.slider("Dry Mass (kg)", min_value=0.05, max_value=2.0, value=0.1, step=0.05)
diameter = st.sidebar.slider("Diameter (m)", min_value=0.01, max_value=0.5, value=0.04, step=0.1)
burn_time = st.sidebar.slider("Burn Time (s)", min_value=0.1, max_value=10.0, value=1.7, step=0.1)
propellant_mass = st.sidebar.slider("Propellant Mass (kg)", min_value=0.05, max_value=5.0, value=0.027, step=0.05)
nose_length = st.sidebar.slider("Nose Length (m)", min_value=0.01, max_value=0.5, value=0.1, step=0.01)
fin_count = st.sidebar.slider("Fin Count", min_value=0, max_value=4, value=3, step=1)
fin_span = st.sidebar.slider("Fin Span (m)", min_value=0.01, max_value=0.5, value=0.1, step=0.01)
fin_root_chord = st.sidebar.slider("Fin Root Chord (m)", min_value=0.01, max_value=0.5, value=0.1, step=0.01)
fin_tip_chord = st.sidebar.slider("Fin Tip Chord (m)", min_value=0.01, max_value=0.5, value=0.05, step=0.01)
cg_location = st.sidebar.slider("Center of Gravity Location (m)", min_value=0.01, max_value=1.0, value=0.5, step=0.01)
rocket_length = st.sidebar.slider("Rocket Length (m)", min_value=0.1, max_value=2.0, value=0.5, step=0.1)
parachute_diameter = st.sidebar.slider("Parachute Diameter (m)", min_value=0.1, max_value=2.0, value=0.3, step=0.1)
deployment_altitude = st.sidebar.slider("Parachute Deployment Altitude (m)", min_value=10.0, max_value=500.0, value=150.0, step=10.0)
st.write(thrust, dry_mass, diameter)
area = math.pi * (diameter/2) ** 2
cp_nose = nose_length / 2
cn_nose = 2
cp_fins = rocket_length - fin_root_chord/2
radius = diameter / 2
cn_fins = (1 + radius /(fin_span + radius)) * (4 * fin_count * (fin_span / diameter) ** 2) / (1 + math.sqrt(1 + (2 * fin_span / (fin_root_chord + fin_tip_chord)) ** 2))
cp_total = (cn_nose * cp_nose + cn_fins * cp_fins) / (cn_nose + cn_fins)
stability_margin = (cp_total - cg_location) / diameter

if st.button("Launch"):
    peak_altitude, velocity, altitudes, times, machs, cds, velocities = simulate(thrust, 0)
    st.write("Peak Altitude:", round(peak_altitude, 1), "m")
    st.write("CP Location:", round(cp_total, 2), "m")
    st.write("CG Location:", round(cg_location, 2), "m")
    st.write("Stability Margin:", round(stability_margin, 2), "calibers")
    st.write("Landing velocity:", round(abs(velocity), 1), "m/s")
    if stability_margin < 1:
        st.write("Stability: Unstable")
    elif stability_margin > 2:
        st.write("Stability: Overstable")
    else:
        st.write("Stability: Stable")
    fig, ax = plt.subplots()
    ax.plot(times, altitudes)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Altitude (m)")
    ax.set_title(name + " Flight Profile")
    ax.grid(True)
    st.pyplot(fig)
    fig, ax = plt.subplots()
    ax.plot(times, velocities)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Velocity (m/s)")
    ax.set_title(name + " Velocity Profile")
    ax.grid(True)
    st.pyplot(fig)
    fig, ax = plt.subplots()
    ax.plot(times, machs)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Mach Number")
    ax.set_title(name + " Mach Profile")
    ax.grid(True)
    st.pyplot(fig)
    with st.spinner("Running 1000 simulations..."):
        monte_carlo_results = []
        for i in range(1000):
            varied_thrust = random.gauss(thrust, thrust * 0.05)
            result = simulate(varied_thrust, 0)
            monte_carlo_results.append(result[0])
    fig, ax = plt.subplots()
    ax.hist(monte_carlo_results, bins=30)
    ax.set_xlabel("Peak Altitude (m)")
    ax.set_ylabel("Frequency")
    ax.set_title(name + " Monte Carlo Peak Altitude Distribution")
    st.pyplot(fig)

