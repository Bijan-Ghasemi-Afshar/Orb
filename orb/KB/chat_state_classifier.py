from orb.RE import general_engine, ticket_engine
from orb.KB import parse_input as parse_user_input
import datetime, pymongo

# Setup connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
orb_database = client["orbDatabase"]

# Classifies the chat state based on user input and returns the right engine
def classify_chat(user_input):
	text = parse_user_input.ParseText()
	conversation = user_input
	thisConversation=text.userInput(conversation)
	# print("Printing the token list:" + str(thisConversation))
	# print(thisConversation)

	# Add the user conversation to the userConvHistory collection in orbDatabase
	# current_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
	# user_conversation = " ".join(str(word) for word in thisConversation)
	# conversation_record = {"conversation" : user_conversation, "date" : current_date}
	# print("Adding conversation record to the database: ", conversation_record)
	# user_conversation_history_collection = orb_database["userConvHistory"]
	# user_conversation_history_collection.insert(conversation_record)

	return ticket_engine
