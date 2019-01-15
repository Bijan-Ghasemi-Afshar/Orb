import json, requests, pymongo

# Setup connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
orb_database = client["orbDatabase"]

# Chcek if database exists
db_list = client.list_database_names()
if "orbDatabase" in db_list:
	print("Database exists")
else:
	print("Database does not exist")


service_metric_url          = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
service_detail_url          = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
headers                     = { "Content-Type": "application/json" }
auths                       = ("b.ghasemi-afshar@uea.ac.uk", "ORBcoursework18%")
service_detail_array        = []
stop_detail_array           = []
service_collection          = orb_database["serviceCollection"] # Creating a service collection and populating it
stop_detail_collection      = orb_database["stopDetailCollection"] # Creating a stop detail collection and populating it



service_metric_data_request = {
  "from_loc": "NRW",
  "to_loc": "LST",
  "from_time": "0000",
  "to_time": "2359",
  "from_date": "2018-11-12",
  "to_date": "2018-11-16",
  "days": "WEEKDAY",
  "tolerance": ["0"]
}


service_metric          = requests.post(service_metric_url, headers=headers, auth=auths, json=service_metric_data_request)
service_metric_data     = json.loads(service_metric.text)

for service_index in service_metric_data['Services']:
    
    for rid in service_index['serviceAttributesMetrics']['rids']:

        origin_station                  = service_index['serviceAttributesMetrics']['origin_location']
        destination_station             = service_index['serviceAttributesMetrics']['destination_location']
        departure_time                  = service_index['serviceAttributesMetrics']['gbtt_ptd']
        arrival_time                    = service_index['serviceAttributesMetrics']['gbtt_pta']
        service_detail_data_request     = {"rid":rid}
        service_detail                  = requests.post(service_detail_url, headers=headers, auth=auths, json=service_detail_data_request)
        service_detail_data             = json.loads(service_detail.text)
        date_of_service                 = service_detail_data['serviceAttributesDetails']['date_of_service']
        stops                           = []
        for stop in service_detail_data['serviceAttributesDetails']['locations']:
            stops.append(stop['location'])

        service_collection.insert({"rid" : rid, "origin" : origin_station, "destination" : destination_station, "stops" : stops, "departure_time": departure_time, "arrival_time": arrival_time, "date" : date_of_service})

        # for stop in service_detail_data['serviceAttributesDetails']['locations']:
        #     stop_detail_collection.insert({"name" : stop['location'], "public_departure_time" : stop['gbtt_ptd'], "actual_departure_time": stop['actual_td'], "public_arrival_time": stop['gbtt_pta'], "actual_arrival_time": stop['actual_ta'], "date":date_of_service, "rid": rid})

    print("Added data for RID: ", rid)
