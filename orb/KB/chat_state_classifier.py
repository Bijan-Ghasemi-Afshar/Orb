from orb.RE import general_engine, ticket_engine
from orb.KB import parse_input as parse_user_input
from orb.KB import bot_classifier as chat_classifier
import datetime, pymongo

# Setup connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
orb_database = client["orbDatabase"]

# Classifies the chat state based on user input and returns the right engine
def classify_chat(user_input):

	text = parse_user_input.ParseText()
	conversation = text.userInput(user_input)
	store_user_conversation(conversation)
	user_conversation = " ".join(str(word) for word in conversation)

	# Classify conversation
	state_classifier = chat_classifier.BotClassifier()
	print(user_conversation)
	conversation_state = state_classifier.classify(user_conversation)
	print('This is the chat state ==> ', conversation_state)

	if conversation_state[0] == 'General':
		return general_engine
	elif conversation_state[0] == 'Booking':
		return ticket_engine
	else:
		return general_engine



def store_user_conversation(conversation):
	current_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
	user_conversation = " ".join(str(word) for word in conversation)
	conversation_record = {"conversation" : user_conversation, "date" : current_date}
	user_conversation_history_collection = orb_database["userConvHistory"]
	user_conversation_history_collection.insert(conversation_record)