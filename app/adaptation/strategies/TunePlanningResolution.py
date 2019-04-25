import matplotlib.pyplot as plt
from numpy import mean
from app.adaptation.Strategy import Strategy
from app.adaptation.Util import *
from app.adaptation import Knowledge
from app import Config
import csv
import collections
import os

class TunePlanningResolution(Strategy):

    def monitor(self):
        if Knowledge.time_of_last_EPOS_invocation > 0 or Config.start_with_epos_optimization:
            horizon = Knowledge.planning_step_horizon
            steps = Knowledge.planning_steps
            utilizations_in_adaptation_period, streets = \
                Util.get_street_utilizations(Knowledge.time_of_last_EPOS_invocation, Knowledge.planning_period)
            mean_utilizations_per_street_in_planning_steps = list()

            for i in range(steps):
                mean_utilizations_in_planning_step = dict()
                for key, value in utilizations_in_adaptation_period.iteritems():
                    slice = value[i*horizon:(i+1)*horizon]
                    if len(slice) > 0:
                        mean_utilizations_in_planning_step[key] = mean(slice)
                    else:
                        print("BREAK!")
                        break
                if mean_utilizations_in_planning_step:
                    mean_utilizations_per_street_in_planning_steps.append(mean_utilizations_in_planning_step)

            predicted_utilizations_per_street_in_planning_steps = \
                Util.get_predicted_street_utilization_in_latest_EPOS_run(steps, streets)

            return mean_utilizations_per_street_in_planning_steps, predicted_utilizations_per_street_in_planning_steps

        else:
            print "EPOS is not invoked yet, aborting"

    def analyze(self, monitor_data):
        mean_utilizations_per_street_in_planning_steps = monitor_data[0]
        predicted_utilizations_per_street_in_planning_steps = monitor_data[1]

        assert len(mean_utilizations_per_street_in_planning_steps) == 1
        assert len(predicted_utilizations_per_street_in_planning_steps) == 1
        self.__write_to_file("actual", mean_utilizations_per_street_in_planning_steps, self.tick)
        self.__write_to_file("predicted", predicted_utilizations_per_street_in_planning_steps, self.tick)

        return 0

        # errors_in_planning_steps = list()
        # for step_id in range(len(mean_utilizations_per_street_in_planning_steps)):
        #     errors_in_planning_step = dict()
        #     for street_id, mean_utilization in mean_utilizations_per_street_in_planning_steps[step_id].iteritems():
        #         errors_in_planning_step[street_id] = \
        #             mean_utilization - float(predicted_utilizations_per_street_in_planning_steps[step_id][street_id])
        #     errors_in_planning_steps.append(errors_in_planning_step)
        #
        # self.__write_to_file("errors", errors_in_planning_steps, self.tick)
        # self.__plot_utilization_errors(errors_in_planning_steps, self.tick)
        #
        # mean_errors = list()
        # for step_id in range(len(mean_utilizations_per_street_in_planning_steps)):
        #     mean_error = mean(errors_in_planning_steps[step_id].values())
        #     mean_errors.append(mean_error)
        #     print("Mean error in step " + str(step_id) + " is " + str(mean_error))
        #
        # return mean(mean_errors)

    def plan(self, mean_error_over_all_planning_periods):
        print("The mean error over all planning periods is " + str(mean_error_over_all_planning_periods))
        if mean_error_over_all_planning_periods > 100:
            print "Error threhold reached, triggering change in planning parameters"
            planning_conf = dict()
            planning_conf["period"] = 60
            planning_conf["steps"] = 3
            planning_conf["step_horizon"] = 20
            return planning_conf

    def execute(self, planning_conf):
        Knowledge.planning_period = planning_conf["period"]
        Knowledge.planning_steps = planning_conf["steps"]
        Knowledge.planning_step_horizon = planning_conf["step_horizon"]
        print "Setting planning period to " + str(planning_conf["period"])
        print "Setting planning steps to " + str(planning_conf["steps"])
        print "Setting planning step horizon to " + str(planning_conf["step_horizon"])

    def __plot_utilization_errors(self, errors_in_planning_steps, tick):
        plt.figure(tick)
        for step_id in range(len(errors_in_planning_steps)):
            plt.plot(errors_in_planning_steps[step_id].values(),label="errors in step " + str(step_id))
        plt.legend(loc='upper right')
        plt.xlabel("streets")
        plt.ylabel("utilization errors")
        plt.title('Errors in edge utilization at tick ' + str(tick) + " with seed " + str(Config.random_seed))

        # fig_title = "TunePlanningResolution-" + str(tick) + "-seed" + str(Config.random_seed)
        # fig_title = "TunePlanningResolution-" + str(Knowledge.planning_steps) + "-seed" + str(Config.random_seed)
        fig_title = "TunePlanningResolution-" + str(Knowledge.planning_period) + "-" + str(tick) + "-seed" + str(Config.random_seed)

        plt.savefig("figures/" + fig_title)
        plt.close()

        print("Figure " + fig_title + " generated!")

    def __write_to_file(self, case, list_of_lists, tick):

        results_folder = "results/"+ Config.resultsFolder
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        with open(results_folder + '/' + case + '_' +
                  str(Knowledge.planning_step_horizon) +
                  '-' + str(Knowledge.planning_steps) +
                  '-' + str(Knowledge.planning_period) +
                  '-' + str(Knowledge.alpha) +
                  '-' + str(Knowledge.beta) +
                  '-' + str(tick) +'.csv', 'ab') as results_file:

            results_writer = csv.writer(results_file, dialect='excel')
            for res in list_of_lists:
                od = collections.OrderedDict(sorted(res.items()))
                results_writer.writerow(od.keys())
                results_writer.writerow([float(v) for v in od.values()])