import pymongo

# Setup connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
orb_database = client["orbDatabase"]

answers = {
	'origin' 		: "NRW",
	'destination' 	: None,
	'date' 			: "16/12/2018",
	'time' 			: "18:00",
	'single' 		: False	
}

questions = {
	'origin' 		: 'What station are you departing from?',
	'destination' 	: 'What is your destination?',
	'date'			: 'What day are you traveling?',
	'time'			: 'What time would you like to leave?',
	'single'		: 'Would you like to book a return ticket?'
}

current_question = current_question_type = None

def response(user_input):

	if all_questions_answered():
		return "All questions are answered"
	else:		

		current_question_type, current_question = get_current_question()

		direct_to_right_validation(current_question_type, user_input)

		return current_question

def all_questions_answered():

	for key in answers:		
		if answers[key] == None:
			return False

	return True

def get_current_question():
	for key, value in answers.items():
		if value == None:
			return key, questions[key]			

def direct_to_right_validation(current_question_type, user_input):

	if current_question_type 	== 'origin':
		pass
	elif current_question_type 	== 'destination':
		
		if vaildate_destination(user_input):
			print("destination is valid")
			next_question()
		else:
			print("destination is not valid")
			repeat_question()

	elif current_question_type 	== 'date':
		pass
	elif current_question_type 	== 'time':
		pass
	else: # current_question_type == 'single'
		pass	

def vaildate_destination(user_input):
	station_abr = get_station_abr(user_input)
	if station_abr == None:
		print("No station was found!")
		return False
	else:
		if station_abr != answers['origin']:
			return True
		else:
			print("Destination cannot be the same as origin")
			return False

def get_station_abr(station_name):
	result = orb_database.trainStations.find_one({"name": station_name})
	if result != None:
		return result["abbreviation"]
	else:
		return None

def next_question():
	pass

def repeat_question():
	pass

def construct_url(origin, destincation, date, time):
	return "http://ojp.nationalrail.co.uk/service/timesandfares/{0}/{1}/{2}/{3}/dep".format(origin, destincation, date, time)        
