from orb.RE import general_engine, ticket_engine
from orb.KB import parse_input as parse_user_input

# Classifies the chat state based on user input and returns the right engine
def classify_chat(user_input):
	text = parse_user_input.ParseText()
	conversation = user_input
	thisConversation=text.userInput(conversation)
	print("Printing the token list:" + str(thisConversation))
	print(thisConversation)

	return general_engine
