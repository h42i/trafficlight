import network
import traffic

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('HaSi-Kein-Internet-Legacy', 'bugsbunny')
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())

traffic.main()
