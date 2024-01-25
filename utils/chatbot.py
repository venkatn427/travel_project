import nltk  # Natural Language Toolkit
from nltk.tokenize import word_tokenize  # Tokenizing text
from nltk.corpus import stopwords  # Removing common words
from nltk.stem import PorterStemmer  # Stemming words
import math
from database_scripts import select_all_from_table, get_all_states_and_cities, create_table, insert_or_update_location

nltk.download('punkt')  # For tokenization
nltk.download('stopwords')  # For stop words
nltk.download('wordnet')  # For lemmatization (optional)

def get_keywords(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    city_state = get_all_states_and_cities
    cities = [city['city'] for city in city_state['city']]
    states = [state['state'] for state in city_state['state']]
    for token in filtered_tokens:
        print(token)
        if token in cities:
            data = select_all_from_table('locations', f"city = '{token}'")
        elif token in states:
            data = select_all_from_table('locations', f"state = '{token}'")
    return data
            
# import pandas as pd
# create_table()

# df = pd.read_csv("/Users/venkat/Desktop/TravelProjecr/travelprojectnew/database/travel_Hub_locations.csv")

# for index, row in df.iterrows():
#     print(row)
#     state, name, city, description, category, image, map_reflink = row
#     insert_or_update_location(state, name, city, description, category, image, map_reflink)                                                                                                       

# print(df)
