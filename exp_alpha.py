from app import Boot
from app.Config import sumoUseGUI
from app.simulation.Simulation import Simulation
from app import Config
from app.adaptation.strategies import Beta

#when running exp_beta or exp_alpha, add to the config file the resultFolder
# and when running this or exp_beta, Config.adaption_strategy can now be also alpha or beta
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
    Config.adaptation_strategy= "alpha"
    #change the name of the results subfolder depending on the cities
    Config.resultsFolder = "NewYorkTest"

    # real alphas that need to be used
    #alphas = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    #for shorter testing  period
    alphas = [0.0, 0.5, 1.0]

    for alpha in alphas:
        # change seed to 5 eventually
        for random_seed in range(2):

            print "########################"
            print "########################"
            print "random_seed: " + str(random_seed)
            print "alpha: " + str(alpha)
            print "########################"
            print "########################"

            Simulation.customizeSimulationConfig(
                random_seed = random_seed,
                alpha = alpha
            )

            #Beta.py can be used for generating alpha values as well
            instance = Beta(alpha)
            Beta.add_overhead_results_folder_if_missing(instance,"alpha")
            Boot.start(0, False, sumoUseGUI)
            Beta.new_file_for_const(instance, "alpha")



