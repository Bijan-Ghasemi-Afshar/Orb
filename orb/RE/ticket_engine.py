import pymongo, datetime, time

# Setup connection to the database
client = pymongo.MongoClient("mongodb://localhost:27017/")
orb_database = client["orbDatabase"]

answers = {
	'origin' 		: "NRW",
	'destination' 	: "LST",
	'date' 			: "12/02/2019",
	'time' 			: "12:12",
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
	'origin'		: None,
	'destination' 	: None,
	'date'			: None,
	'time'			: None,
	'single'		: None,
	'return_date'	: "12/02/2019",
	'return_time'	: None
}

def response(user_input):

	# TODO: This part will make a request to ticket_KB to get ticket information as a dictionary
	# user_answers['return_date'] = user_input

	if all_questions_answered():
		return "All questions are answered"		# Has to assume the input is about confirmation of the ticket
	else:
		user_answers['return_time'] = user_input
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

	# If it is a return ticket add extra questions and question types
	if answers['single'] and 'return_date' not in answers:
		answers['return_date'] = answers['return_time'] = None
		questions['return_date'] = "What is the date that you would like to return?"
		questions['return_time'] = "What is the time that you would like to return?"

	for key in answers:
		if answers[key] == None:
			return False

	return True

def input_is_valid(current_question_type, user_answers):	# TODO: Add validation to other question types and answers

	if current_question_type 	== 'origin':
		return validate_origin(user_answers[current_question_type])
	elif current_question_type 	== 'destination':
		return validate_destination(user_answers[current_question_type])
	elif current_question_type 	== 'date':
		return validate_date(user_answers[current_question_type])
	elif current_question_type 	== 'time':
		return validate_time(user_answers[current_question_type])
	elif current_question_type 	== 'return_date':
		return validate_return_date(user_answers[current_question_type])
	elif current_question_type 	== 'return_time':
		return validate_return_time(user_answers[current_question_type])
	else: # current_question_type == 'single'
		return validate_return(user_answers[current_question_type])

def validate_origin(user_input):
	station_abr = get_station_abr(user_input)
	if station_abr == None:
		print("No station was found!")
		return False
	else:
		return True	

def validate_destination(user_input):
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

def validate_date(user_input):
	date_format = "%d/%m/%Y"
	time_format = "%H:%M"
	try:
		date_object = datetime.datetime.strptime(user_input, date_format)
		if date_object.date() < datetime.datetime.today().date():
			print("Date provided cannot be in the past")
			return False
		elif date_object.date() == datetime.datetime.today().date() and answers['time'] != None:
			time_object = datetime.datetime.strptime(answers['time'], time_format).time()
			if time_object < datetime.datetime.now().time():
				print("Time provided cannot be in the past")
				return False
			else:
				return True
		else:
			return True
	except ValueError:
		print("Date provided is not in the correct format")
	return False

def validate_time(user_input):
	date_format = "%d/%m/%Y"
	time_format = "%H:%M"
	try:
		time_object = datetime.datetime.strptime(user_input, time_format).time()
		
		if answers['date'] != None:
			date_object = datetime.datetime.strptime(answers['date'], date_format)
			if date_object.date() == datetime.datetime.today().date() and time_object < datetime.datetime.now().time():
				print("Time provided cannot be in the past")
				return False

		return True
	except ValueError:
		print("There was an issue with the time format")
		return False

def validate_return(user_input):
	if 'yes' in user_input:
		user_answers['single'] = True
		return True
	elif 'no' in user_input:
		user_answers['single'] = False
		return True
	else:
		return False

def validate_return_date(user_input):
	date_format = "%d/%m/%Y"
	time_format = "%H:%M"
	try:
		departure_date_object = datetime.datetime.strptime(answers['date'], date_format)
		return_date_object = datetime.datetime.strptime(user_input, date_format)
		if return_date_object.date() < departure_date_object.date():
			print("Return date cannot be before the departure")
			return False
		elif return_date_object.date() == departure_date_object.date() and answers['return_time'] != None:
			departure_time_object = datetime.datetime.strptime(answers['time'], time_format).time()
			return_time_object = datetime.datetime.strptime(answers['return_time'], time_format).time()
			if return_time_object <= departure_time_object:
				print("Retrun time cannot be before the departure")
				return False
			else:
				return True
		else:
			return True
	except ValueError:
		print("Date provided is not in the correct format")
	return False

def validate_return_time(user_input):
	date_format = "%d/%m/%Y"
	time_format = "%H:%M"
	try:
		departure_time_object = datetime.datetime.strptime(answers['time'], time_format).time()
		return_time_object = datetime.datetime.strptime(user_input, time_format).time()
		
		if answers['return_date'] != None:
			departure_date_object = datetime.datetime.strptime(answers['date'], date_format)
			return_date_object = datetime.datetime.strptime(answers['return_date'], date_format)
			if return_date_object.date() == departure_date_object.date() and return_time_object <= departure_time_object:
				print("Retrun time cannot be before the departure")
				return False

		return True
	except ValueError:
		print("There was an issue with the time format")
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
	# TODO: Use the answers dictionary and remove slash and colon from date and time to construct url
	return "http://ojp.nationalrail.co.uk/service/timesandfares/{0}/{1}/{2}/{3}/dep".format(origin, destincation, date, time)        
