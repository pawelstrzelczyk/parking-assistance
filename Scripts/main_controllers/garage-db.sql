PRAGMA foreign_keys = ON;
PRAGMA foreign_keys;


DROP TABLE IF EXISTS access;
DROP TABLE IF EXISTS car_parameters;
DROP TABLE IF EXISTS access_log;
DROP TABLE IF EXISTS gas_alerts;


CREATE TABLE car_parameters(
    width REAL NOT NULL,
    length REAL NOT NULL,
    license_plate_number VARCHAR(9) PRIMARY KEY

);


CREATE TABLE access(
    license_plate_number VARCHAR(9) NOT NULL,
    isAllowed INTEGER,
    CONSTRAINT access_FK FOREIGN KEY(license_plate_number)
        REFERENCES car_parameters(license_plate_number) ON DELETE CASCADE
);


CREATE TABLE gas_alerts(
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE access_log(
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved Integer,
    license_plate_number VARCHAR(9) NOT NULL
);

