# main.py — Interrupt-pohjainen reaktiopeli
# LED: GP15 (vastuksen kautta -> LED -> GND)
# BTN: GP14 <-> 3V3 (PULL_DOWN, painettaessa 1)

from machine import Pin
from time import ticks_ms, ticks_diff, sleep_ms
import urandom

LED_PIN = 15
BTN_PIN = 14

led = Pin(LED_PIN, Pin.OUT)
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_DOWN)  # pressed -> 1

# Globaalit kellot ISR:lle
t_off = None   # hetki kun LED sammutettiin
t_click = None # ensimmäinen painallus-hetki

def on_press(pin: Pin):
    """IRQ: talleta ensimmäinen painallus LEDin sammumisen jälkeen."""
    global t_off, t_click
    if t_off is None or t_click is not None:
        return  # ignooraa liian aikaiset tai tuplapainallukset
    now = ticks_ms()
    # 20 ms debounce LEDin sammumisesta
    if ticks_diff(now, t_off) >= 20:
        t_click = now

# RISING, koska PULL_DOWN + 3V3 -> painallus nostaa tason 1:een
btn.irq(trigger=Pin.IRQ_RISING, handler=on_press)

def rand_ms(lo=2000, hi=5000):
    # satunnainen 2000..5000 ms
    return lo + (urandom.getrandbits(12) % (hi - lo + 1))

while True:
    # 1) LED päälle
    led.on()
    t_off = None
    t_click = None

    # 2) Odota satunnainen aika ja sammuta
    sleep_ms(rand_ms())
    led.off()
    t_off = ticks_ms()

    # 3) Odota napin keskeytystä ja laske reaktioaika
    while t_click is None:
        sleep_ms(1)
    rt = ticks_diff(t_click, t_off)
    print("Reaction time: {} ms".format(rt))

    # 4) Lyhyt tauko ennen uutta kierrosta
    sleep_ms(1500)
