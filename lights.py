from machine import Pin
from apa102 import APA102

class Lights:

    def __init__(self):
        self.clock = Pin(12, Pin.OUT)
        self.data = Pin(13, Pin.OUT)
        self.apa = APA102(clock, data, 56)

    def write_pixels:
        apa.write()

    def green:
        for i in range(19)
            apa[i] = (255, 255, 255, 31)
        apa.write()

    def red_mid:
        for i in range(18)
            apa[i+19] = (255, 255, 255, 31)
        apa.write()

    def red_top:
        for i in range(19)
            apa[i+37] = (255, 255, 255, 31)
        apa.write()

