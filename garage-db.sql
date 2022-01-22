DROP TABLE IF EXISTS access;
DROP TABLE IF EXISTS car_parameters;
DROP TABLE IF EXISTS access_log;
DROP TABLE IF EXISTS gas_alerts;



CREATE TABLE access(
    license_plate_number VARCHAR(9),
    isAllowed INTEGER
);

INSERT INTO access values('ERA87TL', 1);

CREATE TABLE gas_alerts(
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE car_parameters(
    width REAL,
    length REAL,
    license_plate_number VARCHAR(9) NOT NULL,
    FOREIGN KEY(license_plate_number) REFERENCES access(license_plate_number)
);
CREATE TABLE access_log(
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved Integer,
    license_plate_number VARCHAR(9) NOT NULL,
    FOREIGN KEY(license_plate_number) REFERENCES access(license_plate_number)
)
