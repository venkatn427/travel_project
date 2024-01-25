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

DROP TABLE IF EXISTS locations;

CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT NOT NULL,
    city TEXT,
    name TEXT, 
    description TEXT ,
    category TEXT,
    image_url TEXT ,
    map_reflink TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);



CREATE TRIGGER aft_insert AFTER INSERT ON users
BEGIN
INSERT INTO user_sessions(username,logout_time)
         VALUES(NEW.username,"");

END;