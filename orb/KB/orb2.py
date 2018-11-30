import nltk
from convo import demo as t
import convo as orbb

def builtinEngines(whichOne):
    if whichOne == 'eliza':
        nltk.chat.eliza.demo()
    elif whichOne =='ORB':
        orbb.demo()
    else:
        print("unknown built-in chat engine {}".format(whichOne))

def myEngine():
    chatpairs = (
        (r"(.*?)Stock price(.*)",
            ("Today stock price is 100",
            "I am unable to find out the stock price.")),
        (r"(.*?)not well(.*)",
            ("Oh, take care. May be you should visit a doctor",
            "Did you take some medicine ?")),
        (r"(.*?)raining(.*)",
            ("Its monsoon season, what more do you expect ?",
            "Yes, its good for farmers")),
        (r"How(.*?)health(.*)",
            ("I am always healthy.",
            "I am a program, super healthy!")),
        (r".*",
            ("I am good. How are you today ?",
            "What brings you here ?"))
    )
    def chat():
        print("ORB system online")
        print("!"*80)
        print(" >> my Engine << ")
        print("Talk to the program using normal english")
        print("="*80)
        print("Enter 'quit' when done")
        chatbot = nltk.chat.util.Chat(chatpairs, nltk.chat.util.reflections)
        chatbot.converse()

    chat()

if __name__ == '__main__':
    for engine in [ 'ORB','eliza']:
        print("=== demo of {} ===".format(engine))
        #myEngine().chat()
        builtinEngines(engine)
        print()

myEngine()