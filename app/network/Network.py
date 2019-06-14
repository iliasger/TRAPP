import sumolib

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
    passenger_edges = None
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
        cls.edgeIds = map(lambda x: x.getID(), net.getEdges(withInternal=False))  # type: list[str]
        cls.nodes = net.getNodes()
        cls.edges = net.getEdges(withInternal=False)
        cls.passenger_edges = [e for e in net.getEdges(withInternal=False) if e.allows("passenger")]
        cls.routingEdges = map(lambda x: RoutingEdge(x), cls.passenger_edges)

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

    @classmethod
    def get_random_node_id_of_passenger_edge(cls, random):
        edge = random.choice(Network.passenger_edges)
        return edge.getFromNode().getID()