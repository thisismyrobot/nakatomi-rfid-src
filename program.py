from machine import Pin
import time

import mfrc522
import neopixel


LIGHT_PIN = 22  # GPIO 22, hardware pin 29

RFID_MISO = 16  # GPIO 16, hardware pin 21
RFID_SDA_CS = 17  # GPIO 17, hardware pin 22
RFID_SCK = 18  # GPIO 18, hardware pin 24
RFID_MOSI = 19  # GPIO 19, hardware pin 25
RFID_RST = 20  # GPIO 20, hardware pin 26

LEDS = 15
BRIGHTNESS = 20
COLOUR = (255, 0, 0)
DELAY = 0.76  # Seconds, based on detected position and illumination start in scene.
TRANSITION = 0.4  # Seconds, based on scene.
TRANSITION_STEP_SPACE = 0.05  # Seconds, to manage smoothness.
STAY_ON = 30  # Seconds

pixels = neopixel.Neopixel(LEDS, 0, LIGHT_PIN, "GRB")
reader = mfrc522.MFRC522(RFID_SCK, RFID_MOSI, RFID_MISO, RFID_RST, RFID_SDA_CS)

steps = int(TRANSITION / TRANSITION_STEP_SPACE)
brightness_per_step = BRIGHTNESS / steps


def detect():
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat != reader.OK:
        return False

    (stat, raw_uid) = reader.anticoll()
    if stat != reader.OK:
        return False

    return True


def fadein():
    brightness = brightness_per_step
    for i in range(steps):
        pixels.brightness(brightness)
        pixels.set_pixel_line(0, LEDS, COLOUR)
        pixels.show()
        time.sleep(TRANSITION_STEP_SPACE)
        brightness += brightness_per_step


def fadeout():
    brightness = BRIGHTNESS
    for i in range(steps):
        pixels.brightness(brightness)
        pixels.set_pixel_line(0, LEDS, COLOUR)
        pixels.show()
        time.sleep(TRANSITION_STEP_SPACE)
        brightness -= brightness_per_step

    pixels.brightness(0)
    pixels.clear()
    pixels.show()


def main():
    fadeout()
    on = False

    while True:
        if detect():
            if not on:
                time.sleep(DELAY)
                fadein()
                time.sleep(STAY_ON - TRANSITION)
            else:
                fadeout()
            on = not on


if __name__ == '__main__':
    main()
