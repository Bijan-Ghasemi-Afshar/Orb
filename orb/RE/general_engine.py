from orb.KB import general_kb as orb_bot

'''
Goal: Handles user engagement in a general conversation.

Action: Sends user input to General Kowledge Base in order to 
retrieve the correct response based on the system knowledge.
'''
def response(user_input):
	return orb_bot.chat_respond(user_input)