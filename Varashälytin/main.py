# main.py — Burglary alarm (PIR)
# Wiring: PIR VCC -> 3V3, PIR OUT -> GP28, PIR GND -> GND  (ei GP20)
from machine import Pin
from time import sleep

pir = Pin(28, Pin.IN)        # PIR data pin
led = Pin('LED', Pin.OUT)    # Pico W:n sisäinen LED

print("Alarm armed.")
while True:
    if pir.value():                 # liike havaittu (OUT=1)
        led.on()
        print("⚠️  Movement detected!")
        sleep(2)                    # pidä ilmoitus näkyvissä/LED päällä hetki
    else:
        led.off()
    sleep(0.05)                     # pieni viive hälyn välttämiseksi
