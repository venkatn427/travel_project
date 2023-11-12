DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS user_sessions; 

CREATE TABLE user_sessions (
    login_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    session_id TEXT,
    login_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    logout_time TIMESTAMP
);

DROP TABLE IF EXISTS location;

CREATE TABLE location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    locationcategory TEXT NOT NULL,
    image_url TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS worldcities; 

CREATE TABLE worldcities (
    city TEXT NOT NULL,
    city_ascii TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    country TEXT NOT NULL,
    country_iso2 TEXT NOT NULL,
    country_iso3 TEXT NOT NULL,
    admin_name TEXT,
    capital TEXT,
    population INTEGER,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

DROP TABLE IF EXISTS city_places;

CREATE TABLE city_places (
    city_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    place TEXT NOT NULL,
    distance FLOAT,
    distancefromcitycenter TEXT ,
    description TEXT
);

CREATE TRIGGER aft_insert AFTER INSERT ON users
BEGIN
INSERT INTO user_sessions(username,logout_time)
         VALUES(NEW.username,"");

END;