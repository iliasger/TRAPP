import os, sys

sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), "tools"))

from app.logging import info
from app.routing.CustomRouter import CustomRouter
from app.network.Network import Network
from app.districts.Districts import Districts
from app.simulation.Simulation import Simulation
from colorama import Fore
from sumo import SUMOConnector, SUMODependency
import Config
import traci, sys
import random
from app.adaptation import Knowledge


def start(processID, parallelMode, useGUI):

    print "Config.random_seed: " + str(Config.random_seed)
    random.seed(Config.random_seed)

    """ main entry point into the application """
    Config.processID = processID
    Config.parallelMode = parallelMode
    Config.sumoUseGUI = useGUI

    info('#####################################', Fore.CYAN)
    info('#        Starting TRAPP v0.1        #', Fore.CYAN)
    info('#####################################', Fore.CYAN)

    # Check if sumo is installed and available
    SUMODependency.checkDeps()
    info('# SUMO-Dependency check OK!', Fore.GREEN)

    # Load the sumo map we are using into Python
    Network.loadNetwork()
    info(Fore.GREEN + "# Map loading OK! " + Fore.RESET)
    info(Fore.CYAN + "# Nodes: " + str(Network.nodesCount()) + " / Edges: " + str(Network.edgesCount()) + Fore.RESET)
    info(Fore.CYAN + "# Passenger Edges: " + str(len(Network.passenger_edges)) + Fore.RESET)

    Districts.loadDistricts()
    info(Fore.GREEN + "# Districts loading OK! " + Fore.RESET)
    info(Fore.CYAN + "# Districts: " + str(Districts.number_districts) + Fore.RESET)

    #if district files are created the simulation is not run
    if (not Config.do_gridding):
        # After the network is loaded, we init the router
        CustomRouter.init()
        # Start sumo in the background
        SUMOConnector.start()

        info("\n# SUMO-Application started OK!", Fore.GREEN)
        # Start the simulation

        print "Knowledge.planning_steps: " + str(Knowledge.planning_steps)
        print "Knowledge.planning_step_horizon: " + str(Knowledge.planning_step_horizon)

        Simulation.start()
        # Simulation ended, so we shutdown


        info(Fore.RED + '# Shutdown' + Fore.RESET)
        traci.close()

    else:
        info(Fore.RED + '# Shutdown' + Fore.RESET)

    sys.stdout.flush()
    return None
