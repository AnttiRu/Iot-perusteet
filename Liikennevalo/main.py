# main.py
# Traffic lights + button + buzzer (matches your diagram.json)
# RED=GP15, YEL=GP14, GRN=GP13, BUZZER=GP12, BUTTON=GP16 (-> 3V3, use PULL_DOWN)

from machine import Pin
from time import ticks_ms, ticks_diff, sleep_ms

# LEDs
RED = Pin(15, Pin.OUT)
YEL = Pin(14, Pin.OUT)
GRN = Pin(13, Pin.OUT)

# Active buzzer (on/off)
BUZ = Pin(12, Pin.OUT)

# Button to 3V3 -> use PULL_DOWN (pressed == 1)
BTN = Pin(16, Pin.IN, Pin.PULL_DOWN)

# timings (ms)
GREEN_MS, YELLOW_MS, RED_MS = 3000, 800, 2000
BEEP_MS = 1500

def all_off():
    RED.off(); YEL.off(); GRN.off()

def set_state(r=False, y=False, g=False):
    RED.value(1 if r else 0)
    YEL.value(1 if y else 0)
    GRN.value(1 if g else 0)

# state
cycle = 0          # 0=green, 1=yellow, 2=red
t_last = ticks_ms()
override = False
beep_until = 0

while True:
    now = ticks_ms()

    # --- button override ---
    if BTN.value():                    # pressed
        if not override:
            override = True
            set_state(r=True, y=False, g=False)
            BUZ.on()
            beep_until = now + BEEP_MS
    else:
        if override:
            override = False
            BUZ.off()
            t_last = now  # resume cycle cleanly

    if override:
        if ticks_diff(now, beep_until) >= 0:
            BUZ.off()
        sleep_ms(5)
        continue

    # --- normal cycle ---
    if cycle == 0:                     # green
        set_state(g=True)
        if ticks_diff(now, t_last) >= GREEN_MS:
            cycle, t_last = 1, now
    elif cycle == 1:                   # yellow
        set_state(y=True)
        if ticks_diff(now, t_last) >= YELLOW_MS:
            cycle, t_last = 2, now
    else:                              # red
        set_state(r=True)
        if ticks_diff(now, t_last) >= RED_MS:
            cycle, t_last = 0, now

    sleep_ms(5)
