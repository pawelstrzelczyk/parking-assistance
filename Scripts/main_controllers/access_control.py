import sqlite3
import time
import subprocess
from sqlite3 import OperationalError
import os

from detection import distance_helper, plates_capture
from gpiozero import Servo

servo = Servo(25)
servo.detach()


def startup():
    distance_helper.setup_diodes()

    init_db_script = open('main_controllers/garage-db.sql')
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
                "select a.isAllowed, c.width, c.length from car_parameters c JOIN access a USING(license_plate_number) "
                "where license_plate_number = (?)",
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
    servo.min()
    time.sleep(1)
    servo.detach()
    return


def close_gate():
    servo.max()
    time.sleep(1)
    servo.detach()
    return


def find_license_plate():
    return plates_capture.capture()


def run_distance_helper():
    distance_helper.light_diode_strips()


def start_gas_measurement():
    subprocess.Popen(["sudo", "python", "detection/gas.py"])


def start_api():
    subprocess.Popen(["sudo", "python", "API/garage_control.py"])


def wait_for_exit():
    parking_distance = distance_helper.measure_distance(
            distance_helper.GPIO_TRIGGER_FRONT, distance_helper.GPIO_ECHO_FRONT)
    counter = 0
    while True:
        current_distance = distance_helper.measure_distance(
                distance_helper.GPIO_TRIGGER_FRONT, distance_helper.GPIO_ECHO_FRONT)
        time.sleep(1)
        if current_distance > parking_distance + 2:
            counter += 1

        if counter > 5:
            return


def wait_car_exit(car_length):
    counter = 0
    while True:
        dist = distance_helper.measure_distance(distance_helper.GPIO_TRIGGER_FRONT, distance_helper.GPIO_ECHO_FRONT)
        time.sleep(1)

        if dist > 2 * car_length:
            counter += 1
        else:
            counter = 0

        if counter > 5:
            return


def wait_and_check_access():
    while True:  # P??tla g????wna programu, obs??uguj??ca zdarzenia dotycz??ce pojazd??w
        time.sleep(2)
        license_plate = find_license_plate()  # Wywo??anie funkcji wykrywaj??cej i odczytuj??cej tablic?? rejestracyjn??

        if 7 <= len(license_plate) <= 8:  # Sprawdzenie poprawno??ci d??ugo??ci odczytanego ci??gu znak??w
            db = sqlite3.connect('garage.db', timeout=5)
            approved, car_width, car_length = is_approved(license_plate)  # Sprawdzenie praw dost??pu
            # wjazdu do gara??u w bazie danych i odczytanie parametr??w pojazdu

            distance_helper.CAR_WIDTH = car_width
            log_access(license_plate, approved)  # Zapisanie do bazy danych aktywno??ci dost??pu

            if approved == 1:  # Obs??uga pojazdu po pomy??lnej weryfikacji
                open_gate()  # Otwarcie bramy
                run_distance_helper()  # Uruchomienie wspomagania parkowania (czujniki + diody LED)
                close_gate()  # Zamkni??cie bramy (po wjechaniu samochodu)
                wait_for_exit()  # Oczekiwanie na rozpocz??cie cofania samochodu
                open_gate()  # Otwieranie bramy
                wait_car_exit(car_length)  # Mierzenie odleg??o??ci pojazdu, a?? do opuszczenia gara??u
                close_gate()  # zakmni??cie bramy

            db.commit()
            db.close()


def run_app():
    try:

        startup()  # Inicjalizacja bazy danych i po????cze?? pin??w do RaspberryPi
        start_gas_measurement()  # Uruchomienie procesu, kt??ry w tle prowadzi pomiary poziomu gazu w powietrzu
        start_api()  # Uruchomienie procesu wystawiaj??cego REST API
        wait_and_check_access()  # Uruchomienie p??tli g????wnej programu,
        # obs??uguj??cej czujniki odleg??o??ci, paski LED oraz sterowanie bram??
        return
    except KeyboardInterrupt:
        distance_helper.turnOffAll(distance_helper.pixels_front)
        distance_helper.turnOffAll(distance_helper.pixels_right)
        distance_helper.turnOffAll(distance_helper.pixels_left)
        print("Application stopped by User")
