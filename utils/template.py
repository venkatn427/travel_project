from database_scripts import insert_or_update_location, create_table, get_city_and_cat_state
csv_file_path = "/Users/venkat/Desktop/TravelProjecr/travelprojectnew/database/travel_Hub_locations.xlsx"
import pandas as pd 
# create_table()
# with open(csv_file_path, 'r') as csv_file:
#     print("loading places data")
#     df = pd.read_excel(csv_file_path, header=None)
#     for index, val in df.iterrows():
#         state = val[0]
#         if len(val[1].split("-")) > 1:
#             place = val[1].split("-")[0]
#             city = val[1].split("-")[1] 
#         else:
#            place = val[1] 
#            city = ""
#         description = val[2]
#         locationcattype = val[3]
#         image = val[4]
#         map_reflink = val[5]
        
#         insert_or_update_location(state, place, city, description, locationcattype, image, map_reflink)
print(get_city_and_cat_state())