import re, datetime
import numpy as np
import pandas as pd
import time
import nltk
from nltk.corpus import stopwords
import sys
##global declaration
hold_facts = {}


'''
Author: Towner Hale
'''

##determines if the structure is empty or now

def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True
    
##will parse through sentence every one word, two words ...1 - n      
def extract_words(sentence, span_amount):
    ignore_words = ['a']
    words = sentence.split(" ") #nltk.word_tokenize(sentence)

    span = span_amount        #seperate by 2nth gram
    words = [" ".join(words[i:i+span]) for i in range(0, len(words), span)]
    words_cleaned = [w.lower() for w in words if w not in ignore_words] ##will be commented out with parsing function
    
    ##print("words_cleaned" + str(words_cleaned))
    return words_cleaned    

##creates bagofwords from user_input as well as vocab and origin sent through
def bagofwords(sentence, words, span_amount):
        #account for combinations of words
    
    bag = np.zeros(len(words))
    for x in range(1, span_amount):
        sentence_words = extract_words(sentence, x)

        ##print("this is sentence_words" + str(sentence_words))
        # frequency word count
        for sw in sentence_words:
            for i,word in enumerate(words):
                if word.lower() == sw: 
                    ##print("match with bag[i] :" + str(bag[i]))
                    bag[i] += 1  
                
    return np.array(bag)
  
class Bag_of_words():
    
    def __init__(self, user_input):
        ##dictionary to hold all the categories
        self.user_input = user_input
        
    def read_vocab(self):    
        hold_facts = {
            'origin': [],
            'time': None,
            'date': None,
            'ticket': [],
            'destination': [],
            'single': None
        }
        
        ##holds the vocab file that determines which words are important
        vocab = pd.read_csv('./scripts/train_vocab.csv')
        ##holds the stations names
        station = pd.read_csv('./scripts/stationAndStation_codes.csv')
        hold_vocab = [] 
    
        ##stores in hold_vocab at and from next to the time values that were in vocab
        for x in range(1, len(vocab['Vocab'])):
            hold_vocab.append("at " + str(vocab['Vocab'][x]))       
        
        for x in range(1, len(vocab['Vocab'])):
            hold_vocab.append("from " + str(vocab['Vocab'][x]))
        
        ##stores what was originally in vocab 
        for x in range(1, len(vocab['Vocab'])):
            hold_vocab.append(str(vocab['Vocab'][x]))
            

        ##adds the station names to hold_vocab but with to and from, which the user will need to specify    
        for x in range(1, len(station['Station Name'])):
            hold_vocab.append("to " + str(station['Station Name'][x]))
            # hold_vocab.append(str(station['Station Name'][x]))
            ##print("this is vocab" + str(vocab['Vocab'][x]))
        for x in range(1, len(station['Station Name'])):
            hold_vocab.append("from " + str(station['Station Name'][x])) ##specify to ##specify from   
            
        for x in range(1, len(station['Station Name'])):
            hold_vocab.append(str(station['Station Name'][x])) 
    
        user_input = self.user_input
        
        bag_index = 0
        
        # print(len(hold_vocab))

        ##the range 1, len(user_input) will match each nth part of the user_input with what's stored in the bag of words, so every 1st, every two, every 
        ##three words will be compared to the bag of words vectors so it will be able to read long station names and other combinations of words that 
        ## were stored in hold_vocab
        ##accounts for different combinations
        
        for x in range(1, len(user_input)):

            if (x > 1):
                user_input= user_input[(x-1):]      ##Will reduce the user input by one word each time it runs through bag of words so it can find different combinations of words grouped together
            # fills the bag of words with 8064 0's
            bag_of_words = bagofwords(user_input, hold_vocab, len(user_input))

            # print('bag of words ', bag_of_words, 'length: ', len(bag_of_words))

            for i in range(1, len(bag_of_words)):
               if bag_of_words[i] > 0:  ##if found a match
                    # print('bag of words index: ', i)
                    bag_index = i
                    ##print("found: " + str(hold_vocab[bag_index]))
                    token = nltk.word_tokenize(hold_vocab[bag_index])   ##tokenize the found word in hold_vocab that matches 
                    # print('token: ', token)
                    if token[0] == 'to':        ##finds the destination
                        for i in range(1, len(token)):
                            #if is_empty(hold_facts['destination']): ##has to check if the destination is already stored
                            hold_facts['destination'].append(token[i].lower()) ##append the destination to the category 
                    if token[0] == 'from':        ##finds the origin
                        for i in range(1, len(token)):
                            #if is_empty(hold_facts['origin']):
                            hold_facts['origin'].append(token[i].lower())
                                ##print("this is found origin" )
                    if token[0] == 'return':
                        if hold_facts['single'] is None:
                            hold_facts['single'] = 'no'
                    if token[0] == 'single':
                        if hold_facts['single'] is None:
                            hold_facts['single'] = 'yes'
                    if token[0] == 'a' and token[1] == 'return':        ##finds the origin
                        for i in range(1, len(token)):
                            if hold_facts['single'] is None:
                                hold_facts['single'] = 'no'

                    try:                                                        ##finds the ticket   
                        if token[1] == 'ticket' or token[1] == 'tickets':        
                            if is_empty(hold_facts['ticket']):
                                hold_facts['ticket'].append(token[0])
                    except IndexError:
                        pass  

                    try:
                        time.strptime(str(hold_vocab[bag_index]), '%H:%M')      ##finds the time
                        if hold_facts['time'] is None:
                            hold_facts['time'] = str(hold_vocab[bag_index])
                    except ValueError:
                        pass

        # Extract date from user input
        if '/' in self.user_input:
            # print("it's a date")
            user_input = re.sub("[^\w/]", " ",  self.user_input).split()
            for user_word in user_input:
                if '/' in user_word:
                    try:
                        # print("checking date")
                        date_format = "%d/%m/%Y"
                        date_object = datetime.datetime.strptime(user_word, date_format)
                        if hold_facts['date'] is None:
                            hold_facts['date'] = user_word
                    except ValueError:
                        print('date is not in correct format')

                                
        hold_facts['destination'] = Remove(hold_facts['destination']) ##will remove duplicates 
        hold_facts['destination'] = " ".join(hold_facts['destination'])
        hold_facts['origin'] = Remove(hold_facts['origin']) ##will remove duplicates 
        hold_facts['origin'] = " ".join(hold_facts['origin'])

        if hold_facts['origin'] == '':
            hold_facts['origin'] = None

        if hold_facts['destination'] == '':
            hold_facts['destination'] = None

        return hold_facts
