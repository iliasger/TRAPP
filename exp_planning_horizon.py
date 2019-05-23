from app import Boot
from app.Config import sumoUseGUI
from app.simulation.Simulation import Simulation
from app import Config

if __name__ == "__main__":

    Simulation.applySimulationConfigFromFile()
    Config.resultsFolder = "planning-horizon"

    planning_steps = 1
    alpha = 0
    beta = 0

    planning_step_horizons = [50, 100, 150, 200, 250, 300]

    for planning_step_horizon in planning_step_horizons:
        for random_seed in range(50):

            print "########################"
            print "########################"
            print "random_seed: " + str(random_seed)
            print "planning_step_horizon: " + str(planning_step_horizon)
            print "########################"
            print "########################"

            simulation_horizon = planning_steps * planning_step_horizon

            Simulation.customizeSimulationConfig(
                random_seed = random_seed,
                simulation_horizon = simulation_horizon,
                adaptation_period = simulation_horizon,
                planning_period = simulation_horizon,
                planning_step_horizon = planning_step_horizon,
                planning_steps = planning_steps,
                alpha = alpha,
                beta = beta
            )

            Boot.start(0, False, sumoUseGUI)

