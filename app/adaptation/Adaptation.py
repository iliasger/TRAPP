from numpy import mean, var
from collections import OrderedDict
from app.adaptation import Knowledge
from app.network.Network import Network
import csv


class Adaptation(object):

    overheads_index = 0
    streets_index = 0

    @classmethod
    def sense_and_adapt(cls, tick):

        trip_overheads = cls.__calculate_trip_overheads()
        street_utilizations = cls.__calculate_street_utilizations()
        print "*******************"
        print "MONITOR"
        print "*******************"
        print "Adaptation triggered at tick " + str(tick)
        print "Average trip overhead: " + str(mean(trip_overheads))
        print "Average street utilization: " + str(mean(street_utilizations.values()))
        print "Variance of street utilization: " + str(var(street_utilizations.values()))

        print "*******************"
        print "ANALYSIS"
        print "*******************"
        print "placeholder"

        print "*******************"
        print "PLANNING"
        print "*******************"
        print "placeholder"

        print "*******************"
        print "EXECUTION"
        print "*******************"


        sorted_street_utilizations = OrderedDict(sorted(street_utilizations.iteritems(), key=lambda (k,v): (v,k), reverse=True))
        print sorted_street_utilizations.keys()[0]
        print sorted_street_utilizations.values()[0]
        cls.__apply_avoid_streets_signal(sorted_street_utilizations.keys()[0])

        # Knowledge.planning_steps = 4
        # Knowledge.beta = 1
        # print "Changing planning steps to: " + str(Knowledge.planning_steps)
        print "*******************"


    @classmethod
    def __calculate_trip_overheads(cls):
        trip_overheads = []
        with open("data/overheads.csv", 'r') as results:
            for i, line in enumerate(results):
                if i >= cls.overheads_index:
                    trip_overheads.append(float(line.split(",")[6]))

            overheads_index_increment = len(trip_overheads)
            cls.overheads_index += overheads_index_increment
        return trip_overheads

    @classmethod
    def __calculate_street_utilizations(cls):
        utilizations = []
        with open("data/streets.csv", 'r') as results:
            for i, line in enumerate(results):
                line = line.split(",")
                line[len(line)-1] = line[len(line)-1].replace('\r', '').replace('\n', '')
                if i == 0:
                    streets = line
                else:
                    if i > cls.streets_index:
                        utilizations.append([float(u) for u in line[1:]])
            streets_index_increment = len(utilizations)
            cls.streets_index += streets_index_increment

        streets_data = {}
        for i in range(len(streets)):
            streets_data[streets[i]] = [utilization[i] for utilization in utilizations]

        streets_utilizations = {}
        for key, value in streets_data.iteritems():
            streets_utilizations[key] = mean(value)

        return streets_utilizations


    @classmethod
    def __apply_avoid_streets_signal(cls, edges_to_avoid):
        avoid_streets_signal = []
        for i in range(Knowledge.planning_steps):
            avoid_streets_signal += [0 if edge.id in edges_to_avoid else 1 for edge in Network.routingEdges]

        with open('datasets/plans/signal.target', 'w') as signal_fil:
            signal_writer = csv.writer(signal_fil, dialect='excel')
            signal_writer.writerow(avoid_streets_signal)

        Knowledge.globalCostFunction = "XCORR"