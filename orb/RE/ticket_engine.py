import pymongo

# Setup connection to the database
client = pymongo.MongoClient("mongodb://localhost:27017/")
orb_database = client["orbDatabase"]

answers = {
	'origin' 		: "NRW",
	'destination' 	: None,
	'date' 			: "10/01/2019",
	'time' 			: "15:00",
	'single' 		: False	
}

questions = {
	'origin' 		: 'What station are you departing from?',
	'destination' 	: 'What is your destination?',
	'date'			: 'What day are you traveling?',
	'time'			: 'What time would you like to leave?',
	'single'		: 'Would you like to book a return ticket?'
}

user_answers = {
	'destination' 	: None
}

def response(user_input):

	# TODO: This part will make a request to ticket_KB to get ticket information as a dictionary
	user_answers['destination'] = user_input

	if all_questions_answered():
		return "All questions are answered"		# Has to assume the input is about confirmation of the ticket
	else:
		for current_question_type in questions:
			if answers[current_question_type] == None:
				if input_is_valid(current_question_type, user_answers):
					answers[current_question_type] = user_answers[current_question_type]
		# Check again to see if all questions are answered
		if all_questions_answered():
			return "All questions are answered"
			pass # Send to web-scrape
		else:
			return get_current_question()
						

def all_questions_answered():
	for key in answers:		
		if answers[key] == None:
			return False

	return True

def input_is_valid(current_question_type, user_answers):

	if current_question_type 	== 'origin':
		return False
	elif current_question_type 	== 'destination':
		return vaildate_destination(user_answers[current_question_type])
	elif current_question_type 	== 'date':
		return False
	elif current_question_type 	== 'time':
		return False
	else: # current_question_type == 'single'
		return False

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

def get_current_question():
	for current_question_type in questions:
		if answers[current_question_type] == None:
			return questions[current_question_type]

def construct_url(origin, destincation, date, time):
	return "http://ojp.nationalrail.co.uk/service/timesandfares/{0}/{1}/{2}/{3}/dep".format(origin, destincation, date, time)        
