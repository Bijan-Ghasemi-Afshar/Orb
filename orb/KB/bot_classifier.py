# use natural language toolkit
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.porter import PorterStemmer
import json

class BotClassifier:

    language = 'english'
    # word stemmer
    # stemmer = LancasterStemmer()
    stemmer = PorterStemmer()
    # hold the words 
    bagOfWords = {}
    classifyText = {}

    def __init__(self):
        self.inputText = []
        self.bagOfWords = {}
        self.classifyText = {}
        self.stemmer = PorterStemmer()
        self.language = 'english'

    # 3 classes of training data
    def train(self):
        
        
        trainingData = []
        trainingData.append({"class":"General", "sentence":"how are you?"})
        trainingData.append({"class":"General", "sentence":"how is your day?"})
        trainingData.append({"class":"General", "sentence":"good day"})
        trainingData.append({"class":"General", "sentence":"how is it going today?"})
        trainingData.append({"class":"General", "sentence":"what day is it?"})
        trainingData.append({"class":"General", "sentence":"hello"})
        trainingData.append({"class":"General", "sentence":"i'm hungry"})
        trainingData.append({"class":"General", "sentence":"what time is it?"})
        trainingData.append({"class":"General", "sentence":"what have you been up to?"})
        trainingData.append({"class":"General", "sentence":"where am I?"})
        trainingData.append({"class":"General", "sentence":"What are you?"})
        trainingData.append({"class":"General", "sentence":"IS this a chat bot?"})
        trainingData.append({"class":"General", "sentence":"Can i book a train from here?"})
        trainingData.append({"class":"General", "sentence":"Can you help me?"})
        trainingData.append({"class":"General", "sentence":"Isn’t it lovely weather today"})
        trainingData.append({"class":"General", "sentence":"Blah blah ticket blah train"})
        trainingData.append({"class":"General", "sentence":"Where do I go if I need to be going?"})
        trainingData.append({"class":"General", "sentence":"Is UEA a school"})
        trainingData.append({"class":"General", "sentence":"What country are you in?"})
        trainingData.append({"class":"General", "sentence":"What do you think about the US election in 2016?"})
        trainingData.append({"class":"General", "sentence":"Is Trump making America great again?"})
        trainingData.append({"class":"General", "sentence":"Error error error"})
        trainingData.append({"class":"General", "sentence":"Please help me, I would like your assistance"})
        trainingData.append({"class":"General", "sentence":"Do you require a fee?"})
        trainingData.append({"class":"General", "sentence":"Why has Grime not made it big in America?"})
        trainingData.append({"class":"General", "sentence":"What are the differences between America and Europe"})
        trainingData.append({"class":"General", "sentence":"Theresa May did nothing wrong, do you agree?"})
        trainingData.append({"class":"General", "sentence":"Will I ever be able to afford Red Dead Redemption 2?"})
        trainingData.append({"class":"General", "sentence":"What are some TV shows that are currently on?"})
        trainingData.append({"class":"General", "sentence":"Is Hawaii a state?"})
        trainingData.append({"class":"General", "sentence":"What is the meaning of life?"})
        trainingData.append({"class":"General", "sentence":"Is coffee the solution to everything?"})
        trainingData.append({"class":"General", "sentence":"Do you know any popular sayings?"})
        trainingData.append({"class":"General", "sentence":"Who is the best US president of all time?"})
        trainingData.append({"class":"General", "sentence":"Is Lebron better than Jordan?"})
        trainingData.append({"class":"General", "sentence":"Can I book a train ticket from here?"})
        trainingData.append({"class":"General", "sentence":"Norwich, Essex, Liverpool London"})
        trainingData.append({"class":"General", "sentence":"Delay, time, 12:00 pm"})
        trainingData.append({"class":"General", "sentence":"fasdfsf time Book Train to Norwich "})
        trainingData.append({"class":"General", "sentence":"I want to book a train from Colchester?"})
        trainingData.append({"class":"General", "sentence":"How have you been doing?"})
        trainingData.append({"class":"General", "sentence":"Who invented you?"})
        trainingData.append({"class":"General", "sentence":"Are you intelligent?"})
        trainingData.append({"class":"General", "sentence":"Can you pass the turing test?"})
        trainingData.append({"class":"General", "sentence":"Did Thanos do nothing wrong?"})
        trainingData.append({"class":"General", "sentence":"Best sport to play"})
        trainingData.append({"class":"General", "sentence":"What are the geopolitical politics at play?"})


        trainingData.append({"class":"Booking", "sentence":"i want to book a train to london"})
        trainingData.append({"class":"Booking", "sentence":"i want three tickets"})
        trainingData.append({"class":"Booking", "sentence":"from norwich"})
        trainingData.append({"class":"Booking", "sentence":"i want to book a train to london from Colchester"})
        trainingData.append({"class":"Booking", "sentence":"i want to book a train to london from Colchester at 12:00 am with a return ticket"})
        trainingData.append({"class":"Booking", "sentence":"i want two tickets"})
        trainingData.append({"class":"Booking", "sentence":"I want to book a train from Abergele & Pensarn to Colchester"})
        trainingData.append({"class":"Booking", "sentence":"I want to book a train from Abergele & Pensarn to Accrington"})
        trainingData.append({"class":"Booking", "sentence":"i want three tickets to Norwich at 7:45 am"})
        trainingData.append({"class":"Booking", "sentence":"I want a return ticket"})
        trainingData.append({"class":"Booking", "sentence":"i want to a return ticket to Alton from Norwich"})
        trainingData.append({"class":"Booking", "sentence":"i want to go to Colchester and have three tickets as well as a return"})
        trainingData.append({"class":"Booking", "sentence":"i want to go to Armadale (West Lothian) from Norwich"})
        trainingData.append({"class":"Booking", "sentence":"i want to go to Ascott-under-Wychwood from Ashford International (Eurostar)"})
        trainingData.append({"class":"Booking", "sentence":"I would like a return to Ashwell & Morden at 12:45 am from Colchester"})
        trainingData.append({"class":"Booking", "sentence":"i need to book a train at 7pm"})
        trainingData.append({"class":"Booking", "sentence":"i need to book a return train at 3pm"})
        trainingData.append({"class":"Booking", "sentence":"i need to book a return train at 3pm"})
        trainingData.append({"class":"Booking", "sentence":"hello Orb, i want to book a train"})
        trainingData.append({"class":"Booking", "sentence":"book a journey for april!"})
        trainingData.append({"class":"Booking", "sentence":"i need to book a return train at 3pm"})
        trainingData.append({"class":"Booking", "sentence":"Can you book me a train?"})
        trainingData.append({"class":"Booking", "sentence":"Are there any trains going to Ashurst (Kent) from where I am?"})
        trainingData.append({"class":"Booking", "sentence":"Can I get 10 tickets to Auchinleck"})
        trainingData.append({"class":"Booking", "sentence":"I would like a ticket to Birmingham"})
        trainingData.append({"class":"Booking", "sentence":"Can I get a return from Crystal Palace to Norwich at 3:00 am"})
        trainingData.append({"class":"Booking", "sentence":"Can I get a ticket from London Liverpool to Dalmarnock"})
        trainingData.append({"class":"Booking", "sentence":"Is there a train to Hale (Manchester)"})
        trainingData.append({"class":"Booking", "sentence":"I am in Hall-i'-th'-Wood and I would like to get a ticket to Auchinleck"})
        trainingData.append({"class":"Booking", "sentence":"I am in Hall-i'-th'-Wood and I would like to get a ticket to A.."})
        trainingData.append({"class":"Booking", "sentence":"Can I book a ticket to Hamstead (Birmingham)"})
        trainingData.append({"class":"Booking", "sentence":"Can I book a ticket to Hamstead Birmingham"})
        trainingData.append({"class":"Booking", "sentence":"Can I book a ticket to Birmingham Hamstead"})
        trainingData.append({"class":"Booking", "sentence":"Hatfield & Stainforth to Hatfield (Herts)"})
        trainingData.append({"class":"Booking", "sentence":"12:00 am Hatfield to Herts"})
        trainingData.append({"class":"Booking", "sentence":"Hertford East two tickets to Hertford North with a return at 12:00 am"})
        trainingData.append({"class":"Booking", "sentence":"i want to book a train High Street (Glasgow) from Hertford North"})
        trainingData.append({"class":"Booking", "sentence":"i want to book a train to london from Hillington East"})
        trainingData.append({"class":"Booking", "sentence":"Hinchley Wood at 7:50 pm I would like a train"})
        trainingData.append({"class":"Booking", "sentence":"Howwood (Renfrewshire) at 3:00 pm to Norwich with a return"})
        trainingData.append({"class":"Booking", "sentence":"I would like to return from Hyde Central to Norwich at 1:00 pm"})
        trainingData.append({"class":"Booking", "sentence":"i want to book a train to Inverness at 4:01 pm "})
        trainingData.append({"class":"Booking", "sentence":"A ticket to Johnston (Pembs)at 5:00 am"})
        trainingData.append({"class":"Booking", "sentence":"A ticket to Johnston (Pembs)at 7:30 am"})
        trainingData.append({"class":"Booking", "sentence":"I would like 4 tickets to Johnstone (Strathclyde)"})
        trainingData.append({"class":"Booking", "sentence":"Kilburn High Road to Norwich and 2 tickets at 3:00 pm "})
        trainingData.append({"class":"Booking", "sentence":"Kilburn High Road to Norwich and 25 tickets at 3:00 pm "})
        trainingData.append({"class":"Booking", "sentence":"Kilburn High Road to Norwich and 2 tickets at 5:00 pm "})
        trainingData.append({"class":"Booking", "sentence":"i want to book a trin from Kings Langley"})


        trainingData.append({"class":"Model", "sentence":"how often is the train late"})
        trainingData.append({"class":"Model", "sentence":"how long will my delay be?"})
        trainingData.append({"class":"Model", "sentence":"is the train late?"})
        trainingData.append({"class":"Model", "sentence":"with the delay, what time will we arrive at the destiniation?"})
        trainingData.append({"class":"Model", "sentence":"how often is the train late"})
        trainingData.append({"class":"Model", "sentence":"how often is the train late from Norwich to Colchester"})
        trainingData.append({"class":"Model", "sentence":"how often is the train late from Norwich to Colchester at 12:00 pm "})
        trainingData.append({"class":"Model", "sentence":"how often is the train late from Norwich to Kilburn High Road"})
        trainingData.append({"class":"Model", "sentence":"how often is the train late from Norwich to Johnston (Pembs)"})
        trainingData.append({"class":"Model", "sentence":"how often is the train late from Hertford East to Hertford North"})
        trainingData.append({"class":"Model", "sentence":"how often is the train late at 1:00 pm from Norwich"})
        trainingData.append({"class":"Model", "sentence":"how often is the train late at 3:00 pm from Colchester"})
        trainingData.append({"class":"Model", "sentence":"how often is the train late at Colchester"})
        trainingData.append({"class":"Model", "sentence":"how often is the train late at Hinchley Wood"})

        print ("%s sentences of training data" % len(trainingData))
        # print(trainingData)
        # Create unique list
        classes = list(set([a['class'] for a in trainingData]))
        for c in classes:
            # dict of class types
            self.classifyText[c] = []

        # remove stopwords
        for word in trainingData:      
            if word in stopwords.words(self.language):
                trainingData.remove(word)
        # loop through each sentence in our training data
        for data in trainingData:
            for word in nltk.word_tokenize(data['sentence']):
                # remove stopwords and punctuation
                if word not in ["?", "'s","!",",","a", "i", "it", "am", "at", "on", "in", "to", "too", "very", 
                    "of", "from", "here", "even", "the", "but", "and", "is", "my", 
                    "them", "then", "this", "that", "than", "though", "so", "are"]:
                    # stem and lowercase each word
                    word = self.stemmer.stem(word.lower())
                    #print(word)
                    
                    if word not in self.bagOfWords:
                        self.bagOfWords[word] = 1
                    else:
                        self.bagOfWords[word] += 1
                    self.classifyText[data['class']].extend([word])
                    #print(self.bagOfWords)

    '''
    calculate a score for a given class
    '''
    def calculateClassValue(self, sentence, class_name, show_details=True):
        score = 0
        # tokenize each word in our new sentence
        for word in nltk.word_tokenize(sentence):
            # check to see if the stem of the word is in any of our classes
            if self.stemmer.stem(word.lower()) in self.classifyText[class_name]:
                # treat each word with same weight
                score += 1
                
                if show_details:
                    print ("   match: %s" % self.stemmer.stem(word.lower() ))
        return score


    '''
    calculate a score for a given class taking into account word commonality
    '''
    def calculateCommonValues(self, sentence, class_name, show_details=True):
        score = 0
        stemmer = PorterStemmer()
        # tokenize each word in our new sentence
        for word in nltk.word_tokenize(sentence):
            # check to see if the stem of the word is in any of our classes
            if stemmer.stem(word.lower()) in self.classifyText[class_name]:
                # treat each word with relative weight
                score += (1 / self.bagOfWords[stemmer.stem(word.lower())])

                if show_details:
                    print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / self.bagOfWords[stemmer.stem(word.lower())]))
        return score

    '''
    Testing contents of the bag of words, classifier types and ground truth classification test 
    '''
    def testClassifier(self):

        # print out the bag of words
        print ("Bag of words: %s \n" % self.bagOfWords)
        # print out the model
        print ("Classify the text : %s" % self.classifyText)
        
        # simple classifier test
        sentence = "plane train car"
        for c in self.classifyText.keys():
            print ("Class: %s  Score: %s \n" % (c,  self.calculateCommonValues(sentence, c)))

    '''
    Define the sentence type by scoring using knn
    '''
    def classify(self,sentence):
        print("classifying")
        self.train()
        maxClassification = None
        maxValue = 0
        for c in self.classifyText.keys():
            score = self.calculateCommonValues(sentence, c, show_details=False)
            
            if score > maxValue:
                maxClassification = c
                maxValue = score

        return maxClassification, maxValue

   
    

def main():
    print("test") 
    v = bot.classify("i would like to book a return ticket")
    print("book a ticket "+ str(v))
    
    p = bot.classify("fly plane")
    print("plane: "+ str(p))
    bot.testClassifier()
if __name__ == "__main__":
    bot = BotClassifier()
    main()