import math
import matplotlib.pyplot as plt

name = input("Enter rocket name: ")
dry_mass = float(input("Enter drymass of the rocket (kg): "))
diameter = float(input("Enter diameter of the rocket (m): "))
thrust = float(input("Enter thrust of the rocket (N): "))
burn_time = float(input("Enter burn time of the rocket (s): "))
propellant_mass = float(input("Enter propellant mass of the rocket (kg): "))
weight = dry_mass * 9.81
total_mass = dry_mass + propellant_mass
total_weight = (dry_mass + propellant_mass) * 9.81
net_force = thrust - total_weight
acceleration = net_force / total_mass
dt = 0.01
velocity = 0
altitude = 0
time = 0
peak_altitude = 0
cd = 0.5
area = math.pi * (diameter/2) ** 2
altitudes = []
times = []
velocities = []

print("Rocket:", name)
print("Dry Mass:", dry_mass, "kg")
print("Diameter:", diameter, "m")
print("Net Force:", round(net_force, 1), "N")
print("Acceleration:", round(acceleration, 1), "m/s²")

if thrust < total_weight:
    print("Warning: Thrust is less than weight. The rocket will not lift off.")
    quit()

while time < burn_time:
    temperature = 288.15 -0.0065 * altitude
    air_density = 1.225 * (temperature / 288.15) ** 5.2561
    current_mass = dry_mass + propellant_mass * (1 - time / burn_time)
    current_weight = current_mass * 9.81
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

print("Altitude at burnout:", round(altitude, 1), "m")
print("Velocity at burnout:", round(velocity, 1), "m/s")

while altitude > 0:
    if altitude > peak_altitude:
        peak_altitude = altitude
    temperature = 288.15 -0.0065 * altitude
    air_density = 1.225 * (temperature / 288.15) ** 5.2561
    drag = 0.5 * cd * air_density * area * velocity ** 2
    acceleration = (-weight - drag * math.copysign(1, velocity)) / dry_mass
    velocity = velocity + acceleration * dt
    altitude = altitude + velocity * dt 
    time = time + dt
    altitudes.append(altitude)
    times.append(time)
    velocities.append(velocity) 

print("Altitude at landing:", round(altitude, 1), "m")
print("Velocity at landing:", round(velocity, 1), "m/s")
print("Peak altitude:", round(peak_altitude, 1), "m")
print("Area:", round(area, 3), "m²")

plt.plot(times, altitudes)
plt.xlabel("Time (s)")
plt.ylabel("Altitude (m)")
plt.title(name + " Flight Profile")
plt.axvline(x=burn_time, color='r', linestyle='--', label='Burnout')
plt.grid(True)
plt.legend()
plt.show()


