import network
from traffic import *
import time
from lights import *

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('HaSi-Kein-Internet-Legacy', 'bugsbunny')
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())

tr = Traffic()
light = Lights()

print('testing...')
light.set_all_color((0, 0, 0, 0))
time.sleep(0.5)
light.set_low_load()
time.sleep(0.2)
light.set_middle_load()
time.sleep(0.2)
light.set_high_load()
time.sleep(0.2)
light.set_all_color((255, 255, 255, 31))
time.sleep(0.2)
light.set_all_color((0, 0, 0, 0))
time.sleep(0.2)
light.set_all_color((255, 255, 255, 31))
time.sleep(0.2)
light.set_all_color((0, 0, 0, 0))
light.set_low_load()
print('testing complete')

while True:
    time.sleep(5)

    traffic = tr.get_traffic()

    if traffic != 0 and traffic != None:
        if traffic < 5:
            light.set_low_load()
        elif traffic < 10:
            light.set_middle_load()
        else:
            light.set_high_load()
