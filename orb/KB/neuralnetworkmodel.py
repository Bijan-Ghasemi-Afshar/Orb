from keras.models import Sequential
from keras.layers import Dense
import numpy
import matplotlib.pyplot as plt
import pandas as pd
from pandas import read_csv
from numpy import array
from keras.models import model_from_json
import math

'''
Neural network to predict train delays 


inputs:
train_no = train id(time +service type),
route_name = the name of the route,
departure_time = train left the initial station 00:00,
arrival_time = expected arrival time of train in 00:00,
train_service_type = local or intercity (0, 1),
distance= account for long trips  (0 <200 miles, 1>200 miles),
day_of_service = weekday value0-4 (0=monday - 4=friday),
total_delay = the daley time 0-maxdelay (3hours),
delay_flag = class value (0 = delay,1 = ontime)


v3 added serialization to the class so a model can be saved after training and reloaded
'''
class NeuralTrainNetwork:

    def __init__(self):
        self.seed = 0

    '''
    Neural network to predict train delays
    '''
    def trainNetwork(self):
        numpy.random.seed(7)
        # load dataset and trim 
        #trainData = pd.read_csv("neural_data.csv", index_col="item")
        #trainData.drop(["route_name"], axis = 1, inplace = True)
        #print(trainData)
        
        #load trimmed dataset
        dataset = numpy.loadtxt('orb/KB/neuralnetworkData.csv', delimiter=",")
        print(dataset)
        # split into input (X) and output (Y) variables
        X = dataset[:,0:8]
        Y = dataset[:,8]
        # create model
        model = Sequential()
        model.add(Dense(12, input_dim=8, activation='relu'))
        model.add(Dense(12, activation='relu'))
        model.add(Dense(8, activation='relu'))
        # output
        model.add(Dense(1, activation='sigmoid'))
        # Compile model
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        # Fit the model
        model.fit(X, Y, epochs=1500, batch_size=10)
        # evaluate the model
        scores = model.evaluate(X, Y)
        print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
        unknown = array([[1900,1900,2055,1,0,1,0,1]])
        newPrediction = model.predict(unknown)
        # show the inputs and predicted outputs
        print("X=%s, Predicted=%s" % (unknown[0], newPrediction[0]))
        return model

    '''
    Save a model in a file
    '''
    def saveModel(self,model):
        # serialize model to JSON
        trainNN = model.to_json()
        with open("neuralTrainModel.json", "w") as json_file:
            json_file.write(trainNN)
        # serialize weights to HDF5
        model.save_weights("model.h5")
        print("Saved model to file")

    '''
    Read in a json file
    '''
    def readModel(self):
        json_file = open('neuralTrainModel.json', 'r')
        loaded_trainNN = json_file.read()
        json_file.close()
        savedTrainModel = model_from_json(loaded_trainNN)
        # load weights into new model
        savedTrainModel.load_weights("model.h5")
        print("Loaded model from file")
        return savedTrainModel

    '''
    function to check datas accuracy
    '''
    def validateSavedModel(self,savedTrainModel):
        # evaluate loaded model on test data
        #print("validation of data")
        dataset = numpy.loadtxt('orb/KB/neuralnetworkData.csv', delimiter=",")
        X = dataset[:,0:8]
        Y = dataset[:,8]
        savedTrainModel.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        score = savedTrainModel.evaluate(X, Y, verbose=0)
        print("%s: %.2f%%" % (savedTrainModel.metrics_names[1], score[1]*100))

def main():
    print("Running neural network")
    model=network.trainNetwork()
    network.saveModel(model)
    savedTrainModel=network.readModel()
    network.validateSavedModel(savedTrainModel)

if __name__ == "__main__":
    network=NeuralTrainNetwork()
    main()

