import sqlite3
from datetime import datetime
import os
import csv
import json

global database_nm 
database_nm = os.path.join("database", "travel_data_demo.db") #check this file in sql lite studio to query data

def create_table_update_contact(name, email, phone, message):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    createtable_q = "CREATE TABLE IF NOT EXISTS contact_us(contact_id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT,phone TEXT, message TEXT, contact_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);"
    cur.execute(createtable_q)
    connection.commit()
    cur.execute("INSERT INTO contact_us (name, email, phone, message) VALUES (?, ?, ?, ?)",
                    (name, email, phone, message))
    connection.commit()
    
def update_user_password(username, newpassword):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    sql_query = f" UPDATE users SET password = '{newpassword}' WHERE username = '{username}';"
    cur.execute(sql_query)
    connection.commit()
        
def get_all_states_and_cities():
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cols = ["state", "city"]
    location_all = {}
    for col in cols:
        query = f"select distinct {col} from locations;"
        result = cur.execute(query).fetchall()
        location_all[col] = [location[0] for location in result]
    return location_all
    
def find_user_login(username):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    sql_query = f"SELECT distinct password FROM users where username = '{username}';"
    t = cur.execute(sql_query).fetchall()
    return str("".join(t[0]))
    
def select_all_from_table(table_name, where_clause):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    if where_clause is not None:
        query = f"select * from {table_name} where " + where_clause
    else:
        query = f"select * from {table_name}"
    print(query)
    all_users = cur.execute(query).fetchall()
    return [user for user in all_users]

def create_table():
   connection = sqlite3.connect(database_nm) 
   with open(os.path.join('database','schema.sql')) as f:
        connection.executescript(f.read())
    
def insert_query_user(username, email, password, fname, lname):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cur.execute("INSERT INTO users (username, email, password, firstname, lastname) VALUES (?, ?, ?, ?, ?)",
                    (username, email, password, fname, lname))
    connection.commit()
    return "Record Inserted Successfully"

def insert_or_update_location(state, name, city, description, category, image, map_reflink):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cur.execute("INSERT INTO locations (state, city, name, description, category, image_url, map_reflink) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (state,  city, name, description, category, image, map_reflink))
    connection.commit()
    return "Record Inserted Successfully" 

def update_user_new_login(username):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    sql_statement = f"INSERT INTO user_sessions(username,logout_time) VALUES('{username}','')";  
    cur.execute(sql_statement)
    connection.commit()

def log_user_session(username, session_id):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    sql_statement = f"UPDATE user_sessions SET logout_time = CURRENT_TIMESTAMP, session_id = '{session_id}' WHERE username='{username}' and session_id is NULL"   
    cur.execute(sql_statement)
    connection.commit()
    connection.close()