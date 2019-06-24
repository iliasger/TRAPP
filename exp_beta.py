from app import Boot
from app.Config import sumoUseGUI
from app.simulation.Simulation import Simulation
from app import Config
from app.adaptation.strategies import Beta

# README
# When running create a new Config.py, from the Config_TEMPLATE.py and do the TODOs
# When running with large number of cars, large map, or a large planning horizon
# these are the suggested Config settings for optimal speed:
#   sumoUseGUI = False
#   debug = False
#   log_overheads = True
#   log_utilizations = False
#   log_baseline_result = False
#   do_adaptation = False
#   do_EPOS_planning = True
#   # want this on to stimulate homogeneous traffic
#   multiple_car_routes = True
#   start_with_epos_optimization = True
#   do_gridding = False
#
# Before trying to run, make sure a TAZ file for the city exists
# If Taz file has not been created turn on:
# do_gridding = True (suggest grid size for large cities 3500)
# and then run run.py


if __name__ == "__main__":

    Simulation.applySimulationConfigFromFile()
    Config.experiment_name = "beta"
    # TODO
    # Name of the folder the results will be saved to,
    # Suggestion: naming folder same as the alpha results folder (when running exp_alpha.py)
    # and naming it the city name that you are testing
    resultsFolder_name= "NewYorkTest"
    Config.resultsFolder = resultsFolder_name

    # betas testing ( should run simulation 11 times)
    betas = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    #betas testing
    #betas = [0, 1.0]

    for beta in betas:
        # see of 5 for testing
        for random_seed in range(5):

            print "########################"
            print "########################"
            print "random_seed: " + str(random_seed)
            print "beta: " + str(beta)
            print "########################"
            print "########################"

            # Starting the application
            Simulation.applySimulationConfigFromFile()

            Simulation.customizeSimulationConfig(
                random_seed=random_seed,
                beta=beta,
                log_baseline_result=False,
                log_overheads=True,
                log_utilizations=False,
                do_adaptation=False,
                do_EPOS_planning=True,
                multiple_car_routes=True,
                start_with_epos_optimization=True,
                simulation_horizon=1800,
                planning_period=100000,
                planning_step_horizon=1800,

            )


            instance = Beta(beta)
            # creating output folders, if not there
            Beta.add_overhead_results_folder_if_missing(instance, "beta")
            # running the simulation, CSVlogger will log the overheads to results folders
            Boot.start(0, False, sumoUseGUI)
            # saving the local and global cost for each run to the results folder
            Beta.new_file_for_cost(instance, "beta")



