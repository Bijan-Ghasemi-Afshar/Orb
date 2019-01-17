'''
Class that asks the user for their ticket information and extract the related data 
passes it to the ticket reasoning engine
'''

import nltk
from orb.RE import ticket_engine

class ticket_kb():

    def __init__(self, user_input):
        self.user_input = user_input
        self.ticket_information = {
            'origin' 		: None,
            'destination' 	: None,
            'date' 			: None,
            'time' 			: None,
            'single' 		: None 
        }
        self.keywords = {
            'origin' 		: 'from',
            'destination' 	: 'to',
            'date' 			: 'on',
            'time' 			: 'at'
        }


    '''
    Retrieves ticket information from user input
    '''
    def get_ticket_information(self):

        self.find_keywords_and_information()

        print(self.ticket_information)

        return self.ticket_information

    '''
    Finds keywords within the user input and gets piece of information after that
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
                            if self.ticket_information[key] is None:
                                self.ticket_information[key] = tokenized_words[words_after_keyword]
                            else:
                                self.ticket_information[key] = ' '.join([self.ticket_information[key],tokenized_words[words_after_keyword]])
                        else:
                            break
        else:
            if ticket_engine.get_current_context() == 'return_date':
                self.ticket_information['date'] = self.user_input
            elif ticket_engine.get_current_context() == 'return_time':
                self.ticket_information['time'] = self.user_input
            else:
                self.ticket_information[ticket_engine.get_current_context()] = self.user_input

        # Treat return and single keywords differnetly
        if 'single' in tokenized_words:
            self.ticket_information['single'] = 'yes'

        if 'return' in tokenized_words:
            self.ticket_information['single'] = 'no'

    '''
    Checks whether a keyword exists within the user input
    '''
    def keyword_exist(self, tokenized_words):
        for key in self.keywords:
            if self.keywords[key] in tokenized_words:
                return True
        return False


    '''
    Checks whether a word is a keyword
    '''
    def is_not_keyword(self, word):
        for key in self.keywords:
            if word == self.keywords[key]:
                return False
        return True
