import sqlite3
import time
import subprocess

db = sqlite3.connect('garage.db')

def startup():
    initDBScript = open('garage-db.sql')
    createtables = initDBScript.read().split(";");
    
    for table in createtables:
        db.execute(table);
    
def log_access(license_plate, approved):
    db.cursor().execute("insert into access_log(license_plate_number, approved) values(?, ?)", (license_plate, approved))
    return

def add_new_access_data(license_plate, is_allowed):
    db.cursor().execute("insert into access(license_plate_number, isAllowedvalues(?, ?))", (license_plate, is_allowed))
    return

def remove_access_data(license_plate):
    db.cursor().execute("delete from access where license_plate_number = (?)", (license_plate,));
    return

def allow_access(license_plate):
    db.cursor().execute("update access where license_plate_number = (?) set isAllowed = TRUE", (license_plate,));
    return

def disallow_acess(license_plate):
    db.cursor().execute("update access where license_plate_number = (?) set isAllowed = FALSE", (license_plate,));
    return

def is_approved(license_plate):
    cursor = db.cursor().execute("select isAllowed from access where license_plate_number = (?)", (license_plate,));    
    value = cursor.fetchone()
    print(value)
    if value != None and value[0] == 1:
        return value[0]
    else:
        return False;

def add_car_parameters(license_plate, width, length):
    db.cursor().execute("insert into car_parameters(width, length, license_plate_number) values (?, ?, ?)", (width, length, license_plate_number));

def open_gate():
    print("opening gate\n");
    return;

def signal_not_approved():
    print("access denied\n");
    return;

def find_license_plate():
    return "ERA87TL"

def start_distance_helper():
    subprocess.call("sudo python3 distance-helper.py", shell=True) //diodki

def start_gas_measurement():
    subprocess.call("sudo python3 gas.py", shell=True)

def wait_and_check_access():
    while True:
        time.sleep(5);
        license_plate = find_license_plate()
        if len(license_plate) == 7 or len(license_plate) == 8:
            approved = is_approved(license_plate)
            log_access(license_plate, approved)
            if approved == 1:
                open_gate()
                start_distance_helper();
            else:
                signal_not_approved()
            db.commit()
        else:
            print("License plate not found\n");




if __name__ == '__main__':
    startup()
    start_gas_measurement()
    wait_and_check_access();
