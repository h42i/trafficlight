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

while True:
    traffic = tr.get_traffic()

    if traffic != 0 and traffic != None:
        print(str(traffic) + " MB/s")
        if traffic < 5:
            light.green()
        elif traffic < 10:
            light.mid_red()
        else:
            light.red_top()
