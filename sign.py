from __future__ import division
# import RPi.GPIO as GPIO
from dotstar import Adafruit_DotStar
from colorsys import hsv_to_rgb
from itertools import cycle
import time
from math import sin
from signal_processing import Stream


NUM_LEDS = 300


# class Button(object):

#     PIN = 17

#     def __init__(self):

#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#     @property
#     def pressed(self):
#         state = GPIO.input(self.PIN)
#         return not bool(state)


class Strip(object):

    def __init__(self):

        self.strip = Adafruit_DotStar(NUM_LEDS, 10, 11)
        self.strip.begin()
        self.stream = None

        self.time = 0

    def set_colour(self, colour, brightness=50):
        # Turn all leds the same colour

        self.strip.setBrightness(brightness)

        for i in range(NUM_LEDS):
            self.strip.setPixelColor(i, colour)

        self.strip.show()

    def set_colour_rgb(self, r, g, b, brightness=50):
        # Turn all leds the same colour

        self.strip.setBrightness(brightness)

        for i in range(NUM_LEDS):
            self.strip.setPixelColor(i, g, r, b)

        self.strip.show()

    def black(self):
        self.strip.setBrightness(0)
        self.strip.show()

    def aqua(self):
        # Aqua logo, white text
        self.strip.setBrightness(50)

        # White
        r, g, b = 255, 255, 255
        for i in range(180):
            self.strip.setPixelColor(i, g, r, b)

        # Aqua
        r, g, b = 64, 191, 180
        for i in range(180, NUM_LEDS):
            self.strip.setPixelColor(i, g, r, b)

        self.strip.show()

    def hue(self, starting_hue=0):
        # Rainbow through hue spectrum

        self.strip.setBrightness(50)
        repeat = 2
        s = 1
        v = 1

        for i in range(NUM_LEDS):
            h = i / NUM_LEDS * repeat + starting_hue

            r, g, b = hsv_to_rgb(h, s, v)
            r = int(r * 255)
            g = int(g * 255)
            b = int(b * 255)
            self.strip.setPixelColor(i, b, r, g)

        self.strip.show()

    def animate_hue(self):

        self.time += 0.01
        self.hue(self.time)

    def red_tick(self, time=0):

        # Full brightness
        brightness = 100

        r = 0.5 + 0.5 * sin(self.time)
        g = 0
        b = 0

        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)

        self.set_colour_rgb(r, g, b, brightness)

    def animate_red(self):
        # Red flashing
        self.time += 0.05
        self.red_tick(self.time)

    def noop(self):
        pass

    def animate_audio_hue(self):
        if self.stream is None:
            self.stream = Stream()

        bass, mid = self.stream.process_chunk()
        self.music_hue(bass, mid)

    def music_hue(self, bass, mid):

        self.strip.setBrightness(50)
        h = 0.7 - mid * 0.7  # hue from blue (0) to red (1)
        s = 1
        v = 0.5 + bass * 0.5
        r, g, b = hsv_to_rgb(h, s, v)
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        self.set_colour_rgb(r, g, b)

    def animate_audio_vis(self):
        if self.stream is None:
            self.stream = Stream()

        bass, mid = self.stream.process_chunk()
        self.music_vis(bass, mid)

    def music_vis(self, bass, mid):

        self.strip.setBrightness(50)

        h = 0.7 - mid * 0.7  # hue from blue (0) to red (1)
        s = 1
        v = 1

        r, g, b = hsv_to_rgb(h, s, v)
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)

        x = int(bass * NUM_LEDS)

        for i in range(x):
            self.strip.setPixelColor(i, g, r, b)

        for i in range(x, NUM_LEDS):
            self.strip.setPixelColor(i, 0, 0, 0)

        self.strip.show()


class Sign(object):

    modes = [
        'aqua',
        'animate_hue',
        'animate_red',
        'animate_audio_hue',
        'animate_audio_vis',
        'noop',
    ]

    iter_modes = cycle(modes)

    def __init__(self):
        self.strip = Strip()
        # self.button = Button()
        self.change_modes()

    def tick(self):
        fun = getattr(self.strip, self.mode)
        fun()

    def change_modes(self):

        self.mode = next(self.iter_modes)
        print(self.mode)
        self.tick()

        # # debounce
        # while self.button.pressed:
        #     time.sleep(0.05)

    def loop(self):

        while True:

            # if self.button.pressed:
            #     self.change_modes()

            if 'animate' in self.mode:
                self.tick()

            time.sleep(0.01)


def main():
    sign = Sign()
    # Pink
    sign.strip.set_colour_rgb(255, 105, 230)

    # sign.loop()

if __name__ == '__main__':
    main()
