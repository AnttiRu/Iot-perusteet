# main.py — Weather station (DHT22)
# Wiring (Wokwi/Pico W):
#   DHT22 VCC -> 3V3   (älä käytä 3V3_EN)
#   DHT22 GND -> GND
#   DHT22 DATA -> GP15

from machine import Pin
from time import sleep
import dht

SENSOR_PIN = 15
led = Pin("LED", Pin.OUT)          # Pico W:n sisäinen LED (status)
sensor = dht.DHT22(Pin(SENSOR_PIN))

print("Weather station ready.")
while True:
    try:
        sensor.measure()
        t = sensor.temperature()   # °C
        h = sensor.humidity()      # %
        print("T: {:.1f} °C  RH: {:.1f} %".format(t, h))
        led.toggle()               # vilkauta kun mittaus onnistui
    except OSError as e:
        print("Sensor read error:", e)
        led.off()
    sleep(2)                        # DHT22: väh. ~2 s mittausten väli
