# download photos

import requests
from PIL import Image
from io import BytesIO


url = f"https://maps.googleapis.com/maps/api/place/details/json?placeid=ChIJudduh3ZmUjoR3cPhhtS_ZRQ&key=AIzaSyCVPecg2shSb1Xu6r_n6gAQ5O-gOIqtZyU"
req = requests.get(url)
data = req.json()
location = data["result"]["geometry"]["location"]
latitude = location["lat"]
longitude = location["lng"]
photos = data["result"].get("photos", [])
photo_urls = [f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo['photo_reference']}&key=AIzaSyCVPecg2shSb1Xu6r_n6gAQ5O-gOIqtZyU" for photo in photos]