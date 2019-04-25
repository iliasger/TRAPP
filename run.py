from app import Boot
import sys
from app.Config import sumoUseGUI
from app.simulation.Simulation import Simulation

# this starts the simulation (int parameters are used for parallel mode)
if __name__ == "__main__":
    try:
        processID = int(sys.argv[1])
    except:
        processID = 0
    if processID is not None:
        parallelMode = False
        # Starting the application
        Simulation.applySimulationConfigFromFile()
        Boot.start(processID, parallelMode, sumoUseGUI)
