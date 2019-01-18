import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics
from sklearn import linear_model
import os

'''
Class to determine the simple linear regression (estimate the relationships) between time and delay.
 A form of predictive analysis to aid model the train delays
'''
class RegressModel:

    date = 0
    regressionScore = 0
    coefficentScore = 0
    slope = 0

    def __init__(self):
        self.data = 0
        self.regressionScore = 0
        self.coefficentScore = 0
        self.slope = 0
        
    '''
    Function to plot the csv data
    '''
    def plotData(self,data):
        print("Plotting all the input csv data")
        sns.pairplot(data)
        plt.legend()
        plt.show()

    '''
    Function to find the system path if csv needs to have the path appended onto the file
    '''
    def checkPath(self):

        print(os.getcwd())
        print(os.listdir(os.getcwd()))

    '''
    Function for correlation data
    '''
    def correlationFunc(self,data):
        data.corr()
        print("The correlation between the data"+str(data.corr))

    '''
    Graphing function for the report
    '''
    def print(self,data):
        print("Printing the graphs")
        # print the raw data
        print(data)
        self.plotData(data)
        plt.style.use('classic')
        sns.pairplot(data,x_vars=['Time'],y_vars='delay',aspect=0.7,kind='reg')
        plt.title("Regression Graph of day")
        plt.legend(loc='upper left')
        plt.show()
    '''
    Validation of data using random samples. 
    '''
    def metricTests(self,data):
        print("Data validation tests")
        data.head()
        data.info()
        data.describe()
        data.columns
 
    '''
    The calculation and prediction function
    '''
    def get_delay_factor(self):
        print("regression starting")
        sns.set()
        sns.set_context('talk', font_scale=1.2)
        # read in the csv file
        data = pd.read_csv("orb/KB/thursday_delay_detail.csv", index_col=0)
        data.columns = ['Day','Time','delay']
        sns.distplot(data['Time'])
        feature_cols = ['Time']
        X = data[feature_cols] 
        y = data['delay']
        y = data.delay
        #create the regression object
        linreg = LinearRegression()
        linreg.fit(X, y)
        # hooks for future development
        mean_y =np.mean(y)
        regressionScore = linreg.score(X,y)

        # default split is 75% for training and 25% for testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
        # fit the model to the training data (learn the coefficients)
        linreg.fit(X_train, y_train)
        #print(linreg.intercept_)
        coefficentScore= linreg.coef_[0]
        slope = linreg.coef_
        #print("Slope"+str(slope))
        prediction = linreg.predict(X)
        #print("prediction",predictions)
        # value out
        print(metrics.mean_absolute_error(X_train, y_train))
        return slope

def main():
    print("running regresion model")

if __name__ == "__main__":
    calculation = RegressModel()
    calculation.get_delay_factor()

    main()