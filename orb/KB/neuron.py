import numpy as np


'''
A basic 3 layer neural network to calculate train delays based on historical data.
Time:
station:
month:

This model could be greatly improved by adding more inputs such as;
weather: 
track repair work:
train capacity:
train engine performance (efficency):
route historical performance:
'''


'''
A single neuron blueprint
'''
class Neuron(object):
    def __init__(self):
        # seeding for random number generation
        np.random.seed(1)
        self.weights = 2 * np.random.random((3, 1)) - 1
    
    '''
    The sigmoid activation function, maps from 0-1
    '''
    def activation(self, input):
        return 1 / (1 + np.exp(-input))

    '''
    calculate the activation derivative
    '''
    def ActDerivative(self, input):
        return input * (1 - input)

    '''
    Train the model 
    '''
    def train(self, inputs, outputValue, iterations):
        for i in range(iterations):
            
            output = self.create(inputs)

            # error rate for back-propagation
            error = outputValue - output
            
            #adjust weights
            adjustments = np.dot(inputs.T, error * self.ActDerivative(output))

            self.weights += adjustments

    '''
    Create a network of neurons
    '''
    def create(self, inputs):
        
        inputs = inputs.astype(float)
        output = self.activation(np.dot(inputs, self.weights))
        return output

    '''
    Testing function
    '''
    def classify(self):
        print("classify neuron value")

    '''
    Feedforward into the network
    '''
    def feedforward(self, inputs):
        self.layer1 = self.activation(np.dot(inputs, self.weights))
        self.output = self.activation(np.dot(self.layer1, self.weights))


if __name__ == "__main__":

    #initializing a neuron
    NeuralNetwork = Neuron()

    print("Generation of weights: ")
    print(NeuralNetwork.weights)

    #fake data to demo model
    #training data consisting of 4 example inputs, 3 input values and 1 output
    inputs = np.array([[0,0,1],
                                [1,1,1],
                                [1,0,1],
                                [0,1,1]])

    outputValue = np.array([[0,1,1,0]]).T

    #training taking place
    NeuralNetwork.train(inputs, outputValue, 15000)

    print("Ending Weights After Training: ")
    print(NeuralNetwork.weights)

    # Here we model a station on a route
    inputOne = str(input("Percentage on time: "))
    inputTwo = str(input("percentage delay 5 mins: "))
    inputThree = str(input("percentage delay 10 minutes: "))
    #inputFour = str(input("percentage delay 30 minutes: "))
    #inputFive = str(input("percentage delay 1 hour: "))
    
    print("Considering New Situation: ", inputOne, inputTwo, inputThree)
    print("New Output data: ")
    print(NeuralNetwork.create(np.array([inputOne, inputTwo, inputThree])))
    print("finished")