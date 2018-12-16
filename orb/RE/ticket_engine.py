from flask_pymongo import PyMongo

def response(user_input):
	pass

def get_station_abvr(user_input, mongo):
	return mongo.db.trainStations.find_one({"name": user_input})


def construct_url(origin, destincation, date, time):
	return "http://ojp.nationalrail.co.uk/service/timesandfares/{0}/{1}/{2}/{3}/dep".format(origin, destincation, date, time)        
