import network
from traffic import *
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('HaSi-Kein-Internet-Legacy', 'bugsbunny')
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())

tr = Traffic()

time.sleep(5)

while True:
    traffic = tr.get_traffic()

    if traffic != 0 and traffic != None:
        print(str(traffic) + " MB/s")
