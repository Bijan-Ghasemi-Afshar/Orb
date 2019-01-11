'''
A predictive model that determines how late a train journey has been for given information.
Historical data assists the prediction values.
'''

'''
Class that asks the user for their route expected journey time and actual journey time based on know delays.
ask the user if their more than ONE delay, 
'''

import nltk
from orb.RE import delay_engine

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

        print(self.delay_information)

        return self.delay_information

        
    def find_keywords_and_information(self):
        tokenized_words = nltk.word_tokenize(self.user_input)
        print(tokenized_words)

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
