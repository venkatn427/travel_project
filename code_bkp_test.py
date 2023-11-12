def download_image():
    pass


import requests
import json 


def download_google_map_(api_key, location, zoom=14, width=400, height=400, maptype='roadmap'):
    # Google Maps Static API endpoint
    endpoint = "https://maps.googleapis.com/maps/api/staticmap"

    # Prepare parameters for the API request
    params = {
        'center': location,
        'zoom': zoom,
        'size': f'{width}x{height}',
        'maptype': maptype,
        'key': api_key,
    }
    
    search_api = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=Maldives&types=geocode&key=AIzaSyD5eTxgUd8qCGHFTHzSAMs8eSC3CvbSGbA"
    place_api = "https://maps.googleapis.com/maps/api/place/details/json?fields=name%2Crating%2Cformatted_phone_number&place_id=ChIJvXv7qr-ZtSQRiWKVgeEJRUE&key=AIzaSyD5eTxgUd8qCGHFTHzSAMs8eSC3CvbSGbA"
    
    t_api = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=ATJ83zhSSAtkh5LTozXMhBghqubeOxnZWUV2m7Hv2tQaIzKQJgvZk9yCaEjBW0r0Zx1oJ9RF1G7oeM34sQQMOv8s2zA0sgGBiyBgvdyMxeVByRgHUXmv-rkJ2wyvNv17jyTSySm_-_6R2B0v4eKX257HOxvXlx_TSwp2NrICKrZM2d5d2P4q&key=AIzaSyD5eTxgUd8qCGHFTHzSAMs8eSC3CvbSGbA"
    
    test_api = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword=cruise&location=12.9716%2C77.5946&radius=1500&type=restaurant&key=AIzaSyD5eTxgUd8qCGHFTHzSAMs8eSC3CvbSGbA"
    try:
        # Make the API request
        response = requests.get(test_api)
        image_metadata = response.json()['results']
        for each in image_metadata:
            print(each)
        response.raise_for_status()
        with open("image_metadata.json", 'w') as json_file:
            json.dump(image_metadata, json_file)
        

        # Save the image
        with open('map_image.png', 'wb') as f:
            f.write(response.content)

        print("Image downloaded successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")

# Replace 'your_api_key' with your actual Google Maps API key
google_maps_api_key = 'AIzaSyD5eTxgUd8qCGHFTHzSAMs8eSC3CvbSGbA'
location_name = 'Eiffel Tower'  # Replace with the desired location

# # Example usage
# download_google_map_(google_maps_api_key, location_name)




# def download_image_fromurl(url, save_path, image_metadata):
#     image_metadata[url] = {}
#     try:
#         response = requests.get(url)
#         image_metadata[url]['download_status'] = response.status_code
#         if response.status_code == 200:
#             out_file_path = os.path.join("images", save_path)
#             image_metadata[url]['localpath'] = out_file_path
#             with open(out_file_path, 'wb') as file:
#                 file.write(response.content)
#         else:
#             print(f"Failed to download image. Status Code: {response.status_code}")
#     except Exception as e:
#         print(f"Error: {e}")

# import json   

# def downloages_all():
#     image_metadata = {}
#     details = html_files_load(html_files)
#     for file in details:
#         image_url = file['location_img']
#         new_image_path = image_url.replace("https://", "").replace("/", "_")
#         download_image_fromurl(image_url, new_image_path, image_metadata) 
#     with open("image_metadata.json", 'w') as json_file:
#         json.dump(image_metadata, json_file)


import csv
import json
from datetime import date
import os

error_files = []
from bs4 import BeautifulSoup
def get_all_details(image_data):
    all_data = []
    for image_metadata in image_data:
        out_data = {}
        try:
            if image_metadata['business_status'] == 'OPERATIONAL':
                out_data['place_name'] = image_metadata['name']
                if 'photos' in image_metadata:
                    html_data = image_metadata['photos'][0]['html_attributions'][0]
                    out_data['map_reflink'] = BeautifulSoup(html_data, 'html.parser').a['href']
                    out_data['map_nametag'] = BeautifulSoup(html_data, 'html.parser').a.text
                    out_data['photo_reference'] = image_metadata['photos'][0]['photo_reference']
                else:
                    out_data['map_reflink'] = ''
                    out_data['photo_reference'] = ''
                    out_data['map_nametag'] = ''
                out_data['latitude_google'] = image_metadata['geometry']['location']['lat']
                out_data['longitude_google'] = image_metadata['geometry']['location']['lng']
                out_data['google_place_id'] = image_metadata['place_id']
                if 'rating' in image_metadata:
                    out_data['google_place_rating'] = image_metadata['rating']
                    out_data['google_user_rating'] = image_metadata['user_ratings_total']
                else:
                    out_data['google_place_rating'] = ''
                    out_data['google_user_rating'] = ''
                out_data['place_types'] = image_metadata['types']
                out_data['google_place_vicinity'] = image_metadata['vicinity']
        except Exception as e:
            error_files.append(f"error while reading {out_data['place_name']}")
        all_data.append(out_data)
    return all_data

csv_file_path = "worldcities.csv"

def get_location_data(csv_file_path):
    print("loading world places data")
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_file.seek(0)
        next(csv_reader)  
        for val in csv_reader:  
            record = val
            if record[4] == "India":
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
                    test_api = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+lat+"%2C"+lng+"&type="+type+"&radius=15000&key=AIzaSyD5eTxgUd8qCGHFTHzSAMs8eSC3CvbSGbA"
                    response = requests.get(test_api)
                    image_metadata = response.json()['results']
                    out_data = get_all_details(image_metadata)
                    record_json['places_city'] = out_data
                    os.mkdir("datafiles")
                    out_file_name = os.path.join("datafiles",f"{city}_{type}_{str(date.today())}_metadata.json")
                    with open(out_file_name, 'w') as json_file:
                        json.dump(record_json, json_file, indent=2)
            else:
                continue
