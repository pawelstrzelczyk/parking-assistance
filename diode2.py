import RPi.GPIO as GPIO
import time
import board
import neopixel

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER_FRONT = 18
GPIO_ECHO_FRONT = 24

GPIO_TRIGGER_SIDE = 19
GPIO_ECHO_SIDE = 26

order = neopixel.RGB

pixels_front = neopixel.NeoPixel(board.D21, 8, brightness = 0.1)

pixels_right = neopixel.NeoPixel(board.D12, 8, brightness = 0.1)

pixels_left = neopixel.NeoPixel(board.D10, 8, brightness = 0.1)



def setup():
    GPIO.setup(GPIO_TRIGGER_FRONT, GPIO.OUT)
    GPIO.setup(GPIO_ECHO_FRONT, GPIO.IN)

    GPIO.setup(GPIO_TRIGGER_SIDE, GPIO.OUT)
    GPIO.setup(GPIO_ECHO_SIDE, GPIO.IN)


def distance(trigger, echo):
    # set Trigger to HIGH
    GPIO.output(trigger, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    start_time = time.time()
    stop_time = time.time()

    # save start_time
    while GPIO.input(echo) == 0:
        start_time = time.time()

    # save time of arrival
    while GPIO.input(echo) == 1:
        stop_time = time.time()

    # time difference between start and arrival
    time_elapsed = stop_time - start_time
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back

    return (time_elapsed * 34300) / 2


def turnOn(i, pixels):
    pixels[i] = (255, 255, 255)


def turnOf(i, pixels):
    pixels[i] = (0, 0, 0)


def allRed(pixels):
    pixels.fill((255, 0, 0))


def allGreen(pixels):
    pixels.fill((0, 255, 0))


def allYellow(pixels):
    pixels.fill((255, 255, 0))


def turnOffAll(pixels):
    pixels.fill((0, 0, 0))


def front_colors(dist, pixels):
    turnOffAll(pixels)
    if dist < 5:
        allRed(pixels)
    elif dist < 50:
        for i in range(int(dist) // 6):
            turnOn(i, pixels)
    else:
        allYellow(pixels)


def side_colors(dist, pixels):
    turnOffAll(pixels)
    if dist < 5:
        allRed(pixels)
    elif dist < 24:
        for i in range(int(dist) // 3):
            turnOn(i, pixels)
    else:
        allYellow(pixels)


if __name__ == '__main__':
    try:
        setup()

        while True:
            front_colors(distance(GPIO_TRIGGER_FRONT, GPIO_ECHO_FRONT), pixels_front)
            side_colors(distance(GPIO_TRIGGER_SIDE, GPIO_ECHO_SIDE), pixels_right)
            side_colors((25-distance(GPIO_TRIGGER_SIDE, GPIO_ECHO_SIDE)), pixels_left)
            time.sleep(0.1)
    except KeyboardInterrupt:
        turnOffAll(pixels_front)
        turnOffAll(pixels_right)
        turnOffAll(pixels_left)
        print("Measurement stopped by User")

