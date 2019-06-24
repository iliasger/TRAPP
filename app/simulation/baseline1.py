# Baseline 1 is for no collision occour at 600th tick to 1200 ticks out of total 2000 ticks

import json
import traci
import traci.constants as tc
from app.network.Network import Network
#from app.catastrophe.Accident import Accident
from app.catastrophe.Accident import getAccidentInstance

from colorama import Fore

from app import Config
from app.entity.CarRegistry import CarRegistry
from app.logging import info
from app.routing.CustomRouter import CustomRouter
import time

from app.logging import CSVLogger

from app.Util import remove_overhead_and_streets_files, prepare_epos_input_data_folders, add_data_folder_if_missing
from app.adaptation import perform_adaptation
from app.adaptation import Knowledge

current_milli_time = lambda: int(round(time.time() * 1000))


class Simulation(object):
    """ here we run the simulation in """

    # the current tick of the simulation
    tick = 0

    # last tick time
    lastTick = current_milli_time()

    @classmethod
    def applyFileConfig(cls):
        """ reads configs from a json and applies it at realtime to the simulation """
        try:
            config = json.load(open('./knobs.json'))
            CustomRouter.explorationPercentage = config['explorationPercentage']
            CustomRouter.averageEdgeDurationFactor = config['averageEdgeDurationFactor']
            CustomRouter.maxSpeedAndLengthFactor = config['maxSpeedAndLengthFactor']
            CustomRouter.freshnessUpdateFactor = config['freshnessUpdateFactor']
            CustomRouter.freshnessCutOffValue = config['freshnessCutOffValue']
            CustomRouter.reRouteEveryTicks = config['reRouteEveryTicks']
        except:
            pass

    @classmethod
    def start(cls):
 
        print ("RUNNING SIMULATION: BASELINE 1")
        remove_overhead_and_streets_files()
        add_data_folder_if_missing()

        CSVLogger.logEvent("streets", [edge.id for edge in Network.routingEdges])

        prepare_epos_input_data_folders()

        #---------------------------------------
        # get edges and set speed to 0.1
        # Changing the lane and edge speed did not work
        # nearedges = Network.getEdgeFromPosition(2314.92, 1161.52, 4)
        # edge1 = nearedges[0][0]
        # edge2 = nearedges[1][0]
        # edge1._speed = 0.1
        # edge2._speed = 0.1
        # lanes1 = edge1.getLanes()
        # lanes2 = edge2.getLanes()
        # for lane in lanes1:
        #     lane._speed = 0.1
        # for lane in lanes2:
        #     lane._speed = 0.1
        #---------------------------------------
        # blockedge = Network.getEdgeByID("-2788#0")
        # blocklanes = blockedge.getLanes()
        # blocklane1 = blocklanes[0]
        # blocklane2 = blocklanes[1]
        # blockedge._speed = 0.1
        # blocklane1.setParam("maxspeed", 0.1)
        # blocklane2.setParam("shoaib", 0.1)
        #-----------------------------------------
        # this works
        #traci.lane.setMaxSpeed("-2788#0_0", 0.1)
        #traci.lane.setMaxSpeed("-2788#0_1", 0.1)

        #traci.lane.setParameter("-2788#0_0", "allowed vehicle class", "authority")

        #Accident.subscribeToAccident(Accident())
        accident = getAccidentInstance()
        x = lambda a : a
        accident.subscribe(cls.printAccident)
        accident.blockLane("-2788#0_0")
        accident.blockLane("-2788#0_1")
        accident.fire(blocked="true")
        #Accident.blockLane("-2788#0_0")
        #Accident.blockLane("-2788#0_1")

        """ start the simulation """
        info("# Start adding initial cars to the simulation", Fore.MAGENTA)
        # apply the configuration from the json file
        cls.applyFileConfig()
        CarRegistry.applyCarCounter()

        cls.loop()

    @classmethod
    def printAccident(cls, event):
        print(event)
        print(event.blocked)

    @classmethod
    # @profile
    def loop(cls):
        """ loops the simulation """

        # start listening to all cars that arrived at their target
        traci.simulation.subscribe((tc.VAR_ARRIVED_VEHICLES_IDS,))
        while 1:

            if len(CarRegistry.cars) == 0:
                print("all cars reached their destinations")
                return

            # Do one simulation step
            cls.tick += 1
            traci.simulationStep()

            # Check for removed cars and re-add them into the system        122 is the VAR_ARRIVED_VEHICLES_IDS in traci constants
            for removedCarId in traci.simulation.getSubscriptionResults()[122]:
                if Config.debug:
                    print str(removedCarId) + "\treached its destination at tick " + str(cls.tick)
                CarRegistry.findById(removedCarId).setArrived(cls.tick)

            CSVLogger.logEvent("streets", [cls.tick] + [traci.edge.getLastStepVehicleNumber(edge.id)*CarRegistry.vehicle_length / edge.length for edge in Network.routingEdges])

            # print status update if we are not running in parallel mode
            if (cls.tick % 100) == 0:
                print("Simulation -> Step:" + str(cls.tick) + " # Driving cars: " + str(
                    traci.vehicle.getIDCount()) + "/" + str(
                    CarRegistry.totalCarCounter) + " # avgTripOverhead: " + str(
                    CarRegistry.totalTripOverheadAverage))

            if Config.simulation_horizon == cls.tick:
                print("Simulation horizon reached!")
                return

            # if (cls.tick % Config.adaptation_period) == 0:
            #     perform_adaptation(cls.tick)

            # if (cls.tick % Knowledge.planning_period) == 0:
            #     CarRegistry.do_epos_planning(cls.tick)

            if (cls.tick % 100) == 0:
                nearedges2 = Network.getEdgeFromPosition(2314.92, 1161.52, 4)
                #Accident.openlane('-2788#0_0')
                #Accident.openlane('-2788#0_1')
                accident = getAccidentInstance()
                accident.openlane('-2788#0_0')
                accident.openlane('-2788#0_1')
                accident.fire(blocked='closed')
                