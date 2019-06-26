import os, sys

sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), "tools"))

from app.logging import info
from app.routing.CustomRouter import CustomRouter
from app.network.Network import Network
from app.simulation.Simulation import Simulation
# from app.simulation.baseline1 import Simulation
# from app.simulation.baseline2 import Simulation
# from app.simulation.baseline3 import Simulation
from colorama import Fore
from sumo import SUMOConnector, SUMODependency
import Config
import traci, sys
import random


def start(processID, parallelMode,useGUI):

    random.seed(Config.random_seed)

    """ main entry point into the application """
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

    # After the network is loaded, we init the router
    CustomRouter.init()
    # Start sumo in the background
    SUMOConnector.start()
    info("\n# SUMO-Application started OK!", Fore.GREEN)
    # Start the simulation
    Simulation.start()
    
    # Simulation ended, so we shutdown
    info(Fore.RED + '# Shutdown' + Fore.RESET)
    traci.close()
    sys.stdout.flush()
    return None
