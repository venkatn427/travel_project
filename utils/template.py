from bs4 import BeautifulSoup
from database_scripts import insert_or_update_location, create_table, insert_load_world_data,get_all_cities,create_indiancities, insert_load_place_data, select_all_with_join
import os
import csv
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# Specify the folder directory containing HTML files
folder_path = "all_htmlfiles"
create_table()
files_in_folder = os.listdir(folder_path)

state_data = []
html_files = [file for file in files_in_folder if file.endswith(".html")]
csv_files = [file for file in files_in_folder if file.endswith(".csv")]

print("table created")
def html_files_load(html_files):
    for file_path in html_files:
        locationcategory = file_path.replace(".html", "").split("_")[1]
        html_path = os.path.join(folder_path, file_path)
        with open(html_path, "r", encoding="utf-8") as file:
            html_data = file.read()
        soup = BeautifulSoup(html_data, 'html.parser')
        article_data = soup.article
        title = soup.title.text
        count = 0
        for section in article_data.find_all('section'):
            section_data = {}
            section_data['state'] = title
            section_data['location_title'] = section.find('h3').text
            section_data['location_description'] = section.find('p').text
            section_data['location_img'] = section.find("img")['src']
            state = title
            location_title = section.find('h3').text
            location_description = section.find('p').text
            location_img = section.find("img")['src']
            insert_or_update_location(state, location_title, location_description,locationcategory, location_img)
            count +=1 
            state_data.append(section_data)
        print(f"{count} records inserted into database")
    return state_data

# html_files_load(html_files)

import requests


csv_file_path = "/Users/venkat/Desktop/TravelProjecr/travel_project/database/worldcities.csv"

def load_world_data_csv(csv_file_path):
    print("loading world places data")
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_file.seek(0)
        next(csv_reader)  
        for val in csv_reader:
            record = val
            city = record[0]
            city_ascii = record[1]
            latitude = record[2]
            longitude = record[3]
            country = record[4]
            country_iso2 = record[5]
            country_iso3 = record[6]
            admin_name = record[7]
            capital = record[8]
            population = record[9]
            insert_load_world_data(city,city_ascii,latitude,longitude,country,country_iso2,country_iso3,admin_name,capital,population)

# load_world_data_csv(csv_file_path)
# create_indiancities()

csv_file_path = "/Users/venkat/Downloads/travel_Hub_locations.xlsx"
import pandas as pd 


import pandas as pd

with open(csv_file_path, 'r') as csv_file:
    print("loading places data")
    df = pd.read_excel(csv_file_path, header=None)
    for index, val in df.iterrows():
        state = val[0]
        if len(val[1].split("-")) > 1:
            place = val[1].split("-")[0]
            city = val[1].split("-")[1] 
        else:
           place = val[1] 
           city = ""
        description = val[2]
        locationcattype = val[3]
        image = val[4]
        map_reflink = val[5]
        
        insert_or_update_location(state, place, city, description, image, map_reflink)

# print(select_all_with_join('Delhi'))