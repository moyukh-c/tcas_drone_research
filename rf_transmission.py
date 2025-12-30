# The following code is inspired from:
# https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/uart-serial
# https://stackoverflow.com/questions/55600132/installing-local-packages-with-python-virtualenv-system-site-packages

from typing import Dict

# Import Blinka Libraries
import board
import busio
import digitalio
# Import the RFM69 radio module.
import adafruit_rfm69


# Configure Packet Radio
CS = digitalio.DigitalInOut(board.D5)
RESET = digitalio.DigitalInOut(board.D6)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)

# Define the onboard LED
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT


# Optionally set an encryption key (16 byte AES key).
rfm69.encryption_key = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"

# Print out some chip state:
print(f"Temperature: {rfm69.temperature}C")
print(f"Frequency: {rfm69.frequency_mhz}mhz")
print(f"Bit rate: {rfm69.bitrate / 1000}kbit/s")
print(f"Frequency deviation: {rfm69.frequency_deviation}hz")


def broadcast_self_location(gps_data: Dict[str, float]):
    gps_data_str = ','.join(str(value) for key, value in gps_data.items())
    rfm69.send(bytes(gps_data_str, "utf-8"))
    print(f"Sent data {gps_data_str}")


def receive_other_drone_location() -> Dict[str, float]:
    packet = rfm69.receive()
    if packet is None:
        # Packet has not been received
        LED.value = False
        print("Received nothing! Listening again...")
        return {}
    else:
        # Received a packet!
        LED.value = True
        # Decode to ASCII text and print it.
        packet_text = str(packet, "utf-8")
        packet_text_split = packet_text.split(",")

        if len(packet_text_split) != 6:
            print("Did not receive enough information")
            return {}

        else:
            return {
                'lat': float(packet_text_split[0]),
                'lon': float(packet_text_split[1]),
                'alt': float(packet_text_split[2]),
                'speed': float(packet_text_split[3]),
                'track': float(packet_text_split[4]),
                'climb_rate': float(packet_text_split[5])
            }
