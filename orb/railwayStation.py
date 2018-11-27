class TrainStation(object):


    def  __init__(self, station):
        self.station= station

    def getTrainStation(self):
        return self.station

    def setStationName(self, station):
        self.station= station

    def printStationName(self, station):
        return "the station is:"+station

my_stations = ["Acle","Alresford","Althorne","Angel Road","Attleborough",
               "Audley End","Battlesbridge","Beccles","Berney Arms","Billericay","Bishops Stortford","Braintree","Braintree Freeport",
               "Brampton","Brandon","Brentwood","Brimsdown","Broxbourne","Bruce Grove","Brundal Gardens","Brundall","Buckenham","Bures",
               "Burnham","Bury","Bush","Cambridge","Cantley","Chadwell Heath","Chappel & Wakes Colne",""]

for i in range(133):
    my_stations.append(TrainStation(i))

print(my_stations[:])