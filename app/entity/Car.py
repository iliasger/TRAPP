import random
import traci
import traci.constants as tc
import csv

from app.Util import addToAverage
from app.logging import CSVLogger
from app.network.Network import Network
from app.routing.CustomRouter import CustomRouter
from app.routing.RouterResult import RouterResult
from app.adaptation import Knowledge
from app.entity.CarHistory import history_prefs
from app import Config

class Car:
    """ a abstract class of something that is driving around in the streets """

    preferences_list= ["min_length", "max_speed", "balanced"]

    def __init__(self, id):
        # the string id
        self.id = id  # type: str
        # the rounds this car already drove
        self.rounds = 0  # type: int
        # the current route as a RouterResult
        self.currentRouterResult = None  # type: RouterResult
        # when we started the route
        self.currentRouteBeginTick = None
        # the id of the current route (somu)
        self.currentRouteID = None  # type: str
        # the id of the current edge/street the car is driving (sumo)
        self.currentEdgeID = None
        # the tick this car got on this edge/street
        self.currentEdgeBeginTick = None
        # the target node this car drives to
        self.targetID = None
        # the source node this car is coming from
        self.sourceID = None
        # if it is disabled, it will stop driving
        self.disabled = False
        # the cars acceleration in the simulation
        self.acceleration = max(1, random.gauss(4, 2))
        # the cars deceleration in the simulation
        self.deceleration = max(1, random.gauss(6, 2))
        # the driver imperfection in handling the car
        self.imperfection = min(0.9, max(0.1, random.gauss(0.5, 0.5)))
        # is this car a smart car
        self.smartCar = True
        # number of ticks since last reroute / arrival
        self.lastRerouteCounter = 0

        preferences_options = ["balanced", "max_speed", "min_length"]
        if Config.do_baseline_run:
            self.driver_preference = random.choice(preferences_options)
        else:
            self.driver_preference = [key for key, value in sorted(history_prefs[self.id].iteritems(), key=lambda (k,v): (v,k))][0]

    def setArrived(self, tick):
        """ car arrived at its target, so we add some statistic data """

        # import here because python can not handle circular-dependencies
        from app.entity.CarRegistry import CarRegistry

        self.lastRerouteCounter = 0
        if self.smartCar:  # as we ignore the first 1000 ticks for this
            # add a route to the global registry
            CarRegistry.totalTrips += 1
            # add the duration for this route to the global tripAverage
            durationForTrip = (tick - self.currentRouteBeginTick)
            CarRegistry.totalTripAverage = addToAverage(CarRegistry.totalTrips,  # 100 for faster updates
                                                        CarRegistry.totalTripAverage,
                                                        durationForTrip)

            minimalCosts = CustomRouter.minimalRoute(self.sourceID, self.targetID).totalCost
            tripOverhead = durationForTrip / minimalCosts / 1.1  # 1.6 is to correct acceleration and deceleration
            # when the distance is very short, we have no overhead
            if durationForTrip < 10:
                tripOverhead = 1
            # in rare cases a trip does take very long - as most outliers are <30, we cap the overhead to 30 here
            if tripOverhead > 30:
                print("-> capped overhead to 30 - " + str(minimalCosts) + " - " + str(durationForTrip) + " - " + str(
                    tripOverhead))
                tripOverhead = 30

            CarRegistry.totalTripOverheadAverage = addToAverage(CarRegistry.totalTrips,
                                                                CarRegistry.totalTripOverheadAverage,
                                                                tripOverhead)

            overheads_file_name = "overheads_" + str(Config.beta) + "-" + str(Config.random_seed)
            if Config.log_overheads:
                CSVLogger.logEvent(overheads_file_name, [tick, self.sourceID, self.targetID, self.rounds, durationForTrip,
                                            minimalCosts, tripOverhead, self.id, self.driver_preference])

            if Config.do_baseline_run:
                CSVLogger.log_baseline_result("overheads", [tick, self.sourceID, self.targetID, self.rounds, durationForTrip,
                                             minimalCosts, tripOverhead, self.id, self.driver_preference])

        # if car is still enabled, restart it in the simulation
        if Config.multiple_car_routes and self.disabled is False:
            # add a round to the car
            self.rounds += 1
            self.addToSimulation(tick, False)

    def __createNewRoute(self, tick):
        """ creates a new route to a random target and uploads this route to SUMO """
        if self.targetID is None:
            self.sourceID = Network.get_random_node_id_of_passenger_edge(random)
        else:
            self.sourceID = self.targetID  # We start where we stopped
        self.targetID = Network.get_random_node_id_of_passenger_edge(random)
        self.currentRouteID = self.id + "-" + str(self.rounds)

        try:
            if self.driver_preference=="min_length":
                self.currentRouterResult = CustomRouter.route_by_min_length(self.sourceID, self.targetID)
            elif self.driver_preference=="max_speed":
                self.currentRouterResult = CustomRouter.route_by_max_speed(self.sourceID, self.targetID)
            else:
                self.currentRouterResult = CustomRouter.minimalRoute(self.sourceID, self.targetID)

            if len(self.currentRouterResult.route) > 0:
                traci.route.add(self.currentRouteID, self.currentRouterResult.route)
                return self.currentRouteID
            else:
                if Config.debug:
                    print "vehicle " + str(self.id) + " could not be added, retrying"
                return self.__createNewRoute(tick)

        except:
            if Config.debug:
                print "vehicle " + str(self.id) + " could not be added [exception], retrying"
            return self.__createNewRoute(tick)

    def create_epos_output_files_based_on_current_location(self, tick, agent_ind):
        route = traci.vehicle.getRoute(self.id)
        route_index = traci.vehicle.getRouteIndex(self.id)
        if route_index < 0:
            if Config.debug:
                print self.id + "\thas not yet started its trip and won't be considered in the optimization."
            return False
        previousEdgeID = route[route_index]
        previousNodeID = Network.getEdgeIDsToNode(previousEdgeID).getID()

        if previousNodeID == self.targetID:
            if Config.debug:
                print self.id + "\tis already reaching its destination and won't be considered in the optimization."
            return False

        self.create_epos_output_files(previousNodeID, self.targetID, tick, agent_ind)
        return True

    def create_epos_output_files(self, sourceID, targetID, tick, agent_ind):

        router_res_length = CustomRouter.route_by_min_length(sourceID, targetID)
        if len(router_res_length.route) > 0:
            self.create_output_files(
                history_prefs[self.id]["min_length"],
                router_res_length.route,
                self.find_occupancy_for_route(router_res_length.meta),
                agent_ind)

        router_res_speeds = CustomRouter.route_by_max_speed(sourceID, targetID)
        if len(router_res_speeds.route) > 0:
            self.create_output_files(
                history_prefs[self.id]["max_speed"],
                router_res_speeds.route,
                self.find_occupancy_for_route(router_res_speeds.meta),
                agent_ind)

        router_res_length_and_speeds = CustomRouter.minimalRoute(sourceID, targetID)
        if len(router_res_length_and_speeds.route) > 0:
            self.create_output_files(
                history_prefs[self.id]["balanced"],
                router_res_length_and_speeds.route,
                self.find_occupancy_for_route(router_res_length_and_speeds.meta),
                agent_ind)

    def create_output_files(self, cost, route, all_routes, agent_ind):

        with open('datasets/plans/agent_' + agent_ind + '.plans', 'ab') as plans_file, \
                open('datasets/routes/agent_' + agent_ind + '.routes', 'ab') as routes_file:

            plans_writer = csv.writer(plans_file, dialect='excel')
            routes_writer = csv.writer(routes_file, dialect='excel')
            routes_writer.writerow(route)

            plans_file.write(str(cost) + ":")
            big_row = []

            for i in range(Knowledge.planning_steps):
                if i< len(all_routes):
                    d = all_routes[i]
                    # print [edge.id for edge in Network.routingEdges]
                    big_row += [d[edge.id] if edge.id in d else 0 for edge in Network.routingEdges]
                else:
                    big_row += [0 for edge in Network.routingEdges]

            plans_writer.writerow(big_row)

    def change_route(self, new_route, first_invocation):
        if first_invocation:
            self.currentRouterResult.route = new_route
            traci.vehicle.setRoute(self.id, self.currentRouterResult.route)
        else:
            currentEdgeID = traci.vehicle.getRoadID(self.id)
            if currentEdgeID not in Network.edgeIds:
                currentEdgeID = traci.vehicle.getRoute(self.id)[traci.vehicle.getRouteIndex(self.id)]
            try:
                currentRoute = self.currentRouterResult.route

                self.currentRouterResult.route = new_route
                traci.vehicle.setRoute(self.id, [currentEdgeID] + self.currentRouterResult.route)
            except Exception as e:
                self.currentRouterResult.route = currentRoute
                if Config.debug:
                    print("error in changing route " + str(e))

    def change_preference(self, pref_id):
        self.driver_preference = Car.preferences_list[pref_id]

    def addToSimulation(self, tick, epos_prepare_inputs):
        """ adds this car to the simulation through the traci API """
        self.currentRouteBeginTick = tick
        try:
            traci.vehicle.add(self.id, self.__createNewRoute(tick))
            traci.vehicle.subscribe(self.id, (tc.VAR_ROAD_ID,))

            if Config.do_EPOS_planning and epos_prepare_inputs:
                agent_ind = self.id[self.id.find("-")+1:]
                self.create_epos_output_files(self.sourceID, self.targetID, tick, agent_ind)

        except Exception as e:
            print("error adding" + str(e))
            # try recursion, as this should normally work
            # self.addToSimulation(tick)


    def find_occupancy_for_route(self, meta):

        from app.entity.CarRegistry import CarRegistry

        interval = Knowledge.planning_step_horizon
        all_streets = []
        trip_time = 0
        checkpoint_index = 1
        streets_for_interval = {}
        all_streets.append(streets_for_interval)

        vehicle_length = CarRegistry.vehicle_length

        for m in meta:
            time =  m["length"]/ m["maxSpeed"]
            length = m["length"]

            trip_time += time
            next_checkpoint = interval * checkpoint_index

            if trip_time > next_checkpoint :
                surplus_time = trip_time - next_checkpoint
                checkpoint_index += 1
                time = time - surplus_time
                percentage = time/interval
                occupancy = vehicle_length*percentage/length
                if occupancy < 0:
                    raise RuntimeError

                streets_for_interval[m["edgeID"]] = occupancy

                while surplus_time > interval:
                    streets_for_interval = {}
                    all_streets.append(streets_for_interval)
                    occupancy = vehicle_length/length
                    if occupancy < 0:
                        raise RuntimeError
                    streets_for_interval[m["edgeID"]] = occupancy
                    surplus_time -= interval
                    checkpoint_index += 1

                streets_for_interval = {}
                all_streets.append(streets_for_interval)
                percentage_surplus = surplus_time/interval
                occupancy = vehicle_length*percentage_surplus/length
                if occupancy < 0:
                    raise RuntimeError
                streets_for_interval[m["edgeID"]] = occupancy

            else:
                percentage = time/interval
                occupancy = vehicle_length*percentage/length
                if occupancy < 0:
                    raise RuntimeError
                streets_for_interval[m["edgeID"]] = occupancy

        return all_streets

    def remove(self):
        """" removes this car from the sumo simulation through traci """
        traci.vehicle.remove(self.id)