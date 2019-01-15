import pymongo, datetime, time, requests, re, json
from orb.KB import delay_kb

# Setup connection to the database
client = pymongo.MongoClient("mongodb://localhost:27017/")
orb_database = client["orbDatabase"]


answers = {
	'origin' 		: None,
	'destination' 	: None,
	'time' 			: None,
	'location'		: None,
	'delay'			: None
}

questions = {
	'origin' 		: 'What station did you depart from?',
	'destination' 	: 'What is your destination?',
	'time'			: 'What is the expected arrival time?',
	'location'		: 'What is your current location?',
	'delay'			: 'How long have you been delayed for (enter the number of minutes)?'
}

user_answers = {
	'origin' 		: None,
	'destination' 	: None,
	'time' 			: None,
	'location'		: None,
	'delay'			: None
}

additional_information = ""


def response(user_input):

    print('user input: ', user_input)

    global additional_information
    additional_information = ""

    delay_kb_object = delay_kb.DelayModel(user_input)

    user_answers = delay_kb_object.get_delay_information()

    # user_answers['delay'] = user_input

    if all_questions_answered():
        return predict_delay()
    else:
        for current_question_type in questions:
            if answers[current_question_type] is None and user_answers[current_question_type] is not None:
                if input_is_valid(current_question_type, user_answers):					
                    answers[current_question_type] = user_answers[current_question_type]

        user_answer_confirmation()
        # Check again to see if all questions are answered
        if all_questions_answered():
            return predict_delay()
        else:
            return get_current_question()
    
    return "I'm the delay engine"

def all_questions_answered():
	for key in answers:
		if answers[key] == None:
			return False

	return True

def get_current_question():
	for current_question_type in questions:
		if answers[current_question_type] == None:
			return additional_information + questions[current_question_type]


def input_is_valid(current_question_type, user_answers):
	
    if current_question_type 	== 'origin':
        return validate_origin(user_answers[current_question_type])
    elif current_question_type 	== 'destination':
        return validate_destination(user_answers[current_question_type])
    elif current_question_type 	== 'time':
        return validate_time(user_answers[current_question_type])
    elif current_question_type 	== 'location':
        return validate_location(user_answers[current_question_type])
    else: # current_question_type == 'delay'
        return validate_delay(user_answers[current_question_type])


def validate_origin(user_input):
	station_abr = get_station_abr(user_input)
	if station_abr == None:
		global additional_information
		additional_information += "Please enter a station name!\n"
		return False
	else:
		return True

def validate_destination(user_input):
    station_abr = get_station_abr(user_input)
    if station_abr == None:
	    global additional_information
	    additional_information += "Please enter a station name!\n"
	    return False
    else:
	    if station_abr != answers['origin']:
		    return True
	    else:
          # print("Destination cannot be the same as origin")
    		additional_information += "Destination cannot be the same as origin\n"
    		return False

def validate_time(user_input):
    time_format = "%H:%M"
    try:
        datetime.datetime.strptime(user_input, time_format).time()
        return True
    except ValueError:
        global additional_information
        additional_information += "There was an issue with the time format\n"
        return False

def validate_location(user_input):
    station_name = get_station_abr(user_input)
    if station_name == None:
        global additional_information
        additional_information += "Please enter a station name!\n"
        return False
    else:
        if station_name == answers['destination']:
            additional_information += "You cannot be at the end of your journey and ask for predicting the delay!\n"
            return False
        else:
            return True

def validate_delay(user_input):
    # TODO: parse text needs to keep numbers for minutes of delay
    user_input = int(user_input)
    if user_input <= 0:
        global additional_information
        additional_information += "Delay cannot be under 1 minute!\n"
        return False
    else:
        return True

def get_station_abr(station_name):
	result = orb_database.trainStations.find_one({"name": station_name})
	if result != None:
		return result["name"]
	else:
		return None

def reset_answers():
	for answer_type in answers:
		answers[answer_type] = None

def user_answer_confirmation():
	global additional_information
	
	for answer_type in answers:
		if answers[answer_type] is not None:
			additional_information += answer_type + ": " + str(answers[answer_type]) + "\n"

def get_current_context():
    for key in answers:
        if answers[key] is None:
            return key
    return None

def predict_delay():

    time_format = "%H:%M"
    delay_time = "00:{0}".format(answers['delay'])
    arrival_time_object = datetime.datetime.strptime(answers['time'], time_format)
    delay_minutes = int(answers['delay'])    

    total_delay_time = arrival_time_object + datetime.timedelta(seconds=(60*delay_minutes)) 
    
    print('expected time of arrival: ', arrival_time_object, ' delay time: ', delay_minutes)

    return 'Your expected arrival time is: {0}'.format(total_delay_time.time())