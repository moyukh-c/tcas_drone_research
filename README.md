# Drone-to-Drone Collision Avoidance System

## Overview

The objective of this project is to find a low-cost, collision avoidance system for drones which is easy to build with off-the-shelf components such as Raspberry Pi, GPS modules, and RF transceivers.
---

## Project Structure

```
project
│
├── gps_controller.py        # Operare GPS module to get precise location
├── rf_transmission.py       # Handles RF communication
└── tcas_drone_app.py        # Main program with collision detection algorithm
```

### gps_controller.py

* Connects to GPS module over UART
* Reads latitude, longitude, altitude, speed, track angle
* Calculates climb rate
* Returns dictionary with drone location

### rf_transmission.py

* Initializes RFM69 module
* Sends local GPS data
* Receives packets from other drones
* Parses received data into dictionary

### tcas_drone_app.py

* Calculates haversine distance for 2D positions
* Predicts future coordinates based on speed and bearing
* Adds altitude and climb rate to compute 3D distance
* Checks for potential collisions in a future time window

---

## Hardware Requirements

* Raspberry Pi zero 2w
* Adafruit Ultimate GPS Breakout
* RAdafruit RFM69HCW Transceiver Radio Breakout (915 MHz Recommended)

---

## Create Virtual Environment

### Create Venv - All packages are transferred from home to the venv

```bash
python3 -m venv --system-site-packages venv.<name>
pip3 install -r requirements.txt
```

---

## Enable UART on Raspberry Pi

```bash
sudo raspi-config
```

* Interface Options → Serial
* Disable login shell
* Enable serial port hardware
* Reboot the system

---

## Running the Program

```bash
python3 collision_detection.py
```

The program will:

1. Read the drone’s GPS position
2. Broadcast it via RFM69
3. Listen for other drones’ data
4. Predict future positions
5. Print collision warnings if a potential collision is detected