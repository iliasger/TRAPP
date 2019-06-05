from app.adaptation.strategies import get_adaptation_stategy
from app.adaptation.Knowledge import time_of_last_adaptation
from colorama import Fore
from app.logging import info

def perform_adaptation(tick):

    info("*******************************", Fore.CYAN)
    info("Starting adaptation at tick " + str(tick), Fore.CYAN)
    info("*******************************", Fore.CYAN)

    strategy = get_adaptation_stategy(tick)
    info("Invoking strategy: " + str(strategy.__class__.__name__), Fore.CYAN)

    monitor_data = strategy.monitor()
    if monitor_data:
        analysis_data = strategy.analyze(monitor_data)
        if analysis_data:
            plan_data = strategy.plan(analysis_data)
            if plan_data:
                strategy.execute(plan_data)

    info("*******************************", Fore.CYAN)