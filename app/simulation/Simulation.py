import json
import traci
import traci.constants as tc
from app.network.Network import Network

from colorama import Fore

from app import Config
from app.entity.CarRegistry import CarRegistry
from app.logging import info
from app.routing.CustomRouter import CustomRouter
import time

from app.logging import CSVLogger

import app.Util as Util
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
    def applySimulationConfigFromFile(cls):
        Knowledge.planning_period = Config.planning_period
        Knowledge.planning_step_horizon = Config.planning_step_horizon
        Knowledge.planning_steps = Config.planning_steps
        Knowledge.alpha = Config.alpha
        Knowledge.beta = Config.beta
        Knowledge.resultsFolder = Config.resultsFolder
        Knowledge.globalCostFunction = Config.globalCostFunction

    @classmethod
    def customizeSimulationConfig(cls, random_seed=None, simulation_horizon=None, adaptation_period=None,
                                  planning_period=None, planning_step_horizon=None, planning_steps=None,
                                  alpha=None, beta=None, globalCostFunction=None, log_baseline_result=None,
                                  log_overheads=None, log_utilizations=None, do_adaptation=None,
                                  do_EPOS_planning=None, multiple_car_routes=None
                                  ):
        if random_seed is not None:
            Config.random_seed = random_seed
        if simulation_horizon is not None:
            Config.simulation_horizon = simulation_horizon
        if adaptation_period is not None:
            Config.adaptation_period = adaptation_period
        if planning_period is not None:
            Knowledge.planning_period = planning_period
        if planning_step_horizon is not None:
            Knowledge.planning_step_horizon = planning_step_horizon
        if planning_steps is not None:
            Knowledge.planning_steps = planning_steps
        if alpha is not None:
            Knowledge.alpha = alpha
        if beta is not None:
            Knowledge.beta = beta
        if globalCostFunction is not None:
            Knowledge.globalCostFunction = globalCostFunction

        if log_baseline_result is not None:
            Config.log_baseline_result = log_baseline_result
        if log_overheads is not None:
            Config.log_overheads = log_overheads
        if log_utilizations is not None:
            Config.log_utilizations = log_utilizations
        if do_adaptation is not None:
            Config.do_adaptation = do_adaptation
        if do_EPOS_planning is not None:
            Config.do_EPOS_planning = do_EPOS_planning
        if multiple_car_routes is not None:
            Config.multiple_car_routes = multiple_car_routes

    @classmethod
    def start(cls):

        Util.remove_overhead_and_streets_files()
        Util.add_data_folder_if_missing()

        if Config.log_utilizations:
            CSVLogger.logEvent("streets", [edge.id for edge in Network.routingEdges])

        if Config.do_EPOS_planning:
            Util.prepare_epos_input_data_folders()

        """ start the simulation """
        info("# Start adding initial cars to the simulation", Fore.MAGENTA)
        # apply the configuration from the json file
        cls.applyFileConfig()
        CarRegistry.applyCarCounter()

        if Config.do_EPOS_planning and Config.start_with_epos_optimization:
            Knowledge.time_of_last_EPOS_invocation = 0
            CarRegistry.change_EPOS_config("conf/epos.properties", "numAgents=", "numAgents=" + str(Config.totalCarCounter))
            CarRegistry.change_EPOS_config("conf/epos.properties", "planDim=", "planDim=" + str(Network.edgesCount() * Knowledge.planning_steps))
            CarRegistry.change_EPOS_config("conf/epos.properties", "alpha=", "alpha=" + str(Knowledge.alpha))
            CarRegistry.change_EPOS_config("conf/epos.properties", "beta=", "beta=" + str(Knowledge.beta))
            CarRegistry.change_EPOS_config("conf/epos.properties", "globalCostFunction=", "globalCostFunction=" + str(Knowledge.globalCostFunction))

            cars_to_indexes = {}
            for i in range(Config.totalCarCounter):
                cars_to_indexes["car-" + str(i)] = i
            CarRegistry.run_epos_apply_results(True, cars_to_indexes, 0)

        cls.tick = 0
        cls.loop()

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

            # Check for removed cars and re-add them into the system
            for removedCarId in traci.simulation.getSubscriptionResults()[122]:
                if Config.debug:
                    print str(removedCarId) + "\treached its destination at tick " + str(cls.tick)
                CarRegistry.findById(removedCarId).setArrived(cls.tick)

            if Config.log_utilizations:
                CSVLogger.logEvent("streets", [cls.tick] + [traci.edge.getLastStepVehicleNumber(edge.id)*CarRegistry.vehicle_length / edge.length for edge in Network.routingEdges])

            current_car_count = traci.vehicle.getIDCount()
            if (cls.tick % 100) == 0:
                info("Simulation -> Step:" + str(cls.tick) +
                      " # Driving cars: " + str(current_car_count) + "/" + str(CarRegistry.totalCarCounter) +
                      " # avgTripOverhead: " + str(CarRegistry.totalTripOverheadAverage), Fore.GREEN)

            if Config.do_adaptation and (cls.tick % Config.adaptation_period) == 0:
                perform_adaptation(cls.tick)

            if Config.simulation_horizon == cls.tick:
                print("Simulation horizon reached!")
                return

            if not Config.multiple_car_routes and current_car_count == 0:
                print("All cars reached their destinations!")
                return

            if Config.do_EPOS_planning and (cls.tick % Knowledge.planning_period) == 0:
                CarRegistry.do_epos_planning(cls.tick)