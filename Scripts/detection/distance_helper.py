import RPi.GPIO as GPIO
import board
import neopixel
import time

CAR_WIDTH = 0

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


def measure_distance(trigger, echo):
    GPIO.output(trigger, True)

    time.sleep(0.00001)
    GPIO.output(trigger, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo) == 0:
        start_time = time.time()

    while GPIO.input(echo) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time

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


def right_side_colors(dist, pixels):
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


def light_diode_strips():
    start = time.time()
    counter = 0
    last_measurement = measure_distance(GPIO_TRIGGER_FRONT, GPIO_ECHO_FRONT)  # Pomiar odległości od końca garażu
    while True:  # Pętla kontrolująca i wspomagająca parkowanie
        front_distance = measure_distance(GPIO_TRIGGER_FRONT, GPIO_ECHO_FRONT)  # Pomiar odległości od końca garażu
        front_colors(front_distance, pixels_front)  # Zapalenie przednich LEDów wspomagających parkowanie
        # w zależności od zmierzonej odległości
        right_side_colors(measure_distance(GPIO_TRIGGER_SIDE, GPIO_ECHO_SIDE), pixels_right)  # Pomiar odległości
        # i zapalenie LEDów z prawej strony
        left_side_colors(measure_distance(GPIO_TRIGGER_SIDE, GPIO_ECHO_SIDE), pixels_left, CAR_WIDTH)  # Pomiar
        # odległości i zapalenie LEDów z lewej strony w zależności od odległości i szerokości pojazdu
        # (pomiar odległości bocznej jest wykonywany tylko z prawej strony)
        time.sleep(0.1)
        counter += 1  # zwiększenie licznika

        if abs(last_measurement - front_distance) > 5 or front_distance >= 5:  # jeśli pozycja samochodu nie zmieniła
            # się znacznie od poprzedniego pomiaru lub samochód podjechał za blisko licznik jest zerowany i kontrola
            # parkowania trwa dalej
            counter = 0
            last_measurement = front_distance
        if counter > 100 and time.time() - start > 30:  # jeśli licznik osiągnął określoną wartość i minął minimalny
            # czas samochód jest uznawany za zaparkowany i kończy się działanie wspomagania parkowania
            break

    turnOffAll(pixels_front)
    turnOffAll(pixels_right)  # wyłączenie pasków LED
    turnOffAll(pixels_left)


if __name__ == '__main__':
    try:
        setup_diodes()

        while True:
            front_colors(measure_distance(GPIO_TRIGGER_FRONT, GPIO_ECHO_FRONT), pixels_front)
            right_side_colors(measure_distance(GPIO_TRIGGER_SIDE, GPIO_ECHO_SIDE), pixels_right)
            left_side_colors(measure_distance(GPIO_TRIGGER_SIDE, GPIO_ECHO_SIDE), pixels_left, CAR_WIDTH)
            time.sleep(0.06)
    except KeyboardInterrupt:
        turnOffAll(pixels_front)
        turnOffAll(pixels_right)
        turnOffAll(pixels_left)
        print("Measurement stopped by User")
