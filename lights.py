from machine import Pin
from apa102 import APA102
import time

class Lights:
    counter = None
    apa = None

    def __init__(self):
        clock = Pin(12, Pin.OUT)          # Green
        data = Pin(13, Pin.OUT)           # Yellow 
        self.apa = APA102(clock, data, 56)
        self.counter = 0

    def set_low_load(self):
        '''  
        define color for green-light
        '''
        self.set_bottom_color((255, 255, 255, 31))
        self.set_middle_color((0, 0, 0, 0))
        self.set_top_color((0, 0, 0, 0))
        self.write_pixels()

    def set_middle_load(self):
        '''
        define color for mid-red-light
        '''
        self.set_bottom_color((0, 0, 0, 0))
        self.set_middle_color((255, 255, 255, 31))
        self.set_top_color((0, 0, 0, 0))
        self.write_pixels()

    def set_high_load(self):
        '''
        define color for top-red-light
        '''
        self.set_bottom_color((0, 0, 0, 0))
        self.set_middle_color((0, 0, 0, 0))
        self.set_top_color((255, 255, 255, 31))
        self.write_pixels()

    def set_chaos_load(self):
        self.set_bottom_color((0, 0, 0, 0))
        self.set_middle_color((0, 0, 0, 0))
        for i in range(620):
            self.counter = i%31
            self.set_top_color((255, 255, 255, self.counter))
            self.write_pixels()
            


    def write_pixels(self):
        '''
        write pixels^^
        '''
        self.apa.write()

    def set_all_color(self, color):
        '''
        sets the color for all Lights
        '''
        self.set_bottom_color(color)
        self.set_middle_color(color)
        self.set_top_color(color)
        self.write_pixels()

    def set_bottom_color(self, color):
        '''
        sets the green-light
        '''
        for i in range(0, 19):
            self.apa[i] = color

    def set_middle_color(self, color):
        '''
        sets the mid-red-light
        '''
        for i in range(19, 37):
            self.apa[i] = color

    def set_top_color(self, color):
        '''
        sets the top-red-light
        '''
        for i in range(37, 56):
            self.apa[i] = color

