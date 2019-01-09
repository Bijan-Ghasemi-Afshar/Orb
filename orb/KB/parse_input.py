
import nltk
import csv
import collections
# import stopwords, tokens, stemmer, spelling
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from autocorrect import spell

'''
Text preprocesing class to parse user text. All text is processed in the following order: reduced to lower case, punctation removed,
tokenised, stopwords removed, stem words and OPTIONAL: change supported language (english default), spell check text.

'''
class ParseText:

    # set the language of our input text add functionality to control later
    language = 'english'
    spelling = True

    def __init__(self):
        self.inputText = []

    '''
    Function for testing text
    '''
    def testing(self):

        print("Testing packages support")
        # Print out the supported stopwords languages
        print(stopwords.fileids())
        # Print out english stopwords 
        print (stopwords.words('english'))

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
    Parse all the input conversation text
    '''
    def userInput(self, userText):

        punctuations = '''!()-[]{};'"\,<>.?@#$%^&*_~'''
        stemmer = PorterStemmer()

        # print ("processing user input")
        # reduce uppercase text to lower case
        userText = userText.lower()

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
        for word in conversation:
            if word in stopwords.words(ParseText.language):
                conversation.remove(word)
        # print("Printing the token list: " + str(conversation)) 

        # stem the words 
        for i in range(len(conversation)):
            conversation[i]= stemmer.stem(conversation[i])
        # print("Printing the token list: " + str(conversation))

        # spell check the text
        if ParseText.spelling == True:
            #print("spell test")
            for j in range(len(conversation)):
                conversation[j]= stemmer.stem(spell(conversation[j]))

            # print("Printing the token list: " + str(conversation))
        return conversation



    def testingLogic(self):
        print("Logic testing")
