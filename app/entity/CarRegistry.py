import subprocess
from app import Config
import fileinput
import sys, os
from app.network.Network import Network

from app.entity.Car import Car
from app.Util import  prepare_epos_input_data_folders
from app.Util import get_output_folder_for_latest_EPOS_run
from app.adaptation import Knowledge

class NullCar:
    """ a car with no function used for error prevention """
    def __init__(self):
        pass

    def setArrived(self, tick):
        pass


class CarRegistry(object):
    """ central registry for all our cars we have in the sumo simulation """

    vehicle_length = 5
    # the total amount of cars that should be in the system
    totalCarCounter = Config.totalCarCounter
    # always increasing counter for carIDs
    carIndexCounter = 0
    # list of all cars
    cars = {}  # type: dict[str,app.entitiy.Car]
    # counts the number of finished trips
    totalTrips = 0
    # average of all trip durations
    totalTripAverage = 0
    # average of all trip overheads (overhead is TotalTicks/PredictedTicks)
    totalTripOverheadAverage = 0

    # @todo on shortest path possible -> minimal value

    @classmethod
    def applyCarCounter(cls):
        """ syncs the value of the carCounter to the SUMO simulation """
        while len(CarRegistry.cars) < cls.totalCarCounter:
            # to less cars -> add new
            c = Car("car-" + str(CarRegistry.carIndexCounter))
            cls.carIndexCounter += 1
            cls.cars[c.id] = c
            c.addToSimulation(0, True)
        while len(CarRegistry.cars) > cls.totalCarCounter:
            # to many cars -> remove cars
            (k, v) = CarRegistry.cars.popitem()
            v.remove()

    @classmethod
    def findById(cls, carID):
        """ returns a car by a given carID """
        try:
            return CarRegistry.cars[carID]  # type: app.entitiy.Car
        except:
            return NullCar()

    @classmethod
    def do_epos_planning(cls, tick):
        prepare_epos_input_data_folders()

        cars_to_indexes = {}
        i = 0
        for car_id, car in CarRegistry.cars.iteritems():
            if car.create_epos_output_files_based_on_current_location(tick, str(i)):
                cars_to_indexes[car_id] = i
                i += 1

        number_of_epos_plans = len([name for name in os.listdir('datasets/plans') if name.endswith("plans")])
        print "Number of EPOS plans: " + str(number_of_epos_plans)

        Knowledge.time_of_last_EPOS_invocation = tick
        
        cls.change_EPOS_config("conf/epos.properties", "numAgents=", "numAgents=" + str(number_of_epos_plans))
        cls.change_EPOS_config("conf/epos.properties", "planDim=", "planDim=" + str(Network.edgesCount() * Knowledge.planning_steps))
        cls.change_EPOS_config("conf/epos.properties", "alpha=", "alpha=" + str(Knowledge.alpha))
        cls.change_EPOS_config("conf/epos.properties", "beta=", "beta=" + str(Knowledge.beta))
        cls.change_EPOS_config("conf/epos.properties", "globalCostFunction=", "globalCostFunction=" + str(Knowledge.globalCostFunction))

        cls.run_epos_apply_results(False, cars_to_indexes, tick)

    @classmethod
    def run_epos_apply_results(cls, first_invocation, cars_to_indexes, tick):
        p = subprocess.Popen(["java", "-jar", Config.epos_jar_path])
        print "Invoking EPOS at tick " + str(tick)
        p.communicate()
        print "EPOS run completed!"
        cls.selectOptimalRoutes(get_output_folder_for_latest_EPOS_run(), first_invocation, cars_to_indexes)

    @classmethod
    def selectOptimalRoutes(cls, output_folder_for_latest_run, first_invocation, cars_to_indexes):

        with open(output_folder_for_latest_run + '/selected-plans.csv', 'r') as results:
            line_id = 1
            for line in results:
                if line_id == 41:
                    res = [int(x) for x in line.split(",")[2:]]
                    break
                line_id += 1

        i = 0
        for car_id, epos_id in cars_to_indexes.iteritems():
            c = cls.cars[car_id]
            with open('datasets/routes/agent_' + str(epos_id) + '.routes', 'r') as plans_file:
                plans=plans_file.readlines()
            if Config.debug:
                print "attempting to change the route of " + str(c.id)
            selected_route = plans[res[epos_id]].replace('\r', '').replace('\n', '').split(",")
            i += 1

            previous_preference = c.driver_preference
            previous_route = c.currentRouterResult.route
            c.change_route(selected_route, first_invocation)
            c.change_preference(res[epos_id])
            current_preference = c.driver_preference
            current_route = c.currentRouterResult.route
            if Config.debug:
                if previous_preference == current_preference:
                    print "preference did not change: " + str(previous_preference)
                else:
                    print "preference changed. Old preference: " + str(previous_preference) + ", New preference: " + str(current_preference)
                if set(current_route) <= set(previous_route):
                    print "route did not change"
                else:
                    print "route changed"

    @classmethod
    def change_EPOS_config(cls, filename, searchExp, replaceExp):
        for line in fileinput.input(filename, inplace=True):
            if searchExp in line:
                line = replaceExp + "\n"
            sys.stdout.write(line)