import time

from dronekit import connect, VehicleMode

from src.modules.autopilot import navigator
from src.modules.autopilot import lander

# TODO: Add connection string
CONN_STR = ""
MESSENGER_PORT = 14560

drone = connect(CONN_STR, wait_ready=True)

nav = navigator.Navigator(drone, MESSENGER_PORT)
lander = lander.Lander()

while not (drone.armed and drone.mode == VehicleMode("GUIDED")):
    pass

nav.takeoff(20)
drone.groundspeed = 5  # m/s

# Fly a square with 50 m side lengths
nav.set_position_relative(0, -50)
nav.set_position_relative(50, 0)
nav.set_position_relative(0, 50)
nav.set_position_relative(-50, 0)

# Diagonal flight
nav.set_position_relative(25, -25)
nav.set_position_relative(25, 25)
nav.set_position_relative(-50, 0)

time.sleep(5)

# Test altitude adjustments
nav.set_altitude_relative(10)
nav.set_altitude_relative(-10)
nav.set_altitude(30)
nav.set_altitude(20)

time.sleep(5)

# Test heading adjustments
nav.set_heading_relative(90)
nav.set_heading_relative(-90)
nav.set_heading(0)
nav.set_heading(180)

time.sleep(5)

# Test landing pad search sequence
lander.generateRoute()
lander.goNext(nav, lander.route, drone.location.global_relative_frame.alt)

time.sleep(5)

# RTL
nav.return_to_launch()

drone.close()
