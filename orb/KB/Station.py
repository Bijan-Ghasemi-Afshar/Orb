
import sys
import csv



'''
Basic class to validate station lociation and destionation
'''
class Station:

    def __init__(self,station):
        self.__x = station

    def getStation(self):
        return self.__x

    def setStation(self, station):
        self.__x = station

    def printStation(self, station):
        print("The station is "+ station)

def ORB_station(station):
    print("ORB\n---------")
    print("Testing station validation")
    print("The station "+station)


def validation():
    station ="LONDON"
    station=station.lower()
    ORB_station(station)

if __name__ == "__main__":
    validation()
