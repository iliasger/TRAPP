import sumolib
import random

from app import Config
from app.routing.RoutingEdge import RoutingEdge

import os, sys

# import of SUMO_HOME
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


class Network(object):
    """ simply ready the network in its raw form and creates a router on this network """

    # empty references to start with
    edges = None
    nodes = None
    nodeIds = None
    edgeIds = None
    routingEdges = None

    @classmethod
    def loadNetwork(cls):
        """ loads the network and applies the results to the Network static class """
        # parse the net using sumolib
        parsedNetwork = sumolib.net.readNet(Config.sumoNet)
        # apply parsing to the network
        Network.__applyNetwork(parsedNetwork)

    @classmethod
    def __applyNetwork(cls, net):
        """ internal method for applying the values of a SUMO map """
        cls.nodeIds = map(lambda x: x.getID(), net.getNodes())  # type: list[str]
        cls.edgeIds = map(lambda x: x.getID(), net.getEdges())  # type: list[str]
        cls.nodes = net.getNodes()
        cls.edges = net.getEdges()
        cls.routingEdges = map(lambda x: RoutingEdge(x), net.getEdges())
        cls.getNeighboringLanes = net.getNeighboringLanes
        cls.getNeighboringEdges = net.getNeighboringEdges
        # Below two arrays are used to hold node ids which are used for traffic flow from source to target ids
        if Config.restrictTrafficFlow == True:
            s, t = Config.trafficSource, Config.trafficTarget
            cls.sourceNodeIds = map(lambda x : Network.getEdgeIDsToNode(x[0].getID()).getID(), Network.getEdgeFromPosition(s[0], s[1], s[2]))
            cls.targetNodeIds = map(lambda x : Network.getEdgeIDsToNode(x[0].getID()).getID(), Network.getEdgeFromPosition(t[0], t[1], t[2]))

    @classmethod
    def nodesCount(cls):
        """ count the nodes """
        return len(cls.nodes)

    @classmethod
    def edgesCount(cls):
        """ count the edges """
        return len(cls.edges)

    @classmethod
    def getEdgeFromNode(cls, edge):
        return edge.getFromNode()

    @classmethod
    def getEdgeByID(cls, edgeID):
        return [x for x in cls.edges if x.getID() == edgeID][0]

    @classmethod
    def getEdgeIDsToNode(cls, edgeID):
        return cls.getEdgeByID(edgeID).getToNode()

    # returns the edge position of an edge
    @classmethod
    def getPositionOfEdge(cls, edge):
        return edge.getFromNode().getCoord()  # @todo average two

    # get edge from x and y cordinates of the map
    @classmethod
    def getEdgeFromPosition(cls, x, y, r):
        return cls.getNeighboringEdges(x, y, r)

    # this method was created to generate source and target of the cars 
    # that will be from the pool or nodes at one side of the map to the
    # other side of the map.
    # i.e can be used to make the flow of traffic from one area to the other area in the map
    @classmethod
    def getDefinedSourceTargetNodeIds(cls):
        return random.choice(cls.sourceNodeIds), random.choice(cls.targetNodeIds)