
import nltk
import csv
import collections
import re
import datetime
# import stopwords, tokens, stemmer, spelling
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from autocorrect import spell
from nltk.stem import WordNetLemmatizer

'''
Text preprocesing class to parse user text. All text is processed in the following order: reduced to lower case, punctation removed,
tokenised, stopwords removed, stem words and OPTIONAL: change supported language (english default), spell check text.

'''
class ParseText:

    # set the language of our input text add functionality to control later
    language = 'english'
    spelling = True
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    def __init__(self):
        self.inputText = []
        self.language = 'english'
        self.spelling = True
        self.stem_flag = False
        self.lammetize_flag = True
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
    '''
    Function for testing text
    '''
    def testing(self, lemmatizer, stemmer):

        # print("Testing packages support")
        # Print out the supported stopwords languages
        # print(stopwords.fileids())
        # Print out english stopwords 
        # print ("yo: ", stopwords.words('english'))
        print ("yo: ")
        # print('Lemmatize: ', lemmatizer.lemmatize("bus"))
        # print('stemmed', stemmer.stem("bus"))

    '''
    Set the system text input langauge 
    '''
    def setLanguage(self):

        language = 'english'
        valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
        print("The default language support is: "+language)
        print("Would you like to change the language? Supported langauges are: "+ str(stopwords.fileids()))
        answer = input("Change langauge: [y/n]")
        if answer in (valid):
            #answer = input("Change langauge: [y/n]")          
            if answer == "yes":
                print("Please enter new Language:")
                langauge =input()
                print(langauge)
            elif answer == "no":
                print("langauage is:"+ langauge)
            else:
                print("Please enter yes or no.")


    '''
    Function to activate or deactivate the spell checker
    '''
    def setSpellChecker(self):

        global spelling 
        valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
        print("The default spellcheck support is: "+ParseText.spelling)
        print("Would you like to change the spellcheck?")
        answer = input("Change spellcheck: [y/n]")
        if answer in (valid):
            
            if answer == "yes":
                print("Spell check active:")
                spelling = True
                print(ParseText.spelling)
            elif answer == "no":
                print("Spell check not active")
                spelling =False
                print(spelling)
            else:
                print("Please enter yes or no.")
   
    '''
    Validate the date and append a date flag
    '''
    def dateChecker(self, userText):
        if '/' in userText:
            modified_text_with_date = []
            userText_arr = re.sub("[^\w/]", " ",  userText).split()
            for user_word in userText_arr:
                if '/' in user_word:
                    try:
                        date_format = "%d/%m/%Y"
                        datetime.datetime.strptime(user_word, date_format)
                        user_word = 'date ' + user_word
                    except ValueError:
                        print('date is not in correct format')
                modified_text_with_date.append(user_word)
            user_input = " ".join(modified_text_with_date)
        return userText



    '''
    Validate the time and append a time flag
    '''
    def timeChecker(self, userText):
        if ':' in userText:
            modified_text_with_time = []
            userText_arr = re.sub("[^\w:]", " ",  userText).split()
            for user_word in userText_arr:
                if ':' in user_word:
                    try:
                        time_format = "%H:%M"
                        datetime.datetime.strptime(user_word, time_format).time()
                        user_word = 'time ' + user_word
                    except ValueError:
                        print('time is not in correct format')
                modified_text_with_time.append(user_word)
            user_input = " ".join(modified_text_with_time)
        return userText

    '''
    Parse all the input conversation text
    '''
    def userInput(self, userText):

        # punctuations = '''!()-[]{};'"\,<>.?@#$%^&*_~'''
        punctuations = '!'
        stemmer = PorterStemmer()
        lemmatizer = WordNetLemmatizer()

        self.testing(lemmatizer, stemmer)


        # print ("processing user input")
        # reduce uppercase text to lower case
        userText = userText.lower()
        userText = self.dateChecker(userText)
        userText = self.timeChecker(userText)
        # remove all punctuation
        noPunct = ""
        for char in userText:
            if char not in punctuations:
                noPunct = noPunct + char

        # print(noPunct)
        # split the sentence into tokens
        conversation = nltk.word_tokenize(noPunct)
        # print("Printing the token list: " + str(conversation))

        # remove stopwords
        stop_words = stopwords.words(ParseText.language)
        stop_words.remove('to')
        stop_words.remove('from')
        stop_words.remove('no')
        stop_words.remove('in')
        stop_words.remove('at')
        stop_words.remove('on')
        for word in conversation:
            if word in stop_words:
                conversation.remove(word)
        # print("Printing the token list 2: " + str(conversation)) 

        # stem the words 
        # stem_flag = True
        # if stem_flag:
        #     for i in range(len(conversation)):
        #         conversation[i]= stemmer.stem(conversation[i])
        #     print("Printing the token list 3: " + str(conversation))

        # lemmentise words
        lammetize_flag = True
        if lammetize_flag:
            for i in range(len(conversation)):
                conversation[i]=lemmatizer.lemmatize(conversation[i])
            # print("Printing from token list 4:"+ str(conversation))

        # spell check the text
        if ParseText.spelling == True:
            #print("spell test")
            for j in range(len(conversation)):
                #  conversation[j]= stemmer.stem(spell(conversation[j]))
                 conversation[j] = lemmatizer.lemmatize(spell(conversation[j]))

            # print("Printing the token list 5: " + str(conversation))
        return conversation



    def testingLogic(self):
        print("Logic testing")
