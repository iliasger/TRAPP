from app.adaptation.strategies import get_adaptation_stategy


def perform_adaptation(tick):

    print "*******************"
    print "Starting adaptation at tick " + str(tick)
    print "*******************"

    strategy = get_adaptation_stategy()

    monitor_data = strategy.monitor()
    if monitor_data:
        analysis_data = strategy.analyze(monitor_data)
        if analysis_data:
            plan_data = strategy.plan(analysis_data)
            if plan_data:
                strategy.execute(plan_data)

    print "*******************"