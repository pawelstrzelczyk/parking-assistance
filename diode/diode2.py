import RPi.GPIO as GPIO
import board
import neopixel
import time

car_width = 0

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER_FRONT = 18
GPIO_ECHO_FRONT = 24

GPIO_TRIGGER_SIDE = 19
GPIO_ECHO_SIDE = 26

order = neopixel.RGB

pixels_front = neopixel.NeoPixel(board.D21, 8, brightness=0.1)

pixels_right = neopixel.NeoPixel(board.D12, 8, brightness=0.1)

pixels_left = neopixel.NeoPixel(board.D10, 8, brightness=0.1)


def setup_diodes():
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
    if dist < 3 or dist > 30:
        allRed(pixels)
    elif 10 > dist >= 3:
        for i in range(3, int(dist)):
            turnOn(i - 3, pixels)
    else:
        allYellow(pixels)


def left_side_colors(dist, pixels, car_width):

    left_dist = 25 - car_width - dist
    turnOffAll(pixels)
    if left_dist > 10 or left_dist < -5:
        allYellow(pixels)
    elif left_dist < 3:
        allRed(pixels)
    elif left_dist < 10:
        for i in range(3, int(left_dist)):
            turnOn(i - 3, pixels)


def run_diodes():
    start = time.time()
    counter = 0
    last_measurement = distance(GPIO_TRIGGER_FRONT, GPIO_ECHO_FRONT)
    while True:
        front_distance = distance(GPIO_TRIGGER_FRONT, GPIO_ECHO_FRONT)
        front_colors(front_distance, pixels_front)
        side_colors(distance(GPIO_TRIGGER_SIDE, GPIO_ECHO_SIDE), pixels_right)
        left_side_colors(distance(GPIO_TRIGGER_SIDE, GPIO_ECHO_SIDE), pixels_left, car_width)
        time.sleep(0.1)
        counter += 1

        #print('dist front: ', front_distance, ' last dist: ', last_measurement, ' counter: ', counter)
        if abs(last_measurement - front_distance) > 5 or 5 <= front_distance:
            counter = 0
            last_measurement = front_distance
        if counter > 100 and time.time() - start > 30:
            break

    turnOffAll(pixels_front)
    turnOffAll(pixels_right)
    turnOffAll(pixels_left)


if __name__ == '__main__':
    try:
        setup_diodes()

        while True:
            front_colors(distance(GPIO_TRIGGER_FRONT, GPIO_ECHO_FRONT), pixels_front)
            side_colors(distance(GPIO_TRIGGER_SIDE, GPIO_ECHO_SIDE), pixels_right)
            left_side_colors(distance(GPIO_TRIGGER_SIDE, GPIO_ECHO_SIDE), pixels_left, car_width)
            time.sleep(0.06)
    except KeyboardInterrupt:
        turnOffAll(pixels_front)
        turnOffAll(pixels_right)
        turnOffAll(pixels_left)
        print("Measurement stopped by User")
