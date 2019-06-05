from app import Boot
from app.Config import sumoUseGUI
from app.simulation.Simulation import Simulation
from app import Config

if __name__ == "__main__":

    Simulation.applySimulationConfigFromFile()
    Config.resultsFolder = "planning-horizon"

    betas = [0, 0.1, 1.0]

    for beta in betas:
        for random_seed in range(2):

            print "########################"
            print "########################"
            print "random_seed: " + str(random_seed)
            print "beta: " + str(beta)
            print "########################"
            print "########################"

            Simulation.customizeSimulationConfig(
                random_seed = random_seed,
                beta = beta
            )

            Boot.start(0, False, sumoUseGUI)

