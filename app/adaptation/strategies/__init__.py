import app.Config as Config
from app.adaptation.strategies.AvoidOverloadedStreets import AvoidOverLoadedStreets
from app.adaptation.strategies.LoadBalancing import LoadBalancing
from app.adaptation.strategies.TunePlanningResolution import TunePlanningResolution
from app.adaptation.strategies.Beta import Beta


def get_adaptation_stategy(tick):

    if Config.adaptation_strategy == "load_balancing":
        return LoadBalancing(tick)
    elif Config.adaptation_strategy == "avoid_overloaded_streets":
        return AvoidOverLoadedStreets(tick)
    elif Config.adaptation_strategy == "tune_planning_resolution":
        return TunePlanningResolution(tick)