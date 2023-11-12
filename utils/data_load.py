import csv
import json
from datetime import date
import os
import requests
import pandas as pd
import sqlite3

error_files = []
from bs4 import BeautifulSoup


def get_all_details(image_data):
    all_data = []
    for image_metadata in image_data:
        out_data = {}
        try:
            if image_metadata["business_status"] == "OPERATIONAL":
                out_data["place_name"] = image_metadata["name"]
                if "photos" in image_metadata:
                    html_data = image_metadata["photos"][0]["html_attributions"][0]
                    out_data["map_reflink"] = BeautifulSoup(html_data, "html.parser").a[
                        "href"
                    ]
                    out_data["map_nametag"] = BeautifulSoup(
                        html_data, "html.parser"
                    ).a.text
                    out_data["photo_reference"] = image_metadata["photos"][0][
                        "photo_reference"
                    ]
                else:
                    out_data["map_reflink"] = ""
                    out_data["photo_reference"] = ""
                    out_data["map_nametag"] = ""
                out_data["latitude_google"] = image_metadata["geometry"]["location"][
                    "lat"
                ]
                out_data["longitude_google"] = image_metadata["geometry"]["location"][
                    "lng"
                ]
                out_data["google_place_id"] = image_metadata["place_id"]
                if "rating" in image_metadata:
                    out_data["google_place_rating"] = image_metadata["rating"]
                    out_data["google_user_rating"] = image_metadata[
                        "user_ratings_total"
                    ]
                else:
                    out_data["google_place_rating"] = ""
                    out_data["google_user_rating"] = ""
                out_data["place_types"] = image_metadata["types"]
                out_data["google_place_vicinity"] = image_metadata["vicinity"]
            all_data.append(out_data)
        except Exception as e:
            error_files.append(f"error {image_metadata}")

    return all_data


csv_file_path = (
    r"/Users/venkat/Desktop/TravelProjecr/travel_project/database/worldcities.csv"
)


def get_location_data(csv_file_path):
<<<<<<< HEAD
    database_nm = os.path.join(
        "database", "travel_data_new.db"
    )  # check this file in sql lite studio to query data
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS traveldata_maps (json_data TEXT)")
    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        record = row
        if record["iso3"] == "IND":
            print(f"Loading {record['city']} data")
            record_json = {}
            record_json["city"] = record["city"]
            record_json["city_ascii"] = record["city_ascii"]
            record_json["latitude"] = record["lat"]
            record_json["longitude"] = record["lng"]
            record_json["country"] = record["country"]
            record_json["country_iso2"] = record["iso2"]
            record_json["country_iso3"] = record["iso3"]
            record_json["admin_name"] = record["admin_name"]
            record_json["capital"] = record["capital"]
            record_json["population"] = record["population"]
            all_types = [
                "restaurant",
                "point_of_interest",
                "food",
                "lodging",
                "hindu_temple",
                "place_of_worship",
                "museum",
                "tourist_attraction",
            ]
            for type in all_types:
                city = record["city"]
                lat = str(record["lat"])
                lng = str(record["lng"])
                test_api = (
                    "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="
                    + lat
                    + "%2C"
                    + lng
                    + "&type="
                    + type
                    + "&radius=200000&key="
                )
                response = requests.get(test_api)
                print(response.status_code)
                image_metadata = response.json()["results"]
                print(image_metadata)
                out_data = get_all_details(image_metadata)
                print(out_data)
                record_json["places_city"] = out_data
                print(record_json)
                # out_file_name = os.path.join("maps","datafiles",f"{city}_{type}_{str(date.today())}_metadata.json")
                cur.execute(
                    "INSERT INTO traveldata_maps (json_data) VALUES (?)",
                    (str(record_json),),
                )
                break
        else:
            continue


# get_location_data(csv_file_path)

def load_json_database():
    database_nm = os.path.join(
        "/Users/venkat/Desktop/TravelProjecr/travel_project/database", "travel_data_new.db"
    )  # check this file in sql lite studio to query data
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    folder_path = "/Users/venkat/Desktop/TravelProjecr/travel_project/database/datafiles"
    files_in_folder = files_in_folder = os.listdir(folder_path)
    json_files = [file for file in files_in_folder if file.endswith(".json")]

    for file_path in json_files:
        json_path = os.path.join(folder_path, file_path)
        with open(json_path, "r", encoding="utf-8") as file:
            json_data = json.load(file)

        keys_d = [
            "city",
            "city_ascii",
            "latitude",
            "longitude",
            "country",
            "country_iso2",
            "country_iso3",
            "admin_name",
            "capital",
            "population",
            "places_city",
        ]
        place_keys = [
            "place_name",
            "map_reflink",
            "map_nametag",
            "photo_reference",
            "latitude_google",
            "longitude_google",
            "google_place_id",
            "google_place_rating",
            "google_user_rating",
            "place_types",
            "google_place_vicinity",
        ]
        
        column_names = keys_d + place_keys

        # Generate the CREATE TABLE SQL statement
        create_table_sql = f'''
        CREATE TABLE IF NOT EXISTS traveldata_explode (
            {", ".join(f"{col} TEXT" for col in column_names)}
        )
        '''
        
        cur.execute(create_table_sql)

        connection.commit()
        out_val = {}
        for col in keys_d:
            if col != "places_city":
                out_val[col] = json_data[col]
            else:
                for place in json_data[col]:
                    if place:
                        for placekey in place_keys:
                            out_val[placekey] = str(place[placekey]).replace("," , "")
                        col_names = out_val.keys()
                        # data_to_insert = ({", ".join(f"{col}" for col in out_val.values())})
                        # sql_statement = f'''INSERT INTO travel_datajson ({", ".join(f"{col}" for col in col_names)}) VALUES ({", ".join("?" for i in range(len(col_names)))})")'''
                        # print(sql_statement)
                        # print(data_to_insert)
                        # cur.execute(sql_statement, data_to_insert)
                    
                    # Define the data you want to insert
                        data_to_insert = (
                            out_val["city"], out_val["city_ascii"], out_val["latitude"], out_val["longitude"],
                            out_val["country"], out_val["country_iso2"], out_val["country_iso3"],
                            out_val["admin_name"], out_val["capital"], out_val["population"],
                            out_val["place_name"], out_val["map_reflink"], out_val["map_nametag"],
                            out_val["photo_reference"], out_val["latitude_google"], out_val["longitude_google"],
                            out_val["google_place_id"], out_val["google_place_rating"],
                            out_val["google_user_rating"], str(out_val["place_types"]),
                            out_val["google_place_vicinity"]
                        )

                        # Execute the SQL INSERT statement
                        cur.execute('''
                            INSERT INTO traveldata_explode (
                                city, city_ascii, latitude, longitude, country, country_iso2, country_iso3,
                                admin_name, capital, population, place_name, map_reflink, map_nametag,
                                photo_reference, latitude_google, longitude_google, google_place_id,
                                google_place_rating, google_user_rating, place_types, google_place_vicinity
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', data_to_insert)
                    connection.commit()
                    
                    
load_json_database()
=======
    print("loading world places data")
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_file.seek(0)
        next(csv_reader)  
        for val in csv_reader:  
            record = val
            print(f"Loading {record[0]} data")
            if record[6] == "IND":
                record_json = {}
                record_json['city'] = record[0]
                record_json['city_ascii'] = record[1]
                record_json['latitude'] = record[2]
                record_json['longitude'] = record[3]
                record_json['country'] = record[4]
                record_json['country_iso2'] = record[5]
                record_json['country_iso3'] = record[6]
                record_json['admin_name'] = record[7]
                record_json['capital'] = record[8]
                record_json['population'] = record[9]
                all_types = ["restaurant","point_of_interest","food","lodging","hindu_temple","place_of_worship","museum","tourist_attraction"]
                for type in all_types:
                    city = record[0]
                    lat = str(record[2])
                    lng = str(record[3])
                    test_api = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+lat+"%2C"+lng+"&type="+type+"&radius=200000&key="
                    response = requests.get(test_api)
                    image_metadata = response.json()['results']
                    out_data = get_all_details(image_metadata)
                    record_json['places_city'] = out_data
                    out_file_name = os.path.join("database/datafiles",f"{city}_{type}_{str(date.today())}_metadata.json")
                    with open(out_file_name, 'w') as json_file:
                        json.dump(record_json, json_file, indent=2)
            else:
                continue

get_location_data(csv_file_path)
>>>>>>> refs/remotes/origin/main
