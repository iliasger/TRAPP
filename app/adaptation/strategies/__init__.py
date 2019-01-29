import app.Config as Config
from app.adaptation.strategies.AvoidOverloadedStreets import AvoidOverLoadedStreets
from app.adaptation.strategies.LoadBalancing import LoadBalancing
from app.adaptation.strategies.TunePlanningResolution import TunePlanningResolution


def get_adaptation_stategy():

    if Config.adaptation_strategy == "load_balancing":
        return LoadBalancing()
    elif Config.adaptation_strategy == "avoid_overloaded_streets":
        return AvoidOverLoadedStreets()
    elif Config.adaptation_strategy == "tune_planning_resolution":
        return TunePlanningResolution()