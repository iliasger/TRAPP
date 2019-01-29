from app.adaptation.Strategy import Strategy
from app.adaptation.Util import *
from app.adaptation import Knowledge


class LoadBalancing(Strategy):

    def monitor(self):
        return Util.calculate_trip_overheads()

    def analyze(self, trip_overheads):
        return mean(trip_overheads)

    def plan(self, mean_overhead):
        if mean_overhead > 1.5:
            print "Mean overhead threshold reached!"
            return 0.5

    def execute(self, beta_value):
        print "Setting beta to " + str(beta_value)
        Knowledge.beta = beta_value
