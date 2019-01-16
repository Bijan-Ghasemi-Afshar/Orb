import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
# conda install seaborn
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics


plt.style.use('classic')
sns.set()
sns.set_context('talk', font_scale=1.2)
delayData = pd.read_csv('monday_delay_detail.csv', index_col=0)
data = pd.read_csv('monday_delay_detail.csv', index_col=0)
delayData.columns = ['Day','Time','delay']
delayData.head()
plt.plot(delayData.columns)
plt.show()
t1='Time','delay'
sns.pairplot(data,x_vars=['Time'],y_vars='delay',aspect=0.7,kind='reg')
plt.show()





# create a Python list of feature names
feature_cols = ['October','November','December']

# use the list to select a subset of the original DataFrame
X = data[feature_cols]

# equivalent command to do this in one line
#X = data['October','November','December']

# print the first 5 rows
X.head()
print(type(X))
print(X.shape)

y = data['delay']
y = data.delay
y.head()
print(y.head())
print(type(y))
print(y.shape)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
# default split is 75% for training and 25% for testing
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

# instantiate
linreg = LinearRegression()

# fit the model to the training data (learn the coefficients)
linreg.fit(X_train, y_train)

# print the intercept and coefficients
print(linreg.intercept_)
print(linreg.coef_)


# pair the feature names with the coefficients
v= list(zip(feature_cols, linreg.coef_))
print(v)
# make predictions on the testing set
y_pred = linreg.predict(X_test)
true = [100, 50, 30, 20]
pred = [90, 50, 50, 30]

print((10 + 0 + 20 + 10)/4.)
print(metrics.mean_absolute_error(true, pred))
print((10**2 + 0**2 + 20**2 + 10**2)/4.)
print(metrics.mean_squared_error(true, pred))
print(np.sqrt((10**2 + 0**2 + 20**2 + 10**2)/4.))

# calculate RMSE using scikit-learn
print(np.sqrt(metrics.mean_squared_error(true, pred)))
print(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
def test():
    rng = np.random.RandomState(0)
    x = np.linspace(0, 10, 500)
    y = np.cumsum(rng.randn(500, 6), 0)
    plt.plot(x, y, linewidth=2.0)
    plt.legend('ABCDEF', ncol=2, loc='upper left')
    plt.show()

def test2():
    # create a Python list of feature names
    feature_cols2 = ['October','November']

    # use the list to select a subset of the original DataFrame
    X = data[feature_cols2]
    y = data['delay']
    # select a Series from the DataFrame
    y = data.delay

    # split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    # fit the model to the training data (learn the coefficients)
    linreg.fit(X_train, y_train)

    # make predictions on the testing set
    y_pred = linreg.predict(X_test)

    # compute the RMSE of our predictions
    plt.plot(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    plt.show()
test2()