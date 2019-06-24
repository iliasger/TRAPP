# Holds the events and methods for Accidents to occour
# Author: Shoaib
# Date: 20 June 2019

import traci
import traci.constants as tc
import Observable as Observable

# singleton instance
# use one instance of the class Accident by always summoning 
# the object from `getAccidentInstance` function
_accidentInstance = None
def getAccidentInstance():
    global _accidentInstance
    if _accidentInstance is None:
        _accidentInstance = Accident()
    return _accidentInstance

# Inherits Observable superclass to hold the events for Accidents hapenning
# NOTE: Don't call or initialize this class directly rather use getAccidentInstance method

class Accident(Observable.Observable):

    # variables required to block and unblock lanes
    __allowedWhenBlocked = ['authority']
    __DisallowedWhenBlocked = ['private','emergency','army','vip','passenger','hov','taxi','bus','coach','delivery','truck','trailer','tram','rail_urban','rail','rail_electric','motorcycle','moped','bicycle','pedestrian','evehicle','ship','custom1','custom2']
    
    _blockedLanes = list()
    _roadBlocked = False

    def __init__(self):
        super(Accident, self).__init__()

    def getBlockedLanes(self):
        return self._blockedLanes

    def getAccidentStatus(self):
        return self._roadBlocked

    def blockLane(self, lane):
        try:
            self._blockedLanes.index(lane)
        except:
            self._blockedLanes.append(lane)
            traci.lane.setAllowed(lane, self.__allowedWhenBlocked)
            traci.lane.setDisallowed(lane, self.__DisallowedWhenBlocked)
            getAccidentInstance().fire(lane=lane, blocked=True)
        else:
            print("Lane already blocked")

    def openlane(self, lane):
        try:
            self._blockedLanes.remove(lane)
        except:
            print("Lane already open")
        else:
            traci.lane.setAllowed(lane, [])
            traci.lane.setDisallowed(lane, [])
            getAccidentInstance().fire(lane=lane, blocked=False)

    def setLaneMaxSpeed(self, lane, speed):
        traci.lane.setMaxSpeed(lane, speed)
