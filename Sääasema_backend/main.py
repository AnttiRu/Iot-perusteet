# main.py — Sää asema simulaatio
# DHT22: VCC->3V3, GND->GND, DATA->GP15

from machine import Pin
from time import sleep, time
import dht

# --- secrets handling ---
try:
    import secrets
except ImportError:
    # fallback jos secrets.py puuttuu; simulaatio-tila
    class secrets:
        WIFI_SSID = ""
        WIFI_PASSWORD = ""
        TS_WRITE_KEY = ""
        DRY_RUN = True

DRY_RUN = getattr(secrets, "DRY_RUN", not bool(getattr(secrets, "TS_WRITE_KEY", "")))

sensor = dht.DHT22(Pin(15))
led = Pin("LED", Pin.OUT)

def measure():
    sensor.measure()
    t = sensor.temperature()
    h = sensor.humidity()
    return t, h

def send_simulated(t, h):
    # ÄLÄ LÄHETÄ — vain näytä mitä lähetettäisiin
    url = "https://api.thingspeak.com/update?api_key={}&field1={:.2f}&field2={:.2f}".format(
        getattr(secrets, "TS_WRITE_KEY", "YOUR_KEY"), t, h
    )
    print("[DRY RUN] Would GET:", url)

def send_thingspeak(t, h):
    import network, socket
    host = "api.thingspeak.com"
    path = "/update?api_key={}&field1={:.2f}&field2={:.2f}".format(secrets.TS_WRITE_KEY, t, h)

    # Wi-Fi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting Wi-Fi…")
        wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        for _ in range(150):  # ~15 s
            if wlan.isconnected():
                break
            sleep(0.1)
        if not wlan.isconnected():
            raise RuntimeError("Wi-Fi connect timeout")

    # HTTP GET ilman urequests-kirjastoa
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    req = "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(path, host)
    s.send(req)
    # Lue ja hylkää vastaus (siivotaan soketti)
    while s.recv(1024):
        pass
    s.close()

MIN_INTERVAL = 20  # s (ThingSpeak raja 15 s -> jätetään varaa)
last = 0

print("Weather station {} mode".format("DRY" if DRY_RUN else "REAL"))
while True:
    if time() - last < (5 if DRY_RUN else MIN_INTERVAL):
        sleep(0.2)
        continue
    try:
        t, h = measure()
        print("T={:.1f} °C  RH={:.1f} %".format(t, h))
        if DRY_RUN:
            send_simulated(t, h)
        else:
            send_thingspeak(t, h)
        led.on(); sleep(0.2); led.off()
        last = time()
    except Exception as e:
        print("Error:", e)
        led.off()
        sleep(2)
