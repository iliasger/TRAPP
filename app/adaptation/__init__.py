from app.adaptation.strategies import get_adaptation_stategy
from app.adaptation.Knowledge import time_of_last_adaptation

def perform_adaptation(tick):

    print "*******************************"
    print "Starting adaptation at tick " + str(tick)
    print "*******************************"

    time_of_last_adaptation = tick
    strategy = get_adaptation_stategy(tick)
    print "Invoking strategy: " + str(strategy.__class__.__name__)

    monitor_data = strategy.monitor()
    if monitor_data:
        analysis_data = strategy.analyze(monitor_data)
        if analysis_data:
            plan_data = strategy.plan(analysis_data)
            if plan_data:
                strategy.execute(plan_data)

    print "*******************************"