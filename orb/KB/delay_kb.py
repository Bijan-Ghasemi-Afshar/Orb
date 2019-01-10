'''
A predictive model that determines how late a train journey has been for given information.
Historical data assists the prediction values.
'''

'''
Class that asks the user for their route expected journey time and actual journey time based on know delays.
ask the user if their more than ONE delay, 
'''
class DelayModel():

    # orb ask to predict new arrival time based on delay
    # orb asks/ checks  how many delays (default 1)
    # orb asks expected arrival time
    # responds time
    # naive>orb return new arrival time based on math time+delay   class CalculateDelay() 
    # predictive> return new time based on math + predictive model class TrainPredictive()
    # advanced> orb retuns new arrival time based on DNN class TrainNN()

    # add provision for broken down train with UNKNOWN delay
    def __init__(self, user_input):
        self.user_input = user_input

    
        