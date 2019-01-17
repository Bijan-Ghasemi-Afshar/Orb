import pymongo, datetime, time, requests, re, json, nltk
from bs4 import BeautifulSoup
from orb.KB import ticket_kb as ticket_kb

'''
Goal: Handles user intention to book a train ticket.

Action: Sends user input to Ticket Kowledge Base in order to 
retrieve information about the ticket, and these information are validate.
Ticket is found and its information is presented to the user and a link to the ticket.
'''

# Setup connection to the database
client = pymongo.MongoClient("mongodb://localhost:27017/")
orb_database = client["orbDatabase"]

# Required information about the ticket that has to be provided by the user
answers = {
	'origin' 		: None,
	'destination' 	: None,
	'date' 			: None,
	'time' 			: None,
	'single' 		: None 
}

# Qustions about each type of ticket information that must be answered
questions = {
	'origin' 		: 'What station are you departing from?',
	'destination' 	: 'What is your destination?',
	'date'			: 'What day are you traveling?',
	'time'			: 'What time would you like to leave?',
	'single'		: 'Would you like a single or return ticket?'
}

# Ticket information that has been retrieved from user input by the Ticket KB that needs to be validated
user_answers = {
	'origin'		: None,
	'destination' 	: None,
	'date' 			: None,
	'time' 			: None,
	'single' 		: None
}

additional_information = ""

def response(user_input):

	global additional_information
	additional_information = ""

	# Call to ticket_kb for ticket information extraction
	get_user_answer(user_input)

	if all_questions_answered():
		return handle_user_confirmation(user_input)
	else:
		for current_question_type in questions:
			if answers[current_question_type] is None and user_answers[current_question_type] is not None:
				if input_is_valid(current_question_type, user_answers):		
					if current_question_type == 'date':
						user_input_tok = nltk.word_tokenize(user_answers[current_question_type])
						answers[current_question_type] = user_input_tok[1]
					elif current_question_type == 'time':
						user_input_tok = nltk.word_tokenize(user_answers[current_question_type])
						answers[current_question_type] = user_input_tok[1]
					else:
						answers[current_question_type] = user_answers[current_question_type]

		user_answer_confirmation()
		# Check again to see if all questions are answered
		if all_questions_answered():
			return get_ticket_information()
		else:
			return get_current_question()

'''
Sends user input to Ticket Kowledge Base to retrieve ticket information
'''
def get_user_answer(user_input):
	ticket_kb_object = ticket_kb.ticket_kb(user_input)

	user_answes_from_kb = ticket_kb_object.get_ticket_information()

	for answer_type in user_answers:
		if answers['single'] is not None and not answers['single']:

			if answer_type == 'date':
				if answers[answer_type] is not None:
					user_answers['return_date'] = user_answes_from_kb[answer_type]
				else:
					user_answers[answer_type] = user_answes_from_kb[answer_type]
				
			elif answer_type == 'time':
				if answers[answer_type] is not None:
					user_answers['return_time'] = user_answes_from_kb[answer_type]
				else:
					user_answers[answer_type] = user_answes_from_kb[answer_type]

			elif answer_type == 'return_date' or answer_type == 'return_time':
				next
			else:
				user_answers[answer_type] = user_answes_from_kb[answer_type]
			
		else:
			user_answers[answer_type] = user_answes_from_kb[answer_type]	


'''
Checks whether all required questions have been answered
'''
def all_questions_answered():

	# If it is a return ticket add extra questions and question types
	if answers['single'] == False and 'return_date' not in answers:
		answers['return_date'] = answers['return_time'] = None
		user_answers['return_date'] = user_answers['return_time'] = None
		questions['return_date'] = "What is the date that you would like to return?"
		questions['return_time'] = "What is the time that you would like to return?"

	for key in answers:
		if answers[key] == None:
			return False

	return True


'''
Directs ticket information provided by the user to the correct validation process
'''
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


'''
Validates the origin of a journey
'''
def validate_origin(user_input):
	station_name = get_station_name(user_input)
	if station_name == None:
		global additional_information
		additional_information += "No station was found!\n"
		return False
	else:
		return True	


'''
Validates the destination of a journey
'''
def validate_destination(user_input):
	station_name = get_station_name(user_input)
	if station_name == None:
		global additional_information
		additional_information += "No station was found!\n"
		return False
	else:
		if station_name != answers['origin']:
			return True
		else:
			# print("Destination cannot be the same as origin")
			additional_information += "Destination cannot be the same as origin\n"
			return False


'''
Validates the departure date of a journey
'''
def validate_date(user_input):
	print('validating date: ', user_input)
	user_input = nltk.word_tokenize(user_input)
	user_input = user_input[1]
	print('validating date: ', user_input)
	date_format = "%d/%m/%Y"
	time_format = "%H:%M"
	try:
		date_object = datetime.datetime.strptime(user_input, date_format)
		if date_object.date() < datetime.datetime.today().date():
			global additional_information
			additional_information += "Date provided cannot be in the past\n"
			return False
		elif date_object.date() == datetime.datetime.today().date() and answers['time'] != None:
			time_object = datetime.datetime.strptime(answers['time'], time_format).time()
			if time_object < datetime.datetime.now().time():
				additional_information += "Time provided cannot be in the past\n"
				return False
			else:
				return True
		else:
			return True
	except ValueError:
		additional_information += "Date provided is not in the correct format\n"
	return False


'''
Validates the departure time of a journey
'''
def validate_time(user_input):
	print('validating time: ', user_input)
	user_input = nltk.word_tokenize(user_input)
	print('validating time: ', user_input)
	user_input = user_input[1]
	print('validating time: ', user_input)
	userText = " ".join(user_input)
	print('validating time: ', user_input)

	date_format = "%d/%m/%Y"
	time_format = "%H:%M"
	try:
		time_object = datetime.datetime.strptime(user_input, time_format).time()
		
		if answers['date'] != None:
			date_object = datetime.datetime.strptime(answers['date'], date_format)
			if date_object.date() == datetime.datetime.today().date() and time_object < datetime.datetime.now().time():
				global additional_information
				additional_information += "Time provided cannot be in the past\n"
				return False

		return True
	except ValueError:
		# print("There was an issue with the time format")
		additional_information += "There was an issue with the time format\n"
		return False


'''
Validates whether information clarifies the type of ticket
'''
def validate_return(user_input):
	if 'yes' in user_input:
		user_answers['single'] = True
		return True
	elif 'no' in user_input:
		user_answers['single'] = False
		return True
	else:
		return False


'''
Validates the return date of a journey
'''
def validate_return_date(user_input):
	date_format = "%d/%m/%Y"
	time_format = "%H:%M"
	try:
		departure_date_object = datetime.datetime.strptime(answers['date'], date_format)
		return_date_object = datetime.datetime.strptime(user_input, date_format)
		if return_date_object.date() < departure_date_object.date():
			# print("Return date cannot be before the departure")
			global additional_information
			additional_information = "Return date cannot be before the departure"
			return False
		elif return_date_object.date() == departure_date_object.date() and answers['return_time'] != None:
			departure_time_object = datetime.datetime.strptime(answers['time'], time_format).time()
			return_time_object = datetime.datetime.strptime(answers['return_time'], time_format).time()
			if return_time_object <= departure_time_object:
				# print("Retrun time cannot be before the departure")
				additional_information = "Retrun time cannot be before the departure"
				return False
			else:
				return True
		else:
			return True
	except ValueError:
		additional_information = "Date provided is not in the correct format"
		# print("Date provided is not in the correct format")
	return False


'''
Validates the return time of a journey
'''
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
				# print("Retrun time cannot be before the departure")
				global additional_information
				additional_information = "Retrun time cannot be before the departure"
				return False

		return True
	except ValueError:
		additional_information = "There was an issue with the time format"
		# print("There was an issue with the time format")
		return False


'''
Gets the name of a train station
'''
def get_station_name(station_name):
	result = orb_database.trainStations.find_one({"name": station_name})
	if result != None:
		return result["name"]
	else:
		return None


'''
Gets the next question that has to be asked by the system about the ticket
'''
def get_current_question():
	for current_question_type in questions:
		if answers[current_question_type] == None:
			return additional_information + questions[current_question_type]


'''
Finds the ticket online and retrieves its information
'''
def get_ticket_information():
	print('constructing url')
	ticket_url_request = construct_ticket_url()
	print(ticket_url_request)

	# Sending a GET request to get ticket information
	r = requests.get(ticket_url_request)
	html_results = BeautifulSoup(r.text, 'html.parser')

	outbound_tickets = html_results.find("table", {"id": "oft"})
	outbound_tickets = outbound_tickets.findAll("td", class_="has-cheapest")[0]
	ticket_data = outbound_tickets.find('script')
	ticket_data = ''.join(ticket_data.findAll(text=True))
	ticket_data = json.loads(ticket_data)
	out_ticket_price = ticket_data['singleJsonFareBreakdowns'][0]['fullFarePrice']
	out_ticket_dep_time = ticket_data['jsonJourneyBreakdown']['departureTime']
	out_ticket_arr_time = ticket_data['jsonJourneyBreakdown']['arrivalTime']

	if not answers['single']:
		return_ticket = html_results.find("table", {"id": "ift"})
		return_ticket = return_ticket.findAll("td", class_="has-cheapest")[0]
		ticket_data = return_ticket.find('script')
		ticket_data = ''.join(ticket_data.findAll(text=True))
		ticket_data = re.sub('%s', '', ticket_data)
		ticket_data = json.loads(ticket_data)
		ret_ticket_price = ticket_data['singleJsonFareBreakdowns'][0]['fullFarePrice']
		ret_ticket_dep_time = ticket_data['jsonJourneyBreakdown']['departureTime']
		ret_ticket_arr_time = ticket_data['jsonJourneyBreakdown']['arrivalTime']
		ticket_result = "Outbound ticket price of £{0} which departs at {1} and arrives at {2} and a return ticket with price of £{3} which departs at {4} and arrives at {5} have been found. Would you like these tickets?".format(out_ticket_price, out_ticket_dep_time, out_ticket_arr_time, ret_ticket_price, ret_ticket_dep_time, ret_ticket_arr_time)
	else:
		ticket_result = "Cheapest ticket price of £{0} which departs at {1} and arrives at {2}. Would you like this ticket?".format(out_ticket_price, out_ticket_dep_time, out_ticket_arr_time)

	return ticket_result


'''
Handle user confirmation about the ticket presented
'''
def handle_user_confirmation(user_input):
	if 'yes' in user_input:
		ticket_link = "<a href=\"{0}\" target=\"_blank\">Ticket</a>".format(construct_ticket_url())
		reset_answers()
		return ticket_link
	elif 'no' in user_input:
		reset_answers()
		return "Ok, thank you for using me"
	else:
		return "Would you like this ticket?"


'''
Reset the process of booking a ticket
'''
def reset_answers():
	answers.pop("return_date", None)
	answers.pop("return_time", None)
	questions.pop("return_time", None)
	questions.pop("return_date", None)
	user_answers.pop("return_time", None)
	user_answers.pop("return_date", None)
	for answer_type in answers:
		answers[answer_type] = None


'''
Construct the URL to the ticket
'''
def construct_ticket_url():
	date_object = datetime.datetime.strptime(answers['date'], "%d/%m/%Y").date()
	date_url_format = date_object.strftime("%d%m%y")
	time_url_format = answers['time'].replace(':', '')

	if not answers['single']:
		date_object = datetime.datetime.strptime(answers['return_date'], "%d/%m/%Y").date()
		return_date_url_format = date_object.strftime("%d%m%y")
		return_time_url_format = answers['return_time'].replace(':', '')
		return "http://ojp.nationalrail.co.uk/service/timesandfares/{0}/{1}/{2}/{3}/dep/{4}/{5}/dep".format(answers['origin'], answers['destination'], date_url_format, time_url_format, return_date_url_format, return_time_url_format)
	else:
		return "http://ojp.nationalrail.co.uk/service/timesandfares/{0}/{1}/{2}/{3}/dep".format(answers['origin'], answers['destination'], date_url_format, time_url_format)


'''
Get the current type information that is needed to be provided by the user
'''
def get_current_context():
    for key in answers:
        if answers[key] is None:
            return key
    return None


'''
Provide confirmation about the ticket information provided by the user
'''
def user_answer_confirmation():
	global additional_information
	
	for answer_type in answers:
		if answers[answer_type] is not None:
			additional_information += answer_type + ": " + str(answers[answer_type]) + "\n"