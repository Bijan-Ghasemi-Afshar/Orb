'''
A predictive model that determines how late a train journey has been for given information.
Historical data assists the prediction values.
'''

'''
Class that asks the user for their route expected journey time and actual journey time based on know delays.
ask the user if their more than ONE delay, 
'''
import nltk, pymongo, datetime, csv
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

    '''
    Retrieves delay information from user input
    '''
    def get_delay_information(self):

        self.find_keywords_and_information()

        # print(self.delay_information)

        return self.delay_information

    '''
    Finds keywords within the user input and gets journey information after keyword
    '''
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
            from orb.RE import delay_engine
            self.delay_information[delay_engine.get_current_context()] = self.user_input

    '''
    Checks whether keyword exists within user input
    '''
    def keyword_exist(self, tokenized_words):
        for key in self.keywords:
            if self.keywords[key] in tokenized_words:
                return True
        return False

    '''
    Checks whether a word is a keyword or not
    '''
    def is_not_keyword(self, word):
        for key in self.keywords:
            if word == self.keywords[key]:
                return False
        return True

    '''
    Retrieves graphing data from the historical data in the database
    '''
    def graphing_data(self, origin, destination):

        file = open("graphing_data.csv","w") 
 

        origin_abbr = self.get_station_abr(origin.lower())
        destination_abbr = self.get_station_abr(destination.lower())
        
        file.write(',train_no,route_name,departure_time,arrival_time,train_service_type,distance,day_of_service,total_delay,delay_flag\n')

        journey_index = 0
        for journey in orb_database.serviceCollection.find({'origin' : origin_abbr, 'destination' : destination_abbr}):
            journey_index += 1            
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
                destination_actual = int(destination_public)

            destination_delay = destination_actual - destination_public

            if destination_delay < 0:
                destination_delay = 0

            # print('destination_delay: ', destination_delay)

            total_delay = destination_delay + origin_delay

            if total_delay > 0:
                delay_flag = 0
            else:
                delay_flag = 1

            file.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(journey_index, train_no, route_name, origin_actual, destination_actual , train_service_type, distance, day_of_service, total_delay, delay_flag))

            # print('train no: ', train_no)
            # print('route name: ', route_name)
            # print('train_service_type: ', train_service_type)
            # print('distance: ', distance)
            # print('day_of_service: ', day_of_service)
            # print('total_delay: ', total_delay)

        file.close() 

    '''
    Get the average delay of a week
    '''
    def get_week_delay_average(self):
        monday_delay_data = []
        tuesday_delay_data = []
        wednesday_delay_data = []
        thursday_delay_data = []
        friday_delay_data = []
        all_delay_data = []

        file = open("weekday_delay.csv","w") 

        with open('graphing_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[7] == '0':
                    monday_delay_data.append(row)
                elif row[7] == '1':
                    tuesday_delay_data.append(row)
                elif row[7] == '2':
                    wednesday_delay_data.append(row)
                elif row[7] == '3':
                    thursday_delay_data.append(row)
                else: # row[7] == 4:
                    friday_delay_data.append(row)
                all_delay_data.append(row)

        average = self.get_average_delay(monday_delay_data)
        file.write("Monday,{0}\n".format(average))
        average = self.get_average_delay(tuesday_delay_data)
        file.write("Tuesday,{0}\n".format(average))
        average = self.get_average_delay(wednesday_delay_data)
        file.write("Wednesday,{0}\n".format(average))
        average = self.get_average_delay(thursday_delay_data)
        file.write("Thursday,{0}\n".format(average))
        average = self.get_average_delay(friday_delay_data)
        file.write("Friday,{0}\n".format(average))
        average = self.get_average_delay(all_delay_data)
        file.write("Total,{0}\n".format(average))


        file.close()

    '''
    Gets delay details of a week
    '''
    def get_week_delay_detail(self):
        
        monday_file = open("monday_delay_detail.csv","w") 
        tuesday_file = open("tuesday_delay_detail.csv","w")
        wednesday_file = open("wednesday_delay_detail.csv","w")
        thursday_file = open("thursday_delay_detail.csv","w")
        friday_file = open("friday_delay_detail.csv","w")

        monday_file.write(',Day,Time,delay\n')
        tuesday_file.write(',Day,Time,delay\n')
        wednesday_file.write(',Day,Time,delay\n')
        thursday_file.write(',Day,Time,delay\n')
        friday_file.write(',Day,Time,delay\n')

        monday_index = 1
        tuesday_index = 1
        wednesday_index = 1
        thursday_index = 1
        friday_index = 1
        with open('graphing_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[7] == '0':
                    monday_file.write("{0},Monday,{1},{2}\n".format(monday_index, row[4], row[8]))
                    monday_index += 1
                elif row[7] == '1':
                    tuesday_file.write("{0},Tuesday,{1},{2}\n".format(tuesday_index, row[4], row[8]))
                    tuesday_index += 1
                elif row[7] == '2':
                    wednesday_file.write("{0},Wednesday,{1},{2}\n".format(wednesday_index, row[4], row[8]))
                    wednesday_index += 1
                elif row[7] == '3':
                    thursday_file.write("{0},Thursday,{1},{2}\n".format(thursday_index, row[4], row[8]))
                    thursday_index += 1
                else: # row[7] == 4:
                    friday_file.write("{0},Friday,{1},{2}\n".format(friday_index, row[4], row[8]))
                    friday_index += 1

        monday_file.close()
        tuesday_file.close()
        wednesday_file.close()
        thursday_file.close()
        friday_file.close()

    '''
    Gets the whole average delay of historical data
    '''
    def get_average_delay(self, data):
        total = 0
        for element in data:            
            try:
                int(element[8])
            except:
                continue
            total += int(element[8])

        return total/len(data)

    '''
    Gets the station abbreviation
    '''
    def get_station_abr(self, station_name):
        result = orb_database.trainStations.find_one({"name": station_name})
        if result != None:
            return result["abbreviation"]
        else:
            return None



if __name__ == "__main__":

    print('running on its own')

    delay_kb = DelayModel('hello there')

    # delay_kb.graphing_data('norwich', 'london liverpool street')

    # delay_kb.get_week_delay_average()

    delay_kb.get_week_delay_detail()