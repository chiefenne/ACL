#!/bin/env python

"""LED control for the pyboard (via GPIO pins) using micropython.
Main aim is to implement aircraft anti collision lights and navigation lights.
"""

import sys
import time
import pyb

__author__ = 'Andreas Ennemoser'
__copyright__ = 'Copyright 2016'
__credits__ = ['Sepp Steiner']
__license__ = 'MIT'
__version__ = '1.0'


class LED:
    """Control LEDs attached to pyboard pins via timer """
    def __init__(self, pin='X1', timer_ID=4):
        self.pin = pyb.Pin(pin, pyb.Pin.OUT_PP)
        self.timer_ID = timer_ID

    def on(self):
        self.pin.high()

    def off(self):
        try:
            self.timer.deinit()
        except AttributeError:
            pass
        self.reset()

    def blink(self):
        self.timer = pyb.Timer(self.timer_ID, freq=20, callback=self.blink_cb)
        self.reset()

    def blink_cb(self, timer):
        """Timer callback routine that switches pin state """
        tc = self.count
        if tc < 4:
            self.pin.value(not self.pin.value())
        self.count = (tc+1) % 40

    def strobe(self):
        self.timer = pyb.Timer(self.timer_ID, freq=20, callback=self.strobe_cb)
        self.reset()

    def strobe_cb(self, timer):
        """Timer callback routine that switches pin state """
        tc = self.count
        if tc < 8:
            self.pin.value(not self.pin.value())
        self.count = (tc+1) % 35

    def reset(self):
        self.pin.low()
        self.count = 0


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print ('\n   Usage: python acl.py [1, 2]')
        print ('        1 ... strobo and blink test')
        print ('        2 ... aircraft navigation and anti collision lights\n')
        sys.exit()
    else:
        ctl = int(sys.argv[1])

    if ctl == 1:
        led = LED(pin='X1', timer_ID=11)
        print ('Strobing ...')
        led.strobe()
        print ('Timer ID: ', led.timer_ID)
        print ('Timer source frequency:',
               led.timer.source_freq() / 1.e6, 'MHz')

        time.sleep(5)
        led.off()

        print ('Blinking ...')
        led.timer_ID = 1
        led.blink()
        print ('Timer ID: ', led.timer_ID)
        print ('Timer source frequency:',
               led.timer.source_freq() / 1.e6, 'MHz')
        time.sleep(5)
        led.off()

        print ('On ...')
        led.on()
        time.sleep(5)
        led.off()

        print ('Done.')

    if ctl == 2:
        strobe_1 = LED('X1', timer_ID=11)
        strobe_2 = LED('X2', timer_ID=12)
        strobe_1.strobe()
        strobe_2.strobe()
        acl_1 = LED('X3', timer_ID=13)
        acl_2 = LED('X4', timer_ID=14)
        acl_1.blink()
        acl_2.blink()
        nav_1 = LED('X5')
        nav_2 = LED('X6')
        nav_1.on()
        nav_2.on()
