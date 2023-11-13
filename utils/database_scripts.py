import sqlite3
from datetime import datetime
import os
import csv
import json

global database_nm 
database_nm = os.path.join("database", "travel_data_new.db") #check this file in sql lite studio to query data


def select_all_with_join(city_name):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    # query = f"select * from {table_name1} t1 join {table_name2} t2 join t1.{joincol} = t2.{joincol}"
    # if where_clause is not None:
    #     query = query + " where " + where_clause
    query = f"select c.city, c.place, c.description, c.distancefromcitycenter, te.map_reflink, te.google_place_rating from traveldata_explode te join city_places c on c.city = te.city_ascii where te.city = '{city_name}'"
    all_users = cur.execute(query).fetchall()
    return [user for user in all_users]
   
def insert_load_place_data(city, place, distance, distancefromcitycenter, description):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cur.execute("INSERT INTO city_places (city, place, distance, distancefromcitycenter, description) VALUES (?, ?, ?, ?, ?)",
                    (city, place, distance, distancefromcitycenter, description))
    connection.commit()
    return "Record Inserted Successfully" 
        
def insert_load_world_data(city,city_ascii,lat,lng,country,iso2,iso3,admin_name,capital,population):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cur.execute("INSERT INTO worldcities (city, city_ascii, latitude, longitude, country, country_iso2, country_iso3, admin_name, capital, population) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (city,city_ascii,lat,lng,country,iso2,iso3,admin_name,capital,population))
    connection.commit()
    return "Record Inserted Successfully"

def create_indiancities():
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cur.execute("DROP TABLE IF EXISTS indiancities;")
    cur.execute("create table indiancities as select * from worldcities where country = 'India';")
    connection.commit()

def get_all_states():
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cols = ["state", "locationcategory"]
    location_all = []
    for col in cols:
        query = f"select distinct {col} from location;"
        result = cur.execute(query).fetchall()
        all_locations = [location[0] for location in result]
        for location in all_locations:
            l = {}
            l[col] = location
            location_all.append(l)
    return location_all

def get_all_cities():
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cols = ["city"]
    location_all = []
    for col in cols:
        query = f"select distinct c.city from traveldata_explode te join city_places c on lower(c.city) = lower(te.city_ascii);"
        result = cur.execute(query).fetchall()
        all_locations = [location[0] for location in result]
        for location in all_locations:
            l = {}
            l[col] = location
            location_all.append(l)
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

def insert_or_update_location(state, name, description, locationcategory, image_url):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cur.execute("INSERT INTO location (state, name, description,locationcategory, image_url) VALUES (?, ?, ?, ?, ?)",
                    (state, name, description, locationcategory, image_url))
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