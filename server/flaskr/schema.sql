DROP TABLE IF EXISTS endpoints;
DROP TABLE IF EXISTS networks;
DROP TABLE IF EXISTS alerts;

CREATE TABLE endpoints (
    endpoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT NOT NULL,
    accessible INTEGER NOT NULL,
    network_id INTEGER NOT NULL,
    FOREIGN KEY (network_id)
        REFERENCES networks (network_id)
);

CREATE TABLE networks (
    network_id INTEGER PRIMARY KEY AUTOINCREMENT,
    SSID TEXT NOT NULL
);

CREATE TABLE alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_datetime TEXT NOT NULL,
    end_datetime TEXT,
    endpoint_id INTEGER NOT NULL,
    failure_type TEXT NOT NULL,
    FOREIGN KEY (endpoint_id)
        REFERENCES endpoints (endpoint_id)
);