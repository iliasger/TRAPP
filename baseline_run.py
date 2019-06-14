from app import Boot
import sys
import app.Config as Config
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

        Simulation.customizeSimulationConfig(
            random_seed = processID,
            log_baseline_result = True,
            log_overheads = False,
            log_utilizations = False,
            do_adaptation = False,
            do_EPOS_planning = False,
            multiple_car_routes = True
        )
        Boot.start(processID, parallelMode, Config.sumoUseGUI)
