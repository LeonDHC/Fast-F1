from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting

fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme='fastf1')

session = fastf1.get_session(2025, 'China', 'Q')

session.load()
fast_leclerc = session.laps.pick_drivers('VER').pick_fastest()
lec_car_data = fast_leclerc.get_car_data()
t = lec_car_data['Time']
vCar = lec_car_data['Speed']

# The rest is just plotting
fig, ax = plt.subplots()
ax.plot(t, vCar, label='Fast')
ax.set_xlabel('Time')
ax.set_ylabel('Speed [Km/h]')
ax.set_title('Leclerc is')
ax.legend()
plt.show()

fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme='fastf1')

session = fastf1.get_session(2025, 'China', 'Q')

session.load()
fast_leclerc = session.laps.pick_drivers('VER').pick_fastest()
lec_car_data = fast_leclerc.get_car_data()
t = lec_car_data['Time']
vCar = lec_car_data['Speed']

fast_ver = session.laps.pick_drivers('LAW').pick_fastest()
ver_car_data = fast_ver.get_car_data()
v = ver_car_data['Time']
vCarVer = ver_car_data['Speed']

# The rest is just plotting
fig, ax = plt.subplots()
ax.plot(t, vCar, label='VER')
ax.plot(v, vCarVer, label='LAW')
ax.set_xlabel('Time')
ax.set_ylabel('Speed [Km/h]')
ax.set_title('vCar')
ax.legend()
plt.show()