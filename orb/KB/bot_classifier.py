# use natural language toolkit
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
# word stemmer
stemmer = LancasterStemmer()

# 3 classes of training data
trainingData = []
        
trainingData.append({"class":"General", "sentence":"how are you?"})
trainingData.append({"class":"General", "sentence":"how is your day?"})
trainingData.append({"class":"General", "sentence":"good day"})
trainingData.append({"class":"General", "sentence":"how is it going today?"})
trainingData.append({"class":"General", "sentence":"what day is it?"})
trainingData.append({"class":"General", "sentence":"hello"})
trainingData.append({"class":"General", "sentence":"i'm hungry"})
trainingData.append({"class":"General", "sentence":"what time is it?"})

trainingData.append({"class":"Booking", "sentence":"i want to book a train to london"})
trainingData.append({"class":"Booking", "sentence":"i want three tickets"})
trainingData.append({"class":"Booking", "sentence":"from norwich"})
trainingData.append({"class":"Booking", "sentence":"i need to book a train at 7pm"})
trainingData.append({"class":"Booking", "sentence":"i need to book a return train at 3pm"})
trainingData.append({"class":"Booking", "sentence":"i need to book a return train at 3pm"})
trainingData.append({"class":"Booking", "sentence":"hello Orb, i want to book a train"})
trainingData.append({"class":"Booking", "sentence":"book a journey for april!"})
trainingData.append({"class":"Booking", "sentence":"i need to book a return train at 3pm"})

trainingData.append({"class":"Model", "sentence":"how often is the train late"})
trainingData.append({"class":"Model", "sentence":"how long will my delay be?"})
trainingData.append({"class":"Model", "sentence":"is the train late?"})
trainingData.append({"class":"Model", "sentence":"with the delay, what time will we arrive at the destiniation?"})
print ("%s sentences of training data" % len(trainingData))

# capture unique stemmed words in the training corpus
corpus_words = {}
class_words = {}
# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = list(set([a['class'] for a in trainingData]))
for c in classes:
    # prepare a list of words within each class
    class_words[c] = []

# loop through each sentence in our training data
for data in trainingData:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a some things
        if word not in ["?", "'s"]:
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1

            # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])

# we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
print ("Corpus words and counts: %s \n" % corpus_words)
# also we have all words in each class
print ("Class words: %s" % class_words)

# we can now calculate a score for a new sentence
sentence = "good day for us to have lunch?"

# calculate a score for a given class
def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with same weight
            score += 1
            
            if show_details:
                print ("   match: %s" % stemmer.stem(word.lower() ))
    return score

# now we can find the class with the highest score
for c in class_words.keys():
    print ("Class: %s  Score: %s \n" % (c, calculate_class_score(sentence, c)))

# calculate a score for a given class taking into account word commonality
def calculate_class_score_commonality(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])

            if show_details:
                print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score

# now we can find the class with the highest score
for c in class_words.keys():
    print ("Class: %s  Score: %s \n" % (c, calculate_class_score_commonality(sentence, c)))

# return the class with highest score for sentence
def classify(sentence):
    print("classifying")
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score_commonality(sentence, c, show_details=False)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score

    return high_class, high_score




v = classify("i would like to book a return ticket")
print("book a ticket "+ str(v))

p = classify("fly plane")
print("plane: "+ str(p))