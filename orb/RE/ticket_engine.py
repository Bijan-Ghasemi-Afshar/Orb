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

current_question = current_question_type = None

def response(user_input):

	if all_questions_answered():
		return "All questions are answered"
	else:		

		# TODO: The ticket_KB must be implemented to extract ticket information and pass them here
		# Ticket engine shuold send a request to its KB to extract information about the ticket and validates them here
		# Returned: a dictionary of answers and answer types which will be validated

		current_question_type, current_question = get_current_question()

		# This part needs to go into a loop to make sure all answers are checked (START)

		if input_is_valid(current_question_type, user_input):

			answers[current_question_type] = user_input
			return next_question()

		else:	# If current question is not answered, repeat the question
			return current_question
		
		# This part needs to go into a loop to make sure all answers are checked (END)

def all_questions_answered():

	for key in answers:		
		if answers[key] == None:
			return False

	return True

def get_current_question():
	for key, value in answers.items():
		if value == None:
			return key, questions[key]			

def input_is_valid(current_question_type, user_input):

	if current_question_type 	== 'origin':
		return False
	elif current_question_type 	== 'destination':
		return vaildate_destination(user_input)
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

def next_question():
	if all_questions_answered():
		# Needs to send to web-scraping and give back some results
		return "No more questions left"
	else:
		current_question_type, current_question = get_current_question()
		return current_question	

def construct_url(origin, destincation, date, time):
	return "http://ojp.nationalrail.co.uk/service/timesandfares/{0}/{1}/{2}/{3}/dep".format(origin, destincation, date, time)        
