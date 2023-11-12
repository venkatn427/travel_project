import math
from database_scripts import select_all_from_table

def calculatedistance_usinglatandlong(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    earth_radius = 6371

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = earth_radius * c

    return distance

def find_nearest_locations(location, city_search):
    pass

import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_temporary_code():
    # Generate a secure, temporary code
    return secrets.token_hex(6)  # Change 6 to the desired length of your code

def send_email(receiver_email, code):
    # Set up the email server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Update with the appropriate port
    smtp_username = "nvenkat427@gmail.com"  # Update with your email address
    smtp_password = "your_email_password"  # Update with your email password

    # Create the email message
    subject = "Temporary Code"
    body = f"Your temporary code is: {code}"

    message = MIMEMultipart()
    message["From"] = smtp_username
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Connect to the email server and send the message
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, receiver_email, message.as_string())

# # Example usage
# email_address = "nvenkat427@gmail.com"  # Update with the recipient's email address
# temporary_code = generate_temporary_code()

# print("checking password function")
# send_email(email_address, temporary_code)
# print(f"Temporary code sent to {email_address}")

import googlemaps
from pprint import pprint

# Replace 'YOUR_API_KEY' with your actual Google Places API key
gmaps = googlemaps.Client(key='AIzaSyD5eTxgUd8qCGHFTHzSAMs8eSC3CvbSGbA')

# Set the location to India
location = "India"

# Make a request to the Places API
places_result = gmaps.places(query=location)

# Extract and print place details
for place in places_result['results']:
    place_id = place['place_id']
    place_details = gmaps.place(place_id=place_id, fields=['name', 'formatted_address'])
    pprint(place_details)
