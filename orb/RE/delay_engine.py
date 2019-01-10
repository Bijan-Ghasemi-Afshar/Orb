# from orb.KB import delay_kb

# answers = {
# 	'origin' 		: None,
# 	'destination' 	: None,
# 	'time' 			: None,
# 	'location'		: None,
# 	'delay'			: None
# }

# questions = {
# 	'origin' 		: 'What station did you depart from?',
# 	'destination' 	: 'What is your destination?',
# 	'time'			: 'What time did you depart from your origin?',
# 	'location'		: 'What is your current location?',
# 	'delay'			: 'How long have you been delayed for?'
# }

# user_answers = {
# 	'origin' 		: None,
# 	'destination' 	: None,
# 	'time' 			: None,
# 	'location'		: None,
# 	'delay'			: None
# }


# def response(user_input):

# 	delay_kb_object = delay_kb.DelayModel(user_input)

# 	if all_questions_answered():
# 		return predict_delay()
# 	else:
# 		for current_question_type in questions:
# 			if answers[current_question_type] is None and user_answers[current_question_type] is not None:
# 				if input_is_valid(current_question_type, user_answers):					
# 					answers[current_question_type] = user_answers[current_question_type]

# 		# Check again to see if all questions are answered
# 		if all_questions_answered():
# 			return predict_delay()
# 		else:
# 			return get_current_question()


# 	return "I'm the delay engine"

# def all_questions_answered():
# 	for key in answers:
# 		if answers[key] == None:
# 			return False

# 	return True

# def get_current_question():
# 	for current_question_type in questions:
# 		if answers[current_question_type] == None:
# 			return questions[current_question_type]


# def input_is_valid(current_question_type, user_answers):
	
# 	if current_question_type 	== 'origin':
# 		return validate_origin(user_answers[current_question_type])
# 	elif current_question_type 	== 'destination':
# 		return validate_destination(user_answers[current_question_type])
# 	elif current_question_type 	== 'date':
# 		return validate_date(user_answers[current_question_type])
# 	elif current_question_type 	== 'time':
# 		return validate_time(user_answers[current_question_type])
# 	elif current_question_type 	== 'return_date':
# 		return validate_return_date(user_answers[current_question_type])
# 	elif current_question_type 	== 'return_time':
# 		return validate_return_time(user_answers[current_question_type])
# 	else: # current_question_type == 'single'
# 		return validate_return(user_answers[current_question_type])


# def validate_origin(user_input):
# 	station_abr = get_station_abr(user_input)
# 	if station_abr == None:
# 		print("No station was found!")
# 		return False
# 	else:
# 		return True

# def validate_destination(user_input):


# def get_station_abr(user_input):
# 	result = orb_database.trainStations.find_one({"name": station_name})
# 	if result != None:
# 		return result["abbreviation"]
# 	else:
# 		return None

# def predict_delay():
# 	pass