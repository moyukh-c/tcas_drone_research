# The following code is inspired from:
# https://docs.circuitpython.org/projects/gps/en/latest/

import time
from typing import Dict, Optional
import serial
import adafruit_gps

# Create serial connection for the GPS module
uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)

# Create GPS object
gps = adafruit_gps.GPS(uart, debug=False)

# Configure which NMEA sentences the GPS module outputs
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
# Set update rate to once per second
gps_data_refresh_rate_sec = 1
gps.send_command(b"PMTK220,1000")


def get_gps_location() -> Dict[str, float]:
    gps.update()
    if not gps.has_fix:  # GPS Fix indicated the connection of GPS module to the number of satellites
        print("GPS did not get fix")
        return {}

    raw_speed_kmh = gps.speed_kmh or 0.0
    speed_kmh = 0.0 if raw_speed_kmh < 2.0 else raw_speed_kmh
    speed_mps = speed_kmh / 3.6  # is meters per second

    # Debug output
    print("-" * 40)
    print(
        "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
            gps.timestamp_utc.tm_mon,
            gps.timestamp_utc.tm_mday,
            gps.timestamp_utc.tm_year,
            gps.timestamp_utc.tm_hour,
            gps.timestamp_utc.tm_min,
            gps.timestamp_utc.tm_sec,
        )
    )
    print(f"Latitude: {gps.latitude:.6f} degrees")
    print(f"Longitude: {gps.longitude:.6f} degrees")
    print(f"Fix quality: {gps.fix_quality}")

    data = {
        "Number of satellites": (gps.satellites, ""),
        "Altitude": (gps.altitude_m, "meters"),
        "Speed (knots)": (gps.speed_knots, "knots"),
        "Speed (km/h)": (speed_kmh, "km/h"),
        "Track angle": (gps.track_angle_deg, "degrees"),
        "Horizontal dilution": (gps.horizontal_dilution, ""),
        "Height geoid": (gps.height_geoid, "meters"),
    }

    for label, (value, unit) in data.items():
        if value is None:
            print(f"Not enough information from GPS, {label}: {value} {unit}")
            return {}

    altitude1 = gps.altitude_m
    # Get new altitude after 2 secs
    time.sleep(2)
    altitude2 = gps.altitude_m
    climb_rate = (altitude2 - altitude1)/2

    # Return data for collision detection
    return {
        "lat": gps.latitude,
        "lon": gps.longitude,
        "alt": gps.altitude_m,
        "speed": speed_mps,
        "track": gps.track_angle_deg,
        "climb_rate": float(climb_rate)
    }
