import math
import matplotlib.pyplot as plt
import numpy as np

diameter = float(input("Enter diameter of the rocket (m): "))
nose_length = float(input("Enter nose length of the rocket (m): "))
rocket_length = float(input("Enter total length of the rocket (m): "))
fin_count = int(input("Enter number of fins: "))
fin_span = float(input("Enter fin span (m): "))
fin_root_chord = float(input("Enter fin root chord length (m): "))
fin_tip_chord = float(input("Enter fin tip chord length (m): "))
cg_location = float(input("Enter center of gravity location from nose (m): "))
cp_nose = nose_length / 2
cn_nose = 2
cp_fins = rocket_length - fin_root_chord/2
radius = diameter / 2
cn_fins = (1 + radius /(fin_span + radius)) * (4 * fin_count * (fin_span / diameter) ** 2) / (1 + math.sqrt(1 + (2 * fin_span / (fin_root_chord + fin_tip_chord)) ** 2))
cp_total = (cn_nose * cp_nose + cn_fins * cp_fins) / (cn_nose + cn_fins)
stability_margin = (cp_total - cg_location) / diameter
name = input("Enter rocket name: ")
dry_mass = float(input("Enter drymass of the rocket (kg): "))
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
area = math.pi * (diameter/2) ** 2
altitudes = []
times = []
velocities = []
machs = []
cds = []
mach_table = [0.0, 0.8, 1.0, 1.5, 2.0, 3.0]
cd_table =   [0.40, 0.45, 0.80, 0.55, 0.45, 0.40]


print("Rocket:", name)
print("Dry Mass:", dry_mass, "kg")
print("Diameter:", diameter, "m")
print("Net Force:", round(net_force, 1), "N")
print("Acceleration:", round(acceleration, 1), "m/s²")

if thrust < total_weight:
    print("Warning: Thrust is less than weight. The rocket will not lift off.")
    quit()
if stability_margin < 1:
    print("Warning: Unstable")
elif stability_margin > 2:
    print("Warning: Overstable")
else:
    print("Stability: GOOD")

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

print("Altitude at burnout:", round(altitude, 1), "m")
print("Velocity at burnout:", round(velocity, 1), "m/s")

while altitude > 0:
    if altitude > peak_altitude:
        peak_altitude = altitude
    temperature = 288.15 -0.0065 * altitude
    speed_of_sound = math.sqrt(1.4 * 287.05 * temperature)
    mach = velocity / speed_of_sound
    air_density = 1.225 * (temperature / 288.15) ** 5.2561
    cd = np.interp(mach, mach_table, cd_table)
    drag = 0.5 * cd * air_density * area * velocity ** 2
    acceleration = (-weight - drag * math.copysign(1, velocity)) / dry_mass
    velocity = velocity + acceleration * dt
    altitude = altitude + velocity * dt 
    time = time + dt
    altitudes.append(altitude)
    times.append(time)
    velocities.append(velocity) 
    machs.append(mach)
    cds.append(cd)

print("Altitude at landing:", round(altitude, 1), "m")
print("Velocity at landing:", round(velocity, 1), "m/s")
print("Peak altitude:", round(peak_altitude, 1), "m")
print("Peak Mach:", round(max(machs), 2))
print("Peak Drag Coefficient:", round(max(cds), 2))
print("Area:", round(area, 3), "m²")
print("CP Location:", round(cp_total, 3), "m from nose")
print("CG Location:", round(cg_location, 3), "m from nose")
print("Stability Margin:", round(stability_margin, 3), "calibers")

plt.figure()
plt.plot(times, altitudes)
plt.xlabel("Time (s)")
plt.ylabel("Altitude (m)")
plt.title(name + " Flight Profile")
plt.axvline(x=burn_time, color='r', linestyle='--', label='Burnout')
plt.grid(True)
plt.legend()
plt.figure()
plt.plot(times, cds)
plt.xlabel("Time (s)")
plt.ylabel("Drag Coefficient")
plt.title(name + " Drag Coefficient Profile")
plt.axvline(x=burn_time, color='r', linestyle='--', label='Burnout')
plt.grid(True)
plt.legend()
plt.figure()
plt.plot(times, velocities)
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title(name + " Velocity Profile")
plt.axvline(x=burn_time, color='r', linestyle='--', label='Burnout')
plt.grid(True)
plt.legend()
plt.figure()
plt.plot(times, machs)
plt.xlabel("Time (s)")
plt.ylabel("Mach Number")
plt.title(name + " Mach Profile")
plt.axvline(x=burn_time, color='r', linestyle='--', label='Burnout')
plt.axhline(y=1, color='g', linestyle='--', label='Mach 1')
plt.grid(True)
plt.legend()
plt.show()


