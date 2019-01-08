import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
# conda install seaborn
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics


'''
A predictive model class using regression to predict the train delay. Uses supervised learning
The model takes in the know data (historical data), known outputs(delays) then generates the output model.
To reinforce the model delay calculations are also added in a naive implementation of the generated model.
'''
class TrainPredictive():
    def __init__(self):