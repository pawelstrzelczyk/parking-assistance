#Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO2_TRIGGER = 19
GPIO2_ECHO = 26

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO2_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO2_ECHO, GPIO.IN)

def distance(TRIGGER, ECHO):
    # set Trigger to HIGH
    GPIO.output(TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    # save start_time
    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    # save time of arrival
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    # time difference between start and arrival
    time_elapsed = stop_time - start_time
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (time_elapsed * 34300) / 2

    return distance


if __name__ == '__main__':
    try:
        while True:
            dist = distance(GPIO_TRIGGER, GPIO_ECHO)
            print("Measured Distance front = %.1f cm" % dist)
            dist2 = distance(GPIO2_TRIGGER, GPIO2_ECHO)
            print("Measured Distance side = %.1f cm" % dist2)
            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()


