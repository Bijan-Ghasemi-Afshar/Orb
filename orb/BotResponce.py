from pyknow import *

def greeting():
    print("Hello I am ORB your friendly travel buddy!")
    print("If at any time you get stuck type stuck!")



greeting()


class Greetings(KnowledgeEngine):





    @DefFacts()
    def _initial_action(self):
        yield Fact(action="greet")



    def greet():
        print("hello humans i'm here to take over the world!")


    @Rule (Fact(action='greet'),
          NOT(Fact(name=W())))
    def bot_hello(self):
        self.declare(Fact("Hello i am ORB your train booking companinion!"))

    @Rule(Fact(action='greet'),
          NOT(Fact(name=W())))
    def ask_name(self):
        self.declare(Fact(name=input("What's your name? ")))

    @Rule(Fact(action='greet'),
          NOT(Fact(location=W())))
    def ask_location(self):
        self.declare(Fact(location=input("What station do you wish to depart from? ")))

       # checkStation(self)

    @Rule(Fact(action='greet'),
          NOT(Fact(time=W())))
    def ask_time(self):
        self.declare(Fact(time=input("What time would you like to depart? ")))

    # checkStation(self)
    def checkStation(self, station):
        if (station!= station):
            print("error")

    @Rule (Fact(action='greet'),
           NOT(Fact(destination=W())))
    def ask_destination(self):
        self.declare(Fact(destination=input("Where do you wish to travel to ")))

    @Rule (Fact(action='greet'),
           NOT(Fact(tickets=W())))
    def ask_tickets(self):
        self.declare(Fact(tickets=input("how many tickets do you require?")))

    @Rule(Fact(action='greet'),
          Fact(name=MATCH.name),
          Fact(location=MATCH.location),
          Fact(time=MATCH.time),
          Fact(destination=MATCH.destination),
          Fact(tickets=MATCH.tickets))
    def greet(self, name, location, time , destination, tickets):
        print("Hi %s! leaving  %s station at %s and travelling to %s with %s reservation"%(name, location, time, destination, tickets))


engine = Greetings()
engine.reset()  # Prepare the engine for the execution.
engine.run()  # Run it
