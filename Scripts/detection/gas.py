import time
import sqlite3
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 20
GPIO.setup(GPIO_TRIGGER, GPIO.IN)


def gasCheck():
    gas_input = GPIO.input(GPIO_TRIGGER)
    if gas_input:
        db = sqlite3.connect('../main_controllers/garage.db', timeout=20)
        db.cursor().execute("INSERT INTO GAS_ALERTS DEFAULT VALUES")
        db.commit()
        db.close()
        time.sleep(5)


if __name__ == '__main__':
    try:
        while True:
            gasCheck()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
