import traci
import traci.constants as tc

class Accident(object):

    __allowedWhenBlocked = ['authority']
    __DisallowedWhenBlocked = ['private','emergency','army','vip','passenger','hov','taxi','bus','coach','delivery','truck','trailer','tram','rail_urban','rail','rail_electric','motorcycle','moped','bicycle','pedestrian','evehicle','ship','custom1','custom2']

    _roadBlocked = False
    _blockedLanes = list()
    
    @classmethod
    def getBlockedLanes(cls):
        return cls._blockedLanes

    @classmethod
    def getAccidentStatus(cls):
        return cls.roadBlocked

    @classmethod
    def blockLane(cls, lane):
        try:
            cls._blockedLanes.index(lane)
        except:
            cls._blockedLanes.append(lane)
            traci.lane.setAllowed(lane, cls.__allowedWhenBlocked)
            traci.lane.setDisallowed(lane, cls.__DisallowedWhenBlocked)
        else:
            print("Lane already blocked")

    @classmethod
    def openlane(cls, lane):
        try:
            cls._blockedLanes.remove(lane)
        except:
            print("Lane already open")
        else:
            traci.lane.setAllowed(lane, [])
            traci.lane.setDisallowed(lane, [])
