import pymongo
import csv

# Setup connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
orb_database = client["orbDatabase"]

# Chcek if database exists
db_list = client.list_database_names()
if "orbDatabase" in db_list:
	print("Database exists")
else:
	print("Database does not exist")



# Reading the csv file containing all train stations___________________________
train_station_file_path = "../database_data/stationAndStation_codes.csv"
train_stations = []
with open(train_station_file_path, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
    	train_name = row[0].lower()    	
    	print(train_name)
    	train_abbreviation = row[1]
    	train_stations.append({"name" : train_name, "abbreviation" : train_abbreviation})



# Creating a train station collection and populating it
train_station_collection = orb_database["trainStations"]
doc = train_station_collection.insert_many(train_stations)

# Print list of the _id values of the inserted documents
print(doc.inserted_ids)