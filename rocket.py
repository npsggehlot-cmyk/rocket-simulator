import math
import matplotlib.pyplot as plt

name = input("Enter rocket name: ")
mass = float(input("Enter mass of the rocket (kg): "))
diameter = float(input("Enter diameter of the rocket (m): "))
thrust = float(input("Enter thrust of the rocket (N): "))
burn_time = float(input("Enter burn time of the rocket (s): "))
weight = mass * 9.81
net_force = thrust - weight
acceleration = net_force / mass
dt = 0.01
velocity = 0
altitude = 0
time = 0
peak_altitude = 0
cd = 0.5
air_density = 1.225
area = math.pi * (diameter/2) ** 2
altitudes = []
times = []


print("Rocket:", name)
print("Mass:", mass, "kg")
print("Diameter:", diameter, "m")
print("Net Force:", round(net_force, 1), "N")
print("Acceleration:", round(acceleration, 1), "m/s²")

if thrust < weight:
    print("Warning: Thrust is less than weight. The rocket will not lift off.")
    quit()

while time < burn_time:
    drag = 0.5 * cd * air_density * area * velocity ** 2
    acceleration = (thrust - drag - weight) / mass
    velocity = velocity + acceleration * dt
    altitude = altitude + velocity * dt
    time = time + dt
    altitudes.append(altitude)
    times.append(time)

print("Altitude at burnout:", round(altitude, 1), "m")
print("Velocity at burnout:", round(velocity, 1), "m/s")

while altitude > 0:
    if altitude > peak_altitude:
        peak_altitude = altitude
    drag = 0.5 * cd * air_density * area * velocity ** 2
    acceleration = (-weight - drag * math.copysign(1, velocity)) / mass
    velocity = velocity + acceleration * dt
    altitude = altitude + velocity * dt 
    time = time + dt
    altitudes.append(altitude)
    times.append(time)

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



