from app.adaptation.Strategy import Strategy
from app.adaptation.Util import *
from app.adaptation import Knowledge
from numpy import mean
from app.Config import adaptation_period


class LoadBalancing(Strategy):

    def monitor(self):
        return Util.get_trip_overheads(Knowledge.time_of_last_adaptation, adaptation_period)

    def analyze(self, trip_overheads):
        mean_overhead = mean(trip_overheads)
        print "Mean overhead is: " +  str(mean_overhead)
        return mean_overhead

    def plan(self, mean_overhead):
        if mean_overhead > 1.2:
            print "Mean overhead threshold reached!"
            return 0.9
        else:
            print "Mean overhead is less than threshold, no action needed"

    def execute(self, beta_value):
        print "Setting beta to " + str(beta_value)
        Knowledge.beta = beta_value
