-- -- File generated with SQLiteStudio v3.2.1
-- ON Wed Sep 23 16:46:57 2020 --
-- Text encoding used: UTF-8
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: device
CREATE TABLE device (
    deviceId INTEGER PRIMARY KEY AUTOINCREMENT,
    deviceName VARCHAR NOT NULL,
    platformName VARCHAR DEFAULT Android,
    platformVersion VARCHAR,
    udid VARCHAR NOT NULL,
    server VARCHAR NOT NULL,
    systemPort INTEGER,
    mjpegServerPort INTEGER,
    wdaPort INTEGER,
    status VARCHAR NOT NULL DEFAULT FREE,
    teamName VARCHAR NOT NULL DEFAULT "",
    version INT DEFAULT (1) NOT NULL,
    borrowerIp VARCHAR,
    borrowerHostname VARCHAR,
    currentTestCase VARCHAR,
    previousTestCase VARCHAR,
    previousTestStatus VARCHAR,
    lastBorrowed VARCHAR,
    deviceType VARCHAR DEFAULT Emulator NOT NULL,
    driverPath VARCHAR DEFAULT "/path/to/webdriver" NOT NULL
);

-- Table: servers
CREATE TABLE servers (
    serverId INTEGER PRIMARY KEY AUTOINCREMENT,
    serverAddress VARCHAR NOT NULL,
    adbActive INTEGER DEFAULT 0,
    iosActive INTEGER DEFAULT 0
);

-- Set Default serverAddress during development
-- TODO: REMOVE this before release.
INSERT INTO servers (serverAddress) VALUES('0.0.0.0');
COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
