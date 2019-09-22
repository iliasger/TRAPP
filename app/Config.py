######################################
####### GENERAL CONFIGURATION ########
######################################

# True if we want to use the SUMO GUI
sumoUseGUI = True  # False

debug = False  # False

# which seed to be used in the random functions, for repeatability
random_seed = 10

epos_jar_path = "C:\\Users\\Shoaib\\Documents\\Lectures\\Thesis\\docs\\release-0.0.1\\epos-tutorial.jar"

######################################
#### CONFIGURATION OF SIMULATION #####
######################################

# The network config (links to the net) we use for our simulation
sumoConfig = "./app/map/eichstaedt.sumo.cfg"

# The network net we use for our simulation
sumoNet = "./app/map/eichstaedt.net.xml"

# The total number of cars we use in our simulation
totalCarCounter = 1000

# How long the simulation will run
# simulation_horizon = 300
simulation_horizon = 1400

######################################
##### CONFIGURATION OF PLANNING ######
######################################

# whether the simulation should start with an EPOS invocation
start_with_epos_optimization = False

# How frequently EPOS planning will be invoked (runtime-configurable parameter)
# planning_period = 100
# planning_period = 600
# planning_period = 200
planning_period = 9000

# the number of steps to look in the future while planning
# planning_steps = 2
planning_steps = 2

# how long a planning step should be
planning_step_horizon = 300

# double from [0, 1], unfairness
alpha = 1

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
# adaptation_period = 600
# adaptation_period = 200
adaptation_period = 9000

# the actual adaptation logic. Possible values: "load_balancing", "avoid_overloaded_streets", "tune_planning_resolution"
#adaptation_strategy = "load_balancing"
adaptation_strategy = "avoid_overloaded_streets"


######################################
##### CONFIGURATION OF ACCIDENT ######
######################################

restrictTrafficFlow = True              # if true then traffic will flow from source to target nodes as defined below
trafficSource = [[(3951, 161, 80), (3890, 314, 80), (4340,501,60), (3237,1246,70), (3099, 1078, 30), (2966, 501, 50), (3730, 1486, 50),(4355, 18, 50), (4088, 868,50), (4447, 371, 80), (2981, 1501, 50)], [(2645,2762,50), (2540,2327,50,), (2540,2012, 80), (3052,1822,50)], [(1147, 2949, 50), (1693, 2673, 40), (1795,2555,40)]]       # region where traffic will generate or start from. Tuple: (x-position, y-position, radius) on the map
trafficTarget = [[(446, 1627, 80), (7, 2155, 50), (198, 2028, 50)], [(2167, 800, 50), (1883, 878, 50)], [(2921, 456, 50), (2987, 507, 50)]] #(568, 2659, 80)         # Target of the traffic. Tuple: (x-position, y-position, radius) on the map
triggerAccident = False                  # Trigger accident scenario or not. Below parameters will be considered if this value is True
accidentFrom = 200                      # simulation tick where accident will happen. Block the road in this case for example
accidentTill = 500                      # simulation tick when the accident is cleared. Unblock the road in this case for example
blockLanes = ["-2788#0_0", "-2788#0_1"] # list of lane ids to block when accident happen
blockEdges = ["-2788#0"]
blockedLaneSpeed = 0.5