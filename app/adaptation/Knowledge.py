# These parameters can be changed at runtime by the self-adaptation logic
# for explanation of each parameter check app.Config.py

planning_period = None
planning_steps = None
planning_step_horizon = None
alpha = None
beta = None
globalCostFunction=None

# This parameter should only be queried by the adaptation logic, but not changed

time_of_last_EPOS_invocation = 0
time_of_last_adaptation = 0