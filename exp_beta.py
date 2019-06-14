from app import Boot
from app.Config import sumoUseGUI
from app.simulation.Simulation import Simulation
from app import Config
from app.adaptation.strategies import Beta

#when running exp_beta or exp_alpha, add to the config file the resultFolder
# and when running this or exp_alpha, Config.adaption_strategy can now be also alpha or beta
# For running while testing large number of cars, large map, or a large planning horizon
# these are the suggested Config settings for optimal speed:
#   sumoUseGUI = False
#   debug = False
#   log_overheads = True
#   log_utilizations = False
#   log_baseline_result = False
#   do_adaptation = False
#   do_EPOS_planning = True
#   multiple_car_routes = False
#   start_with_epos_optimization = True

if __name__ == "__main__":

    Simulation.applySimulationConfigFromFile()
    Config.experiment_name = "beta"
    resultsFolder_name= "NewYorkTest"
    Config.resultsFolder = resultsFolder_name

    # real betas that need to be used
    #betas = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    #for shorter testing  period
    betas= [0.0, 0.5, 1.0]

    for beta in betas:
        # change seed to 5 eventually when running the real program
        for random_seed in range(2):

            print "########################"
            print "########################"
            print "random_seed: " + str(random_seed)
            print "beta: " + str(beta)
            print "########################"
            print "########################"

            Simulation.customizeSimulationConfig(
                random_seed = random_seed,
                beta = beta,
            )

            instance = Beta(beta)
            # creating output folders, if not there
            Beta.add_overhead_results_folder_if_missing(instance, "beta")
            # running the simulation, CSVlogger will log the overheads to results folders
            Boot.start(0, False, sumoUseGUI)
            # saving the local and global cost for each run to the results folder
            Beta.new_file_for_const(instance, "beta")



