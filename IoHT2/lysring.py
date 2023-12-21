import time
import colorsys
from rpi_ws281x import Adafruit_NeoPixel, Color
import math

# NeoPixel configuration
pixel_pin = 18  # GPIO pin for NeoPixel Data In (DI)
num_pixels = 12
brightness = 25  # Set to 255 for full brightness

# Set up the NeoPixel strip
strip = Adafruit_NeoPixel(num_pixels, pixel_pin, 800000, 10, False, brightness)
strip.begin()

def set_air_quality(level):
    # Map air quality level to RGB values (green to red gradient)
    if level == 0:
        for j in range(num_pixels):
            strip.setPixelColor(j, Color(0, 0, 0))
        strip.show()
        return

    if level == 11:
        for j in range(num_pixels):
            strip.setPixelColor(j, Color(0, 0, 255))  # Blue color
        strip.show()
        return

    if level <= 5:
        r = int((level / 5.0) * 255)
        g = 255
        b = 0
    else:
        r = 255
        g = int(((10 - level) / 5.0) * 255)
        b = 0

    # Get the current color to smoothly transition
    current_color = strip.getPixelColor(0)
    current_r = (current_color >> 16) & 0xFF
    current_g = (current_color >> 8) & 0xFF
    current_b = current_color & 0xFF

    # Smooth transition to the new color
    steps = 50  # Adjust the number of steps for smoother or faster transitions
    for i in range(steps + 1):
        new_r = int(current_r + (r - current_r) * (i / steps))
        new_g = int(current_g + (g - current_g) * (i / steps))
        new_b = int(current_b + (b - current_b) * (i / steps))

  # Pulsing effect when level is 10 (all LEDs are red)
        if level == 10:
            brightness_factor = abs(math.sin(i / steps * math.pi))  # Sine wave for pulsing
            new_r = int(new_r * brightness_factor)
            new_g = int(new_g * brightness_factor)
            new_b = int(new_b * brightness_factor)

         # Turn off NeoPixel LEDs when the loop is complete

        # Set NeoPixel LEDs color
        for j in range(num_pixels):
            strip.setPixelColor(j, Color(new_r, new_g, new_b))
        strip.show()
        time.sleep(0.02)  # Adjust the sleep duration for smoother or faster transitions


def set_leds(num_leds, color):
    # Set NeoPixel LEDs color
    for j in range(num_leds):
        strip.setPixelColor(j, color)
    strip.show()


def pulse_color(color, cycles=5):
    # Smoothly pulse the specified color for the given number of cycles
    for cycle in range(cycles):
        for i in range(101):
            brightness_factor = abs(math.sin(i / 100 * math.pi))  # Sine wave for pulsing
            r = int(color[0] * brightness_factor)
            g = int(color[1] * brightness_factor)
            b = int(color[2] * brightness_factor)

            # Set NeoPixel LEDs color
            for j in range(num_pixels):
                strip.setPixelColor(j, Color(r, g, b))
            strip.show()
            
            # Adjust the sleep duration for smoother or faster transitions
            time.sleep(0.01)

        # Additional sleep between pulses 
        time.sleep(0.1)

def pulse_color2(color, cycles=5):
    # Smoothly pulse the specified color for the given number of cycles
    for cycle in range(cycles):
        for i in range(101):
            brightness_factor = abs(math.sin(i / 100 * math.pi))  # Sine wave for pulsing
            r = int(color[0] * brightness_factor)
            g = int(color[1] * brightness_factor)
            b = int(color[2] * brightness_factor)

            # Set NeoPixel LEDs color
            for j in range(num_pixels):
                strip.setPixelColor(j, Color(r, g, b))
            strip.show()
            
            # Adjust the sleep duration for smoother or faster transitions
            time.sleep(0.01)

        # Additional sleep between pulses 
        time.sleep(0.2)

def alarm():
    # Pulse all LEDs red for 5 cycles
    red_color = (255, 0, 0)
    pulse_color(red_color, cycles=3)
    return 10 

def loading():
    # Pulse all LEDs red for 5 cycles
    red_color = (150, 0, 150)
    pulse_color2(red_color, cycles=3)

