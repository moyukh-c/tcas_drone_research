## Enhancing Airspace Safety Through a Cost-Effective Collision Avoidance Solution For Drones

### Overview

This repository contains the code of the collision detector for drones described in the paper
["Enhancing Airspace Safety Through a Cost-Effective Collision Avoidance Solution"](https://nhsjs.com/2025/enhancing-airspace-safety-through-a-cost-effective-collision-avoidance-solution/). The objective of this project is to find a low-cost, collision avoidance system for drones which is easy to build with off-the-shelf components such as Raspberry Pi, GPS modules, and RF transceivers.

---

### Project Structure

```
project
│
├── gps_controller.py        # Operates GPS module to get precise location
├── rf_transmission.py       # Handles RF communication
└── tcas_drone_app.py        # Main program with collision detection logic
```

The program will:
1. Get the drone’s GPS location
2. Broadcast it via RFM69HCW
3. Listen for other drones’ location data
4. Print collision warnings if a potential collision is detected
---
### Hardware Requirements

* Raspberry Pi Zero 2w / Pico
* Adafruit Ultimate GPS Breakout
* Adafruit RFM69HCW Transceiver Radio Breakout (915 MHz Recommended)

---

### Create Virtual Environment on Raspberry Pi

```bash
python3 -m venv --system-site-packages venv.<name>
pip3 install -r requirements.txt
```

---

### Enable UART on Raspberry Pi

```bash
sudo raspi-config
```

* Interface Options → Serial
* Enable serial port hardware
* Reboot the system

---

### Running the Program

```bash
python3 tcas_drone_app.py
```
