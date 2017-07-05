from machine import Pin
from apa102 import APA102

class Lights:

    apa = None

    def __init__(self):
        clock = Pin(12, Pin.OUT)
        data = Pin(13, Pin.OUT)
        self.apa = APA102(clock, data, 56)

    def write_pixels(self):
        self.apa.write()
    

    def red_top(self):
        '''sets the top-red-light on and all others off'''
        for i in range(19):
            self.apa[i+37] = (255, 255, 255, 31)
            self.apa[i+19] = (0, 0, 0, 0)
            self.apa[i] = (0, 0, 0, 0)
        self.apa.write()
    
    def red_mid(self):
        '''sets the mid-red-light on and all others off'''
        for i in range(18):
            self.apa[i+37] =(0, 0, 0, 0)
            self.apa[i+19] = (255, 255, 255, 31)
            self.apa[i] = (0, 0, 0, 0)
        self.apa.write()

    def green(self):
        '''sets the green light on and all others off'''
        for i in range(19):
            self.apa[i+37] = (0, 0, 0, 0)
            self.apa[i+19] = (0, 0, 0, 0)
            self.apa[i] = (255, 255, 255, 31)
        self.apa.write()



