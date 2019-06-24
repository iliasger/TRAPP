import traci
import traci.constants as tc
import Observable as Observable

_accidentInstance = None
def getAccidentInstance():
    global _accidentInstance
    if _accidentInstance is None:
        _accidentInstance = Accident()
    return _accidentInstance


class Accident(Observable.Observable):
    def __init__(self):
        super(Accident, self).__init__()

    __allowedWhenBlocked = ['authority']
    __DisallowedWhenBlocked = ['private','emergency','army','vip','passenger','hov','taxi','bus','coach','delivery','truck','trailer','tram','rail_urban','rail','rail_electric','motorcycle','moped','bicycle','pedestrian','evehicle','ship','custom1','custom2']

    _roadBlocked = False
    _blockedLanes = list()
    
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
            #self.fire(Accident, type="Accident")
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
            #self.fire("XXX-Cleared-XXX")

    def setLaneMaxSpeed(self, lane, speed):
        traci.lane.setMaxSpeed(lane, speed)

    #@classmethod
    #def subscribeToAccident(self, callback): 
    #    self.subscribe(callback)