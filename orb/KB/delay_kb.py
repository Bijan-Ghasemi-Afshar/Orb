'''
A predictive model that determines how late a train journey has been for given information.
Historical data assists the prediction values.
'''

'''
Class that asks the user for their route expected journey time and actual journey time based on know delays.
ask the user if their more than ONE delay, 
'''
import nltk, pymongo, datetime
# from orb.RE import delay_engine
# from orb.RE import delay_engine

# Setup connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
orb_database = client["orbDatabase"]


class DelayModel():

    def __init__(self, user_input):
        self.user_input = user_input
        self.delay_information = {
            'origin' 		: None,
            'destination' 	: None,
            'time' 			: None,
            'location'		: None,
            'delay'			: None
        }
        self.keywords = {
            'origin' 		: "from",
            'destination' 	: "to",
            'time' 			: "at",
            'location'		: "in"
        }

    def get_delay_information(self):

        self.find_keywords_and_information()

        # print(self.delay_information)

        return self.delay_information

        
    def find_keywords_and_information(self):
        tokenized_words = nltk.word_tokenize(self.user_input)
        # print(tokenized_words)

        if self.keyword_exist(tokenized_words):
            for key in self.keywords:
                if self.keywords[key] in tokenized_words:
                    keyword_index = tokenized_words.index(self.keywords[key])
                    for words_after_keyword in range((keyword_index+1), len(tokenized_words)):
                        if self.is_not_keyword(tokenized_words[words_after_keyword]):
                            if self.delay_information[key] is None:
                                self.delay_information[key] = tokenized_words[words_after_keyword]
                            else:
                                self.delay_information[key] = ' '.join([self.delay_information[key],tokenized_words[words_after_keyword]])
                        else:
                            break
        else:
            self.delay_information[delay_engine.get_current_context()] = self.user_input

    def keyword_exist(self, tokenized_words):
        for key in self.keywords:
            if self.keywords[key] in tokenized_words:
                return True
        return False

    def is_not_keyword(self, word):
        for key in self.keywords:
            if word == self.keywords[key]:
                return False
        return True

    def graphing_data(self, origin, destination):

        file = open("graphing_data.csv","w") 
 

        origin_abbr = self.get_station_abr(origin.lower())
        destination_abbr = self.get_station_abr(destination.lower())
        

        for journey in orb_database.serviceCollection.find({'origin' : origin_abbr, 'destination' : destination_abbr}):
            departure_time = journey['departure_time']
            arrival_time = journey['arrival_time']

            # Getting the Train Number
            if departure_time[-2] == '3':
                train_no = '1{0}'.format(departure_time)
            else:
                train_no = '0{0}'.format(departure_time)

            # Getting the Route Name
            route_name = '{0}-{1}'.format(origin_abbr, destination_abbr)

            # Getting Type Train Service
            train_service_type = 1

            # Getting Distance: 0 -> <200 | 1 -> >200
            distance = 0

            # Getting Day
            journey_date = journey['date']
            day_of_service = datetime.datetime.strptime(journey_date, '%Y-%m-%d').weekday()

            # Getting Delay
            origin_time_detail = orb_database.stopDetailCollection.find_one({"name" : origin_abbr, "rid": journey['rid']})
            # print('public: ', origin_time_detail['public_departure_time'])
            # print('actua: ', origin_time_detail['actual_departure_time'])
            origin_public = origin_time_detail['public_departure_time']
            origin_actual = origin_time_detail['actual_departure_time']

            if origin_public != '':
                origin_public = int(origin_public)
           
            if origin_actual != '':
                origin_actual = int(origin_actual)
            else:
                origin_actual = origin_public

            origin_delay = origin_actual - origin_public

            if origin_delay < 0:
                origin_delay = 0

            # print('origin delay: ', origin_delay)


            destination_time_detail = orb_database.stopDetailCollection.find_one({"name" : destination_abbr, "rid": journey['rid']})
            # print('public: ', destination_time_detail['public_arrival_time'])
            # print('actua: ', destination_time_detail['actual_arrival_time'])
            destination_public = destination_time_detail['public_arrival_time']
            destination_actual = destination_time_detail['actual_arrival_time']

            if destination_public != '':
                destination_public = int(destination_public)
            
            if destination_actual != '':
                destination_actual = int(destination_actual)
            else:
                destination_actual = destination_public

            destination_delay = destination_actual - destination_public

            if destination_delay < 0:
                destination_delay = 0

            # print('destination_delay: ', destination_delay)

            total_delay = destination_delay + origin_delay

            if total_delay > 0:
                delay_flag = 0
            else:
                delay_flag = 1

            file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}\n".format(train_no, route_name, train_service_type, distance, day_of_service, total_delay, delay_flag))

            # print('train no: ', train_no)
            # print('route name: ', route_name)
            # print('train_service_type: ', train_service_type)
            # print('distance: ', distance)
            # print('day_of_service: ', day_of_service)
            # print('total_delay: ', total_delay)

        file.close() 

    def get_station_abr(self, station_name):
        result = orb_database.trainStations.find_one({"name": station_name})
        if result != None:
            return result["abbreviation"]
        else:
            return None



if __name__ == "__main__":

    print('running on its own')

    delay_kb = DelayModel('hello there')

    delay_kb.graphing_data('norwich', 'london liverpool street')
