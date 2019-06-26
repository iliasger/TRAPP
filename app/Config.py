######################################
####### GENERAL CONFIGURATION ########
######################################

# True if we want to use the SUMO GUI
sumoUseGUI = True  # False

debug = False  # False

# which seed to be used in the random functions, for repeatability
random_seed = 1

epos_jar_path = "C:\\Users\\Shoaib\\Documents\\Lectures\\Thesis\\docs\\release-0.0.1\\epos-tutorial.jar"

######################################
#### CONFIGURATION OF SIMULATION #####
######################################

# The network config (links to the net) we use for our simulation
sumoConfig = "./app/map/eichstaedt.sumo.cfg"

# The network net we use for our simulation
sumoNet = "./app/map/eichstaedt.net.xml"

# The total number of cars we use in our simulation
totalCarCounter = 300

# How long the simulation will run
# simulation_horizon = 300
simulation_horizon = 1000

######################################
##### CONFIGURATION OF PLANNING ######
######################################

# whether the simulation should start with an EPOS invocation
start_with_epos_optimization = False

# How frequently EPOS planning will be invoked (runtime-configurable parameter)
planning_period = 100
# planning_period = 600

# the number of steps to look in the future while planning
# planning_steps = 2
planning_steps = 1

# how long a planning step should be
planning_step_horizon = 50

# double from [0, 1], unfairness
alpha = 0

# double from [0, 1], selfishness or local objective
beta = 1
# unfairness + selfishness <= 1
# alpha*unfairness + beta*local_cost + (1-alpha-beta)*global_costs

# Suggested values : "XCORR", VAR", "RSS", "RMSE"
globalCostFunction="VAR"

######################################
#### CONFIGURATION OF ADAPTATION #####
######################################

# how often adaptation should be triggered
# adaptation_period = 100
adaptation_period = 600

# the actual adaptation logic. Possible values: "load_balancing", "avoid_overloaded_streets", "tune_planning_resolution"
#adaptation_strategy = "load_balancing"
adaptation_strategy = "avoid_overloaded_streets"


######################################
##### CONFIGURATION OF ACCIDENT ######
######################################

restrictTrafficFlow = False              # if true then traffic will flow from source to target nodes as defined below
trafficSource = (4025, 532, 80)         # region where traffic will generate or start from. Tuple: (x-position, y-position, radius) on the map
trafficTarget = (568, 2659, 80)         # Target of the traffic. Tuple: (x-position, y-position, radius) on the map
triggerAccident = True                  # Trigger accident scenario or not. Below parameters will be considered if this value is True
accidentFrom = 200                      # simulation tick where accident will happen. Block the road in this case for example
accidentTill = 600                      # simulation tick when the accident is cleared. Unblock the road in this case for example
blockLanes = ["-2788#0_0", "-2788#0_1"] # list of lane ids to block when accident happen