import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
# conda install seaborn
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics
from sklearn import linear_model
import os


class RegressModel:

    mydataFame = pd.read_csv("orb/KB/thursday_delay_detail.csv", index_col=0)
    def __init__(self):
        
        self.mydataFrame= pd.read_csv("orb/KB/thursday_delay_detail.csv", index_col=0)
    '''
    Function to plot the csv data
    '''
    def plotData(data,self):
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

    def correlationFunc(data,self):
        print("The correlation between the data"+str(data.corr))
        data.corr()

 
    def get_delay_factor(self):
        print("regression starting")
        plt.style.use('classic')
        sns.set()
        sns.set_context('talk', font_scale=1.2)
        #delayData = pd.read_csv("orb/KB/thursday_delay_detail.csv", index_col=0)
        data = pd.read_csv("orb/KB/thursday_delay_detail.csv", index_col=0)
        print(data)
        data.head()
        data.info()
        data.describe()
        data.columns
        data.columns = ['Day','Time','delay']
        print('correleation data'+str(data.corr()))


        #t1='Time','delay'
        print("Plotting")
        sns.distplot(data['Time'])
        plotData(data)
        sns.pairplot(data,x_vars=['Time'],y_vars='delay',aspect=0.7,kind='reg')
        plt.legend()
        plt.show()
        correlationFunc(data)
        feature_cols = ['Time']
        X = data[feature_cols]

        X.head()

        y = data['delay']
        y = data.delay
        y.head()


        linreg = LinearRegression()
        linreg.fit(X, y)
        print('Coefficients: \n', linreg.coef_)
        mean_y =np.mean(y)

        # sm=np.sum((y-mean_y)**2)
        # smod = np.sum((y-linreg.predict(X)**2))
        # out =1- (sm/smod)

        # print ("out =" +str(out))
        print("regression score " +str(linreg.score(X,y)))
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
        # default split is 75% for training and 25% for testing


        # linreg = LinearRegression()

        # fit the model to the training data (learn the coefficients)
        linreg.fit(X_train, y_train)
        print("regression score " +str(linreg.score(X_train,y_train)))
        # print the intercept and coefficients
        print(linreg.intercept_)
        print("coef")
        print(linreg.coef_[0])
        slope = linreg.coef_
        print("Slope"+str(slope))
        predictions = linreg.predict(X)


        # value out
        print(metrics.mean_absolute_error(X_train, y_train))
        # pair the feature names with the coefficients
        v= list(zip(feature_cols, linreg.coef_))
        # print(v)
        # make predictions on the testing set
        y_pred = linreg.predict(X_test)
        true = [100, 50, 30, 20]
        pred = [90, 50, 50, 30]
        clf = linear_model.LinearRegression()
        clf.fit(X_train,y_train)
        # print(np.sqrt((10**2 + 0**2 + 20**2 + 10**2)/4.))

        # calculate RMSE using scikit-learn
        # print(np.sqrt(metrics.mean_squared_error(true, pred)))
        # print(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

        print (clf.coef_)
        print (clf.intercept_)
        
        return slope

def main():
    print("running regresiion model")

if __name__ == "__main__":
    calculation = RegressModel()
    calculation.get_delay_factor()
    a= RegressModel(mydataFrame)

    main()