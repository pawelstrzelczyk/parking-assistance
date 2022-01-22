import time

import board
import neopixel
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 20

GPIO.setup(GPIO_TRIGGER, GPIO.IN)

pixels = neopixel.NeoPixel(board.D21, 8)

ORDER = neopixel.RGB


def gasCheck():
    input = GPIO.input(GPIO_TRIGGER)
    if input:
        pixels.fill((255, 0, 0))
    else:
        pixels.fill((0, 0, 0))


if __name__ == '__main__':
    try:
        while True:
            gasCheck()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
