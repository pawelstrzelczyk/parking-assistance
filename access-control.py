import sqlite3
import time
import subprocess
from sqlite3 import OperationalError

from diode import diode2
from detection import rec_test
from gpiozero import Servo

servo = Servo(25)
servo.detach()

car_width = 0


def startup():
    diode2.setup_diodes()
    init_db_script = open('garage-db.sql')
    created_tables = init_db_script.read().split(";")
    db = sqlite3.connect('garage.db', timeout=25)
    for table in created_tables:
        print(table)
        db.execute(table)
    db.close()


def log_access(license_plate, approved):
    db = sqlite3.connect('garage.db', timeout=25)
    db.cursor().execute("insert into access_log(license_plate_number, approved) values(?, ?)",
                        (license_plate, approved))
    db.commit()
    db.close()
    return


def is_approved(license_plate):
    db = sqlite3.connect('garage.db', timeout=25)
    try:
        cursor = db.cursor().execute(
            "select a.isAllowed, c.width, c.length from car_parameters c JOIN access a USING(license_plate_number) where license_plate_number = (?)",
            (license_plate,))
    except OperationalError:
        return False, 0, 0

    value = cursor.fetchone()
    db.close()
    if value is not None and value[0] == 1:
        return value
    else:
        return False, 0, 0


def open_gate():
    #print("opening gate\n")
    servo.min()
    time.sleep(1)
    servo.detach()
    return


def close_gate():
    #print("closing gate\n")
    servo.max()
    time.sleep(1)
    servo.detach()
    return


def signal_not_approved():
    print("access denied\n")
    return


def find_license_plate():
    # "ERA87TL"

    return rec_test.capture()


def run_distance_helper():
    diode2.run_diodes()


def start_gas_measurement():
    subprocess.Popen(["sudo", "python", "gas.py"])


def start_api():
    subprocess.Popen(["sudo", "python", "flask_demo.py"])


def wait_for_exit():
    parking_distance = diode2.distance(diode2.GPIO_TRIGGER_FRONT, diode2.GPIO_ECHO_FRONT)
    counter = 0
    while True:
        current_distance = diode2.distance(diode2.GPIO_TRIGGER_FRONT, diode2.GPIO_ECHO_FRONT)
        time.sleep(1)
        if current_distance > parking_distance + 2:
            counter += 1

        if counter > 5:
            return


def car_exit(car_length):
    counter = 0
    while True:
        dist = diode2.distance(diode2.GPIO_TRIGGER_FRONT, diode2.GPIO_ECHO_FRONT)
        time.sleep(4)
        print('in exit', car_length)
        if dist > 2 * car_length:
            counter += 1

        if counter > 5:
            return


def wait_and_check_access():
    while True:
        time.sleep(2)
        license_plate = find_license_plate()
        print(license_plate)
        if len(license_plate) == 7 or len(license_plate) == 8:
            db = sqlite3.connect('garage.db', timeout=5)
            approved, car_width, car_length = is_approved(license_plate)

            diode2.car_width = car_width

            log_access(license_plate, approved)
            if approved == 1:
                open_gate()
                run_distance_helper()
                close_gate()
                wait_for_exit()
                open_gate()
                car_exit(car_length)
                print(car_length)
                close_gate()

            else:
                signal_not_approved()
            db.commit()
            db.close()
        else:
            print("License plate not found\n")


if __name__ == '__main__':

    try:
        startup()  # Inicjalizacja bazy danych i połączeń pinów do RaspberryPi
        start_gas_measurement()  # Uruchomienie procesu, który w tle prowadzi pomiary poziomu gazu w powietrzu
        start_api()  # Uruchomienie procesu wystawiającego REST API
        wait_and_check_access() # Uruchomienie pętli głównej programu,
        # obsługującej czujniki odległości, paski LED oraz sterowanie bramą
    except KeyboardInterrupt:
        diode2.turnOffAll(diode2.pixels_front)
        diode2.turnOffAll(diode2.pixels_right)
        diode2.turnOffAll(diode2.pixels_left)
        print("Application stopped by User")
