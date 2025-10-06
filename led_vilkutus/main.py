# main.py
# Tehtävä 1 – MicroPython LED vilkutus
# Author: Student
# Date: 2025-10-06

from machine import Pin
from time import sleep

led = Pin(15, Pin.OUT)  # GPIO15

while True:
    led.value(1)
    sleep(1)
    led.value(0)
    sleep(1)
