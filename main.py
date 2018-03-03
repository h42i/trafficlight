import network
import time
from umqtt.simple import MQTTClient
from lights import *
from traffic import *

# Config
wifi_ssid = "HaSi-Kein-Internet-Legacy"
wifi_psk = "bugsbunny"
mqtt_server = "atlas.hasi"
mqtt_client_name = "traffic_light"
mqtt_topic = "hasi/lights/traffic_light"

# State
lights_on = True
mqtt_client = None
snmp_traffic = None
light = None

# Set everything up
def setup():
    global wifi_ssid
    global wifi_psk

    global mqtt_topic
    global mqtt_server
    global mqtt_client
    global mqtt_client_name

    global snmp_traffic
    global light

    # Setup Network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(wifi_ssid, wifi_psk)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

    # Setup MQTT
    mqtt_client = MQTTClient(mqtt_client_name, mqtt_server)
    mqtt_client.set_callback(mqtt_callback)
    mqtt_client.connect()
    mqtt_client.subscribe(bytes(mqtt_topic, "utf-8"))

    # Setup remaining stuff
    snmp_traffic = Traffic()
    light = Lights()

# MQTT-Callback; Triggered by c.check_msg()
def mqtt_callback(topic, msg):
    global lights_on

    message = str(msg, "utf-8")

    if message == "on":
        lights_on = True
    elif message == "off":
        lights_on = False

# Test routine
def test_lights():
    global light

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

# Work work work...
def loop():
    global mqtt_client
    global lights_on
    global light
    global snmp_traffic

    while True:
        if wlan.isconnected():
            #check for mqtt-messages
            time.sleep(1)
            mqtt_client.check_msg()

            if not lights_on:
                light.set_all_color((0, 0, 0, 0))
            else:
                traffic = snmp_traffic.get_traffic()

                if traffic != 0 and traffic != None:
                    if traffic < 5:
                        light.set_low_load()
                    elif traffic < 10:
                        light.set_middle_load()
                    elif traffic < 14:
                        light.set_high_load()
                    else:
                        light.set_chaos_load()
        
        else:
            setup()

setup()
test_lights()
loop()
mqtt_client.disconnect()
