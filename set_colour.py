# python2
# util to change all LEDs to same colour
import sys
from dotstar import Adafruit_DotStar

NUM_LEDS = 300

strip = Adafruit_DotStar(NUM_LEDS, 10, 11)
strip.begin()


def set_colour_rgb(r, g, b, brightness=50):
    # Turn all leds the same colour

    strip.setBrightness(brightness)

    for i in range(NUM_LEDS):
        strip.setPixelColor(i, g, r, b)

    strip.show()


if __name__ == "__main__":
    inputs = tuple(int(v) for v in sys.argv[1:])
    if len(inputs) == 3:
        set_colour_rgb(*inputs)
    elif len(inputs) == 4:
        set_colour_rgb(*inputs)
